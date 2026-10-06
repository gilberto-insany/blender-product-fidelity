#!/bin/sh
set -eu

codex_root="${CODEX_HOME:-$HOME/.codex}"
cli="$codex_root/skills/blender-toolkit/scripts/dist/cli/cli.js"

if [ ! -f "$cli" ]; then
  echo "Blender Toolkit CLI not built: $cli" >&2
  exit 1
fi

exec node "$cli" "$@"
