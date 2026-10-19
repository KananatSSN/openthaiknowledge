"""f(x + f(y)) = αx + α²y + γ forces f(t) = αt + γ/(α + 1)."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 8",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def value_at(alpha: int, gamma: int, t: int) -> Fraction:
    """x ↦ x + f(y) shows f is affine with slope α: comparing y-coefficients
    gives α·(slope of f) = α², and the constants give (α + 1)c = γ
    (source: α = 2, γ = 2547 → f(0) = 849)."""
    return alpha * t + Fraction(gamma, alpha + 1)


@question_type(
    "math.composed_linear_functional_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันที่ซ้อนอาร์กิวเมนต์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class ComposedLinearFunctional(WordProblem):
    def expr(self, rng: Random):
        alpha = rng.randint(2, 5)
        gamma = rng.randint(100, 3000)
        t = rng.choice([0, 0, rng.randint(1, 20)])
        answer = value_at(alpha, gamma, t)
        c = Fraction(gamma, alpha + 1)
        wrong = [frac_tex(v) for v in dict.fromkeys([alpha * t + Fraction(gamma, alpha), alpha * t + Fraction(gamma), alpha * t + Fraction(gamma, 2 * alpha + 1), alpha * alpha * t + c, alpha * t - c]) if v != answer]
        return MathDraw(
            rf"f(x+f(y))={alpha}x+{alpha * alpha}y+{gamma}",
            frac_tex(answer),
            prompt=f"f : ℝ → ℝ สอดคล้องสมการต่อไปนี้สำหรับทุก x, y ∈ ℝ จงหา f({t})",
            hint="แทน x = t − f(y) จะได้ f เป็นฟังก์ชันเชิงเส้น ลองสมมติ f(t) = αt + c แล้วเทียบค่าคงตัว",
            distractors=wrong,
        )
