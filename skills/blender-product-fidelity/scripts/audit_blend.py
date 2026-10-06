import bpy
import json


scene = bpy.context.scene
cycles = getattr(scene, "cycles", None)
materials = []
for material in bpy.data.materials:
    materials.append({
        "name": material.name,
        "uses_nodes": bool(material.use_nodes),
        "node_count": len(material.node_tree.nodes) if material.use_nodes else 0,
    })

font_objects = [obj.name for obj in bpy.data.objects if obj.type == "FONT"]
droplets = [obj.name for obj in bpy.data.objects if obj.name.upper().startswith(("DROP", "DROPLET"))]
geometry_nodes = []
for obj in bpy.data.objects:
    for modifier in obj.modifiers:
        if modifier.type == "NODES":
            geometry_nodes.append({"object": obj.name, "modifier": modifier.name})

report = {
    "file": bpy.data.filepath,
    "engine": scene.render.engine,
    "cycles_samples": getattr(cycles, "samples", None),
    "denoise": getattr(cycles, "use_denoising", None),
    "resolution": [scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage],
    "camera": scene.camera.name if scene.camera else None,
    "object_count": len(bpy.data.objects),
    "mesh_count": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
    "font_objects": font_objects,
    "droplet_object_count": len(droplets),
    "geometry_nodes": geometry_nodes,
    "materials": materials,
    "render_path": scene.render.filepath,
}

warnings = []
if scene.render.engine != "CYCLES":
    warnings.append("Final realism render is not configured for Cycles")
if not scene.camera:
    warnings.append("Scene has no active camera")
if scene.render.resolution_percentage < 100:
    warnings.append("Render resolution percentage is below 100")
if not materials:
    warnings.append("Scene has no materials")
report["warnings"] = warnings

print("BLENDER_PRODUCT_AUDIT_BEGIN")
print(json.dumps(report, indent=2, sort_keys=True))
print("BLENDER_PRODUCT_AUDIT_END")
