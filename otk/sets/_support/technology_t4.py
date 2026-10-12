"""Phase 7 Technology wave T4 — reading and fixing short Python programs, ม.1-ม.2.

The knowledge halves of ``ว 4.2 ม.1/2`` (simple programs for mathematics and
science) and ``ม.2/2`` (programs using logic and functions). Writing and running
code needs an editor the product does not have, so these sets show a program in
a :class:`~otk.core.content.CodeBlock` — monospace, indentation kept — and ask
what it prints or which change fixes it:

* ``ม.1/2`` — trace assignments and arithmetic, trace a ``for`` loop, and pick
  the change that makes a maths or science program give the intended result.
* ``ม.2/2`` — follow ``if``/``elif``/``else``, trace functions, and fix a
  program whose logic or function is wrong.

Programs are ASCII only (Python 3). Trace answers are worked out here in plain
arithmetic; the fix sets run each candidate program to keep only changes that
really do not fix it, and the tests run every displayed program independently.
"""

from __future__ import annotations

import contextlib
import io
import re
from random import Random

from otk.core.content import code, text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion
from otk.sets._support.technology_t1s4 import _near

M1, M2 = {"th": "ม.1"}, {"th": "ม.2"}
FIX_HINT = ("ไล่โปรแกรมเดิมเพื่อดูว่าผิดที่บรรทัดใด แล้วลองแก้ตามแต่ละตัวเลือกและไล่ใหม่ "
            "ตัวเลือกที่ถูกต้องต้องทำให้ได้ผลตามที่ต้องการ")


def _question(stem: str, program: str, correct: str, wrongs, hint: str, topic: str):
    return GeneratedQuestion(
        stem=[text(stem), code(program)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


def _numbers(rng: Random, answer: int, slips) -> list[str]:
    return [str(w) for w in rng.sample(_near(answer, slips)[:5], 3)]


def output(program: str) -> str | None:
    """What ``program`` prints, lines joined by a space; ``None`` if it fails.

    Only ever runs programs built in this module from fixed templates.
    """
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            exec(program, {"__builtins__": {"print": print, "range": range}})  # otk: allow exec
    except Exception:
        return None
    return " ".join(out.getvalue().split())


def _lines(*lines: str) -> str:
    return "\n".join(lines)


# ══ ว 4.2 ม.1/2 ═══════════════════════════════════════════════════════════════


# ── fixing a program ─────────────────────────────────────────────────────────

_SWAPS = {" + ": (" - ", " * "), " - ": (" + ",), " * ": (" + ", " - "),
          " >= ": (" > ", " <= "), " > ": (" >= ", " < "), " <= ": (" < ", " >= "),
          " < ": (" <= ", " > "), " == ": (" != ",), " != ": (" == ",)}
_DATA = re.compile(r"^\s*\w+ = -?\d+$")


def variants(line: str) -> list[str]:
    """Plausible slips of one line: a swapped operator or comparison, or a range bound."""
    if line.lstrip().startswith(("def ", "else", "for i in range(1, n + 1)")) or _DATA.match(line):
        found: list[str] = []
    else:
        found = [line.replace(a, b, 1) for a, bs in _SWAPS.items() if a in line for b in bs]
    if "range(1, n + 1)" in line:
        found += [line.replace("range(1, n + 1)", "range(1, n)"), line.replace("range(1, n + 1)", "range(n)")]
    return [v for v in dict.fromkeys(found) if v != line]


def _fix(old: str, new: str) -> str:
    return f"เปลี่ยน {old.strip()} เป็น {new.strip()}"


def _fix_question(rng: Random, templates, topic: str):
    """A program with one slipped line; the change that restores the intended output."""
    while True:
        intent, program = rng.choice(templates)(rng)
        lines = program.split("\n")
        want = output(program)
        slips = [(i, v) for i, line in enumerate(lines) for v in variants(line)]
        rng.shuffle(slips)
        for index, slip in slips:
            broken = lines[:index] + [slip] + lines[index + 1:]
            got = output("\n".join(broken))
            if got is None or got == want:
                continue
            wrongs = []
            for other, line in enumerate(broken):
                for variant in variants(line):
                    tried = broken[:other] + [variant] + broken[other + 1:]
                    if output("\n".join(tried)) != want and variant.strip() != lines[other].strip():
                        wrongs.append(_fix(line, variant))
            wrongs = list(dict.fromkeys(wrongs))
            if len(wrongs) >= 3:
                return _question(
                    f"โปรแกรมนี้เขียนขึ้นเพื่อ{intent} ซึ่งควรแสดงผล {want} แต่แสดงผล {got} "
                    "ต้องแก้โปรแกรมอย่างไรจึงจะได้ผลที่ถูกต้อง",
                    "\n".join(broken), _fix(slip, lines[index]), rng.sample(wrongs, 3), FIX_HINT, topic)


# ══ ว 4.2 ม.2/2 ═══════════════════════════════════════════════════════════════


