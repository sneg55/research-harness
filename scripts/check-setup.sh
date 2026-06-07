#!/usr/bin/env bash
# Fail if any {{PLACEHOLDER}} is left unfilled after spinning a project up from
# the harness. Exits 1 with the offending file:line list, 0 when clean.
#
# Note: the harness template itself ships with placeholders by design, so running
# this in the template repo is expected to fail. It is meant for a real project
# created from the template.
set -euo pipefail

root="${1:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"

hits="$(grep -rn '{{' "$root" \
  --include='*.md' --include='*.json' --include='*.py' \
  --exclude-dir='.git' 2>/dev/null || true)"

if [ -n "$hits" ]; then
  echo "Unfilled placeholders remain:"
  echo "$hits"
  exit 1
fi

echo "OK: no {{placeholders}} remain."
