"""การบวกและการลบ

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.2/4

Sets moved here from: math, math_formats, math_p2.
"""

from __future__ import annotations

import math
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_p2 import LEVEL

PROVENANCE = Provenance("original")


def _digits_near(d: int) -> list[str]:
    return [str(v % 10) for v in (d + 1, d - 1, d + 2, d - 2)]


@question_type("math.add_columns",
               display_name={"th": "บวกหลายหลัก (มีการทด)"}, level={"th": "ป.2"},
               topic="การบวกและการลบ")
class AddColumns(MathType):
    def expr(self, rng: Random, a_digits: int = 2, b_digits: int = 2, carry: int = 1):
        a_digits = max(1, min(int(a_digits), 4))
        b_digits = max(1, min(int(b_digits), a_digits))
        if carry:
            a_ones = rng.randint(1, 9)
            b_ones = rng.randint(10 - a_ones, 9)
        else:
            a_ones = rng.randint(1 if a_digits == 1 else 0, 8)
            b_ones = rng.randint(1 if b_digits == 1 else 0, 9 - a_ones)

        def num(digits, ones):
            if digits == 1:
                return ones
            return rng.randint(10 ** (digits - 2), 10 ** (digits - 1) - 1) * 10 + ones

        a, b = num(a_digits, a_ones), num(b_digits, b_ones)
        return rf"{a} + {b}", rf"{a + b}"


@question_type("math.sub_columns",
               display_name={"th": "ลบหลายหลัก (มีการยืม)"}, level={"th": "ป.2"},
               topic="การบวกและการลบ")
class SubColumns(MathType):
    def expr(self, rng: Random, a_digits: int = 2, b_digits: int = 2, borrow: int = 1):
        a_digits = max(2, min(int(a_digits), 4))
        b_digits = max(1, min(int(b_digits), a_digits))
        while True:
            if borrow:
                a_ones = rng.randint(0, 8)
                b_ones = rng.randint(a_ones + 1, 9)
            else:
                b_ones = rng.randint(1 if b_digits == 1 else 0, 9)
                a_ones = rng.randint(b_ones, 9)
            if a_digits == b_digits:
                b_head = rng.randint(10 ** (b_digits - 2),
                                     10 ** (b_digits - 1) - (2 if borrow else 1))
                a_head = rng.randint(b_head + (1 if borrow else 0),
                                     10 ** (a_digits - 1) - 1)
            else:
                a_head = rng.randint(10 ** (a_digits - 2), 10 ** (a_digits - 1) - 1)
                b_head = (rng.randint(10 ** (b_digits - 2), 10 ** (b_digits - 1) - 1)
                          if b_digits >= 2 else 0)
            a = a_head * 10 + a_ones
            b = b_head * 10 + b_ones
            if a > b:
                break
        return rf"{a} - {b}", rf"{a - b}"


@question_type("math.missing_digit_p2", display_name={"th": "หาเลขโดดที่หายไปในการบวกและการลบ"},
               level={"th": "ป.2"}, topic="การบวกและการลบ")
class MissingDigitP2(QuestionType):
    """``4□7 + 285 = 762``: one digit hidden, in a column that carries or
    borrows, so reading the column alone is one off."""

    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            a = rng.randint(120, 699)
            b = rng.randint(105, 999 - a)
            if (a % 10 + b % 10 >= 10) or (a // 10 % 10 + b // 10 % 10 >= 10):
                break
        add = rng.random() < 0.5
        # a + b = c, shown either as it is or as c − b = a.
        terms = [a, b, a + b] if add else [a + b, b, a]
        which = rng.randrange(3)
        place = rng.choice((1, 10)) if which != 2 or rng.random() < 0.5 else 100
        number = terms[which]
        digit = number // place % 10
        shown = []
        for i, n in enumerate(terms):
            s = str(n)
            if i == which:
                k = len(s) - 1 - int(math.log10(place))
                s = s[:k] + r"\square " + s[k + 1:]
            shown.append(s)
        op = "+" if add else "-"
        tex = f"{shown[0]} {op} {shown[1]} = {shown[2]}"
        return _math_q([text("จงหาเลขโดดที่แทน □"), content_math(tex)], str(digit),
                       _digits_near(digit), self.topic)


@question_type("math.missing_addsub_p2",
               display_name={"th": "หาตัวไม่ทราบค่าในประโยคสัญลักษณ์การบวกและการลบ"},
               level=LEVEL, topic="การบวกและการลบ")
class MissingAddSubP2(MathType):
    def expr(self, rng: Random, hi: int = 1000):
        hi = max(100, min(int(hi), 1000))
        a = rng.randint(100, hi - 50)
        b = rng.randint(20, hi - a)
        c = a + b
        sq = r"\square"
        form = rng.randrange(4)
        if form == 0:
            tex, x = rf"{a} + {sq} = {c}", b
        elif form == 1:
            tex, x = rf"{sq} + {b} = {c}", a
        elif form == 2:
            tex, x = rf"{c} - {sq} = {a}", b
        else:
            tex, x = rf"{sq} - {b} = {a}", c
        # The box is found by the inverse operation; applying the one written
        # in the sentence is the slip.
        other = (c + a, c + b, c + a, a - b)[form]
        return MathDraw(tex, str(x), prompt="จงหาจำนวนที่แทนใน □",
                        distractors=_story.keep(other, x + 10, x - 10, x + 100,
                                                answer=x, lo=0))
