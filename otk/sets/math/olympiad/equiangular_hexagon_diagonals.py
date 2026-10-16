"""Recover a symmetric side expression from three equiangular-hexagon diagonals."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def pair_product_square(diagonal_ac_sq: int, diagonal_ce_sq: int, diagonal_ea_sq: int) -> int:
    """Compute (ab+bc+ca)^2 from the three alternate-vertex diagonals."""
    x, y, z = diagonal_ac_sq, diagonal_ce_sq, diagonal_ea_sq
    if min(x, y, z) <= 0:
        raise ValueError("diagonal squares must be positive")
    numerator = 2 * (x * y + y * z + z * x) - (x * x + y * y + z * z)
    if numerator <= 0 or numerator % 3:
        raise ValueError("diagonals do not give an integral target")
    return numerator // 3


@question_type(
    "math.equiangular_hexagon_diagonals_olympiad",
    display_name={"th": "ผลบวกผลคูณด้านจากเส้นทแยงมุมหกเหลี่ยมมุมเท่า"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="รูปหลายเหลี่ยม",
)
class EquiangularHexagonDiagonals(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.sample(range(2, 16), 3)
        x = a * a + a * b + b * b
        y = a * a + a * c + c * c
        z = b * b + b * c + c * c
        answer = pair_product_square(x, y, z)
        pair_sum = a * b + b * c + c * a
        return MathDraw(
            rf"AC^2={x},\quad CE^2={y},\quad EA^2={z}",
            str(answer),
            prompt=("รูปหกเหลี่ยมมุมเท่า ABCDEF มี AB=DE=a, BC=EF=b และ CD=FA=c "
                    "โดยกำหนดกำลังสองของเส้นทแยงมุม AC, CE และ EA ตามลำดับ "
                    "จงหาค่า (ab+bc+ca)^2"),
            hint="ใช้พื้นที่สามเหลี่ยม ACE จากด้านทั้งสาม แล้วเทียบกับพื้นที่จากเวกเตอร์ด้านของหกเหลี่ยม",
            distractors=[
                str(3 * answer),  # omit the sqrt(3) factor in the area relation
                str(4 * answer),  # double the side-pair sum before squaring
                str((a + b + c) ** 2),  # square the side sum instead
                str(x + y + z),  # add diagonal squares instead of using area
                str(pair_sum),  # forget the outer square
            ],
        )
