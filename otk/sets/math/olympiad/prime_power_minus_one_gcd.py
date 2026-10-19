"""The largest integer dividing pᵏ − 1 for every prime p above a bound."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 1",)
)


def _is_prime(n: int) -> bool:
    return n > 1 and all(n % d for d in range(2, int(n**0.5) + 1))


def _exponent_fits(q: int, e: int, k: int) -> bool:
    """x^k ≡ 1 (mod q^e) for every x prime to q."""
    modulus = q**e
    return all(pow(x, k, modulus) == 1 for x in range(1, modulus) if x % q)


def universal_divisor(k: int, bound: int) -> int:
    """gcd of pᵏ − 1 over primes p > bound.

    By Dirichlet the primes p > bound meet every residue class prime to a
    modulus, so a prime power q^e divides them all iff q ≤ bound (else
    p = q itself fails) and x^k ≡ 1 (mod q^e) for all x prime to q.
    """
    result = 1
    for q in range(2, min(bound, k + 1) + 1):
        if not _is_prime(q):
            continue
        e = 0
        while _exponent_fits(q, e + 1, k):
            e += 1
        result *= q**e
    return result


@question_type(
    "math.prime_power_minus_one_gcd_olympiad",
    display_name={"th": "จำนวนมากสุดที่หาร pᵏ − 1 ทุกจำนวนเฉพาะ p"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class PrimePowerMinusOneGcd(WordProblem):
    def expr(self, rng: Random):
        k = rng.choice([2, 4, 6, 8, 12])
        bound = rng.randint(3, k + 3)
        answer = universal_divisor(k, bound)
        wrong = []
        for value in (
            universal_divisor(k, k + 3),  # forget that p itself may equal a small prime
            universal_divisor(k, 2),
            answer * 2,
            answer // 2 if answer % 2 == 0 else answer * 3,
            universal_divisor(k // 2, bound) if k > 2 else 4 * answer,
            answer * 5,
        ):
            if value != answer and value > 0 and value not in wrong:
                wrong.append(value)
        return MathDraw(
            rf"p^{{{k}}}-1,\quad p>{bound}",
            str(answer),
            prompt=f"จงหาจำนวนเต็มที่มากที่สุดซึ่งหาร p^{k} − 1 ลงตัวสำหรับทุกจำนวนเฉพาะ p ที่มากกว่า {bound}",
            hint="แยกพิจารณากำลังของ 2, 3, 5, … ทีละตัว และอย่าลืมว่าจำนวนเฉพาะที่ไม่เกินขอบเขตอาจเป็น p เองได้",
            distractors=[str(value) for value in wrong],
        )
