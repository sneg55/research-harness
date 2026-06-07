# Writing and Sourcing Rules

Canonical, numbered rule set for all prose, analysis, and deliverables in this
project. This file is the **single source of truth**. `CLAUDE.md` carries a short
summary; the `deliverable-check` skill, the `citation-checker` agent, and the
`style-reviewer` agent all reference these R-numbers instead of restating the
rules, so a change here propagates everywhere.

Example violations below are wrapped in backticks so the write-time hooks do not
flag this file itself.

## R1. No em dashes

Em dash (U+2014) and horizontal bar (U+2015) are banned in all prose, including
tables and chat. Hard fail. En dash (U+2013) is allowed only in a numeric range,
and even there prefer "to" or a hyphen. Fix with a comma, parentheses, two
sentences, a colon, or "vs."/"or"/"to". Enforced at write time by
`check-em-dash.py`.

## R2. No unsourced or invented numbers

For every specific figure (`%`, `$`, rate, pass-rate, audience size, comp), ask:
is there a traceable primary source? If not, it must be reframed with sourceable
evidence pointing at the same conclusion, labeled illustrative/estimate with
round numbers, or cut. "Sounds right" is not a source. Bounding arguments beat
fabricated point estimates.

In `research/` notes, every specific figure or factual claim carries a `[S#]`
source marker that resolves to the note's `## Sources` block (see
`research/TEMPLATE.md`). The `citation-checker` agent validates those markers.
The `check-prose.py` hook flags figures written without a marker or an
illustrative label. Defer deep sourcing judgment to `citation-checker` for any
number-heavy doc.

## R3. No invented requirements

Every "what X needs" item must trace to the spec, a transcript, a stated
decision, or a documented constraint. Do not pattern-match (`it's enterprise, so
SOC 2 must be required`). Unsourced-but-useful items become open questions for the
decision owner, not fixed requirements.

## R4. Exec-summary bullets are findings only

Each bullet states a conclusion, a binding constraint, an open decision, or a
reframe versus prior framing. No number restatement, no revenue-line / segment /
surface enumeration, no prior-sprint references. One bullet is one tight
paragraph, 60 to 100 words. If it restates a body number or enumerates a list,
it is doing the body's work.

## R5. No process attribution

Scrub `per [name]`, `[name] confirmed`, `per Part 1`, `Part 1 concluded`,
`Apr 15 framing`, `as discussed`. State conclusions flat. Exception:
authoritative external evidence the reader must evaluate (a regulator briefing, an
agency ruling, a public dataset) is a real citation, not attribution.

## R6. Terminology: enforce the project glossary

Enforce the project's canonical terms over their synonyms. Each glossary entry is
a preferred term, the banned synonym, and any context where the synonym is
allowed (verbatim transcripts, imported reference texts, a literal API param).
Fill in the glossary for this project in `CLAUDE.md`.

## R7. Spelling: canonical project and product names

Normalize speech-to-text and common misspellings of the project and product names
in any synthesized doc. Verbatim transcripts may keep the original.

## R8. Name actual owners

Owner / responsible / decision-maker columns in internal deliverables name the
person, not a generic `Founder/PM/lead` label. External briefs keep generic
labels (see R12).

## R9. No scaffolding

Cut meta-structure: `Decision target` / `Decision owner` / `Scope` header blocks,
"what this does and does not lock" sections, a `Sources` section that only
duplicates inline links, and requirements lists that restate the spec. Cut
mid-sentence bolded inline labels (`**Topic.** ...`); use prose with the topic in
the topic sentence, or a real subheading.

## R10. No restating known info

Drop `Frame` / `Scope` / `Intro` / `Context` / `Background` sections for internal
readers who know the project. Open with the content. Setup paragraphs earn their
place only for outside readers.

## R11. No unrelated context / scope bleed

Each doc is scoped to its own decision. Do not recap adjacent decisions to show
awareness. Boundary-fencing ("this doesn't lock X") earns its place only when X is
a real confusion risk for this doc.

## R12. External-brief jargon (counsel / partner / investor only)

Drop internal phase / layer / option / config labels, sprint, scope section
symbols, internal cohort names, internal acronyms, raw math symbols. Use the
project's canonical external framing. Industry vocabulary the recipient already
knows stays. Case-law and peer-operator references the recipient would recognize
stay.

## R13. No slope

Lead with limitations and trade-offs, not benefits. Do not frame a shared
weakness as an advantage. A cost hidden elsewhere is not a free benefit. Ground
volume / revenue claims in realistic numbers. Keep theoretical-cap revenue out of
the headline.

## R14. No time estimates

Never size work in hours, days, or weeks (`~3 days`, `a couple of weeks`). Use
concrete units: lines of code, files touched, item counts, token count. If
genuinely unknown, say so (`unknown, need to read X first`) rather than guessing
in time. Enforced at write time by `check-prose.py`.

## Humanizer pass

These rules are mechanical and structural. Once content is locked on a
stakeholder-facing doc, run the `humanizer` skill for the prose-rhythm pass
(em-dash density, mid-sentence bold, rule-of-three, negative parallelism, arrow
notation, AI vocabulary).
