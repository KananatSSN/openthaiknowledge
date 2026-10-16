"""Every prime factor of (n − 1)! − 1 exceeds n."""

from __future__ import annotations

from math import factorial
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 1",)
)


def smallest_prime_factor(value: int) -> int:
    d = 2
    while d * d <= value:
        if value % d == 0:
            return d
        d += 1
    return value


def factorial_minus_one_factor(n: int) -> int:
    """q | (n − 1)! − 1 rules out q ≤ n − 1, and q = n would need
    (n − 1)! ≡ 1 (mod n), against Wilson's (n − 1)! ≡ −1 for n ≥ 3; so every
    such q exceeds n, and hence every prime p | n!."""
    return smallest_prime_factor(factorial(n - 1) - 1)


def _primes_up_to(n: int) -> list[int]:
    return [p for p in range(2, n + 1) if smallest_prime_factor(p) == p]


@question_type(
    "math.factorial_minus_one_prime_olympiad",
    display_name={"th": "ตัวประกอบเฉพาะน้อยสุดของ (n − 1)! − 1"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class FactorialMinusOnePrime(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 14)
        answer = factorial_minus_one_factor(n)
        largest_small = _primes_up_to(n)[-1]
        wrong = [v for v in dict.fromkeys([
            largest_small,  # a prime dividing n!
            n, n - 1, n + 1, 2 * n + 1,
            answer + 2,
        ]) if v != answer]
        return MathDraw(
            rf"{n - 1}!-1={factorial(n - 1) - 1}",
            str(answer),
            prompt="จงหาตัวประกอบเฉพาะที่น้อยที่สุดของจำนวนต่อไปนี้",
            hint=f"จำนวนเฉพาะ q ที่หาร ({n - 1})! − 1 ต้องมากกว่า {n - 1} และ q = {n} ขัดกับทฤษฎีบทวิลสัน",
            distractors=[str(v) for v in wrong],
        )
