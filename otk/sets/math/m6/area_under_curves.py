"""พื้นที่

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม แคลคูลัส 1 ม.6/3

Sets moved here from: math, math_bank_calculus, math_calculus, math_thin_topics.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import (
    MathDraw,
    MathType,
    frac_answer_tex,
    frac_tex,
    poly_tex,
)
from otk.kit.math_problems import (
    poly_tex as poly_tex_math_calculus,
)
from otk.kit.math_problems import (
    poly_tex as poly_tex_math_thin_topics,
)
from otk.sets._support.math_bank_calculus import (
    M6,
    _num_q,
    _tex_q,
)
from otk.sets._support.math_bank_calculus import (
    poly_tex as poly_tex_math_bank_calculus,
)
from otk.sets._support.math_chapters import _distinct
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_thin_topics import M5

AREA = "พื้นที่"


@question_type("math.area_power_curve_m5", display_name={"th": "พื้นที่ใต้เส้นโค้ง y = kxⁿ"},
               level=M5, topic="พื้นที่")
class AreaPowerCurveM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            k, b = rng.choice((1, 3)), rng.randint(1, 5)
            curve, lo, hi, area = poly_tex_math_thin_topics((k, "x^{2}")), 0, b, Fraction(k * b ** 3, 3)
            wrongs = [Fraction(k * b ** 2, 2), Fraction(k * b ** 3), Fraction(2 * k * b), Fraction(k * b ** 3, 2)]
        elif kind == 1:
            k, b = rng.choice((1, 2, 4)), rng.randint(1, 4)
            curve, lo, hi, area = poly_tex_math_thin_topics((k, "x^{3}")), 0, b, Fraction(k * b ** 4, 4)
            wrongs = [Fraction(k * b ** 3, 3), Fraction(k * b ** 4), Fraction(3 * k * b ** 2), Fraction(k * b ** 4, 2)]
        else:
            c = rng.randint(1, 4)
            # Below the axis: the integral is negative, the area is not.
            curve, lo, hi, area = poly_tex_math_thin_topics((1, "x^{2}"), (-c * c, "")), -c, c, Fraction(4 * c ** 3, 3)
            wrongs = [-area, Fraction(2 * c ** 3, 3), Fraction(8 * c ** 3, 3)]
        return _maths([text("จงหาพื้นที่ของบริเวณที่ปิดล้อมด้วยเส้นโค้ง"), content_math(f"y = {curve}"),
                       text(f"แกน X และเส้นตรง x = {lo} ถึง x = {hi}" if kind < 2 else "และแกน X")],
                      frac_tex(area), _distinct(frac_tex(area), *[frac_tex(w) for w in wrongs])[:3],
                      self.topic)
AreaPowerCurveM5.PROVENANCE = Provenance("original")


@question_type("math.area_under_curve",
               display_name={"th": "พื้นที่ระหว่างเส้นโค้งกับแกน x"}, level={"th": "ม.5"},
               topic="พื้นที่")
class AreaUnderCurve(MathType):
    def expr(self, rng: Random):
        r1 = rng.randint(-4, 2)
        r2 = r1 + rng.randint(2, 5)
        tex = poly_tex((1, "x^{2}"), (-(r1 + r2), "x"), (r1 * r2, ""))
        area = Fraction((r2 - r1) ** 3, 6)
        return MathDraw(rf"y = {tex}", frac_answer_tex(area),
                        hint=rf"\text{{roots: }} x = {r1}, {r2}",
                        prompt="จงหาพื้นที่ที่ล้อมด้วยเส้นโค้งกับแกน x")
AreaUnderCurve.PROVENANCE = Provenance("original")


@question_type("math.parabola_area_m6",
               display_name={"th": "หาพาราโบลาจากพื้นที่ที่ปิดล้อมกับแกน X"},
               level=M6, topic=AREA)
class ParabolaAreaM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            s = rng.choice((3, 6))
            k = Fraction(s * s)
            area = Fraction(4, 3) * s ** 3
            t = rng.randint(1, s - 1)
            right = 2 * (k - t * t)
            stem = [text("ให้"), content_math(r"f(x) = -x^{2} + k"),
                    text("เมื่อ k เป็นจำนวนจริงบวก ถ้าพื้นที่ที่ปิดล้อมด้วยเส้นโค้ง"), content_math("y = f(x)"),
                    text("กับแกน X เท่ากับ"), content_math(frac_tex(area)), text("ตารางหน่วย แล้ว"),
                    content_math(f"f(-{t}) + f({t})"), text("เท่ากับเท่าใด")]
            # f(t) once; 2k (f(±t) read as k); t² added instead of subtracted.
            return _num_q(stem, right, [k - t * t, 2 * k, 2 * (k + t * t)], self.topic)
        c = Fraction(rng.choice((1, 4, 9, 16, 25, 8, 12)))
        while True:
            r = rng.choice((Fraction(1, 2), Fraction(3, 4), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(3)))
            a = c / (r * r)
            if a.denominator == 1 and a <= 64:
                break
        area = Fraction(4, 3) * c * r
        cc = int(c)
        if kind == 1:
            stem = [text("ถ้าพื้นที่ที่ปิดล้อมด้วยกราฟของพาราโบลาซึ่งมีจุดยอดอยู่ที่"), content_math(f"(0, -{cc})"),
                    text("กับแกน X มีค่าเท่ากับ"), content_math(frac_tex(area)),
                    text("ตารางหน่วย แล้วสมการพาราโบลาคือข้อใด")]
            fmt = lambda aa: rf"y = {poly_tex_math_bank_calculus([aa, 0, -c])}"
            # Area taken as the full rectangle 2rc; as half of it; r read as a.
            r_rect, r_half = area / (2 * c), area / c
            wrongs = [fmt(c / (r_rect * r_rect)), fmt(c / (r_half * r_half)), fmt(a * 4), fmt(a / 4), fmt(2 * a)]
            return _tex_q(stem, fmt(a), wrongs, self.topic)
        t = rng.randint(1, 4)
        right = a * t * t - c
        stem = [text("ให้ f(x) เป็นฟังก์ชันกำลังสอง ซึ่งกราฟของ y = f(x) มีจุดต่ำสุดที่"), content_math(f"(0, -{cc})"),
                text("และพื้นที่ที่ปิดล้อมด้วยกราฟกับแกน X เท่ากับ"), content_math(frac_tex(area)),
                text("ตารางหน่วย แล้ว"), content_math(f"f({t})"), text("มีค่าเท่ากับเท่าใด")]
        # Area as the rectangle 2rc; a read as 1/r²; forgetting −c.
        r_rect = area / (2 * c)
        named = [c / (r_rect * r_rect) * t * t - c, t * t / (r * r) - c, a * t * t]
        return _num_q(stem, right, named, self.topic)
ParabolaAreaM6.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/15 แคลคูลัส',))


@question_type("math.area_between_curve_and_line",
               display_name={"th": "พื้นที่ระหว่างพาราโบลากับแกน x"},
               level={"th": "ม.5"}, topic="พื้นที่")
class AreaBetweenCurveAndLine(MathType):
    """∫ from p to q of −(x−p)(x−q) is (q−p)³/6 — exact, no decimals."""

    def expr(self, rng: Random, root_hi: int = 6):
        p, q = sorted(rng.sample(range(-root_hi, root_hi + 1), 2))
        area = Fraction((q - p) ** 3, 6)
        shown = poly_tex_math_calculus((-1, "x^2"), (p + q, "x"), (-p * q, ""))
        return MathDraw(
            rf"y = {shown}", frac_tex(area),
            prompt="จงหาพื้นที่ที่ปิดล้อมด้วยเส้นโค้งนี้กับแกน x",
            distractors=[frac_tex(-area), frac_tex(Fraction((q - p) ** 3, 3)),
                         frac_tex(Fraction((q - p) ** 2, 2))])
AreaBetweenCurveAndLine.PROVENANCE = Provenance("original")


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType  # noqa: E402
from otk.kit.math_problems import binomial_tex  # noqa: E402
from otk.sets._support.math_m6 import M6 as LEVEL  # noqa: E402


def _nz6(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk6(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk6(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk6(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt6(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk6(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk6(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))


def _num6(v) -> str:
    """A terminating decimal without trailing zeros: Fraction(25, 2) -> 12.5."""
    v = Fraction(v)
    sign = "-" if v < 0 else ""
    v = abs(v)
    whole, rem = divmod(v.numerator, v.denominator)
    if not rem:
        return f"{sign}{whole}"
    digits = ""
    for _ in range(6):
        rem *= 10
        d, rem = divmod(rem, v.denominator)
        digits += str(d)
        if not rem:
            break
    return f"{sign}{whole}.{digits.rstrip('0')}"


def _dk6(*values, answer) -> list[str]:
    """Distinct decimal distractors, the answer left out."""
    return _tk6(*(_num6(v) for v in values), answer=_num6(answer))

# ── More areas (2026-11): under a line, under x³, inside a downward parabola, under √x, under x² + c, and
# between y = x² − a² and the x-axis ──


@question_type("math.area_under_line_m6", display_name={"th": "พื้นที่ใต้เส้นตรง"}, level=LEVEL, topic="พื้นที่")
class AreaUnderLineM6(MathType):
    def expr(self, rng: Random):
        m, c = rng.randint(1, 5), rng.randint(1, 9)
        a, b = sorted(rng.sample(range(0, 7), 2))
        right = Fraction(m, 2) * (b * b - a * a) + c * (b - a)
        return MathDraw(rf"y = {poly_tex((m, 'x'), (c, ''))}, \quad {a} \le x \le {b}",
                        frac_tex(right), prompt="จงหาพื้นที่ใต้เส้นตรงนี้เหนือแกน X ในช่วงที่กำหนด",
                        distractors=_fk6(m * (b * b - a * a) + c * (b - a), (m * b + c) * (b - a), Fraction(m, 2) * (b * b - a * a),
                                         right + 1, answer=right))


@question_type("math.area_under_cubic_m6", display_name={"th": "พื้นที่ใต้เส้นโค้ง y = x³"}, level=LEVEL, topic="พื้นที่")
class AreaUnderCubicM6(MathType):
    def expr(self, rng: Random):
        a = rng.randint(1, 6)
        right = Fraction(a ** 4, 4)
        return MathDraw(rf"y = x^{{3}}, \quad 0 \le x \le {a}", frac_tex(right), prompt="จงหาพื้นที่ใต้เส้นโค้งเหนือแกน X ในช่วงที่กำหนด",
                        distractors=_fk6(Fraction(a ** 4, 3), a ** 3, 3 * a * a, Fraction(a ** 3, 4), answer=right))


@question_type("math.area_inside_parabola_m6", display_name={"th": "พื้นที่ระหว่างพาราโบลาคว่ำกับแกน X"}, level=LEVEL, topic="พื้นที่")
class AreaInsideParabolaM6(MathType):
    def expr(self, rng: Random):
        p, q = sorted(rng.sample(range(-5, 6), 2))
        right = Fraction((q - p) ** 3, 6)
        return MathDraw(rf"y = -{binomial_tex(-p)}{binomial_tex(-q)}", frac_tex(right), prompt="จงหาพื้นที่ที่ปิดล้อมด้วยเส้นโค้งนี้กับแกน X",
                        distractors=_fk6(Fraction((q - p) ** 3, 3), Fraction((q - p) ** 2, 4) * (q - p), (q - p) ** 2, Fraction((q - p) ** 3, 12),
                                         answer=right))


@question_type("math.area_under_root_m6", display_name={"th": "พื้นที่ใต้เส้นโค้ง y = √x"}, level=LEVEL, topic="พื้นที่")
class AreaUnderRootM6(MathType):
    def expr(self, rng: Random):
        k = rng.randint(1, 5)
        right = Fraction(2 * k ** 3, 3)
        return MathDraw(rf"y = \sqrt{{x}}, \quad 0 \le x \le {k * k}", frac_tex(right), prompt="จงหาพื้นที่ใต้เส้นโค้งเหนือแกน X ในช่วงที่กำหนด",
                        distractors=_fk6(Fraction(k ** 3, 3), k ** 3, Fraction(3 * k ** 3, 2), Fraction(2 * k * k, 3), answer=right))


@question_type("math.area_under_shifted_square_m6", display_name={"th": "พื้นที่ใต้เส้นโค้ง y = x² + c"}, level=LEVEL, topic="พื้นที่")
class AreaUnderShiftedSquareM6(MathType):
    def expr(self, rng: Random):
        a, c = rng.randint(1, 6), rng.randint(1, 9)
        right = Fraction(a ** 3, 3) + c * a
        return MathDraw(rf"y = x^{{2}} + {c}, \quad 0 \le x \le {a}", frac_tex(right), prompt="จงหาพื้นที่ใต้เส้นโค้งเหนือแกน X ในช่วงที่กำหนด",
                        distractors=_fk6(Fraction(a ** 3, 3), Fraction(a ** 3, 3) + c, a ** 3 + c * a, right + a, answer=right))


@question_type("math.area_below_axis_m6", display_name={"th": "พื้นที่ใต้แกน X ของพาราโบลา"}, level=LEVEL, topic="พื้นที่")
class AreaBelowAxisM6(MathType):
    def expr(self, rng: Random):
        a = rng.randint(1, 6)
        right = Fraction(4 * a ** 3, 3)
        return MathDraw(rf"y = x^{{2}} - {a * a}", frac_tex(right), prompt="จงหาพื้นที่ที่ปิดล้อมด้วยเส้นโค้งนี้กับแกน X",
                        distractors=_fk6(-right, Fraction(2 * a ** 3, 3), Fraction(8 * a ** 3, 3), 2 * a ** 3, answer=right))


AreaUnderLineM6.PROVENANCE = Provenance("original")
AreaUnderCubicM6.PROVENANCE = Provenance("original")
AreaInsideParabolaM6.PROVENANCE = Provenance("original")
AreaUnderRootM6.PROVENANCE = Provenance("original")
AreaUnderShiftedSquareM6.PROVENANCE = Provenance("original")
AreaBelowAxisM6.PROVENANCE = Provenance("original")
