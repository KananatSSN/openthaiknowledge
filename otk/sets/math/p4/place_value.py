"""ค่าประจำหลัก

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.4/*

Sets moved here from: math_apply_stage, math_p4.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.math_apply_stage import _PlaceValueWord
from otk.sets._support.math_p2 import NumberReadingType, _maths, _texts
from otk.sets._support.math_p4 import LEVEL, grouped

PROVENANCE = Provenance("original")


def grouped_tex(n: int) -> str:
    """4572318 -> 4{,}572{,}318 (TeX: a comma without the list space)."""
    return f"{n:,}".replace(",", "{,}")


_PV_TOPIC = "ค่าประจำหลัก"


_PLACES = ("หน่วย", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน")


@question_type("math.number_reading_p4",
               display_name={"th": "อ่านและเขียนจำนวนนับที่มากกว่า 100,000"},
               level=LEVEL, topic=_PV_TOPIC)
class NumberReadingP4(NumberReadingType):
    LO, HI = 100_000, 9_999_999


@question_type("math.place_value_millions_p4",
               display_name={"th": "หลักและค่าของเลขโดดในจำนวนหลักล้าน"},
               level=LEVEL, topic=_PV_TOPIC)
class PlaceValueMillionsP4(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        digits = rng.sample(range(1, 10), 7)
        n = int("".join(map(str, digits)))
        pos = rng.randrange(2, 7)
        digit = digits[6 - pos]
        if rng.random() < 0.5:
            wrongs = [f"หลัก{_PLACES[p]}" for p in (pos - 1, pos + 1 if pos < 6 else pos - 2,
                                                     6 - pos if 6 - pos != pos else 0)]
            wrongs.append(f"หลัก{_PLACES[(pos + 3) % 7]}")
            right = f"หลัก{_PLACES[pos]}"
            return _texts([text(f"ในจำนวน {grouped(n)} เลขโดด {digit} อยู่ในหลักใด")], right,
                          [w for w in dict.fromkeys(wrongs) if w != right], self.topic)
        value = digit * 10 ** pos
        wrongs = [digit, digit * 10 ** (pos - 1), digit * 10 ** (pos + 1)]
        return _maths([text(f"ในจำนวน {grouped(n)} เลขโดด {digit} มีค่าเท่าใด")],
                      grouped_tex(value), [grouped_tex(w) for w in wrongs], self.topic)


@question_type("math.place_value_word_p4", display_name={"th": "จำนวนนับที่มากกว่า 100,000 ในสถานการณ์"},
               level={"th": "ป.4"}, topic="ค่าประจำหลัก")
class PlaceValueWordP4(_PlaceValueWord):
    lo, hi = 1_000_000, 9_999_999
    sentences = ("จังหวัดแห่งหนึ่งมีประชากร {n} คน", "ปีที่แล้วมีนักท่องเที่ยว {n} คน",
                 "สหกรณ์ขายข้าวได้ {n} กิโลกรัม")
    compare = ("จำนวนนักท่องเที่ยว", ("จังหวัด ก", "จังหวัด ข", "จังหวัด ค", "จังหวัด ง"))


@question_type("math.compare_large_numbers_p4",
               display_name={"th": "เปรียบเทียบจำนวนหลักแสนและหลักล้าน"},
               level=LEVEL, topic=_PV_TOPIC)
class CompareLargeNumbersP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        # Six- and seven-digit numbers from the same digits: the longest is
        # largest, and among equals the first differing place decides.
        digits = rng.sample(range(0, 10), 7)
        if digits[0] == 0:
            digits[0], digits[1] = digits[1], digits[0]
        nums: list[int] = []
        while len(nums) < 4:
            d = digits[:]
            rng.shuffle(d)
            if d[0] == 0:
                continue
            m = int("".join(map(str, d[: rng.choice((6, 7))])))
            if m not in nums:
                nums.append(m)
        most = rng.random() < 0.5
        pick = (max if most else min)(nums)
        by_lead = (max if most else min)(nums, key=lambda m: str(m)[0])
        wrongs = [by_lead] + [m for m in nums if m != by_lead]
        return _maths([text(f"จำนวนใด{'มากที่สุด' if most else 'น้อยที่สุด'}")],
                      grouped_tex(pick), [grouped_tex(w) for w in dict.fromkeys(wrongs)
                                          if w != pick], self.topic)
