"""การคูณยาว

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.4/9

Sets moved here from: math, math_apply_basic, math_formats, math_number.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_apply_add import _c
from otk.sets._support.math_diagrams import _math_q

PROVENANCE = Provenance("original")


@question_type("math.multiply_by_tens", display_name={"th": "คูณด้วยพหุคูณของสิบ"},
               level={"th": "ป.4"}, topic="การคูณยาว")
class MultiplyByTens(MathType):
    """The zero-shifting shortcut: 34 × 200 is 34 × 2 with two zeros after it."""

    def expr(self, rng: Random, lo: int = 12, hi: int = 99):
        a = rng.randint(lo, hi)
        d, zeros = rng.randint(2, 9), rng.randint(1, 3)
        b = d * 10 ** zeros
        return MathDraw(rf"{a} \times {b}", str(a * b),
                        prompt="จงหาผลคูณ",
                        hint=rf"{a} \times {d} = {a * d}",
                        distractors=[str(a * d * 10 ** (zeros + 1)),
                                     str(a * d * 10 ** max(zeros - 1, 0)),
                                     str(a * d)])


@question_type("math.multiply_partial_products_p4", display_name={"th": "คูณโดยแยกเป็นผลคูณย่อย"},
               level={"th": "ป.4"}, topic="การคูณยาว")
class MultiplyPartialProductsP4(QuestionType):
    """``23 × 14 = 23 × 10 + 23 × 4``: the step long multiplication writes as
    two rows."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random) -> GeneratedQuestion:
        a = rng.randint(12, 98)
        t, o = rng.randint(1, 9), rng.randint(2, 9)
        b = 10 * t + o
        if rng.random() < 0.5:
            correct = rf"{a} \times {10 * t} + {a} \times {o}"
            wrongs = [rf"{a} \times {t} + {a} \times {o}",            # the tens digit as ones
                      rf"{a} \times {10 * t} \times {a} \times {o}",
                      rf"{a // 10 * 10} \times {10 * t} + {a % 10} \times {o}",
                      rf"{a} \times {10 * t} + {o}"]
            return _math_q([text(f"ข้อใดมีค่าเท่ากับ {a} × {b}")], correct, wrongs, self.topic)
        # The second row of the long multiplication, and the total.
        first, second = a * o, a * 10 * t
        return _math_q([text(f"ในการคูณ {a} × {b} แบบแยกหลัก ได้ {a} × {o} = {first} "
                             f"และ {a} × {10 * t} = {second} ผลคูณ {a} × {b} เท่ากับเท่าใด")],
                       # Adding the tens row without its zero; one row only.
                       str(a * b), [str(first + a * t), str(second), str(first + second + 10),
                                    str(a * b - a)],
                       self.topic)


@question_type("math.multiply_3x1", display_name={"th": "คูณยาว (สามหลัก × หลักเดียว)"},
               level={"th": "ป.4"}, topic="การคูณยาว")
class Multiply3x1(MathType):
    def expr(self, rng: Random, lo: int = 112, hi: int = 989):
        a, b = rng.randint(lo, hi), rng.randint(3, 9)
        return MathDraw(rf"{a} \times {b}", str(a * b),
                        prompt="จงหาผลคูณ",
                        distractors=[str(a * (b + 1)), str(a * (b - 1)),
                                     str(a * b + 100)])


@question_type("math.multiply_2x2",
               display_name={"th": "คูณยาว (สองหลัก × สองหลัก)"}, level={"th": "ป.4"},
               topic="การคูณยาว")
class Multiply2x2(MathType):
    def expr(self, rng: Random, a_lo: int = 12, a_hi: int = 98,
             b_lo: int = 12, b_hi: int = 98):
        a = rng.randint(a_lo, a_hi)
        b = rng.randint(b_lo, b_hi)
        return rf"{a} \times {b}", rf"{a * b}"


@question_type("math.multiply_multistep_p4",
               display_name={"th": "โจทย์ปัญหาการคูณหลายขั้นตอน"},
               level={"th": "ป.4"}, topic="การคูณยาว")
class MultiplyMultistepP4(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(5)
        if kind == 0:
            n, k, price = rng.randint(12, 48), rng.choice((12, 18, 24)), rng.randint(5, 9)
            total = n * k * price
            return MathDraw("", _c(total),
                            prompt=(f"ร้านค้ามีน้ำดื่ม {n} ลัง ลังละ {k} ขวด ขายขวดละ {price} บาท "
                                    f"ถ้าขายหมดจะได้เงินกี่บาท"),
                            distractors=[_c(n * k), _c(n * price + k), _c((n + k) * price)])
        if kind == 1:
            n, k, price = rng.randint(12, 30), rng.choice((12, 20, 24)), rng.randint(6, 12)
            cost = k * price - rng.choice((12, 20, 24, 30))
            profit = n * k * price - n * cost
            return MathDraw("", _c(profit),
                            prompt=(f"{p}ซื้อขนม {n} กล่อง กล่องละ {cost} บาท แต่ละกล่องมีขนม {k} ชิ้น "
                                    f"นำไปขายชิ้นละ {price} บาท ถ้าขายหมด{p}ได้กำไรกี่บาท"),
                            distractors=[_c(n * k * price), _c(n * cost), _c(k * price - cost)])
        if kind == 2:
            weeks, pages = rng.randint(2, 4), rng.randint(12, 25)
            book = 7 * weeks * pages + rng.randint(20, 90)
            left = book - 7 * weeks * pages
            return MathDraw("", str(left),
                            prompt=(f"หนังสือเล่มหนึ่งหนา {book} หน้า {p}อ่านวันละ {pages} หน้า ทุกวันเป็นเวลา {weeks} สัปดาห์ "
                                    f"ยังเหลือที่ยังไม่ได้อ่านอีกกี่หน้า"),
                            distractors=_story.keep(book - weeks * pages, 7 * weeks * pages, book - 7 * pages,
                                                    answer=left, lo=1))
        if kind == 3:
            rows, cols, kg, price = rng.randint(12, 25), rng.randint(11, 19), rng.randint(3, 8), rng.randint(15, 40)
            total = rows * cols * kg * price
            return MathDraw("", _c(total),
                            prompt=(f"สวนมะม่วงปลูกต้นมะม่วง {rows} แถว แถวละ {cols} ต้น แต่ละต้นเก็บมะม่วงได้ {kg} กิโลกรัม "
                                    f"ขายกิโลกรัมละ {price} บาท จะได้เงินทั้งหมดกี่บาท"),
                            distractors=[_c(rows * cols * kg), _c(rows * cols * price), _c((rows + cols) * kg * price)])
        a, b, adult, child = rng.randint(12, 35), rng.randint(15, 45), rng.choice((120, 150, 180)), rng.choice((60, 70, 80))
        total = a * adult + b * child
        return MathDraw("", _c(total),
                        prompt=(f"โรงเรียนพานักเรียน {b} คน และครู {a} คน ไปสวนสัตว์ ค่าเข้าชมครูคนละ {adult} บาท "
                                f"นักเรียนคนละ {child} บาท ต้องจ่ายค่าเข้าชมทั้งหมดกี่บาท"),
                        distractors=[_c((a + b) * adult), _c((a + b) * child), _c(a * child + b * adult)])
