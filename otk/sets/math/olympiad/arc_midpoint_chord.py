"""B the midpoint of arc AC in cyclic ABCD: AB² = BD² − AD·CD."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 2",))


def chord_square(ad: int, bd: int, cd: int) -> int:
    """DB bisects ∠ADC; the law of cosines in ABD and CBD with AB = BC gives
    cos∠ADB = (AD + CD)/(2BD), hence AB² = BD² − AD·CD (source: 16 − 6 = 10)."""
    return bd * bd - ad * cd


def root_tex(n: int) -> str:
    outside, inside = 1, n
    f = 2
    while f * f <= inside:
        while inside % (f * f) == 0:
            inside //= f * f
            outside *= f
        f += 1
    if inside == 1:
        return str(outside)
    return ("" if outside == 1 else str(outside)) + rf"\sqrt{{{inside}}}"


CASES = tuple(
    (a, d, c) for a in range(2, 12) for c in range(1, a) for d in range(2, 14)
    if d * d > a * c and a + c < 2 * d and isqrt(d * d - a * c) ** 2 != d * d - a * c
)


@question_type(
    "math.arc_midpoint_chord_olympiad",
    display_name={"th": "ความยาวคอร์ดเมื่อ B เป็นจุดกึ่งกลางส่วนโค้ง AC"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class ArcMidpointChord(WordProblem):
    def expr(self, rng: Random):
        ad, bd, cd = rng.choice(CASES)
        answer = root_tex(chord_square(ad, bd, cd))
        wrong = [t for t in dict.fromkeys([root_tex(bd * bd + ad * cd), root_tex(ad * cd), root_tex(bd * bd - cd * cd), root_tex(ad * ad - cd * cd + 1), str(bd)]) if t != answer]
        return MathDraw(
            rf"AD={ad},\quad BD={bd},\quad CD={cd}",
            answer,
            prompt="ABCD แนบในวงกลม และส่วนโค้ง AB ยาวเท่าส่วนโค้ง BC จงหา AB",
            hint="AB = BC และ DB แบ่งครึ่งมุม ADC ใช้กฎของโคไซน์ในรูปสามเหลี่ยม ABD และ CBD",
            distractors=wrong,
        )
