#!/usr/bin/env python3
"""Backfill frontmatter into authored markdown files.

For every authored `.md` that lacks a `status` field, prepend a frontmatter
block with a path-inferred `status` (see build_index.STATUS_RULES) and a rough
`summary` (first sentence of the first paragraph, else the first heading).
Idempotent: files that already carry a `status` are left untouched, so re-running
never clobbers curated summaries. Useful when a project adopts the harness with
notes already written; a greenfield repo will not need it.

    python3 scripts/seed_frontmatter.py --dry-run   # show what would change
    python3 scripts/seed_frontmatter.py             # write

Path classification is imported from build_index.py so the seeder and the index
generator never disagree.
"""

import argparse
import os
import re

import frontmatter
from build_index import repo_root, walk_authored, infer_status, first_heading

SUMMARY_MAX = 200

# A version/date line ("v0.7, 2026-07-06", "**v0.4**") is not a description.
_VERSION_LINE = re.compile(r"^[*_]*v?\d[\d.]*[,\s*_]*(\d{4}-\d\d-\d\d)?[*_]*$", re.I)


def derive_summary(body):
    """First sentence of the first real paragraph, else the first heading."""
    for line in body.split("\n"):
        s = line.strip()
        if not s or s.startswith(("#", "|", ">", "-", "*", "`", "!", "<")):
            continue
        if _VERSION_LINE.match(s):
            continue
        sentence = s.split(". ")[0].rstrip(".")
        if len(sentence) > SUMMARY_MAX:
            sentence = sentence[:SUMMARY_MAX].rsplit(" ", 1)[0] + "…"
        return sentence
    return first_heading(body) or "(no summary)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = repo_root()
    seeded = skipped = 0
    for rel in sorted(walk_authored(root)):
        path = os.path.join(root, rel)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fields, body = frontmatter.parse(text)
        if "status" in fields:
            skipped += 1
            continue
        new_fields = {
            "status": infer_status(rel),
            "summary": derive_summary(body),
        }
        if args.dry_run:
            print(
                f"{rel}\n    status: {new_fields['status']}\n    summary: {new_fields['summary']}"
            )
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(frontmatter.render(new_fields) + "\n" + body)
        seeded += 1

    verb = "would seed" if args.dry_run else "seeded"
    print(f"\n{verb} {seeded} files, skipped {skipped} already-seeded.")


if __name__ == "__main__":
    main()
