"""Reduce paired fifth-power numerators modulo a sum of squares."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def fifth_power_pair_remainders(m: int, n: int) -> tuple[int, int]:
    """Use m²=-n² modulo m²+n² to avoid fifth powers."""
    if m <= 0 or n <= 0:
        raise ValueError("positive integers required")
    modulus = m * m + n * n
    return (
        n * (1 + m * n**3) % modulus,
        m * (1 + n * m**3) % modulus,
    )


def _pair(first: int, second: int) -> str:
    return f"({first}, {second})"


@question_type(
    "math.fifth_power_pair_remainders_olympiad",
    display_name={"th": "เศษเหลือคู่ของกำลังห้าและผลบวกกำลังสอง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class FifthPowerPairRemainders(WordProblem):
    def expr(self, rng: Random):
        while True:
            m, n = rng.sample(range(2, 31), 2)
            if gcd(m, n) == 1:
                break
        modulus = m * m + n * n
        first, second = fifth_power_pair_remainders(m, n)
        return MathDraw(
            rf"m={m},\quad n={n}",
            _pair(first, second),
            prompt=(
                "ให้ D=m²+n² จงหาเศษเหลือเรียงลำดับของ m⁵+n และ n⁵+m "
                "เมื่อหารด้วย D"
            ),
            hint="ใช้ m² ≡ −n² (mod D) เพื่อลดเลขชี้กำลังก่อนหาร",
            distractors=[
                _pair(second, first),  # reverse the ordered pair
                _pair((m**3 + n) % modulus, (n**3 + m) % modulus),  # use cubes
                _pair(m**5 % modulus, n**5 % modulus),  # omit linear terms
                _pair((m**5 + n) % (m + n), (n**5 + m) % (m + n)),  # wrong modulus
            ],
        )
