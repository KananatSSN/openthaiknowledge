"""Right triangles on the vertices of a regular 2n-gon (Thales)."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 3",)
)


def right_triangles(sides: int) -> int:
    """A right triangle on the circumcircle has a diameter as hypotenuse:
    sides/2 diameters, each with sides − 2 choices of the third vertex."""
    if sides % 2:
        return 0
    return sides // 2 * (sides - 2)


def half_equilateral_triangles(sides: int) -> int:
    """30–60–90 triangles: the third vertex is 60° along the circle from an
    end of a diameter, four positions per diameter (sides divisible by 6)."""
    if sides % 6:
        return 0
    return sides // 2 * 4


@question_type(
    "math.regular_polygon_right_triangles_olympiad",
    display_name={"th": "สามเหลี่ยมมุมฉากจากจุดยอดของรูปหลายเหลี่ยมปกติ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class RegularPolygonRightTriangles(WordProblem):
    def expr(self, rng: Random):
        if rng.randrange(2):
            sides = 2 * rng.randint(3, 15)
            answer = right_triangles(sides)
            asked = "รูปสามเหลี่ยมมุมฉาก"
            candidates = [sides * (sides - 2), sides // 2 * (sides - 2) // 2, sides * (sides - 1) * (sides - 2) // 6, sides // 2 * (sides - 1)]
            variant = "right"
        else:
            sides = 6 * rng.randint(1, 6)
            answer = half_equilateral_triangles(sides)
            asked = "รูปสามเหลี่ยมมุมฉากที่มีมุม 30° (ด้านยาวเป็นอัตราส่วน 1 : √3 : 2)"
            candidates = [sides // 2 * 2, sides * 4, right_triangles(sides), sides]
            variant = "half"
        wrong = [v for v in dict.fromkeys(candidates + [answer + 2, answer - 2]) if v != answer and v > 0]
        return MathDraw(
            rf"n={sides}",
            str(answer),
            prompt=f"จุดยอดทั้งหมดของรูป n เหลี่ยมด้านเท่ามุมเท่าสร้าง{asked}ได้กี่รูป",
            hint="รูปสามเหลี่ยมมุมฉากที่แนบในวงกลมมีด้านตรงข้ามมุมฉากเป็นเส้นผ่านศูนย์กลาง",
            distractors=[str(v) for v in wrong],
            variant=variant,
        )
