"""Construct consecutive non-perfect-powers using exact prime valuations."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def nonpower_block_start(primes: tuple[int, ...]) -> int:
    """Least N >= 0 with N+i congruent to p_i modulo p_i squared."""
    if not primes or len(set(primes)) != len(primes):
        raise ValueError("distinct primes required")
    modulus = 1
    residue = 0
    for i, prime in enumerate(primes, 1):
        if prime < 2 or any(prime % divisor == 0 for divisor in range(2, prime)):
            raise ValueError("primes required")
        next_modulus = prime * prime
        target = (prime - i) % next_modulus
        step = ((target - residue) * pow(modulus, -1, next_modulus)) % next_modulus
        residue += modulus * step
        modulus *= next_modulus
    return residue


@question_type(
    "math.consecutive_nonpowers_crt_olympiad",
    display_name={"th": "สร้างจำนวนติดกันที่ไม่เป็นกำลังสมบูรณ์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class ConsecutiveNonpowersCRT(WordProblem):
    def expr(self, rng: Random):
        count = rng.choice((2, 3))
        primes = tuple(rng.sample((2, 3, 5, 7), count))
        answer = nonpower_block_start(primes)
        moduli = [p * p for p in primes]
        product = 1
        for modulus in moduli:
            product *= modulus
        return MathDraw(
            ", ".join(rf"p_{i}={prime}" for i, prime in enumerate(primes, 1)),
            str(answer),
            prompt=(
                "กำหนดจำนวนเฉพาะต่างกัน p₁,…,pₖ ตามลำดับ จงหา N จำนวนเต็มไม่ลบที่น้อยที่สุด "
                "ซึ่ง N+i ≡ pᵢ (mod pᵢ²) สำหรับทุก i=1,…,k"
            ),
            hint="ใช้ทฤษฎีบทเศษเหลือจีนกับมอดูลัส pᵢ² ที่เป็นจำนวนเฉพาะสัมพัทธ์กัน",
            distractors=[
                str(answer + product),  # find a solution but ignore least
                str(answer + moduli[0]),  # satisfy first congruence only
                str(answer + moduli[1]),  # satisfy second congruence only
                str(answer + 1),  # shift residue by one
            ],
        )
