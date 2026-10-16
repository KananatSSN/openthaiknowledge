"""Minimize a power sum under a reciprocal-sum constraint."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2564, ข้อ 3",)
)


def minimum_reciprocal_power_sum(scale: int) -> int:
    """Return the attained minimum of a^a bc+b^b ca+c^c ab."""
    if scale < 1:
        raise ValueError("scale must be a positive integer")
    return 3 * (3 * scale) ** (3 * scale + 2)


@question_type(
    "math.reciprocal_sum_power_minimum_olympiad",
    display_name={"th": "ค่าน้อยสุดของผลบวกกำลังจากผลบวกส่วนกลับ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class ReciprocalSumPowerMinimum(WordProblem):
    def expr(self, rng: Random):
        scale = rng.randint(1, 5)
        base = 3 * scale
        answer = minimum_reciprocal_power_sum(scale)
        return MathDraw(
            (
                rf"ab+bc+ca=\frac{{abc}}{{{scale}}},\quad "
                r"F=a^a bc+b^b ca+c^c ab"
            ),
            str(answer),
            prompt="เมื่อ a,b,c เป็นจำนวนจริงบวก จงหาค่าต่ำสุดของ F",
            hint=(
                "หารเงื่อนไขด้วย abc แล้วใช้ AM–GM กับส่วนกลับ "
                "เขียน F=abc(a^(a−1)+b^(b−1)+c^(c−1)) แล้วใช้ความนูน"
            ),
            distractors=[
                str(3 * base ** (3 * scale)),  # omit the bc factor
                str(base ** (3 * scale + 2)),  # omit three equal summands
                str(3 * base ** (3 * scale + 1)),  # lose one base factor
                str(3 * base ** (3 * scale + 3)),  # add one base factor
                str(3 * scale ** (3 * scale + 2)),  # omit the factor three in the base
                str(3 * base**3),  # use the number of variables as exponent
            ],
        )
