"""Count close root pairs forced by reciprocity and six disk sectors."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2564, ข้อ 10",)
)


def sector_pair_lower_bound(degree: int) -> int:
    """Close pairs certified among at least ceil(degree/2) roots in the disk."""
    if degree < 13:
        raise ValueError("the six-sector guarantee starts at degree 13")
    inside = (degree + 1) // 2
    quotient, remainder = divmod(inside, 6)
    return 6 * quotient * (quotient - 1) // 2 + remainder * quotient


@question_type(
    "math.reciprocal_roots_sectors_olympiad",
    display_name={"th": "รากพหุนามสมมาตรกับหลักช่องมุมหกส่วน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามและเศษเหลือ",
)
class ReciprocalRootsSectors(WordProblem):
    def expr(self, rng: Random):
        degree = rng.randint(13, 35)
        inside = (degree + 1) // 2
        answer = sector_pair_lower_bound(degree)
        return MathDraw(
            rf"d={degree},\quad P(z)=\sum_{{j=0}}^d a_jz^j,\quad a_j=a_{{d-j}}",
            str(answer),
            prompt=(
                "พหุนามดีกรี d นี้ไม่มีรากซ้ำและมีสัมประสิทธิ์ต้นไม่เป็นศูนย์ "
                "จับคู่ราก z กับ 1/z แล้วแบ่งจานหน่วยเป็นหกช่องมุมเท่ากัน "
                "วิธีนี้รับประกันรากต่างกันอย่างน้อยกี่คู่ที่มีระยะห่างน้อยกว่า 1"
            ),
            hint=(
                "มีรากในจานหน่วยอย่างน้อย ⌈d/2⌉ ราก "
                "กระจายรากเหล่านี้ในหกช่องให้สมดุลที่สุดเพื่อลดจำนวนคู่ในช่องเดียวกัน"
            ),
            distractors=[
                str(max(0, inside - 6)),  # count only one pair per overflow root
                str(answer + 1),  # overcount one same-sector pair
                str(max(0, answer - 1)),  # miss one forced pair
                str(inside // 6),  # count occupied groups, not pairs
                str(inside),  # count roots instead of root pairs
                str(degree - 6),  # put all roots, including exterior ones, in sectors
            ],
        )
