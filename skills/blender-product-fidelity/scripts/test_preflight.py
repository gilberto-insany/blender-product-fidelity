"""Regression fixtures. Run only in a disposable background factory-startup process."""
import importlib.util
from pathlib import Path
import bpy
assert bpy.app.background,'Tests must not run in an interactive user scene'
assert not bpy.data.filepath,'Use --factory-startup with no user .blend'
spec=importlib.util.spec_from_file_location('preflight',Path(__file__).with_name('preflight.py'))
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
s=bpy.context.scene
for obj in list(s.objects):bpy.data.objects.remove(obj,do_unlink=True)
s.render.engine='CYCLES';s.cycles.device='CPU';s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.frame_start=1;s.frame_end=20;s.frame_step=1
cam=bpy.data.objects.new('TestCamera',bpy.data.cameras.new('TestCamera'));s.collection.objects.link(cam);s.camera=cam
bpy.ops.mesh.primitive_cube_add();cube=bpy.context.object;cube.name='CleanCube'
s.frame_set(7,subframe=.25)
base=p.inspect_scene(s,[1,20])
assert base['frames'][0]['evaluated_triangles']==12
assert not any(i['severity']=='error' for i in base['issues'])
assert (s.frame_current,s.frame_subframe)==(7,.25)
assert any(i['code']=='cpu_selected' for i in base['issues'])
print('PASS clean mesh, CPU warning, frame restoration')
dup=cube.copy();s.collection.objects.link(dup);dup.name='Duplicate'
a=p.inspect_scene(s,[1]);assert any(i['code']=='coincident_meshes' for i in a['issues'])
dup.hide_render=True;dup.keyframe_insert('hide_render',frame=1);dup.hide_render=False;dup.keyframe_insert('hide_render',frame=10)
a=p.inspect_scene(s,[1,10]);assert not a['frames'][0]['coincident_candidates'];assert a['frames'][1]['coincident_candidates']
print('PASS coincident detection and animated visibility')
dup.hide_viewport=True
bpy.data.objects.remove(dup,do_unlink=True)
mesh=bpy.data.meshes.new('BadMesh');mesh.from_pydata([(0,0,0),(1,0,0),(2,0,0),(9,9,9)],[],[(0,1,2),(0,1,2)])
bad=bpy.data.objects.new('BadMesh',mesh);s.collection.objects.link(bad)
a=p.inspect_scene(s,[1]);row=next(x for x in a['frames'][0]['meshes'] if x['name']=='BadMesh')
assert row['zero_area_faces']==2 and row['duplicate_faces']==1 and row['loose_vertices']==1
print('PASS degenerate/duplicate faces and loose vertex')
bpy.data.objects.remove(bad,do_unlink=True)
mod=cube.modifiers.new('RenderOnly','SUBSURF');mod.show_viewport=False;mod.show_render=True
assert any(i['code']=='modifier_visibility_mismatch' for i in p.inspect_scene(s,[1])['issues'])
cube.modifiers.remove(mod)
print('PASS render modifier mismatch')
image=bpy.data.images.new('Missing',width=1,height=1);image.source='FILE';image.filepath='/nonexistent/preflight_fixture_texture.png'
s.camera=None;s.render.resolution_percentage=50
if hasattr(s.render.image_settings,'media_type'):s.render.image_settings.media_type='VIDEO'
s.render.image_settings.file_format='FFMPEG'
a=p.inspect_scene(s,[1]);codes={i['code'] for i in a['issues']}
assert {'missing_camera','missing_image','scaled_resolution','direct_video'}<=codes
assert a['effective_resolution']==[960,540] and a['status']=='errors_found'
print('PASS missing camera/asset, effective size, direct-video risk')
assert len([o for o in s.objects if o.type=='MESH'])==1
assert s.cycles.device=='CPU' and s.render.resolution_percentage==50
print('PASS no automatic repair or render-setting changes')
print('ALL SIX REGRESSION GROUPS PASSED')
