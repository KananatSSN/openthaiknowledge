"""Locate the maximum of a set closed under an LCM quotient."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2564, ข้อ 9",)
)


def largest_lcm_difference_member(index: int, pronic_minimum: bool) -> int:
    """Maximum when the minimum is n² or n(n+1), respectively."""
    if index < 2:
        raise ValueError("index must be at least 2")
    return (index + 1) ** 2 if pronic_minimum else index * (index + 1)


@question_type(
    "math.lcm_difference_set_olympiad",
    display_name={"th": "สมาชิกมากสุดของเซตปิดภายใต้ผลหาร ค.ร.น."},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class LcmDifferenceSet(WordProblem):
    def expr(self, rng: Random):
        index = rng.randint(2, 16)
        pronic_minimum = bool(rng.randrange(2))
        minimum = index * (index + 1) if pronic_minimum else index * index
        gap = index + int(pronic_minimum)
        answer = largest_lcm_difference_member(index, pronic_minimum)
        return MathDraw(
            rf"\min S={minimum}",
            str(answer),
            prompt=(
                "ให้ S เป็นเซตจำนวนเต็มบวกที่มีสมาชิกอย่างน้อยสองตัว "
                "สำหรับทุก a<b ใน S ผลต่าง b−a หาร ค.ร.น.(a,b) ลงตัว "
                "และ ค.ร.น.(a,b)/(b−a) อยู่ใน S จงหาสมาชิกมากสุดของ S"
            ),
            hint=(
                "เขียน a=gu, b=gv โดย g=ห.ร.ม.(a,b) "
                "เงื่อนไขการหารลงตัวบังคับ v−u=1 แล้วใช้สมาชิกน้อยสุดและมากสุด"
            ),
            distractors=[
                str(minimum + gap - 1),  # stop one short of the necessary gap
                str(minimum + gap + 1),  # add one beyond the necessary gap
                str(minimum + 2 * gap),  # double the extremal gap
                str(minimum + gap * gap),  # square the gap
                str(minimum * (index + 1)),  # multiply rather than add
                str(minimum + 2 * gap + 1),  # carry the second gap too far
            ],
        )
