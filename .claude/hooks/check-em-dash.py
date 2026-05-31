#!/usr/bin/env python3
"""PostToolUse hook: flag em dashes in Markdown files after a Write/Edit.

Em dashes are banned in all prose in this harness. This catches them at write
time instead of at review. The file has already been written when this runs, so
we read it from disk and report any offending lines back to Claude (exit 2) for
an immediate fix.

Banned: em dash U+2014 (—) and horizontal bar U+2015 (―).
Not flagged here: en dash U+2013 (–), which is allowed in numeric ranges and
would produce too many false positives. Hyphens are fine.
"""
import json
import os
import sys

EM_DASH = "—"
HORIZONTAL_BAR = "―"
BANNED = (EM_DASH, HORIZONTAL_BAR)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # not our problem; let the tool result stand

    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "")
    if not file_path.lower().endswith((".md", ".markdown")):
        return 0

    # Scope to the project repo: this rule governs this project's deliverables
    # and research, not files elsewhere (e.g. Claude's memory dir under ~/.claude).
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        try:
            real = os.path.realpath(file_path)
            root = os.path.realpath(project_dir)
            if os.path.commonpath([real, root]) != root:
                return 0
        except (ValueError, OSError):
            return 0

    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except (OSError, UnicodeDecodeError):
        return 0

    hits = []
    for n, line in enumerate(lines, start=1):
        if any(ch in line for ch in BANNED):
            hits.append((n, line.rstrip("\n")))

    if not hits:
        return 0

    print(
        f"Em dash(es) found in {file_path}, banned in all prose. "
        f"Replace with a comma, parentheses, two sentences, a colon, "
        f"or 'vs.'/'or'/'to'. Offending lines:",
        file=sys.stderr,
    )
    for n, text in hits[:25]:
        print(f"  L{n}: {text.strip()}", file=sys.stderr)
    if len(hits) > 25:
        print(f"  ... and {len(hits) - 25} more", file=sys.stderr)
    return 2  # surface stderr to Claude


if __name__ == "__main__":
    sys.exit(main())
