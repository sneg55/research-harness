# research-harness

A reusable Claude Code setup for research and deliverable-writing projects. Clone
it, fill in the placeholders, and you start with a memory system, writing/sourcing
discipline, and pre-ship quality gates already wired up.

## Setup

### Prerequisite

You need the **Claude Code CLI**. This harness is built around Claude Code's
skills, subagents, hooks, and memory system; without it the hooks won't fire and
the skills and agents won't load. Install it from
[claude.com/claude-code](https://claude.com/claude-code), then open this repo as
your working directory.

> The em-dash hook needs Python 3 (preinstalled on macOS and most Linux). `gh` is
> optional, only for creating the GitHub repo.

### Fastest: let the agent set it up

Open this repo in Claude Code and say:

> read SETUP.md and set up my project from this harness

Claude reads `SETUP.md` and `CLAUDE.md`, then walks you through filling the
placeholders, customizing the project glossary, and making the first commit.

### Manual

```bash
cp -R research-harness my-new-project
cd my-new-project
rm -rf .git && git init
grep -rn '{{' . --include='*.md'   # every placeholder left to fill
```

Then follow `SETUP.md` step by step: replace each `{{PLACEHOLDER}}`, customize the
glossary, verify the hook fires, and commit.

### Using the skills in another project

The bundled skills (`deliverable-check`, `dream`, `remember`) live in
`.claude/skills/` and are available automatically once this repo is your working
directory. To pull them into a different project, copy the folder you want from
`.claude/skills/` into that project's `.claude/skills/`.

## What's inside

| Piece | Path | Does |
| --- | --- | --- |
| Project instructions | `CLAUDE.md` | Memory system, git safety, writing/sourcing discipline, project placeholders |
| Writing rules (canonical) | `docs/writing-rules.md` | The 14 rules (R1 to R14) in one place; the skill and agents reference it so nothing drifts |
| Memory scaffold | `memory/` | `MEMORY.md` index plus the four-type memory format documented |
| Research note template | `research/TEMPLATE.md` | Starting point for a note, with `[S#]` source markers and a Sources block |
| Em-dash hook | `.claude/hooks/check-em-dash.py` | PostToolUse hook that blocks em dashes in Markdown at write time |
| Prose hook | `.claude/hooks/check-prose.py` | PostToolUse hook that flags time estimates (R14) and unsourced figures (R2) at write time |
| Hook wiring | `.claude/settings.json` | Registers both hooks on Write/Edit/MultiEdit |
| `deliverable-check` skill | `.claude/skills/deliverable-check/` | Pre-ship checklist: mechanical scans plus a judged pass against R1 to R14 |
| `dream` skill | `.claude/skills/dream/` | Consolidates memory: review, merge, prune, and re-index memory files |
| `remember` skill | `.claude/skills/remember/` | Reviews loose memory entries and proposes promotions to CLAUDE.md or shared memory |
| `citation-checker` agent | `.claude/agents/citation-checker.md` | Validates every figure against recorded `[S#]` sources; web search is the fallback |
| `style-reviewer` agent | `.claude/agents/style-reviewer.md` | Catches structural/rhetorical problems a linter misses (slope, attribution, scaffolding) |
| Setup + test scripts | `scripts/` | `setup.sh`, `check-setup.sh`, `test-hooks.sh` |
| Directory scaffold | `research/ analysis/ docs/ scripts/` | Where notes, analysis scripts, docs, and utilities live |

## Folder structure

```
research-harness/
├── CLAUDE.md            Project instructions Claude loads every session
├── README.md           This file
├── SETUP.md            How to spin up a real project from the template
├── research/           Research notes, analysis, and findings (Markdown)
│   └── TEMPLATE.md       Copy to start a note: source markers + Sources block
├── analysis/           Short, focused scripts for data analysis and prototyping
├── docs/               Structured documentation and reference material
│   └── writing-rules.md  Canonical R1 to R14; the skill and agents reference it
├── scripts/            setup.sh, check-setup.sh, test-hooks.sh
├── memory/             Persistent memory files plus the MEMORY.md index
│   ├── MEMORY.md         The index loaded into context each session
│   └── README.md         The four memory types and the file format
└── .claude/
    ├── settings.json     Hook wiring (shared); settings.local.json is per-machine
    ├── hooks/            check-em-dash.py, check-prose.py
    ├── skills/           deliverable-check, dream, remember
    └── agents/           citation-checker, style-reviewer
```

What goes where:

- **`research/`** holds the thinking: notes, drafts, findings. One topic per file.
- **`docs/`** holds the polished, structured output other people read.
- **`analysis/`** holds throwaway and reusable scripts. Keep them short and focused.
- **`memory/`** is not for documents. It holds one durable fact per file, indexed
  by `MEMORY.md`. See the digest and memory sections below.

## Best practices for using this harness

1. **Let the memory system carry context across sessions.** Don't re-explain who
   you are or what the project is each time. When Claude learns something durable
   (your role, a decision, a correction), it writes a memory file and indexes it in
   `memory/MEMORY.md`. That index loads every session so the next conversation
   starts oriented. See `memory/README.md` for the four types and the format.
2. **Save the non-obvious, not the derivable.** Never store anything Claude can get
   from the code, `git log`, the file tree, or `CLAUDE.md`. Memory is for context
   that lives only in your head or in a conversation: why a call was made, what to
   avoid, who owns what.
3. **Correct once.** When Claude does something the wrong way, say so. The
   correction becomes a `feedback` memory so you don't repeat it. Confirmations of
   a non-obvious approach that worked are worth saving too.
4. **Write prose clean from the start.** Two write-time hooks keep drafts
   compliant without a cleanup pass: `check-em-dash.py` blocks em dashes, and
   `check-prose.py` flags time estimates and unsourced figures. The full rule set
   (R1 to R14) lives in `docs/writing-rules.md`.
5. **Gate every stakeholder deliverable.** Before a doc leaves the project, run the
   `deliverable-check` skill. For number-heavy or external docs, also run the
   `citation-checker` and `style-reviewer` subagents. Run the `humanizer` skill
   once content is locked.
6. **Tend the memory store.** Run `dream` and `remember` periodically (see below)
   so the store stays accurate and the index stays short.

## Memory hygiene: dream and remember

Two skills keep the memory store healthy. They work on the files in `memory/`
(and any auto-memory directory under `~/.claude` if your harness uses one).

### dream

`dream` is a consolidation pass. Run it periodically, or after a stretch of heavy
work, to keep memories organized instead of letting them sprawl. It:

- orients on what already exists (`MEMORY.md` plus the topic files),
- gathers recent signal worth persisting,
- merges new facts into existing files rather than creating near-duplicates,
- converts relative dates ("last week") to absolute ones,
- deletes facts the latest work has contradicted, and
- prunes and re-indexes `MEMORY.md` so it stays a short index, not a dump.

Invoke it with the `dream` skill (or `/dream`). It reports what it consolidated,
updated, or pruned, and says so plainly when nothing changed.

### remember

`remember` reviews loose or auto-captured memory entries and proposes where each
belongs: project-wide `CLAUDE.md`, personal `CLAUDE.local.md`, shared/team memory,
or staying put. It also flags duplicates, outdated entries, and conflicts across
layers. It only proposes; it does not apply changes without your approval.

Use `dream` to compress and re-index what's already saved. Use `remember` when you
want to decide whether a working note should graduate into a durable instruction.

## Digesting meeting notes

Meetings produce decisions, owners, and dates: exactly the `project` and `feedback`
context the memory system exists to hold. The digest workflow turns a transcript or
notes file into durable memory and, where useful, a research note. It does not dump
the transcript into the repo.

1. **Bring in the notes.** Paste them, point Claude at a file in `research/`, or
   pull them from a connected meeting source (this harness can read from a
   Circleback MCP if configured) by meeting, date, or search term.
2. **Extract, don't transcribe.** Claude pulls out decisions, action items with
   owners, deadlines, and any correction to how the work should be done. Raw
   transcript text stays out of the repo.
3. **Route each item:**
   - Decisions, owners, and dates become `project` memories (relative dates
     converted to absolute).
   - "Do it this way from now on" guidance becomes a `feedback` memory.
   - Pointers to where something lives (a doc, a ticket, a dashboard) become a
     `reference` memory.
   - Substantive findings or analysis that the team will read become a note in
     `research/`, not a memory.
4. **Index and dedupe.** Each new memory gets a one-line pointer in `MEMORY.md`,
   merged into an existing file when one already covers the topic. Run `dream`
   afterward if a digest produced several overlapping entries.

The test for memory versus a document: if it's one durable fact the next session
needs to start oriented, it's a memory. If it's something a person sits down to
read, it's a note in `research/` or `docs/`.

## The workflow it encodes

1. Research and draft in `research/` and `docs/`; the em-dash hook keeps prose clean as you write.
2. The memory system accumulates context across sessions (who the user is, feedback, project decisions); `dream` and `remember` keep it tidy.
3. Meeting notes get digested into memory and, where warranted, a research note.
4. Before anything ships to a stakeholder, run `deliverable-check`, then the `citation-checker` and `style-reviewer` subagents for number-heavy or external docs.

## More detail

Full step-by-step setup, including the hook-fires test and the
`settings.local.json` note, is in `SETUP.md`.
