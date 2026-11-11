"""การบวกและการลบ

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.4/8

Sets moved here from: math_gaps_primary.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.sets._support.math_gaps_primary import _AddSubLarge, _AddSubWordLarge, _MissingAddSubLarge

PROVENANCE = Provenance("original")


@question_type("math.add_sub_large_p4", display_name={"th": "บวกและลบจำนวนนับที่มากกว่า 100,000"},
               level={"th": "ป.4"}, topic="การบวกและการลบ")
class AddSubLargeP4(_AddSubLarge):
    lo, hi = 100_000, 9_000_000


@question_type("math.missing_addsub_large_p4",
               display_name={"th": "หาตัวไม่ทราบค่าในประโยคการบวกและการลบ (มากกว่า 100,000)"},
               level={"th": "ป.4"}, topic="การบวกและการลบ")
class MissingAddSubLargeP4(_MissingAddSubLarge):
    lo, hi = 100_000, 9_000_000


@question_type("math.addsub_word_large_p4",
               display_name={"th": "โจทย์ปัญหาการบวกและการลบ (มากกว่า 100,000)"},
               level={"th": "ป.4"}, topic="การบวกและการลบ")
class AddSubWordLargeP4(_AddSubWordLarge):
    lo, hi = 100_000, 9_000_000


# ── More adding and subtracting (2026-11): three six-digit numbers, checking with the opposite operation,
# how many more, a missing digit, the largest result, a budget after two costs, and two sums compared ──
from random import Random  # noqa: E402

from otk.core.registry import question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import LEVEL  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _p4_no_carry(a: int, b: int) -> int:
    out, place = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * place
        a, b, place = a // 10, b // 10, place * 10
    return out


@question_type("math.add_three_large_p4", display_name={"th": "บวกจำนวนหกหลักสามจำนวน"},
               level=LEVEL, topic="การบวกและการลบ")
class AddThreeLargeP4(MathType):
    def expr(self, rng: Random):
        a, b, c = (rng.randint(100_000, 999_999) for _ in range(3))
        right = a + b + c
        return MathDraw(f"{_g(a)} + {_g(b)} + {_g(c)}", _g(right), prompt="จงหาผลบวก",
                        distractors=_gk(a + b, _p4_no_carry(_p4_no_carry(a, b), c), right + 100_000, right - 1_000,
                                        answer=right, lo=1))


@question_type("math.check_addsub_p4", display_name={"th": "ตรวจคำตอบการบวกและการลบ (มากกว่า 100,000)"},
               level=LEVEL, topic="การบวกและการลบ")
class CheckAddSubP4(ChoiceType):
    def compose(self, rng: Random):
        a = rng.randint(2_000_000, 9_000_000)
        b = rng.randint(100_000, a - 500_000)
        d = a - b
        if rng.random() < 0.5:
            return (f"ข้อใดใช้ตรวจคำตอบของ {a:,} − {b:,} = {d:,}", f"{d:,} + {b:,} = {a:,}",
                    [f"{a:,} + {b:,} = {a + b:,}", f"{a:,} + {d:,} = {a + d:,}", f"{d:,} + {b:,} = {a + 100_000:,}"])
        return (f"ข้อใดใช้ตรวจคำตอบของ {d:,} + {b:,} = {a:,}", f"{a:,} − {b:,} = {d:,}",
                [f"{a:,} + {b:,} = {a + b:,}", f"{a:,} + {d:,} = {a + d:,}", f"{a:,} − {b:,} = {d + 100_000:,}"])


@question_type("math.how_many_more_p4", display_name={"th": "โจทย์ปัญหามากกว่ากันเท่าใด (มากกว่า 100,000)"},
               level=LEVEL, topic="การบวกและการลบ")
class HowManyMoreP4(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(1_000_000, 9_900_000)
        b = rng.randint(500_000, a - 10_000)
        right = a - b
        x, y = rng.sample(("จังหวัดแรก", "จังหวัดที่สอง"), 2)
        prompt = f"{x}มีประชากร {a:,} คน {y}มีประชากร {b:,} คน {x}มีประชากรมากกว่า{y}กี่คน"
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(a + b, right + 100_000, right - 10_000, right + 1_000, answer=right, lo=1))


@question_type("math.missing_digit_add_p4", display_name={"th": "หาเลขโดดที่หายไปในการบวก (จำนวนหกหลัก)"},
               level=LEVEL, topic="การบวกและการลบ")
class MissingDigitAddP4(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(100_000, 499_999), rng.randint(100_000, 499_999)
        s = a + b
        pos = rng.randrange(6)
        digit = int(str(a)[pos])
        shown = "".join("□" if i == pos else ch for i, ch in enumerate(str(a)))
        prompt = f"{shown} + {b} = {s} เลขโดดใน □ คือเลขใด"
        return MathDraw("", str(digit), prompt=prompt,
                        distractors=_story.keep((digit + 1) % 10, (digit - 1) % 10, int(str(s)[pos]),
                                                int(str(b)[pos]), answer=digit, lo=0, hi=9))


@question_type("math.largest_result_p4", display_name={"th": "ผลบวกหรือผลลบใดมากที่สุด (มากกว่า 100,000)"},
               level=LEVEL, topic="การบวกและการลบ")
class LargestResultP4(ChoiceType):
    def compose(self, rng: Random):
        while True:
            exprs = {}
            for _ in range(4):
                a, b = rng.randint(100_000, 900_000), rng.randint(100_000, 900_000)
                if rng.random() < 0.5:
                    exprs[f"{a:,} + {b:,}"] = a + b
                else:
                    exprs[f"{a + b:,} − {b:,}"] = a
            if len(exprs) == 4 and len(set(exprs.values())) == 4:
                break
        most = rng.random() < 0.5
        right = (max if most else min)(exprs, key=exprs.get)
        return f"ข้อใดมีผลลัพธ์{'มากที่สุด' if most else 'น้อยที่สุด'}", right, [e for e in exprs if e != right]


@question_type("math.budget_left_p4", display_name={"th": "งบประมาณเหลือเท่าใด"},
               level=LEVEL, topic="การบวกและการลบ")
class BudgetLeftP4(WordProblem):
    def expr(self, rng: Random):
        budget = rng.choice((1_000_000, 2_500_000, 5_000_000))
        a = rng.randint(budget // 10, budget // 2) // 100 * 100
        b = rng.randint(budget // 10, budget - a - 10_000) // 100 * 100
        right = budget - a - b
        x, y = rng.sample(("ซ่อมถนน", "สร้างห้องสมุด", "ซื้อคอมพิวเตอร์", "ปลูกต้นไม้", "ทาสีอาคาร"), 2)
        prompt = f"หมู่บ้านได้งบประมาณ {budget:,} บาท ใช้{x} {a:,} บาท และ{y} {b:,} บาท เหลืองบประมาณกี่บาท"
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(budget - a, budget - b, a + b, budget - a + b, answer=right, lo=1))


@question_type("math.compare_two_sums_p4", display_name={"th": "ผลรวมสองชุดต่างกันเท่าใด (มากกว่า 100,000)"},
               level=LEVEL, topic="การบวกและการลบ")
class CompareTwoSumsP4(WordProblem):
    def expr(self, rng: Random):
        while True:
            a, b, c, d = (rng.randint(100_000, 900_000) for _ in range(4))
            if a + b != c + d:
                break
        if a + b < c + d:
            a, b, c, d = c, d, a, b
        right = (a + b) - (c + d)
        prompt = (f"บริษัทแรกมีรายได้สองเดือน {a:,} บาท และ {b:,} บาท บริษัทที่สองมีรายได้ {c:,} บาท และ {d:,} บาท "
                  f"บริษัทแรกมีรายได้รวมมากกว่ากี่บาท")
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(abs(a - c), a + b + c + d, right + 100_000, abs(b - d) + 1, answer=right, lo=1))
