"""Distinct nonempty clubs where every club with the leader has odd size."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันแรก ข้อ 3",))


def club_maximum(students: int) -> int:
    """Clubs without the leader: any nonempty subset of the other n − 1
    (2^{n−1} − 1); with the leader: the leader plus an even subset (2^{n−2})."""
    return 2 ** (students - 1) - 1 + 2 ** (students - 2)


@question_type(
    "math.odd_club_maximum_olympiad",
    display_name={"th": "จำนวนชมรมมากสุดเมื่อชมรมที่มีหัวหน้ามีสมาชิกเป็นจำนวนคี่"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class OddClubMaximum(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(5, 20)
        answer = club_maximum(n)
        wrong = [v for v in dict.fromkeys([2**n - 1, 2 ** (n - 1), 2 ** (n - 1) + 2 ** (n - 2), 2 ** (n - 1) - 1, 2 ** (n - 1) - 1 + 2 ** (n - 3)]) if v != answer]
        return MathDraw(
            rf"n={n}",
            str(answer),
            prompt=(
                "ห้องเรียนมีนักเรียน n คน หนึ่งในนั้นเป็นหัวหน้าห้อง ต้องการตั้งชมรมที่มีสมาชิกอย่างน้อยหนึ่งคน "
                "สองชมรมใด ๆ มีสมาชิกไม่เหมือนกันทั้งหมด และชมรมที่มีหัวหน้าห้องต้องมีสมาชิกเป็นจำนวนคี่ ตั้งได้มากที่สุดกี่ชมรม"
            ),
            hint="แยกชมรมที่ไม่มีหัวหน้า และชมรมที่มีหัวหน้า (ซึ่งสมาชิกอื่นต้องมีจำนวนคู่)",
            distractors=[str(v) for v in wrong],
        )
