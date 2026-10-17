"""Ordered rolls of n dice with total s, by a convolution table."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 5",))


def roll_count(dice: int, total: int) -> int:
    """Coefficient of x^s in (x + … + x⁶)ⁿ, built die by die
    (source: 6 dice, total 21 → 4332)."""
    counts = {0: 1}
    for _ in range(dice):
        new: dict[int, int] = {}
        for s, v in counts.items():
            for face in range(1, 7):
                new[s + face] = new.get(s + face, 0) + v
        counts = new
    return counts.get(total, 0)


@question_type(
    "math.dice_sum_count_olympiad",
    display_name={"th": "จำนวนวิธีโยนลูกเต๋าให้ได้ผลรวมตามกำหนด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class DiceSumCount(WordProblem):
    def expr(self, rng: Random):
        dice = rng.randint(3, 8)
        total = rng.randint(dice + 3, 6 * dice - 3)
        answer = roll_count(dice, total)
        wrong = [v for v in dict.fromkeys([comb(total - 1, dice - 1), roll_count(dice, total - 1), roll_count(dice, total + 1), answer // dice if answer // dice != answer else answer + dice, comb(total - 1, dice - 1) - dice * comb(total - 7, dice - 1) if total > 7 else 2 * answer]) if v != answer and v > 0]
        return MathDraw(
            rf"n={dice},\quad \text{{sum}}={total}",
            str(answer),
            prompt=f"โยนลูกเต๋าลูกหนึ่ง {dice} ครั้ง (ลำดับมีความสำคัญ) จงหาจำนวนวิธีทั้งหมดที่ให้แต้มรวมเท่ากับ {total}",
            hint="นับคำตอบของ x₁ + … + xₙ = s เมื่อ 1 ≤ xᵢ ≤ 6 ด้วยหลักการรวมและแยก หรือคำนวณทีละลูก",
            distractors=[str(v) for v in wrong],
        )
