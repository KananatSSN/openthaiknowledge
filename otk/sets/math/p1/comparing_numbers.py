"""การเปรียบเทียบ

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.1/2, ค 1.1 ป.1/3

Sets moved here from: math, math_p1, math_pictures.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import ChoiceType, MathDraw, MathType
from otk.sets._support.math_diagrams import _math_q, _text_q
from otk.sets._support.math_p1 import LEVEL
from otk.sets._support.math_pictures import BY_KEY, TWO_ROWS, _img, _near

PROVENANCE = Provenance("original")


def _seq(nums) -> str:
    """A comma-separated number list as spacing-only TeX (no Thai)."""
    return r",\ ".join(str(n) for n in nums)


@question_type("math.min_max_of_four",
               display_name={"th": "หาจำนวนมากที่สุด/น้อยที่สุด"}, level={"th": "ป.1"},
               topic="การเปรียบเทียบ")
class MinMaxOfFour(MathType):
    def expr(self, rng: Random, hi: int = 100):
        nums = rng.sample(range(0, hi + 1), 4)
        most = rng.random() < 0.5
        target = max(nums) if most else min(nums)
        mode = "มากที่สุด" if most else "น้อยที่สุด"
        return MathDraw(_seq(nums), str(target),
                        prompt=f"จำนวนใดมีค่า{mode}",
                        distractors=[str(n) for n in nums if n != target])


@question_type("math.compare_groups_p1", display_name={"th": "เปรียบเทียบจำนวนสิ่งของสองกลุ่ม"},
               level=LEVEL, topic="การเปรียบเทียบ")
class CompareGroupsP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        r = rng.choice(TWO_ROWS)
        top, bottom = BY_KEY[r.top], BY_KEY[r.bottom]
        img = _img(r.asset_id, [top.key, bottom.key])
        more, fewer = (top, bottom) if r.top_n > r.bottom_n else (bottom, top)
        if rng.random() < 2 / 3:
            # One true statement; the reversals and "equal" are the mistakes.
            m, f = more.thai, fewer.thai
            true, reversed_ = rng.choice(((f"{m}มากกว่า{f}", f"{f}มากกว่า{m}"),
                                          (f"{f}น้อยกว่า{m}", f"{m}น้อยกว่า{f}")))
            wrongs = [reversed_, f"{m}กับ{f}มีจำนวนเท่ากัน",
                      f"{f}มากกว่า{m}" if reversed_ != f"{f}มากกว่า{m}" else f"{m}น้อยกว่า{f}"]
            return _text_q([text("จากภาพ ข้อใดถูกต้อง"), img], true, wrongs, self.topic)
        diff = abs(r.top_n - r.bottom_n)
        big, small = max(r.top_n, r.bottom_n), min(r.top_n, r.bottom_n)
        return _math_q([text(f"จำนวน{more.thai}มากกว่าจำนวน{fewer.thai}อยู่เท่าใด"), img],
                       str(diff), _near(diff, big, small, big + small, lo=1), self.topic)


@question_type("math.order_numbers",
               display_name={"th": "เรียงลำดับจำนวน"}, level={"th": "ป.1"},
               topic="การเปรียบเทียบ")
class OrderNumbers(MathType):
    def expr(self, rng: Random, hi: int = 100):
        a, b, c = rng.sample(range(0, hi + 1), 3)
        asc = rng.random() < 0.5
        ordered = sorted([a, b, c], reverse=not asc)
        # Never show the numbers already in the order asked for: the stem
        # would then be the answer.
        while [a, b, c] == ordered:
            a, b, c = rng.sample([a, b, c], 3)
        mode = "จากน้อยไปมาก" if asc else "จากมากไปน้อย"
        distractors = [
            _seq(sorted([a, b, c], reverse=asc)),               # reversed
            _seq([ordered[1], ordered[0], ordered[2]]),         # swap first pair
            _seq([ordered[0], ordered[2], ordered[1]]),         # swap last pair
        ]
        return MathDraw(_seq([a, b, c]), _seq(ordered),
                        prompt=f"จงเรียงลำดับ{mode}", distractors=distractors)


@question_type("math.true_comparison_p1",
               display_name={"th": "ใช้เครื่องหมาย = ≠ > < ให้ถูกต้อง"},
               level=LEVEL, topic="การเปรียบเทียบ")
class TrueComparisonP1(QuestionType):
    """Exactly one of four comparison sentences is true."""

    def build(self, rng: Random) -> GeneratedQuestion:
        a = rng.randint(12, 98)
        tens, ones = divmod(a, 10)
        b = ones * 10 + tens if ones and ones != tens else a - 9
        lo, hi = sorted((a, b))
        true = rng.choice([rf"{lo} < {hi}", rf"{hi} > {lo}", rf"{lo} \neq {hi}",
                           rf"{lo} = {lo}"])
        false = [rf"{lo} > {hi}", rf"{hi} < {lo}", rf"{lo} = {hi}", rf"{hi} \neq {hi}"]
        return GeneratedQuestion(
            stem=[text("ข้อใดถูกต้อง")],
            correct=[content_math(true)],
            distractors=fixed(*[[content_math(f)] for f in rng.sample(false, 3)]),
            topic=self.topic,
        )


@question_type("math.compare_who_most_p1",
               display_name={"th": "เปรียบเทียบจำนวน: ใครมีมากที่สุด/น้อยที่สุด"},
               level=LEVEL, topic="การเปรียบเทียบ")
class CompareWhoMostP1(ChoiceType):
    def compose(self, rng: Random):
        p, q, r = _story.names(rng, 3)
        t = rng.choice(_story.THINGS)
        # Digits swapped (38 and 83) make the comparison worth doing.
        a = rng.randint(12, 98)
        tens, ones = divmod(a, 10)
        b = ones * 10 + tens if ones and ones != tens else (a - 10 if a > 50 else a + 10)
        c = rng.choice([m for m in range(10, 100) if m not in (a, b)])
        amounts = {p: a, q: b, r: c}
        most = rng.random() < 0.5
        pick = (max if most else min)(amounts, key=amounts.get)
        stem = (f"{p}มี{t.noun} {a} {t.cl} {q}มี {b} {t.cl} {r}มี {c} {t.cl} "
                f"ใครมี{t.noun}{'มากที่สุด' if most else 'น้อยที่สุด'}")
        return stem, pick, [n for n in amounts if n != pick] + ["มีเท่ากันทั้งสามคน"]
