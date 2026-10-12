"""Sets for gaps the rathcenter 🍰 lecture books exposed.

Converting the books (``answerkey`` reads each one against the key bound at
its back) and claiming their exercise sections left three knowledge units
with no problem set:

=====================================  ==========================================  ============
unit                                   set                                         topic
=====================================  ==========================================  ============
series.sigma                           math.sigma_sums_m6                          อนุกรม
radical.equations                      math.radical_equation_m4                    จัดรูปกรณฑ์
counting.stars-bars                    math.stars_bars_m5                          หลักการนับ
=====================================  ==========================================  ============

``test_math_bank_notes.py`` checks the sums term by term, substitutes every
radical-equation root back (and shows the extraneous one fails), and counts
distributions by enumeration.
"""

from __future__ import annotations

from fractions import Fraction

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.kit.math_problems import frac_tex

M4, M5, M6 = {"th": "ม.4"}, {"th": "ม.5"}, {"th": "ม.6"}


def num(v) -> str:
    v = Fraction(v)
    return f"{v.numerator:,}".replace(",", "{,}") if v.denominator == 1 else frac_tex(v)


def _q(stem: list, right, named: list, topic: str) -> GeneratedQuestion:
    right = Fraction(right)
    pool = [*named, right + 1, right - 1, right * 2, right + 2]
    wrongs = [w for w in dict.fromkeys(num(Fraction(w)) for w in pool if w is not None) if w != num(right)][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(num(right))],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


# ── Σ sums ───────────────────────────────────────────────────────────────────


# ── Radical equations ────────────────────────────────────────────────────────


# ── Stars and bars ───────────────────────────────────────────────────────────


