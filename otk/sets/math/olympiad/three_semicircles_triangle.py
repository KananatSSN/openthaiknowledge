"""Area of an equilateral triangle from three tangent semicircles."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def equilateral_area_from_semicircle_radius(radius: int) -> int:
    """Return the coefficient of sqrt(3) in the triangle area."""
    if radius <= 0:
        raise ValueError("expected positive radius")
    # Centers of two adjacent radius-r semicircles have vertical
    # separation r and horizontal separation L-sqrt(3)*r. Tangency
    # gives (L-sqrt(3)*r)^2+r^2=(2r)^2, hence L=2sqrt(3)*r.
    return 3 * radius**2


@question_type(
    "math.three_tangent_semicircles_triangle_area_olympiad",
    display_name={"th": "พื้นที่สามเหลี่ยมด้านเท่าจากครึ่งวงกลมสัมผัสกันสามรูป"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class ThreeTangentSemicirclesTriangleArea(WordProblem):
    def expr(self, rng: Random):
        radius = rng.randint(2, 12)
        answer = equilateral_area_from_semicircle_radius(radius)
        return MathDraw(
            rf"r={radius}",
            str(answer),
            prompt=("ในสามเหลี่ยมด้านเท่า ABC วางครึ่งวงกลมรัศมี r สามรูป "
                    "ให้เส้นผ่านศูนย์กลางอยู่บน AB, BC, CA ตามลำดับ "
                    "ส่วนโค้งอยู่ภายในสามเหลี่ยม รูปบน AB สัมผัสด้าน AC "
                    "รูปบน BC สัมผัสด้าน AB และรูปบน CA สัมผัสด้าน BC "
                    "ครึ่งวงกลมทั้งสามสัมผัสกันเป็นคู่ "
                    "ถ้าพื้นที่สามเหลี่ยมเป็น k√3 จงหา k"),
            hint=r"(L-\sqrt{3}r)^2+r^2=(2r)^2",
            distractors=[
                str(radius**2),  # miss factor from three equal arcs
                str(6 * radius**2),  # double triangular area
                str(12 * radius**2),  # use the equilateral side as 4sqrt(3)r
                str(3 * radius),  # forget to square the radius
            ],
        )
