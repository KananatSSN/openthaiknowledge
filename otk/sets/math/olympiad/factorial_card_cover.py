"""Fewest factorial cards whose subset sums reach every t ≤ n!."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2557, ข้อ 8",)
)


def fewest_cards(n: int) -> int:
    """n! − 1 = Σ j·j! (j < n) needs at least that digit sum n(n − 1)/2 of
    cards below n!, and those sum to at most n! − 1 unless one more card is
    added; j copies of j! for j < n plus one extra 1! reach everything."""
    if n < 1:
        raise ValueError("n must be positive")
    return n * (n - 1) // 2 + 1


@question_type(
    "math.factorial_card_cover_olympiad",
    display_name={"th": "จำนวนบัตรแฟกทอเรียลน้อยสุดที่รวมได้ทุกจำนวน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class FactorialCardCover(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 40)
        answer = fewest_cards(n)
        wrong = [
            answer - 1,  # forget the card that reaches n! itself
            n * (n + 1) // 2,  # use digits up to n
            n * (n + 1) // 2 + 1,
            2 * n - 1,
            answer + n - 1,
        ]
        wrong = [v for v in dict.fromkeys(wrong) if v != answer]
        return MathDraw(
            rf"n={n}",
            str(answer),
            prompt=(
                "ต้องการชุดบัตรที่แต่ละใบเขียนจำนวนในรูป m! (m เป็นจำนวนเต็มบวก) "
                "โดยทุกจำนวนเต็มบวก t ≤ n! เลือกบัตรบางใบมารวมกันได้เท่ากับ t "
                "ชุดบัตรนี้ต้องมีอย่างน้อยกี่ใบ"
            ),
            hint="เขียน n! − 1 ในระบบฐานแฟกทอเรียล: 1·1! + 2·2! + ⋯ + (n − 1)·(n − 1)!",
            distractors=[str(v) for v in wrong],
        )
