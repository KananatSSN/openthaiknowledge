"""With p = a/(a − b), q = b/(b − c), r = c/(c − a): pq + qr + rp = p + q + r − 1, so Σ(1 + p)² = (p + q + r)² + 5."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันที่สอง ข้อ 6",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def square_sum(a: int, b: int, c: int) -> Fraction:
    """Σ((2a − b)/(a − b))² = S² + 5 with S = Σ a/(a − b), because
    (p − 1)(q − 1)(r − 1) = pqr. Hence the source bound ≥ 5."""
    s = Fraction(a, a - b) + Fraction(b, b - c) + Fraction(c, c - a)
    return s * s + 5


@question_type(
    "math.cyclic_ratio_square_sum_olympiad",
    display_name={"th": "ค่าผลบวกกำลังสองของอัตราส่วนวัฏจักร"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class CyclicRatioSquareSum(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.sample(range(-12, 13), 3)
        answer = square_sum(a, b, c)
        s = Fraction(a, a - b) + Fraction(b, b - c) + Fraction(c, c - a)
        plus = sum(Fraction(2 * x + y, x - y) ** 2 for x, y in ((a, b), (b, c), (c, a)))
        wrong = [frac_tex(v) for v in dict.fromkeys([s * s, Fraction(5), s * s + 3, plus, (s + 1) ** 2 + 5]) if v != answer]
        return MathDraw(
            rf"a={a},\ b={b},\ c={c},\quad \left(\frac{{2a-b}}{{a-b}}\right)^2+\left(\frac{{2b-c}}{{b-c}}\right)^2+\left(\frac{{2c-a}}{{c-a}}\right)^2",
            frac_tex(answer),
            prompt="จงหาค่าของนิพจน์ต่อไปนี้ (นิพจน์นี้มีค่าอย่างน้อย 5 เสมอเมื่อ a, b, c ต่างกัน)",
            hint="ให้ p = a/(a − b) เป็นต้น จะได้ (2a − b)/(a − b) = 1 + p และ pq + qr + rp = p + q + r − 1",
            distractors=wrong,
        )
