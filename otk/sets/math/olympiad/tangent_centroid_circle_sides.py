"""AC tangent to the circle ABG (G the centroid) iff a² + c² = 2b²."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 8",)
)


def tangent_side(bc: int, ab: int) -> int:
    """The B-median meets AC at its midpoint K; tangency gives KA² = KG·KB,
    i.e. b²/4 = m_b²/3, and m_b² = (2a² + 2c² − b²)/4 turns this into
    a² + c² = 2b². Then (a + c)² ≤ 2(a² + c²) = 4b² gives a + c ≤ 2b."""
    square = (bc * bc + ab * ab) // 2
    root = isqrt(square)
    if 2 * square != bc * bc + ab * ab or root * root != square:
        raise ValueError("not a tangent configuration")
    return root


PAIRS = tuple(
    (a, c)
    for a in range(1, 80) for c in range(a + 1, 80)
    if (a * a + c * c) % 2 == 0 and isqrt((a * a + c * c) // 2) ** 2 == (a * a + c * c) // 2
    and isqrt((a * a + c * c) // 2) + a > c
)


@question_type(
    "math.tangent_centroid_circle_sides_olympiad",
    display_name={"th": "ด้านของสามเหลี่ยมเมื่อ AC สัมผัสวงกลมผ่าน A, B และจุดเซนทรอยด์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: เส้นสัมผัสวงกลม",
)
class TangentCentroidCircleSides(WordProblem):
    def expr(self, rng: Random):
        a, c = rng.choice(PAIRS)
        if rng.randrange(2):
            a, c = c, a
        answer = tangent_side(a, c)
        wrong = [v for v in dict.fromkeys([(a + c) // 2, isqrt(a * a + c * c), abs(c - a), answer + 1, answer - 1, (a + c + 1) // 2 + 1]) if v != answer and v > 0]
        return MathDraw(
            rf"BC={a},\quad AB={c}",
            str(answer),
            prompt="G เป็นจุดเซนทรอยด์ของรูปสามเหลี่ยม ABC และเส้นตรง AC สัมผัสวงกลมล้อมรอบรูปสามเหลี่ยม ABG จงหา AC",
            hint="ให้ K เป็นจุดกึ่งกลาง AC ใช้กำลังของจุด K: KA² = KG·KB และ KG = KB/3",
            distractors=[str(v) for v in wrong],
        )
