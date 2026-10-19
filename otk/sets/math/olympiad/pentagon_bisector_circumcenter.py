"""Angles in a pentagon whose diagonal bisects two angles at right-angle feet."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2562, ข้อ 1",)
)

ASKED = ("BDE", "DEB", "DPE", "AED")


def pentagon_angle(asked: str, half_a: int, half_c: int) -> int:
    """The asked angle, in degrees, when ∠BAE = 2·half_a and ∠BCD = 2·half_c.

    P is the circumcentre of BDE, so ∠BDE and ∠DEB are half the central
    angles ∠BPE = 180° − 2·half_a and ∠BPD = 180° − 2·half_c, and ACDE is
    cyclic, so ∠AED = 180° − ∠ACD.
    """
    if asked == "BDE":
        return 90 - half_a
    if asked == "DEB":
        return 90 - half_c
    if asked == "DPE":
        return 2 * (half_a + half_c)
    if asked == "AED":
        return 180 - half_c
    raise ValueError(asked)


def _wrong(asked: str, half_a: int, half_c: int) -> list[int]:
    swapped = pentagon_angle(asked, half_c, half_a)
    common = [
        swapped,  # mix up the two bisected angles
        half_a + half_c,  # the inscribed angle ∠DBE instead
        180 - 2 * half_a,  # the central angle ∠BPE instead
    ]
    if asked == "BDE":
        return [half_a, 2 * half_a, *common, 90 + half_a]
    if asked == "DEB":
        return [half_c, 2 * half_c, *common, 90 + half_c]
    if asked == "DPE":
        return [half_a + half_c, 180 - 2 * (half_a + half_c), *common,
                2 * (half_a + half_c) + 20]
    return [180 - 2 * half_c, 90 + half_c, *common, 180 - half_a]


@question_type(
    "math.pentagon_bisector_circumcenter_olympiad",
    display_name={"th": "มุมในห้าเหลี่ยมที่เส้นทแยงแบ่งครึ่งมุมสองมุม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมล้อมรูปสามเหลี่ยม",
)
class PentagonBisectorCircumcenter(WordProblem):
    def expr(self, rng: Random):
        half_a = rng.randint(10, 35)
        half_c = rng.choice([v for v in range(10, 36) if v != half_a])
        asked = rng.choice(ASKED)
        answer = pentagon_angle(asked, half_a, half_c)
        wrong = []
        for value in _wrong(asked, half_a, half_c):
            if 0 < value < 180 and value != answer and value not in wrong:
                wrong.append(value)
        return MathDraw(
            rf"\angle BAE={2 * half_a}^\circ,\quad \angle BCD={2 * half_c}^\circ",
            rf"{answer}^\circ",
            prompt=(
                "รูปห้าเหลี่ยมนูน ABCDE มี ∠AEB = ∠BDC = 90° "
                "และเส้นทแยง AC แบ่งครึ่งทั้งมุม BAE และมุม BCD "
                "วงกลมผ่าน A, B, E ตัดเส้นตรง AC อีกครั้งที่ P "
                f"จงหาขนาดของมุม {asked}"
            ),
            hint=(
                "P เป็นจุดกึ่งกลางส่วนโค้ง BE จึง PB = PE; "
                "ทำนองเดียวกันกับวงกลมที่มี BC เป็นเส้นผ่านศูนย์กลาง ได้ PB = PD "
                "จึง P เป็นจุดศูนย์กลางวงกลมผ่าน B, D, E"
            ),
            distractors=[rf"{value}^\circ" for value in wrong],
            variant=asked,
        )
