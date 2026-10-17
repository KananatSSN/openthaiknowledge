"""Σ k^(M·2^M) mod 2^M: odd k give 1, even k give 0."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 10",))


def power_sum_residue(last: int, m: int) -> int:
    """Odd k: the unit group mod 2^M has exponent 2^(M − 2), which divides
    M·2^M, so k^E ≡ 1. Even k: k^E is divisible by 2^E ⊇ 2^M. The sum is the
    number of odd k ≤ N (source: N = M = 2005 → 1003)."""
    return (last + 1) // 2 % 2**m


@question_type(
    "math.odd_power_sum_mod_two_power_olympiad",
    display_name={"th": "เศษจากการหารผลบวกกำลังสูงด้วยกำลังของสอง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class OddPowerSumModTwoPower(WordProblem):
    def expr(self, rng: Random):
        m = rng.randint(12, 2005)
        last = rng.randint(m, 3 * m)
        answer = power_sum_residue(last, m)
        wrong = [v for v in dict.fromkeys([last // 2 if last % 2 else last // 2 + 1, last, 0, 1, last - answer]) if v != answer]
        return MathDraw(
            rf"\sum_{{k=1}}^{{{last}}}k^{{{m}\cdot 2^{{{m}}}}}\bmod 2^{{{m}}}",
            str(answer),
            prompt="จงหาเศษเหลือที่ได้จากการหารผลบวกต่อไปนี้ด้วยกำลังของสองที่กำหนด",
            hint="ถ้า k คี่ แล้ว k^(2^(M−2)) ≡ 1 (mod 2^M) ถ้า k คู่ แล้ว k ยกกำลังที่สูงมากหารด้วย 2^M ลงตัว",
            distractors=[str(v) for v in wrong],
        )
