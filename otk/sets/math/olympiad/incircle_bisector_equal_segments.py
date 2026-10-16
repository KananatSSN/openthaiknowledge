"""Compare two bisector intersections in an incircle triangle."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2563, ข้อ 6",)
)


def common_bisector_segment(af: int, bf: int) -> Fraction:
    """Both FK and FL equal AF·BF/AB."""
    if af <= 0 or bf <= 0:
        raise ValueError("tangent lengths must be positive")
    return Fraction(af * bf, af + bf)


def _acute_sides(x: int, y: int, z: int) -> bool:
    sides = sorted((x + y, x + z, y + z))
    return sides[2] ** 2 < sides[0] ** 2 + sides[1] ** 2


@question_type(
    "math.incircle_bisector_equal_segments_olympiad",
    display_name={"th": "เส้นแบ่งครึ่งมุมสองเส้นในสามเหลี่ยมมีวงกลมแนบใน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิตของวงกลม",
)
class IncircleBisectorEqualSegments(WordProblem):
    def expr(self, rng: Random):
        while True:
            x, y, z = (rng.randint(3, 12) for _ in range(3))
            if _acute_sides(x, y, z):
                break
        answer = common_bisector_segment(x, y)
        return MathDraw(
            rf"AF={x},\quad BF={y},\quad CE={z}",
            str(answer),
            prompt=(
                "สามเหลี่ยมมุมแหลม ABC มีวงกลมแนบในสัมผัส BC,CA,AB ที่ D,E,F "
                "จุด K,L อยู่บน AB โดย DF แบ่งครึ่งมุม ADK และ EF แบ่งครึ่งมุม BEL "
                "จงหาความยาว FK ซึ่งเท่ากับ FL"
            ),
            hint=(
                "ใช้ความยาวเส้นสัมผัสจากจุดเดียวกัน แล้วใช้ทฤษฎีบทเส้นแบ่งครึ่งมุม "
                "จะได้ AL=AF²/AB และ AK=AF+AF·BF/AB"
            ),
            distractors=[
                str(Fraction(x * x, x + y)),  # report AL instead of FL
                str(Fraction(y * y, x + y)),  # exchange tangent lengths
                str(Fraction(x * y, 2 * (x + y))),  # halve the bisected segment
                str(Fraction(x * y, z + y)),  # use BC instead of AB
                str(x + y),  # report the whole AB side
                str(answer + 1),  # shift the intersection by one unit
            ],
        )
