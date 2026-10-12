"""Sets for gaps the (สสวท) จำนวนจริง textbook exercises exposed.

The chapter's seven files print their maths as pictures, so they were
transcribed by eye (``sheetpipe.transcript``). Claiming the 286 exercises
left three knowledge units without a set that practises them:

=====================================  ==========================================  =======================
unit                                   set                                         topic
=====================================  ==========================================  =======================
poly.division-algorithm                math.polynomial_long_division_m4            การหารพหุนาม
real.partial-fractions                 math.partial_fractions_m4                   สมการและอสมการเศษส่วน
abs.properties                         math.absolute_value_properties_m4           ค่าสัมบูรณ์
=====================================  ==========================================  =======================

``math.polynomial_division`` already divides by ``x − c``; the textbook
divides by quadratics and asks for the dividend back, which is what the first
set adds.

How each answer is decided:

- **Long division** is exact integer arithmetic on coefficient lists, and
  every item is built as ``a = b·q + r`` so the construction is the check.
  The named mistakes are real divisions too: of the dividend with its missing
  terms dropped, and by the divisor with its lower signs flipped (subtracting
  as if adding).
- **Partial fractions** pick the constants first and build the numerator
  from them; the cover-up rule must give them back.
- **Absolute-value statements** are decided by counterexample search over a
  grid of halves from −6 to 6.

``test_math_bank_textbook_real.py`` re-solves each family with SymPy.
"""

from __future__ import annotations

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.kit.math_problems import poly_tex

M4 = {"th": "ม.4"}


def _q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


# ── Polynomials as coefficient lists, highest degree first ───────────────────

def trim(p: list) -> list:
    i = 0
    while i < len(p) - 1 and p[i] == 0:
        i += 1
    return list(p[i:])


def ptex(p: list, var: str = "x") -> str:
    p = trim(p)
    deg = len(p) - 1
    syms = [f"{var}^{{{deg - i}}}" if deg - i > 1 else (var if deg - i == 1 else "")
            for i in range(deg + 1)]
    return poly_tex(*zip(p, syms))


# ── Partial fractions ────────────────────────────────────────────────────────


# ── Absolute-value statements ────────────────────────────────────────────────


