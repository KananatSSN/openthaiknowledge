"""Append one wrong answer to bank rows, located by their correct answer.

A helper for the MCQ guessability rewrite (docs/for_admin/MCQ_GUESSABILITY.md):
several banks promise a fixed number of wrongs per row (the technology tests
hold five), so a rewrite that drops one must add one back.

    import sys; sys.path.insert(0, "scripts")
    from append_bank_wrongs import append
    append("otk/core/types/technology_t1.py", {"<correct text>": "<new wrong>", ...})

Rows are tuples ``(lead, correct, (wrong, ...))``. The new wrong goes in as the
last element of the wrongs tuple, on its own line, matching the indentation of
the previous wrong.
"""

from __future__ import annotations

import ast


def append(path: str, additions: dict[str, str]) -> None:
    source = open(path, encoding="utf8").read()
    tree = ast.parse(source)
    lines = source.split("\n")
    # (line index, column) of the wrongs tuple's closing paren, per correct text
    targets: dict[str, tuple[ast.Tuple, ast.expr]] = {}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Tuple) and len(node.elts) >= 3
                and isinstance(node.elts[1], ast.Constant) and isinstance(node.elts[1].value, str)
                and isinstance(node.elts[2], ast.Tuple)):
            correct = node.elts[1].value
            if correct in additions:
                assert correct not in targets, f"correct text appears in two rows: {correct}"
                targets[correct] = node.elts[2]
    missing = set(additions) - set(targets)
    assert not missing, f"rows not found: {missing}"
    edits = []
    for correct, wrongs in targets.items():
        new = additions[correct]
        existing = [e.value for e in wrongs.elts if isinstance(e, ast.Constant)]
        assert new not in existing and new != correct, new
        last = wrongs.elts[-1]
        # ast columns count UTF-8 bytes; Thai text needs them as characters.
        line_bytes = lines[last.end_lineno - 1].encode("utf8")
        end_col = len(line_bytes[:last.end_col_offset].decode("utf8"))
        start_bytes = lines[last.lineno - 1].encode("utf8")
        indent = " " * len(start_bytes[:last.col_offset].decode("utf8"))
        # Insert after the last element (before any trailing comma/paren).
        quoted = '"' + new + '"' if '"' not in new else repr(new)
        edits.append((last.end_lineno - 1, end_col, f",\n{indent}{quoted}"))
    for line, col, text in sorted(edits, reverse=True):
        lines[line] = lines[line][:col] + text + lines[line][col:]
    open(path, "w", encoding="utf8", newline="\n").write("\n".join(lines))
