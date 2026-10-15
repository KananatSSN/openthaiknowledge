"""Use cycle generators to explain a totient divisibility."""

from __future__ import annotations

from math import factorial
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2563, ข้อ 1",)
)


def euler_totient(number: int) -> int:
    """Count reduced residues through the Euler product formula."""
    if number < 1:
        raise ValueError("number must be positive")
    result = number
    remaining = number
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            result -= result // divisor
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        result -= result // remaining
    return result


def factorial_totient_quotient(index: int) -> int:
    """The integer n!/phi(2n)."""
    if index < 1:
        raise ValueError("index must be positive")
    quotient, remainder = divmod(factorial(index), euler_totient(2 * index))
    if remainder:
        raise ArithmeticError("the totient divisibility must hold")
    return quotient


@question_type(
    "math.totient_factorial_divisibility_olympiad",
    display_name={"th": "ฟังก์ชันออยเลอร์หารแฟกทอเรียล"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class TotientFactorialDivisibility(WordProblem):
    def expr(self, rng: Random):
        index = rng.randint(4, 13)
        denominator = euler_totient(2 * index)
        answer = factorial_totient_quotient(index)
        return MathDraw(
            rf"n={index},\quad \varphi(2n)={denominator}",
            str(answer),
            prompt="จงหาค่าของ n!/φ(2n) ซึ่งเป็นจำนวนเต็มเสมอ",
            hint=(
                "จำนวนวงรอบยาว n ใน S_n คือ (n−1)! "
                "และวงรอบที่สร้างกลุ่มย่อยเดียวกันมี φ(n) วงรอบ"
            ),
            distractors=[
                str(factorial(index - 1) // denominator),  # use (n−1)! directly
                str(factorial(index)),  # omit the totient divisor
                str(max(1, answer // 2)),  # divide by an extra factor two
                str(answer * 2),  # miss the factor two when n is even
                str(denominator),  # return the totient itself
                str(answer + index),  # add n instead of multiplying by it
            ],
        )
