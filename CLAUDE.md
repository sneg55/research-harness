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

### Where memory lives (single source of truth)

The repo `memory/` directory is the **only** place memories are stored. Each
memory is one `.md` file there, indexed by a one-line pointer in
`memory/MEMORY.md`. This tree is checked into git, so memory travels with the
project.

Do **not** write memories to any other location. In particular:

- The harness auto-memory path
  (`~/.claude/projects/<project>/memory/`) is symlinked to this repo's `memory/`
  directory, so anything the harness writes there lands in the committed tree.
  If you set this project up on a new machine, recreate that symlink:
  `ln -s <repo>/memory ~/.claude/projects/<project-slug>/memory`
- `CLAUDE.local.md` (if present) is for machine-specific, **uncommitted**
  preferences and overrides only. It is gitignored and is **not** a place to
  store memory entries. Memories always go in `memory/`.

When you save a memory: write the file in `memory/`, then add its one-line
pointer to `memory/MEMORY.md`.

---

## Writing and Sourcing Discipline

The full, numbered rule set (R1 to R14) lives in `docs/writing-rules.md`. That
file is the single source of truth; the `deliverable-check` skill and the
`citation-checker` and `style-reviewer` agents reference it by R-number. Read it
before writing any deliverable. The three rules the project owner is most burned
by, in brief:

- **No made-up numbers (R2).** Never present an invented figure as fact. Source
  it, label it illustrative with round numbers, or cut it. In `research/` notes
  every figure carries a `[S#]` marker resolving to the note's Sources block.
- **No time estimates (R14).** Never size work in hours, days, or weeks. Use
  concrete units: lines of code, files touched, item counts, token count.
- **No em dashes (R1).** Banned in all prose. Replace with a comma, parentheses,
  two sentences, a colon, or "vs."/"or"/"to".

Two PostToolUse hooks enforce these at write time on Markdown files:
`check-em-dash.py` (R1, hard block) and `check-prose.py` (R2 and R14, advisory).

**Pre-ship gate.** Before any document goes to a stakeholder, run the
`deliverable-check` skill, and for number-heavy docs the `citation-checker` and
`style-reviewer` subagents.

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

- All research documents in Markdown. Start a note from `research/TEMPLATE.md`.
- Provenance as you go: every specific figure or factual claim in a `research/`
  note carries a `[S#]` source marker that resolves to the note's `## Sources`
  block. This is what `citation-checker` validates and `check-prose.py` looks for.
- Analysis scripts stay short and focused
- No build system. The only dependency is Python 3 (for the hooks) and bash (for
  the `scripts/` helpers).

### Scripts

- `scripts/setup.sh`: one-shot setup for a project spun up from the harness
  (memory symlink, placeholder check, hook tests). Idempotent.
- `scripts/check-setup.sh`: fails if any `{{PLACEHOLDER}}` is unfilled.
- `scripts/test-hooks.sh`: committed tests for both write-time hooks. Run after
  editing a hook.
