"""ความเว้าและจุดเปลี่ยนโค้ง

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, WordProblem, poly_tex
from otk.sets._support.math_calculus import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.inflection_point",
               display_name={"th": "จุดเปลี่ยนโค้ง"}, level={"th": "แคลคูลัส 1"},
               topic="ความเว้าและจุดเปลี่ยนโค้ง")
class InflectionPoint(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(2, 9)
        return MathDraw("", "0",
                        prompt=f"จุดเปลี่ยนโค้งของ f(x) = x³ − {k}x อยู่ที่ x เท่าใด?",
                        distractors=[str(k), str(-k), str(k // 2 or 1)])


@question_type("math.concave_up_interval", display_name={"th": "ช่วงที่กราฟเว้าขึ้น"},
               level={"th": "แคลคูลัส 1"}, topic="ความเว้าและจุดเปลี่ยนโค้ง")
class ConcaveUpInterval(MathType):
    def expr(self, rng: Random, point_hi: int = 6):
        p = rng.randint(-point_hi, point_hi)
        # f = x³ − 3px²…  →  f″ = 6(x − p): concave up exactly for x > p.
        shown = poly_tex((1, "x^3"), (-3 * p, "x^2"), (rng.randint(-9, 9), "x"), (0, ""))
        return MathDraw(
            rf"f(x) = {shown}", rf"({p}, \infty)",
            prompt="กราฟของฟังก์ชันนี้เว้าขึ้นบนช่วงใด",
            hint=r"f''(x) = 6(x - p)",
            distractors=[rf"(-\infty, {p})", rf"({-p}, \infty)",
                         r"(-\infty, \infty)"])


@question_type("math.second_derivative_test",
               display_name={"th": "การทดสอบอนุพันธ์อันดับสอง"},
               level={"th": "แคลคูลัส 1"}, topic="ความเว้าและจุดเปลี่ยนโค้ง")
class SecondDerivativeTest(ChoiceType):
    def compose(self, rng: Random):
        a = _nonzero(rng, -4, 4)
        h = rng.randint(-5, 5)
        k = rng.randint(-9, 9)
        shown = poly_tex((a, "x^2"), (-2 * a * h, "x"), (a * h * h + k, ""))
        stem = (f"ให้ f(x) = {shown.replace('^2', '²')} "
                f"จุดวิกฤตที่ x = {h} เป็นจุดใด")
        if a > 0:
            return stem, "จุดต่ำสุดสัมพัทธ์", [
                "จุดสูงสุดสัมพัทธ์", "จุดเปลี่ยนโค้ง", "ไม่ใช่จุดวิกฤต"]
        return stem, "จุดสูงสุดสัมพัทธ์", [
            "จุดต่ำสุดสัมพัทธ์", "จุดเปลี่ยนโค้ง", "ไม่ใช่จุดวิกฤต"]
