# Physically credible condensation

## Geometry

Use spherical caps or metaball-like deformed droplets that intersect the product surface slightly and form a contact region. Full spheres resting on the surface read as beads or bubbles.

Use a skewed distribution:

- many microdroplets;
- fewer medium droplets;
- rare large droplets;
- several elongated drops and short gravity trails;
- dry and wet zones instead of uniform coverage.

Instance shared meshes through Geometry Nodes or linked data. Orient each cap to the local surface normal. Elongate larger drops along gravity and merge nearby drops selectively. Keep branding partially readable by using a density mask rather than removing all drops from the label.

## Water shader

Use IOR approximately 1.333, transmission near 1, low but nonzero roughness, and no metallic response. Reflection and refraction must come from the environment. Avoid emission and opaque silver materials.

In Cycles, confirm sufficient transmission bounces and denoising. Check large droplets at 100% render scale for black cores, excessive fireflies, or gray opacity.

## Surface interaction

A believable cold product combines droplets with a subtle wetness layer beneath dense regions. Use a restrained roughness reduction or thin-film darkening mask; do not make the entire can uniformly glossy.

The key light should produce sharp highlights on droplets while the can retains broader reflections. If droplets disappear, adjust light size and angle before increasing their color or opacity.
