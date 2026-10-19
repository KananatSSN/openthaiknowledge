"""The smallest m > 0 with the fractional part of m√d in a short window."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 10",)
)


def in_window(m: int, d: int, low_den: int, high_den: int) -> bool:
    """1/low_den < m√d − ⌊m√d⌋ < 1/high_den, decided in integers."""
    k = isqrt(m * m * d)
    over_low = low_den * low_den * m * m * d > (low_den * k + 1) ** 2
    under_high = high_den * high_den * m * m * d < (high_den * k + 1) ** 2
    return over_low and under_high


def first_multiple(d: int, low_den: int, high_den: int) -> int:
    """Pigeonhole on fractional parts guarantees one exists for irrational √d."""
    m = 1
    while not in_window(m, d, low_den, high_den):
        m += 1
    return m


NONSQUARES = tuple(d for d in range(2, 40) if isqrt(d) ** 2 != d)


@question_type(
    "math.irrational_multiple_window_olympiad",
    display_name={"th": "พหุคูณของจำนวนอตรรกยะที่ส่วนเศษตกในช่วงแคบ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ค่าสัมบูรณ์และค่าสุดขีด",
)
class IrrationalMultipleWindow(WordProblem):
    def expr(self, rng: Random):
        d = rng.choice(NONSQUARES)
        high = rng.randint(4, 15)
        low = high + rng.randint(2, 8)
        answer = first_multiple(d, low, high)
        wrong = [v for v in dict.fromkeys([answer + 1, max(answer - 1, 1), 2 * answer, low, high, answer + low]) if v != answer]
        return MathDraw(
            rf"\frac{{1}}{{{low}}}<m\sqrt{{{d}}}+n<\frac{{1}}{{{high}}}",
            str(answer),
            prompt="จงหาจำนวนเต็มบวก m ที่น้อยที่สุดซึ่งมีจำนวนเต็ม n ทำให้อสมการต่อไปนี้เป็นจริง",
            hint="n ต้องเป็น −⌊m√d⌋ จึงต้องการส่วนเศษของ m√d อยู่ในช่วง ตรวจ m = 1, 2, 3, … อย่างเป็นระบบ",
            distractors=[str(v) for v in wrong],
        )
