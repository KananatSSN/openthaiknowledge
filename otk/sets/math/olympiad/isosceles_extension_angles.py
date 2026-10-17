"""Angles after extending the leg of an isosceles triangle by its base."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2557, ข้อ 1",)
)

ASKED = ("BEC", "ACE", "CBE")


def extension_angle(asked: str, apex: int) -> int:
    """AB = AC with ∠BAC = apex, and E beyond B on ray AB with BE = BC.

    ∠CBE = 180° − ∠ABC = 90° + apex/2; triangle BCE is isosceles, so
    ∠BEC = ∠BCE = 45° − apex/4, and ∠ACE = ∠ACB + ∠BCE = 135° − 3·apex/4.
    """
    if apex % 4 or not 0 < apex < 180:
        raise ValueError("apex must be a multiple of 4 below 180")
    if asked == "BEC":
        return 45 - apex // 4
    if asked == "ACE":
        return 135 - 3 * apex // 4
    if asked == "CBE":
        return 90 + apex // 2
    raise ValueError(asked)


@question_type(
    "math.isosceles_extension_angles_olympiad",
    display_name={"th": "มุมจากการต่อด้านของสามเหลี่ยมหน้าจั่วยาวเท่าฐาน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สามเหลี่ยม",
)
class IsoscelesExtensionAngles(WordProblem):
    def expr(self, rng: Random):
        apex = rng.randrange(20, 141, 4)
        asked = rng.choice(ASKED)
        answer = extension_angle(asked, apex)
        base = 90 - apex // 2
        candidates = {
            "BEC": [base // 2, base, 90 - apex // 4, 45 + apex // 4, apex // 4],
            "ACE": [base, 135 - apex // 4, 90 - apex // 4, 180 - 3 * apex // 4, 45 + apex // 4],
            "CBE": [base, 180 - apex, 90 - apex // 2 + 45, 90 + apex // 4, 180 - apex // 2],
        }[asked]
        wrong = []
        for value in candidates:
            if 0 < value < 180 and value != answer and value not in wrong:
                wrong.append(value)
        return MathDraw(
            rf"AB=AC,\quad \angle BAC={apex}^\circ,\quad BE=BC",
            rf"{answer}^\circ",
            prompt=(
                "รูปสามเหลี่ยมหน้าจั่ว ABC มี AB = AC ต่อด้าน AB ออกไปทาง B ถึงจุด E "
                f"โดย BE = BC จงหาขนาดของมุม {asked}"
            ),
            hint="∠CBE เป็นมุมภายนอกของ ∠ABC และรูปสามเหลี่ยม BCE เป็นรูปหน้าจั่ว",
            distractors=[rf"{value}^\circ" for value in wrong],
            variant=asked,
        )
