# Product modeling and material construction

## Curved packaging and relief

Use a revolved measured profile for rotational packaging. Include separate parts for seams, lid, tab, score, opening, base chime, and concavity so each can carry the correct metal response.

For editable curved branding:

1. Preserve hidden source artwork as Text or Curve objects.
2. Duplicate the source for the visible render object.
3. Convert only the visible duplicate when the modifier stack requires mesh geometry.
4. Conform it to the package with Shrinkwrap or a cylindrical deformation derived from the same body radius.
5. Give raised graphics a plausible height, typically 0.3–0.6 mm on packaging unless the reference indicates more.
6. Add a small physical bevel, normally 0.05–0.15 mm, so grazing light can reveal the edge.
7. Check for penetration, floating corners, inconsistent offsets, and incorrect normals.

For debossing, use a non-destructive Boolean or displacement workflow and preserve the cutter/source collection. Do not fake requested relief with a flat normal map in close hero views.

## Painted aluminum

Build the response in layers rather than assigning one glossy Principled shader:

- Aluminum substrate: metallic 1, anisotropic response aligned to manufacture, moderate roughness.
- Black lacquer or paint: near-black dielectric layer with subtle color lift rather than absolute zero.
- Microstructure: fine directional brushing beneath paint where visible; restrained orange-peel normal and roughness variation in the coating.
- Clear coat: physically separate top response or Principled coat with its own roughness.
- Spot varnish: smoother localized material for tone-on-tone graphics, with contrast driven by roughness and edge relief rather than gray base color.
- Anodized trim: metallic colored reflection with controlled roughness; avoid emission unless the reference visibly glows.

Use object scale and Mapping nodes so procedural frequencies correspond to real dimensions. Large pebbled noise is not aluminum microtexture.

## Typography

Match font category, condensation, stroke weight, width, cap height, and spacing independently. Avoid scaling a font uniformly when only height or width needs adjustment. Inspect tangency and rhythm at the final camera angle, not only in orthographic front view.
