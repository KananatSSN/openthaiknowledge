"""From p₁, p₂, p₃ of three complex numbers, Newton's identities give p₄."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 7",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fourth_power_sum(p1: int, p2: int, p3: int) -> Fraction:
    """e₁ = p₁, e₂ = (p₁² − p₂)/2, e₃ = (p₃ − e₁p₂ + e₂p₁)/3 and
    p₄ = e₁p₃ − e₂p₂ + e₃p₁ (source: 1, 2, 3 → 25/6)."""
    e1 = Fraction(p1)
    e2 = (e1 * e1 - p2) / 2
    e3 = (p3 - e1 * p2 + e2 * p1) / 3
    return e1 * p3 - e2 * p2 + e3 * p1


@question_type(
    "math.complex_power_sums_olympiad",
    display_name={"th": "ผลบวกกำลังสี่ของจำนวนเชิงซ้อนสามจำนวน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามสมมาตร",
)
class ComplexPowerSums(WordProblem):
    def expr(self, rng: Random):
        p1, p2, p3 = rng.randint(-3, 4), rng.randint(-3, 6), rng.randint(-4, 8)
        answer = fourth_power_sum(p1, p2, p3)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(p1 * p3), Fraction(p2 * p2), answer + 1, Fraction(p1 * p3 + p2 * p2, 2), answer * 2]) if v != answer]
        return MathDraw(
            rf"a+b+c={p1},\ a^2+b^2+c^2={p2},\ a^3+b^3+c^3={p3}",
            frac_tex(answer),
            prompt="a, b, c เป็นจำนวนเชิงซ้อนที่สอดคล้องเงื่อนไขต่อไปนี้ จงหา a⁴ + b⁴ + c⁴",
            hint="หา ab + bc + ca และ abc จากเอกลักษณ์ของนิวตัน แล้วใช้ p₄ = e₁p₃ − e₂p₂ + e₃p₁",
            distractors=wrong,
        )
