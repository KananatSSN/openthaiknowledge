"""With AB ∥ CD, the bisector of ∠ACD meets ray BA at K with AK = AC."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันที่สอง ข้อ 3",))


def bisector_distance(ab: int, ac: int) -> int:
    """∠AKC = ∠KCD (alternate angles, AB ∥ CD) = ∠ACK, so AK = AC and K lies
    beyond A on ray BA: BK = AB + AC."""
    return ab + ac


@question_type(
    "math.trapezoid_bisector_point_olympiad",
    display_name={"th": "จุดที่เส้นแบ่งครึ่งมุมตัดรังสีในรูปสี่เหลี่ยมคางหมู"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: สี่เหลี่ยมคางหมู",
)
class TrapezoidBisectorPoint(WordProblem):
    def expr(self, rng: Random):
        ab = rng.randint(3, 30)
        ac = rng.randint(3, 30)
        answer = bisector_distance(ab, ac)
        wrong = [v for v in dict.fromkeys([abs(ab - ac), ab, ac, 2 * ac, ab + 2 * ac, answer + 1]) if v != answer and v > 0]
        return MathDraw(
            rf"AB={ab},\quad AC={ac},\quad AB\parallel CD",
            str(answer),
            prompt="ABCD เป็นรูปสี่เหลี่ยมนูนที่ AB ∥ CD เส้นแบ่งครึ่งมุม ACD ตัดรังสี BA ที่ K จงหา BK",
            hint="ใช้มุมแย้งระหว่างเส้นขนาน: ∠AKC = ∠KCD = ∠ACK จึงรูปสามเหลี่ยม AKC เป็นหน้าจั่ว",
            distractors=[str(v) for v in wrong],
        )
