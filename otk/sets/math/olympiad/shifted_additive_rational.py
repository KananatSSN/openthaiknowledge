"""f(x + y) = f(x) + f(y) + c on ℚ: g = f + c is additive, so f(t) = (b + c)t/a − c."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันที่สอง ข้อ 2",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def value_at(c: int, a: int, b: int, t: int) -> Fraction:
    """g(x) = f(x) + c satisfies g(x + y) = g(x) + g(y) on ℚ, so g(x) = kx with
    k = (b + c)/a (source: c = 2547, f(2004) = 2547 → f(2547) = 1311705/334)."""
    return Fraction((b + c) * t, a) - c


@question_type(
    "math.shifted_additive_rational_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันบวกที่มีค่าคงตัวบนจำนวนตรรกยะ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class ShiftedAdditiveRational(WordProblem):
    def expr(self, rng: Random):
        c, a, b = rng.randint(10, 3000), rng.randint(10, 3000), rng.randint(10, 3000)
        t = rng.randint(10, 3000)
        answer = value_at(c, a, b, t)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(b * t, a), Fraction((b + c) * t, a), Fraction((b - c) * t, a) + c, Fraction(b * t, a) - c, Fraction((b + c) * t, a) + c]) if v != answer]
        return MathDraw(
            rf"f(x+y)=f(x)+f(y)+{c},\quad f({a})={b}",
            frac_tex(answer),
            prompt=f"f : ℚ → ℚ สอดคล้องสมการต่อไปนี้สำหรับทุก x, y ∈ ℚ จงหา f({t})",
            hint="ให้ g(x) = f(x) + c จะได้ g(x + y) = g(x) + g(y) บนจำนวนตรรกยะ จึง g(x) = kx",
            distractors=wrong,
        )
