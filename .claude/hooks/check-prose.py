#!/usr/bin/env python3
"""PostToolUse hook: flag the two rules the project owner gets burned by most.

Two write-time checks the em-dash hook does not cover:

  R14 No time estimates  -- "~3 days", "a couple of weeks". Sized work belongs in
      concrete units (files, lines, item counts), not hours/days/weeks.
  R2  Unsourced figures   -- a specific $ amount or % presented with no source
      marker ([S1]), no link, and no illustrative/estimate label.

Both are advisory: this hook surfaces candidates back to Claude (exit 2) so the
real ones get fixed, but the patterns have false positives (a factual "the trial
lasted 3 months", a number cited on a nearby line). Read each hit in context.

Skips fenced code blocks and inline `code` spans, so docs that *document* the
banned patterns (like docs/writing-rules.md) do not flag themselves. Scoped to
.md/.markdown files inside CLAUDE_PROJECT_DIR, matching check-em-dash.py.
"""
import json
import os
import re
import sys

# R14: a number immediately followed by a time-effort unit.
TIME_RE = re.compile(
    r"\b\d+\s*(?:\+|-|to|–)?\s*\d*\s*"
    r"(hours?|hrs?|days?|weeks?|months?|quarters?|years?)\b"
    r"|\ba (?:few|couple of|couple) (hours?|days?|weeks?|months?)\b"
    r"|\b(hour|day|week|month)-long\b",
    re.IGNORECASE,
)

# R2: a specific dollar amount or percentage presented as fact.
FIGURE_RE = re.compile(r"\$\d[\d,]*(?:\.\d+)?\s*[KMB]?\b|\b\d+(?:\.\d+)?%")

# A line carrying any of these is treated as sourced or labelled -> not flagged.
SOURCED_RE = re.compile(
    r"\[S\d+\]"            # source marker, e.g. [S1]
    r"|\]\("               # markdown link
    r"|\[est\]|\best\.|\bestimate|illustrative|placeholder|roughly|approx"
    r"|~\s*\$|~\s*\d",     # leading ~ means a rough/round figure
    re.IGNORECASE,
)

INLINE_CODE_RE = re.compile(r"`[^`]*`")


def strip_noncprose(lines):
    """Yield (lineno, prose-only text), dropping fenced blocks and inline code."""
    in_fence = False
    for n, raw in enumerate(lines, start=1):
        stripped = raw.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield n, INLINE_CODE_RE.sub("", raw.rstrip("\n"))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "")
    if not file_path.lower().endswith((".md", ".markdown")):
        return 0

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

    time_hits, figure_hits = [], []
    for n, text in strip_noncprose(lines):
        if TIME_RE.search(text):
            time_hits.append((n, text.strip()))
        if FIGURE_RE.search(text) and not SOURCED_RE.search(text):
            figure_hits.append((n, text.strip()))

    if not time_hits and not figure_hits:
        return 0

    out = sys.stderr
    print(f"check-prose flagged {file_path} (advisory, review in context):", file=out)
    if time_hits:
        print("  R14 time estimates (use files/lines/item counts instead):", file=out)
        for n, t in time_hits[:15]:
            print(f"    L{n}: {t}", file=out)
    if figure_hits:
        print("  R2 figures with no source marker, link, or estimate label:", file=out)
        print("      add a [S#] marker, a link, or label it [est] with round numbers.", file=out)
        for n, t in figure_hits[:15]:
            print(f"    L{n}: {t}", file=out)
    return 2


if __name__ == "__main__":
    sys.exit(main())
