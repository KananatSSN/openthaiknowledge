"""A vector identity among opposite-side midpoint chords of a hexagon."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def opposite_midpoint_chord_square(ux: int, wz: int, angle: int) -> int:
    """Return VY squared from directed UX + WZ = VY."""
    if ux <= 0 or wz <= 0 or angle not in (60, 120):
        raise ValueError("positive lengths and a 60 or 120 degree angle required")
    return ux * ux + wz * wz + (ux * wz if angle == 60 else -ux * wz)


@question_type(
    "math.opposite_midpoint_chord_square_olympiad",
    display_name={"th": "เวกเตอร์ระหว่างจุดกึ่งกลางด้านตรงข้าม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="รูปหลายเหลี่ยม",
)
class OppositeMidpointChordSquare(WordProblem):
    def expr(self, rng: Random):
        ux, wz = rng.sample(range(3, 17), 2)
        angle = rng.choice((60, 120))
        answer = opposite_midpoint_chord_square(ux, wz, angle)
        sign = 1 if angle == 60 else -1
        return MathDraw(
            rf"UX={ux},\quad WZ={wz},\quad \theta={angle}^\circ",
            str(answer),
            prompt=(
                "หกเหลี่ยมนูน ABCDEF มี U,V,W,X,Y,Z เป็นจุดกึ่งกลางของด้าน "
                "AB,BC,CD,DE,EF,FA ตามลำดับ "
                "มุมระหว่างเวกเตอร์ UX และ WZ เท่ากับ θ จงหา VY²"
            ),
            hint="เขียนเวกเตอร์จากพิกัดจุดกึ่งกลางก่อนใช้กฎโคไซน์",
            distractors=[
                str(ux * ux + wz * wz),  # ignore the included angle
                str(ux * ux + wz * wz - sign * ux * wz),  # reverse the cosine sign
                str((ux + wz) ** 2),  # assume parallel, same direction
                str((ux - wz) ** 2),  # assume parallel, opposite directions
                str(ux * ux + wz * wz + 2 * sign * ux * wz),  # omit cos 60 factor
            ],
        )
