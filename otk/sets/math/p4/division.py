"""การหาร

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.4/9

Sets moved here from: math, math_thin_topics.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import combine, fixed, sibling_answers
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem

PROVENANCE = Provenance("original")


P4 = {"th": "ป.4"}


@question_type("math.division",
               display_name={"th": "การหาร (ลงตัวเสมอ)"}, level={"th": "ป.4"},
               topic="การหาร")
class Division(MathType):
    def expr(self, rng: Random, d_lo: int = 2, d_hi: int = 9,
             q_lo: int = 2, q_hi: int = 12):
        d = rng.randint(d_lo, d_hi)
        q = rng.randint(q_lo, q_hi)
        return rf"{d * q} \div {d}", rf"{q}"


@question_type("math.division_2digit",
               display_name={"th": "การหารยาว (ตัวหารสองหลัก)"}, level={"th": "ป.4"},
               topic="การหาร")
class Division2Digit(MathType):
    """Answers read ผลหาร … เศษ …, as a Thai ป.4 book writes them.

    The wrong answers are the mistakes of long division: a quotient one too
    small (so the remainder is not less than the divisor), quotient and
    remainder swapped, and a subtraction slip in the remainder.
    """

    def expr(self, rng: Random, d_lo: int = 12, d_hi: int = 39,
             q_lo: int = 2, q_hi: int = 9, rem: int = 1):
        d = rng.randint(d_lo, d_hi)
        q = rng.randint(q_lo, q_hi)
        r = rng.randint(0, d - 1) if rem else 0
        return d, q, r

    @staticmethod
    def _choice(q: int, r: int) -> list:
        return [text(f"ผลหาร {q} เศษ {r}")]

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        d, q, r = self.expr(rng, **params)
        wrongs = [(q - 1, r + d), (r, q), (q, r + 1 if r + 1 < d else r - 1),
                  (q + 1, abs(d * (q + 1) - (d * q + r)))]
        wrongs = [w for w in wrongs if w != (q, r) and min(w) >= 0]

        def sample():
            d2, q2, r2 = self.expr(rng, **params)
            return self._choice(q2, r2)

        return GeneratedQuestion(
            stem=[content_math(rf"{d * q + r} \div {d}")],
            correct=self._choice(q, r),
            distractors=combine(fixed(*[self._choice(*w) for w in wrongs]),
                                sibling_answers(sample)),
            topic=self.topic,
        )


@question_type("math.division_context_p4", display_name={"th": "โจทย์ปัญหาการหารที่มีเศษ"},
               level=P4, topic="การหาร")
class DivisionContextP4(WordProblem):
    def expr(self, rng: Random):
        d = rng.randint(3, 15)
        q = rng.randint(8, 60)
        r = rng.randint(1, d - 1)
        n = d * q + r
        kind = rng.randrange(3)
        if kind == 0:
            vehicle, cl = rng.choice((("รถตู้", "คัน"), ("เรือ", "ลำ"), ("รถสองแถว", "คัน")))
            return MathDraw("", str(q + 1),
                            prompt=(f"นักเรียน {n} คนไปทัศนศึกษา นั่ง{vehicle}{cl}ละ {d} คน "
                                    f"ต้องใช้{vehicle}อย่างน้อยกี่{cl}"),
                            # The quotient alone leaves r children behind.
                            distractors=_story.keep(q, r, q + 2, answer=q + 1, lo=1))
        if kind == 1:
            goods, cl = rng.choice((("สมุด", "เล่ม"), ("ดินสอสี", "กล่อง"), ("ขนม", "ชิ้น")))
            return MathDraw("", str(q),
                            prompt=f"มีเงิน {n} บาท ซื้อ{goods}{cl}ละ {d} บาท ซื้อได้มากที่สุดกี่{cl}",
                            # Rounding up buys a piece there is no money for.
                            distractors=_story.keep(q + 1, r, q - 1, answer=q, lo=1))
        thing = rng.choice(_story.THINGS)
        return MathDraw("", str(r),
                        prompt=(f"มี{thing.noun} {n} {thing.cl} แบ่งให้เด็ก {d} คน คนละเท่า ๆ กันให้ได้มากที่สุด "
                                f"จะเหลือ{thing.noun}กี่{thing.cl}"),
                        distractors=_story.keep(q, d - r, r + 1, answer=r, lo=0))


# ── More dividing (2026-11): by whole hundreds, the missing dividend, the dividend from the quotient and
# remainder, sharing a large amount, the largest quotient, a number that divides evenly, and the remainder ──

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import LEVEL  # noqa: E402
from otk.core.content import text as _text_block  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


@question_type("math.divide_by_hundreds_p4", display_name={"th": "หารด้วยพหุคูณของร้อย"},
               level=LEVEL, topic="การหาร")
class DivideByHundredsP4(MathType):
    def expr(self, rng: Random):
        k = rng.randint(2, 9) * 100
        q = rng.randint(12, 250)
        n = q * k
        return MathDraw(rf"{_g(n)} \div {k}", str(q), prompt="จงหาผลหาร",
                        distractors=_story.keep(q * 10, q // 10, q + 1, n // 100, answer=q, lo=1))


@question_type("math.missing_dividend_p4", display_name={"th": "หาตัวตั้งในประโยคการหาร (ตัวหารสองหลัก)"},
               level=LEVEL, topic="การหาร")
class MissingDividendP4(MathType):
    def expr(self, rng: Random):
        b, q = rng.randint(11, 40), rng.randint(12, 60)
        right = b * q
        return MathDraw(rf"\square \div {b} = {q}", _g(right), prompt="จำนวนใดเติมใน □ แล้วทำให้ประโยคเป็นจริง",
                        distractors=_gk(b + q, b * (q + 1), (b - 1) * q, q, answer=right, lo=1))


@question_type("math.dividend_from_remainder_p4", display_name={"th": "หาตัวตั้งจากตัวหาร ผลหาร และเศษ"},
               level=LEVEL, topic="การหาร")
class DividendFromRemainderP4(WordProblem):
    def expr(self, rng: Random):
        b, q = rng.randint(11, 30), rng.randint(12, 90)
        r = rng.randint(1, b - 1)
        right = b * q + r
        prompt = f"การหารครั้งหนึ่งมีตัวหาร {b} ผลหาร {q} และเศษ {r} ตัวตั้งคือจำนวนใด"
        # The remainder taken away; left out; added to the quotient.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(b * q - r, b * q, b * (q + r), right + b, answer=right, lo=1))


@question_type("math.share_large_p4", display_name={"th": "โจทย์ปัญหาแบ่งเท่า ๆ กัน (จำนวนมาก)"},
               level=LEVEL, topic="การหาร")
class ShareLargeP4(WordProblem):
    def expr(self, rng: Random):
        b = rng.randint(12, 48)
        q = rng.randint(150, 2500)
        n = b * q
        prompt = f"มูลนิธิมีเงินบริจาค {n:,} บาท แบ่งให้โรงเรียน {b} แห่งเท่า ๆ กัน ได้โรงเรียนละกี่บาท"
        return MathDraw("", _g(q), prompt=prompt,
                        distractors=_gk(q * 10, q // 10, q + b, n - b, answer=q, lo=1))


@question_type("math.largest_quotient_p4", display_name={"th": "ผลหารใดมากที่สุดหรือน้อยที่สุด (ตัวหารสองหลัก)"},
               level=LEVEL, topic="การหาร")
class LargestQuotientP4(ChoiceType):
    def compose(self, rng: Random):
        while True:
            exprs = {}
            for _ in range(4):
                b, q = rng.randint(11, 40), rng.randint(11, 99)
                exprs[f"{b * q:,} ÷ {b}"] = q
            if len(exprs) == 4 and len(set(exprs.values())) == 4:
                break
        most = rng.random() < 0.5
        right = (max if most else min)(exprs, key=exprs.get)
        return f"ข้อใดมีผลหาร{'มากที่สุด' if most else 'น้อยที่สุด'}", right, [e for e in exprs if e != right]


@question_type("math.divides_evenly_p4", display_name={"th": "จำนวนใดหารด้วยจำนวนสองหลักลงตัว"},
               level=LEVEL, topic="การหาร")
class DividesEvenlyP4(QuestionType):
    """Fixed choices: a number from another draw could also divide evenly."""

    def build(self, rng: Random):
        b = rng.randint(11, 25)
        right = b * rng.randint(20, 99)
        return _fixed_maths([_text_block(f"จำนวนใดหารด้วย {b} ลงตัว")], _g(right),
                            _gk(right + 1, right - 1, right + b + 1, right + 2, answer=right, lo=1), self.topic)


@question_type("math.remainder_only_p4", display_name={"th": "หาเศษจากการหาร"},
               level=LEVEL, topic="การหาร")
class RemainderOnlyP4(WordProblem):
    def expr(self, rng: Random):
        b, q = rng.randint(11, 30), rng.randint(12, 90)
        r = rng.randint(1, b - 1)
        n = b * q + r
        prompt = f"{n:,} ÷ {b} ได้เศษเท่าใด"
        # The quotient; what the divisor still lacks; one off.
        return MathDraw("", str(r), prompt=prompt,
                        distractors=_story.keep(q, b - r, r + 1, r - 1, answer=r, lo=0))
