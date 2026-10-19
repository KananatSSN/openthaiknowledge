"""Sides √(a₁² + a₂²), …: the triangle exists and 16Δ² is a quadratic form."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันที่สอง ข้อ 4",)
)


def sixteen_area_sq(x: int, y: int, z: int) -> int:
    """16Δ² = 2xy + 2yz + 2zx − x² − y² − z² with x, y, z the squared sides."""
    return 2 * (x * y + y * z + z * x) - x * x - y * y - z * z


def combined(t1, t2) -> int:
    """With squared sides adding, 16Δ₃² = Q(u₁ + u₂) = Q(u₁) + Q(u₂) + 2B(u₁, u₂)
    for the Heron form Q. Aczél's inequality for this Lorentzian form gives
    B(u₁, u₂) ≥ √(Q(u₁)Q(u₂)) > 0, so the third triangle exists; the source's
    altitude inequality p₃² ≥ p₁² + p₂² is checked numerically in the tests."""
    (a1, b1, c1), (a2, b2, c2) = t1, t2
    return sixteen_area_sq(a1 * a1 + a2 * a2, b1 * b1 + b2 * b2, c1 * c1 + c2 * c2)


TRIANGLES = tuple((a, b, c) for a in range(2, 12) for b in range(a, 12) for c in range(b, 12) if c < a + b)


@question_type(
    "math.squared_side_triangle_area_olympiad",
    display_name={"th": "พื้นที่ของรูปสามเหลี่ยมที่ด้านยกกำลังสองเป็นผลบวก"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สามเหลี่ยม",
)
class SquaredSideTriangleArea(WordProblem):
    def expr(self, rng: Random):
        t1, t2 = rng.choice(TRIANGLES), rng.choice(TRIANGLES)
        answer = combined(t1, t2)
        q1 = sixteen_area_sq(*(v * v for v in t1))
        q2 = sixteen_area_sq(*(v * v for v in t2))
        wrong = [v for v in dict.fromkeys([q1 + q2, 2 * (q1 + q2), answer + 2, answer - 4, abs(q1 - q2) + answer // 2]) if v != answer and v > 0]
        (a1, b1, c1), (a2, b2, c2) = t1, t2
        return MathDraw(
            rf"({a1},{b1},{c1}),\ ({a2},{b2},{c2})",
            str(answer),
            prompt=(
                "รูปสามเหลี่ยมสองรูปมีด้านยาวดังนี้ สร้างรูปสามเหลี่ยมที่สามซึ่งมีด้าน "
                "a₃ = √(a₁² + a₂²), b₃ = √(b₁² + b₂²), c₃ = √(c₁² + c₂²) ให้ Δ₃ เป็นพื้นที่ของรูปที่สาม จงหา 16Δ₃²"
            ),
            hint="สูตรเฮรอนในรูปกำลังสองของด้าน: 16Δ² = 2(xy + yz + zx) − x² − y² − z² เมื่อ x, y, z เป็นกำลังสองของด้าน",
            distractors=[str(v) for v in wrong],
        )
