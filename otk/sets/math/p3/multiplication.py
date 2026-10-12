"""การคูณ

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.3/6

Sets moved here from: math, math_p3, math_pictures_hi.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_p3 import LEVEL
from otk.sets._support.math_pictures import _near
from otk.sets._support.math_pictures_hi import AREA_MODELS

PROVENANCE = Provenance("original")


_MUL_HINT = r"\text{ab} \times \text{c} = \text{a}{\cdot}10{\cdot}\text{c} + \text{b}{\cdot}\text{c}"


def _product_story(rng: Random, a: int, b: int) -> str:
    """a × b in a ป.3 situation; a is the per-group amount."""
    p = rng.choice(_story.NAMES)
    return rng.choice((
        f"โรงเรียนจ้างรถบัส {b} คัน แต่ละคันนั่งได้ {a} คน รถบัสทั้งหมดนั่งได้กี่คน",
        f"โรงงานผลิตขนมได้วันละ {a} ชิ้น {b} วันผลิตขนมได้กี่ชิ้น",
        f"ค่าเข้าชมพิพิธภัณฑ์คนละ {a} บาท นักเรียน {b} คน ต้องจ่ายค่าเข้าชมกี่บาท",
        f"{p}ปั่นจักรยานวันละ {a} เมตร เป็นเวลา {b} วัน {p}ปั่นได้ระยะทางกี่เมตร",
        f"ร้านค้าสั่งน้ำดื่ม {b} ลัง ลังละ {a} ขวด ร้านค้าได้น้ำดื่มกี่ขวด",
        f"สวนแห่งหนึ่งปลูกต้นยาง {b} แถว แถวละ {a} ต้น ปลูกต้นยางทั้งหมดกี่ต้น",
    ))


AREA_ALT = "ภาพรูปสี่เหลี่ยมผืนผ้าแบ่งเป็นสองส่วน ใช้หาผลคูณ"


@question_type("math.times_table",
               display_name={"th": "สูตรคูณ แม่ 2–9"}, level={"th": "ป.3"}, topic="การคูณ")
class TimesTable(MathType):
    def expr(self, rng: Random, table_lo: int = 2, table_hi: int = 9,
             n_lo: int = 1, n_hi: int = 9):
        a = rng.randint(table_lo, table_hi)
        n = rng.randint(n_lo, n_hi)
        problem = rf"{a} \times {n}" if rng.random() < 0.5 else rf"{n} \times {a}"
        return MathDraw(problem, rf"{a * n}", topic=f"สูตรคูณแม่ {a}")


@question_type("math.multiplication",
               display_name={"th": "การคูณ"}, level={"th": "ป.3"}, topic="การคูณ")
class Multiplication(MathType):
    def expr(self, rng: Random, a_lo: int = 2, a_hi: int = 20,
             b_lo: int = 2, b_hi: int = 9):
        a = rng.randint(a_lo, a_hi)
        b = rng.randint(b_lo, b_hi)
        problem = rf"{a} \times {b}" if rng.random() < 0.5 else rf"{b} \times {a}"
        return MathDraw(problem, rf"{a * b}", hint=_MUL_HINT)


@question_type("math.multiply_2x1",
               display_name={"th": "คูณ (หลายหลัก × หลักเดียว)"}, level={"th": "ป.3"},
               topic="การคูณ")
class Multiply2x1(MathType):
    def expr(self, rng: Random, a_lo: int = 12, a_hi: int = 99,
             b_lo: int = 2, b_hi: int = 9):
        a = rng.randint(a_lo, a_hi)
        b = rng.randint(b_lo, b_hi)
        return rf"{a} \times {b}", rf"{a * b}"


@question_type("math.one_digit_multiply",
               display_name={"th": "คูณเลขสองหลักด้วยเลขหลักเดียว"}, level={"th": "ป.3"},
               topic="การคูณ")
class OneDigitMultiply(MathType):
    def expr(self, rng: Random, a_lo: int = 11, a_hi: int = 19,
             b_lo: int = 2, b_hi: int = 9):
        a = rng.randint(a_lo, a_hi)
        b = rng.randint(b_lo, b_hi)
        problem = rf"{a} \times {b}" if rng.random() < 0.5 else rf"{b} \times {a}"
        return MathDraw(problem, rf"{a * b}", hint=_MUL_HINT)


@question_type("math.area_model_p3", display_name={"th": "การคูณด้วยแผนภาพพื้นที่"},
               level={"th": "ป.3"}, topic="การคูณ")
class AreaModelP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        m = rng.choice(AREA_MODELS)
        tens, ones = m.a // 10 * 10, m.a % 10
        img = image(m.asset_id, alt=AREA_ALT)
        if rng.random() < 0.5:
            # The ones part times the tens digit only; adding instead of multiplying.
            return _math_q([text(f"จากภาพ {m.a} × {m.b} เท่ากับเท่าใด"), img], str(m.a * m.b),
                           _near(m.a * m.b, tens // 10 * m.b + ones * m.b, tens * m.b, m.a + m.b,
                                 m.a * m.b + m.b, lo=1), self.topic)
        part = rng.choice(("tens", "ones"))
        value = tens * m.b if part == "tens" else ones * m.b
        where = "ส่วนที่ใหญ่กว่า" if part == "tens" else "ส่วนที่เล็กกว่า"
        return _math_q([text(f"จากภาพ พื้นที่{where}แทนผลคูณเท่าใด"), img], str(value),
                       _near(value, m.a * m.b, tens // 10 * m.b if part == "tens" else ones + m.b,
                             value + m.b, lo=1), self.topic)


@question_type("math.multiply_4x1_p3",
               display_name={"th": "การคูณจำนวนหนึ่งหลักกับจำนวนไม่เกินสี่หลัก"},
               level=LEVEL, topic="การคูณ")
class Multiply4x1P3(MathType):
    def expr(self, rng: Random, lo: int = 1000, hi: int = 9999):
        a = rng.randint(max(100, int(lo)), min(9999, int(hi)))
        b = rng.randint(2, 9)
        ans = a * b
        # Each place multiplied with its carry dropped.
        no_carry = sum(((int(d) * b) % 10) * 10 ** i for i, d in enumerate(str(a)[::-1]))
        return MathDraw(rf"{a} \times {b}", str(ans), prompt="จงหาผลคูณ",
                        distractors=_story.keep(no_carry, ans + 100, ans - 10, a * (b - 1),
                                                answer=ans))


@question_type("math.multiply_3x1_p3",
               display_name={"th": "การคูณจำนวนหนึ่งหลักกับจำนวนสามหลัก"},
               level=LEVEL, topic="การคูณ")
class Multiply3x1P3(Multiply4x1P3):
    """The step between two digits and four: one more carry to track."""

    def expr(self, rng: Random, lo: int = 100, hi: int = 999):
        return super().expr(rng, lo=lo, hi=hi)


@question_type("math.multiplication_word_problem_p3",
               display_name={"th": "โจทย์ปัญหาการคูณ (ไม่เกินสี่หลัก และสองหลักคูณสองหลัก)"},
               level=LEVEL, topic="การคูณ")
class MultiplicationWordProblemP3(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            a, b = rng.randint(12, 99), rng.randint(11, 99)      # สองหลัก × สองหลัก
        else:
            a, b = rng.randint(105, 9999), rng.randint(2, 9)     # หลายหลัก × หนึ่งหลัก
        ans = a * b
        # Adding instead, and the tens digit multiplied as if it were ones.
        slip = a * (b % 10) + a * (b // 10) if b >= 10 else a * (b + 1)
        return MathDraw("", str(ans), prompt=_product_story(rng, a, b),
                        distractors=_story.keep(slip, a + b, ans + a, ans - 10, answer=ans))
