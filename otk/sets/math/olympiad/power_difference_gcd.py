"""gcd(a^m − 1, a^n − 1) = a^gcd(m, n) − 1, by the Euclidean algorithm on exponents."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 14",))


def power_gcd(a: int, m: int, n: int) -> int:
    """a^m − 1 ≡ a^(m − n) − 1 (mod a^n − 1), so the exponents follow the
    Euclidean algorithm (source: 5, 2547, 2004 → 5³ − 1 = 124)."""
    return a ** gcd(m, n) - 1


@question_type(
    "math.power_difference_gcd_olympiad",
    display_name={"th": "ห.ร.ม. ของ a^m − 1 กับ a^n − 1"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class PowerDifferenceGcd(WordProblem):
    def expr(self, rng: Random):
        while True:
            a = rng.randint(2, 9)
            m, n = rng.randint(100, 3000), rng.randint(100, 3000)
            g = gcd(m, n)
            if m != n and 2 <= g <= 6:
                break
        answer = power_gcd(a, m, n)
        wrong = [v for v in dict.fromkeys([a - 1, a ** (2 * g) - 1, a**g, a**g + 1, g]) if v != answer]
        return MathDraw(
            rf"\gcd({a}^{{{m}}}-1,\ {a}^{{{n}}}-1)",
            str(answer),
            prompt="จงหา ห.ร.ม. ต่อไปนี้",
            hint="a^m − 1 ≡ a^(m−n) − 1 (mod a^n − 1) เลขชี้กำลังจึงลดลงแบบขั้นตอนวิธีของยุคลิด",
            distractors=[str(v) for v in wrong],
        )
