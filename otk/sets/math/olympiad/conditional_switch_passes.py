"""Count switches after conditional passes over numbered positions."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def switches_on(
    total: int,
    first_divisor: int,
    second_divisor: int,
    third_divisor: int,
    *,
    skip_first: bool = False,
    skip_last: bool = False,
    toggle_middle: bool = False,
    toggle_last: bool = False,
) -> int:
    """Apply off/on/off passes; optional variants represent named mistakes."""
    if total < 2 or total % 2 or min(first_divisor, second_divisor, third_divisor) < 2:
        raise ValueError("expected an even switch count and divisors above one")
    on = [False] + [number <= total // 2 for number in range(1, total + 1)]
    for number in range(first_divisor, total + 1, first_divisor):
        if not skip_first:
            on[number] = False
    for number in range(second_divisor, total + 1, second_divisor):
        on[number] = not on[number] if toggle_middle else True
    for number in range(third_divisor, total + 1, third_divisor):
        if not skip_last:
            on[number] = not on[number] if toggle_last else False
    return sum(on)


@question_type(
    "math.conditional_switch_passes_olympiad",
    display_name={"th": "นับสวิตช์หลังคำสั่งเปิดปิดตามตัวหาร"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class ConditionalSwitchPasses(WordProblem):
    def expr(self, rng: Random):
        total = 2 * rng.randint(40, 160)
        first, second, third = rng.sample(range(2, 8), 3)
        answer = switches_on(total, first, second, third)
        return MathDraw(
            rf"N={total},\quad a={first},\quad b={second},\quad c={third}",
            str(answer),
            prompt=("มีสวิตช์หมายเลข 1 ถึง N โดยครึ่งแรกเปิดและครึ่งหลังปิด เริ่มจากปิดสวิตช์หมายเลขที่หารด้วย a ลงตัว "
                    "เฉพาะตัวที่เปิดอยู่ จากนั้นเปิดสวิตช์หมายเลขที่หารด้วย b ลงตัวเฉพาะตัวที่ปิดอยู่ "
                    "และปิดสวิตช์หมายเลขที่หารด้วย c ลงตัวเฉพาะตัวที่เปิดอยู่ สุดท้ายมีสวิตช์เปิดกี่ตัว"),
            hint="นับเซตของสวิตช์ที่เปิดหลังแต่ละรอบ โดยแยกครึ่งแรกและครึ่งหลัง",
            distractors=[
                str(switches_on(total, first, second, third, skip_first=True)),  # omit first pass
                str(switches_on(total, first, second, third, skip_last=True)),  # omit last pass
                str(switches_on(total, first, second, third, toggle_middle=True)),  # toggle rather than open
                str(switches_on(total, first, second, third, toggle_last=True)),  # toggle rather than close
            ],
        )
