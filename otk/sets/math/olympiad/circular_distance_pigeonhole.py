"""k residues on a cycle of length L: two lie within ⌊L/k⌋ of each other."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันแรก ข้อ 8",)
)


def guaranteed_distance(length: int, size: int) -> int:
    """Sorted around the cycle, the k gaps sum to L, so one is at most ⌊L/k⌋;
    spacing the residues as evenly as possible attains it. For L = 2553 and
    k = 70 this is 36 (d(x, y) is the circular distance of x − y mod 2553)."""
    return length // size


@question_type(
    "math.circular_distance_pigeonhole_olympiad",
    display_name={"th": "หลักรังนกพิราบกับระยะบนวงรอบมอดุโล"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class CircularDistancePigeonhole(WordProblem):
    def expr(self, rng: Random):
        length = rng.randint(200, 5000)
        size = rng.randint(10, 120)
        answer = guaranteed_distance(length, size)
        wrong = [v for v in dict.fromkeys([answer + 1, answer - 1, length // (size - 1), (length // 2) // size, length // (size + 1)]) if v != answer and v >= 0]
        return MathDraw(
            rf"L={length},\quad k={size}",
            str(answer),
            prompt=(
                "สำหรับจำนวนเต็ม x, y ให้ d(x, y) คือระยะของ x − y บนวงรอบมอดุโล L คือค่าที่น้อยกว่าระหว่าง (x − y) mod L กับ L − ((x − y) mod L) "
                "ค่า t ที่น้อยที่สุดที่รับประกันว่าเซตของจำนวนเต็ม k ตัวใด ๆ มีสองตัวที่ d ≤ t คือเท่าใด"
            ),
            hint="เรียงเศษมอดุโล L บนวงกลม ช่องว่าง k ช่องรวมกันได้ L",
            distractors=[str(v) for v in wrong],
        )
