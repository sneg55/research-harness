#!/usr/bin/env bash
# Committed tests for the index tooling (frontmatter.py, build_index.py,
# check-index-stale.py). Run after editing any of them:
#   bash scripts/test-index.sh
set -uo pipefail

root="${1:-$(cd "$(dirname "$0")/.." && pwd)}"

pass=0
fail=0
assert() { # assert <label> <expected> <actual>
  if [ "$2" = "$3" ]; then
    pass=$((pass + 1)); echo "  ok: $1"
  else
    fail=$((fail + 1)); echo "  FAIL: $1 (expected '$2', got '$3')"
  fi
}

echo "frontmatter.py:"
# Pure-logic edge cases. Each python snippet prints PASS or raises.
out="$(cd "$root/scripts" && python3 - <<'PY' 2>&1
import frontmatter as fm
# real frontmatter parsed, body preserved
d, b = fm.parse("---\nstatus: working\nsummary: hi\n---\n\n# Title\nbody")
assert d["status"] == "working" and b.startswith("# Title"), (d, b)
# leading --- horizontal rule is NOT frontmatter
txt = "---\n\n## Heading\n\nprose\n\n---\n"
d, b = fm.parse(txt)
assert d == {} and b == txt, (d, repr(b))
# only the leading block is stripped; a body rule survives
d, b = fm.parse("---\nstatus: source\nsummary: x\n---\n\n# H\n\n---\n\nmore")
assert d["status"] == "source" and "---" in b, (d, b)
# inline list + null
d, _ = fm.parse("---\nstatus: draft\ntags: [a, b]\nsuperseded_by: null\n---\nx")
assert d["tags"] == ["a", "b"] and d["superseded_by"] is None, d
# render round-trips a colon-bearing summary through the flat parser
r = fm.render({"status": "working", "summary": "a: b, c"})
d, _ = fm.parse(r + "\nbody")
assert d["summary"] == "a: b, c", (r, d)
print("PASS")
PY
)"
assert "edge cases pass" "PASS" "$out"

echo "build_index.py:"
( cd "$root" && python3 scripts/build_index.py >/dev/null 2>&1 ); assert "generator runs" 0 $?
[ -f "$root/INDEX.md" ]; assert "INDEX.md produced" 0 $?
( cd "$root" && python3 scripts/build_index.py --check >/dev/null 2>&1 ); assert "--check runs" 0 $?

echo "check-index-stale.py:"
CLAUDE_PROJECT_DIR="$root" python3 "$root/.claude/hooks/check-index-stale.py" >/dev/null 2>&1
assert "hook exits 0 (advisory)" 0 $?

echo
echo "index: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
