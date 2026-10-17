"""Balls in five boxes where the largest and smallest box hold at least the rest."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันแรก ข้อ 1",)
)


def extreme_box_count(balls: int) -> int:
    """With s balls in the two named boxes (s ≥ ⌈N/2⌉ so that s ≥ N − s):
    s − 1 ways for the pair, C(N − s − 1, 2) for the other three."""
    return sum((s - 1) * comb(balls - s - 1, 2) for s in range((balls + 1) // 2, balls - 2))


@question_type(
    "math.ball_box_extremes_count_olympiad",
    display_name={"th": "นับวิธีใส่ลูกบอลเมื่อกล่องใหญ่สุดกับเล็กสุดรวมกันไม่น้อยกว่าที่เหลือ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class BallBoxExtremesCount(WordProblem):
    def expr(self, rng: Random):
        balls = rng.randint(8, 30)
        answer = extreme_box_count(balls)
        strict = sum((s - 1) * comb(balls - s - 1, 2) for s in range(balls // 2 + 1, balls - 2))
        wrong = [v for v in dict.fromkeys([
            comb(balls - 1, 4),  # drop the condition
            strict,  # read "not less than" as "more than"
            comb(balls - 1, 4) - answer,
            answer + balls,
            2 * answer,
        ]) if v != answer and v > 0]
        return MathDraw(
            rf"N={balls}",
            str(answer),
            prompt=(
                "ใส่ลูกบอลที่เหมือนกัน N ลูกลงกล่อง 5 ใบที่มีขนาดต่างกันหมด กล่องละอย่างน้อย 1 ลูก "
                "โดยจำนวนลูกบอลในกล่องใบใหญ่สุดรวมกับใบเล็กสุดไม่น้อยกว่าจำนวนในอีกสามใบรวมกัน มีกี่วิธี"
            ),
            hint="ให้ s เป็นจำนวนลูกในสองกล่องนั้น เงื่อนไขคือ s ≥ N − s แล้วนับแบบดาวและแท่งแยกสองส่วน",
            distractors=[str(v) for v in wrong],
        )
