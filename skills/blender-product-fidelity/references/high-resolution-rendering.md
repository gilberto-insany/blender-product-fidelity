# High-Resolution Product Rendering

Use this guide for photoreal final renders, 4K/8K requests, and archival master images. The goal is a converged image with verifiable output properties, not merely a large file or a high sample count.

## Stage the work

1. **Measured blockout:** solve overall dimensions, part spacing, silhouette, camera height, azimuth, elevation, and focal compression.
2. **Low-cost preview:** use Eevee for layout or low-sample Cycles for appearance. Start around 1000–1500 px on the long edge, preserving final aspect ratio. Compare framing, silhouette, negative spaces, and lighting direction against the original reference using the reference-convergence guide.
3. **Geometry/material proof:** render a close crop around the hardest surface transition, branding edge, display, seam, or condensation area.
4. **Hero validation:** start around 2K after shape and component checks pass; use 4K when needed to resolve a fidelity question. Correct remaining camera, material, lighting, and composition issues. Do not launch a full multi-angle 4K batch while geometry discrepancies remain. Render close crops at final pixel density where necessary to check small details.
5. **Second correction pass:** recheck contact shadows, bevel highlights, dark-part separation, labels, roughness variation, and background values.
6. **Final master:** render at the declared final dimensions only after the validation image passes.

Preserve approved intermediate files. A failed final render must not replace the latest known-good `.blend` or image.

## Define the output precisely

- State exact width, height, orientation, and aspect ratio. “8K” alone is ambiguous.
- For an 8K master, use a 7680-pixel long edge and derive the other dimension from the approved camera aspect ratio. For example, 16:9 landscape is 7680×4320; 4:5 portrait is 6144×7680.
- Do not distort the camera composition to fit a preset. Preserve the approved aspect ratio unless the user requests a crop.
- Save the master as 16-bit PNG for a compact finished image or OpenEXR for maximum grading/compositing latitude. Use 32-bit EXR only when the workflow requires it.
- Treat JPEG as a review or delivery derivative, never as the only master.
- Use an absolute, versioned output path and ensure enough disk space is available before a long render.

## Cycles convergence profile

Use these as starting points and convergence caps, not as proof of quality:

- Engine: Cycles.
- Device: verified GPU Compute when available; CPU is an acceptable fallback. Record which device actually rendered.
- Adaptive sampling: enabled.
- Noise threshold: about `0.01–0.006` for validation; `0.005` or lower for the final only when 100% crops show a benefit.
- Maximum samples: `512–1024` for many product scenes; increase only when important regions have not converged. A scene may finish earlier under adaptive sampling.
- Denoiser: OpenImageDenoise for the final. Inspect fine type, brushed metal, microtexture, droplets, and glossy edges for smearing.
- Color management: AgX. Choose a contrast look that preserves highlights and separates near-black materials instead of crushing them into absolute black.
- Light paths starting point: max bounces `8`, diffuse `4`, glossy `5`, transmission `6`, transparent `4`. Increase transmission or total bounces for glass, deep liquid, or nested transparent parts when inspection justifies it.

Avoid absolute-black product materials. Near-black plastics, anodized metal, rubber, and coated surfaces need distinct values, roughness, specular behavior, and readable edge reflections.

## Repeatable render command

The helper configures Cycles, adaptive sampling, OpenImageDenoise, AgX when available, output format, bit depth, exact dimensions, and GPU selection with an automatic CPU fallback.

```bash
BLENDER_BIN="/Applications/Blender.app/Contents/MacOS/Blender"
"$BLENDER_BIN" --background /absolute/path/product_v12.blend \
  --python "${CODEX_HOME:-$HOME/.codex}/skills/blender-product-fidelity/scripts/render_product.py" -- \
  --output /absolute/path/renders/product_v12_final.png \
  --long-edge 7680 \
  --samples 1024 \
  --threshold 0.005 \
  --device AUTO \
  --save-blend /absolute/path/product_v12_final.blend
```

Use `--width` and `--height` instead of `--long-edge` when the exact dimensions are already known. Use `--format OPEN_EXR --color-depth 16` for a half-float EXR master. Run `render_product.py --help` after Blender's `--` separator for all options.

## Preflight before the master

- Confirm the correct scene and render camera are active.
- Confirm all linked assets, fonts, textures, color spaces, and modifiers resolve from the saved file.
- Confirm the camera aspect and resolution percentage are correct.
- Confirm the output path is absolute, versioned, and writable.
- Save a versioned `.blend` before rendering.
- Record engine, device, dimensions, format, bit depth, samples, threshold, denoiser, and color transform.

## Inspect the result

Review both the complete frame and 100% crops of:

- silhouette and bevel highlights;
- seams, gaps, keys, caps, labels, logos, and fine type;
- glossy dark materials and near-black separation;
- displays, glass, liquid, transmission, and reflective metal;
- microtexture, condensation, droplets, and contact shadows;
- residual noise, fireflies, denoiser smearing, banding, clipped highlights, and crushed shadows.

If the 2K/4K validation fails, correct the scene and repeat it. If the 8K render fails or the file cannot be inspected, report the result as WIP and preserve the last verified version.
