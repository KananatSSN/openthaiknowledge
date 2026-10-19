"""Primes p with p | C(N, p) + c: by Lucas, C(N, p) ≡ ⌊N/p⌋ (mod p)."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันแรก ข้อ 10",)
)


def _primes(limit: int) -> list[int]:
    return [p for p in range(2, limit + 1) if all(p % d for d in range(2, int(p**0.5) + 1))]


def binomial_primes(n: int, c: int) -> list[int]:
    """For p > N the binomial is 0, so p | c ≤ N anyway; otherwise test it."""
    return [p for p in _primes(max(n, c)) if (comb(n, p) + c) % p == 0]


@question_type(
    "math.binomial_prime_lucas_olympiad",
    display_name={"th": "จำนวนเฉพาะ p ที่หาร C(N, p) + c ลงตัว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class BinomialPrimeLucas(WordProblem):
    def expr(self, rng: Random):
        while True:
            n = rng.randint(30, 200)
            c = rng.randint(1, 20)
            found = binomial_primes(n, c)
            if found:
                break
        answer = sum(found)
        wrong = [v for v in dict.fromkeys([
            sum(p for p in _primes(c) if c % p == 0),  # only the primes dividing c
            answer + 2, answer + 5, max(found), answer - 1,
        ]) if v != answer and v > 0]
        return MathDraw(
            rf"\binom{{{n}}}{{p}}+{c}",
            str(answer),
            prompt="จงหาผลบวกของจำนวนเฉพาะ p ทั้งหมดที่หารนิพจน์ต่อไปนี้ลงตัว",
            hint="ทฤษฎีบทของลูคัส: C(N, p) ≡ ⌊N/p⌋ (mod p) จึงต้องการ p | ⌊N/p⌋ + c",
            distractors=[str(v) for v in wrong],
        )
