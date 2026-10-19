"""p^(q−1) + q^(p−1) + (p − 1)!(q − 1)! modulo pq for twin primes q = p + 2."""

from __future__ import annotations

from math import factorial
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 13",))


PAIRS = ((11, 13), (17, 19), (29, 31), (41, 43), (59, 61), (71, 73), (101, 103), (107, 109), (137, 139), (149, 151), (179, 181), (191, 193), (197, 199))


def residue(p: int, q: int) -> int:
    """Mod p: 0 + 1 + 0 = 1. Mod q: 1 + 0 + (p − 1)!·(−1), and
    (q − 1)! = (q − 1)(q − 2)(p − 1)! gives (p − 1)! ≡ −1/2, so the total is
    3/2 (source: 29, 31 → 668). Computed directly here."""
    n = p * q
    return (pow(p, q - 1, n) + pow(q, p - 1, n) + factorial(p - 1) * factorial(q - 1)) % n


@question_type(
    "math.twin_prime_factorial_residue_olympiad",
    display_name={"th": "เศษจากการหารด้วยผลคูณจำนวนเฉพาะแฝด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class TwinPrimeFactorialResidue(WordProblem):
    def expr(self, rng: Random):
        p, q = rng.choice(PAIRS)
        answer = residue(p, q)
        n = p * q
        half = pow(2, -1, q)

        def crt(rp: int, rq: int) -> int:
            return next(x for x in range(rq, n, q) if x % p == rp)

        wrong = [v for v in dict.fromkeys([crt(1, (1 - half) % q), crt(1, 2), crt(2, (1 + half) % q), crt(1, 1), (pow(p, q - 1, n) + pow(q, p - 1, n)) % n]) if v != answer]
        return MathDraw(
            rf"{p}^{{{q - 1}}}+{q}^{{{p - 1}}}+{p - 1}!\,({q - 1}!)",
            str(answer),
            prompt=f"จงหาเศษที่เกิดจากการหารจำนวนต่อไปนี้ด้วย {p}·{q}",
            hint=f"คิดมอดุโล {p} และ {q} แยกกัน ใช้ทฤษฎีบทแฟร์มาต์และวิลสัน ({q - 1}! = {q - 1}·{q - 2}·{p - 1}!) แล้วรวมด้วยทฤษฎีบทเศษเหลือของจีน",
            distractors=[str(v) for v in wrong],
        )
