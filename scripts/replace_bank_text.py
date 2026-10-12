"""Replace string constants in a Python module by their value.

A helper for the MCQ guessability rewrite (docs/for_admin/MCQ_GUESSABILITY.md).
Bank texts are often split over lines by implicit concatenation, so a plain
text search misses them; this finds each constant by its *value* with ``ast``
and rewrites its whole source span as one literal.

    import sys; sys.path.insert(0, "scripts")
    from replace_bank_text import replace
    replace("otk/core/types/science_wave_b.py", {"<old value>": "<new value>", ...})

Every old value must occur as a whole string constant (f-strings are left
alone); one that occurs more than once is skipped with a message. ``ast`` columns count UTF-8 bytes; they are converted to
characters for Thai text.
"""

from __future__ import annotations

import ast


def _char_col(line: str, byte_col: int) -> int:
    return len(line.encode("utf8")[:byte_col].decode("utf8"))


def replace(path: str, changes: dict[str, str], *, every: bool = False) -> None:
    source = open(path, encoding="utf8").read()
    lines = source.split("\n")
    found: dict[str, list[ast.Constant]] = {old: [] for old in changes}
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in found:
            found[node.value].append(node)
    missing = [old for old, nodes in found.items() if not nodes]
    assert not missing, f"not found: {missing}"
    # A value used twice (one row's answer is another row's distractor) is
    # skipped rather than guessed at; the caller rewrites it another way.
    # ``every=True`` rewrites all of them, for a change that is right wherever
    # the value appears (a term gaining its gloss).
    if not every:
        for old in [old for old, nodes in found.items() if len(nodes) > 1]:
            print(f"skipped, appears {len(found[old])} times: {old}")
            del found[old]
    # Offsets as (line, char col) pairs, applied bottom-up so earlier ones stay valid.
    spans = []
    for old, nodes in found.items():
        new = changes[old]
        literal = '"' + new + '"' if '"' not in new and "\\" not in new else repr(new)
        for node in nodes:
            start = (node.lineno - 1, _char_col(lines[node.lineno - 1], node.col_offset))
            end = (node.end_lineno - 1, _char_col(lines[node.end_lineno - 1], node.end_col_offset))
            spans.append((start, end, literal))
    for (sl, sc), (el, ec), literal in sorted(spans, reverse=True):
        head, tail = lines[sl][:sc], lines[el][ec:]
        lines[sl:el + 1] = [head + literal + tail]
    open(path, "w", encoding="utf8", newline="\n").write("\n".join(lines))
