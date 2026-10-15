"""A variable segment ratio from an angle bisector and two cevians."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def cevian_segment_ratio(ac: int, ad: int) -> Fraction:
    """Return CF/FD in the construction described by the set."""
    if ac <= 0 or ad <= 0:
        raise ValueError("lengths must be positive")
    return Fraction(ac, ad)


@question_type(
    "math.cevian_angle_bisector_ratio_olympiad",
    display_name={"th": "อัตราส่วนจากเส้นแบ่งครึ่งมุมและเส้นตัดสองเส้น"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต",
)
class CevianAngleBisectorRatio(WordProblem):
    def expr(self, rng: Random):
        ab, ac, ad = rng.sample(range(3, 15), 3)
        answer = cevian_segment_ratio(ac, ad)
        return MathDraw(
            rf"AB={ab},\quad AC={ac},\quad AD={ad}",
            str(answer),
            prompt=(
                "ในสามเหลี่ยม ABC ให้ D อยู่บนรังสี BA เลยจุด A "
                "เส้นแบ่งครึ่งมุม BAC ตัด BC ที่ N และ DN ตัด AC ที่ E "
                "ลาก BE ตัด CD ที่ F จงหาอัตราส่วน CF/FD"
            ),
            hint="ใช้ทฤษฎีบทเส้นแบ่งครึ่งมุม แล้วใช้เมเนเลาส์ในสามเหลี่ยม ABC และ ACD",
            distractors=[
                str(Fraction(ad, ac)),  # reverse the requested ratio
                str(Fraction(ab, ad)),  # substitute AB for AC
                str(Fraction(ac, ab)),  # substitute AB for AD
                str(Fraction(ac + ab, ad)),  # add the triangle sides
                str(Fraction(ac, ab + ad)),  # use BD instead of AD
            ],
        )
