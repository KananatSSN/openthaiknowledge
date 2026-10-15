"""Starting values of an infinite rational quadratic recurrence."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def starting_value_sum(shift: int) -> int:
    """Sum the two possible starts of the shifted rational recurrence.

    Put a_n=b_n-shift. Then a_n=a_(n+1)^2-a_(n+1). If a_(n+1)=u/v
    in lowest terms, the reduced denominator of a_n is v^2. Repeating
    backwards through an infinite rational sequence forces every a_n to
    have denominator 1. Integer successors exist only for nonnegative
    even a_n. Above 2 they strictly decrease, but neither 0 nor 2 has
    an integer predecessor greater than 2, so no infinite path begins
    there. The constant sequences 0 and 2 do exist. Shift them back.
    """
    return 2 * shift + 2


@question_type(
    "math.rational_recurrence_starts_olympiad",
    display_name={"th": "ค่าเริ่มต้นของลำดับตรรกยะไม่สิ้นสุด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ลำดับและอนุกรม",
)
class RationalRecurrenceStarts(WordProblem):
    def expr(self, rng: Random):
        shift = rng.randint(2, 10)
        answer = starting_value_sum(shift)
        return MathDraw(
            rf"b_n=b_{{n+1}}^2-{2 * shift + 1}b_{{n+1}}+{shift * shift + 2 * shift}"
            rf"\qquad(n\ge1)",
            str(answer),
            prompt=("ลำดับ b₁,b₂,… ประกอบด้วยจำนวนตรรกยะทุกพจน์และดำเนินต่อไปได้"
                    "ไม่สิ้นสุด จงหาผลบวกของค่า b₁ ทั้งหมดที่เป็นไปได้"),
            hint=(rf"a_n=b_n-{shift};\quad a_n=a_{{n+1}}^2-a_{{n+1}}.\ "
                  r"\text{พิจารณาตัวส่วนของจำนวนตรรกยะในรูปอย่างต่ำ}"),
            distractors=[
                str(2 * shift + 1),  # take the other fixed root one too low
                str(2 * shift + 3),  # take it one too high
                str(shift + 2),  # report just one possible start
                str(2),  # forget the affine shift
            ],
        )
