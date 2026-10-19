"""A triangulation of a convex h-gon with N interior points has 2N + h − 2 triangles."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 7",)
)


def triangle_count(corners: int, interior: int) -> int:
    """Angle sum: T·180° = (h − 2)·180° + N·360°."""
    return 2 * interior + corners - 2


@question_type(
    "math.triangulation_triangle_count_olympiad",
    display_name={"th": "จำนวนสามเหลี่ยมในการแบ่งรูปหลายเหลี่ยมนูนที่มีจุดภายใน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class TriangulationTriangleCount(WordProblem):
    def expr(self, rng: Random):
        corners = rng.randint(3, 12)
        interior = rng.randint(5, 3000)
        answer = triangle_count(corners, interior)
        wrong = [v for v in dict.fromkeys([
            interior + corners - 2,  # one triangle per point
            2 * interior + corners,  # forget the −2
            3 * interior + corners - 2,  # each point splits into three, net +3
            2 * interior + corners - 1,
            2 * (interior + corners) - 2,
        ]) if v != answer]
        return MathDraw(
            rf"h={corners},\quad N={interior}",
            str(answer),
            prompt=(
                "รูปหลายเหลี่ยมนูน h เหลี่ยมมีจุด N จุดอยู่ภายใน โดยไม่มีสามจุดใดในบรรดาจุดยอดและจุดเหล่านี้อยู่บนเส้นตรงเดียวกัน "
                "แบ่งรูปเป็นรูปสามเหลี่ยมที่มีจุดยอดเป็นจุดเหล่านี้ทั้งหมด (ทุกจุดถูกใช้ และสามเหลี่ยมไม่ซ้อนกัน) ได้สามเหลี่ยมกี่รูป"
            ),
            hint="เทียบผลบวกมุมภายในของทุกสามเหลี่ยมกับมุมรอบจุดภายในแต่ละจุด (360°) และมุมภายในของรูปหลายเหลี่ยม",
            distractors=[str(v) for v in wrong],
        )
