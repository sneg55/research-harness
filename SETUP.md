# Setting up a new project from this harness

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

Memory files go in `memory/` with a one-line pointer in `memory/MEMORY.md`. If
your Claude Code harness uses an auto-memory directory under `~/.claude` instead,
store the files there and keep `memory/MEMORY.md` as the in-repo index. Either
way the format in `memory/README.md` applies.

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
