"""a ∗ b = (a + b + α)/(ab + t(t + α)) makes t ∗ w = 1/t for every w, so the chain collapses."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 17",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def chain_value(alpha: int, t: int, last: int) -> Fraction:
    """t ∗ w = (t + w + α)/(t(w + t + α)) = 1/t, so evaluate
    0 ∗ (1 ∗ (… ((t − 1) ∗ 1/t))) by hand-sized fractions
    (source: α = 1, t = 3 → 23/233)."""
    beta = t * (t + alpha)
    value = Fraction(1, t)
    for a in range(t - 1, -1, -1):
        value = (a + value + alpha) / (a * value + beta)
    return value


@question_type(
    "math.collapsing_operation_chain_olympiad",
    display_name={"th": "ค่าของการดำเนินการซ้อนที่ยุบตัว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ตัวดำเนินการนิยามใหม่",
)
class CollapsingOperationChain(WordProblem):
    def expr(self, rng: Random):
        alpha, t = rng.randint(1, 4), rng.randint(2, 5)
        last = rng.randint(100, 3000)
        answer = chain_value(alpha, t, last)
        beta = t * (t + alpha)
        skip = Fraction(1, t)
        for a in range(t - 2, -1, -1):
            skip = (a + skip + alpha) / (a * skip + beta)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(1, t), skip, Fraction(1, beta), (answer + 1) / 2, Fraction(alpha + 1, beta)]) if v != answer]
        return MathDraw(
            rf"a*b=\frac{{a+b+{alpha}}}{{ab+{beta}}},\quad 0*(1*(2*(\cdots({last - 1}*{last})\cdots)))",
            frac_tex(answer),
            prompt="ให้ a, b ≥ 0 และนิยามการดำเนินการ ∗ ดังนี้ จงหาค่าของนิพจน์",
            hint="ลองหาค่า a ที่ทำให้ a ∗ w ไม่ขึ้นกับ w: ตัวส่วน aw + β ต้องเป็น a เท่าของตัวเศษ",
            distractors=wrong,
        )
