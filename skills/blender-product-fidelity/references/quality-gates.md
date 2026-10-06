# Product-render quality gates

Inspect the render at 100% scale and compare against the supplied references before delivery.

## Input sufficiency

- The prompt identifies the exact product/variant, deliverable, target camera, must-match features, and allowed approximations.
- The reference pack includes materially different views and detail crops for judged branding and signature construction.
- At least one known physical dimension or reliable ratio anchors the model when scale matters.
- Geometry evidence and art direction are labeled separately; variant conflicts and lens distortion are resolved or disclosed.
- A one-view reconstruction is labeled as a target-view match, not as verified on unseen surfaces.

## Geometry

- Silhouette, thickness, curvature and part transitions match the specific referenced product, not merely its product category. Compare aligned views; account for camera perspective before changing geometry.
- Every visible signature component is accounted for in the reference checklist, including attachment, position and shape. Unsupported hidden details remain marked as assumptions.
- A correction passes both its detail view and at least one other relevant view; smooth shading alone does not establish geometric fidelity.
- Grazing highlights are continuous and do not reveal faceting.
- Seams, lid, tab, opening, shoulders, and base read as manufactured parts.
- Requested embossing or debossing follows the surface, has consistent depth, rounded edges, and visible contact shadows.
- No floating, intersecting, or obviously planar branding on curved surfaces.

## Materials

- The body reads as the intended substrate and coating, not generic plastic.
- Roughness variation is subtle, scale-correct, and visible only where light reveals it.
- Near-black plastics, rubber, coated metal, and graphics remain distinct through measured value, roughness, specular response, relief, or localized finish; important product regions are not crushed into featureless absolute black.
- Colored metal edges read as coated or anodized metal rather than emissive neon.

## Condensation

- Droplets vary naturally in size, shape, density, and orientation.
- Large drops show surface tension and contact with the product.
- Some clustering and gravity behavior are visible.
- Water is optically transparent and reflects the studio; it is not gray or opaque.

## Composition and rendering

- Camera angle and focal length reproduce the intended visual language.
- Lighting reveals the product without flattening black materials.
- On a dark background, the contour and relevant details remain readable at every materially different angle. Backlight separates the product without clipped rims, unintended metallic response, gray graphics or excessive visibility of unfinished internals.
- The object is grounded or convincingly floating through its shadow and light relationship.
- A 2K/4K hero validation passed before an expensive final master was launched.
- Final output uses Cycles when photorealism is requested, adaptive sampling, a verified render device, adequate convergence, denoising, and documented settings.
- The master has declared pixel dimensions and aspect ratio, 100% resolution scale, and a 16-bit PNG or OpenEXR output rather than JPEG-only delivery.
- The full frame and representative 100% crops are free from unacceptable residual noise, denoiser smearing, fireflies, banding, clipped highlights, crushed shadows, and lost microtexture.

## Animation and real-time derivatives

- For a continuous movement, camera, framing, orientation and light changes remain continuous across the complete path. Consecutive transition checks support this claim; isolated pose screenshots do not verify temporal smoothness. Intentional cuts remain valid when part of the requested direction.
- Display activation preserves timing, artwork and black levels behind the optical cover.
- Geometry/resource reporting identifies which curves, instances, render branches and passes were counted. Transfer size, geometric complexity and measured runtime performance are reported separately.
- A lightweight derivative preserves approved silhouette, functional details, cord routing and material identity at its own target viewing scale. Browser or viewport evidence is labeled by engine and does not certify photoreal Cycles output or untested phone performance.

If any major gate fails, present the result as a work-in-progress proof and continue iterating. A technically valid `.blend` or export is not evidence of visual fidelity. Apply the render-specific checks above only to the requested render deliverable; a real-time prototype follows [real-time delivery](realtime-delivery.md) instead of requiring a Cycles master.
