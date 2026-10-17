"""f(xy) = f(x) + f(y) into ℚ is never injective: f(2^a) = f(3^b)."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันที่สอง ข้อ 2",))


def frac_tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def collision_exponent(f2: Fraction, f3: Fraction) -> int:
    """a·f(2) = b·f(3) with a/b = f(3)/f(2) in lowest terms; then
    f(2^a) = f(3^b) although 2^a ≠ 3^b (if the signs differ, f(2^a3^b) = f(1))."""
    return (f3 / f2).numerator


@question_type(
    "math.log_injective_collision_olympiad",
    display_name={"th": "ฟังก์ชันที่ f(xy) = f(x) + f(y) ไม่เป็นฟังก์ชันหนึ่งต่อหนึ่ง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class LogInjectiveCollision(WordProblem):
    def expr(self, rng: Random):
        while True:
            f2 = Fraction(rng.randint(1, 9), rng.randint(1, 9))
            f3 = Fraction(rng.randint(1, 9), rng.randint(1, 9))
            if f2 != f3:
                break
        answer = collision_exponent(f2, f3)
        b = (f3 / f2).denominator
        wrong = [v for v in dict.fromkeys([b, answer * b, f3.numerator * f2.denominator, answer + 1, f3.numerator]) if v != answer and v > 0]
        return MathDraw(
            rf"f(2)={frac_tex(f2)},\quad f(3)={frac_tex(f3)}",
            str(answer),
            prompt="f : ℕ → ℚ สอดคล้อง f(xy) = f(x) + f(y) ทุก x, y จงหาจำนวนนับ a ที่น้อยที่สุดซึ่งมีจำนวนนับ b ทำให้ f(2^a) = f(3^b)",
            hint="f(2^a) = a·f(2) และ f(3^b) = b·f(3) จึงต้องการ a/b = f(3)/f(2) ในรูปอย่างต่ำ",
            distractors=[str(v) for v in wrong],
        )
