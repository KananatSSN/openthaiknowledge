"""Expose the smaller Sophie Germain factor in a divisibility proof."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2564, ข้อ 5",)
)


def smaller_sophie_factor(odd_base: int, odd_exponent: int) -> int:
    """The smaller factor of u^4+4^k for odd positive u,k."""
    if odd_base < 1 or odd_base % 2 != 1 or odd_exponent < 1 or odd_exponent % 2 != 1:
        raise ValueError("base and exponent must be positive odd integers")
    power = 2 ** ((odd_exponent - 1) // 2)
    return (odd_base - power) ** 2 + power**2


@question_type(
    "math.sophie_germain_prime_power_olympiad",
    display_name={"th": "ตัวประกอบจากเอกลักษณ์โซฟี แฌร์แม็ง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามและการแยกตัวประกอบ",
)
class SophieGermainPrimePower(WordProblem):
    def expr(self, rng: Random):
        odd_base = rng.choice((1, 3, 5, 7, 9, 11, 13, 15))
        odd_exponent = rng.choice((1, 3, 5, 7))
        if odd_base == odd_exponent == 1:
            odd_base = 3
        power = 2 ** ((odd_exponent - 1) // 2)
        answer = smaller_sophie_factor(odd_base, odd_exponent)
        return MathDraw(
            rf"u={odd_base},\quad k={odd_exponent},\quad N=u^4+4^k",
            str(answer),
            prompt=(
                "เมื่อใช้เอกลักษณ์โซฟี แฌร์แม็งแยก N เป็นผลคูณ "
                "จงหาค่าของตัวประกอบที่น้อยกว่า"
            ),
            hint=(
                "เขียน 4^k=4v^4 โดย v=2^((k−1)/2) "
                "แล้วแยกเป็น (u²−2uv+2v²)(u²+2uv+2v²)"
            ),
            distractors=[
                str(odd_base**2 + 2 * odd_base * power + 2 * power**2),
                # choose the larger factor
                str((odd_base - power) ** 2),  # omit the remaining v²
                str((odd_base - power) ** 2 + 2 * power**2),
                # add v² twice
                str(odd_base**2 + power**2),  # omit the mixed term
                str(odd_base**2 + 2 * power**2),  # use the midpoint of factors
                str(odd_base**2 - 2 * odd_base * power + power**2 + 1),
                # replace v² by one
            ],
        )
