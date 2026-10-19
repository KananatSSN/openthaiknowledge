"""1 + 1/3 + ⋯ + 1/(2n − 1): the power of 3 in its denominator."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 9",)
)


def three_power(n: int) -> int:
    """Let 3^t ≤ 2n − 1 < 3^{t+1}. The only odd multiple of 3^t up to 2n − 1
    is 3^t itself (2·3^t is even, 3·3^t too big), so 1/3^t is the one term
    with the full power and the denominator has exactly 3^t; for n > 1, t ≥ 1
    and the sum is not an integer."""
    t = 0
    while 3 ** (t + 1) <= 2 * n - 1:
        t += 1
    return t


@question_type(
    "math.odd_harmonic_three_adic_olympiad",
    display_name={"th": "กำลังของ 3 ในตัวส่วนของผลบวกส่วนกลับของจำนวนคี่"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class OddHarmonicThreeAdic(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(5, 5000)
        answer = three_power(n)
        wrong = [v for v in dict.fromkeys([answer + 1, max(answer - 1, 0), three_power(n // 2), answer + 2, 0]) if v != answer]
        return MathDraw(
            rf"\frac{{1}}{{1}}+\frac{{1}}{{3}}+\frac{{1}}{{5}}+\cdots+\frac{{1}}{{{2 * n - 1}}}",
            str(answer),
            prompt="เขียนผลบวกต่อไปนี้เป็นเศษส่วนอย่างต่ำ ตัวส่วนหารด้วย 3^t ลงตัวโดยที่ t มากที่สุดเท่าใด",
            hint="หากำลังสูงสุดของ 3 ที่ไม่เกิน 2n − 1 และแสดงว่ามีพจน์เดียวที่มีกำลังนั้น",
            distractors=[str(v) for v in wrong],
        )
