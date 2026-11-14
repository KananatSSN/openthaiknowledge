"""การลบ

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.1/4

Sets moved here from: math, math_apply_stage, math_p1, math_pictures.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType
from otk.sets._support.math_apply_stage import _P1_THINGS, _nums
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_p1 import LEVEL
from otk.sets._support.math_pictures import BY_KEY, CROSSED, _img, _near

PROVENANCE = Provenance("original")


@question_type("math.one_digit_subtraction",
               display_name={"th": "การลบ 1 หลัก"}, level={"th": "ป.1"}, topic="การลบ")
class OneDigitSubtraction(MathType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def expr(self, rng: Random, lo: int = 2, hi: int = 9):
        a = rng.randint(lo, hi)
        b = rng.randint(1, a)
        return rf"{a} - {b}", rf"{a - b}"


@question_type("math.subtract_pictures_p1", display_name={"th": "การลบจากภาพ"},
               level=LEVEL, topic="การลบ")
class SubtractPicturesP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        c = rng.choice(CROSSED)
        kind = BY_KEY[c.kind]
        img = _img(c.asset_id, [c.kind])
        left = c.total - c.gone
        lead = text(f"{kind.thai}ที่มีเครื่องหมาย ✕ ถูกนำออกไปแล้ว")
        if rng.random() < 0.5:
            # Counting the crossed ones, counting all of them, adding.
            return _math_q([lead, text(f"เหลือ{kind.thai}กี่{kind.unit}"), img],
                           str(left), _near(left, c.gone, c.total, c.total + c.gone, lo=0),
                           self.topic)
        correct = f"{c.total} - {c.gone} = {left}"
        wrongs = [f"{c.total} + {c.gone} = {c.total + c.gone}", f"{c.total} - {c.gone} = {left + 1}",
                  f"{c.total} - {c.gone} = {left - 1}"]
        return _math_q([lead, text("ประโยคสัญลักษณ์ใดตรงกับภาพ"), img], correct, wrongs, self.topic)


@question_type("math.two_digit_subtraction_no_borrow",
               display_name={"th": "การลบ 2 หลัก (ไม่ยืม)"}, level={"th": "ป.1"}, topic="การลบ")
class TowDigitSubtractionNoBorrow(MathType):
    def expr(self, rng: Random, lo: int = 20, hi: int = 99):
        a = rng.randint(lo, hi)
        b0 = rng.randint(0, a % 10)
        b1 = rng.randint(1, a // 10)
        b = 10*b1 + b0
        return rf"{a} - {b}", rf"{a - b}"


@question_type("math.subtract_within_20_p1",
               display_name={"th": "การลบจำนวนไม่เกิน 20 (ข้ามสิบ)"},
               level=LEVEL, topic="การลบ")
class SubtractWithinTwentyP1(MathType):
    """11–18 minus a one-digit number that crosses ten (15 − 8): the step the
    book takes between การลบ 1 หลัก and two-digit subtraction."""

    def expr(self, rng: Random, lo: int = 11, hi: int = 18):
        a = rng.randint(lo, hi)
        b = rng.randint(a % 10 + 1, 9)
        # Adding instead; taking the smaller ones digit from the larger (15 − 8
        # read as 10 + 8 − 5); one off from counting back.
        return MathDraw(rf"{a} - {b}", str(a - b), prompt="จงหาผลลบ",
                        distractors=[str(a + b), str(10 + b - a % 10), str(a - b + 1)])


@question_type("math.two_digit_subtraction_with_borrow",
               display_name={"th": "การลบ 2 หลัก (ยืม)"}, level={"th": "ป.1"}, topic="การลบ")
class TowDigitSubtractionWithBorrow(MathType):
    def expr(self, rng: Random, lo: int = 20, hi: int = 99):
        a0 = rng.randint(0, 8)
        a1 = rng.randint(2, 9)
        a = 10*a1 + a0
        b0 = rng.randint(a0 + 1, 9)
        b1 = rng.randint(1, a1 - 1)
        b = 10*b1 + b0
        return rf"{a} - {b}", rf"{a - b}"


@question_type("math.missing_subtrahend",
               display_name={"th": "หาตัวลบที่หายไป"}, level={"th": "ป.1"},
               topic="การลบ")
class MissingSubtrahend(MathType):
    def expr(self, rng: Random, hi: int = 100):
        a = rng.randint(2, hi)
        b = rng.randint(1, a)
        return MathDraw(rf"{a} - \square = {a - b}", rf"{b}",
                        prompt="จงหาตัวลบที่หายไป",
                        distractors=[str(a - b), str(b + 1), str(b - 1)])


@question_type("math.subtract_word_p1", display_name={"th": "โจทย์ปัญหาการลบในชีวิตประจำวัน"},
               level={"th": "ป.1"}, topic="การลบ")
class SubtractWordP1(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a = rng.randint(25, 99)
        b = rng.randint(4, a - 5)
        who, other = _story.names(rng)
        thing, unit = rng.choice(_P1_THINGS)
        stem = rng.choice((
            f"{who}มี{thing} {a} {unit} ให้เพื่อนไป {b} {unit} {who}เหลือ{thing}กี่{unit}",
            f"{who}มี{thing} {a} {unit} {other}มี{thing} {b} {unit} {who}มีมากกว่า{other}กี่{unit}",
            f"ในห้องมีนักเรียน {a} คน เป็นนักเรียนหญิง {b} คน เป็นนักเรียนชายกี่คน",
        ))
        left = a - b
        return maths([text(stem)], str(left), _nums(left, a + b, left + 10, left - 10, left + 1, lo=1),
                     self.topic)


# ── More subtraction (2026-11): whole tens, subtraction that undoes an addition, hopping back on a
# number line ──

from otk.kit.math_problems import WordProblem  # noqa: E402


@question_type("math.subtract_tens_p1", display_name={"th": "ลบจำนวนเต็มสิบ"},
               level=LEVEL, topic="การลบ")
class SubtractTensP1(MathType):
    def expr(self, rng: Random):
        a = rng.randint(2, 9)
        b = rng.randint(1, a - 1)
        right = 10 * (a - b)
        # The tens digits alone; added instead; ten off.
        return MathDraw(f"{10 * a} - {10 * b}", str(right), prompt="จงหาผลลบ",
                        distractors=_story.keep(a - b, 10 * (a + b), right + 10, right - 10,
                                                answer=right, lo=1, hi=100))


@question_type("math.add_sub_inverse_p1", display_name={"th": "ความสัมพันธ์ของการบวกและการลบ"},
               level=LEVEL, topic="การลบ")
class AddSubInverseP1(MathType):
    def expr(self, rng: Random):
        a, b = rng.sample(range(2, 30), 2)
        s = a + b
        # The number taken away; the total; the total plus.
        return MathDraw(rf"{s} - {b} = \square", str(a),
                        prompt=f"ถ้า {a} + {b} = {s} จำนวนใดเติมใน □ แล้วทำให้ประโยคเป็นจริง",
                        distractors=_story.keep(b, s, s + b, a + 1, answer=a, lo=0))


@question_type("math.number_line_back_p1", display_name={"th": "นับถอยหลังบนเส้นจำนวน"},
               level=LEVEL, topic="การลบ")
class NumberLineBackP1(WordProblem):
    def expr(self, rng: Random):
        start = rng.randint(8, 30)
        hop = rng.randint(2, 9)
        right = start - hop
        prompt = f"บนเส้นจำนวน เริ่มที่ {start} แล้วนับถอยหลังไป {hop} ช่อง จะอยู่ที่จำนวนใด"
        # Counted forward instead; one hop short or long.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(start + hop, right + 1, right - 1, hop, answer=right, lo=0))
