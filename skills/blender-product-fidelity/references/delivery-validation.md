# Delivery checks and evidence

## Select the scope

Before editing, identify the authoritative source file and approved reference/version. Record delivery dimensions, duration/FPS where applicable, alpha/background expectation and invariants such as colors, logo geometry and camera layout. A web workaround may not belong in the physical source. Save a revision; change one cause at a time when diagnosing a defect.

Run the existing audit for basic scene metadata. For geometry, animation or performance review, add:

```bash
"$BLENDER_BIN" --background /absolute/path/project.blend --python-exit-code 1 \
  --python /absolute/path/blender-product-fidelity/scripts/preflight.py -- \
  --frames 1,75,310 --json /absolute/path/new-preflight.json
```

Choose frames relevant to the actual project; the example numbers are not a required sequence. The script does not render, save the scene, change device preferences or repair meshes. It restores frame/subframe and refuses to overwrite a report. Run on a saved copy in a background process: evaluating frames can invoke scene handlers. Use `--python-exit-code 1` to detect script failures; geometric findings are in JSON `status`/`issues`, not process exit status. `no_automated_findings` is not a certification.

## Acceptance evidence

- Geometry: inspect silhouette, grazing highlights, gaps and contact shadows at rest and maximum travel. Compare against the approved reference, with identical camera and lighting when isolating geometry changes.
- Materials: inspect native-resolution crops for lost texture, white seams, denoiser smearing and shifted brand colors. Do not replace palette or color management merely to make a background white.
- Output: inspect an actual encoded image for pixel dimensions, channels/alpha and background. Shader base-color white and Film Transparent flags do not alone prove white/opaque final output; compositor and view transform can change it.
- Animation: inspect a consecutive representative segment containing press/release and camera motion, not only widely separated frames. Check collisions, text transitions, flicker, shimmering texture, sliding shadows and keyframe easing. Still checks do not establish temporal quality.
- Performance: record completed frame timings for the final settings; see animation-rendering.md. Do not launch the full sequence as a test.

## Honest handoff

**Prepared:** file/settings and applicable static checks verified, full visual or temporal output not verified. Appropriate when the user asks for setup only or prohibits renders.

**Still-verified:** representative native-resolution frames inspected. List sampled views; animation stability and unseen frames remain unverified.

**Animation-verified:** a specified sequence was rendered and inspected in motion. State whether that was a short proof or the full delivery; neither automatically validates another version.

Disclose unresolved failures and their impact. A user can receive a prepared file without extra approval gates, but do not label an untested animation production-validated. Include the exact file, changes, checks, remaining limitations and how to resume/encode if using image sequences.

## Regression checks for this skill

Run only in a disposable background process with no user file:

```bash
"$BLENDER_BIN" --background --factory-startup --python-exit-code 1 \
  --python /absolute/path/blender-product-fidelity/scripts/test_preflight.py
```

These fixtures check observable findings and that settings/frame state are preserved. They validate the automated checks, not the quality of arbitrary product modeling or rendering decisions. After changing the audit, rerun fixtures and one representative saved project without rendering or saving it.
