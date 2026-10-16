"""Integer polynomials with P(n) | bⁿ + K for every n are the divisors of a gcd."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2557, ข้อ 4",)
)


def common_divisor(base: int, constant: int) -> int:
    """gcd of bⁿ + K over n ≥ 1: consecutive differences are bⁿ(b − 1), all
    multiples of b(b − 1), so the gcd is gcd(b + K, b(b − 1))."""
    return gcd(base + constant, base * (base - 1))


def divisor_count(value: int) -> int:
    return sum(1 for d in range(1, value + 1) if value % d == 0)


def polynomial_count(base: int, constant: int) -> int:
    """A prime p | P(n) divides P(n + kp), so p | bᵐ + K for all m ≥ n by
    Fermat, hence p | b(b − 1): P takes values with finitely many prime
    factors and is constant (Schur). The constants are ±d with d | gcd."""
    return 2 * divisor_count(common_divisor(base, constant))


@question_type(
    "math.exponential_divisor_polynomials_olympiad",
    display_name={"th": "พหุนามที่ค่าหาร bⁿ + K ลงตัวทุก n"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามสัมประสิทธิ์จำนวนเต็ม",
)
class ExponentialDivisorPolynomials(WordProblem):
    def expr(self, rng: Random):
        base = rng.randint(3, 40)
        constant = rng.randint(2, 300)
        g = common_divisor(base, constant)
        answer = polynomial_count(base, constant)
        wrong = []
        for value in (
            divisor_count(g),  # positive constants only
            2 * divisor_count(base + constant),  # divisors of the n = 1 value
            2,  # only ±1
            2 * g,
            answer + 2,
            max(answer - 2, 1),
        ):
            if value != answer and value not in wrong:
                wrong.append(value)
        return MathDraw(
            rf"P(n)\ \Big|\ {base}^n+{constant}\quad (n=1,2,3,\ldots)",
            str(answer),
            prompt="จงหาจำนวนพหุนาม P(x) ที่มีสัมประสิทธิ์เป็นจำนวนเต็มทั้งหมด ซึ่ง P(n) หารนิพจน์ต่อไปนี้ลงตัวทุกจำนวนเต็มบวก n",
            hint="ถ้า p หาร P(n) แล้ว p หาร P(n + kp) ใช้ทฤษฎีบทแฟร์มาต์แสดงว่า p หาร b(b − 1) แล้ว P ต้องเป็นค่าคงตัว",
            distractors=[str(value) for value in wrong],
        )
