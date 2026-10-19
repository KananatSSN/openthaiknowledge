"""Odd polynomial with roots 0, ±b_i: a₃·a_{2n−1} = (−1)ⁿ(Σ b_i²)(Σ b_i⁻²)·Π b_i²."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 8",)
)


def coefficient_product(roots) -> Fraction:
    """p(x) = x·Π(x² − b²), so a_{2n−1} = −e₁(b²) = −Σb² and
    a₃ = (−1)ⁿ⁻¹e_{n−1}(b²) = (−1)ⁿ⁻¹Πb²·Σb⁻². For even n and Πb = 1 the
    product is (Σb²)(Σb⁻²) ≥ n² by Cauchy–Schwarz."""
    squares = [Fraction(b) ** 2 for b in roots]
    product = Fraction(1)
    for s in squares:
        product *= s
    sign = (-1) ** len(squares)
    return sign * sum(squares) * sum(1 / s for s in squares) * product


def _num(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


@question_type(
    "math.symmetric_root_coefficient_product_olympiad",
    display_name={"th": "ผลคูณสัมประสิทธิ์ของพหุนามที่รากสมมาตร"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามสมมาตร",
)
class SymmetricRootCoefficientProduct(WordProblem):
    def expr(self, rng: Random):
        if rng.randrange(2):
            n = 2 * rng.randint(2, 1000)
            degree = 2 * n + 1
            answer = n * n
            wrong = [v for v in dict.fromkeys([n, 2 * n, (2 * n + 1) ** 2, n * (n + 1), (n - 1) ** 2, 4 * n * n]) if v != answer]
            return MathDraw(
                rf"p(x)=x^{{{degree}}}+a_{{{degree - 1}}}x^{{{degree - 1}}}+\cdots+a_{{1}}x+a_{{0}}",
                str(answer),
                prompt=(
                    f"รากทั้งหมดของ p(x) คือ 0, ±b₁, …, ±b_{n} โดย b_i เป็นจำนวนจริงบวกที่มีผลคูณเท่ากับ 1 "
                    f"จงหาค่าน้อยที่สุดของ a₃·a_{degree - 2}"
                ),
                hint="p(x) = x(x² − b₁²)⋯(x² − b_n²) อ่านสัมประสิทธิ์จากพหุนามในตัวแปร x² แล้วใช้อสมการโคชี–ชวาร์ซ",
                distractors=[str(v) for v in wrong],
                variant="minimum",
            )
        base = rng.randint(2, 5)
        roots = (Fraction(1), Fraction(base), Fraction(1, base))
        answer = coefficient_product(roots)
        squares = [b * b for b in roots]
        wrong_values = [
            -answer,  # drop the sign (−1)ⁿ
            -sum(squares),  # one coefficient only
            Fraction(-9),  # the equality value, negated
            -sum(roots) * sum(1 / b for b in roots),  # forget to square
            answer - 1,
        ]
        wrong = [_num(v) for v in dict.fromkeys(wrong_values) if v != answer]
        return MathDraw(
            rf"p(x)=x\left(x^2-1\right)\left(x^2-{base * base}\right)\left(x^2-\frac{{1}}{{{base * base}}}\right)",
            _num(answer),
            prompt="เขียน p(x) = x⁷ + a₆x⁶ + ⋯ + a₁x + a₀ จงหาค่าของ a₃·a₅",
            hint="มองเป็นพหุนามในตัวแปร t = x²: a₅ = −(ผลบวกราก) และ a₃ = −(ผลบวกของผลคูณรากทีละสองตัว)",
            distractors=wrong,
            variant="explicit",
        )
