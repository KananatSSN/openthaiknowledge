"""x·f(y) + y·f(x) ≤ c·xy for all reals forces f(x) = cx/2."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2562, ข้อ 6",)
)


def bilinear_bound_value(c: int, n: int) -> Fraction:
    """f(n) for the only solution f(x) = cx/2.

    With h = f − cx/2, x = y gives h ≤ 0 on the positives and h ≥ 0 on the
    negatives; a positive x with a negative y then makes both terms of
    x·h(y) + y·h(x) ≤ 0 nonnegative, so h vanishes, and x = 0 gives h(0) = 0.
    """
    return Fraction(c * n, 2)


def _tex(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    sign = "-" if value < 0 else ""
    return rf"{sign}\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"


@question_type(
    "math.bilinear_bound_functional_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันจากอสมการ x f(y) + y f(x)"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class BilinearBoundFunctional(WordProblem):
    def expr(self, rng: Random):
        c = rng.choice([v for v in range(-9, 10) if v not in (-1, 0, 1)])
        n = rng.choice([v for v in range(-15, 16) if v not in (-1, 0, 1)])
        answer = bilinear_bound_value(c, n)
        wrong = []
        for value in (
            Fraction(c * n),  # forget the halving from x = y
            -answer,  # sign slip
            Fraction(c * n, 4),
            Fraction(c, 2),  # read f as constant
            answer + 1,
            answer - 1,
        ):
            if value != answer and value not in wrong:
                wrong.append(value)
        coefficient = "" if c == 1 else ("-" if c == -1 else str(c))
        return MathDraw(
            rf"x\,f(y)+y\,f(x)\le {coefficient}xy",
            _tex(answer),
            prompt=f"ให้ f : ℝ → ℝ สอดคล้องอสมการต่อไปนี้ทุกจำนวนจริง x, y จงหา f({n})",
            hint="ให้ x = y เพื่อเทียบ f(x) กับ cx/2 ทั้งสองฝั่งของศูนย์ แล้วใช้ x > 0 กับ y < 0",
            distractors=[_tex(value) for value in wrong],
        )
