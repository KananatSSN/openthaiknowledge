"""เส้นสัมผัส

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม แคลคูลัส 1 ม.6/2

Sets moved here from: math, math_bank_calculus, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import redraw_until_full
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex, poly_tex
from otk.sets._support.math_bank_calculus import M6, _num_q, _tex_q
from otk.sets._support.math_calculus import _nonzero

TANGENT = "เส้นสัมผัส"


def tangent_with_slope(c: int, m: int) -> tuple[Fraction, Fraction]:
    """For y = c − x² and slope m: x₀ = −m/2, and the tangent is y = mx + b₀. Returns (x₀, b₀)."""
    x0 = Fraction(-m, 2)
    y0 = c - x0 * x0
    return x0, y0 - m * x0


def triangle_with_axes(m: int, b0: Fraction) -> Fraction:
    """Area cut from the first quadrant (or any) by y = mx + b₀ with the axes: b₀²/(2|m|)."""
    return b0 * b0 / (2 * abs(m))


def quadratic_from_tangent(min_value: int, x0: int, m: int, y0: int) -> tuple[Fraction, Fraction]:
    """(a, h) for f = a(x − h)² − M tangent to y = y₀ + m(x − x₀) at x₀: a·u² = y₀ + M, 2a·u = m, u = x₀ − h."""
    u = Fraction(2 * (y0 + min_value), m)
    a = Fraction(m) / (2 * u)
    return a, x0 - u


def line_form(p: Fraction, q: Fraction, r: Fraction) -> str:
    """px + qy = r with integer, coprime coefficients and p > 0 (or q > 0 when p = 0)."""
    den = 1
    for v in (p, q, r):
        den = den * Fraction(v).denominator // gcd(den, Fraction(v).denominator)
    p, q, r = (int(v * den) for v in (p, q, r))
    g = gcd(gcd(abs(p), abs(q)), abs(r)) or 1
    p, q, r = p // g, q // g, r // g
    if p < 0 or (p == 0 and q < 0):
        p, q, r = -p, -q, -r
    x = "" if p == 0 else ("x" if p == 1 else f"{p}x")
    y = "" if q == 0 else (("" if abs(q) == 1 else str(abs(q))) + "y")
    if x and y:
        body = f"{x} {'-' if q < 0 else '+'} {y}"
    else:
        body = x or ("-" if q < 0 else "") + y
    return f"{body} = {r}"


@question_type("math.tangent_line",
               display_name={"th": "เส้นสัมผัสเส้นโค้ง"}, level={"th": "ม.5"},
               topic="เส้นสัมผัส")
class TangentLine(MathType):
    def expr(self, rng: Random):
        b, c = rng.randint(-5, 5), rng.randint(-6, 6)
        a = rng.randint(-3, 3)
        m = 2 * a + b
        y0 = a * a + b * a + c
        poly = poly_tex((1, "x^{2}"), (b, "x"), (c, ""))
        tangent = poly_tex((m, "x"), (y0 - m * a, ""))
        return MathDraw(rf"y = {poly}, \;\; x = {a}", rf"y = {tangent}",
                        hint=r"m = y'(a)",
                        prompt="จงหาสมการเส้นสัมผัสที่ค่า x ที่กำหนด")
TangentLine.PROVENANCE = Provenance("original")


@question_type("math.horizontal_tangent", display_name={"th": "จุดที่เส้นสัมผัสขนานแกน x"},
               level={"th": "ม.5"}, topic="เส้นสัมผัส")
class HorizontalTangent(MathType):
    def expr(self, rng: Random, lead_hi: int = 4, root_hi: int = 6):
        a = _nonzero(rng, -lead_hi, lead_hi)
        h = rng.randint(-root_hi, root_hi)
        k = rng.randint(-9, 9)
        # a(x − h)² + k has its only horizontal tangent at x = h.
        shown = poly_tex((a, "x^2"), (-2 * a * h, "x"), (a * h * h + k, ""))
        return MathDraw(
            rf"y = {shown}", f"x = {h}",
            prompt="เส้นสัมผัสเส้นโค้งนี้ขนานกับแกน x ที่ค่า x ใด",
            distractors=[f"x = {-h}", f"x = {k}", "x = 0"])
HorizontalTangent.PROVENANCE = Provenance("original")


@question_type("math.tangent_conditions_m6",
               display_name={"th": "เส้นสัมผัสที่กำหนดความชันหรือกำหนดเส้นมา"},
               level=M6, topic=TANGENT)
class TangentConditionsM6(QuestionType):
    @redraw_until_full()
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            while True:
                c, m = rng.randint(3, 20), rng.choice((-2, -4, -6, 2, 4))
                x0, b0 = tangent_with_slope(c, m)
                if b0 > 0:
                    break
            right = triangle_with_axes(m, b0)
            stem = [text(f"ให้ L เป็นเส้นตรงซึ่งมีความชันเท่ากับ {m} และสัมผัสพาราโบลา"),
                    content_math(f"y = {c} - x^{{2}}"),
                    text("พื้นที่ที่ปิดล้อมด้วยแกน X แกน Y และเส้นตรง L เท่ากับกี่ตารางหน่วย")]
            # Forgetting ½; the parabola's own intercept c instead of b₀; the intercept b₀ itself.
            named = [2 * right, triangle_with_axes(m, Fraction(c)), b0]
            return _num_q(stem, right, named, self.topic)
        if kind == 1:
            while True:
                a, h, big_m = rng.choice((1, 2, 3)), rng.randint(-2, 4), rng.randint(2, 20)
                x0 = rng.choice((1, 0, 2, -1))
                if x0 != h:
                    break
            f = lambda x: a * (x - h) ** 2 - big_m
            m, y0 = 2 * a * (x0 - h), f(x0)
            b0 = y0 - m * x0
            line = line_form(Fraction(-m), Fraction(1), Fraction(b0))
            t = rng.choice([v for v in range(-2, 5) if v != x0])
            aa, hh = quadratic_from_tangent(big_m, x0, m, y0)
            right = aa * (t - hh) ** 2 - big_m
            stem = [text(f"กำหนดให้ f เป็นฟังก์ชันพหุนามกำลังสองที่มีค่าต่ำสุดเป็น −{big_m} ถ้าเส้นตรง"),
                    content_math(line), text("สัมผัสเส้นโค้ง y = f(x) ที่ x = " + str(x0) + " แล้ว"),
                    content_math(f"f({t})"), text("เท่ากับเท่าใด")]
            # The tangent line's value at t; vertex taken at x₀; a from m alone (u = 1).
            named = [y0 + m * (t - x0), Fraction(m, 2) * (t - x0) ** 2 + y0, Fraction(m, 2) * (t - x0 + 1) ** 2 - big_m]
            return _num_q(stem, right, named, self.topic)
        k, d = rng.choice((2, 3, 4, 6, 8, 12)), rng.randint(0, 3)
        x0 = rng.choice([v for v in range(-1, 4) if v + d > 0])
        y0 = Fraction(k, x0 + d)
        m = Fraction(-k, (x0 + d) ** 2)
        den = "x" if not d else f"x + {d}"
        right = line_form(-m, Fraction(1), y0 - m * x0)
        stem = [text("สมการเส้นสัมผัสเส้นโค้ง"), content_math(rf"y = \frac{{{k}}}{{{den}}}"), text("ที่จุด"),
                content_math(f"\\left({x0}, {frac_tex(y0)}\\right)"), text("คือข้อใด")]
        # The slope's sign lost; the normal line; the slope −k/(x₀ + d) without squaring; y₀ used as the intercept.
        m2 = Fraction(-k, x0 + d)
        wrongs = [line_form(m, Fraction(1), y0 + m * x0), line_form(Fraction(1), m, x0 + m * y0),
                  line_form(-m2, Fraction(1), y0 - m2 * x0), line_form(-m, Fraction(1), y0),
                  line_form(-2 * m, Fraction(1), y0 - 2 * m * x0)]
        return _tex_q(stem, right, wrongs, self.topic)
TangentConditionsM6.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/15 แคลคูลัส',))


@question_type("math.normal_line", display_name={"th": "เส้นตั้งฉากกับเส้นโค้ง"},
               level={"th": "ม.5"}, topic="เส้นสัมผัส")
class NormalLine(MathType):
    def expr(self, rng: Random, coef_hi: int = 4, point_hi: int = 4):
        a = _nonzero(rng, -coef_hi, coef_hi)
        b = rng.randint(-6, 6)
        c = rng.randint(-9, 9)
        x0 = _nonzero(rng, -point_hi, point_hi)
        slope = 2 * a * x0 + b                    # tangent slope
        if slope == 0:
            b += 1
            slope = 2 * a * x0 + b
        normal = Fraction(-1, slope)
        shown = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        return MathDraw(
            rf"y = {shown}, \quad x = {x0}", frac_tex(normal),
            prompt="จงหาความชันของเส้นตั้งฉากกับเส้นโค้ง ณ จุดนี้",
            distractors=[str(slope), frac_tex(Fraction(1, slope)),
                         str(-slope)])
NormalLine.PROVENANCE = Provenance("original")
