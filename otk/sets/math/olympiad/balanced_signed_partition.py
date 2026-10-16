"""Count sizes admitting a zero-sum half of a signed symmetric set."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def balanced_sizes_sum(limit: int) -> int:
    """For 1 <= n <= limit, exactly n = 2, ..., limit are feasible."""
    if limit < 1:
        raise ValueError("limit must be positive")
    return limit * (limit + 1) // 2 - 1


@question_type(
    "math.balanced_signed_partition_olympiad",
    display_name={"th": "แบ่งจำนวนบวกและลบให้ผลรวมศูนย์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class BalancedSignedPartition(WordProblem):
    def expr(self, rng: Random):
        limit = rng.randint(4, 20)
        answer = balanced_sizes_sum(limit)
        return MathDraw(
            rf"1\le n\le {limit}",
            str(answer),
            prompt=(
                "นำจำนวนเต็มที่ไม่เป็นศูนย์ตั้งแต่ −n ถึง n มาเลือก n จำนวน "
                "โดยให้ผลรวมของจำนวนที่เลือกเท่ากับศูนย์ "
                "จงหาผลบวกของค่า n ทั้งหมดในช่วงที่กำหนดซึ่งทำได้"
            ),
            hint="พิจารณา n=1 แล้วสร้างชุดที่สมดุลแยกกรณี n คู่และ n คี่",
            distractors=[
                str(answer + 1),  # mistakenly include n=1
                str(answer - limit),  # omit the largest feasible n
                str(limit - 1),  # count feasible n rather than sum them
                str(answer - 2),  # mistakenly exclude n=2
            ],
        )
