# Blender product assets for real-time delivery

Read this when exporting an approved Blender product for Three.js, WebGL or an app. This covers the product asset, materials, lighting and motion fidelity; it does not prescribe an app framework or authorize publishing.

## Preserve the source and define the derivative

- Record the approved source/hash and export from a separate copy or unsaved working scene. Do not overwrite the user's render master to optimize an app.
- Retain silhouette, proportions, camera/controls/openings, approved cord routing and supplied display artwork. Use the [microdetail budget](clean-production.md#budget-microgeometry-before-building-it) to choose lighter surface representations. Simplifying or removing an entire cord is a design change, not routine data cleanup; require task authorization for that change.
- Identify which geometry is preserved, simplified, replaced by texture or omitted. Prefer linked geometry or material batching where compatible; preserve separate optical layers and components that animate independently. Do not batch away their controls.
- Establish consistent units and axes for the product, camera, lights, cord curves and shader thickness. Check a known dimension and front/up direction after import rather than assuming the exporter matches the product's construction axes.

## Reconstruct material response in the destination

- A glTF export does not guarantee preservation of Blender procedural weave, volume absorption, emission graphs or layered optics. Inspect actual imported materials and deliberately rebuild or bake unsupported features.
- Treat polished fumé polymer as a dielectric, with controlled transmission, thickness and attenuation. Simple alpha transparency can expose unfinished internals or make the shell look clear. Preserve the reference's slight internal visibility; do not increase metallic response to create stronger reflections.
- Keep the front cover, opaque black bezel and display distinct. Use the supplied bitmap/UVs on the display layer; animate its contribution independently of the cover. Verify off-state blacks and on-state color/sharpness, including unwanted reflections on the display material itself.
- Keep directional weave aligned along the cord and at a scale proportional to its diameter. Check bends and both sides of a knot for stretching, seams, flipped frames or changed crossings. A texture-based cord is a documented approximation to physical filaments.

## Light and animate the actual runtime asset

- For a dark launch/onboarding scene, provide deliberate rear/side separation and useful reflected sources, plus only enough fill to show required detail. Check front, side, rear and final hero poses. A light named "backlight" is not evidence that the product is readable.
- For a requested continuous sequence, sample one connected camera/framing path and continuous light controls. Carry across the intended duration, orbit and display activation; replace cuts only when the user requests continuity. Inspect transition intervals in the running implementation.
- Inspect the final runtime renderer and color management. A smaller payload or higher exposure alone cannot establish material fidelity. Compare source and destination at matched poses, and explain optical differences that remain.

## Measure what the user will actually load and run

- Report asset bytes and decoded geometry separately. Draco/mesh compression can reduce download size while leaving triangle count unchanged. Transmission, resolution, pixel ratio, lights and extra render passes can still dominate frame cost.
- Count cords and other generated runtime geometry in the scene total. Distinguish unique scene triangles from a render counter that includes repeated passes. Document any geometry or pass exclusions.
- Preserve silhouette and optical normals when applying LOD or quantization. Review the decoded compressed asset under grazing highlights and at the nearest allowed view, including camera rings, button edges, openings and display UVs.
- Test on the intended runtime/device when available, with representative poses and startup/steady-state costs. Desktop browser evidence does not certify phone memory or 60 fps. If no phone was tested, state that limit without inventing a guaranteed budget.
- In an onboarding integration, let the user continue/skip without waiting for the full sequence, respect reduced motion, pause unnecessary background updates and release renderer/texture/geometry resources when the screen unmounts. Keep a fallback for an unavailable 3D renderer. These are relevant integration criteria, not permission to expand unrelated app flows.

Deliver the editable asset/code and useful runtime previews. Label the result as prepared or runtime-verified according to actual evidence, independently of the source Blender render's verification state. Do not launch a full offline animation render when the user requested only a setup or interactive prototype.
