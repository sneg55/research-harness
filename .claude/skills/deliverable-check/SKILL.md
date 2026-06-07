---
name: deliverable-check
description: Run before any doc goes to a stakeholder (internal reader, counsel, partner, investor). Checks a deliverable against the project's accumulated writing and sourcing rules: em dashes, unsourced numbers, exec-summary discipline, process attribution, terminology, named owners, scaffolding, scope bleed, and external-brief jargon. Reports a pass/fail checklist with line-level findings. Use when finalizing a research note, deliverable, scope doc, brief, or deck source.
---

# deliverable-check

A pre-ship gate for stakeholder-facing documents. Read the target file, run the
mechanical scans, then judge each rule and report findings with file:line
references. This skill reports; it does not edit. Hand fixes back to the user or
apply them in a separate step.

If no file is named, ask which file (or accept a path argument).

## Step 1: Mechanical scans

Run these against the target file and capture results. Customize the
project-specific scans (terminology, naming) for your project; see the
PROJECT GLOSSARY note below.

```bash
F="<target>"
# Em dashes (U+2014) and horizontal bars (U+2015), banned in all prose
grep -nP '[\x{2014}\x{2015}]' "$F" || echo "OK: no em dashes"
# Process attribution tells
grep -niE 'per [A-Z][a-z]+|said|confirmed|per part 1|part 1 (concluded|landed|established)|as discussed|in the .* call' "$F" || echo "OK: no obvious attribution"
# Deliverable sizing tells (scope docs)
grep -niE '\b(one|1)[ -]pager?\b|\bone-page\b|bridge paragraph|short brief|\b[0-9]+-page\b' "$F" || echo "OK: no sizing claims"
# Time estimates (use concrete units instead)
grep -niE '\b[0-9]+ ?(hours?|days?|weeks?|months?)\b|\ba (day|week|month)\b' "$F" || echo "OK: no time estimates"
# Scaffolding header blocks
grep -niE '\*\*(decision target|decision owner|scope|objective|frame|context|background):\*\*|^#+ +(frame|scope|intro|context|background)\b' "$F" || echo "OK: no scaffolding headers"
# PROJECT GLOSSARY: add greps for your banned synonyms here, e.g.
#   grep -ni 'BANNED_SPELLING' "$F"   # canonical project/product spelling
#   grep -niP '\bBANNED_SYNONYM\b' "$F"   # preferred term vs synonym
# Specific numbers (manual review needed for sourcing)
grep -noE '[0-9]+(\.[0-9]+)?%|\$[0-9][0-9,]*' "$F" | head -40
```

## Step 2: Judge each rule

Mechanical scans flag candidates, not verdicts. Read each hit in context and
decide. The canonical rule text and judgment calls live in
`docs/writing-rules.md` (R1 to R14). Read that file, then walk every Step 1 hit
against the matching rule. Do not restate the rules here; the rules file is the
single source of truth, so it cannot drift from what the agents enforce.

Skill-specific operational notes:

- The grep block covers R1 (em dashes), R5 (attribution), R14 (time estimates),
  R9 (scaffolding headers), and R2 (figures, listed for manual sourcing review).
  R3, R4, R6 to R8, and R10 to R13 are judgment-only: no grep substitutes for
  reading the doc.
- R2: for any number-heavy doc, hand sourcing judgment to the `citation-checker`
  subagent rather than ruling on each figure here.
- R6, R7: customize the PROJECT GLOSSARY greps in Step 1 for this project's
  banned synonyms and canonical names.

## Step 3: Humanizer reminder

If the doc is stakeholder-facing and content is locked, remind the user to run
the humanizer skill (em-dash density, mid-sentence bold, rule-of-three, AI
vocabulary, arrow notation). This skill checks rule 1 mechanically; humanizer
handles the broader prose-rhythm pass.

## Step 4: Report

Output a checklist. For each rule: PASS, or FAIL with file:line references and
the specific fix. Group fails first. Close with whether the doc is ship-ready
and whether a humanizer pass and/or citation-checker run is still owed.
