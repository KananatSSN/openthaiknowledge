"""Statistics sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found two units, exercised by กสพท, A-level and O-NET
questions in ``openthaiknowledge-bank/rathcenter/16 สถิติ``, that no problem set
practised. The existing sets compute a measure from data they print; the
exams hide data behind conditions or hand over sums and transforms:

=====================================  ==========================================  ================
unit                                   set                                         topic
=====================================  ==========================================  ================
stats.data-from-conditions             math.stats_data_conditions_m6               ค่ากลางของข้อมูล
stats.transform-sums                   math.stats_transform_m6                     การวัดการกระจาย
=====================================  ==========================================  ================

Hidden data are recovered by brute force over every candidate, and a draw is
kept only when the asked quantity is determined uniquely.
``test_math_bank_stats.py`` rechecks the answers with ``statistics`` and
brute force, and pins the source exams' answers.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.kit.math_problems import frac_tex

M6 = {"th": "ม.6"}


def num(v) -> str:
    """Fractions as decimals when they terminate within two places, else as \\frac."""
    v = Fraction(v)
    if v.denominator == 1:
        return f"{v.numerator:,}".replace(",", "{,}")
    for places in (1, 2):
        if (v * 10 ** places).denominator == 1:
            s = f"{float(v):.{places}f}"
            return s
    return frac_tex(v)


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """Named mistakes first; duplicates and the answer itself dropped; three kept."""
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def _num_q(stem: list, right, named: list, topic: str) -> GeneratedQuestion:
    right = Fraction(right)
    pool = [*named, right + 1, right - 1, right + 2, right * 2, right - 2]
    return _tex_q(stem, num(right), [num(w) for w in pool if w is not None], topic)


def median(xs) -> Fraction:
    s = sorted(xs)
    n = len(s)
    return Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)


def modes(xs) -> list:
    c = Counter(xs)
    top = max(c.values())
    return sorted(v for v, k in c.items() if k == top)


# ── Data from conditions ─────────────────────────────────────────────────────


# ── Transforms and sums of squares ───────────────────────────────────────────


