"""พื้นที่ระหว่างเส้นโค้ง

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม แคลคูลัส 1 ม.6/3

Sets moved here from: math, math_pictures_add, math_thin_topics.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, frac_answer_tex, frac_tex, poly_tex
from otk.sets._support.math_chapters import _distinct
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_pictures_add import AREA_REGIONS, _fr, _q
from otk.sets._support.math_thin_topics import M6

PROVENANCE = Provenance("original")


AREA_ALT = "บริเวณที่แรเงาบนระนาบพิกัดฉาก ล้อมรอบด้วยเส้นโค้งสองเส้น"


@question_type("math.area_integral_setup_m6", display_name={"th": "เขียนอินทิกรัลแทนพื้นที่ระหว่างเส้นโค้ง"},
               level=M6, topic="พื้นที่ระหว่างเส้นโค้ง")
class AreaIntegralSetupM6(QuestionType):
    break_convergence = True  # one-part slips cluster round the answer
    def build(self, rng: Random) -> GeneratedQuestion:
        k = rng.randint(1, 5)
        kind = rng.randrange(3)
        if kind == 0:
            curves = f"y = {k if k > 1 else ''}x"
            top, bottom = f"{k if k > 1 else ''}x", "x^{2}"
            lo, hi = 0, k
        elif kind == 1:
            # A downward parabola on top: they meet where x² = k².
            curves = f"y = {2 * k * k} - x^{{2}}"
            top, bottom = f"{2 * k * k} - x^{{2}}", "x^{2}"
            lo, hi = -k, k
        else:
            curves = f"y = {k * k}"
            top, bottom = str(k * k), "x^{2}"
            lo, hi = -k, k

        def integral(length, h, upper, lower):
            # A two-term curve subtracted keeps its brackets: x² − (8 − x²).
            lower = f"({lower})" if " - " in lower else lower
            return rf"\int_{{{length}}}^{{{h}}} \left({upper} - {lower}\right)dx"

        right = integral(lo, hi, top, bottom)
        # Upper and lower swapped, the wrong bounds, and x² for the bound.
        wrongs = _distinct(right, integral(lo, hi, bottom, top), integral(0, k * k, top, bottom),
                           integral(-hi, hi, top, bottom) if lo == 0 else integral(0, hi, top, bottom),
                           integral(0, 1, top, bottom), integral(0, 2 * hi, top, bottom))
        return _maths([text("อินทิกรัลในข้อใดแทนพื้นที่ของบริเวณที่ปิดล้อมด้วยเส้นโค้ง"), content_math("y = x^{2}"),
                       text("และ"), content_math(curves)],
                      right, wrongs[:3], self.topic)


@question_type("math.area_region_picture_m6",
               display_name={"th": "หาพื้นที่บริเวณที่แรเงาระหว่างเส้นโค้ง"},
               level={"th": "ม.6"}, topic="พื้นที่ระหว่างเส้นโค้ง")
class AreaRegionPictureM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        r = rng.choice(AREA_REGIONS)
        f, g = r.curves()
        a = r.area
        return _q([text("บริเวณที่แรเงาในภาพล้อมรอบด้วยเส้นโค้ง"), content_math(f), text("และ"),
                   content_math(g), text("จงหาพื้นที่ของบริเวณนี้"), image(r.asset_id, alt=AREA_ALT)],
                  _fr(a), [_fr(a / 2), _fr(2 * a), _fr(r.box - a)], self.topic,
                  [_fr(a + 1), _fr(a + Fraction(1, 3))])


@question_type("math.area_two_curves_m6", display_name={"th": "พื้นที่ระหว่างพาราโบลากับพาราโบลาหรือเส้นตรงแนวนอน"},
               level=M6, topic="พื้นที่ระหว่างเส้นโค้ง")
class AreaTwoCurvesM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a = rng.randint(1, 4)
        kind = rng.randrange(3)
        if kind == 0:
            other = poly_tex((-1, "x^{2}"), (2 * a * a, ""))
            area = Fraction(8 * a ** 3, 3)
            wrongs = [Fraction(4 * a ** 3, 3), Fraction(16 * a ** 3, 3), Fraction(2 * a ** 3)]
        elif kind == 1:
            # y = x² and y = kx meet at 0 and k: the area is k³/6.
            k = rng.randint(1, 6)
            other = f"{k if k > 1 else ''}x"
            area = Fraction(k ** 3, 6)
            wrongs = [Fraction(k ** 3, 3), Fraction(k ** 3, 2), Fraction(k ** 2, 2), Fraction(k ** 3, 12)]
        else:
            other = str(a * a)
            area = Fraction(4 * a ** 3, 3)
            wrongs = [Fraction(2 * a ** 3, 3), Fraction(2 * a ** 3), Fraction(a ** 3, 3)]
        return _maths([text("จงหาพื้นที่ของบริเวณที่ปิดล้อมด้วยเส้นโค้ง"),
                       content_math("y = x^{2}"), text("และ"), content_math(f"y = {other}")],
                      frac_tex(area), _distinct(frac_tex(area), *[frac_tex(w) for w in wrongs])[:3], self.topic)


@question_type("math.area_between_curves",
               display_name={"th": "พื้นที่ระหว่างเส้นโค้งสองเส้น"}, level={"th": "ม.6"},
               topic="พื้นที่ระหว่างเส้นโค้ง")
class AreaBetweenCurves(MathType):
    def expr(self, rng: Random):
        r1 = rng.randint(-3, 2)
        r2 = r1 + rng.randint(2, 4)
        b, c = rng.randint(-4, 4), rng.randint(-5, 5)
        parab = poly_tex((1, "x^{2}"), (b, "x"), (c, ""))
        line = poly_tex((b + r1 + r2, "x"), (c - r1 * r2, ""))
        return MathDraw(
            rf"y = {parab}, \;\; y = {line}",
            frac_answer_tex(Fraction((r2 - r1) ** 3, 6)),
            hint=rf"\text{{intersections: }} x = {r1}, {r2}",
            prompt="จงหาพื้นที่ระหว่างเส้นโค้งทั้งสอง")
