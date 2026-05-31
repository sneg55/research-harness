# research-harness

A reusable Claude Code setup for research and deliverable-writing projects. Clone
it, fill in the placeholders, and you start with a memory system, writing/sourcing
discipline, and pre-ship quality gates already wired up.

## What's inside

| Piece | Path | Does |
| --- | --- | --- |
| Project instructions | `CLAUDE.md` | Memory system, git safety, writing/sourcing discipline, project placeholders |
| Memory scaffold | `memory/` | `MEMORY.md` index + the four-type memory format documented |
| Em-dash hook | `.claude/hooks/check-em-dash.py` | PostToolUse hook that blocks em dashes in Markdown at write time |
| Hook wiring | `.claude/settings.json` | Registers the hook on Write/Edit/MultiEdit |
| `deliverable-check` skill | `.claude/skills/deliverable-check/` | Pre-ship checklist: 14 writing and sourcing rules with line-level findings |
| `citation-checker` agent | `.claude/agents/citation-checker.md` | Audits every figure for a traceable source; flags invented numbers |
| `style-reviewer` agent | `.claude/agents/style-reviewer.md` | Catches structural/rhetorical problems a linter misses (slope, attribution, scaffolding) |
| Directory scaffold | `research/ analysis/ docs/ scripts/` | Where notes, analysis scripts, docs, and utilities live |

## The workflow it encodes

1. Research and draft in `research/` and `docs/`; the em-dash hook keeps prose clean as you write.
2. The memory system accumulates context across sessions (who the user is, feedback, project decisions).
3. Before anything ships to a stakeholder, run `deliverable-check`, then the `citation-checker` and `style-reviewer` subagents for number-heavy or external docs.

## Quick start

See `SETUP.md`. In short: copy this directory, replace every `{{PLACEHOLDER}}`,
customize the project glossary, and commit.
