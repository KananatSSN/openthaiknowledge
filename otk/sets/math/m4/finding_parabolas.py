"""หาสมการพาราโบลา

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม การวัดและเรขาคณิต 1 ม.4/1

Sets moved here from: math, math_thin_topics.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, poly_tex
from otk.sets._support.math_chapters import _distinct
from otk.sets._support.math_m4 import maths as _num_maths
from otk.sets._support.math_p2 import _maths

PROVENANCE = Provenance("original")


M4 = {"th": "ม.4"}


def _quad(a: int, b: int, c: int) -> str:
    return "y = " + poly_tex((a, "x^{2}"), (b, "x"), (c, ""))


@question_type("math.determine_quadratic",
               display_name={"th": "หาสมการพาราโบลาจากจุดยอด"}, level={"th": "ม.4"},
               topic="หาสมการพาราโบลา")
class DetermineQuadratic(MathType):
    def expr(self, rng: Random):
        a = rng.choice([1, -1, 2])
        p, q = rng.randint(-4, 4), rng.randint(-6, 6)
        x0 = p + rng.choice([1, 2, -1, -2])
        y0 = a * (x0 - p) ** 2 + q
        expanded = poly_tex((a, "x^{2}"), (-2 * a * p, "x"), (a * p * p + q, ""))
        return MathDraw(rf"V({p}, {q}), \;\; ({x0}, {y0})", rf"y = {expanded}",
                        hint=r"y = a(x - p)^2 + q",
                        prompt="จงหาสมการพาราโบลาที่มีจุดยอด V และผ่านจุดที่กำหนด")


@question_type("math.parabola_from_roots_m4", display_name={"th": "หาสมการพาราโบลาจากจุดตัดแกน X"},
               level=M4, topic="หาสมการพาราโบลา")
class ParabolaFromRootsM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a = rng.choice((1, -1, 2, -2))
        r1, r2 = sorted(rng.sample(range(-5, 6), 2))
        x0 = rng.choice([x for x in range(-4, 5) if x not in (r1, r2)])
        y0 = a * (x0 - r1) * (x0 - r2)
        right = _quad(a, -a * (r1 + r2), a * r1 * r2)
        # a taken with the wrong sign, the roots' signs flipped, a left out.
        wrongs = _distinct(right, _quad(-a, a * (r1 + r2), -a * r1 * r2),
                           _quad(a, a * (r1 + r2), a * r1 * r2),
                           _quad(1 if a != 1 else 2, -(1 if a != 1 else 2) * (r1 + r2), (1 if a != 1 else 2) * r1 * r2),
                           _quad(a, -a * (r1 + r2), -a * r1 * r2),
                           # The point's y taken as the constant term.
                           _quad(a, -a * (r1 + r2), y0) if y0 != a * r1 * r2 else _quad(2 * a, 0, a * r1 * r2),
                           _quad(a, a * (r1 - r2), a * r1 * r2))
        return _maths([text(f"พาราโบลาตัดแกน X ที่ x = {r1} และ x = {r2} และผ่านจุด ({x0}, {y0}) "
                            f"สมการของพาราโบลาคือข้อใด")], right, wrongs[:3], self.topic)


@question_type("math.parabola_three_points_m4", display_name={"th": "หาสมการพาราโบลาที่ผ่านสามจุด"},
               level=M4, topic="หาสมการพาราโบลา")
class ParabolaThreePointsM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a = rng.choice((1, -1, 2, -2, 3))
        b = rng.choice([v for v in range(-5, 6) if v])
        c = rng.randint(-6, 6)
        pts = [(x, a * x * x + b * x + c) for x in (-1, 0, 1)]
        shown = ", ".join(f"({x}, {y})" for x, y in pts)
        stem = text(f"พาราโบลา y = ax² + bx + c ผ่านจุด {shown}")
        if rng.random() < 0.5:
            right = _quad(a, b, c)
            wrongs = _distinct(right, _quad(a, -b, c), _quad(c or 1, b, a), _quad(a, 2 * b, c), _quad(-a, b, c))
            return _maths([stem, text("สมการของพาราโบลาคือข้อใด")], right, wrongs[:3], self.topic)
        # a = (y(1) + y(−1))/2 − c: forgetting the halving, or the minus c.
        return _num_maths([stem, text("จงหาค่า a")], str(a),
                          [str(2 * a), str(a + c), str(b)], self.topic)
