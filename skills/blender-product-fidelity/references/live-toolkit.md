# Live Blender toolkit

Blender Toolkit is an optional, separately installed integration; it is not bundled with this skill. Before using it, verify that a compatible toolkit exists at `${CODEX_HOME:-$HOME/.codex}/skills/blender-toolkit`, that its CLI has been built, and that the corresponding Blender add-on is installed and enabled. Do not assume any of these steps have already happened. If it is unavailable, use Blender Python in background mode instead. Installing or enabling an integration requires the user's authorization.

## Start and verify

Open Blender, then use `View3D > Sidebar > Blender Toolkit > Start Server`. The server binds only to `127.0.0.1` and defaults to port 9400.

Run the wrapper with `--help` before the first command:

```bash
"${CODEX_HOME:-$HOME/.codex}/skills/blender-product-fidelity/scripts/toolkit.sh" --help
"${CODEX_HOME:-$HOME/.codex}/skills/blender-product-fidelity/scripts/toolkit.sh" list-objects --port 9400
```

Use it for read-only inspection first. Resolve exact object names before transforms, deletions, modifier application, or material replacement. Never clear a scene or delete broad collections merely to simplify automation.

The toolkit supports primitives, transforms, selected modifiers, collections, basic material values, and animation retargeting. It does not expose arbitrary Python or advanced shader/Geometry Nodes authoring. Use a versioned Blender Python build script for those operations.

If the CLI cannot connect, verify that Blender is open, the add-on is enabled, and Start Server was clicked. Do not repeatedly reinstall the add-on to solve a stopped server.
