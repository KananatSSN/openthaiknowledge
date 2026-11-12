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

from fractions import Fraction  # noqa: E402

from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType  # noqa: E402
from otk.kit.math_problems import binomial_tex, frac_tex  # noqa: E402
from otk.sets._support.math_m4 import M4 as LEVEL  # noqa: E402


def _nz4(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk4(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk4(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk4(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt4(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk4(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk4(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))

# ── More finding parabolas (2026-11): a from the vertex and a point, the y-intercept from the vertex, the
# vertex from the roots, b from three points, the axis from two equal heights, the greatest value from the
# roots, and the equation from the vertex ──


def _vform4(a: int, h: int, k: int) -> str:
    lead = "" if a == 1 else "-" if a == -1 else str(a)
    inner = f"(x {'-' if h > 0 else '+'} {abs(h)})^{{2}}" if h else "x^{2}"
    tail = f" {'+' if k > 0 else '-'} {abs(k)}" if k else ""
    return f"y = {lead}{inner}{tail}"


@question_type("math.parabola_a_from_point_m4", display_name={"th": "หาค่า a จากจุดยอดและจุดที่ผ่าน"}, level=LEVEL,
               topic="หาสมการพาราโบลา")
class ParabolaAFromPointM4(MathType):
    def expr(self, rng: Random):
        h, k = rng.randint(-5, 5), rng.randint(-9, 9)
        a = _nz4(rng, 1, 4)
        d = _nz4(rng, 1, 3)
        x, y = h + d, k + a * d * d
        # The sign lost; k ignored; d not squared.
        return MathDraw(rf"V({h}, {k}), \; P({x}, {y})", str(a), prompt="พาราโบลา y = a(x − h)² + k มีจุดยอด V และผ่านจุด P ค่าของ a เท่ากับเท่าใด",
                        distractors=_tk4(str(-a), frac_tex(Fraction(y, d * d)), frac_tex(Fraction(y - k, d)), str(a + 1), answer=str(a)))


@question_type("math.parabola_y_intercept_vertex_m4", display_name={"th": "จุดตัดแกน y จากจุดยอด"}, level=LEVEL,
               topic="หาสมการพาราโบลา")
class ParabolaYInterceptVertexM4(MathType):
    def expr(self, rng: Random):
        h, k = _nz4(rng, 1, 8), rng.randint(-9, 9)
        right = h * h + k
        # The vertex height; h not squared; the square taken away.
        return MathDraw(_vform4(1, h, k), str(right), prompt="พาราโบลานี้ตัดแกน y ที่ y เท่ากับเท่าใด",
                        distractors=_nk4(k, h + k, k - h * h, right + 1, answer=right))


@question_type("math.vertex_from_roots_m4", display_name={"th": "จุดยอดจากจุดตัดแกน x"}, level=LEVEL, topic="หาสมการพาราโบลา")
class VertexFromRootsM4(MathType):
    def expr(self, rng: Random):
        while True:
            p, q = sorted(rng.sample(range(-9, 10), 2))
            if (p + q) % 2 == 0:
                break
        h = (p + q) // 2
        k = -((q - p) // 2) ** 2
        right = _pt4(h, k)
        wrongs = [_pt4(-h, k), _pt4(h, -k), _pt4(h, p * q - 1 if p * q - 1 != k else k - 1), _pt4(h + 1, k)]
        return MathDraw(rf"y = {binomial_tex(-p)}{binomial_tex(-q)}", right, prompt="พาราโบลานี้มีจุดยอดที่จุดใด",
                        distractors=_tk4(*wrongs, answer=right))


@question_type("math.b_from_three_points_m4", display_name={"th": "หาค่า b จากจุดสามจุด"}, level=LEVEL, topic="หาสมการพาราโบลา")
class BFromThreePointsM4(MathType):
    def expr(self, rng: Random):
        a, b, c = _nz4(rng, 1, 4), _nz4(rng, 1, 8), rng.randint(-9, 9)
        y1, y0, y2 = a - b + c, c, a + b + c
        # The heights' sum; the difference not halved; c.
        return MathDraw(rf"(-1, {y1}), \; (0, {y0}), \; (1, {y2})", str(b),
                        prompt="พาราโบลา y = ax² + bx + c ผ่านจุดทั้งสามนี้ ค่าของ b เท่ากับเท่าใด",
                        distractors=_nk4(y2 - y1, -b, y2 + y1 - 2 * y0, b + 1, answer=b))


@question_type("math.axis_from_equal_heights_m4", display_name={"th": "แกนสมมาตรจากสองจุดที่สูงเท่ากัน"}, level=LEVEL,
               topic="หาสมการพาราโบลา")
class AxisFromEqualHeightsM4(MathType):
    def expr(self, rng: Random):
        while True:
            p, q = sorted(rng.sample(range(-9, 10), 2))
            if (p + q) % 2 == 0:
                break
        y = rng.randint(-9, 9)
        right = f"x = {(p + q) // 2}"
        wrongs = [f"x = {q - p}", f"x = {(q - p) // 2}", f"y = {y}", f"x = {p + q}"]
        return MathDraw(rf"({p}, {y}), \; ({q}, {y})", right, prompt="พาราโบลาผ่านจุดทั้งสองนี้ แกนสมมาตรคือเส้นใด",
                        distractors=_tk4(*wrongs, answer=right))


@question_type("math.max_from_roots_m4", display_name={"th": "ค่าสูงสุดของพาราโบลาคว่ำจากจุดตัดแกน x"}, level=LEVEL,
               topic="หาสมการพาราโบลา")
class MaxFromRootsM4(MathType):
    def expr(self, rng: Random):
        while True:
            p, q = sorted(rng.sample(range(-9, 10), 2))
            if (p + q) % 2 == 0:
                break
        right = ((q - p) // 2) ** 2
        # The product; the gap not halved; the axis.
        return MathDraw(rf"y = -{binomial_tex(-p)}{binomial_tex(-q)}", str(right), prompt="ค่าสูงสุดของฟังก์ชันนี้เท่ากับเท่าใด",
                        distractors=_nk4(-p * q, (q - p) ** 2, (p + q) // 2, right + 1, answer=right))


@question_type("math.equation_from_vertex_m4", display_name={"th": "สมการพาราโบลาจากจุดยอด"}, level=LEVEL, topic="หาสมการพาราโบลา")
class EquationFromVertexM4(MathType):
    def expr(self, rng: Random):
        h, k = _nz4(rng, 1, 6), rng.randint(-9, 9)
        right = f"y = {poly_tex((1, 'x^{2}'), (-2 * h, 'x'), (h * h + k, ''))}"
        wrongs = [f"y = {poly_tex((1, 'x^{2}'), (2 * h, 'x'), (h * h + k, ''))}", f"y = {poly_tex((1, 'x^{2}'), (-2 * h, 'x'), (k, ''))}",
                  f"y = {poly_tex((1, 'x^{2}'), (-h, 'x'), (h * h + k, ''))}"]
        return MathDraw(rf"V({h}, {k})", right, prompt="พาราโบลา y = x² + bx + c มีจุดยอด V สมการพาราโบลาคือข้อใด",
                        distractors=_tk4(*wrongs, answer=right))
