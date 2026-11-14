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


# ── More dividing (2026-11): by 10 and 100, the missing divisor, sharing equally, a number that divides
# evenly, the largest quotient, and half of a number ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p3 import LEVEL  # noqa: E402


from otk.core.content import text as _text_block  # noqa: E402
from otk.core.registry import QuestionType as _QT  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


@question_type("math.divide_by_ten_p3", display_name={"th": "หารด้วย 10 และ 100"},
               level=LEVEL, topic="การหาร")
class DivideByTenP3(MathType):
    def expr(self, rng: Random):
        k = rng.choice((10, 100))
        q = rng.randint(12, 999)
        n = q * k
        # One zero too many or too few dropped; multiplied instead.
        return MathDraw(rf"{n} \div {k}", str(q), prompt="จงหาผลหาร",
                        distractors=_story.keep(q * 10, q // 10, n * k, q + 1, answer=q, lo=1))


@question_type("math.missing_divisor_p3", display_name={"th": "หาตัวหารในประโยคการหาร"},
               level=LEVEL, topic="การหาร")
class MissingDivisorP3(MathType):
    def expr(self, rng: Random):
        b, q = rng.randint(2, 9), rng.randint(3, 12)
        n = b * q
        # The quotient; the dividend; one off.
        return MathDraw(rf"{n} \div \square = {q}", str(b), prompt="จำนวนใดเติมใน □ แล้วทำให้ประโยคเป็นจริง",
                        distractors=_story.keep(q, n - q, b + 1, b - 1, answer=b, lo=1))


@question_type("math.share_equally_p3", display_name={"th": "โจทย์ปัญหาแบ่งเท่า ๆ กัน (ตัวตั้งหลายหลัก)"},
               level=LEVEL, topic="การหาร")
class ShareEquallyP3(WordProblem):
    def expr(self, rng: Random):
        b = rng.randint(2, 9)
        q = rng.randint(100, 2000)
        n = b * q
        what, unit = rng.choice((("เงิน", "บาท"), ("ข้าวสาร", "กิโลกรัม"), ("สมุด", "เล่ม")))
        prompt = f"แบ่ง{what} {n} {unit} ให้ {b} ครอบครัวเท่า ๆ กัน ได้ครอบครัวละกี่{unit}"
        # Multiplied instead; a place lost; one off.
        return MathDraw("", str(q), prompt=prompt,
                        distractors=_story.keep(n * b, q // 10, q + 1, n - b, answer=q, lo=1))


@question_type("math.divides_evenly_p3", display_name={"th": "จำนวนใดหารด้วยจำนวนที่กำหนดลงตัว"},
               level=LEVEL, topic="การหาร")
class DividesEvenlyP3(_QT):
    """Fixed choices: a number from another draw could also divide evenly."""

    def build(self, rng: Random):
        b = rng.randint(3, 9)
        right = b * rng.randint(11, 99)
        # Neighbours of the answer leave a remainder.
        wrongs = _story.keep(right + 1, right - 1, right + b + 1, right + 2, answer=right, lo=1)
        return _fixed_maths([_text_block(f"จำนวนใดหารด้วย {b} ลงตัว")], str(right), wrongs, self.topic)


@question_type("math.largest_quotient_p3", display_name={"th": "ผลหารใดมากที่สุดหรือน้อยที่สุด"},
               level=LEVEL, topic="การหาร")
class LargestQuotientP3(ChoiceType):
    def compose(self, rng: Random):
        while True:
            exprs = {}
            for _ in range(4):
                b, q = rng.randint(2, 9), rng.randint(11, 99)
                exprs[f"{b * q} ÷ {b}"] = q
            if len(exprs) == 4 and len(set(exprs.values())) == 4:
                break
        most = rng.random() < 0.5
        right = (max if most else min)(exprs, key=exprs.get)
        return f"ข้อใดมีผลหาร{'มากที่สุด' if most else 'น้อยที่สุด'}", right, [e for e in exprs if e != right]


@question_type("math.half_of_p3", display_name={"th": "ครึ่งหนึ่งของจำนวน"},
               level=LEVEL, topic="การหาร")
class HalfOfP3(WordProblem):
    def expr(self, rng: Random):
        right = rng.randint(51, 4999)
        n = 2 * right
        # Doubled instead; each digit halved and the carry lost; one off.
        return MathDraw("", str(right), prompt=f"ครึ่งหนึ่งของ {n} คือจำนวนใด",
                        distractors=_story.keep(n * 2, n - 2, right + 10, right - 1, answer=right, lo=1))
