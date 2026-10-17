"""Maximise a·b^(1/2)·c^(1/3)·d^(1/4) on a linear constraint: each term cᵢxᵢ is proportional to its weight."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 20",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


WEIGHTS = (Fraction(1), Fraction(1, 2), Fraction(1, 3), Fraction(1, 4))


def maximiser(coeffs: tuple[int, int, int, int], total: int) -> tuple[Fraction, ...]:
    """Weighted AM–GM: the maximum of Π xᵢ^wᵢ under Σ cᵢxᵢ = S has
    cᵢxᵢ = wᵢS/W with W = Σwᵢ = 25/12 (source: 36, 4, 4, 3 and S = 25 give
    a, b, c, d = 1/3, 3/2, 1, 1 and maximum √6/6)."""
    w_total = sum(WEIGHTS)
    return tuple(w * total / (w_total * c) for w, c in zip(WEIGHTS, coeffs))


@question_type(
    "math.weighted_amgm_maximiser_olympiad",
    display_name={"th": "ค่าของตัวแปรที่ทำให้ผลคูณถ่วงน้ำหนักสูงสุด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class WeightedAmgmMaximiser(WordProblem):
    def expr(self, rng: Random):
        coeffs = tuple(rng.randint(1, 40) for _ in range(4))
        total = rng.choice([25, 50, 12, 24, 100])
        which = rng.randint(0, 3)
        point = maximiser(coeffs, total)
        answer = point[which]
        w = WEIGHTS[which]
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(total, 4 * coeffs[which]), w * total / coeffs[which], point[(which + 1) % 4], Fraction(total, coeffs[which]) * Fraction(12, 25) , answer * 2]) if v != answer]
        name = "abcd"[which]
        return MathDraw(
            rf"{coeffs[0]}a+{coeffs[1]}b+{coeffs[2]}c+{coeffs[3]}d={total},\quad a\,b^{{1/2}}c^{{1/3}}d^{{1/4}}",
            frac_tex(answer),
            prompt=f"a, b, c, d > 0 และสอดคล้องสมการต่อไปนี้ เมื่อผลคูณ ab^(1/2)c^(1/3)d^(1/4) มีค่าสูงสุด จงหาค่า {name}",
            hint="ใช้อสมการ AM–GM แบบถ่วงน้ำหนัก ค่าสูงสุดเกิดเมื่อแต่ละพจน์ cᵢxᵢ เป็นสัดส่วนกับน้ำหนัก 1, 1/2, 1/3, 1/4",
            distractors=wrong,
        )
