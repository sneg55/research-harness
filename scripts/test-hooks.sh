#!/usr/bin/env bash
# Committed tests for the write-time hooks. The hooks are the harness's only
# automated enforcement, so their exit codes are load-bearing. Run after any hook
# edit: bash scripts/test-hooks.sh
#
# Each case feeds a crafted PostToolUse payload to a hook and asserts its exit
# code (2 = flagged and surfaced to Claude, 0 = clean / out of scope).
set -uo pipefail

root="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
hooks="$root/.claude/hooks"
tmp="$root/.tmp-hooktest"
mkdir -p "$tmp"
trap 'rm -rf "$tmp"' EXIT

pass=0
fail=0

# run <hook.py> <target-file> -> echoes the hook's exit code
run() {
  printf '{"tool_input": {"file_path": "%s"}}' "$2" \
    | CLAUDE_PROJECT_DIR="$root" python3 "$hooks/$1" >/dev/null 2>&1
  echo $?
}

# assert <label> <expected-code> <actual-code>
assert() {
  if [ "$2" = "$3" ]; then
    pass=$((pass + 1))
    echo "  ok: $1 (exit $3)"
  else
    fail=$((fail + 1))
    echo "  FAIL: $1 (expected $2, got $3)"
  fi
}

emfile="$tmp/em.md"
cleanfile="$tmp/clean.md"
txtfile="$tmp/note.txt"
timefile="$tmp/time.md"
figfile="$tmp/fig.md"
sourcedfile="$tmp/sourced.md"

# check-em-dash.py
printf '# t\nan em dash \xe2\x80\x94 here\n' > "$emfile"
printf '# t\na clean line, no dashes.\n' > "$cleanfile"
printf 'an em dash \xe2\x80\x94 here\n' > "$txtfile"
echo "check-em-dash.py:"
assert "em dash flagged"        2 "$(run check-em-dash.py "$emfile")"
assert "clean md passes"        0 "$(run check-em-dash.py "$cleanfile")"
assert "non-md ignored"         0 "$(run check-em-dash.py "$txtfile")"
assert "outside project ignored" 0 "$(run check-em-dash.py "/tmp/outside.md")"

# check-prose.py
printf '# t\nThis should take about 3 days to finish.\n' > "$timefile"
printf '# t\nRevenue was $4,200 last quarter.\n' > "$figfile"
printf '# t\nRevenue was $4,200 last quarter [S1].\n\nroughly 40%% [est] churn.\n' > "$sourcedfile"
echo "check-prose.py:"
assert "time estimate flagged"  2 "$(run check-prose.py "$timefile")"
assert "unsourced figure flagged" 2 "$(run check-prose.py "$figfile")"
assert "sourced + labelled passes" 0 "$(run check-prose.py "$sourcedfile")"
assert "clean md passes"        0 "$(run check-prose.py "$cleanfile")"

echo
echo "hooks: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
