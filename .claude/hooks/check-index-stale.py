#!/usr/bin/env python3
"""Advisory PostToolUse hook: warn when INDEX.md is out of date.

Cheap mtime scan (no git, no full parse) so it is safe to run on every edit: if
any authored markdown file is newer than INDEX.md, print a reminder to run the
generator. Silent otherwise, and self-gating: edits that touch no authored `.md`
leave INDEX.md the newest file, so nothing prints. Never blocks (exit 0).
"""

import os
import sys

PROJECT_DIR = os.environ.get(
    "CLAUDE_PROJECT_DIR",
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
)
sys.path.insert(0, os.path.join(PROJECT_DIR, "scripts"))

try:
    from build_index import walk_authored
except Exception:
    sys.exit(0)  # generator not importable; stay out of the way


def main():
    index = os.path.join(PROJECT_DIR, "INDEX.md")
    if not os.path.exists(index):
        print("INDEX.md is missing. Run: python3 scripts/build_index.py")
        sys.exit(0)
    idx_mtime = os.path.getmtime(index)
    for rel in walk_authored(PROJECT_DIR):
        try:
            if os.path.getmtime(os.path.join(PROJECT_DIR, rel)) > idx_mtime:
                print("INDEX.md is out of date. Run: python3 scripts/build_index.py")
                break
        except OSError:
            continue  # silent-ok: file vanished mid-walk, nothing to compare
    sys.exit(0)


if __name__ == "__main__":
    main()
