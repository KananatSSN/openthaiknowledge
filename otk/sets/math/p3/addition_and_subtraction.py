"""การบวกและการลบ

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.3/5

Sets moved here from: math_gaps_primary.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.sets._support.math_gaps_primary import _AddSubLarge, _AddSubWordLarge, _MissingAddSubLarge

PROVENANCE = Provenance("original")


@question_type("math.add_sub_large_p3", display_name={"th": "บวกและลบจำนวนไม่เกิน 100,000"},
               level={"th": "ป.3"}, topic="การบวกและการลบ")
class AddSubLargeP3(_AddSubLarge):
    lo, hi = 1_000, 100_000


@question_type("math.missing_addsub_large_p3",
               display_name={"th": "หาตัวไม่ทราบค่าในประโยคการบวกและการลบ (ไม่เกิน 100,000)"},
               level={"th": "ป.3"}, topic="การบวกและการลบ")
class MissingAddSubLargeP3(_MissingAddSubLarge):
    lo, hi = 1_000, 100_000


@question_type("math.addsub_word_large_p3",
               display_name={"th": "โจทย์ปัญหาการบวกและการลบ (ไม่เกิน 100,000)"},
               level={"th": "ป.3"}, topic="การบวกและการลบ")
class AddSubWordLargeP3(_AddSubWordLarge):
    lo, hi = 1_000, 100_000


# ── More adding and subtracting (2026-11): three four-digit numbers, checking with the opposite operation,
# how many more, a missing digit, the largest result, money left after two buys, and two sums compared ──
from random import Random  # noqa: E402

from otk.core.registry import question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p3 import LEVEL  # noqa: E402


def _p3_no_carry(a: int, b: int) -> int:
    out, place = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * place
        a, b, place = a // 10, b // 10, place * 10
    return out


@question_type("math.add_three_four_digit_p3", display_name={"th": "บวกจำนวนสี่หลักสามจำนวน"},
               level=LEVEL, topic="การบวกและการลบ")
class AddThreeFourDigitP3(MathType):
    def expr(self, rng: Random):
        a, b, c = (rng.randint(1000, 9999) for _ in range(3))
        right = a + b + c
        # Only two added; carries dropped; a thousand off.
        return MathDraw(f"{a} + {b} + {c}", str(right), prompt="จงหาผลบวก",
                        distractors=_story.keep(a + b, _p3_no_carry(_p3_no_carry(a, b), c), right + 1000,
                                                right - 100, answer=right, lo=1))


@question_type("math.check_addsub_p3", display_name={"th": "ตรวจคำตอบการบวกและการลบ (ไม่เกิน 100,000)"},
               level=LEVEL, topic="การบวกและการลบ")
class CheckAddSubP3(ChoiceType):
    def compose(self, rng: Random):
        a = rng.randint(20000, 90000)
        b = rng.randint(1000, a - 5000)
        d = a - b
        if rng.random() < 0.5:
            return (f"ข้อใดใช้ตรวจคำตอบของ {a} − {b} = {d}", f"{d} + {b} = {a}",
                    [f"{a} + {b} = {a + b}", f"{a} + {d} = {a + d}", f"{d} + {b} = {a + 1000}"])
        return (f"ข้อใดใช้ตรวจคำตอบของ {d} + {b} = {a}", f"{a} − {b} = {d}",
                [f"{a} + {b} = {a + b}", f"{a} + {d} = {a + d}", f"{a} − {b} = {d + 1000}"])


@question_type("math.how_many_more_p3", display_name={"th": "โจทย์ปัญหามากกว่ากันเท่าใด (ไม่เกิน 100,000)"},
               level=LEVEL, topic="การบวกและการลบ")
class HowManyMoreP3(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(20000, 99000)
        b = rng.randint(10000, a - 1000)
        right = a - b
        what, unit = rng.choice((("ผู้ชมฟุตบอล", "คน"), ("ต้นกล้า", "ต้น"), ("ขวดพลาสติก", "ขวด")))
        x, y = rng.sample(("ปีที่แล้ว", "ปีนี้", "เดือนที่แล้ว", "เดือนนี้"), 2)
        prompt = f"{x}มี{what} {a} {unit} {y}มี {b} {unit} {x}มีมากกว่า{y}กี่{unit}"
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a + b, right + 1000, right - 100, right + 10, answer=right, lo=1))


@question_type("math.missing_digit_add_p3", display_name={"th": "หาเลขโดดที่หายไปในการบวก"},
               level=LEVEL, topic="การบวกและการลบ")
class MissingDigitAddP3(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(1000, 4999), rng.randint(1000, 4999)
        s = a + b
        pos = rng.randrange(4)
        digit = int(str(a)[pos])
        shown = "".join("□" if i == pos else ch for i, ch in enumerate(str(a)))
        prompt = f"{shown} + {b} = {s} เลขโดดใน □ คือเลขใด"
        # A neighbouring digit; the sum's digit in that place; the other number's digit there.
        return MathDraw("", str(digit), prompt=prompt,
                        distractors=_story.keep((digit + 1) % 10, (digit - 1) % 10, int(str(s)[-4 + pos]),
                                                int(str(b)[pos]), answer=digit, lo=0, hi=9))


@question_type("math.largest_result_p3", display_name={"th": "ผลบวกหรือผลลบใดมากที่สุด (ไม่เกิน 100,000)"},
               level=LEVEL, topic="การบวกและการลบ")
class LargestResultP3(ChoiceType):
    def compose(self, rng: Random):
        while True:
            exprs = {}
            for _ in range(4):
                a, b = rng.randint(10000, 50000), rng.randint(1000, 40000)
                if rng.random() < 0.5:
                    exprs[f"{a} + {b}"] = a + b
                else:
                    exprs[f"{a + b} − {b}"] = a
            if len(exprs) == 4 and len(set(exprs.values())) == 4:
                break
        most = rng.random() < 0.5
        right = (max if most else min)(exprs, key=exprs.get)
        return f"ข้อใดมีผลลัพธ์{'มากที่สุด' if most else 'น้อยที่สุด'}", right, [e for e in exprs if e != right]


@question_type("math.money_left_two_buys_p3", display_name={"th": "ซื้อของสองอย่างแล้วเหลือเงินเท่าใด"},
               level=LEVEL, topic="การบวกและการลบ")
class MoneyLeftTwoBuysP3(WordProblem):
    def expr(self, rng: Random):
        have = rng.choice((5000, 10000, 20000))
        a = rng.randint(have // 10, have // 2)
        b = rng.randint(have // 10, have - a - 100)
        right = have - a - b
        x, y = rng.sample(("พัดลม", "หม้อหุงข้าว", "จักรยาน", "โต๊ะ", "เก้าอี้", "ตู้หนังสือ"), 2)
        prompt = f"พ่อมีเงิน {have} บาท ซื้อ{x}ราคา {a} บาท และ{y}ราคา {b} บาท พ่อเหลือเงินกี่บาท"
        # Only one taken off; the two added on; the total spent.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(have - a, have - b, a + b, have - a + b, answer=right, lo=1))


@question_type("math.compare_two_sums_p3", display_name={"th": "ผลบวกสองชุดต่างกันเท่าใด"},
               level=LEVEL, topic="การบวกและการลบ")
class CompareTwoSumsP3(WordProblem):
    def expr(self, rng: Random):
        while True:
            a, b, c, d = (rng.randint(1000, 9000) for _ in range(4))
            if a + b != c + d:
                break
        if a + b < c + d:
            a, b, c, d = c, d, a, b
        right = (a + b) - (c + d)
        x, y = rng.sample(("ร้านแรก", "ร้านที่สอง"), 2)
        prompt = (f"สัปดาห์นี้{x}ขายได้ {a} บาท และ {b} บาท ส่วน{y}ขายได้ {c} บาท และ {d} บาท "
                  f"{x}ขายได้มากกว่า{y}กี่บาท")
        # One pair compared; everything added; a thousand off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(abs(a - c), a + b + c + d, right + 1000, abs(b - d) + 1,
                                                answer=right, lo=1))
