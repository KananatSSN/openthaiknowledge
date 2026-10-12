"""อนุพันธ์โดยปริยาย

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex

PROVENANCE = Provenance("original")


@question_type("math.implicit_diff",
               display_name={"th": "อนุพันธ์โดยปริยาย"}, level={"th": "แคลคูลัส 1"},
               topic="อนุพันธ์โดยปริยาย")
class ImplicitDiff(MathType):
    def expr(self, rng: Random):
        r = rng.randint(2, 8)
        return MathDraw(
            rf"x^{{2}} + y^{{2}} = {r * r}", r"-\frac{x}{y}",
            prompt="จงหา dy/dx",
            distractors=[r"\frac{x}{y}", r"-\frac{y}{x}", r"-\frac{x}{y^{2}}"])


@question_type("math.implicit_circle", display_name={"th": "อนุพันธ์โดยปริยายของวงกลม"},
               level={"th": "แคลคูลัส 1"}, topic="อนุพันธ์โดยปริยาย")
class ImplicitCircle(MathType):
    def expr(self, rng: Random, radius_hi: int = 12):
        r = rng.randint(2, radius_hi)
        return MathDraw(
            rf"x^2 + y^2 = {r * r}", r"-\frac{x}{y}",
            prompt="จงหา dy/dx",
            distractors=[r"\frac{x}{y}", r"-\frac{y}{x}", r"-\frac{2x}{y}"])


@question_type("math.implicit_slope_at_point",
               display_name={"th": "ความชันโดยปริยาย ณ จุดหนึ่ง"},
               level={"th": "แคลคูลัส 1"}, topic="อนุพันธ์โดยปริยาย")
class ImplicitSlopeAtPoint(MathType):
    def expr(self, rng: Random, k_lo: int = 1, k_hi: int = 4):
        a, b, c = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10)])
        k = rng.randint(k_lo, k_hi)
        x, y, r = a * k, b * k, c * k
        slope = Fraction(-x, y)
        return MathDraw(
            rf"x^2 + y^2 = {r * r}, \quad P({x}, {y})", frac_tex(slope),
            prompt="จงหาความชันของเส้นสัมผัสวงกลมที่จุด P",
            distractors=[frac_tex(-slope), frac_tex(Fraction(-y, x)),
                         frac_tex(Fraction(y, x))])
