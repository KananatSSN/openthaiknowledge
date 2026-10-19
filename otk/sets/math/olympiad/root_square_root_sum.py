"""s = √a + √b + √c over the roots of x³ − px² + qx − w² satisfies s⁴ − 2ps² − 8ws = 4q − p²."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 8",))


def quartic_value(p: int, q: int) -> int:
    """With t = √ab + √bc + √ca: s² = p + 2t and t² = q + 2ws, so
    (s² − p)² = 4q + 8ws (source: p = 9, q = 11, w = 1 → −37)."""
    return 4 * q - p * p


def three_positive_roots(p: int, q: int, r: int) -> bool:
    """Signs alternate, so no root is ≤ 0; a positive discriminant gives three real roots."""
    disc = 18 * p * q * r - 4 * p**3 * r + p * p * q * q - 4 * q**3 - 27 * r * r
    return disc > 0


CASES = tuple((p, q, w) for p in range(5, 25) for q in range(3, p * p // 3) for w in (1, 2, 3) if three_positive_roots(p, q, w * w) and 4 * q != p * p)


@question_type(
    "math.root_square_root_sum_olympiad",
    display_name={"th": "ค่าของนิพจน์ในผลบวกรากที่สองของรากพหุนาม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามสมมาตร",
)
class RootSquareRootSum(WordProblem):
    def expr(self, rng: Random):
        p, q, w = rng.choice(CASES)
        answer = quartic_value(p, q)
        wrong = [v for v in dict.fromkeys([p * p - 4 * q, 2 * q - p * p, 4 * q - p * p + 8 * w, 4 * q - 2 * p, q - p * p]) if v != answer]
        return MathDraw(
            rf"x^3-{p}x^2+{q}x-{w * w}=0,\quad s=\sqrt{{a}}+\sqrt{{b}}+\sqrt{{c}},\quad s^4-{2 * p}s^2-{8 * w}s",
            str(answer),
            prompt="a, b, c เป็นคำตอบของสมการต่อไปนี้ และ s = √a + √b + √c จงหาค่าของนิพจน์ท้ายสุด",
            hint=f"ให้ t = √(ab) + √(bc) + √(ca) จะได้ s² = {p} + 2t และ t² = {q} + 2√(abc)·s แล้วกำจัด t",
            distractors=[str(v) for v in wrong],
        )
