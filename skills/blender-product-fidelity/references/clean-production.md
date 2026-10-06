# Clean production and optimization without fidelity loss

Read this reference when cleaning an approved scene, consolidating several assets into a production file, reducing memory use, or preparing a heavy groom for delivery. Preserve the user's selected resolution and approved appearance; cleanup is a derived deliverable, not permission to redesign.

## Source, history, and production

- Record the approved source's SHA-256 and work in a new file. Keep iterations, experiments, and alternatives in separate restorable files. A production file should contain final assets and their real dependencies rather than every historical generation.
- Audit reverse references before deleting anything. Old names, `hide_render`, `hide_viewport`, and collection exclusion do not prove that data is unused: Geometry Nodes, curve surfaces, deformation, constraints, drivers, instances, light linking, or active collections may consume it.
- Inventory objects, raw and evaluated curve/point counts, modifiers, attributes, material graphs, packed images, and external files. Remove only verified candidates and their unused data. Avoid broad prefix deletion or an unaudited recursive purge.
- Preserve editability. When a static cache is necessary, keep it in an identified copy, prove its fidelity, and state which deformation or editing capabilities are lost.
- Keep a restorable source and a deletion/change manifest. Confirm the original hash after saving and reopen the derived file with script auto-execution disabled. Audit dependencies rather than assuming packing makes a file self-contained.

## Fidelity evidence

Compare active curve attribute hashes (positions, radii, UVs and surface links), Geometry Nodes controls, materials and their connections before and after cleanup. Preserve geometry, pose, lighting, camera, frame, color management, sampling, passes and output settings.

When renders are authorized, run A/B tests with the same camera, framing, seed, frame/subframe, resolution, samples, adaptive minimum/threshold, denoiser and passes. Normalize a packed background's domain identically in both tests. Compare decoded pixels at the original bit depth, including alpha; an 8-bit thumbnail is not an RGBA16 comparison. Label exact pixel equivalence separately from visual equivalence. If pixels differ, isolate the change before accepting it.

Do not silently reduce density, strand length/radius/segments, sampling quality, or final resolution to claim optimization. Test BVH changes separately and retain them only when measured performance and fidelity evidence support the change.

## Budget microgeometry before building it

Choose the representation for the closest authorized view, output size and workload before generating hundreds of strands. A still macro, a long animation and a real-time onboarding can need different derivatives of the same approved product.

- Estimate projected strand diameter, weave spacing and silhouette contribution at the closest camera. Use texture, normal/bump or restrained displacement for surface detail that does not need separate geometry at that scale. Physical fibers can be justified by visible silhouette, depth, occlusion or macro optical behavior; keep density local to that need.
- Build and measure a small representative section before multiplying it. Curve sampling, bevel cross-section and strand count multiply: approximately `strands × longitudinal segments × radial segments × 2` triangles for simple evaluated tubes, before caps or extra modifiers. Actual evaluation remains the authority.
- Inventory raw control points and evaluated triangles, including curves, instances and render-only branches. A mesh-only report or simplified viewport can omit the dominant cost. If a complete evaluation is too costly, report the counted scope and estimate separately instead of claiming a complete scene total.
- Set a workload-specific budget from the intended device, camera, resolution and duration. File size, polygon count and peak render memory are different measurements; a compressed `.blend` can open quickly while generating tens of millions of triangles during rendering.
- Keep approved centerlines, knot crossings, gravity/drape, attachment position and visible rope thickness as the shape contract. A lightweight tube with directional weave can replace filament microgeometry in a derived animation or real-time asset. Verify front, rear and a grazing view so UV orientation, silhouette and crossings still read correctly.
- Preserve the approved detailed source when building a lighter representation. Distinguish data cleanup, lossless consolidation and a fidelity tradeoff. Required but expensive fibers are not orphan data. Do not silently strip a cord, redesign a knot or simplify an approved final render merely to meet a numerical target.
- A lighter viewport improves editing only; it does not certify lower render cost. If an animation is still heavy, prepare an appropriate derivative and validate it rather than relying only on hidden viewport collections. Compression reduces transfer size; it does not itself reduce evaluated triangles or GPU shading cost.

Read [real-time delivery](realtime-delivery.md) when the derivative will run in a browser or app.

## Avoid duplicate viewport and render evaluation

For a heavy single-scene render, prefer a clean background process that loads only the chosen scene with `bpy.data.libraries.load`, then renders it explicitly without activating its viewport graph. Avoid unnecessary `window.scene` switches, `frame_set`, `view_layer.update`, `evaluated_depsgraph_get`, or context overrides before rendering: these can build an additional evaluated groom. Copy frame/subframe by assignment into the lightweight context and target scene when required; the render operator may copy context time.

Use `use_persistent_data=False` when reuse has no measured benefit. Retain the other approved settings. For several assets, use independent scenes and load/render one at a time. The normal opening should be lightweight and usable without autorun scripts or required handlers, with real previews and clear scene selection.

For inspection or save-only setup, use `--disable-autoexec` and, when the installed version supports it, `--disable-depsgraph-on-file-load`. Verify CLI support locally. Temporarily excluding heavy curves from evaluation is acceptable only when their intended viewport/render state is restored before saving and validated after reopening.

A simplified viewport must be identified and separated through a native `Is Viewport` branch, preserving the complete render branch. Verify the full render result. Do not bake or freeze a simplified viewport evaluation as the final groom.

## Reusable variants

Add cameras for different angles instead of cloning an entire groom. Keep the approved camera as default. Extra camera presets need their own visual QA and must not be presented as verified views.

For alternate eye states, share the body/groom and switch only validated eye geometry reversibly. Do not expose a control for a state that does not exist yet. Dependency audits must include camera references, drivers, and lookups by name even when unused camera presets are excluded from the default-render comparison.

## Resource and resolution limits

Record test device, OS/Blender version, scene, settings, elapsed time and peak RSS, and distinguish cloud evidence from a Mac measurement. First use a small fidelity test and then a pilot at the requested intermediate size when authorized. A 512px or 1K pilot does not certify 2K/4K: image buffers, auxiliary passes, compositor and denoising can scale with pixel area.

Smaller tiles are an execution option at native resolution, not a resolution reduction; measure their memory and fidelity effects before recommending them. Do not promise that a large render fits a machine without testing that configuration.

Use a conservative workload-specific resource guard when available, avoid accidental concurrent Blender/render processes, and stop/report a guard failure rather than repeatedly launching the same expensive workload. Never terminate unrelated user processes or use `killall` to reclaim memory. Honor no-render and setup-only requests.
