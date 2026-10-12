"""Problem-set code may only compute: no files, network, processes or imports
beyond plain maths.

Set modules (``otk/sets``, ``otk/kit``, ``otk/sheets``) run inside every consumer's
server — TutorRank's generator draws from them on each practice request — and
contributors write them with their own agents. This is the first line of
defence, not a sandbox: it keeps the obvious ways out of a module visible to
review. A line that genuinely needs a banned call says so with
``# otk: allow <name>`` and gets a reviewer's eyes (CODEOWNERS).

It also holds each set to a time budget, so one slow set cannot stall a
consumer's request.
"""

from __future__ import annotations

import ast
import time
from pathlib import Path
from random import Random

import pytest

from otk.core import REGISTRY

PACKAGE = Path(__file__).resolve().parents[1]
SET_CODE = [*sorted((PACKAGE / "sets").rglob("*.py")),
            *sorted((PACKAGE / "kit").rglob("*.py")),
            *sorted((PACKAGE / "sheets").rglob("*.py"))]
# Plumbing that reads the package's own data files, reviewed as part of otk itself.
INFRASTRUCTURE = {PACKAGE / "sheets" / "__init__.py", PACKAGE / "sets" / "__init__.py"}

ALLOWED_MODULES = {
    "__future__", "abc", "bisect", "cmath", "collections", "contextlib", "dataclasses",
    "decimal", "enum", "fractions", "functools", "hashlib", "heapq", "io", "itertools",
    "math", "numbers", "operator", "random", "re", "statistics", "string", "textwrap",
    "typing", "unicodedata",
    "numpy",  # olympiad solvers; installed with matplotlib
    "otk",
}
BANNED_CALLS = {"eval", "exec", "compile", "__import__", "open", "input", "breakpoint",
                "globals", "locals", "vars", "setattr", "delattr"}
# Five draws per set; the slowest takes ~1.6 s on a laptop.
SECONDS_PER_SET = 10.0


def _problems(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    found = []

    def allowed(node: ast.AST, name: str) -> bool:
        return f"# otk: allow {name}" in lines[node.lineno - 1]

    for node in ast.walk(ast.parse(source, str(path))):
        if isinstance(node, ast.Import):
            found += [f"{node.lineno}: import {a.name}" for a in node.names
                      if a.name.split(".")[0] not in ALLOWED_MODULES]
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            if (node.module or "").split(".")[0] not in ALLOWED_MODULES:
                found.append(f"{node.lineno}: from {node.module} import ...")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in BANNED_CALLS and not allowed(node, node.func.id):
                found.append(f"{node.lineno}: {node.func.id}(...)")
            if (node.func.id == "getattr" and len(node.args) > 1
                    and isinstance(node.args[1], ast.Constant)
                    and str(node.args[1].value).startswith("__")):
                found.append(f"{node.lineno}: getattr(..., {node.args[1].value!r})")
        elif isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            found.append(f"{node.lineno}: .{node.attr}")
    return found


@pytest.mark.parametrize("path", [p for p in SET_CODE if p not in INFRASTRUCTURE],
                         ids=lambda p: p.relative_to(PACKAGE).as_posix())
def test_set_code_only_computes(path):
    problems = _problems(path)
    assert not problems, (
        "set code may not do this (mark a reviewed exception with '# otk: allow <name>'):\n"
        + "\n".join(problems))


def test_the_check_catches_what_it_should(tmp_path):
    bad = tmp_path / "bad.py"
    bad.write_text("import os\nfrom urllib import request\nx = open('f')\n"
                   "y = ().__class__\nz = getattr(x, '__globals__')\n"
                   "eval('1')  # otk: allow eval\n", encoding="utf-8")
    assert [p.split(":")[0] for p in _problems(bad)] == ["1", "2", "3", "4", "5"]


@pytest.mark.parametrize("key", sorted(REGISTRY))
def test_a_set_draws_within_its_time_budget(key):
    started = time.perf_counter()
    for seed in (0, 1, 2, 20260824, 2**31 - 1):
        REGISTRY[key].generate(Random(seed))
    assert time.perf_counter() - started < SECONDS_PER_SET
