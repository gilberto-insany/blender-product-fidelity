# Geometry hygiene without damaging product fidelity

- Count evaluated vertices/triangles after modifiers, not only source polygons. Identify the largest contributors, dense text, bevel/subdivision stacks, repeated microdetails and invisible construction objects. There is no universal polygon limit.
- Check zero-area faces, loose vertices, duplicate faces/objects at identical transforms, reversed/inconsistent normals, coplanar competing surfaces, self-intersections, excessive bevel widths and intersections at animation extremes. A topology scan cannot prove absence of all shading artifacts.
- Treat duplicate candidates as evidence to inspect, not permission to delete. Compare materials, modifiers, visibility keys, parent animation and purpose. Text variants intentionally occupy the same place but appear at different frames. Transparent shells, switches and bevel layers can be intentional.
- Prefer linked meshes or instances for truly repeated geometry. Reduce subdivisions only when silhouette and grazing highlights survive native-resolution closeups. Do not globally decimate, weld by a large tolerance, apply every modifier or delete interiors blindly.
- Diagnose white seams and dirty edges under neutral and grazing light. Distinguish mesh gaps/z-fighting from projected-texture bleed, incorrect UV padding, normals, excessive specular response, sampling noise and denoiser smearing. Fix the responsible layer.
- When porting web changes back to Blender, inspect whether the change was camera perspective, physical geometry, UV/baked lighting correction, or interaction. A dark shader patch used to cover a baked fringe is not automatically appropriate for a physically rendered surface.
- Move key caps and legends together along their local travel axis; keep the bed and housing stationary. Inspect rest, maximum depression and return for collisions and duplicate silhouettes. Under-key lights should originate below the cap, without painting the cap itself.
- Preserve approved color management, palette, lighting and materials during geometry cleanup unless evidence requires a scoped change. Keep the original version and document what was changed, scanned and visually verified.

## Automated checks

Use `scripts/preflight.py` at representative frames before choosing a repair. It reports evaluated triangle counts, exact coincident mesh candidates, zero-area and duplicate faces, loose vertices and boundary/nonmanifold edge counts. It also flags missing file images and differing render/viewport modifier visibility. It does not perform arbitrary collision detection, weld geometry or certify normals/visual quality. Nonmanifold counts can be intentional on sheets and labels.

Its dependency graph is a viewport evaluation; excluded collections, procedural instances and render-only subdivision can require a separate render evaluation. Report that limit instead of calling the count a complete render memory estimate. Exact duplicate matching can miss equivalent meshes with a different vertex order or tiny positional differences.
