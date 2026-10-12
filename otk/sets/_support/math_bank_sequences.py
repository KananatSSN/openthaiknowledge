"""Sequence, series and compounding sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found units, exercised by กสพท, A-level and O-NET
questions in ``sheet_database/rathcenter/14 ลำดับและอนุกรม``, that no problem
set practised. The existing sets give the first term and the common
difference or ratio; the exams hide them:

=====================================  ==========================================  ================
unit                                   set                                         topic
=====================================  ==========================================  ================
sequence.arithmetic-tricks             math.arithmetic_series_tricks_m6            ลำดับเลขคณิต
sequence.patterns                      math.sequence_patterns_m6                   ลำดับเลขคณิต
sequence.geometric-tricks              math.geometric_series_tricks_m6             ลำดับเรขาคณิต
series.telescoping                     math.telescoping_series_m6                  อนุกรม
finance.compounding-periods            math.compounding_periods_m5                 ลำดับและอนุกรม
sequence.terms                         math.sequence_terms_m6                      ลำดับเลขคณิต
=====================================  ==========================================  ================

Everything is ``Fraction`` arithmetic from integer or small rational draws.
``test_math_bank_sequences.py`` recomputes every answer term by term (or with
SymPy's summation) and pins the source exams' answers.
"""

from __future__ import annotations

from fractions import Fraction

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.kit.math_problems import frac_tex

M6 = {"th": "ม.6"}


def num(v) -> str:
    """Integers with a thousands separator, other fractions as \\frac."""
    v = Fraction(v)
    if v.denominator == 1:
        return f"{v.numerator:,}".replace(",", "{,}")
    return frac_tex(v)


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """Named mistakes first; duplicates and the answer itself dropped; three kept."""
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def _num_q(stem: list, right, named: list, topic: str) -> GeneratedQuestion:
    right = Fraction(right)
    pool = [*named, right + 1, right - 1, right * 2, -right, right + 2]
    return _tex_q(stem, num(right), [num(w) for w in pool if w is not None], topic)


# ── Arithmetic-series tricks ─────────────────────────────────────────────────


# ── Patterns: second differences, Sₙ, recurrences ────────────────────────────


# ── Geometric ratio tricks ───────────────────────────────────────────────────


# ── Telescoping sums ─────────────────────────────────────────────────────────


# ── Compounding several times a year ─────────────────────────────────────────


# ── Terms from a general term or a recursion ─────────────────────────────────


