"""Arc AC is a third of the circle: AC = R√3 and OD = R√3/2, so AC = 2(AC − OD)."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 1",))


def chord_length(difference: int) -> int:
    """With OA on the x-axis and OB on the y-axis, C sits 120° from A, so
    AC = R√3 and the foot D of C on OB has OD = R√3/2: AC − OD = AC/2."""
    return 2 * difference


@question_type(
    "math.chord_arc_projection_olympiad",
    display_name={"th": "ความยาวคอร์ดจากส่วนโค้งหนึ่งในสามของวงกลม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class ChordArcProjection(WordProblem):
    def expr(self, rng: Random):
        difference = rng.randint(1, 30)
        answer = chord_length(difference)
        wrong = [v for v in dict.fromkeys([difference, 3 * difference, 4 * difference, 2 * difference + 2, difference + 2]) if v != answer]
        return MathDraw(
            rf"AC-OD={difference}",
            str(answer),
            prompt="ในวงกลมจุดศูนย์กลาง O รัศมี OA ตั้งฉากกับรัศมี OB คอร์ด AC ตัด OB และส่วนโค้ง AC ยาวหนึ่งในสามของเส้นรอบวง CD ตั้งฉากกับ OB ที่ D จงหา AC",
            hint="ส่วนโค้ง AC รองรับมุมที่จุดศูนย์กลาง 120° หา AC และ OD ในรูปของรัศมี",
            distractors=[str(v) for v in wrong],
        )
