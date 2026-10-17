"""∏ b^(p_n² − 1) mod a prime m: reduce the exponent sum modulo m − 1."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 11",))


MODULI = (7, 11, 13, 17, 19, 23, 29, 31)


def first_primes(count: int) -> list[int]:
    limit = 30000
    sieve = bytearray([1]) * limit
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(range(i * i, limit, i)))
    return [i for i in range(limit) if sieve[i]][:count]


PRIMES = first_primes(3000)


def product_residue(base: int, last: int, m: int, first: int = 1) -> int:
    """b^(Σ (p_n² − 1)) with the exponent reduced mod m − 1 by Fermat
    (source: b = 2006, n ≤ 2549, m = 13 → 10)."""
    exponent = sum(p * p - 1 for p in PRIMES[first - 1 : last]) % (m - 1)
    return pow(base, exponent, m)


@question_type(
    "math.prime_square_exponent_product_olympiad",
    display_name={"th": "เศษจากผลคูณกำลังที่มีเลขชี้กำลังจากจำนวนเฉพาะ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class PrimeSquareExponentProduct(WordProblem):
    def expr(self, rng: Random):
        m = rng.choice(MODULI)
        while True:
            base = rng.randint(100, 3000)
            if base % m:
                break
        last = rng.randint(10, 3000)
        answer = product_residue(base, last, m)
        wrong = [v for v in dict.fromkeys([product_residue(base, last, m, first=2), product_residue(base, last, m, first=3), pow(base, sum(p * p - 1 for p in PRIMES[:last]) % m, m), 1, base % m]) if v != answer]
        return MathDraw(
            rf"\prod_{{n=1}}^{{{last}}}{base}^{{\,p_n^2-1}}",
            str(answer),
            prompt=f"ให้ p_n เป็นจำนวนเฉพาะตัวที่ n (p₁ = 2) จงหาเศษจากการหารผลคูณต่อไปนี้ด้วย {m}",
            hint=f"รวมเลขชี้กำลังเป็นผลบวกเดียว แล้วลดมอดุโล {m - 1} ด้วยทฤษฎีบทแฟร์มาต์ สำหรับ p > 3 จะได้ p² − 1 หารด้วย 24 ลงตัว",
            distractors=[str(v) for v in wrong],
        )
