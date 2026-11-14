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


# ── More place value (2026-11): ten thousand, a hundred thousand or a million more or less, the largest or
# smallest number from seven digits, a number between two, zeros in a number read aloud, a number from its
# expanded form, and how many digits ──

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import MathDraw, MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import LEVEL  # noqa: E402
from otk.core.content import text as _text_block  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]
def _join7(ds) -> int:
    return int("".join(map(str, ds)))


@question_type("math.more_less_large_p4", display_name={"th": "มากกว่าหรือน้อยกว่าอยู่ 10,000, 100,000 หรือ 1,000,000"},
               level=LEVEL, topic="ค่าประจำหลัก")
class MoreLessLargeP4(WordProblem):
    def expr(self, rng: Random):
        step = rng.choice((10_000, 100_000, 1_000_000))
        more = rng.random() < 0.5
        n = rng.randint(1_200_000, 8_800_000)
        right = n + step if more else n - step
        others = [s for s in (10_000, 100_000, 1_000_000) if s != step]
        prompt = f"จำนวนที่{'มากกว่า' if more else 'น้อยกว่า'} {n:,} อยู่ {step:,} คือจำนวนใด"
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(n - step if more else n + step, *[n + s if more else n - s for s in others],
                                        answer=right))


@question_type("math.number_from_digits_p4", display_name={"th": "สร้างจำนวนเจ็ดหลักที่มากที่สุดหรือน้อยที่สุด"},
               level=LEVEL, topic="ค่าประจำหลัก")
class NumberFromDigitsP4(WordProblem):
    def expr(self, rng: Random):
        digits = rng.sample(range(10), 7)
        most = rng.random() < 0.5
        big = sorted(digits, reverse=True)
        small = sorted(digits)
        if small[0] == 0:
            small[0], small[1] = small[1], small[0]
        swap = (lambda ds, i, j: _join7([*ds[:i], ds[j], *ds[i + 1:j], ds[i], *ds[j + 1:]]))
        if most:
            right = _join7(big)
            wrongs = [_join7(small), swap(big, 0, 1), swap(big, 5, 6)]
        else:
            right = _join7(small)
            wrongs = [_join7(big), swap(small, 5, 6), swap(small, 2, 3)]
        prompt = (f"ใช้เลขโดด {', '.join(map(str, digits))} หลักละหนึ่งตัว สร้างจำนวนเจ็ดหลักที่"
                  f"{'มากที่สุด' if most else 'น้อยที่สุด'} ได้จำนวนใด")
        return MathDraw("", _g(right), prompt=prompt, distractors=_gk(*wrongs, answer=right, lo=1_000_000))


@question_type("math.number_between_p4", display_name={"th": "จำนวนที่อยู่ระหว่างสองจำนวน (หลักล้าน)"},
               level=LEVEL, topic="ค่าประจำหลัก")
class NumberBetweenP4(QuestionType):
    """Fixed choices: a number from another draw could also lie between the two."""

    def build(self, rng: Random):
        a = rng.randint(1_000_000, 9_000_000)
        b = a + rng.randint(1_000, 9_000)
        right = rng.randint(a + 1, b - 1)
        below, above = a - rng.randint(1, 999), b + rng.randint(1, 999)
        return _fixed_maths([_text_block(f"จำนวนใดอยู่ระหว่าง {a:,} กับ {b:,}")], _g(right),
                            _gk(below, above, b + 100_000, answer=right), self.topic)


@question_type("math.zeros_in_number_p4", display_name={"th": "เขียนจำนวนหลักล้านจากคำอ่านแล้วนับเลข 0"},
               level=LEVEL, topic="ค่าประจำหลัก")
class ZerosInNumberP4(WordProblem):
    def expr(self, rng: Random):
        while True:
            digits = [rng.randint(1, 9)]
            for _ in range(6):
                other = rng.randint(1, 9)
                digits.append(rng.choice((0, 0, other)))
            if 1 <= digits.count(0) <= 5:
                break
        right = digits.count(0)
        prompt = f"จำนวน{_story.thai_words(_join7(digits))} เขียนเป็นตัวเลขฮินดูอารบิกจะมีเลข 0 กี่ตัว"
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right + 1, right - 1, 7 - right, right + 2, answer=right, lo=0, hi=7))


@question_type("math.expanded_to_number_p4", display_name={"th": "เขียนจำนวนจากรูปกระจาย"},
               level=LEVEL, topic="ค่าประจำหลัก")
class ExpandedToNumberP4(MathType):
    def expr(self, rng: Random):
        places = sorted(rng.sample(range(7), 4), reverse=True)
        parts = [rng.randint(1, 9) * 10 ** p for p in places]
        right = sum(parts)
        # Digits written side by side; one place shifted down; one shifted up.
        side = int("".join(str(p // 10 ** pl) for p, pl in zip(parts, places)))
        return MathDraw(" + ".join(_g(p) for p in parts), _g(right), prompt="ผลบวกนี้เท่ากับจำนวนใด",
                        distractors=_gk(side, right - parts[-1] + parts[-1] * 10, right - parts[0] + parts[0] // 10,
                                        right + 10 ** places[1], answer=right, lo=1))


@question_type("math.digit_count_p4", display_name={"th": "จำนวนนี้มีกี่หลัก"},
               level=LEVEL, topic="ค่าประจำหลัก")
class DigitCountP4(WordProblem):
    def expr(self, rng: Random):
        length = rng.randint(5, 8)
        n = rng.randint(10 ** (length - 1), 10 ** length - 1)
        prompt = f"จำนวน{_story.thai_words(n)} เขียนเป็นตัวเลขแล้วมีกี่หลัก"
        return MathDraw("", str(length), prompt=prompt,
                        distractors=_story.keep(length + 1, length - 1, length + 2, length - 2, answer=length, lo=1))
