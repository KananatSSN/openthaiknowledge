"""การหาร

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.3/7

Sets moved here from: math, math_formats, math_p3.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_p3 import LEVEL

PROVENANCE = Provenance("original")


@question_type("math.division_remainder",
               display_name={"th": "การหารมีเศษ"}, level={"th": "ป.3"},
               topic="การหาร")
class DivisionRemainder(MathType):
    def expr(self, rng: Random, d_lo: int = 2, d_hi: int = 9,
             q_lo: int = 2, q_hi: int = 9):
        d = rng.randint(max(2, d_lo), d_hi)
        q = rng.randint(q_lo, q_hi)
        r = rng.randint(1, d - 1)
        return MathDraw(rf"{d * q + r} \div {d}", rf"{q} \text{{ R }} {r}",
                        hint=rf"{d} \times {q} = {d * q}")


@question_type("math.division_long",
               display_name={"th": "การหารยาว (ตัวหารหลักเดียว)"}, level={"th": "ป.3"},
               topic="การหาร")
class DivisionLong(MathType):
    def expr(self, rng: Random, d_lo: int = 2, d_hi: int = 9,
             q_lo: int = 10, q_hi: int = 99, rem: int = 1):
        d = rng.randint(max(2, d_lo), d_hi)
        q = rng.randint(q_lo, q_hi)
        r = rng.randint(0, d - 1) if rem else 0
        n = d * q + r
        answer = rf"{q}" + (rf" \text{{ R }} {r}" if r else "")
        return rf"{n} \div {d}", answer


@question_type("math.division_check_p3", display_name={"th": "ตัวตั้ง ตัวหาร ผลหาร และเศษ"},
               level={"th": "ป.3"}, topic="การหาร")
class DivisionCheckP3(QuestionType):
    """ตัวตั้ง = ตัวหาร × ผลหาร + เศษ, in both directions."""

    def build(self, rng: Random) -> GeneratedQuestion:
        d = rng.randint(3, 9)
        q = rng.randint(11, 99)
        r = rng.randint(1, d - 1)
        n = d * q + r
        kind = rng.randrange(3)
        if kind == 2:
            # The same relation told as sharing, with some left over.
            thing, bag, unit = rng.choice((("ลูกอม", "ถุง", "เม็ด"), ("ดินสอ", "กล่อง", "แท่ง"),
                                           ("ไข่ไก่", "แผง", "ฟอง"), ("ส้ม", "ตะกร้า", "ผล")))
            return _math_q([text(f"แบ่ง{thing}ใส่{bag} {bag}ละ {d} {unit} ได้ {q} {bag} และเหลืออีก {r} {unit} "
                                 f"เดิมมี{thing}กี่{unit}")],
                           str(n), [str(d * q), str(d * q - r), str(d + q + r), str(n + d)], self.topic)
        if kind == 0:
            # Forgetting the remainder; subtracting it; adding everything.
            return _math_q([text(f"การหารครั้งหนึ่งมีตัวหาร {d} ผลหาร {q} และเศษ {r} "
                                 "ตัวตั้งคือจำนวนใด")],
                           str(n), [str(d * q), str(d * q - r), str(d + q + r), str(n + d)],
                           self.topic)
        correct = f"{n} = {d} \\times {q} + {r}"
        wrongs = [f"{n} = {d} \\times {q} - {r}", f"{n} = {d} \\times {q + 1} + {r}",
                  f"{n} = {d} + {q} + {r}", f"{n} = {d} \\times {r} + {q}"]
        return _math_q([text(f"ข้อใดแสดงความสัมพันธ์ของ {n} ÷ {d} ได้ถูกต้อง")],
                       correct, wrongs, self.topic)


@question_type("math.division_word_problem_p3",
               display_name={"th": "โจทย์ปัญหาการหาร (เศษและการปัดขึ้น)"},
               level=LEVEL, topic="การหาร")
class DivisionWordProblemP3(WordProblem):
    def expr(self, rng: Random):
        per = rng.randint(3, 9)
        q = rng.randint(12, 150)
        r = rng.randint(1, per - 1)
        total = per * q + r
        kind = rng.randrange(4)
        if kind == 0:
            # Everyone has to ride: one more van for the remainder.
            return MathDraw("", str(q + 1),
                            prompt=(f"นักเรียน {total} คน ไปทัศนศึกษา รถตู้นั่งได้คันละ {per} คน "
                                    f"ต้องใช้รถตู้อย่างน้อยกี่คัน"),
                            distractors=_story.keep(q, r, q + 2, total - per, answer=q + 1))
        if kind == 1:
            return MathDraw("", str(q),
                            prompt=(f"ผ้ายาว {total} เมตร ตัดเป็นผืนละ {per} เมตร "
                                    f"ได้ผ้าเต็มผืนกี่ผืน"),
                            distractors=_story.keep(q + 1, r, q - 1, answer=q))
        if kind == 2:
            return MathDraw("", str(r),
                            prompt=(f"จัดไข่ไก่ {total} ฟอง ใส่กล่อง กล่องละ {per} ฟอง "
                                    f"จะเหลือไข่ไก่ที่ไม่ได้ใส่กล่องกี่ฟอง"),
                            distractors=_story.keep(q, per - r, r + 1, answer=r))
        exact = per * q
        return MathDraw("", str(q),
                        prompt=(f"แบ่งเงิน {exact} บาท ให้ลูก {per} คน คนละเท่า ๆ กัน "
                                f"ลูกแต่ละคนได้เงินกี่บาท"),
                        distractors=_story.keep(exact - per, q + 10, q - 1, answer=q))
