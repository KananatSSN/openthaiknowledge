"""1/(1 + tanᵖx) + 1/(1 + tanᵖ(π/2 − x)) = 1 pairs the terms."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 18",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def pair_sum(denominator: int) -> Fraction:
    """Σ_{k=0}^{D/2 − 1} 1/(1 + tanᵖ(kπ/D)): k = 0 gives 1, and k ↔ D/2 − k
    pairs the rest into sums of 1 (the middle term is 1/2 when 4 | D), so the
    total is (D + 2)/4 (source: D = 2548 → 1275/2)."""
    return Fraction(denominator + 2, 4)


@question_type(
    "math.tangent_power_pair_sum_olympiad",
    display_name={"th": "ผลบวกที่จับคู่มุมประกอบมุมฉาก"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ลำดับและอนุกรม",
)
class TangentPowerPairSum(WordProblem):
    def expr(self, rng: Random):
        denominator = 2 * rng.randint(10, 2000)
        power = rng.randint(2, 3000)
        answer = pair_sum(denominator)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(denominator, 4), Fraction(denominator - 2, 4), Fraction(denominator, 2), Fraction(denominator + 2, 2), answer - Fraction(1, 2)]) if v != answer]
        top = denominator // 2 - 1
        return MathDraw(
            rf"\sum_{{k=0}}^{{{top}}}\frac{{1}}{{1+\tan^{{{power}}}\left(\frac{{k\pi}}{{{denominator}}}\right)}}",
            frac_tex(answer),
            prompt="จงหาค่าของผลบวกต่อไปนี้",
            hint="1/(1 + tanᵖx) + 1/(1 + tanᵖ(π/2 − x)) = 1 จับคู่พจน์ที่ k กับ D/2 − k และระวังพจน์ k = 0 กับพจน์ตรงกลาง",
            distractors=wrong,
        )
