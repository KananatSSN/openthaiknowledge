"""Most sides of a convex polygon cut into triangles on regular n-gon vertices."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2562, ข้อ 9",)
)


def most_sides(n: int) -> int:
    """Every angle is a multiple of π/n, so each corner is at most (n−1)π/n
    and (m − 2)π ≤ m(n − 1)π/n gives m ≤ 2n. For odd n the regular 2n-gon,
    fanned from its centre, uses triangles with angles π/n, (n−1)π/2n twice."""
    if n % 2 == 0 or n < 3:
        raise ValueError("n must be odd and at least 3")
    return 2 * n


@question_type(
    "math.regular_vertex_triangle_dissection_olympiad",
    display_name={"th": "จำนวนเหลี่ยมมากสุดของรูปที่ตัดเป็นสามเหลี่ยมจากรูปหลายเหลี่ยมปกติ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: รูปหลายเหลี่ยมปกติ",
)
class RegularVertexTriangleDissection(WordProblem):
    def expr(self, rng: Random):
        n = rng.randrange(5, 2600, 2)
        answer = most_sides(n)
        options = [n, 2 * n - 1, 2 * n - 2, 2 * n + 1, 2 * n + 2, n - 1]
        return MathDraw(
            "",
            str(answer),
            prompt=(
                f"เรียกสามเหลี่ยมที่จุดยอดทั้งสามเป็นจุดยอดของรูป {n} เหลี่ยมด้านเท่ามุมเท่า"
                "รูปใดรูปหนึ่ง (ขนาดใดก็ได้) ว่าสามเหลี่ยมดี "
                "รูปหลายเหลี่ยมนูนที่ตัดแบ่งออกเป็นสามเหลี่ยมดีหลายรูปได้ มีจำนวนเหลี่ยมมากสุดเท่าใด"
            ),
            hint=f"มุมทุกมุมของสามเหลี่ยมดีเป็นพหุคูณของ 180°/{n} มุมภายในแต่ละมุมของรูปนูนจึงไม่เกิน {n - 1}·180°/{n}",
            distractors=[str(v) for v in options],
        )
