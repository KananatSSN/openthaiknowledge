"""ดิสคริมิแนนต์

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/1

Sets moved here from: math, math_algebra.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, poly_tex

PROVENANCE = Provenance("original")


@question_type("math.discriminant",
               display_name={"th": "ดิสคริมิแนนต์: จำนวนรากจริง"}, level={"th": "ม.4"},
               topic="ดิสคริมิแนนต์")
class Discriminant(MathType):
    def expr(self, rng: Random):
        b, c = rng.randint(-6, 6), rng.randint(-9, 9)
        if rng.random() < 0.25:
            b = rng.choice([-6, -4, -2, 2, 4, 6])
            c = b * b // 4
        disc = b * b - 4 * c
        if disc > 0:
            verdict = rf"D = {disc} > 0 \;\Rightarrow\; 2"
        elif disc == 0:
            verdict = r"D = 0 \;\Rightarrow\; 1"
        else:
            verdict = rf"D = {disc} < 0 \;\Rightarrow\; 0"
        tex = poly_tex((1, "x^{2}"), (b, "x"), (c, ""))
        return MathDraw(rf"{tex} = 0", verdict, hint=r"D = b^2 - 4ac",
                        prompt="สมการนี้มีรากจริงกี่ราก")


@question_type("math.discriminant_k", display_name={"th": "หาค่า k จากเงื่อนไขของราก"},
               level={"th": "ม.4"}, topic="ดิสคริมิแนนต์")
class DiscriminantK(MathType):
    """A repeated root means b² − 4ac = 0 — solved for the unknown coefficient."""

    def expr(self, rng: Random, a_hi: int = 4, half_b_hi: int = 9):
        a = rng.randint(1, a_hi)
        m = rng.randint(1, half_b_hi)
        b = 2 * a * m
        c = a * m * m                              # makes b² − 4ac = 0 exactly
        return MathDraw(
            poly_tex((a, "x^2"), (b, "x"), (0, "")) + " + k = 0", str(c),
            prompt="จงหาค่า k ที่ทำให้สมการมีรากซ้ำ",
            hint=r"b^2 - 4ac = 0",
            distractors=[str(-c), str(b * b), str(c * 2)])


@question_type("math.quadratic_complex",
               display_name={"th": "สมการกำลังสอง (รากเชิงซ้อน)"}, level={"th": "ม.4"},
               topic="ดิสคริมิแนนต์")
class QuadraticComplex(MathType):
    def expr(self, rng: Random):
        m = rng.randint(-3, 3)
        k = rng.randint(1, 3)
        tex = poly_tex((1, "x^{2}"), (-2 * m, "x"), (m * m + k * k, ""))
        ki = "i" if k == 1 else f"{k}i"
        answer = rf"x = \pm {ki}" if m == 0 else rf"x = {m} \pm {ki}"
        return MathDraw(rf"{tex} = 0", answer, hint=r"\sqrt{-1} = i",
                        prompt="จงแก้สมการ")
