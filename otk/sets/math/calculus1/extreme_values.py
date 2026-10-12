"""ค่าสุดขีด

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem, poly_tex

PROVENANCE = Provenance("original")


@question_type("math.critical_point",
               display_name={"th": "จุดวิกฤต"}, level={"th": "แคลคูลัส 1"},
               topic="ค่าสุดขีด")
class CriticalPoint(WordProblem):
    def expr(self, rng: Random):
        b = rng.choice([n for n in range(-8, 9) if n and n % 2 == 0])
        return MathDraw("", str(-b // 2),
                        prompt=f"จุดวิกฤตของ f(x) = {poly_tex((1, 'x^{2}'), (b, 'x'))}"
                               f" เกิดที่ x เท่าใด?",
                        distractors=[str(b // 2), str(-b), "0"])


@question_type("math.absolute_extremum_closed",
               display_name={"th": "ค่าสูงสุด-ต่ำสุดสัมบูรณ์บนช่วงปิด"},
               level={"th": "แคลคูลัส 1"}, topic="ค่าสุดขีด")
class AbsoluteExtremumClosed(MathType):
    """The endpoints are candidates too — a closed interval is not just f′ = 0."""

    def expr(self, rng: Random, lead_hi: int = 3, h_hi: int = 4):
        a = rng.randint(1, lead_hi)
        h = rng.randint(-h_hi, h_hi)
        k = rng.randint(-9, 9)
        lo, hi = sorted(rng.sample(range(h - 5, h + 6), 2))
        shown = poly_tex((a, "x^2"), (-2 * a * h, "x"), (a * h * h + k, ""))

        def f(x):
            return a * (x - h) ** 2 + k

        candidates = [lo, hi] + ([h] if lo <= h <= hi else [])
        values = [f(x) for x in candidates]
        want_max = rng.random() < 0.5
        answer = max(values) if want_max else min(values)
        word = "สูงสุด" if want_max else "ต่ำสุด"
        return MathDraw(
            rf"f(x) = {shown}, \quad {lo} \le x \le {hi}", str(answer),
            prompt=f"จงหาค่า{word}สัมบูรณ์ของฟังก์ชันบนช่วงนี้",
            distractors=[str(min(values) if want_max else max(values)),
                         str(k), str(h)])
