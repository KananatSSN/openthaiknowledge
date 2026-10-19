"""Maximise αa + βb + γc on pa² + qb² + rc² = K by Cauchy–Schwarz: each variable is (coefficient/weight)·t."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 19",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def _cases():
    out = []
    for weights in ((9, 4, 1), (1, 4, 9), (4, 1, 9), (1, 1, 4), (9, 1, 4), (16, 4, 1)):
        for coeffs in ((1, 2, 3), (2, 1, 1), (3, 2, 1), (1, 1, 2), (2, 3, 1)):
            w = sum(Fraction(c * c, p) for c, p in zip(coeffs, weights))
            for t in range(1, 7):
                k = t * t * w
                if k.denominator == 1:
                    out.append((weights, coeffs, t, int(k)))
    return tuple(out)


CASES = _cases()


def maximiser(weights: tuple[int, ...], coeffs: tuple[int, ...], t: int) -> tuple[Fraction, ...]:
    """(Σ cᵢxᵢ)² ≤ (Σ wᵢxᵢ²)(Σ cᵢ²/wᵢ) with equality when wᵢxᵢ/cᵢ is constant
    (source: weights 9, 4, 1, coefficients 1, 2, 3, K = 91 → (1/3, 3/2, 9))."""
    return tuple(Fraction(c * t, p) for c, p in zip(coeffs, weights))


@question_type(
    "math.cauchy_weighted_maximiser_olympiad",
    display_name={"th": "จุดที่ทำให้ผลบวกเชิงเส้นมากสุดบนทรงรี"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class CauchyWeightedMaximiser(WordProblem):
    def expr(self, rng: Random):
        weights, coeffs, t, k = rng.choice(CASES)
        point = maximiser(weights, coeffs, t)
        which = rng.randint(0, 2)
        answer = point[which]
        wrong = [frac_tex(v) for v in dict.fromkeys([point[(which + 1) % 3], Fraction(coeffs[which] * t, 1), Fraction(t, weights[which]), Fraction(coeffs[which] * t * t, weights[which]), answer * 2]) if v != answer]
        name = "abc"[which]
        return MathDraw(
            rf"{weights[0]}a^2+{weights[1]}b^2+{weights[2]}c^2={k},\quad {coeffs[0]}a+{coeffs[1]}b+{coeffs[2]}c",
            frac_tex(answer),
            prompt=f"a, b, c เป็นจำนวนจริงบวกที่สอดคล้องเงื่อนไข เมื่อนิพจน์เชิงเส้นมีค่าสูงสุด จงหาค่า {name}",
            hint="ใช้อสมการโคชี–ชวาร์ซ (Σ cᵢxᵢ)² ≤ (Σ wᵢxᵢ²)(Σ cᵢ²/wᵢ) สมการเมื่อ wᵢxᵢ/cᵢ เท่ากันทุกตัว",
            distractors=wrong,
        )
