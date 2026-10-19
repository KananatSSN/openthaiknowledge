"""Σ_{i<j} cos(θᵢ − θⱼ) = (|Σ e^{iθ}|² − n)/2 ≥ −n/2."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 21",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def minimum(n: int, scale: int) -> Fraction:
    """|Σ e^{iθₖ}|² = n + 2Σ_{i<j} cos(θᵢ − θⱼ) ≥ 0, with equality for equally
    spaced angles (source: n = 3 → −3/2)."""
    return Fraction(-n * scale, 2)


@question_type(
    "math.cosine_difference_minimum_olympiad",
    display_name={"th": "ค่าต่ำสุดของผลบวกโคไซน์ของผลต่างมุม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class CosineDifferenceMinimum(WordProblem):
    def expr(self, rng: Random):
        n, scale = rng.randint(3, 12), rng.choice([1, 1, 2, 3])
        answer = minimum(n, scale)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(-n * (n - 1) * scale, 2), Fraction(-n * scale), Fraction(-3 * scale, 2), Fraction(-scale), Fraction(-(n - 1) * scale, 2)]) if v != answer]
        k = "" if scale == 1 else str(scale)
        return MathDraw(
            rf"{k}\sum_{{1\le i<j\le {n}}}\cos(\theta_i-\theta_j)",
            frac_tex(answer),
            prompt=f"ให้ θ₁, θ₂, …, θₙ (n = {n}) เป็นจำนวนจริงใด ๆ จงหาค่าต่ำสุดของนิพจน์ต่อไปนี้",
            hint="พิจารณา |e^{iθ₁} + … + e^{iθₙ}|² = n + 2Σ cos(θᵢ − θⱼ) ≥ 0",
            distractors=wrong,
        )
