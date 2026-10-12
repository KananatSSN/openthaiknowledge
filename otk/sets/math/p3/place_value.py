"""ค่าประจำหลัก

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.3/1, ค 1.1 ป.3/2

Sets moved here from: math, math_apply_stage, math_number, math_p3.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_apply_stage import _PlaceValueWord
from otk.sets._support.math_p2 import NumberReadingType, _maths
from otk.sets._support.math_p3 import LEVEL

PROVENANCE = Provenance("original")


@question_type("math.number_reading_p3",
               display_name={"th": "อ่านและเขียนจำนวนไม่เกิน 100,000"},
               level=LEVEL, topic="ค่าประจำหลัก")
class NumberReadingP3(NumberReadingType):
    LO, HI = 1000, 100000


@question_type("math.place_value_expanded",
               display_name={"th": "ค่าประจำหลัก (ค่าของเลข)"}, level={"th": "ป.3"},
               topic="ค่าประจำหลัก")
class PlaceValueExpanded(WordProblem):
    _NAMES = {"หมื่น": 10000, "พัน": 1000, "ร้อย": 100, "สิบ": 10, "หน่วย": 1}

    def expr(self, rng: Random):
        n = rng.randint(10000, 99999)
        pos = rng.choice(list(self._NAMES))
        place = self._NAMES[pos]
        digit = (n // place) % 10
        return MathDraw("", str(digit * place),
                        prompt=f"ค่าของเลขในหลัก{pos}ของ {n} เป็นเท่าใด?",
                        distractors=[str(digit), str(digit * place * 10),
                                     str(digit * (place // 10 or 1))])


@question_type("math.place_value_compose",
               display_name={"th": "ประกอบจำนวนจากค่าประจำหลัก"},
               level={"th": "ป.3"}, topic="ค่าประจำหลัก")
class PlaceValueCompose(MathType):
    """The reverse of expanding: read a sum of place values back as one number."""

    def expr(self, rng: Random, digits_lo: int = 3, digits_hi: int = 4):
        n = rng.randint(digits_lo, digits_hi)
        # No zero digits: every place has to appear in the sum, or the question
        # would silently show fewer terms than the answer has digits.
        ds = [rng.randint(1, 9) for _ in range(n)]
        value = int("".join(str(d) for d in ds))
        parts = [d * 10 ** (n - 1 - i) for i, d in enumerate(ds)]
        return MathDraw(" + ".join(str(p) for p in parts), str(value),
                        prompt="ผลบวกนี้เท่ากับจำนวนใด",
                        distractors=[str(int("".join(str(d) for d in reversed(ds)))),
                                     str(value + 10 ** (n - 1)),
                                     str(sum(ds))])


@question_type("math.place_value_word_p3", display_name={"th": "จำนวนนับไม่เกิน 100,000 ในสถานการณ์"},
               level={"th": "ป.3"}, topic="ค่าประจำหลัก")
class PlaceValueWordP3(_PlaceValueWord):
    lo, hi = 10_000, 99_999
    sentences = ("งานแสดงสินค้ามีผู้เข้าชม {n} คน", "ตำบลแห่งหนึ่งมีประชากร {n} คน",
                 "โครงการปลูกป่าปลูกต้นไม้ได้ {n} ต้น")
    compare = ("จำนวนประชากร", ("ตำบลนาดี", "ตำบลหนองบัว", "ตำบลโคกสูง", "ตำบลบ้านใหม่"))


@question_type("math.order_numbers_p3",
               display_name={"th": "เปรียบเทียบและเรียงลำดับจำนวนไม่เกิน 100,000"},
               level=LEVEL, topic="ค่าประจำหลัก")
class OrderNumbersP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        digits = rng.sample(range(1, 10), 5)
        nums: list[int] = []
        while len(nums) < 4:
            d = digits[:]
            rng.shuffle(d)
            n = int("".join(map(str, d)))
            if n not in nums:
                nums.append(n)
        most = rng.random() < 0.5
        pick = max(nums) if most else min(nums)
        # The number with the largest (smallest) last digit is the glance answer.
        by_ones = (max if most else min)(nums, key=lambda m: m % 10)
        wrongs = [by_ones] + [n for n in nums if n != by_ones]
        return _maths([text(f"จำนวนใด{'มากที่สุด' if most else 'น้อยที่สุด'}")],
                      str(pick), [str(w) for w in dict.fromkeys(wrongs) if w != pick],
                      self.topic)
