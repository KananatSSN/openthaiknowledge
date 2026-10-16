"""Reduce a high-degree quotient at a quadratic irrational."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def crafted_numerator(integer_part: int, irrational_part: int, coefficients: tuple[int, int, int, int]) -> tuple[int, ...]:
    """Coefficients of (k+qx)(2x^3-x)+(2x^2+2x-1)(ux^3+vx^2+wx+z)."""
    u, v, w, z = coefficients
    k, q = integer_part, irrational_part
    return (
        2 * u,
        2 * u + 2 * v + 2 * q,
        -u + 2 * v + 2 * w + 2 * k,
        -v + 2 * w + 2 * z - q,
        -w + 2 * z - k,
        -z,
    )


def floor_quadratic_irrational(integer_part: int, irrational_part: int) -> int:
    """Floor of k+q(sqrt(3)-1)/2 without floating-point rounding."""
    if irrational_part < 0:
        raise ValueError("expected a nonnegative irrational coefficient")
    return integer_part + (isqrt(3 * irrational_part**2) - irrational_part) // 2


def _polynomial_tex(coefficients: tuple[int, ...]) -> str:
    terms = []
    degree_max = len(coefficients) - 1
    for index, coefficient in enumerate(coefficients):
        if coefficient == 0:
            continue
        degree = degree_max - index
        variable = "" if degree == 0 else "a" if degree == 1 else rf"a^{{{degree}}}"
        magnitude = "" if variable and abs(coefficient) == 1 else str(abs(coefficient))
        prefix = "-" if coefficient < 0 else "+" if terms else ""
        terms.append(prefix + magnitude + variable)
    return "".join(terms) or "0"


@question_type(
    "math.quadratic_irrational_reduction_olympiad",
    display_name={"th": "ลดรูปเศษส่วนพหุนามที่จำนวนอตรรกยะกำลังสอง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เอกลักษณ์พีชคณิต",
)
class QuadraticIrrationalReduction(WordProblem):
    def expr(self, rng: Random):
        integer_part = rng.randint(3, 12)
        irrational_part = rng.randint(2, 6)
        coefficients = (rng.randint(1, 3), rng.randint(-2, 2), rng.randint(-7, -2), rng.randint(2, 6))
        numerator = crafted_numerator(integer_part, irrational_part, coefficients)
        answer = floor_quadratic_irrational(integer_part, irrational_part)
        mistaken = [
            integer_part,  # discard the residual irrational term
            integer_part + irrational_part,  # replace the irrational by one
            integer_part + irrational_part // 2,  # replace it by one half
            answer + 1,  # round upward
            answer - 1,  # round down one extra step
        ]
        distractors = [str(value) for value in dict.fromkeys(mistaken) if value != answer]
        return MathDraw(
            rf"a=\frac{{\sqrt{{3}}-1}}{{2}},\quad b=\frac{{{_polynomial_tex(numerator)}}}{{2a^3-a}}",
            str(answer),
            prompt="ให้ a และ b มีค่าตามที่กำหนด จงหาจำนวนเต็มที่มากที่สุดที่ไม่เกิน b",
            hint="ใช้สมการ 2a²+2a−1=0 ลดพหุนามก่อนหาร",
            distractors=distractors,
        )
