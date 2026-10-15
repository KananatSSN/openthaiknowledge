"""Locate a cross-pair tangent chord in an isosceles triangle."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2564, ข้อ 1",)
)

_TRIPLES = (
    (3, 4, 5),
    (4, 3, 5),
    (5, 12, 13),
    (12, 5, 13),
    (8, 15, 17),
    (15, 8, 17),
    (7, 24, 25),
    (24, 7, 25),
)


def half_base(leg: int, altitude: int, radius: int) -> int:
    """BM when the opposite contact points' line meets base BC at M."""
    if not (0 < radius < leg and 0 < altitude < leg):
        raise ValueError("expected an interior circle and positive altitude")
    squared = leg * leg - altitude * altitude
    result = isqrt(squared)
    if result * result != squared:
        raise ValueError("the exact variant requires an integral half-base")
    return result


@question_type(
    "math.isosceles_tangent_midpoint_olympiad",
    display_name={"th": "เส้นผ่านจุดสัมผัสตัดฐานสามเหลี่ยมหน้าจั่ว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class IsoscelesTangentMidpoint(WordProblem):
    def expr(self, rng: Random):
        base_half, altitude, leg = rng.choice(_TRIPLES)
        radius = rng.choice(tuple(r for r in range(1, leg) if r != altitude))
        answer = half_base(leg, altitude, radius)
        return MathDraw(
            rf"AB=AC={leg},\quad AH={altitude},\quad r={radius}",
            str(answer),
            prompt=(
                "สามเหลี่ยม ABC เป็นสามเหลี่ยมหน้าจั่ว มี H เป็นเท้าฉากจาก A ลงฐาน BC "
                "วงกลมศูนย์กลาง A รัศมี r อยู่ภายในระยะ AB "
                "เลือกจุดสัมผัส P จาก B และ Q จาก C ให้เส้น PQ ตัด BC ที่ M "
                "จงหาความยาว BM"
            ),
            hint=(
                "ใช้ความสมมาตรของจุดสัมผัสสองคู่เพื่อพิสูจน์ว่า M=H "
                "จากนั้นใช้ทฤษฎีพีทาโกรัสในสามเหลี่ยม ABH"
            ),
            distractors=[
                str(altitude),  # use AH instead of BH
                str(leg),  # use AB instead of BH
                str(2 * base_half),  # return BC instead of BM
                str(base_half + 1),  # shift the midpoint one unit toward C
                str(base_half - 1),  # shift the midpoint one unit toward B
                str(abs(leg - altitude)),  # subtract lengths instead of squaring
            ],
        )
