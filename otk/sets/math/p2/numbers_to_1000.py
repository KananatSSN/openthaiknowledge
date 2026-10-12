"""จำนวนนับไม่เกิน 1,000

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.2/1, ค 1.1 ป.2/2, ค 1.1 ป.2/3

Sets moved here from: math, math_p2, math_pictures_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_p2 import LEVEL, NumberReadingType, _maths
from otk.sets._support.math_pictures import _near
from otk.sets._support.math_pictures_p2 import BLOCKS, P2

PROVENANCE = Provenance("original")


def expanded(n: int) -> str:
    """507 -> 500 + 7 (zero places are left out, as the books write it)."""
    s = str(n)
    parts = [int(d) * 10 ** (len(s) - 1 - i) for i, d in enumerate(s) if d != "0"]
    return " + ".join(str(p) for p in parts)


@question_type("math.skip_counting",
               display_name={"th": "นับเพิ่มทีละ 10 / 100"}, level={"th": "ป.2"}, topic="จำนวนนับไม่เกิน 1,000")
class SkipCounting(MathType):
    def expr(self, rng: Random):
        step = rng.choice([10, 100])
        n = rng.randint(0, 800 // step) * step
        return MathDraw(
            rf"{n},\ {n + step},\ {n + 2 * step},\ \square", rf"{n + 3 * step}",
            prompt=f"นับต่อไปอีกทีละ {step}",
            distractors=[str(n + 2 * step), str(n + 4 * step), str(n + step)])


@question_type("math.number_reading_p2",
               display_name={"th": "อ่านและเขียนจำนวนไม่เกิน 1,000"},
               level=LEVEL, topic="จำนวนนับไม่เกิน 1,000")
class NumberReadingP2(NumberReadingType):
    LO, HI = 100, 1000


@question_type("math.base_ten_blocks_p2", display_name={"th": "อ่านจำนวนจากภาพหลักร้อย หลักสิบ หลักหน่วย"},
               level=P2, topic="จำนวนนับไม่เกิน 1,000")
class BaseTenBlocksP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        b = rng.choice(BLOCKS)
        img = image(b.asset_id, alt="ภาพแผ่นร้อย แท่งสิบ และก้อนหน่วย")
        lead = text("แผ่นใหญ่แทน 100 แท่งยาวแทน 10 ก้อนเล็กแทน 1")
        if rng.random() < 0.6:
            # Dropping a zero (305 read as 35); hundreds and tens swapped;
            # counting every piece as one.
            dropped = int(f"{b.hundreds}{b.tens or ''}{b.ones}")
            swapped = 100 * b.tens + 10 * b.hundreds + b.ones
            pieces = b.hundreds + b.tens + b.ones
            return _math_q([lead, text("ภาพนี้แสดงจำนวนใด"), img], str(b.value),
                           _near(b.value, dropped, swapped, pieces, b.value + 10, lo=1),
                           self.topic)

        def expanded(h: int, t: int, o: int) -> str:
            return " + ".join(str(v) for v in (100 * h, 10 * t, o) if v) or "0"

        correct = expanded(b.hundreds, b.tens, b.ones)
        wrongs = [f"{b.hundreds} + {b.tens} + {b.ones}", expanded(b.tens, b.hundreds, b.ones),
                  expanded(b.hundreds, b.tens + 1, b.ones), expanded(b.hundreds + 1, b.tens, b.ones)]
        return _math_q([lead, text("ภาพนี้เขียนในรูปกระจายได้อย่างไร"), img],
                       correct, wrongs, self.topic)


@question_type("math.place_value_digit",
               display_name={"th": "ค่าประจำหลัก (ตัวเลข)"}, level={"th": "ป.2"},
               topic="จำนวนนับไม่เกิน 1,000")
class PlaceValueDigit(WordProblem):
    _NAMES = {"ร้อย": 100, "สิบ": 10, "หน่วย": 1}

    def expr(self, rng: Random):
        n = rng.randint(100, 999)
        pos = rng.choice(list(self._NAMES))
        digit = (n // self._NAMES[pos]) % 10
        others = [str((n // p) % 10) for p in self._NAMES.values()]
        return MathDraw("", str(digit),
                        prompt=f"เลขในหลัก{pos}ของ {n} คือเลขใด?",
                        distractors=others + ["0"])


@question_type("math.expanded_form_p2",
               display_name={"th": "เขียนจำนวนในรูปกระจาย"},
               level=LEVEL, topic="จำนวนนับไม่เกิน 1,000")
class ExpandedFormP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        h, t, o = rng.randint(1, 9), rng.choice([0, *range(1, 10)]), rng.randint(0, 9)
        if t == o == 0:
            o = rng.randint(1, 9)
        n = 100 * h + 10 * t + o
        # Digits alone, a digit shifted into an empty place, and a place value
        # one step off.
        wrong_forms = [f"{h} + {t} + {o}",
                       f"{h * 100} + {o * 10}" if not t else f"{h * 100} + {t * 100} + {o}",
                       f"{h * 10} + {t * 10} + {o}" if t else f"{h * 10} + {o}",
                       f"{h * 1000} + {t * 10} + {o}"]
        if rng.random() < 0.5:
            return _maths([text("จำนวนนี้เขียนในรูปกระจายได้อย่างไร"), content_math(str(n))],
                          expanded(n),
                          [w for w in dict.fromkeys(wrong_forms) if w != expanded(n)],
                          self.topic)
        # 500 + 7 read as 57 or 570, and the digits simply added.
        wrongs = (_story.keep(int(f"{h}{o}"), int(f"{h}{o}0"), n + 10, n + 100, answer=n)
                  if not t else
                  _story.keep(int(f"{h}{o}{t}"), h + t + o, n + 10, n - 10, answer=n))
        return _maths([text("จำนวนในรูปกระจายนี้คือจำนวนใด"), content_math(expanded(n))],
                      str(n), wrongs, self.topic)


@question_type("math.compare_sign",
               display_name={"th": "เติมเครื่องหมาย <, >, ="}, level={"th": "ป.2"},
               topic="จำนวนนับไม่เกิน 1,000")
class CompareSign(QuestionType):
    @staticmethod
    def _side(rng: Random, n: int) -> str:
        """n as a bare number, in expanded form, or as a sum of two parts."""
        kind = rng.randrange(3)
        if kind == 1 and n >= 10:
            parts = [int(d) * 10 ** i for i, d in enumerate(str(n)[::-1]) if d != "0"]
            return " + ".join(str(p) for p in parts[::-1])
        if kind == 2 and n >= 20:
            first = rng.randint(1, n - 1)
            return f"{first} + {n - first}"
        return str(n)

    def build(self, rng: Random, hi: int = 1000) -> GeneratedQuestion:
        a = rng.randint(0, hi)
        roll = rng.random()
        # Near misses — equal, or the digits of a reordered — are the
        # comparisons that need looking at rather than a glance.
        if roll < 0.2:
            b = a
        elif roll < 0.45 and a >= 100:
            digits = list(str(a))
            rng.shuffle(digits)
            b = int("".join(digits))
        else:
            b = rng.randint(0, hi)
        sign = "<" if a < b else ">" if a > b else "="
        wrong = [s for s in ("<", ">", "=") if s != sign]
        left = self._side(rng, a) if rng.random() < 0.5 else str(a)
        right = str(b) if left != str(a) else self._side(rng, b)
        return GeneratedQuestion(
            stem=[text(f"จงเติมเครื่องหมายที่ถูกต้อง:  {left} ___ {right}")],
            correct=[content_math(sign)],
            distractors=fixed(*[[content_math(s)] for s in wrong]),
            topic=self.topic,
        )


@question_type("math.order_numbers_p2",
               display_name={"th": "เรียงลำดับจำนวนไม่เกิน 1,000"},
               level=LEVEL, topic="จำนวนนับไม่เกิน 1,000")
class OrderNumbersP2(QuestionType):
    def build(self, rng: Random, count: int = 4) -> GeneratedQuestion:
        count = max(3, min(int(count), 5))
        # Same digits in different places make the order worth working out.
        digits = rng.sample(range(1, 10), 3)
        pool = {int(f"{a}{b}{c}") for a in digits for b in digits for c in digits
                if len({a, b, c}) == 3}
        nums = rng.sample(sorted(pool), min(count, len(pool)))
        asc = rng.random() < 0.5
        right = sorted(nums, reverse=not asc)
        # Never show the numbers already in the order asked for.
        while nums == right:
            nums = rng.sample(nums, len(nums))
        fmt = lambda xs: r",\ ".join(map(str, xs))
        by_last = sorted(nums, key=lambda m: (m % 10, m), reverse=not asc)
        swapped = right[:]
        swapped[1], swapped[2] = swapped[2], swapped[1]
        first = right[:]
        first[0], first[1] = first[1], first[0]
        wrongs = [fmt(right[::-1]), fmt(swapped), fmt(by_last), fmt(first), fmt(nums)]
        return _maths([text(f"จงเรียงลำดับ{'จากน้อยไปมาก' if asc else 'จากมากไปน้อย'}"),
                       content_math(fmt(nums))],
                      fmt(right), [w for w in dict.fromkeys(wrongs) if w != fmt(right)],
                      self.topic)
