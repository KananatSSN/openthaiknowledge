"""สมการอิงตัวแปรเสริม

คณิตศาสตร์ · แคลคูลัส 2 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex, poly_tex
from otk.sets._support.math_calculus import _signed

PROVENANCE = Provenance("original")


@question_type("math.parametric_derivative",
               display_name={"th": "อนุพันธ์ของเส้นโค้งพารามิเตอร์"},
               level={"th": "แคลคูลัส 2"}, topic="สมการอิงตัวแปรเสริม")
class ParametricDerivative(MathType):
    def expr(self, rng: Random):
        return MathDraw(
            r"x = f(t),\ y = g(t)", r"\frac{dy/dt}{dx/dt}",
            prompt="dy/dx เท่ากับข้อใด",
            distractors=[r"\frac{dx/dt}{dy/dt}",
                         r"\frac{dy}{dt}\cdot\frac{dx}{dt}", r"g'(t)"])


@question_type("math.parametric_second_derivative",
               display_name={"th": "อนุพันธ์อันดับสองของเส้นโค้งพารามิเตอร์"},
               level={"th": "แคลคูลัส 2"}, topic="สมการอิงตัวแปรเสริม")
class ParametricSecondDerivative(MathType):
    def expr(self, rng: Random, coef_hi: int = 5):
        a = rng.randint(1, coef_hi)
        b = rng.randint(1, coef_hi)
        # x = a·t, y = b·t²  →  dy/dx = 2bt/a, d²y/dx² = 2b/a²
        return MathDraw(
            rf"x = {poly_tex((a, 't'))}, \quad y = {poly_tex((b, 't^2'))}",
            frac_tex(Fraction(2 * b, a * a)),
            prompt="จงหา d²y/dx²",
            distractors=[frac_tex(Fraction(2 * b, a)),
                         frac_tex(Fraction(b, a * a)),
                         frac_tex(Fraction(2 * b, a) * 2)])


@question_type("math.parametric_eliminate", display_name={"th": "กำจัดตัวแปรเสริม"},
               level={"th": "แคลคูลัส 2"}, topic="สมการอิงตัวแปรเสริม")
class ParametricEliminate(MathType):
    def expr(self, rng: Random, coef_hi: int = 5):
        a = rng.randint(1, coef_hi)
        b = rng.randint(1, coef_hi)
        c = rng.randint(-6, 6)
        # x = t + c, y = a·t + b  →  y = a(x − c) + b
        return MathDraw(
            rf"x = t{_signed(c)}, \quad y = {poly_tex((a, 't'), (b, ''))}",
            f"y = {poly_tex((a, 'x'), (b - a * c, ''))}",
            prompt="จงกำจัดตัวแปรเสริมเพื่อหาความสัมพันธ์ระหว่าง x กับ y",
            distractors=[f"y = {poly_tex((a, 'x'), (b + a * c, ''))}",
                         f"y = {poly_tex((a, 'x'), (b, ''))}",
                         f"y = {poly_tex((a, 'x'), (c, ''))}"])
