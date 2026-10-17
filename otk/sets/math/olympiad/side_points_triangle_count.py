"""Most triangles from the vertices plus N points on the sides of a triangle."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันแรก ข้อ 10",))


def most_triangles(extra: int) -> int:
    """With kᵢ points on side i (vertices included, Σkᵢ = N + 6), only the
    collinear triples on a side are lost; C(kᵢ, 3) is convex, so the sides
    should be as equal as possible. The source (N = 17) gives 993."""
    total = extra + 3
    per_side = extra + 6
    base, extra_sides = divmod(per_side, 3)
    sides = [base + 1] * extra_sides + [base] * (3 - extra_sides)
    return comb(total, 3) - sum(comb(k, 3) for k in sides)


@question_type(
    "math.side_points_triangle_count_olympiad",
    display_name={"th": "จำนวนรูปสามเหลี่ยมมากสุดจากจุดบนด้านของรูปสามเหลี่ยม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class SidePointsTriangleCount(WordProblem):
    def expr(self, rng: Random):
        extra = rng.randint(4, 40)
        answer = most_triangles(extra)
        total = extra + 3
        wrong = [v for v in dict.fromkeys([comb(total, 3), answer - 1, answer + 3, comb(total, 3) - 3 * comb((extra + 6) // 3, 3) - 1, answer - total]) if v != answer and v > 0]
        return MathDraw(
            rf"N={extra}",
            str(answer),
            prompt="เติมจุด N จุดบนด้านของรูปสามเหลี่ยม (ไม่ซ้ำจุดยอด) รวมกับจุดยอดสามจุด จำนวนรูปสามเหลี่ยมที่มีจุดยอดจากจุดเหล่านี้มีได้มากที่สุดกี่รูป",
            hint="จำนวนทั้งหมด C(N + 3, 3) ลบสามจุดที่อยู่บนด้านเดียวกัน แล้วกระจายจุดให้ทั้งสามด้านใกล้เคียงกัน",
            distractors=[str(v) for v in wrong],
        )
