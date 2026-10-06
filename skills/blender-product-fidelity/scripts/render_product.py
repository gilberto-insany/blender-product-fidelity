#!/usr/bin/env python3
"""Configure and render a versioned high-resolution product master in Blender."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import bpy


def script_args() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("value must be at least 1")
    return parsed


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be greater than 0")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a Cycles product master with explicit, auditable settings."
    )
    parser.add_argument("--output", required=True, help="Absolute output image path.")
    size = parser.add_mutually_exclusive_group(required=True)
    size.add_argument(
        "--long-edge",
        type=positive_int,
        help="Long edge in pixels; derives the other edge from the current camera aspect.",
    )
    size.add_argument(
        "--width",
        type=positive_int,
        help="Exact output width; requires --height.",
    )
    parser.add_argument("--height", type=positive_int, help="Exact output height.")
    parser.add_argument("--samples", type=positive_int, default=1024)
    parser.add_argument("--threshold", type=positive_float, default=0.005)
    parser.add_argument(
        "--device", choices=("AUTO", "GPU", "CPU"), default="AUTO"
    )
    parser.add_argument("--format", choices=("PNG", "OPEN_EXR"))
    parser.add_argument("--color-depth", choices=("16", "32"), default="16")
    parser.add_argument("--camera", help="Optional render camera object name.")
    parser.add_argument("--transparent", action="store_true")
    parser.add_argument(
        "--save-blend", help="Optional absolute path for the configured versioned .blend."
    )
    args = parser.parse_args(script_args())

    if args.width and not args.height:
        parser.error("--width requires --height")
    if args.height and not args.width:
        parser.error("--height requires --width")
    if args.color_depth == "32" and args.format == "PNG":
        parser.error("32-bit output requires --format OPEN_EXR")
    return args


def absolute_path(raw: str, label: str) -> Path:
    path = Path(os.path.expandvars(os.path.expanduser(raw)))
    if not path.is_absolute():
        raise ValueError(f"{label} must be an absolute path: {raw}")
    return path.resolve()


def output_format(args: argparse.Namespace, output: Path) -> str:
    if args.format:
        selected = args.format
    elif output.suffix.lower() == ".exr":
        selected = "OPEN_EXR"
    else:
        selected = "PNG"

    expected = ".exr" if selected == "OPEN_EXR" else ".png"
    if output.suffix.lower() != expected:
        raise ValueError(f"{selected} output path must end in {expected}")
    if selected == "PNG" and args.color_depth == "32":
        raise ValueError("PNG supports 8 or 16 bits here; use OPEN_EXR for 32-bit output")
    return selected


def resolve_dimensions(scene: bpy.types.Scene, args: argparse.Namespace) -> tuple[int, int]:
    if args.width:
        return args.width, args.height

    render = scene.render
    display_width = render.resolution_x * render.pixel_aspect_x
    display_height = render.resolution_y * render.pixel_aspect_y
    aspect = display_width / max(display_height, 1e-9)
    if aspect >= 1.0:
        return args.long_edge, max(1, round(args.long_edge / aspect))
    return max(1, round(args.long_edge * aspect)), args.long_edge


def select_camera(scene: bpy.types.Scene, camera_name: str | None) -> str:
    if camera_name:
        camera = bpy.data.objects.get(camera_name)
        if camera is None or camera.type != "CAMERA":
            raise ValueError(f"camera not found or not a camera: {camera_name}")
        scene.camera = camera
    if scene.camera is None:
        raise ValueError("the scene has no active render camera")
    return scene.camera.name


def configure_device(scene: bpy.types.Scene, requested: str) -> dict[str, object]:
    if requested == "CPU":
        scene.cycles.device = "CPU"
        return {"requested": requested, "selected": "CPU", "devices": ["CPU"]}

    addon = bpy.context.preferences.addons.get("cycles")
    if addon is None:
        if requested == "GPU":
            raise RuntimeError("Cycles preferences are unavailable; GPU cannot be verified")
        scene.cycles.device = "CPU"
        return {"requested": requested, "selected": "CPU", "devices": ["CPU"]}

    preferences = addon.preferences
    candidates = ["METAL", "OPTIX", "CUDA", "HIP", "ONEAPI"]
    if sys.platform == "darwin":
        candidates = ["METAL"]

    selected_type = None
    gpu_devices = []
    for compute_type in candidates:
        try:
            preferences.compute_device_type = compute_type
            preferences.get_devices()
        except (TypeError, ValueError, RuntimeError):
            continue
        found = [device for device in preferences.devices if device.type != "CPU"]
        if found:
            selected_type = compute_type
            gpu_devices = found
            break

    if not gpu_devices:
        if requested == "GPU":
            raise RuntimeError("GPU was requested, but no supported Cycles GPU was found")
        scene.cycles.device = "CPU"
        return {"requested": requested, "selected": "CPU", "devices": ["CPU"]}

    enabled_names = []
    gpu_ids = {device.id for device in gpu_devices}
    for device in preferences.devices:
        device.use = device.id in gpu_ids
        if device.use:
            enabled_names.append(device.name)
    scene.cycles.device = "GPU"
    return {
        "requested": requested,
        "selected": f"GPU:{selected_type}",
        "devices": enabled_names,
    }


def set_agx(scene: bpy.types.Scene) -> dict[str, str]:
    result = {
        "view_transform": scene.view_settings.view_transform,
        "look": scene.view_settings.look,
    }
    try:
        scene.view_settings.view_transform = "AgX"
        result["view_transform"] = scene.view_settings.view_transform
    except TypeError:
        pass

    for look in ("Medium High Contrast", "AgX - Medium High Contrast"):
        try:
            scene.view_settings.look = look
            result["look"] = scene.view_settings.look
            break
        except TypeError:
            continue
    return result


def configure_scene(
    scene: bpy.types.Scene, args: argparse.Namespace, output: Path, image_format: str
) -> dict[str, object]:
    camera_name = select_camera(scene, args.camera)
    width, height = resolve_dimensions(scene, args)
    render = scene.render

    scene.render.engine = "CYCLES"
    scene.cycles.samples = args.samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = args.threshold
    scene.cycles.use_denoising = True
    if hasattr(scene.cycles, "denoiser"):
        scene.cycles.denoiser = "OPENIMAGEDENOISE"

    scene.cycles.max_bounces = 8
    scene.cycles.diffuse_bounces = 4
    scene.cycles.glossy_bounces = 5
    scene.cycles.transmission_bounces = 6
    scene.cycles.transparent_max_bounces = 4

    render.resolution_x = width
    render.resolution_y = height
    render.resolution_percentage = 100
    render.pixel_aspect_x = 1.0
    render.pixel_aspect_y = 1.0
    render.filepath = str(output)
    render.use_file_extension = True
    render.film_transparent = args.transparent
    render.image_settings.file_format = image_format
    render.image_settings.color_depth = args.color_depth
    render.image_settings.color_mode = "RGBA" if args.transparent else "RGB"

    color = set_agx(scene)
    device = configure_device(scene, args.device)
    return {
        "scene": scene.name,
        "camera": camera_name,
        "engine": scene.render.engine,
        "device": device,
        "resolution": [width, height],
        "aspect_ratio": round(width / height, 6),
        "format": image_format,
        "color_depth": args.color_depth,
        "samples_cap": args.samples,
        "adaptive_threshold": args.threshold,
        "denoiser": getattr(scene.cycles, "denoiser", "enabled"),
        "color_management": color,
        "output": str(output),
    }


def main() -> None:
    args = parse_args()
    output = absolute_path(args.output, "--output")
    image_format = output_format(args, output)
    output.parent.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    summary = configure_scene(scene, args, output, image_format)

    if args.save_blend:
        blend_path = absolute_path(args.save_blend, "--save-blend")
        if blend_path.suffix.lower() != ".blend":
            raise ValueError("--save-blend path must end in .blend")
        blend_path.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
        summary["saved_blend"] = str(blend_path)

    print("PRODUCT_RENDER_PROFILE=" + json.dumps(summary, sort_keys=True))
    bpy.ops.render.render(write_still=True)
    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError(f"render did not create a non-empty output: {output}")
    print(
        "PRODUCT_RENDER_COMPLETE="
        + json.dumps(
            {"output": str(output), "bytes": output.stat().st_size}, sort_keys=True
        )
    )


if __name__ == "__main__":
    main()
