"""ฟังก์ชัน-chapter sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found five units, exercised by A-level, กสพท and O-NET
questions in ``openthaiknowledge-bank/rathcenter/4 ฟังก์ชัน``, that no problem set
practised:

=====================================  ==========================================  =========================
unit                                   set                                         topic
=====================================  ==========================================  =========================
function.piecewise                     math.piecewise_function_m4                  ความสัมพันธ์และฟังก์ชัน
function.graph-inequality              math.graph_inequality_parameters_m4         ความสัมพันธ์และฟังก์ชัน
function.relation-pairs                math.relation_pairs_m4                      ความสัมพันธ์และฟังก์ชัน
function.transformations               math.graph_transform_point_m4               ฟังก์ชัน
derivative.composite                   math.derivative_chain_m5                    อนุพันธ์
=====================================  ==========================================  =========================

Answers are exact (``Fraction``). Where an item states a condition and asks
for constants, the constants are solved from the stated numbers alone, and
``_agree`` checks them against the hidden ones. ``test_math_bank_functions.py``
re-derives each family with SymPy and pins the source exams' answers.
"""

from __future__ import annotations

from fractions import Fraction

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.kit.math_problems import frac_tex

M4, M5 = {"th": "ม.4"}, {"th": "ม.5"}


def _agree(solved, truth):
    if solved != truth:                                    # pragma: no cover
        raise AssertionError(f"solver gave {solved}, the construction says {truth}")
    return solved


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def _frac_q(stem: list, right: Fraction, named: list, topic: str) -> GeneratedQuestion:
    """A rational answer with named mistakes, padded by ±1, ±2 when they collide."""
    out: list[str] = []
    for w in [*named, right + 1, right - 1, right + 2, right - 2]:
        t = frac_tex(Fraction(w))
        if t != frac_tex(right) and t not in out:
            out.append(t)
        if len(out) == 3:
            break
    return _tex_q(stem, frac_tex(right), out, topic)


def _minus(n) -> str:
    return str(n).replace("-", "−")


# ── Piecewise functions ──────────────────────────────────────────────────────


# ── Constants from where two graphs meet ─────────────────────────────────────


# ── Relations as sets of pairs ───────────────────────────────────────────────


# ── Shifts and reflections ───────────────────────────────────────────────────


# ── The chain rule ───────────────────────────────────────────────────────────

