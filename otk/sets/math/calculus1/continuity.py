"""ความต่อเนื่อง

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem
from otk.sets._support.math_calculus import _linear, _nonzero

PROVENANCE = Provenance("original")


@question_type("math.continuity_k",
               display_name={"th": "หาค่าที่ทำให้ฟังก์ชันต่อเนื่อง"},
               level={"th": "แคลคูลัส 1"}, topic="ความต่อเนื่อง")
class ContinuityK(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(2, 6)
        return MathDraw(
            "", str(a * a - 2 * a),
            prompt=f"กำหนด f(x) = 2x + k เมื่อ x < {a} และ f(x) = x² เมื่อ x ≥ {a} "
                   f"จงหา k ที่ทำให้ f ต่อเนื่องที่ x = {a}",
            distractors=[str(a * a), str(a * a + 2 * a), str(2 * a - a * a)])


@question_type("math.ivt",
               display_name={"th": "ทฤษฎีบทค่าระหว่างกลาง (IVT)"},
               level={"th": "แคลคูลัส 1"}, topic="ความต่อเนื่อง")
class IVT(ChoiceType):
    def compose(self, rng: Random):
        a, b = rng.randint(0, 3), rng.randint(4, 7)
        fa, fb = -rng.randint(1, 9), rng.randint(1, 9)
        stem = (f"ฟังก์ชัน f ต่อเนื่อง โดย f({a}) = {fa} และ f({b}) = {fb} "
                f"IVT รับประกันสิ่งใดในช่วง ({a}, {b})?")
        # Each wrong reading claims something about c too, so the answer is not
        # the one detailed statement among bare ones.
        return stem, "มีอย่างน้อยหนึ่ง c ที่ f(c) = 0", [
            "ไม่มี c ใดในช่วงนี้ที่ f(c) = 0", "มี c เพียงค่าเดียวที่ f(c) = 0",
            "f(c) > 0 สำหรับทุก c ในช่วงนี้", "f เพิ่มขึ้นตลอดช่วงนี้ทุกค่า c"]


@question_type("math.continuity_check", display_name={"th": "ตรวจสอบความต่อเนื่อง"},
               level={"th": "แคลคูลัส 1"}, topic="ความต่อเนื่อง")
class ContinuityCheck(ChoiceType):
    def compose(self, rng: Random):
        a = _nonzero(rng, -5, 5)
        m = rng.randint(2, 6)
        b = rng.randint(-9, 9)
        left = m * a + b                          # value of mx + b at x = a
        matches = rng.random() < 0.5
        right = left if matches else left + rng.choice([-3, -2, 2, 3])
        stem = (f"ให้ f(x) = {_linear(m, b)} เมื่อ x ≤ {a} และ f(x) = {right} "
                f"เมื่อ x > {a} ฟังก์ชันนี้ต่อเนื่องที่ x = {a} หรือไม่")
        agree = f"ต่อเนื่อง เพราะลิมิตที่จุดนั้นเท่ากับ f({a})"
        if matches:
            return stem, agree, [
                "ไม่ต่อเนื่อง เพราะลิมิตซ้ายและขวาไม่เท่ากัน",
                "ไม่ต่อเนื่อง เพราะหาค่า f ที่จุดนั้นไม่ได้",
                "ไม่ต่อเนื่อง เพราะลิมิตที่จุดนั้นไม่มีค่า"]
        return stem, "ไม่ต่อเนื่อง เพราะลิมิตซ้ายและขวาไม่เท่ากัน", [
            agree, "ไม่ต่อเนื่อง เพราะหาค่า f ที่จุดนั้นไม่ได้",
            "ไม่ต่อเนื่อง เพราะลิมิตที่จุดนั้นไม่มีค่า"]
