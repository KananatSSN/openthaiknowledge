"""Primes p < 60 with (a^(p−1) − 1)/p a perfect square, by exact search."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันที่สอง ข้อ 4",))


BASES = (2, 3, 7, 9, 19, 26, 33, 97)
SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59)


def square_quotient_primes(a: int) -> list[int]:
    """Exact search over p < 60 not dividing a (source: a = 2 gives p = 3, 7;
    there a^((p−1)/2) ± 1 are coprime, which proves no other p works)."""
    out = []
    for p in SMALL_PRIMES:
        if a % p:
            q = (a ** (p - 1) - 1) // p
            if isqrt(q) ** 2 == q:
                out.append(p)
    return out


def listing(primes: list[int]) -> str:
    return r"p\in\{" + ",".join(map(str, primes)) + r"\}"


@question_type(
    "math.fermat_quotient_square_olympiad",
    display_name={"th": "จำนวนเฉพาะที่ทำให้ผลหารแฟร์มาต์เป็นกำลังสองสมบูรณ์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวนเชิงพีชคณิต",
)
class FermatQuotientSquare(WordProblem):
    def expr(self, rng: Random):
        a = rng.choice(BASES)
        sols = square_quotient_primes(a)
        answer = listing(sols)
        others = [p for p in SMALL_PRIMES if p not in sols and a % p]
        extra = sorted(sols + [others[0]])
        swapped = sorted(sols[:-1] + [others[1]])
        divisor = sorted(sols + [p for p in SMALL_PRIMES if a % p == 0][:1]) if a % 2 == 0 or a % 3 == 0 else sorted(sols + [others[2]])
        wrong = [t for t in dict.fromkeys([listing(extra), listing(swapped), listing(divisor), listing(sols[:1] if len(sols) > 1 else [others[1]])]) if t != answer]
        return MathDraw(
            rf"\frac{{{a}^{{p-1}}-1}}{{p}}",
            answer,
            prompt=f"จงหาจำนวนเฉพาะ p < 60 ทั้งหมดที่ไม่หาร {a} และทำให้จำนวนต่อไปนี้เป็นกำลังสองสมบูรณ์",
            hint="แยก a^(p−1) − 1 = (a^((p−1)/2) − 1)(a^((p−1)/2) + 1) ตัวประกอบสองตัวมี ห.ร.ม. หาร 2 แล้วพิจารณาว่า p อยู่ในตัวใด",
            distractors=wrong,
        )
