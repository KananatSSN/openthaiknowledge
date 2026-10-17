"""Last three digits of b^(b^k): reduce the exponent modulo λ(1000) = 100 (with care for the factor 8)."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 16",))


def last_three(base: int, k: int) -> int:
    """Computed by a modular power with the full exponent b^k; by hand: the
    residue mod 8 is 0 for even b (large exponent), and mod 125 the exponent
    reduces mod 100 (source: b = 2, k = 2004 → 536)."""
    return pow(base, base**k, 1000)


@question_type(
    "math.power_tower_last_digits_olympiad",
    display_name={"th": "เลขสามหลักสุดท้ายของหอคอยเลขยกกำลัง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class PowerTowerLastDigits(WordProblem):
    def expr(self, rng: Random):
        base, k = rng.choice([2, 3, 7]), rng.randint(10, 3000)
        answer = last_three(base, k)
        wrong = [v for v in dict.fromkeys([pow(base, k, 1000), pow(base, base**k % 100, 1000), pow(base, base**k % 1000, 1000), pow(base, base**k, 100), (answer + 500) % 1000]) if v != answer]
        return MathDraw(
            rf"{base}^{{{base}^{{{k}}}}}",
            f"{answer:03d}",
            prompt="จงหาเลขสามหลักสุดท้ายของจำนวนต่อไปนี้",
            hint="แยก 1000 = 8 · 125 ลดเลขชี้กำลังมอดุโล φ(125) = 100 แล้วรวมด้วยทฤษฎีบทเศษเหลือของจีน",
            distractors=[f"{v:03d}" for v in wrong],
        )
