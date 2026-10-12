"""การบวก

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.1/4

Sets moved here from: math, math_apply_stage, math_pictures.
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
from otk.sets._support.math_pictures import BY_KEY, HIDDEN, JOINED, LEVEL, _img, _near

PROVENANCE = Provenance("original")


@question_type("math.one_digit_plus_no_carry",
               display_name={"th": "บวกเลข 1 หลัก (ไม่ทด)"}, level={"th": "ป.1"}, topic="การบวก")
class OneDigitPlusNoCarry(MathType):
    def expr(self, rng: Random, lo: int = 2, hi: int = 9):
        answer = rng.randint(lo, hi)
        a = rng.randint(1, answer - 1)
        b = answer - a
        return rf"{a} + {b}", rf"{a + b}"


@question_type("math.add_pictures_p1", display_name={"th": "การบวกจากภาพ"},
               level=LEVEL, topic="การบวก")
class AddPicturesP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        j = rng.choice(JOINED)
        kind = BY_KEY[j.kind]
        img = _img(j.asset_id, [j.kind])
        total = j.a + j.b
        if rng.random() < 0.5:
            return _math_q([text(f"{kind.thai}สองกลุ่มรวมกันมีกี่{kind.unit}"), img],
                           str(total), _near(total, abs(j.a - j.b), lo=1), self.topic)
        correct = f"{j.a} + {j.b} = {total}"
        wrongs = [f"{j.a} + {j.b} = {total + 1}", f"{max(j.a, j.b)} - {min(j.a, j.b)} = {abs(j.a - j.b)}",
                  f"{j.a} + {total} = {j.a + total}", f"{j.a} + {j.b} = {total - 1}"]
        return _math_q([text("ประโยคสัญลักษณ์ใดตรงกับภาพ"), img], correct, wrongs, self.topic)


@question_type("math.one_digit_plus_with_carry",
               display_name={"th": "บวกเลข 1 หลัก (ทด)"}, level={"th": "ป.1"}, topic="การบวก")
class OneDigitPlusWithCarry(MathType):
    def expr(self, rng: Random, lo: int = 1, hi: int = 9):
        a = rng.randint(lo, hi) 
        b = rng.randint(10 - a, hi) 
        return rf"{a} + {b}", rf"{a + b}"


@question_type("math.part_whole_p1", display_name={"th": "ส่วนย่อยและส่วนรวม"},
               level=LEVEL, topic="การบวก")
class PartWholeP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        h = rng.choice(HIDDEN)
        kind = BY_KEY[h.kind]
        shown = h.total - h.inside
        # Adding what is shown to the total; answering with the part that is shown.
        return _math_q([text(f"มี{kind.thai}ทั้งหมด {h.total} {kind.unit} "
                             f"บาง{kind.unit}อยู่ในกล่อง ในกล่องมี{kind.thai}กี่{kind.unit}"),
                        _img(h.asset_id, [h.kind])],
                       str(h.inside), _near(h.inside, h.total + shown, shown, h.total, lo=1),
                       self.topic)


@question_type("math.two_digit_plus",
               display_name={"th": "บวกเลข 2 หลัก"}, level={"th": "ป.1"}, topic="การบวก")
class TwoDigitPlus(MathType):
    def expr(self, rng: Random, lo: int = 20, hi: int = 50):
        answer = rng.randint(lo, hi)
        a = rng.randint(10, answer - 9)
        b = answer - a
        return rf"{a} + {b}", rf"{a + b}"


@question_type("math.missing_addend",
               display_name={"th": "หาจำนวนที่หายไป (การบวก)"}, level={"th": "ป.1"},
               topic="การบวก")
class MissingAddend(MathType):
    def expr(self, rng: Random, a_hi: int = 90, sum_hi: int = 100):
        a = rng.randint(1, a_hi)
        b = rng.randint(1, sum_hi - a)
        return MathDraw(rf"{a} + \square = {a + b}", rf"{b}",
                        prompt="จงหาจำนวนที่หายไป",
                        distractors=[str(b + 1), str(b - 1), str(a)])


@question_type("math.add_word_p1", display_name={"th": "โจทย์ปัญหาการบวกในชีวิตประจำวัน"},
               level={"th": "ป.1"}, topic="การบวก")
class AddWordP1(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = rng.randint(10, 60), rng.randint(3, 35)
        who, other = _story.names(rng)
        thing, unit = rng.choice(_P1_THINGS)
        stem = rng.choice((
            f"{who}มี{thing} {a} {unit} {rng.choice(_story.GIVERS)}ให้อีก {b} {unit} {who}มี{thing}ทั้งหมดกี่{unit}",
            f"ในสวนมีต้นมะม่วง {a} ต้น และต้นมะพร้าว {b} ต้น ในสวนมีต้นไม้ทั้งหมดกี่ต้น",
            f"{who}มี{thing} {a} {unit} {other}มี{thing}มากกว่า{who} {b} {unit} {other}มี{thing}กี่{unit}",
        ))
        total = a + b
        # Taking away, off by one ten, and off by one.
        return maths([text(stem)], str(total), _nums(total, a - b, total + 10, total - 10, total + 1, lo=1),
                     self.topic)
