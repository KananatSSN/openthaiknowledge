"""Find constants preserving rational roots under quadratic coefficient swaps."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def valid_swapped_constants(leading: int, middle_magnitude: int) -> tuple[int, ...]:
    """Positive constants making every two-coefficient swap rational-rooted."""
    if leading < 1 or middle_magnitude <= leading:
        raise ValueError("expected positive leading and larger middle magnitude")
    upper = middle_magnitude**2 // (4 * leading)
    valid = []
    for constant in range(1, upper + 1):
        discriminants = (
            middle_magnitude**2 - 4 * leading * constant,
            leading**2 + 4 * middle_magnitude * constant,
            constant**2 + 4 * leading * middle_magnitude,
        )
        if all(isqrt(discriminant) ** 2 == discriminant for discriminant in discriminants):
            valid.append(constant)
    return tuple(valid)


@question_type(
    "math.swapped_quadratic_coefficients_olympiad",
    display_name={"th": "สมการกำลังสองที่สลับสัมประสิทธิ์แล้วยังมีรากตรรกยะ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการกำลังสอง",
)
class SwappedQuadraticCoefficients(WordProblem):
    def expr(self, rng: Random):
        leading = rng.randint(2, 9)
        middle_magnitude = rng.randint(leading + 3, 30)
        solutions = valid_swapped_constants(leading, middle_magnitude)
        answer = solutions[0]
        return MathDraw(
            rf"{leading}x^2-{middle_magnitude}x+a=0",
            str(answer),
            prompt=("จงหาจำนวนเต็มบวก a ที่ทำให้สมการกำลังสองมีรากตรรกยะ "
                    "และเมื่อสลับสัมประสิทธิ์สองตำแหน่งใด ๆ จากสามตำแหน่ง "
                    "สมการใหม่ยังมีรากตรรกยะเสมอ"),
            hint="ตรวจว่าดิสคริมิแนนต์ของสมการเดิมและสมการจากการสลับทั้งสามแบบเป็นกำลังสองสมบูรณ์",
            distractors=[
                str(middle_magnitude),  # ignore leading coefficient in zero-sum relation
                str(middle_magnitude + leading),  # add instead of subtract leading coefficient
                str(max(1, answer - 1)),  # do not test all swaps
                str(answer + 1),  # do not test all swaps
            ],
        )
