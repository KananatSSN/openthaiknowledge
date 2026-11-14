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


# ── More adding and subtracting (2026-11): three-digit stories both ways, checking with the opposite
# operation, three two-digit numbers, the largest sum, and how many more ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p2 import LEVEL  # noqa: E402


def _no_carry(a: int, b: int) -> int:
    """a + b with every carry dropped: 368 + 457 -> 715."""
    out, place = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * place
        a, b, place = a // 10, b // 10, place * 10
    return out


def _no_borrow(a: int, b: int) -> int:
    """a − b taking the smaller digit from the larger in each place: 523 − 278 -> 355."""
    out, place = 0, 1
    while a or b:
        out += abs(a % 10 - b % 10) * place
        a, b, place = a // 10, b // 10, place * 10
    return out


@question_type("math.add_word_three_digit_p2", display_name={"th": "โจทย์ปัญหาการบวกจำนวนสามหลัก"},
               level=LEVEL, topic="การบวกและการลบ")
class AddWordThreeDigitP2(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(120, 600)
        b = rng.randint(100, 999 - a)
        right = a + b
        place = rng.choice(("ห้องสมุด", "โรงเรียน", "สวนสัตว์", "ร้านหนังสือ"))
        what, unit = rng.choice((("หนังสือ", "เล่ม"), ("นักเรียน", "คน"), ("ผู้เข้าชม", "คน")))
        prompt = f"{place}มี{what} {a} {unit} มีเพิ่มมาอีก {b} {unit} รวมมี{what}ทั้งหมดกี่{unit}"
        # Every carry dropped; subtracted instead; a hundred off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(_no_carry(a, b), a - b if a > b else b - a, right + 100,
                                                right - 10, answer=right, lo=1))


@question_type("math.sub_word_three_digit_p2", display_name={"th": "โจทย์ปัญหาการลบจำนวนสามหลัก"},
               level=LEVEL, topic="การบวกและการลบ")
class SubWordThreeDigitP2(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(300, 999)
        b = rng.randint(101, a - 50)
        right = a - b
        thing, unit = rng.choice((("ไข่ไก่", "ฟอง"), ("ส้ม", "ผล"), ("ขนมปัง", "ชิ้น"), ("น้ำดื่ม", "ขวด")))
        prompt = f"ร้านค้ามี{thing} {a} {unit} ขายไป {b} {unit} เหลือ{thing}กี่{unit}"
        # The smaller digit from the larger everywhere; added instead; ten off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(_no_borrow(a, b), a + b, right + 10, right - 10,
                                                answer=right, lo=1))


@question_type("math.check_with_inverse_p2", display_name={"th": "ตรวจคำตอบการบวกและการลบ"},
               level=LEVEL, topic="การบวกและการลบ")
class CheckWithInverseP2(ChoiceType):
    def compose(self, rng: Random):
        a = rng.randint(300, 900)
        b = rng.randint(100, a - 100)
        d = a - b
        # Wrong choices: sums that use the same numbers but check nothing, and the check with a wrong total.
        if rng.random() < 0.5:
            stem = f"ข้อใดใช้ตรวจคำตอบของ {a} − {b} = {d}"
            right = f"{d} + {b} = {a}"
            wrongs = [f"{a} + {b} = {a + b}", f"{a} + {d} = {a + d}", f"{d} + {b} = {a + 10}"]
        else:
            stem = f"ข้อใดใช้ตรวจคำตอบของ {d} + {b} = {a}"
            right = f"{a} − {b} = {d}"
            wrongs = [f"{a} + {b} = {a + b}", f"{a} + {d} = {a + d}", f"{a} − {b} = {d + 10}"]
        return stem, right, wrongs


@question_type("math.add_three_two_digit_p2", display_name={"th": "บวกจำนวนสองหลักสามจำนวน"},
               level=LEVEL, topic="การบวกและการลบ")
class AddThreeTwoDigitP2(MathType):
    def expr(self, rng: Random):
        a, b, c = rng.randint(11, 99), rng.randint(11, 99), rng.randint(11, 99)
        right = a + b + c
        # Only two added; carries dropped; ten off.
        return MathDraw(f"{a} + {b} + {c}", str(right), prompt="จงหาผลบวก",
                        distractors=_story.keep(a + b, _no_carry(_no_carry(a, b), c), right + 10, right - 10,
                                                answer=right, lo=1))


@question_type("math.largest_sum_p2", display_name={"th": "ผลบวกหรือผลลบใดมากที่สุด"},
               level=LEVEL, topic="การบวกและการลบ")
class LargestSumP2(ChoiceType):
    def compose(self, rng: Random):
        while True:
            exprs = {}
            for _ in range(4):
                a, b = rng.randint(150, 500), rng.randint(100, 400)
                if rng.random() < 0.5:
                    exprs[f"{a} + {b}"] = a + b
                else:
                    big = a + b
                    exprs[f"{big} − {b}"] = a
            if len(exprs) == 4 and len(set(exprs.values())) == 4:
                break
        most = rng.random() < 0.5
        right = (max if most else min)(exprs, key=exprs.get)
        return f"ข้อใดมีผลลัพธ์{'มากที่สุด' if most else 'น้อยที่สุด'}", right, [e for e in exprs if e != right]


@question_type("math.how_many_more_p2", display_name={"th": "โจทย์ปัญหาเปรียบเทียบมากกว่ากันเท่าใด"},
               level=LEVEL, topic="การบวกและการลบ")
class HowManyMoreP2(WordProblem):
    def expr(self, rng: Random):
        x, y = rng.sample(("ป.1", "ป.2", "ป.3", "ป.4", "ป.5", "ป.6"), 2)
        a = rng.randint(200, 900)
        b = rng.randint(100, a - 20)
        right = a - b
        prompt = (f"นักเรียนชั้น {x} เก็บขวดพลาสติกได้ {a} ขวด ชั้น {y} เก็บได้ {b} ขวด "
                  f"ชั้น {x} เก็บได้มากกว่าชั้น {y} กี่ขวด")
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a + b, _no_borrow(a, b), right + 10, right - 1, answer=right, lo=1))
