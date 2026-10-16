"""Pigeonhole and discrete intermediate values for signed prefix sums."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def minimum_positive_prefix_values(total: int, groups: int = 4) -> int:
    """Find the least possible number of distinct positive prefix sums.

    One of the groups has total at least ceil(total/groups). Its prefix sums
    walk from zero in unit steps, so they include every positive integer up
    to that total. Distributing `total` positive unit terms as evenly as
    possible among the groups attains this lower bound.
    """
    if total < 1 or groups < 1:
        raise ValueError("total and groups must be positive")
    return (total + groups - 1) // groups


@question_type(
    "math.prefix_pigeonhole_olympiad",
    display_name={"th": "ผลรวมสะสมจากสี่ลำดับ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class PrefixPigeonhole(WordProblem):
    def expr(self, rng: Random):
        quotient = rng.randint(5, 50)
        total = 4 * quotient + rng.randint(1, 3)
        answer = minimum_positive_prefix_values(total)
        return MathDraw(
            rf"\sum_{{j=1}}^4\sum_{{x\in L_j}}x={total}",
            str(answer),
            prompt=("มีลำดับจำนวนจำกัดสี่ลำดับ L₁,L₂,L₃,L₄ แต่ละพจน์เป็น +1 หรือ −1 "
                    "และผลรวมของทุกพจน์เป็นไปตามสมการ นับค่าจำนวนเต็มบวกที่แตกต่างกัน "
                    "ซึ่งปรากฏเป็นผลรวมสะสมจากต้นลำดับถึงตำแหน่งใดตำแหน่งหนึ่ง "
                    "ในอย่างน้อยหนึ่งลำดับ จำนวนค่านี้น้อยที่สุดได้เท่าใด"),
            hint=rf"\max_j\sum_{{x\in L_j}}x\ge\left\lceil\frac{{{total}}}4\right\rceil",
            distractors=[
                str(quotient),  # floor instead of ceiling
                str(answer + 1),  # count the zero prefix as positive
                str(total),  # assume every positive total must appear
            ],
        )
