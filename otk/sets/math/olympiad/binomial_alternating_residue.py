"""Σ (−1)ᵏ C(2n + 1, 2k + 1)·cᵏ modulo p, via √(−c) in ℤ/p."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันที่สอง ข้อ 4",))


def alternating_sum(n: int, c: int) -> int:
    return sum((-1) ** k * comb(2 * n + 1, 2 * k + 1) * c**k for k in range(n + 1))


def residue(n: int, c: int, p: int) -> int:
    """The sum is ((1 + s)^{2n+1} − (1 − s)^{2n+1})/(2s) with s² = −c. For the
    source (c = 2008, p = 19) s ≡ 5, giving (6^{2n+1} + 4^{2n+1})/10, which is
    0 only if 11^{2n+1} ≡ −1 — impossible since 11 has order 3 mod 19."""
    return alternating_sum(n, c) % p


@question_type(
    "math.binomial_alternating_residue_olympiad",
    display_name={"th": "เศษของผลบวกทวินามสลับเครื่องหมาย"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class BinomialAlternatingResidue(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(1, 12)
        c = rng.choice([2008, 12, 30, 45, 7, 20])
        p = rng.choice([19, 13, 17, 23])
        answer = residue(n, c, p)
        wrong = [v for v in dict.fromkeys([(answer + 1) % p, (p - answer) % p, (2 * n + 1) % p, 0 if answer else 1, (answer + 3) % p]) if v != answer]
        return MathDraw(
            rf"\sum_{{k=0}}^{{{n}}}(-1)^k\binom{{{2 * n + 1}}}{{2k+1}}{c}^k\ \bmod\ {p}",
            str(answer),
            prompt="จงหาเศษเหลือจากการหารผลบวกต่อไปนี้ด้วยจำนวนเฉพาะที่กำหนด",
            hint="เขียนผลบวกเป็น ((1 + s)^(2n+1) − (1 − s)^(2n+1))/(2s) เมื่อ s² = −c แล้วคำนวณในมอดุโล p",
            distractors=[str(v) for v in wrong],
        )
