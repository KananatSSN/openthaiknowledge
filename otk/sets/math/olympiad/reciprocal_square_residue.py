"""Σ 1/k² modulo a prime p; the half sum up to (p − 1)/2 vanishes for p ≥ 5."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันแรก ข้อ 10",))

PRIMES = (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)


def reciprocal_square_residue(p: int, m: int) -> int:
    """Σ_{k ≤ m} k⁻² mod p. For m = p − 1 it is Σk² ≡ 0 (p ≥ 5); k and p − k
    have equal squares, so the half sum is 0 too, which is the source's
    p | a for Σ 1/(2k)² = (1/4)Σ 1/k²."""
    return sum(pow(k * k, -1, p) for k in range(1, m + 1)) % p


@question_type(
    "math.reciprocal_square_residue_olympiad",
    display_name={"th": "ผลบวกส่วนกลับของกำลังสองมอดุโลจำนวนเฉพาะ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class ReciprocalSquareResidue(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(PRIMES)
        m = rng.randint(2, p - 2)
        answer = reciprocal_square_residue(p, m)
        wrong = [v for v in dict.fromkeys([(answer + 1) % p, (p - answer) % p, sum(k * k for k in range(1, m + 1)) % p, m % p, (answer + 2) % p]) if v != answer]
        return MathDraw(
            rf"p={p},\quad \frac{{1}}{{1^2}}+\frac{{1}}{{2^2}}+\cdots+\frac{{1}}{{{m}^2}}=\frac{{a}}{{b}}",
            str(answer),
            prompt="เขียนผลบวกเป็นเศษส่วนอย่างต่ำ a/b (p ไม่หาร b) จงหาเศษเหลือของ a·b⁻¹ มอดุโล p ซึ่งอยู่ใน 0, 1, …, p − 1",
            hint="ทำงานในมอดุโล p: แทน 1/k² ด้วยตัวผกผันของ k² แล้วบวกกัน",
            distractors=[str(v) for v in wrong],
        )
