"""ทฤษฎีบทค่ามัชฌิม

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem, poly_tex
from otk.sets._support.math_calculus import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.mean_value_theorem",
               display_name={"th": "ทฤษฎีบทค่ามัชฌิม (MVT)"},
               level={"th": "แคลคูลัส 1"}, topic="ทฤษฎีบทค่ามัชฌิม")
class MeanValueTheorem(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(-3, 2)
        b = a + rng.choice([2, 4, 6])              # b − a even → integer c
        c = (a + b) // 2
        return MathDraw("", str(c),
                        prompt=f"หา c ใน ({a}, {b}) ที่ f′(c) = "
                               f"(f(b) − f(a))/(b − a) สำหรับ f(x) = x² บน "
                               f"[{a}, {b}]",
                        distractors=[str(a), str(b), str(c + 1)])


@question_type("math.mvt_c_value", display_name={"th": "ค่า c จากทฤษฎีบทค่ามัชฌิม"},
               level={"th": "แคลคูลัส 1"}, topic="ทฤษฎีบทค่ามัชฌิม")
class MvtCValue(MathType):
    """For a quadratic the MVT point is always the midpoint of the interval —
    worth discovering rather than being told."""

    def expr(self, rng: Random, coef_hi: int = 5, bound_hi: int = 8):
        a = _nonzero(rng, -coef_hi, coef_hi)
        b = rng.randint(-9, 9)
        c = rng.randint(-9, 9)
        lo, hi = sorted(rng.sample(range(-bound_hi, bound_hi + 1), 2))
        if (lo + hi) % 2:
            hi += 1
        mid = (lo + hi) // 2
        shown = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        return MathDraw(
            rf"f(x) = {shown}, \quad [{lo}, {hi}]", f"c = {mid}",
            prompt="จงหาค่า c ตามทฤษฎีบทค่ามัชฌิม",
            distractors=[f"c = {lo}", f"c = {hi}", f"c = {mid + 1}"])


@question_type("math.rolle_c_value", display_name={"th": "ทฤษฎีบทของโรล"},
               level={"th": "แคลคูลัส 1"}, topic="ทฤษฎีบทค่ามัชฌิม")
class RolleCValue(MathType):
    def expr(self, rng: Random, root_hi: int = 8):
        p, q = sorted(rng.sample(range(-root_hi, root_hi + 1), 2))
        if (p + q) % 2:
            q += 1
        mid = (p + q) // 2
        # f = (x − p)(x − q) vanishes at both ends; f′ = 0 at the midpoint.
        shown = poly_tex((1, "x^2"), (-(p + q), "x"), (p * q, ""))
        return MathDraw(
            rf"f(x) = {shown}, \quad [{p}, {q}]", f"c = {mid}",
            prompt="f มีค่าเท่ากันที่ปลายทั้งสองข้าง จงหาค่า c ที่ทำให้ f′(c) = 0",
            distractors=[f"c = {p}", f"c = {q}", f"c = {mid + 1}"])
