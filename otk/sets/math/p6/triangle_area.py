"""พื้นที่รูปสามเหลี่ยม

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.6/*

Sets moved here from: math, math_apply_stage, math_diagrams, math_p6.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sets._support.math_apply_stage import _n, _nums
from otk.sets._support.math_diagrams import (
    L_FIGURES,
    TRIANGLE_FIGURES,
    _img,
    _math_q,
    figure_alt,
)
from otk.sets._support.math_diagrams import (
    _nums as _nums_math_diagrams,
)
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_p6 import LEVEL

PROVENANCE = Provenance("original")


_AREA_TOPIC = "พื้นที่รูปสามเหลี่ยม"


@question_type("math.triangle_area",
               display_name={"th": "พื้นที่รูปสามเหลี่ยม"}, level={"th": "ป.6"},
               topic="พื้นที่รูปสามเหลี่ยม")
class TriangleArea(WordProblem):
    def expr(self, rng: Random):
        base = rng.randint(2, 10) * 2               # even → integer area
        h = rng.randint(3, 15)
        prompt = rng.choice((
            f"สามเหลี่ยมฐาน {base} สูง {h} หน่วย มีพื้นที่เท่าใด?",
            f"ธงสามเหลี่ยมมีฐานยาว {base} เซนติเมตร สูง {h} เซนติเมตร ใช้ผ้ากี่ตารางเซนติเมตร",
            f"แปลงดอกไม้รูปสามเหลี่ยมมีฐานยาว {base} เมตร สูง {h} เมตร มีพื้นที่กี่ตารางเมตร",
        ))
        return MathDraw("", str(base * h // 2), prompt=prompt,
                        distractors=[str(base * h), str(base + h),
                                     str((base + h) // 2)])


@question_type("math.triangle_area_figure_p6", display_name={"th": "หาพื้นที่รูปสามเหลี่ยมจากรูป"},
               level={"th": "ป.6"}, topic="พื้นที่รูปสามเหลี่ยม")
class TriangleAreaFigureP6(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        f = rng.choice(TRIANGLE_FIGURES)
        b, h, _ = f.dims
        ans = Fraction(b * h, 2)
        tex = frac_tex(ans) if ans.denominator != 1 else str(ans.numerator)
        wrongs = [str(b * h), str(b + h), str(2 * (b + h)), frac_tex(Fraction(b * h, 4))]
        return _math_q([text("รูปสามเหลี่ยมนี้มีพื้นที่กี่ตารางเซนติเมตร"), _img(f.asset_id, figure_alt(f))],
                       tex, wrongs, self.topic)


@question_type("math.triangle_missing_side_p6",
               display_name={"th": "หาความยาวฐานหรือความสูงจากพื้นที่รูปสามเหลี่ยม"},
               level=LEVEL, topic=_AREA_TOPIC)
class TriangleMissingSideP6(WordProblem):
    def expr(self, rng: Random):
        base, h = rng.randint(3, 30), rng.randint(2, 30)
        if base * h % 2:
            base += 1
        area = base * h // 2
        prompt = rng.choice((
            f"รูปสามเหลี่ยมมีพื้นที่ {area} ตารางเซนติเมตร ฐานยาว {base} เซนติเมตร สูงกี่เซนติเมตร",
            f"ป้ายรูปสามเหลี่ยมมีพื้นที่ {area} ตารางเซนติเมตร ฐานของป้ายยาว {base} เซนติเมตร "
            f"ป้ายสูงกี่เซนติเมตร",
            f"ที่ดินรูปสามเหลี่ยมมีพื้นที่ {area} ตารางเมตร ด้านที่เป็นฐานยาว {base} เมตร "
            f"ความสูงของที่ดินที่วัดจากฐานยาวกี่เมตร",
        ))
        return MathDraw("", str(h), prompt=prompt,
                        # Dividing by the base but forgetting the half.
                        distractors=_story.keep(area // base if area % base == 0 else h + 2,
                                                area - base, 2 * area, answer=h, lo=1))


@question_type("math.composite_area_p6",
               display_name={"th": "พื้นที่ของรูปหลายเหลี่ยม (แบ่งเป็นสี่เหลี่ยมและสามเหลี่ยม)"},
               level=LEVEL, topic=_AREA_TOPIC)
class CompositeAreaP6(WordProblem):
    def expr(self, rng: Random):
        w, length = rng.randint(4, 20), rng.randint(6, 30)
        h = 2 * rng.randint(1, 8)
        rect, tri = w * length, w * h // 2
        kind = rng.randrange(3)
        if kind == 0:
            ans = rect + tri
            prompt = (f"รูปห้าเหลี่ยมรูปบ้านประกอบด้วยรูปสี่เหลี่ยมผืนผ้ากว้าง {w} ม. ยาว {length} ม. "
                      f"และมีหลังคารูปสามเหลี่ยมฐานยาว {w} ม. สูง {h} ม. อยู่ด้านบน "
                      f"รูปทั้งหมดมีพื้นที่กี่ตารางเมตร")
            wrongs = [rect + w * h, rect, rect - tri]
        elif kind == 1:
            ans = rect - tri
            prompt = (f"แผ่นป้ายรูปสี่เหลี่ยมผืนผ้ากว้าง {w} ซม. ยาว {length} ซม. ถูกตัดมุมออกเป็น"
                      f"รูปสามเหลี่ยมมุมฉากที่มีด้านประกอบมุมฉากยาว {w} ซม. และ {h} ซม. "
                      f"แผ่นป้ายที่เหลือมีพื้นที่กี่ตารางเซนติเมตร")
            wrongs = [rect - w * h, rect + tri, rect]
        else:
            a, b = rng.randint(4, 15), rng.randint(4, 15)
            ans = w * length + a * b
            prompt = (f"ที่ดินรูปตัวแอลแบ่งได้เป็นรูปสี่เหลี่ยมผืนผ้าสองรูป รูปหนึ่งกว้าง {w} ม. ยาว {length} ม. "
                      f"อีกรูปกว้าง {a} ม. ยาว {b} ม. ที่ดินมีพื้นที่กี่ตารางเมตร")
            wrongs = [(w + a) * (length + b), w * length, 2 * (w + length + a + b)]
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=_story.keep(*wrongs, ans + 10, answer=ans, lo=1))


@question_type("math.triangle_area_word_p6", display_name={"th": "โจทย์ปัญหาพื้นที่รูปสามเหลี่ยม"},
               level={"th": "ป.6"}, topic="พื้นที่รูปสามเหลี่ยม")
class TriangleAreaWordP6(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        b, h = rng.randint(4, 20), rng.randrange(4, 21, 2)
        area = b * h // 2
        kind = rng.randrange(3)
        if kind == 0:
            price = rng.choice((20, 25, 50, 100))
            cost = area * price
            stem = (f"สนามหญ้ารูปสามเหลี่ยมมีฐานยาว {b} เมตร สูง {h} เมตร ปูหญ้าตารางเมตรละ {price} บาท "
                    f"ต้องจ่ายค่าหญ้ากี่บาท")
            return maths([text(stem)], _n(cost), _nums(cost, b * h * price, area, (b + h) * price, lo=1), self.topic)
        if kind == 1:
            flags = rng.randint(3, 12)
            total = area * flags
            stem = f"ธงรูปสามเหลี่ยมมีฐานยาว {b} เซนติเมตร สูง {h} เซนติเมตร ทำธง {flags} ผืน ใช้ผ้ากี่ตารางเซนติเมตร"
            return maths([text(stem)], _n(total), _nums(total, b * h * flags, area, area + flags, lo=1), self.topic)
        stem = (f"จั่วหลังคารูปสามเหลี่ยมมีพื้นที่ {area} ตารางเมตร ฐานยาว {b} เมตร จั่วนี้สูงกี่เมตร")
        return maths([text(stem)], str(h), _nums(h, area // b if area % b == 0 else h + 2, h // 2 or h + 1, b,
                                                 lo=1), self.topic)


@question_type("math.composite_area_figure_p6",
               display_name={"th": "หาพื้นที่และความยาวรอบรูปของรูปหลายเหลี่ยมจากรูป"},
               level={"th": "ป.6"}, topic="พื้นที่รูปสามเหลี่ยม")
class CompositeAreaFigureP6(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        f = rng.choice(L_FIGURES)
        w, h, cw, ch = f.dims
        if rng.random() < 0.6:
            ans = w * h - cw * ch
            ask = "รูปนี้มีพื้นที่กี่ตารางเซนติเมตร"
            # The whole rectangle, the notch added instead of removed.
            wrongs = _nums_math_diagrams(w * h, w * h + cw * ch, (w - cw) * (h - ch), answer=ans, lo=1)
        else:
            ans = 2 * (w + h)
            ask = "รูปนี้ยาวรอบรูปกี่เซนติเมตร"
            # The notch's two edges left out.
            wrongs = _nums_math_diagrams(2 * (w + h) - cw - ch, 2 * (w + h) + cw + ch, w + h, answer=ans, lo=1)
        return _math_q([text(ask), _img(f.asset_id, figure_alt(f))], str(ans), wrongs, self.topic)


from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import as_mixed  # noqa: E402
from otk.sets._support.math_p6 import LEVEL  # noqa: E402


def _g6(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk6(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g6(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _d6(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk6(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_d6(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


def _fk6(*values: Fraction, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer and non-positive values left out."""
    out: list[str] = []
    for v in values:
        if v > 0 and v != answer and as_mixed(v) not in out:
            out.append(as_mixed(v))
    return out


# ── More triangle areas (2026-11): a right triangle from its two short sides, the largest of four, a
# rectangle with a triangle cut out, and two triangles on one base ──


@question_type("math.right_triangle_area_p6", display_name={"th": "พื้นที่รูปสามเหลี่ยมมุมฉาก"},
               level=LEVEL, topic="พื้นที่รูปสามเหลี่ยม")
class RightTriangleAreaP6(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(2, 15) * 2
        b = rng.randint(3, 30)
        right = a * b // 2
        prompt = (f"รูปสามเหลี่ยมมุมฉากมีด้านประกอบมุมฉากยาว {a} และ {b} เซนติเมตร "
                  "มีพื้นที่กี่ตารางเซนติเมตร")
        # Not halved; the sides added; the sides added and doubled.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a * b, a + b, 2 * (a + b), right + a, answer=right, lo=1))


@question_type("math.largest_triangle_area_p6", display_name={"th": "รูปสามเหลี่ยมใดมีพื้นที่มากที่สุด"},
               level=LEVEL, topic="พื้นที่รูปสามเหลี่ยม")
class LargestTriangleAreaP6(ChoiceType):
    def compose(self, rng: Random):
        while True:
            dims = [(rng.randint(2, 10) * 2, rng.randint(3, 20)) for _ in range(4)]
            areas = [b * h // 2 for b, h in dims]
            if len(set(areas)) == 4:
                break
        texts = [f"ฐาน {b} ซม. สูง {h} ซม." for b, h in dims]
        most = rng.random() < 0.5
        pick = areas.index(max(areas) if most else min(areas))
        return (f"รูปสามเหลี่ยมใดมีพื้นที่{'มากที่สุด' if most else 'น้อยที่สุด'}", texts[pick],
                [t for i, t in enumerate(texts) if i != pick])


@question_type("math.rectangle_minus_triangle_p6", display_name={"th": "พื้นที่ที่เหลือเมื่อตัดรูปสามเหลี่ยมออก"},
               level=LEVEL, topic="พื้นที่รูปสามเหลี่ยม")
class RectangleMinusTriangleP6(WordProblem):
    def expr(self, rng: Random):
        w = rng.randint(6, 30)
        h = rng.randint(2, 15) * 2
        base = rng.randint(2, w - 2)
        tri = base * h // 2
        right = w * h - tri
        prompt = (f"แผ่นกระดาษรูปสี่เหลี่ยมผืนผ้ากว้าง {h} ซม. ยาว {w} ซม. ตัดรูปสามเหลี่ยมที่มีฐาน {base} ซม. "
                  f"และสูง {h} ซม. ออก เหลือพื้นที่กี่ตารางเซนติเมตร")
        # The triangle not halved; the triangle alone; the whole sheet.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(w * h - base * h, tri, w * h, w * h + tri, answer=right, lo=1))


@question_type("math.two_triangles_one_base_p6", display_name={"th": "รูปสามเหลี่ยมสองรูปที่มีฐานร่วมกัน"},
               level=LEVEL, topic="พื้นที่รูปสามเหลี่ยม")
class TwoTrianglesOneBaseP6(WordProblem):
    def expr(self, rng: Random):
        base = rng.randint(2, 15) * 2
        h1, h2 = sorted(rng.sample(range(3, 30), 2))
        right = base * (h2 - h1) // 2
        prompt = (f"รูปสามเหลี่ยมสองรูปมีฐานเดียวกันยาว {base} เซนติเมตร รูปแรกสูง {h1} เซนติเมตร "
                  f"รูปที่สองสูง {h2} เซนติเมตร รูปที่สองมีพื้นที่มากกว่ารูปแรกกี่ตารางเซนติเมตร")
        # Not halved; the heights' difference; both areas added.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(base * (h2 - h1), h2 - h1, base * (h1 + h2) // 2, right + base,
                                                answer=right, lo=1))
