"""จำนวนจริง-chapter sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found units of the real-numbers chapter that no problem
set practised, all exercised by กสพท and O-NET questions in
``openthaiknowledge-bank/rathcenter/3 จำนวนจริง``. The chapter spans several registry
topics, so each set is filed with the existing sets of its own topic:

=====================================  ==========================================  ==============
unit                                   set                                         topic
=====================================  ==========================================  ==============
ineq.integer-count                     math.inequality_integer_count_m4            อสมการกำลังสอง
ineq.solution-to-parameters            math.inequality_parameters_m4               อสมการกำลังสอง
abs.piecewise-equation                 math.absolute_value_multi_equation_m4       ค่าสัมบูรณ์
abs.integer-solutions                  math.absolute_value_integer_count_m4        ค่าสัมบูรณ์
poly.unknown-coefficients              math.polynomial_unknown_coefficients_m4     การหารพหุนาม
real.order-properties                  math.inequality_order_properties_m3         อสมการเชิงเส้น
quad.discriminant                      math.quadratic_discriminant_m3              สมการกำลังสอง
real.remainders                        math.remainder_arithmetic_m4                การหารพหุนาม
=====================================  ==========================================  ==============

How each answer is decided:

- **Counts of integer solutions** come from an exact scan with integer and
  ``Fraction`` arithmetic, over a range that the item's construction proves
  contains every solution.
- **Absolute-value equations** use an exact piecewise-linear solver.
- **Coefficient items** answer from the stated conditions only. Each item
  asserts that this recovers the hidden polynomial.
- **Order-property statements** are decided by counterexample search over a
  grid of rationals.

``test_math_bank_real.py`` re-solves every item family with SymPy, an
independent route, and pins the source exams' answers.
"""

from __future__ import annotations

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.sets._support.math_m4 import maths as _num_maths

M2, M3, M4 = {"th": "ม.2"}, {"th": "ม.3"}, {"th": "ม.4"}
SCAN = range(-400, 401)          # every item's solution set lies well inside this


def _agree(solved, truth):
    if solved != truth:                                    # pragma: no cover
        raise AssertionError(f"solver gave {solved}, the construction says {truth}")
    return solved


def _count_q(stem: list, right: int, wrongs: list[int], topic: str) -> GeneratedQuestion:
    return _num_maths(stem, str(right), [str(w) for w in wrongs if w >= 0 and w != right], topic)


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def count_integers(pred) -> int:
    return sum(1 for x in SCAN if pred(x))


# ── Integer solutions of polynomial and rational inequalities ────────────────


# ── Parameters from a solution set ───────────────────────────────────────────


# ── Equations with several absolute values ───────────────────────────────────


# ── Integer solutions of absolute-value inequalities ─────────────────────────


# ── Unknown coefficients from remainders and factors ─────────────────────────


# ── Order properties of the reals ────────────────────────────────────────────


# ── The discriminant ─────────────────────────────────────────────────────────


# ── Remainders of sums, powers and factorials ────────────────────────────────


