"""For K ≡ 23 (mod 24) and p > 3, 24 | p² + K, which pushes τ(p² + K) up; search the primes below a bound."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันที่สอง ข้อ 5",))


SMALL_PRIMES = tuple(p for p in range(2, 200) if all(p % f for f in range(2, int(p**0.5) + 1)))


def divisor_count(n: int) -> int:
    count, f = 1, 2
    while f * f <= n:
        e = 0
        while n % f == 0:
            n //= f
            e += 1
        count *= e + 1
        f += 1
    return count * (2 if n > 1 else 1)


def qualifying(k: int, limit: int) -> list[int]:
    """Primes p < 200 with τ(p² + K) < limit (source: K = 2543, limit 16 →
    only p = 2: 2547 = 3²·283 has 6 divisors; p = 3 gives 2552 with 16)."""
    return [p for p in SMALL_PRIMES if divisor_count(p * p + k) < limit]


@question_type(
    "math.divisor_count_prime_square_olympiad",
    display_name={"th": "จำนวนเฉพาะที่ทำให้ p² + K มีตัวหารน้อย"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ตัวประกอบของจำนวนเต็ม",
)
class DivisorCountPrimeSquare(WordProblem):
    def expr(self, rng: Random):
        while True:
            k = 24 * rng.randint(20, 300) + 23
            limit = rng.choice([12, 16])
            found = qualifying(k, limit)
            if 1 <= len(found) <= 3:
                break
        answer = sum(found)
        near = [p for p in SMALL_PRIMES if divisor_count(p * p + k) <= limit]
        wrong = [v for v in dict.fromkeys([sum(near), sum(found) + 3 if 3 not in found else sum(found) - 3 + 5, 2 if 2 not in found else 5, sum(p for p in SMALL_PRIMES[:6] if divisor_count(p * p + k) < 2 * limit), answer + 2]) if v != answer]
        return MathDraw(
            rf"\tau(p^2+{k})<{limit}",
            str(answer),
            prompt=f"จงหาผลบวกของจำนวนเฉพาะ p < 200 ทั้งหมดที่ทำให้ p² + {k} มีจำนวนตัวหารบวกที่แตกต่างกันน้อยกว่า {limit} ตัว",
            hint="ถ้า p > 3 แล้ว p² ≡ 1 (mod 24) จึง 24 หาร p² + K ทำให้มีตัวหารมาก ตรวจ p = 2 และ p = 3 แยกต่างหาก",
            distractors=[str(v) for v in wrong],
        )
