"""Feet from A to the bisectors at B and C lie on the midline: DE = (b + c − a)/2."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันที่สอง ข้อ 3",)
)


def frac_tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def feet_distance(a: int, b: int, c: int) -> Fraction:
    """Reflecting A in the bisector at B lands on BC, so D is the midpoint of
    A and that reflection: D lies on the midline MN with MD = MA = c/2 (M, N
    the midpoints of AB, AC). Likewise NE = b/2, so DE = (b + c − a)/2 with
    MN = a/2, which gives (AB + AC)/BC = DE/MN + 1."""
    return Fraction(b + c - a, 2)


TRIANGLES = tuple(
    (a, b, c) for a in range(3, 30) for b in range(3, 30) for c in range(2, 30)
    if c < a < b and b < a + c
)


@question_type(
    "math.bisector_foot_midline_olympiad",
    display_name={"th": "เท้าตั้งฉากบนเส้นแบ่งครึ่งมุมอยู่บนเส้นเชื่อมจุดกึ่งกลาง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: เส้นแบ่งครึ่งมุม",
)
class BisectorFootMidline(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(TRIANGLES)
        answer = feet_distance(a, b, c)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(a, 2), Fraction(b + c, 2), Fraction(a + b - c, 2), Fraction(b - c, 2), answer + Fraction(1, 2)]) if v != answer and v > 0]
        return MathDraw(
            rf"BC={a},\ CA={b},\ AB={c}",
            frac_tex(answer),
            prompt=(
                "D และ E เป็นเท้าของเส้นตั้งฉากจาก A ไปยังเส้นแบ่งครึ่งมุมภายในของมุม B และมุม C ตามลำดับ จงหา DE"
            ),
            hint="สะท้อน A ข้ามเส้นแบ่งครึ่งมุม B จะได้จุดบน BC จึง D อยู่บนเส้นเชื่อมจุดกึ่งกลางของ AB และ AC",
            distractors=wrong,
        )
