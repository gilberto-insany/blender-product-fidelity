# Product animation: quality with a measured render budget

- Preserve the original and save a versioned copy. Inspect the live app separately: a saved file may differ from the currently rendering scene. Never interrupt an active render without authorization.
- Declare resolution, FPS, frame range and duration. Check all camera extremes, intentional detail crops, key press/release poses, text visibility transitions and final pose.
- Inspect both the scene Cycles device and preferences backend/enabled devices. GPU hardware availability does not prove it was used. Verify a bounded render log before claiming acceleration. Do not silently fall back to CPU for a long sequence.
- Start testing around 256 maximum samples, adaptive threshold 0.01, min samples 16–32 and denoising; these are test candidates, not guaranteed final settings. Preserve transport settings initially when glass, translucency or reflections are important. Raise samples only where measured noise or temporal instability justifies it.
- Avoid treating tile size (including 248/256) as a universal speed fix. Its role and performance depend on Blender version, device and memory. Profile it only after identifying the bottleneck. Persistent data can help animation when memory allows; measure memory across successive frames.
- Benchmark a wide view, a detail view and a difficult transparent/reflection frame. Inspect native-resolution crops and a short consecutive sequence for denoiser shimmer and disappearing microtexture. Low-resolution proofs verify composition, not final 4K detail or animation stability.
- Report measured seconds per frame, resolution, samples, device, cold-start overhead and a full-sequence estimate with uncertainty. Multiply representative steady-state frame cost by frame count; do not promise a speedup from sample ratios alone.
- If rendering is prohibited or out of scope, deliver settings and a bounded benchmark procedure, clearly labeled unbenchmarked. Never automatically launch an entire animation to validate a prepared file.
- Prefer PNG 16-bit RGB for an opaque finished look, or EXR for a linear compositing master, then encode the delivery video separately. Use a new versioned output directory. Resume only validated complete frames from the same settings/version; avoid overwrite and disable placeholder files unless concurrency is intentionally managed.
- Keep 4K when requested. Higher resolution is not a substitute for adequate sampling and can increase cost. A 30fps/15s sequence is 450 frames; do not alter duration or FPS silently.

## Camera and light continuity

Determine whether the requested direction uses intentional edits or one continuous movement. Several detail angles do not imply permission for cuts when the user asks for a fluid reveal.

- For a continuous reveal, interpolate camera position, target/orientation and framing across the whole path. Disjoint per-shot endpoints can produce a jump even when every individual shot has easing. Inspect values and movement on both sides of former shot boundaries, including angular wraparound and quaternion sign changes.
- Validate a short consecutive interval around transitions and the approach to the final pose, not only six isolated stills. Watch for camera jumps, abrupt velocity changes, clipping, framing changes and distracting focus/exposure shifts. Use timing/transform checks when rendering is prohibited, and label the motion's visual smoothness unverified.
- On dark products, check the rim/backlight at front, side, rear, knot/detail and final display-on poses. A fixed light can disappear from useful reflection angles during an orbit. Choose a deliberate fixed studio or continuously moving light rig; do not snap the rig or its powers at camera boundaries.
- Keep a dark background compatible with readable curvature and functional details. Adjust light placement, source size, reflection cards and restrained fill before altering approved material color, opacity or roughness. Avoid clipped white rims, a metallic-looking polymer, gray bezels or washed-out display blacks.
- Animate screen-off/screen-on behavior on the actual display/emission layer and check the fade behind the front cover. Exposure changes must not substitute for turning the display on. Preserve the user's timing and artwork.

Before adding physical braid or fiber detail to a long sequence, apply the [microdetail budget](clean-production.md#budget-microgeometry-before-building-it). A hidden viewport groom remains expensive if the animation render still evaluates it.

## Reliable timing

Benchmark the exact saved revision and production settings. Do not benchmark a discarded compositor or preview scene and report it as final performance. Run GPU tests sequentially with no competing renders; disclose unavoidable contention. Record the file hash, Blender version, device, output dimensions, sample/adaptive limits, denoiser, compositor and measured wall-clock time.

A Cycles sampling time limit is not a whole-process deadline: initialization, tiles, denoising, compositing and encoding can add time. Use an external watchdog when a hard budget is required, target only the test process created for the task, and preserve the main Blender session. A time-capped render may not have converged; label it accordingly.

Calculate an estimated range only from representative, completed production-setting frames on the intended hardware. Separate startup overhead from steady-state costs and mention harder closeups. If settings or geometry change after measuring, invalidate the estimate or benchmark again. Never imply that a 4× sample reduction guarantees a 4× speedup.
