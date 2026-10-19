"""10 | a³b − ab³ = ab(a − b)(a + b): always even, and divisible by 5 when 5 | ab or a² ≡ b² (mod 5)."""

from __future__ import annotations

from itertools import combinations
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันที่สอง ข้อ 2",))


def good_pairs(values: list[int]) -> int:
    """a³b − ab³ = ab(a − b)(a + b) is always even (a, b same parity or one
    even). Nonzero squares mod 5 are 1, 4, so among any three integers two
    have 5 | ab or a² ≡ b² — the source's claim. Counted directly here."""
    return sum(1 for a, b in combinations(values, 2) if (a**3 * b - a * b**3) % 10 == 0)


@question_type(
    "math.quartic_difference_pairs_olympiad",
    display_name={"th": "จำนวนคู่ที่ทำให้ 10 หาร a³b − ab³"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การหารลงตัวและเศษเหลือ",
)
class QuarticDifferencePairs(WordProblem):
    def expr(self, rng: Random):
        values = sorted(rng.sample(range(-60, 61), rng.randint(5, 7)))
        answer = good_pairs(values)
        pairs = list(combinations(values, 2))
        square_only = sum(1 for a, b in pairs if (a * a - b * b) % 5 == 0)
        zero_only = sum(1 for a, b in pairs if a * b % 5 == 0)
        wrong = [v for v in dict.fromkeys([square_only, zero_only, len(pairs), sum(1 for a, b in pairs if (a - b) % 10 == 0), len(pairs) - answer]) if v != answer]
        listing = ", ".join(map(str, values))
        return MathDraw(
            rf"S=\{{{listing}\}}",
            str(answer),
            prompt="จงหาจำนวนคู่ {a, b} ของสมาชิกที่ต่างกันใน S (ไม่สนใจลำดับ) ซึ่ง 10 หาร a³b − ab³",
            hint="แยก a³b − ab³ = ab(a − b)(a + b) ซึ่งเป็นจำนวนคู่เสมอ จึงต้องการเพียงให้ 5 หาร: 5 | a, 5 | b หรือ a² ≡ b² (mod 5)",
            distractors=[str(v) for v in wrong],
        )
