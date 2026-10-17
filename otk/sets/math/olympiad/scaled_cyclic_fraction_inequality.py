"""Minimum of Σ (4a − s)/(2b + s)² when abc = s³."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2562, ข้อ 5",)
)


def cyclic_fraction_sum(a, b, c, s=1):
    return sum(
        (4 * x - s) / (2 * y + s) ** 2 for x, y in ((a, b), (b, c), (c, a))
    )


def scaled_minimum(s: int) -> Fraction:
    """Putting a = s·a′ (and so on) divides every term by s, leaving the
    source inequality Σ (4a′ − 1)/(2b′ + 1)² ≥ 1 under a′b′c′ = 1, with
    equality at a′ = b′ = c′ = 1."""
    if s < 1:
        raise ValueError("s must be positive")
    return Fraction(1, s)


def _tex(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    sign = "-" if value < 0 else ""
    return rf"{sign}\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"


@question_type(
    "math.scaled_cyclic_fraction_inequality_olympiad",
    display_name={"th": "ค่าต่ำสุดของผลบวกเศษส่วนวนรอบเมื่อผลคูณคงตัว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class ScaledCyclicFractionInequality(WordProblem):
    def expr(self, rng: Random):
        s = rng.randint(2, 9)
        answer = scaled_minimum(s)
        wrong = []
        for value in (
            Fraction(3 * (4 - s), (2 + s) ** 2),  # test a = b = c = 1, not s
            Fraction(1, s * s),  # scale the terms by s²
            Fraction(3, s),  # count three equal terms twice
            Fraction(1, 3 * s),  # one term only
            Fraction(1),  # keep the unscaled minimum
            Fraction(0),  # assume a negative numerator can reach zero
        ):
            if value != answer and value not in wrong:
                wrong.append(value)
        num = "" if s == 1 else str(s)
        terms = "+".join(
            rf"\frac{{4{x}-{num}}}{{\left(2{y}+{num}\right)^2}}"
            for x, y in (("a", "b"), ("b", "c"), ("c", "a"))
        )
        return MathDraw(
            rf"abc={s**3},\quad S={terms}",
            _tex(answer),
            prompt="ให้ a, b, c เป็นจำนวนจริงบวกที่สอดคล้องเงื่อนไขต่อไปนี้ จงหาค่าต่ำสุดของ S",
            hint=f"แทน a = {s}a′, b = {s}b′, c = {s}c′ แล้วพิจารณากรณีเท่ากันเมื่อ a′ = b′ = c′ = 1",
            distractors=[_tex(value) for value in wrong],
        )
