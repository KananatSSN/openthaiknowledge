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
