"""Positive real roots with product 1: Σ 1/e_k ≤ Σ 1/C(n, k)."""

from __future__ import annotations

from fractions import Fraction
from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 7",)
)


def reciprocal_maximum(n: int) -> Fraction:
    """All roots are positive (the signs alternate) with product 1, so each
    e_k is a sum of C(n, k) terms with product 1 and e_k ≥ C(n, k) by AM–GM."""
    return sum((Fraction(1, comb(n, k)) for k in range(1, n)), Fraction(0))


def _tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


@question_type(
    "math.symmetric_reciprocal_bound_olympiad",
    display_name={"th": "ค่ามากสุดของผลบวกส่วนกลับของสัมประสิทธิ์พหุนามรากบวก"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามสมมาตร",
)
class SymmetricReciprocalBound(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(3, 9)
        answer = reciprocal_maximum(n)
        wrong = [_tex(v) for v in dict.fromkeys([
            Fraction(n - 1, n),  # every e_k at least n
            sum((Fraction(1, comb(n, k)) for k in range(0, n + 1)), Fraction(0)),  # include e₀ and eₙ
            Fraction(2, n),  # only the two outer terms
            answer * 2,
            Fraction(n - 1, comb(n, 2)),
        ]) if v != answer]
        return MathDraw(
            rf"x^{{{n}}}-e_{{1}}x^{{{n - 1}}}+e_{{2}}x^{{{n - 2}}}-\cdots+(-1)^{{{n}}}=0",
            _tex(answer),
            prompt=(
                f"e₁, e₂, …, e_{n - 1} เป็นจำนวนจริงบวก และสมการต่อไปนี้มีรากเป็นจำนวนจริงทั้งหมด "
                f"จงหาค่ามากที่สุดของ 1/e₁ + 1/e₂ + ⋯ + 1/e_{n - 1}"
            ),
            hint="เครื่องหมายสลับทำให้รากเป็นบวกทั้งหมดและมีผลคูณ 1 ใช้ AM–GM กับแต่ละ e_k",
            distractors=wrong,
        )
