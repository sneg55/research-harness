#!/usr/bin/env python3
"""Generate INDEX.md: a single LLM-readable map of every authored doc in the repo.

Walks the authored tree, reads each file's frontmatter (falling back to a
path-inferred status when a file has none), derives the last-updated date from
git, and writes a grouped table to INDEX.md at the repo root. An LLM landing cold
reads INDEX.md first to find the right file (and tell current from superseded)
instead of grepping the whole tree.

Usage:
    python3 scripts/build_index.py           # (re)write INDEX.md
    python3 scripts/build_index.py --check    # validate frontmatter + report staleness (no write)

# ---------------------------------------------------------------------------
# CONFIG: this is the block a project spun up from the harness edits.
# Everything below CONFIG is generic and rarely needs changing.
# ---------------------------------------------------------------------------

Add a top-level content dir to AUTHORED_ROOTS. Map a path prefix to the status a
file there gets when it carries no `status` of its own via STATUS_RULES (first
match wins; DEFAULT_STATUS if none match). List any imported/vendored subtree in
VENDORED so it is linked once rather than enumerated file by file.
"""

import argparse
import os
import re
import subprocess

import frontmatter

# ----- CONFIG (edit for your project) --------------------------------------

# Top-level trees that hold authored docs and are expected to carry frontmatter.
AUTHORED_ROOTS = ["research", "docs"]

# Ordered (path-prefix, status) rules. First match wins. Used when a file has no
# `status` in its frontmatter. Keep prefixes trailing-slashed.
STATUS_RULES = [
    ("docs/archive/", "frozen"),
    ("docs/reference/", "canonical"),
    ("docs/", "source"),
    ("research/", "working"),
]
DEFAULT_STATUS = "working"

# Vendored/imported subtrees: linked once, not enumerated. Each is
# (subtree_path, path_to_its_own_index_or_readme).
#   e.g. ("docs/vendor-kb", "docs/vendor-kb/INDEX.md")
VENDORED = []

# Groups (directories) to float to the top of the index, in this order.
GROUP_ORDER = []

# Statuses surfaced in the "Start here" section, most-authoritative first.
START_HERE_STATUSES = ("canonical",)

# ----- end CONFIG ----------------------------------------------------------

STATUSES = ["canonical", "working", "source", "draft", "superseded", "frozen"]
REQUIRED_FIELDS = ["status", "summary"]
DEAD_STATUSES = ("superseded", "frozen")

SKIP_DIR_NAMES = {".git", "__pycache__", "node_modules", ".archive"}

# In-body version line, e.g. "v0.7, 2026-07-06" or "**v0.7**". If a doc carries a
# version in the body, the index reads it from there rather than duplicating it
# into frontmatter (single source of truth).
_BODY_VERSION = re.compile(r"^[*_]*v(\d[\d.]*)\b", re.I | re.M)


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)


def is_vendored(rel):
    return any(rel == v or rel.startswith(v + "/") for v, _ in VENDORED)


def infer_status(rel):
    """Status a file gets from its location when it carries no frontmatter."""
    for prefix, status in STATUS_RULES:
        if rel.startswith(prefix):
            return status
    return DEFAULT_STATUS


def is_authored_md(rel):
    """A markdown file we index and expect to carry frontmatter."""
    if not rel.endswith(".md"):
        return False
    if is_vendored(rel):
        return False
    if os.path.basename(rel).startswith("."):
        return False
    top = rel.split("/", 1)[0]
    return top in AUTHORED_ROOTS


def walk_authored(root):
    """Yield repo-relative paths of authored markdown files."""
    for base in AUTHORED_ROOTS:
        base_abs = os.path.join(root, base)
        if not os.path.isdir(base_abs):
            continue
        for dirpath, dirnames, filenames in os.walk(base_abs):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
            rel_dir = os.path.relpath(dirpath, root)
            if is_vendored(rel_dir):
                dirnames[:] = []
                continue
            for fn in filenames:
                rel = os.path.normpath(os.path.join(rel_dir, fn))
                if is_authored_md(rel):
                    yield rel


def git_updated(root, rel):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        return out.stdout.strip() or "-"
    except OSError:
        return "-"


def first_heading(body):
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith("#"):
            return s.lstrip("#").strip()
    return ""


def load_records(root):
    """Return list of dicts: rel, status, summary, version, supersedes, updated, group."""
    records = []
    for rel in walk_authored(root):
        with open(os.path.join(root, rel), encoding="utf-8") as f:
            text = f.read()
        fields, body = frontmatter.parse(text)
        status = fields.get("status") or infer_status(rel)
        summary = fields.get("summary") or first_heading(body) or "(no summary)"
        version = fields.get("version")
        if version is None:
            m = _BODY_VERSION.search(body)
            if m:
                version = m.group(1)
        records.append(
            {
                "rel": rel,
                "status": status,
                "summary": summary,
                "version": version,
                "supersedes": fields.get("supersedes"),
                "superseded_by": fields.get("superseded_by"),
                "updated": git_updated(root, rel),
                "group": os.path.dirname(rel),
                "has_fm": bool(fields),
            }
        )
    records.sort(key=lambda r: r["rel"])
    return records


def _cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ") if s is not None else ""


def _row(r):
    ver = _cell(r["version"]) if r["version"] is not None else ""
    return (
        f"| [{os.path.basename(r['rel'])}]({r['rel']}) | {r['status']} | {ver} "
        f"| {_cell(r['summary'])} | {r['updated']} |"
    )


def render_index(root, records):
    live = [r for r in records if r["status"] not in DEAD_STATUSES]
    dead = [r for r in records if r["status"] in DEAD_STATUSES]

    lines = [
        "# Repository Index",
        "",
        "> Generated by `scripts/build_index.py` from each file's frontmatter. **Do not edit by hand.**",
        "> Read this first to find the right file. Every authored `.md` carries `status` + `summary` frontmatter;",
        "> `status` tells you whether to trust it: `canonical`/`working`/`source`/`draft` are current, "
        "`superseded`/`frozen` are not (see the bottom section).",
        "",
    ]

    start = [r for r in live if r["status"] in START_HERE_STATUSES]
    if start:
        lines += [
            "## Start here",
            "",
            "| file | status | v | summary | updated |",
            "|------|--------|---|---------|---------|",
        ]
        lines += [_row(r) for r in start]
        lines.append("")

    groups = sorted({r["group"] for r in live})
    ordered = [g for g in GROUP_ORDER if g in groups] + [
        g for g in groups if g not in GROUP_ORDER
    ]
    for g in ordered:
        rows = [r for r in live if r["group"] == g]
        lines += [
            f"## {g}",
            "",
            "| file | status | v | summary | updated |",
            "|------|--------|---|---------|---------|",
        ]
        lines += [_row(r) for r in rows]
        lines.append("")

    if VENDORED:
        lines += ["## Vendored (own indexes, not enumerated here)", ""]
        for base, idx in VENDORED:
            note = (
                idx
                if os.path.exists(os.path.join(root, idx))
                else "(no internal index)"
            )
            lines.append(f"- `{base}/` → {note}")
        lines.append("")

    if dead:
        lines += [
            "## Superseded / frozen (do not cite)",
            "",
            "| file | status | superseded_by | summary |",
            "|------|--------|---------------|---------|",
        ]
        for r in sorted(dead, key=lambda r: (r["status"], r["rel"])):
            sb = _cell(r["superseded_by"]) if r["superseded_by"] else ""
            lines.append(
                f"| [{os.path.basename(r['rel'])}]({r['rel']}) | {r['status']} | {sb} | {_cell(r['summary'])} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def validate(records):
    """Return list of (rel, problem) for authored files with bad frontmatter."""
    problems = []
    for r in records:
        if not r["has_fm"]:
            problems.append((r["rel"], "no frontmatter (using path-inferred status)"))
            continue
        if r["status"] not in STATUSES:
            problems.append((r["rel"], f"unknown status '{r['status']}'"))
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--check",
        action="store_true",
        help="validate frontmatter and report staleness; do not write",
    )
    args = ap.parse_args()

    root = repo_root()
    records = load_records(root)
    content = render_index(root, records)
    index_path = os.path.join(root, "INDEX.md")

    if args.check:
        problems = validate(records)
        current = ""
        if os.path.exists(index_path):
            with open(index_path, encoding="utf-8") as f:
                current = f.read()
        stale = current != content
        for rel, prob in problems:
            print(f"  frontmatter: {rel}: {prob}")
        if stale:
            print("  INDEX.md is out of date. Run: python3 scripts/build_index.py")
        if not problems and not stale:
            print("INDEX.md is current and all frontmatter is valid.")
        return

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"wrote {os.path.relpath(index_path, root)} ({len(records)} files indexed)")


if __name__ == "__main__":
    main()
