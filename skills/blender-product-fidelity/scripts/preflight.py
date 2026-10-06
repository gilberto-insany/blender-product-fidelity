"""Read-only Blender preflight. No render, save, device refresh, or automatic repair.
Run: blender -b file.blend --python preflight.py -- --frames 1,75,310 --json report.json
Evaluates viewport dependency graph; render-only modifiers and instances need review.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy


def inspect_scene(scene, frames):
    issues = []
    def flag(code, severity, detail, **evidence):
        issues.append(dict(code=code, severity=severity, detail=detail, **evidence))
    r = scene.render
    cy = getattr(scene, 'cycles', None)
    fps = r.fps / r.fps_base
    frame_count = len(range(scene.frame_start, scene.frame_end + 1, scene.frame_step))
    report = dict(schema_version=1, blender_version=bpy.app.version_string,
                  file=bpy.data.filepath, scene=scene.name,
                  resolution=[r.resolution_x, r.resolution_y, r.resolution_percentage],
                  effective_resolution=[int(r.resolution_x*r.resolution_percentage/100), int(r.resolution_y*r.resolution_percentage/100)],
                  fps=fps, frame_range=[scene.frame_start, scene.frame_end], frame_step=scene.frame_step,
                  output_frame_count=frame_count, timeline_duration_seconds=(scene.frame_end-scene.frame_start+1)/fps,
                  engine=r.engine, output=dict(path=r.filepath, format=r.image_settings.file_format,
                  color_mode=r.image_settings.color_mode, overwrite=r.use_overwrite),
                  render_execution_verified=False, frames=[], issues=issues,
                  limitations=['Viewport dependency graph, not a render geometry pass.',
                    'Duplicate matching is exact and topology-order dependent; candidates are not automatic deletions.',
                    'No general intersection, collision, temporal flicker or visual fidelity proof.',
                    'Visibility uses object and ancestor collection render flags; view-layer exclusions and instances need manual review.'])
    if not scene.camera: flag('missing_camera','error','No active render camera.')
    if scene.frame_end < scene.frame_start: flag('invalid_range','error','End frame precedes start frame.')
    if r.resolution_percentage != 100: flag('scaled_resolution','review','Confirm effective dimensions match the delivery request.')
    if frame_count > 1 and r.image_settings.file_format == 'FFMPEG':
        flag('direct_video','review','Long video renders are harder to resume than an image sequence.')
    if cy and r.engine == 'CYCLES':
        report['cycles'] = {k:getattr(cy,k,None) for k in ('device','samples','adaptive_threshold','adaptive_min_samples','use_denoising','denoiser','use_auto_tile','tile_size')}
        addon = bpy.context.preferences.addons.get('cycles')
        prefs = addon.preferences if addon else None
        report['device_configuration'] = dict(backend=getattr(prefs,'compute_device_type',None),
            cached_devices=[dict(name=d.name,type=d.type,enabled=d.use) for d in getattr(prefs,'devices',[])])
        if cy.device == 'CPU': flag('cpu_selected','review','CPU selected; compare against available hardware before a long render.')
        if cy.device == 'GPU' and not any(d['enabled'] and d['type'] != 'CPU' for d in report['device_configuration']['cached_devices']):
            flag('gpu_unverified','review','No enabled GPU in cached preferences; inspect devices in the render environment.')
    for im in bpy.data.images:
        if im.source != 'FILE' or not im.filepath or im.packed_file: continue
        path = bpy.path.abspath(im.filepath, library=im.library)
        if not Path(path).is_file(): flag('missing_image','error','Unpacked image file is missing.',image=im.name,path=path)
    # Collection flags are independent of viewport hide flags. Multiple memberships can keep an object renderable.
    render_members = set()
    def visit(col, hidden=False):
        hidden = hidden or col.hide_render
        if not hidden: render_members.update(o.name for o in col.objects)
        for child in col.children: visit(child, hidden)
    visit(scene.collection)
    initial_frame, initial_subframe = scene.frame_current, scene.frame_subframe
    try:
        for frame in frames:
            scene.frame_set(frame)
            dg = bpy.context.evaluated_depsgraph_get()
            meshes, candidates = [], {}
            for obj in scene.objects:
                if obj.type != 'MESH' or obj.hide_render or obj.name not in render_members: continue
                evaluated = obj.evaluated_get(dg)
                mesh = evaluated.to_mesh()
                try:
                    mesh.calc_loop_triangles()
                    coords = [tuple(v.co) for v in mesh.vertices]
                    faces = [tuple(p.vertices) for p in mesh.polygons]
                    used = {i for e in mesh.edges for i in e.vertices}
                    used.update(i for face in faces for i in face)
                    edges = {}
                    for face in faces:
                        for i, a in enumerate(face):
                            key = tuple(sorted((a,face[(i+1)%len(face)])))
                            edges[key] = edges.get(key,0)+1
                    zero = sum(p.area == 0 for p in mesh.polygons)
                    nonfinite = sum(not all(math.isfinite(x) for x in co) for co in coords)
                    duplicate_faces = len(faces)-len({tuple(sorted(f)) for f in faces})
                    row = dict(name=obj.name, source_vertices=len(obj.data.vertices), evaluated_vertices=len(coords),
                        evaluated_triangles=len(mesh.loop_triangles), zero_area_faces=zero, nonfinite_vertices=nonfinite,
                        loose_vertices=len(coords)-len(used), duplicate_faces=duplicate_faces,
                        boundary_edges=sum(n==1 for n in edges.values()), nonmanifold_edges=sum(n>2 for n in edges.values()),
                        materials=[m.name if m else None for m in obj.data.materials])
                    meshes.append(row)
                    for count, code in [(zero,'zero_area_faces'),(duplicate_faces,'duplicate_faces'),(nonfinite,'nonfinite_vertices')]:
                        if count: flag(code,'error' if code=='nonfinite_vertices' else 'review','Inspect evaluated geometry before repair.',object=obj.name,frame=frame,count=count)
                    if any(m.show_viewport != m.show_render for m in obj.modifiers):
                        flag('modifier_visibility_mismatch','review','Evaluated viewport geometry differs from render configuration.',object=obj.name,frame=frame)
                    signature = hashlib.sha256(repr((coords,faces,[tuple(v) for v in evaluated.matrix_world])).encode()).hexdigest()
                    candidates.setdefault(signature,[]).append(obj.name)
                finally: evaluated.to_mesh_clear()
            duplicates = [v for v in candidates.values() if len(v)>1]
            for group in duplicates: flag('coincident_meshes','review','Exact coincident mesh candidate; inspect materials and purpose.',frame=frame,objects=group)
            report['frames'].append(dict(frame=frame, evaluated_triangles=sum(m['evaluated_triangles'] for m in meshes),
                mesh_objects=len(meshes), meshes=sorted(meshes,key=lambda m:-m['evaluated_triangles']), coincident_candidates=duplicates))
    finally:
        scene.frame_set(initial_frame,subframe=initial_subframe)
    report['status'] = 'errors_found' if any(x['severity']=='error' for x in issues) else 'review_needed' if issues else 'no_automated_findings'
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frames',help='Comma-separated integer frames; default current frame only.')
    parser.add_argument('--json',type=Path,help='New JSON path (refuses overwrite).')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    frames=list(dict.fromkeys(map(int,args.frames.split(',')))) if args.frames else [bpy.context.scene.frame_current]
    result=inspect_scene(bpy.context.scene,frames)
    payload=json.dumps(result,indent=2,allow_nan=False)
    if args.json:
        with args.json.open('x') as stream: stream.write(payload+'\n')
    print(payload)

if __name__=='__main__': main()
