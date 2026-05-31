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
decide. The rules, with their judgment calls:

**1. No em dashes.** Banned in all prose, including tables and chat. Em dash
U+2014 and horizontal bar U+2015 are hard fails. En dash U+2013 is allowed only
in a numeric range, and even there prefer "to" or a hyphen. Fix with a comma,
parentheses, two sentences, a colon, or "vs."/"or"/"to".

**2. No unsourced or invented numbers.** For every specific figure (%, $, rate,
pass-rate, audience size, comp), ask: is there a traceable primary source? If
not, it must be reframed with sourceable evidence pointing at the same
conclusion, labeled illustrative/estimate with round numbers, or cut. "Sounds
right" is not a source. Bounding arguments beat fabricated point estimates.
Defer deep sourcing judgment to the `citation-checker` subagent for any
number-heavy doc.

**3. No invented requirements.** Every "what X needs" item must trace to the
spec, a transcript, a stated decision, or a documented constraint. Don't
pattern-match ("it's enterprise, so SOC 2 must be required"). Unsourced-but-
useful items become open questions for the decision owner, not fixed
requirements.

**4. Exec-summary bullets are findings only.** Each bullet states a conclusion,
a binding constraint, an open decision, or a reframe. No number restatement, no
revenue-line/segment enumeration, no prior-sprint references. 60 to 100 words
per bullet; if longer it's doing the body's work.

**5. No process attribution.** Scrub "per [name]", "[name] confirmed", "per Part
1", "Part 1 concluded", "Apr 15 framing", "as discussed". State conclusions
flat. Exception: authoritative external evidence the reader must evaluate (a
regulator briefing, an agency ruling, a public dataset) is a real citation, not
attribution.

**6. Terminology: enforce the project glossary.** Enforce the project's canonical
terms over their synonyms. Fill in the glossary for this project: each entry is a
preferred term, the banned synonym, and any contexts where the synonym is allowed
(verbatim transcripts, imported reference texts, a literal API param).

**7. Spelling: canonical project and product names.** Normalize speech-to-text or
common misspellings of the project and product names in any synthesized doc.
Verbatim transcripts may keep the original.

**8. Name actual owners.** Owner/responsible/decision-maker columns in internal
deliverables name the person, not a generic "Founder/PM/lead" label. External
briefs keep generic labels (see rule 12).

**9. No scaffolding.** Cut meta-structure: Decision target/owner/Scope header
blocks, "what this does and does not lock" sections, a Sources section that
duplicates inline links, and requirements lists that restate the spec. Cut
mid-sentence bolded inline labels (`**Topic.** ...`); use prose with the topic
in the topic sentence, or a real subheading.

**10. No restating known info.** Drop Frame/Scope/Intro/Context sections for
internal readers who know the project. Open with the content. Setup paragraphs
earn their place only for outside readers.

**11. No unrelated context / scope bleed.** Each doc is scoped to its own
decision. Don't recap adjacent decisions to show awareness. Boundary-fencing
("this doesn't lock X") earns its place only when X is a real confusion risk for
this doc.

**12. External-brief jargon (counsel/partner/investor only).** Drop internal
phase/layer/option/config labels, sprint, scope §, internal cohort names,
internal acronyms, raw math symbols. Use the project's canonical external
framing. Industry vocabulary the recipient knows stays.

**13. No slope.** Lead with limitations and trade-offs, not benefits. Don't
frame a shared weakness as an advantage. A cost hidden elsewhere is not a free
benefit. Ground volume/revenue claims in realistic numbers.

**14. No time estimates.** Never size work in hours/days/weeks. Use concrete
units: lines of code, files touched, item counts, token count. If genuinely
unknown, say so ("unknown, need to read X first") rather than guessing in time.

## Step 3: Humanizer reminder

If the doc is stakeholder-facing and content is locked, remind the user to run
the humanizer skill (em-dash density, mid-sentence bold, rule-of-three, AI
vocabulary, arrow notation). This skill checks rule 1 mechanically; humanizer
handles the broader prose-rhythm pass.

## Step 4: Report

Output a checklist. For each rule: PASS, or FAIL with file:line references and
the specific fix. Group fails first. Close with whether the doc is ship-ready
and whether a humanizer pass and/or citation-checker run is still owed.
