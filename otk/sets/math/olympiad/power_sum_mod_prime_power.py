"""Σ k^E mod M over k ≤ N, reduced through the period M of k ↦ k^E mod M."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 17",))


MODULI = (25, 27, 49, 125, 16, 32, 9)


def power_sum(last: int, e: int, modulus: int) -> int:
    """k^E mod M depends only on k mod M, so sum one period and the tail
    (source: N = E = 2547, M = 25 → 4)."""
    period = sum(pow(k, e, modulus) for k in range(1, modulus + 1))
    tail = sum(pow(k, e, modulus) for k in range(1, last % modulus + 1))
    return (last // modulus * period + tail) % modulus


@question_type(
    "math.power_sum_mod_prime_power_olympiad",
    display_name={"th": "เศษจากการหารผลบวกกำลังด้วยกำลังของจำนวนเฉพาะ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class PowerSumModPrimePower(WordProblem):
    def expr(self, rng: Random):
        modulus = rng.choice(MODULI)
        e, last = rng.randint(100, 3000), rng.randint(100, 3000)
        answer = power_sum(last, e, modulus)
        wrong = [v for v in dict.fromkeys([last * (last + 1) // 2 % modulus, last % modulus, power_sum(last - 1, e, modulus), power_sum(last, e % modulus, modulus), (answer + 1) % modulus]) if v != answer]
        return MathDraw(
            rf"1^{{{e}}}+2^{{{e}}}+3^{{{e}}}+\cdots+{last}^{{{e}}}",
            str(answer),
            prompt=f"จงหาเศษเหลือจากการหารผลบวกต่อไปนี้ด้วย {modulus}",
            hint=f"k^E มอดุโล {modulus} ขึ้นกับ k มอดุโล {modulus} เท่านั้น หาผลบวกหนึ่งคาบ แล้วรวมกับส่วนที่เหลือ",
            distractors=[str(v) for v in wrong],
        )
