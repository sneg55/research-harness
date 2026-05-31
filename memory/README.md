# memory/

Persistent, file-based memory. Each memory is one `.md` file holding one fact,
indexed by a one-line pointer in `MEMORY.md`. `MEMORY.md` is the index loaded
into context each session; the individual files are recalled on relevance.

Save only information NOT derivable from the project state (code, git history,
file structure).

## Four types

| Type | Stores | Save when |
| --- | --- | --- |
| `user` | The user's role, goals, responsibilities, knowledge, preferences | You learn anything about who the user is |
| `feedback` | Guidance on how to work, both corrections and confirmed approaches | The user corrects your approach or confirms a non-obvious one worked |
| `project` | Ongoing work, goals, decisions not in files or git | You learn who is doing what, why, or by when (convert relative dates to absolute) |
| `reference` | Pointers to where info lives in external systems | You learn about an external resource and its purpose |

## File format

```markdown
---
name: short-kebab-case-slug
description: one-line summary used to decide relevance during recall
type: user | feedback | project | reference
---

The fact. For feedback/project, follow with **Why:** and **How to apply:** lines.
Link related memories with [[their-slug]].
```

## Rules

- Before saving, check for an existing file that already covers it; update that
  file rather than duplicating.
- Delete memories that turn out to be wrong.
- Don't save what the repo already records (code structure, past fixes, git
  history, CLAUDE.md).
- After writing a file, add its one-line pointer to `MEMORY.md`.
