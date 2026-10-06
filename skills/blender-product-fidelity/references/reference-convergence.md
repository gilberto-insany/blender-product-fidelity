# Reference convergence and existing-model repair

Use for reconstruction from product references, especially after a user reports repeated mismatches. Read the actual images; a prose brief or an earlier agent's statement is not visual verification.

## Establish evidence and the current baseline

- Locate the current working `.blend`, reference pack and latest user corrections. The latest filename is not necessarily the approved model. Preserve a versioned baseline and any approved features; do not restart the whole object without a demonstrated structural reason.
- Use original photos, footage and reliable drawings as evidence. Treat generated technical sheets as illustrative hypotheses, never as proof of unseen parts or dimensions. Where sources conflict, resolve product variant and perspective first.
- Maintain a compact project checklist: feature or region, source image/frame, expected shape or attachment, current discrepancy, verification view, and status (observed, inferred, unresolved, verified). Update the existing checklist instead of duplicating it. Prioritize identity-defining form and missing components over microtexture.

## Component evidence contract

Extend the existing project checklist for each visible product feature with its source crop, physical location, outline/profile, recess or protrusion, attachment, material and verification views. Track two separate facts: the observed form and the confirmed function. A circular window can have a well-supported shape while its sensor type remains unknown.

- Reproduce observed construction: an opening needs a rim and believable depth or backing; a button needs the observed seat, clearance and height; an optical window needs its visible surround and optical surface; a hinge needs the demonstrated joint rather than an invented socket. Use geometry for silhouette and depth, and texture for appropriate microdetail. Do not add unseen mechanisms simply to make a feature seem functional.
- Never substitute arbitrary black discs, generic slots, floating capsules or decorative meshes for reference-supported components. Do not mirror asymmetric controls, branding or cable placement without evidence. Check both underside and inner faces when sources show them.
- Preserve exact visible inscriptions and their position, orientation and surface application. Treat a cable and its strain relief as part of the product when required by the current reference/configuration. New user corrections supersede older exclusions.
- Separate **observed but modeled incorrectly** from **not established by evidence**. The former remains an open correction; the latter remains an explicitly unresolved hypothesis. A successful mesh audit does not close either category.
- Accept a corrected feature only when a matched detail comparison and another relevant angle show its shape and attachment without hiding them in shadows. Record the visible result, not only the code or object count.
- Generated guide images may explore finish or communicate a proposed reconstruction. Keep them separate from original references and never use their invented details, consistent-looking views or sharpness as evidence. When the user requests only guide images, do not silently modify the Blender model.

## Compare before correcting

Match the reference's camera orientation, perspective, crop and object scale as closely as the evidence permits. Show side-by-side comparisons and, when alignment is meaningful, an overlay of silhouettes or landmarks. Do not warp either image to hide discrepancies. Do not claim dimensional accuracy from an uncalibrated perspective image.

Separate the possible causes: geometry, camera, missing component, material, or lighting. Record the mismatch and change the relevant cause. In particular, broad reflections can make black surfaces look gray; inspect lighting, roughness and exposure before changing the underlying color.

## Progress through visible proofs

- **Form:** low-cost, clearly lit views reveal contour, thickness, curvature, part transitions and negative spaces. Model real continuity and seams; hide neither incorrect joins with darkness nor irregular geometry with smoothing alone.
- **Components:** use detail crops to check camera surrounds, controls, openings, logos and attachments. Each visible component needs the right placement, scale and shape. Do not infer the function of a hole from its appearance alone. Inspect cords and knots for smooth curves, believable routing, contact and intersections.
- **Appearance:** use low-sample Cycles to test surface finish, texture scale, transparency and black-level separation after the form passes. Do not use Eevee layout images as final material evidence.
- **Multiple views:** inspect every requested delivery angle in preview; disclose angles without original reference coverage. For each significant correction, recheck the local close-up and another view that can expose regressions. Keep camera and lighting stable when isolating a geometry change.

Keep previews roughly 1000–1500 px for form and up to 2K for appearance as useful starting points. Retain high-quality source references and use close crops or higher-resolution proofs when small details are unresolved. Low preview resolution must not become lower modeling fidelity.

## Resume an existing project

Temporarily defer new final-render batches while known fidelity issues remain. Do not terminate a running render or overwrite its output without authorization. Inspect the current model before applying previous correction scripts; they may reintroduce earlier defects or overwrite manual changes. Rebuild a local surface when repeated patches have made it irregular rather than accumulating modifiers or control points without diagnosis.

Report the comparison images, concrete corrections and remaining uncertainties. A successful script, audit, smooth viewport or high-resolution image is not a fidelity pass. If user approval is requested, stop at the agreed preview checkpoint; otherwise progress within the existing authorization after evidence passes. Setup-only deliveries remain prepared when render validation was not authorized. For final render quality and handoff status, use quality-gates.md and delivery-validation.md.
