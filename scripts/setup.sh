#!/usr/bin/env bash
# One-shot setup for a project spun up from research-harness. Idempotent.
#
#   1. Links the harness auto-memory path to the repo memory/ dir (single source
#      of truth), computing the project slug so you do not have to.
#   2. Warns if any {{PLACEHOLDER}} is still unfilled.
#   3. Runs the committed hook tests so you know the write-time gates fire.
#
# Run from anywhere: bash scripts/setup.sh
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"

echo "== 1. memory symlink =="
slug="$(printf '%s' "$root" | sed 's:/:-:g')"
projdir="$HOME/.claude/projects/$slug"
mkdir -p "$projdir"
if [ -L "$projdir/memory" ] || [ -e "$projdir/memory" ]; then
  echo "memory link already present: $projdir/memory"
else
  ln -s "$root/memory" "$projdir/memory"
  echo "linked $projdir/memory -> $root/memory"
fi

echo
echo "== 2. placeholders =="
if ! bash "$root/scripts/check-setup.sh" "$root"; then
  echo "WARN: fill the placeholders above before shipping (see SETUP.md step 2)."
fi

echo
echo "== 3. hook tests =="
bash "$root/scripts/test-hooks.sh" "$root"

echo
echo "Setup complete."
