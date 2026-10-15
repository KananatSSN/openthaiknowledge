"""Optimize an angle under a line-of-sight dominance condition."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2566, ข้อ 5",)
)

_ANGLES = (100, 110, 120, 130, 140, 150, 160, 170)


def least_foot_angle(theta: int) -> int:
    """Minimum angle PQR in degrees when 90 < theta < 180."""
    if not 90 < theta < 180:
        raise ValueError("theta must be obtuse")
    return 270 - theta


@question_type(
    "math.obtuse_angle_dominance_olympiad",
    display_name={"th": "มุมต่ำสุดจากเงื่อนไขการมองส่วนของเส้นตรง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต",
)
class ObtuseAngleDominance(WordProblem):
    def expr(self, rng: Random):
        theta = rng.choice(_ANGLES)
        answer = least_foot_angle(theta)
        return MathDraw(
            rf"\theta={theta}^\circ",
            rf"{answer}^\circ",
            prompt=(
                "ให้ P เป็นเท้าฉากจาก Q ลงบนเส้นตรงเส้นหนึ่ง และ R อยู่ฝั่งเดียวกับ Q "
                "ของเส้นตรงนั้น ทุกครั้งที่ปลาย A, B บนเส้นตรงมองจาก R เป็นมุม θ "
                "ปลายคู่นั้นต้องมองจาก Q เป็นมุมไม่น้อยกว่า θ "
                "จงหามุม PQR ที่เล็กที่สุดที่เป็นไปได้"
            ),
            hint=(
                "ตั้ง P=(0,0), Q=(0,1) แล้วพิจารณาคู่ A,B ที่เลื่อนไปไกล "
                "ทั้งสองทิศทางบนเส้นตรง เพื่อจำกัดตำแหน่งของ R"
            ),
            distractors=[
                rf"{theta}^\circ",  # assume the sight angle is the target angle
                rf"{180 - theta}^\circ",  # take only its supplement
                rf"{180 - theta // 2}^\circ",  # halve the wrong turning angle
                r"90^\circ",  # ignore the strict line-of-sight constraint
                r"180^\circ",  # use the vertical construction, not the minimum
            ],
        )
