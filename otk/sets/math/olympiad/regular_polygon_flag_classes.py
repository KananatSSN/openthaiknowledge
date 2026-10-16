"""Count repeated minimal color classes in an odd regular polygon."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def minimum_smallest_color_classes(prime: int) -> int:
    """For p-cubed vertices, the least possible multiplicity is p."""
    if prime not in (3, 5, 7, 11):
        raise ValueError("expected one of the supported odd primes")
    return prime


@question_type(
    "math.regular_polygon_flag_classes_olympiad",
    display_name={"th": "ชั้นสีที่เล็กที่สุดบนรูปหลายเหลี่ยมปกติ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class RegularPolygonFlagClasses(WordProblem):
    def expr(self, rng: Random):
        prime = rng.choice((3, 5, 7, 11))
        vertices = prime**3
        return MathDraw(
            rf"N={vertices}",
            str(minimum_smallest_color_classes(prime)),
            prompt=(
                "วางธงบนจุดยอดทุกจุดของรูป N เหลี่ยมด้านเท่ามุมเท่า ใช้อย่างน้อยสองสี "
                "และจุดยอดที่มีสีเดียวกันต้องเป็นจุดยอดทั้งหมดของรูปหลายเหลี่ยม "
                "ด้านเท่ามุมเท่ารูปหนึ่ง จงหาจำนวนน้อยที่สุดที่เป็นไปได้ของ "
                "สีซึ่งมีจำนวนธงเท่ากับสีที่มีธงน้อยที่สุด"
            ),
            hint=(
                "มองสีเป็นชั้นเศษเหลือของเลขจุดยอด แล้วใช้ผลบวกรากเอกภาพ "
                "ที่มีอันดับเป็นกำลังของจำนวนเฉพาะ"
            ),
            distractors=[
                "2",  # pair opposite roots, impossible at odd order
                str(prime - 1),  # stop one class before the vanishing sum
                str(prime + 1),  # add a redundant smallest class
                str(prime**2),  # partition by p-squared residue classes
                str(vertices),  # put one color on each vertex
            ],
        )
