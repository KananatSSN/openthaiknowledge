"""ปัญหาการหาค่าเหมาะที่สุด

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


@question_type("math.optimization_area",
               display_name={"th": "ปัญหาค่าเหมาะที่สุด (พื้นที่มากสุด)"},
               level={"th": "แคลคูลัส 1"}, topic="ปัญหาการหาค่าเหมาะที่สุด")
class OptimizationArea(WordProblem):
    def expr(self, rng: Random):
        p = rng.randint(5, 25) * 4                  # divisible by 4
        return MathDraw("", str((p // 4) ** 2),
                        prompt=f"สี่เหลี่ยมมุมฉากเส้นรอบรูป {p} มีพื้นที่มากสุดเท่าใด?",
                        distractors=[str((p // 2) ** 2), str(p * p // 4),
                                     str((p // 4) * (p // 2))])


@question_type("math.optimization_max_product",
               display_name={"th": "ผลคูณมากที่สุดเมื่อผลบวกคงที่"},
               level={"th": "แคลคูลัส 1"}, topic="ปัญหาการหาค่าเหมาะที่สุด")
class OptimizationMaxProduct(WordProblem):
    def expr(self, rng: Random, total_lo: int = 10, total_hi: int = 60):
        total = rng.randrange(total_lo, total_hi, 2)   # even, so halves are whole
        half = total // 2
        return MathDraw(
            "", str(half * half),
            prompt=(f"จำนวนสองจำนวนบวกกันได้ {total} "
                    "ผลคูณที่มากที่สุดของสองจำนวนนี้เป็นเท่าใด"),
            distractors=[str(total), str(half), str(total * total)])


@question_type("math.optimization_max_area_fence",
               display_name={"th": "พื้นที่มากที่สุดเมื่อเส้นรอบรูปคงที่"},
               level={"th": "แคลคูลัส 1"}, topic="ปัญหาการหาค่าเหมาะที่สุด")
class OptimizationMaxAreaFence(WordProblem):
    def expr(self, rng: Random, perimeter_lo: int = 20, perimeter_hi: int = 200):
        p = rng.randrange(perimeter_lo, perimeter_hi, 4)   # divisible by 4
        side = p // 4
        return MathDraw(
            "", str(side * side),
            prompt=(f"ต้องการล้อมรั้วรูปสี่เหลี่ยมผืนผ้าด้วยรั้วยาว {p} เมตร "
                    "พื้นที่ที่มากที่สุดที่ล้อมได้เป็นกี่ตารางเมตร"),
            distractors=[str(p * p), str(side * 2 * side),
                         str((p // 2) * (p // 2))])
