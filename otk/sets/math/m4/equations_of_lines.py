"""สมการเส้นตรง

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม การวัดและเรขาคณิต 1 ม.4/1

Sets moved here from: math, math_bank_conics, math_geometry, math_m4, m2 linear_functions (2026-11-14).
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
from otk.sets._support.math_diagrams import LINE_FN_ALT, LINE_FNS, _img, _math_q
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
LineClosestPointM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/7 เรขาคณิตวิเคราะห์ และภาคตัดกรวย',))


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


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
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

# ── More equations of lines (2026-11): ax + by = c as y = mx + k, a parallel line through a point, a
# perpendicular line through a point, where two lines meet, and an x-intercept ──


def _line4(m, k) -> str:
    """y = mx + k with fractions as TeX."""
    m, k = Fraction(m), Fraction(k)
    mt = "" if m == 1 else "-" if m == -1 else frac_tex(m)
    head = f"y = {mt}x" if m else "y = "
    if not m:
        return f"y = {frac_tex(k)}"
    return head if not k else f"{head} {'+' if k > 0 else '-'} {frac_tex(abs(k))}"


@question_type("math.slope_intercept_form_m4", display_name={"th": "เขียนสมการเส้นตรงในรูป y = mx + c"}, level=LEVEL,
               topic="สมการเส้นตรง")
class SlopeInterceptFormM4(MathType):
    def expr(self, rng: Random):
        b = rng.choice((1, 2, 3, 4, 5))
        a, c = _nz4(rng, 1, 9), rng.randint(-15, 15)
        m, k = Fraction(-a, b), Fraction(c, b)
        right = _line4(m, k)
        wrongs = [_line4(-m, k), _line4(m, -k), _line4(Fraction(a, b), Fraction(-c, b)), _line4(-a, c)]
        return MathDraw(f"{poly_tex((a, 'x'), (b, 'y'))} = {c}", right, prompt="เขียนสมการนี้ในรูป y = mx + c",
                        distractors=_tk4(*wrongs, answer=right))


@question_type("math.parallel_through_point_m4", display_name={"th": "เส้นตรงขนานที่ผ่านจุดที่กำหนด"}, level=LEVEL,
               topic="สมการเส้นตรง")
class ParallelThroughPointM4(MathType):
    def expr(self, rng: Random):
        m, c = _nz4(rng, 1, 5), rng.randint(-9, 9)
        p, q = rng.randint(-6, 6), rng.randint(-9, 9)
        k = q - m * p
        right = _line4(m, k)
        wrongs = [_line4(m, c), _line4(-m, q + m * p), _line4(m, q + m * p), _line4(Fraction(-1, m), q + Fraction(p, m))]
        return MathDraw(rf"y = {poly_tex((m, 'x'), (c, ''))}, \; P({p}, {q})", right,
                        prompt="สมการเส้นตรงที่ขนานกับเส้นตรงนี้และผ่านจุด P คือข้อใด", distractors=_tk4(*wrongs, answer=right))


@question_type("math.perpendicular_through_point_m4", display_name={"th": "เส้นตรงตั้งฉากที่ผ่านจุดที่กำหนด"}, level=LEVEL,
               topic="สมการเส้นตรง")
class PerpendicularThroughPointM4(MathType):
    def expr(self, rng: Random):
        m = _nz4(rng, 1, 4)
        p = m * rng.randint(-3, 3)
        q = rng.randint(-9, 9)
        slope = Fraction(-1, m)
        k = q - slope * p
        right = _line4(slope, k)
        wrongs = [_line4(m, q - m * p), _line4(-slope, q + slope * p), _line4(slope, q + slope * p), _line4(-m, q + m * p)]
        return MathDraw(rf"y = {poly_tex((m, 'x'))}, \; P({p}, {q})", right,
                        prompt="สมการเส้นตรงที่ตั้งฉากกับเส้นตรงนี้และผ่านจุด P คือข้อใด", distractors=_tk4(*wrongs, answer=right))


@question_type("math.lines_meet_m4", display_name={"th": "จุดตัดของเส้นตรงสองเส้น"}, level=LEVEL, topic="สมการเส้นตรง")
class LinesMeetM4(MathType):
    def expr(self, rng: Random):
        x, y = rng.randint(-6, 6), rng.randint(-6, 6)
        m1, m2 = rng.sample((-3, -2, -1, 1, 2, 3), 2)
        c1, c2 = y - m1 * x, y - m2 * x
        right = _pt4(x, y)
        wrongs = [_pt4(y, x), _pt4(-x, -y), _pt4(x, c1), _pt4(x + 1, y)]
        return MathDraw(rf"{_line4(m1, c1)}, \;\; {_line4(m2, c2)}", right, prompt="เส้นตรงสองเส้นนี้ตัดกันที่จุดใด",
                        distractors=_tk4(*wrongs, answer=right))


@question_type("math.x_intercept_point_slope_m4", display_name={"th": "จุดตัดแกน x จากจุดและความชัน"}, level=LEVEL,
               topic="สมการเส้นตรง")
class XInterceptPointSlopeM4(MathType):
    def expr(self, rng: Random):
        m = _nz4(rng, 1, 5)
        p = rng.randint(-6, 6)
        q = m * rng.randint(-5, 5)
        x0 = p - q // m
        right = f"({x0}, 0)"
        # The y-intercept; the sign of the shift flipped; the axes swapped.
        wrongs = [f"(0, {q - m * p})", f"({p + q // m}, 0)", f"(0, {x0})", f"({x0 + 1}, 0)"]
        return MathDraw(rf"P({p}, {q}), \; m = {m}", right, prompt="เส้นตรงผ่านจุด P มีความชัน m ตัดแกน x ที่จุดใด",
                        distractors=_tk4(*wrongs, answer=right))


SlopeInterceptFormM4.PROVENANCE = Provenance("original")
ParallelThroughPointM4.PROVENANCE = Provenance("original")
PerpendicularThroughPointM4.PROVENANCE = Provenance("original")
LinesMeetM4.PROVENANCE = Provenance("original")
XInterceptPointSlopeM4.PROVENANCE = Provenance("original")


def _line_tex(m: int, c: int) -> str:
    mx = "x" if m == 1 else "-x" if m == -1 else f"{m}x"
    return f"y = {mx}" + (f" + {c}" if c > 0 else f" - {-c}" if c < 0 else "")


@question_type("math.linear_function_graph_m2", display_name={"th": "หาสมการของเส้นตรงจากกราฟ"},
               level={"th": "ม.4"}, topic="สมการเส้นตรง")
class LinearFunctionGraphM2(QuestionType):
    break_convergence = True  # one-part slips cluster round the answer
    def build(self, rng: Random) -> GeneratedQuestion:
        fn = rng.choice(LINE_FNS)
        img = _img(fn.asset_id, LINE_FN_ALT)
        m, c = fn.m, fn.c
        if rng.random() < 0.5:
            # Slope and intercept swapped, the slope's sign lost, rise over run inverted.
            wrongs = [_line_tex(c, m) if c else _line_tex(m, 1), _line_tex(-m, c),
                      _line_tex(m, -c) if c else _line_tex(m, 2), _line_tex(m + 1, c),
                      _line_tex(m, c + 1), _line_tex(m - 1, c) if m != 1 else _line_tex(2, c)]
            return _math_q([text("สมการของเส้นตรงในกราฟคือข้อใด"), img], _line_tex(m, c), wrongs,
                           self.topic)
        inv = frac_tex(Fraction(1, m))
        return _math_q([text("เส้นตรงในกราฟมีความชันเท่าใด"), img], str(m),
                       [str(-m), inv, str(c) if c != m else str(m + 1), str(m + 1)], self.topic)


@question_type("math.linear_function",
               display_name={"th": "หาสมการเส้นตรงจากสองจุด"}, level={"th": "ม.4"},
               topic="สมการเส้นตรง")
class LinearFunction(MathType):
    def expr(self, rng: Random):
        m = rng.choice([1, -1]) * rng.randint(1, 4)
        c = rng.randint(-9, 9)
        x1, x2 = rng.sample(range(-5, 6), 2)
        return MathDraw(
            rf"({x1}, {m * x1 + c}), \;\; ({x2}, {m * x2 + c})",
            rf"y = {poly_tex((m, 'x'), (c, ''))}",
            hint=r"m = \frac{y_2 - y_1}{x_2 - x_1}",
            prompt="จงหาสมการเส้นตรงที่ผ่านจุดทั้งสอง")

LinearFunctionGraphM2.PROVENANCE = Provenance("original")
LinearFunction.PROVENANCE = Provenance("original")
