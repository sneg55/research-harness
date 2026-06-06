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

## 4. Verify the hook fires

The em-dash hook is registered in `.claude/settings.json` and runs on every
Write/Edit. Test it:

```bash
printf '# t\nan em dash \xe2\x80\x94 here\n' > /tmp/t.md
CLAUDE_PROJECT_DIR="$PWD" python3 .claude/hooks/check-em-dash.py <<'JSON'
{"tool_input": {"file_path": "/tmp/t.md"}}
JSON
echo "exit: $?"   # expect exit 2 and a flagged line
```

(The hook only flags files inside `CLAUDE_PROJECT_DIR`, so the test path must be
inside the project, or set `CLAUDE_PROJECT_DIR` to the file's directory.)

## 5. Memory

Memory lives in **one** place: the repo `memory/` directory, with a one-line
pointer per file in `memory/MEMORY.md`. The format is in `memory/README.md`.

Claude Code also injects an auto-memory path under
`~/.claude/projects/<project-slug>/memory/`. To keep everything in the single
committed tree, symlink that path to the repo's `memory/` directory after
`git init`:

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
