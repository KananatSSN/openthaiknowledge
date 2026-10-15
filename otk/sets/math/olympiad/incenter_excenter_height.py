"""Compare incenter and opposite-A excenter heights in a reflected triangle."""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")

_TRIPLES = (
    (12, 9, 5),
    (12, 16, 9),
    (15, 20, 8),
    (15, 36, 20),
    (16, 30, 12),
    (20, 21, 15),
    (21, 28, 20),
    (24, 18, 10),
    (24, 32, 18),
    (28, 45, 21),
    (30, 40, 16),
    (33, 56, 44),
)


def _sides(a: int, d: int, c: int) -> tuple[int, int]:
    if not (a > d > 0 and c > 0):
        raise ValueError("expected AB > BD > 0 and BC > 0")
    ac = isqrt(a * a + c * c)
    cd = isqrt(d * d + c * c)
    if ac * ac != a * a + c * c or cd * cd != d * d + c * c:
        raise ValueError("this exact solver requires integer hypotenuses")
    return ac, cd


def excenter_height(a: int, d: int, c: int) -> Fraction:
    """Distance from the A-excenter of ACD to the line AB."""
    ac, cd = _sides(a, d, c)
    return Fraction(c * (ac + cd), ac + cd + a + d)


@question_type(
    "math.incenter_excenter_height_olympiad",
    display_name={"th": "ความสูงของจุดศูนย์กลางวงกลมแนบนอก"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมแนบใน",
)
class IncenterExcenterHeight(WordProblem):
    def expr(self, rng: Random):
        c, a, d = rng.choice(_TRIPLES)
        ac, cd = _sides(a, d, c)
        answer = excenter_height(a, d, c)
        incenter = Fraction(c * (a + d), ac + cd + a + d)
        wrong_gap = Fraction(c * (a - d), ac + cd + a + d)
        wrong_denominator = Fraction(c * (ac + cd), ac + cd + a - d)
        return MathDraw(
            rf"AB={a},\quad BD={d},\quad BC={c}",
            str(answer),
            prompt=(
                "สามเหลี่ยม ABC มีมุม B เป็นมุมฉาก จุด D อยู่ภายใน AB และ E อยู่บน "
                "เส้นตรง AB โดย B เป็นจุดกึ่งกลาง DE ให้ I เป็นจุดศูนย์กลางวงกลมแนบใน "
                "ACE และ J เป็นจุดศูนย์กลางวงกลมแนบนอก ACD ฝั่งตรงข้าม A "
                "จงหาระยะจาก J ถึงเส้นตรง AB"
            ),
            hint="ใช้สูตรพิกัดจุดศูนย์กลางวงกลมแนบใน แล้วสังเกตว่าความสูงของ I และ J รวมกันเป็น BC",
            distractors=[
                str(incenter),  # swap the two centers
                str(Fraction(c, 2)),  # assume both centers have equal height
                str(wrong_gap),  # use AD in place of AE
                str(wrong_denominator),  # use AD in place of AE in the denominator
                str(c),  # put the excenter at C's height
                str(answer + 1),  # shift the exact perpendicular distance
            ],
        )
