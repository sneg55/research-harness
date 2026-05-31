# Project Instructions

> Template note: replace every `{{PLACEHOLDER}}` below and delete this line when
> you spin up a real project from this harness. See `SETUP.md`.

## Memory System

You have a persistent, file-based memory system. Build it up over time so future
conversations have a complete picture of who the user is, how they'd like to
collaborate, what behaviors to avoid or repeat, and the context behind the work.

If the user explicitly asks you to remember something, save it immediately as
whichever type fits best. If they ask you to forget something, find and remove
the relevant entry.

## Types of Memory

There are four discrete types. Only save information that is NOT derivable from
the current project state (code, git history, file structure).

### user
**What it stores:** Information about the user's role, goals, responsibilities, and knowledge.
**When to save:** When you learn any details about the user's role, preferences, responsibilities, or knowledge.
**How to use:** Tailor your behavior to the user's profile.

### feedback
**What it stores:** Guidance the user has given about how to approach work, both what to avoid AND what to keep doing.
**When to save:** Any time the user corrects your approach OR confirms a non-obvious approach worked.
**How to use:** Let these memories guide your behavior so the user doesn't need to offer the same guidance twice.
**Structure:** Lead with the rule, then a **Why:** line and a **How to apply:** line.

### project
**What it stores:** Information about ongoing work, goals, initiatives NOT derivable from files or git history.
**When to save:** When you learn who is doing what, why, or by when. Convert relative dates to absolute.
**Structure:** Lead with the fact/decision, then **Why:** and **How to apply:** lines.

### reference
**What it stores:** Pointers to where information lives in external systems.
**When to save:** When you learn about resources in external systems and their purpose.

## What NOT to Save

- File contents, document summaries, or research findings, derivable by reading the files
- Git history, `git log` is authoritative
- Anything already documented in CLAUDE.md
- Ephemeral task details or current conversation context

## Memory File Format

Each memory is its own `.md` file with YAML frontmatter:

```markdown
---
name: {{memory name}}
description: {{one-line description}}
type: {{user, feedback, project, reference}}
---

{{memory content}}
```

Store memory files in the `memory/` directory. Add a one-line pointer in
`memory/MEMORY.md`. (If your harness uses an auto-memory directory under
`~/.claude` instead, store them there and keep `memory/MEMORY.md` as the index.)

---

## Writing and Sourcing Discipline

These rules apply to all prose, analysis, and deliverables in this project.

### No time estimates

Never estimate work in hours, days, or weeks. Use concrete units instead: lines
of code, files touched, item counts, or token count. If the size is genuinely
unknown, say "unknown, need to read X first" rather than guessing in time units.

**Why:** time estimates for this kind of work are made up. They don't reflect
actual effort and mislead planning. Size estimates are verifiable.

### No made-up numbers

Never invent specific dollar amounts, percentages, market rates, comp data,
costs, or any other figures presented as factual. If real data isn't available,
either (a) do actual research (web search, ask the user for the source), or (b)
clearly label every figure as "illustrative" / "rough estimate" / "placeholder
pending research" and use round numbers, not fake-precision ones.

**Why:** pro-formas, market analyses, and strategic docs become misleading when
invented numbers are presented as researched. Tables of line items with specific
dollar amounts are especially dangerous because they imply precision.

**How to apply:**
1. Before citing any specific number, ask: do I actually know this, or am I
   generating a plausible-looking estimate?
2. Default assumption: when the user asks for analysis, they want researched
   numbers, not estimates. If research is required, say so and ask whether to
   proceed with research or with explicitly-labeled estimates.
3. If using a pro-forma table without researched inputs, every cell needs an
   "[est]" tag or the whole table needs a banner labeling it illustrative.
4. The rule covers: market prices, comp data, costs, tax rates, interest rates,
   conversion rates, traffic stats, audience sizes, salary ranges, and any other
   specific number that can be verified or sourced.

### No em dashes

Em dashes (U+2014) and horizontal bars (U+2015) are banned in all prose.
Replace with a comma, parentheses, two sentences, a colon, or "vs."/"or"/"to".
The `check-em-dash.py` PostToolUse hook enforces this at write time.

### Pre-ship gate

Before any document goes to a stakeholder, run the `deliverable-check` skill,
and for number-heavy docs the `citation-checker` and `style-reviewer` subagents.

---

## Git Safety

- Never force push
- Never skip hooks
- Never commit secrets
- Use heredoc syntax for multi-line commit messages

---

## Project-Specific Instructions

**Project:** {{PROJECT_NAME}}
**Description:** {{PROJECT_DESCRIPTION}}

**Stakeholders:** {{STAKEHOLDERS}} (named owners for internal deliverables)

**Project glossary:** list canonical terms vs banned synonyms, and the canonical
spelling of the project and product names. The `deliverable-check` skill and
`style-reviewer` agent enforce these.

### Repository Structure

- `research/`: research notes, analysis, and findings (Markdown)
- `analysis/`: scripts for data analysis and quick prototyping
- `docs/`: structured documentation and reference material
- `scripts/`: utility scripts
- `memory/`: persistent memory files plus the `MEMORY.md` index

### Conventions

- All research documents in Markdown
- Analysis scripts stay short and focused
- No build system, no dependencies unless truly necessary
