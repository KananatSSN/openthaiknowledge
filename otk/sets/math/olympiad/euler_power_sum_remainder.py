"""m^{φ(n)+1} + n^{φ(m)+1} ≡ m + n (mod mn) for coprime m, n."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 3",)
)


def totient(n: int) -> int:
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def euler_remainder(m: int, n: int) -> int:
    """Mod m the sum is n·n^{φ(m)} ≡ n, mod n it is m; m + n has both
    residues, so by CRT the remainder is m + n when m + n < mn. For odd m, n
    the sum and m + n are even, so the floor of the quotient is even."""
    return (m + n) % (m * n)


PAIRS = tuple((m, n) for m in range(3, 30) for n in range(m + 1, 40) if gcd(m, n) == 1)


@question_type(
    "math.euler_power_sum_remainder_olympiad",
    display_name={"th": "เศษจากการหารผลบวกกำลังด้วยฟังก์ชันออยเลอร์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class EulerPowerSumRemainder(WordProblem):
    def expr(self, rng: Random):
        m, n = rng.choice(PAIRS)
        answer = euler_remainder(m, n)
        wrong = [v for v in dict.fromkeys([
            2,  # treat both powers as 1
            m * n - (m + n),
            abs(n - m),
            (m + n) // 2,
            m + n + 1,
            m * n - 1,
        ]) if v != answer]
        return MathDraw(
            rf"m={m},\ n={n},\quad m^{{\varphi(n)+1}}+n^{{\varphi(m)+1}}\ \bmod\ mn",
            str(answer),
            prompt="φ คือฟังก์ชันออยเลอร์-ฟี จงหาเศษเหลือจากการหาร m^(φ(n)+1) + n^(φ(m)+1) ด้วย mn",
            hint="ใช้ทฤษฎีบทของออยเลอร์มอดุโล m และมอดุโล n แยกกัน แล้วรวมด้วยทฤษฎีบทเศษเหลือของจีน",
            distractors=[str(v) for v in wrong],
        )
