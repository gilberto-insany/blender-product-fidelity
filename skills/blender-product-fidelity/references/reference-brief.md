# Product reference brief

Use this brief to convert a prompt and image set into measured evidence for a physically credible Blender model.

## Recommended reference pack

Aim for four to eight useful images of the same product variant:

- one target hero view for the final visual comparison;
- front, rear, left, and right views where construction differs;
- top and bottom views for seams, lids, feet, ports, recesses, and wall thickness;
- close-ups of logos, labels, typography, controls, connectors, coatings, relief, and condensation;
- an official drawing, manufacturer specification, or one known real measurement.

Prefer sharp, minimally cropped references with limited wide-angle distortion. A new angle or resolved detail is more valuable than another near-duplicate marketing shot.

## Prompt fields

```text
Product: exact name, generation, color/finish, configuration
Deliverable: target-view match or verified whole-product reconstruction
Target output: camera, focal character, crop, background, resolution, engine
Must match: silhouette, dimensions, manufactured parts, branding, materials
May approximate: hidden internals, microtext, unseen surfaces, minor fasteners
Known dimensions: at least one physical measurement or trusted ratio
Branding: source artwork, required relief, exactness, permitted substitutions
Editability: source artwork, modifiers, Geometry Nodes, material controls
```

## Evidence handling

Classify each source as geometry evidence, surface evidence, or art direction. Check that geometry and surface sources show the same SKU, generation, and finish. Prefer official dimensions and clearer orthogonal views when references conflict. Perspective compression, reflections, label artwork, shadows, and condensation are not body geometry.

If coverage is incomplete, choose an honest scope:

1. **Target-view match:** optimize the requested view and disclose assumptions elsewhere.
2. **Whole-product reconstruction:** obtain the missing views, measurements, or artwork before claiming complete fidelity.
