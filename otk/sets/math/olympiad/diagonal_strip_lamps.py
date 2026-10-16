"""Dominate a one-cell-wide lattice strip with unit-radius lamps."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def minimum_strip_lamps(length: int) -> int:
    """Every diagonal lattice point is needed after off-strip replacements."""
    if length < 1:
        raise ValueError("positive strip length required")
    return length + 1


@question_type(
    "math.diagonal_strip_lamps_olympiad",
    display_name={"th": "เสาไฟบนแถบจุดทแยง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class DiagonalStripLamps(WordProblem):
    def expr(self, rng: Random):
        length = rng.randint(2, 30)
        answer = minimum_strip_lamps(length)
        points = 3 * length + 1
        return MathDraw(
            rf"0\le x,y\le {length},\quad |x-y|\le1",
            str(answer),
            prompt=(
                "ติดเสาไฟที่จุดพิกัดจำนวนเต็มในเงื่อนไขที่กำหนด "
                "เสาแต่ละต้นส่องถึงจุดที่ห่างไม่เกิน 1.01 หน่วย "
                "จงหาจำนวนเสาไฟน้อยสุดที่ทำให้ทุกจุดสว่าง"
            ),
            hint=(
                "จุดนอกแนวทแยงเกิดเป็นคู่ระหว่างจุดทแยงสองจุดติดกัน "
                "ลองแทนเสานอกแนวด้วยเสาบนแนวทแยง"
            ),
            distractors=[
                str(length),  # overlook an endpoint
                str((points + 4) // 5),  # divide by the five-point maximum footprint
                str(2 * length),  # place one lamp on every off-diagonal pair member
                str(points),  # place a lamp at every point
                str(length + 2),  # duplicate an endpoint lamp
            ],
        )
