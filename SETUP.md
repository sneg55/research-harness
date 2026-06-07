# Setting up a new project from this harness

## 0. Prerequisites

- **Claude Code CLI** (required). This harness is built around Claude Code's
  skills, subagents, hooks, and memory system. Without it the em-dash hook won't
  fire and the skills and agents won't load, so the harness does nothing on its
  own. Install it from [claude.com/claude-code](https://claude.com/claude-code).
- **Python 3** for the em-dash hook (preinstalled on macOS and most Linux).
- **`gh`** (optional) only if you want Claude to create the GitHub repo for you.

## 1. Copy the harness

```bash
cp -R research-harness my-new-project
cd my-new-project
rm -rf .git           # start fresh history
git init
```

## 2. Fill in the placeholders

Search for `{{` and replace every placeholder. They live in:

- `CLAUDE.md`: `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{STAKEHOLDERS}}`,
  the project glossary block, and the template note at the top (delete it).
- `.claude/agents/citation-checker.md`: `{{PROJECT_NAME}}`, `{{PRIMARY_SOURCES}}`.
- `.claude/agents/style-reviewer.md`: `{{PROJECT_NAME}}`, `{{STAKEHOLDERS}}`,
  `{{STAKEHOLDER}}`, `{{PROJECT_GLOSSARY}}`.
- `.claude/skills/deliverable-check/SKILL.md`: the PROJECT GLOSSARY grep block
  in Step 1, and the glossary judgment in rule 6.

```bash
grep -rn '{{' . --include='*.md'      # find everything left to fill
```

## 3. Customize the project glossary

The `deliverable-check` skill and `style-reviewer` agent enforce your project's
canonical terms. For each term decide: preferred word, banned synonym, and any
context where the synonym is allowed (verbatim transcripts, imported reference
texts, a literal API param). Add a grep per banned term to the Step 1 scan block
in `SKILL.md`. Also pin the canonical spelling of the project and product names.

## 4. Verify the hooks fire

Two PostToolUse hooks are registered in `.claude/settings.json` and run on every
Write/Edit: `check-em-dash.py` (blocks em dashes, R1) and `check-prose.py` (flags
time estimates and unsourced figures, R14 and R2). The committed test exercises
both:

```bash
bash scripts/test-hooks.sh      # expect "hooks: 8 passed, 0 failed"
```

Run it again any time you edit a hook. (The hooks only flag `.md` files inside
`CLAUDE_PROJECT_DIR`, so a hand test path must be inside the project.)

## 5. Memory

Memory lives in **one** place: the repo `memory/` directory, with a one-line
pointer per file in `memory/MEMORY.md`. The format is in `memory/README.md`.

Claude Code also injects an auto-memory path under
`~/.claude/projects/<project-slug>/memory/`. To keep everything in the single
committed tree, that path must be a symlink to the repo's `memory/` directory.
`scripts/setup.sh` computes the slug and creates the link for you (it also runs
the placeholder check and the hook tests), so the simplest path is:

```bash
bash scripts/setup.sh
```

To do it by hand instead:

```bash
# <project-slug> is the project dir path with / replaced by - and a leading -,
# e.g. /Users/me/code/my-new-project -> -Users-me-code-my-new-project
slug=$(pwd | sed 's:/:-:g')
mkdir -p ~/.claude/projects/"$slug"
ln -s "$PWD/memory" ~/.claude/projects/"$slug"/memory
```

Now anything written to either path lands in the repo. Do not store memory in
`CLAUDE.local.md`; that file is for machine-specific, uncommitted prefs only.

## 6. First commit

```bash
git add -A
git commit -m "Initial project from research-harness"
```

## Notes

- `.claude/settings.local.json` is gitignored. Put machine-local permissions
  (allowed Bash commands, WebFetch domains) there, not in `settings.json`.
- Nothing here needs a build system or dependencies beyond Python 3 (for the hook)
  and, optionally, `gh` for repo creation.
