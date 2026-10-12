"""ฟังก์ชันเพิ่ม/ลด

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, poly_tex

PROVENANCE = Provenance("original")


@question_type("math.increasing_interval",
               display_name={"th": "ช่วงที่ฟังก์ชันเพิ่ม"},
               level={"th": "แคลคูลัส 1"}, topic="ฟังก์ชันเพิ่ม/ลด")
class IncreasingInterval(ChoiceType):
    def compose(self, rng: Random):
        k = rng.choice([2, 4, 6, 8])
        h = k // 2
        return (f"f(x) = x² − {k}x เป็นฟังก์ชันเพิ่มในช่วงใด?",
                f"x > {h}", [f"x < {h}", f"x > {k}", "ทุกค่า x",
                             # Direction and bound both wrong.
                             f"x < {k}", f"x < -{h}"])


@question_type("math.decreasing_interval", display_name={"th": "ช่วงที่ฟังก์ชันลด"},
               level={"th": "แคลคูลัส 1"}, topic="ฟังก์ชันเพิ่ม/ลด")
class DecreasingInterval(MathType):
    def expr(self, rng: Random, root_hi: int = 6):
        p, q = sorted(rng.sample(range(-root_hi, root_hi + 1), 2))
        # f = 2x³ − 3(p+q)x² + 6pq·x, so f′ = 6(x − p)(x − q) and f decreases
        # exactly on (p, q).
        shown = poly_tex((2, "x^3"), (-3 * (p + q), "x^2"), (6 * p * q, "x"), (0, ""))
        return MathDraw(
            rf"f(x) = {shown}", f"({p}, {q})",
            prompt="ฟังก์ชันนี้เป็นฟังก์ชันลดบนช่วงใด",
            hint=r"f'(x) = 6(x - p)(x - q)",
            distractors=[f"({q}, {p})",
                         rf"(-\infty, {p}) \cup ({q}, \infty)",
                         rf"({p}, \infty)"])


@question_type("math.monotonic_at_point", display_name={"th": "เพิ่มหรือลดที่จุดหนึ่ง"},
               level={"th": "แคลคูลัส 1"}, topic="ฟังก์ชันเพิ่ม/ลด")
class MonotonicAtPoint(ChoiceType):
    def compose(self, rng: Random):
        p, q = sorted(rng.sample(range(-6, 7), 2))
        inside = rng.random() < 0.5
        if inside and q - p > 1:
            x0 = rng.randint(p + 1, q - 1)
            answer = "เป็นฟังก์ชันลด"
        else:
            x0 = rng.choice([p - 2, q + 2])
            answer = "เป็นฟังก์ชันเพิ่ม"
        shown = poly_tex((2, "x^3"), (-3 * (p + q), "x^2"), (6 * p * q, "x"), (0, ""))
        stem = (f"ให้ f(x) = {shown.replace('^3', '³').replace('^2', '²')} "
                f"ที่ x = {x0} ฟังก์ชันมีลักษณะอย่างไร")
        wrong = ["เป็นฟังก์ชันเพิ่ม" if answer.endswith("ลด") else "เป็นฟังก์ชันลด",
                 "เป็นจุดวิกฤต", "ไม่มีอนุพันธ์ที่จุดนี้"]
        return stem, answer, wrong
