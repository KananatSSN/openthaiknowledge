"""สมการเส้นตรง

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม การวัดและเรขาคณิต 1 ม.4/1

Sets moved here from: math, math_bank_conics, math_geometry, math_m4.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, poly_tex
from otk.sets._support.math_bank_conics import M4, _tex_q, line_tex, pt
from otk.sets._support.math_m4 import _TRIPLES, M5, _sgn


def foot_of_perpendicular(a: int, b: int, c: int, x0, y0) -> tuple[Fraction, Fraction]:
    """The point of ax + by + c = 0 nearest (x0, y0)."""
    t = Fraction(a * x0 + b * y0 + c, a * a + b * b)
    return x0 - a * t, y0 - b * t


@question_type("math.line_equation",
               display_name={"th": "สมการเส้นตรง (จุด + ความชัน)"}, level={"th": "ม.5"},
               topic="สมการเส้นตรง")
class LineEquation(MathType):
    def expr(self, rng: Random):
        m = rng.choice([1, -1]) * rng.randint(1, 3)
        a, b = rng.randint(-5, 5), rng.randint(-6, 6)
        return MathDraw(rf"P({a}, {b}), \;\; m = {m}",
                        rf"y = {poly_tex((m, 'x'), (b - m * a, ''))}",
                        hint=r"y - y_1 = m(x - x_1)",
                        prompt="จงหาสมการเส้นตรงผ่านจุด P ความชัน m")
LineEquation.PROVENANCE = Provenance("original")


@question_type("math.line_intercepts", display_name={"th": "จุดตัดแกนของเส้นตรง"},
               level={"th": "ม.5"}, topic="สมการเส้นตรง")
class LineIntercepts(MathType):
    def expr(self, rng: Random, coef_hi: int = 9):
        a = rng.randint(1, coef_hi)
        b = rng.randint(1, coef_hi)
        # Constant is a multiple of both, so both intercepts are whole numbers.
        c = a * b * rng.randint(1, 4)
        return MathDraw(
            f"{a}x + {b}y = {c}", f"({c // a}, 0)",
            prompt="เส้นตรงนี้ตัดแกน x ที่จุดใด",
            distractors=[f"(0, {c // b})", f"({c // b}, 0)", f"({a}, {b})"])
LineIntercepts.PROVENANCE = Provenance("original")


@question_type("math.line_from_two_points_intercept",
               display_name={"th": "จุดตัดแกน y ของเส้นตรง"},
               level={"th": "ม.5"}, topic="สมการเส้นตรง")
class LineFromTwoPointsIntercept(MathType):
    def expr(self, rng: Random, slope_hi: int = 6, intercept_hi: int = 12):
        m = rng.choice([n for n in range(-slope_hi, slope_hi + 1) if n])
        b = rng.randint(-intercept_hi, intercept_hi)
        # Neither point may sit on the y-axis, or the question shows its answer.
        x1 = rng.choice([n for n in range(-6, 7) if n])
        x2 = rng.choice([n for n in range(-6, 7) if n and n != x1])
        y1, y2 = m * x1 + b, m * x2 + b
        return MathDraw(
            f"({x1}, {y1}), \\; ({x2}, {y2})", str(b),
            prompt="เส้นตรงผ่านสองจุดนี้ ตัดแกน y ที่ค่า y เท่าใด",
            distractors=[str(m), str(-b), str(y1)])
LineFromTwoPointsIntercept.PROVENANCE = Provenance("original")


@question_type("math.line_closest_point_m4",
               display_name={"th": "จุดบนเส้นตรงที่ใกล้จุดที่กำหนดที่สุด"},
               level=M4, topic="สมการเส้นตรง")
class LineClosestPointM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            a, b = rng.choice([v for v in range(-4, 5) if v]), rng.choice([v for v in range(-4, 5) if v])
            if math.gcd(a, b) == 1:
                break
        fx, fy = rng.randint(-5, 5), rng.randint(-5, 5)
        c = -(a * fx + b * fy)
        s = rng.choice([v for v in (-2, -1, 1, 2)])
        px, py = (0, 0) if rng.random() < 0.3 and (a * 0 + b * 0 + c) != 0 else (fx + s * a, fy + s * b)
        foot = foot_of_perpendicular(a, b, c, px, py)
        line = line_tex(a, b, c)
        where = "จุดกำเนิด" if (px, py) == (0, 0) else f"จุด {pt(px, py)}"
        right = pt(*foot)
        # Moving the wrong way along the normal; the reflection of P; a point on the line's axis crossing.
        t = Fraction(a * px + b * py + c, a * a + b * b)
        wrongs = [pt(px + a * t, py + b * t), pt(px - 2 * a * t, py - 2 * b * t),
                  pt(Fraction(-c, a), 0), pt(0, Fraction(-c, b)), pt(foot[0] + b, foot[1] - a)]
        stem = [text("จุดบนเส้นตรง"), content_math(line), text(f"ซึ่งอยู่ใกล้{where} ที่สุดคือจุดในข้อใด")]
        return _tex_q(stem, right, wrongs, self.topic)
LineClosestPointM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/7 เรขาคณิตวิเคราะห์ และภาคตัดกรวย',))


@question_type("math.point_line_distance_m4",
               display_name={"th": "ระยะทางจากจุดถึงเส้นตรง"},
               level=M5, topic="สมการเส้นตรง")
class PointLineDistanceM4(MathType):
    def expr(self, rng: Random):
        a, b, c = rng.choice(_TRIPLES[:5])
        if rng.random() < 0.5:
            a = -a
        x0, y0 = rng.randint(-6, 6), rng.randint(-6, 6)
        d = rng.randint(1, 6)
        # Choose the constant so the distance comes out whole: |a x0 + b y0 + k| = d·c.
        k = d * c - (a * x0 + b * y0)
        line = rf"{a}x {_sgn(b)}y {_sgn(k)} = 0"
        return MathDraw(rf"({x0}, {y0}),\quad {line}", str(d),
                        prompt="จงหาระยะทางจากจุดถึงเส้นตรง",
                        # Forgetting to divide by √(a² + b²), or dividing by a² + b².
                        distractors=_story.keep(d * c, d * c * c if d * c * c < 999 else d + c, d + 1,
                                                abs(a * x0 + b * y0), answer=d, lo=1))
PointLineDistanceM4.PROVENANCE = Provenance("original")
