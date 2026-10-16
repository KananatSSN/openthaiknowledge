"""Classify polynomial divisors of factorials with a fixed offset."""

from __future__ import annotations

from math import factorial, gcd, isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2563, ข้อ 10",)
)


def positive_divisor_count(number: int) -> int:
    if number < 1:
        raise ValueError("number must be positive")
    count = 0
    for divisor in range(1, isqrt(number) + 1):
        if number % divisor == 0:
            count += 1 if divisor * divisor == number else 2
    return count


def polynomial_divisor_count(start: int, offset: int) -> int:
    """Count P in Z[x] with P(n) dividing n!+offset for all n>=start."""
    if start < 1 or offset < 1:
        raise ValueError("start and offset must be positive")
    return 2 * positive_divisor_count(gcd(factorial(start), offset))


@question_type(
    "math.factorial_offset_polynomial_divisors_olympiad",
    display_name={"th": "พหุนามที่หารแฟกทอเรียลบวกค่าคงที่"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนาม",
)
class FactorialOffsetPolynomialDivisors(WordProblem):
    def expr(self, rng: Random):
        start = rng.randint(3, 7)
        offset = 2 * rng.randint(1, 40)
        common = gcd(factorial(start), offset)
        answer = polynomial_divisor_count(start, offset)
        return MathDraw(
            rf"N={start},\quad c={offset}",
            str(answer),
            prompt=(
                "จงหาจำนวนพหุนาม P(x) สัมประสิทธิ์จำนวนเต็มที่ทำให้ "
                "P(n) หาร n!+c ลงตัวสำหรับทุกจำนวนเต็ม n≥N"
            ),
            hint=(
                "ตรึง m≥N แล้วเลือก n≡m (mod |P(m)|) ให้ใหญ่พอ "
                "จะได้ |P(m)| หาร c จึงทำให้ P เป็นพหุนามคงที่"
            ),
            distractors=[
                str(positive_divisor_count(common)),  # omit negative constants
                str(2 * positive_divisor_count(offset)),  # ignore the first factorial
                str(2 * positive_divisor_count(factorial(start))),  # ignore offset
                str(2 * common),  # count all integers in a bound
                str(answer + 1),  # include the zero polynomial
                "2",  # assume only ±1 survive
            ],
        )
