---
title: <one-line topic>
date: YYYY-MM-DD
status: draft
summary: <one line for INDEX.md: what this note answers>
---

# <Topic>

> Copy this file to start a research note: `cp research/TEMPLATE.md research/<topic>.md`.
> Delete this quote block and fill the sections. One topic per file.
> `status` and `summary` feed the generated `INDEX.md` (see CLAUDE.md). Bump
> `status` from `draft` to `working` once the note has real findings.

## Question

What this note answers, in one or two sentences.

## Findings

State each finding flat (see R4, R5 in `docs/writing-rules.md`). Attach a source
marker to every specific figure or factual claim, like this [S1]. A claim without
a marker is treated as unsourced by `citation-checker` and may be flagged by the
`check-prose.py` hook. Labelled estimates are fine: write "roughly 40% [est]" with
round numbers, not a fake-precise figure.

## Open questions

Track unknowns here so they survive across sessions. Promote project-level ones to
`research/open-questions.md` if you keep one.

-

## Sources

One entry per marker. Keep the marker stable once cited.

[S1] Title. Publisher or author, date. URL or repo path.
[S2]
