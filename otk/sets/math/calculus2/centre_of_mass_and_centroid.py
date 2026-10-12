"""จุดศูนย์กลางมวลและเซนทรอยด์

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

PROVENANCE = Provenance("original")


@question_type("math.centroid",
               display_name={"th": "เซนทรอยด์ x̄ ของพื้นที่"},
               level={"th": "แคลคูลัส 2"}, topic="จุดศูนย์กลางมวลและเซนทรอยด์")
class Centroid(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        return MathDraw(
            r"y = f(x),\ x \in [a, b]",
            r"\frac{\int_{a}^{b} x\,f(x)\,dx}{\int_{a}^{b} f(x)\,dx}",
            prompt="สูตร x̄ ของเซนทรอยด์ใต้เส้น y = f(x) คือข้อใด",
            distractors=[r"\frac{\int_{a}^{b} f(x)\,dx}{\int_{a}^{b} x\,f(x)\,dx}",
                         r"\int_{a}^{b} x\,f(x)\,dx",
                         r"\frac{\int_{a}^{b} \tfrac{1}{2}[f(x)]^{2}\,dx}"
                         r"{\int_{a}^{b} f(x)\,dx}",
                         r"\int_{a}^{b} f(x)\,dx",
                         r"\frac{\int_{a}^{b} x^{2} f(x)\,dx}{\int_{a}^{b} f(x)\,dx}"])


@question_type("math.average_value", display_name={"th": "ค่าเฉลี่ยของฟังก์ชันบนช่วง"},
               level={"th": "แคลคูลัส 2"}, topic="จุดศูนย์กลางมวลและเซนทรอยด์")
class AverageValue(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 4, bound_hi: int = 5):
        a = rng.randint(1, coef_hi)
        b = rng.randint(-6, 6)
        lo, hi = sorted(rng.sample(range(-bound_hi, bound_hi + 1), 2))

        def antideriv(x):
            return Fraction(a, 3) * x ** 3 + Fraction(b, 2) * x ** 2

        avg = (antideriv(hi) - antideriv(lo)) / (hi - lo)
        shown = poly_tex((a, "x^2"), (b, "x"), (0, ""))
        return MathDraw(
            rf"f(x) = {shown}, \quad [{lo}, {hi}]", frac_tex(avg),
            prompt="จงหาค่าเฉลี่ยของฟังก์ชันบนช่วงนี้",
            hint=r"\frac{1}{b-a}\int_a^b f(x)\,dx",
            distractors=[frac_tex(avg * (hi - lo)), frac_tex(-avg),
                         frac_tex(avg / 2)])


@question_type("math.centroid_rectangle_region",
               display_name={"th": "เซนทรอยด์ของแผ่นสี่เหลี่ยม"},
               level={"th": "แคลคูลัส 2"}, topic="จุดศูนย์กลางมวลและเซนทรอยด์")
class CentroidRectangle(MathType):
    def expr(self, rng: Random, bound_hi: int = 10):
        x1, x2 = sorted(rng.sample(range(-bound_hi, bound_hi + 1), 2))
        y1, y2 = sorted(rng.sample(range(-bound_hi, bound_hi + 1), 2))
        cx, cy = Fraction(x1 + x2, 2), Fraction(y1 + y2, 2)
        return MathDraw(
            rf"{x1} \le x \le {x2}, \quad {y1} \le y \le {y2}",
            f"({frac_tex(cx)}, {frac_tex(cy)})",
            prompt="จงหาเซนทรอยด์ของแผ่นสม่ำเสมอรูปสี่เหลี่ยมนี้",
            distractors=[f"({frac_tex(cy)}, {frac_tex(cx)})",
                         f"({x1}, {y1})", f"({x2}, {y2})"])
