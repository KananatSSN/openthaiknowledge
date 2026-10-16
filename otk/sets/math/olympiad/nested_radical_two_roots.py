"""Find the first parameter giving two roots in a nested-radical equation."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def first_two_root_parameter(offset: int, inner_root: int) -> int:
    """Minimum positive a for x+2√(x+m(m+2)-a√(x-b))-a√(x-b)=0."""
    if offset < 0 or inner_root < 1:
        raise ValueError("expected nonnegative offset and positive inner root")
    constant = offset + 2 * inner_root
    return isqrt(4 * constant) + 1


@question_type(
    "math.nested_radical_two_roots_olympiad",
    display_name={"th": "ค่าพารามิเตอร์ต่ำสุดที่สมการรากซ้อนมีสองคำตอบ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการและอสมการ",
)
class NestedRadicalTwoRoots(WordProblem):
    def expr(self, rng: Random):
        offset = rng.randint(4, 15)
        inner_root = rng.randint(1, 4)
        shift = inner_root * (inner_root + 2)
        answer = first_two_root_parameter(offset, inner_root)
        constant = offset + 2 * inner_root
        mistaken = [
            answer - 1,  # count a repeated root twice
            isqrt(constant) + 1,  # forget factor four in the discriminant
            answer + 1,  # skip the first allowable integer
            constant,  # confuse the quadratic constant with the parameter
        ]
        distractors = [str(value) for value in dict.fromkeys(mistaken) if value != answer]
        return MathDraw(
            rf"x+2\sqrt{{x+{shift}-a\sqrt{{x-{offset}}}}}-a\sqrt{{x-{offset}}}=0",
            str(answer),
            prompt="จงหาจำนวนเต็มบวก a ที่น้อยที่สุดซึ่งทำให้สมการมีคำตอบจริงที่แตกต่างกันสองคำตอบ",
            hint="ให้ t=√(x-b) และ y เป็นรากชั้นนอก แล้วใช้สมการที่ y ต้องเป็นราก",
            distractors=distractors,
        )
