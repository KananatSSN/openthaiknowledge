"""Σ p_k^(p_k⁴ − 1) modulo M: primes coprime to M contribute 1 each because λ(M) | p⁴ − 1."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 18",))


MODULI = (2550, 510, 1530, 1020, 3060, 4080)


def first_primes(count: int) -> list[int]:
    limit = 30000
    sieve = bytearray([1]) * limit
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(range(i * i, limit, i)))
    return [i for i in range(limit) if sieve[i]][:count]


PRIMES = first_primes(3000)


def tower_sum(last: int, modulus: int, first: int = 2) -> int:
    """Σ_{k=first}^{last} p_k^(p_k⁴ − 1) mod M, term by term with modular
    powers (source: k = 2…2550, M = 2550 gives 1273)."""
    return sum(pow(p, p ** 4 - 1, modulus) for p in PRIMES[first - 1 : last]) % modulus


@question_type(
    "math.prime_power_tower_residue_olympiad",
    display_name={"th": "เศษจากผลบวกกำลังของจำนวนเฉพาะ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class PrimePowerTowerResidue(WordProblem):
    def expr(self, rng: Random):
        modulus = rng.choice(MODULI)
        last = rng.randint(40, 3000)
        answer = tower_sum(last, modulus)
        wrong = [v for v in dict.fromkeys([(last - 1) % modulus, tower_sum(last, modulus, first=1), tower_sum(last - 1, modulus), (answer + 1) % modulus if last % 2 else tower_sum(last + 1, modulus)]) if v != answer]
        return MathDraw(
            rf"\sum_{{k=2}}^{{{last}}}p_k^{{\,p_k^4-1}}",
            str(answer),
            prompt=f"ให้ p_k เป็นจำนวนเฉพาะตัวที่ k (p₁ = 2) จงหาเศษจากการหารผลบวกต่อไปนี้ด้วย {modulus}",
            hint="แยกตัวประกอบมอดุลัส ถ้า p ไม่หารมอดุลัส แล้ว p⁴ − 1 เป็นพหุคูณของ λ ของมอดุลัส พจน์นั้นจึงเหลือเศษ 1 เหลือคิดเฉพาะจำนวนเฉพาะที่หารมอดุลัส",
            distractors=[str(v) for v in wrong],
        )
