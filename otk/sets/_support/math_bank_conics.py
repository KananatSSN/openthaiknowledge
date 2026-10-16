"""Analytic-geometry sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found four units, exercised by A-level and กสพท questions
in ``openthaiknowledge-bank/rathcenter/7 เรขาคณิตวิเคราะห์ และภาคตัดกรวย``, that no
problem set practised. The existing conic sets start from a standard form
centred at the origin; the exams start from a general form or from foci:

=====================================  ==========================================  ============
unit                                   set                                         topic
=====================================  ==========================================  ============
conic.general-form                     math.conic_general_form_m4                  ภาคตัดกรวย
conic.focal-definition                 math.conic_focal_definition_m4              ภาคตัดกรวย
circle.tangency                        math.circle_tangency_m4                     สมการวงกลม
line.closest-point                     math.line_closest_point_m4                  สมการเส้นตรง
=====================================  ==========================================  ============

Every item is built backwards from integer choices (Pythagorean (a, b, c)
for the conics, the tangency point, the foot of the perpendicular), so every
answer is exact. ``test_math_bank_conics.py`` checks the results with SymPy
and pins the source exams' answers.
"""

from __future__ import annotations

from fractions import Fraction

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.kit.math_problems import frac_tex, poly_tex

M4 = {"th": "ม.4"}


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def line_tex(a: int, b: int, c: int) -> str:
    """ax + by + c = 0 with the leading coefficient made positive."""
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return poly_tex((a, "x"), (b, "y"), (c, "")) + " = 0"


def pt(x, y) -> str:
    f = lambda v: frac_tex(Fraction(v)) if Fraction(v).denominator != 1 else str(Fraction(v).numerator)
    return f"({f(x)}, {f(y)})"


def shifted(var: str, c: int) -> str:
    return var if c == 0 else f"({var} {'-' if c > 0 else '+'} {abs(c)})"


# ── Conics from their focal definition ───────────────────────────────────────


# ── Circles tangent to lines and axes ────────────────────────────────────────


# ── The nearest point on a line ──────────────────────────────────────────────


