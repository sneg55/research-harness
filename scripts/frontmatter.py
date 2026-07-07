"""Minimal YAML-frontmatter handling for the repo's markdown files.

No third-party deps (honours the harness's Python-3-only rule). Supports only the
small YAML subset this convention uses in frontmatter:

    ---
    status: working
    summary: One line about the file.
    tags: [markets, onchain]
    supersedes: ../old.md
    superseded_by: null
    ---

Scalars, `null`, and inline `[a, b, c]` lists. That is all the schema needs.

Crucially, `parse()` distinguishes a real frontmatter block from a leading `---`
markdown horizontal rule: a doc may open with `---` as a rule followed by prose,
and that must NOT be mistaken for metadata. A candidate block only counts as
frontmatter if every non-blank inner line is a `key: value` pair (or an
inline-list value); a heading or prose line disqualifies it.
"""

import re

_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*:(\s|$)")

# Frontmatter keys we emit, in the order they should serialize.
FIELD_ORDER = [
    "status",
    "summary",
    "version",
    "tags",
    "audience",
    "supersedes",
    "superseded_by",
]


def _looks_like_yaml(block: str) -> bool:
    """True only if every non-blank line is a `key:` line (our flat schema)."""
    saw_key = False
    for line in block.split("\n"):
        if not line.strip():
            continue
        if not _KEY_RE.match(line):
            return False
        saw_key = True
    return saw_key


def _parse_scalar(raw: str):
    raw = raw.strip()
    if raw == "" or raw.lower() == "null" or raw == "~":
        return None
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [_unquote(x.strip()) for x in inner.split(",") if x.strip()]
    return _unquote(raw)


def _unquote(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def split(text: str):
    """Return (frontmatter_block_str_or_None, body_str).

    frontmatter_block excludes the `---` delimiters. body is everything after
    the closing delimiter (leading newline trimmed).
    """
    if not text.startswith("---"):
        return None, text
    lines = text.split("\n")
    if lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            block = "\n".join(lines[1:i])
            if not _looks_like_yaml(block):
                return None, text
            body = "\n".join(lines[i + 1 :])
            return block, body.lstrip("\n")
    return None, text  # no closing delimiter -> not frontmatter


def parse(text: str):
    """Return (dict_of_fields, body). Empty dict if no valid frontmatter."""
    block, body = split(text)
    if block is None:
        return {}, text
    data = {}
    for line in block.split("\n"):
        if not line.strip():
            continue
        key, _, val = line.partition(":")
        data[key.strip()] = _parse_scalar(val)
    return data, body


def strip(text: str) -> str:
    """Return body with any valid frontmatter removed.

    Useful when publishing a doc to a surface that should not show the repo's
    internal metadata block (e.g. a Google Doc or a rendered page).
    """
    _, body = parse(text)
    return body


def _serialize_value(val) -> str:
    if val is None:
        return "null"
    if isinstance(val, list):
        return "[" + ", ".join(str(v) for v in val) + "]"
    s = str(val)
    # Quote scalars that would confuse the flat parser (colon, leading list/quote).
    if s == "" or s[0] in "[\"'#" or ": " in s or s.endswith(":"):
        return '"' + s.replace('"', '\\"') + '"'
    return s


def render(fields: dict) -> str:
    """Serialize a fields dict to a `---`-delimited block (with trailing newline)."""
    out = ["---"]
    for key in FIELD_ORDER:
        if key in fields:
            out.append(f"{key}: {_serialize_value(fields[key])}")
    for key, val in fields.items():
        if key not in FIELD_ORDER:
            out.append(f"{key}: {_serialize_value(val)}")
    out.append("---")
    return "\n".join(out) + "\n"
