"""การประมาณค่าเชิงเส้น

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex, poly_tex
from otk.sets._support.math_calculus import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.linear_approximation",
               display_name={"th": "การประมาณค่าเชิงเส้น"},
               level={"th": "แคลคูลัส 1"}, topic="การประมาณค่าเชิงเส้น")
class LinearApproximation(MathType):
    def expr(self, rng: Random):
        return MathDraw(
            r"L(x) \approx f(a) + ?", r"f(a) + f'(a)\,\Delta x",
            prompt="การประมาณเชิงเส้นของ f ใกล้ x = a คือข้อใด",
            # Two as complete as the answer, so "pick the formula with every
            # part" no longer finds it; and not all one-slip copies of it, which
            # would make it the one every other choice resembles.
            distractors=[r"f'(a) + f(a)\,\Delta x", r"f'(a) - f(a)\,\Delta x",
                         r"f'(a)\,\Delta x"])


@question_type("math.differential_dy", display_name={"th": "ผลต่างอนุพันธ์ dy"},
               level={"th": "แคลคูลัส 1"}, topic="การประมาณค่าเชิงเส้น")
class DifferentialDy(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 5, point_hi: int = 4):
        a = _nonzero(rng, -coef_hi, coef_hi)
        b = rng.randint(-9, 9)
        x0 = rng.randint(-point_hi, point_hi)
        dx = Fraction(rng.choice([1, 2, 5]), rng.choice([10, 100]))
        slope = 2 * a * x0 + b
        dy = slope * dx
        shown = poly_tex((a, "x^2"), (b, "x"), (0, ""))
        return MathDraw(
            rf"y = {shown}, \quad x = {x0}, \quad dx = {frac_tex(dx)}",
            frac_tex(dy), prompt="จงหาค่า dy",
            distractors=[frac_tex(-dy), str(slope), frac_tex(dx)])


@question_type("math.linear_approximation_sqrt",
               display_name={"th": "ประมาณค่ารากที่สองด้วยเส้นสัมผัส"},
               level={"th": "แคลคูลัส 1"}, topic="การประมาณค่าเชิงเส้น")
class LinearApproximationSqrt(MathType):
    """√(a² + h) ≈ a + h/(2a): the tangent to √x at a perfect square."""

    def expr(self, rng: Random, base_lo: int = 3, base_hi: int = 12):
        a = rng.randint(base_lo, base_hi)
        h = rng.choice([-2, -1, 1, 2])
        target = a * a + h
        approx = Fraction(a) + Fraction(h, 2 * a)
        return MathDraw(
            rf"\sqrt{{{target}}}", frac_tex(approx),
            prompt=f"จงประมาณค่าด้วยเส้นสัมผัสที่ x = {a * a}",
            distractors=[frac_tex(Fraction(a) - Fraction(h, 2 * a)),
                         frac_tex(Fraction(a) + Fraction(h, a)), str(a)])
