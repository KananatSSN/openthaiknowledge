"""จำนวนเต็ม

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.1/*

Sets moved here from: math, math_diagrams, math_m1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import NUMBER_LINES, _img, _math_q, _nums
from otk.sets._support.math_m1 import LEVEL
from otk.sets._support.math_p4 import grouped

PROVENANCE = Provenance("original")


def paren(n: int) -> str:
    """Wrap negative operands in parentheses: (-3), but 4 stays bare."""
    return f"({n})" if n < 0 else str(n)


NUMBER_LINE_ALT = "เส้นจำนวนจาก -10 ถึง 10 ที่มีขีดทุก 1 หน่วย กำกับเฉพาะ -5, 0 และ 5 และมีจุด A"


_INT_TOPIC = "จำนวนเต็ม"


@question_type("math.number_line_picture_m1", display_name={"th": "อ่านจำนวนเต็มจากเส้นจำนวน"},
               level={"th": "ม.1"}, topic="จำนวนเต็ม")
class NumberLinePictureM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(NUMBER_LINES)
        p = s.p
        # The sign lost, one tick off, and counting from 5 the wrong way.
        wrongs = _nums(-p, p + 1, p - 1, (10 - p) if p > 0 else (-10 - p), answer=p, lo=-10)
        return _math_q([text("จุด A บนเส้นจำนวนแทนจำนวนใด"), _img(s.asset_id, NUMBER_LINE_ALT)],
                       str(p), wrongs, self.topic)


@question_type("math.integer_distance_m1",
               display_name={"th": "ระยะห่างบนเส้นจำนวนและค่าสัมบูรณ์"},
               level=LEVEL, topic=_INT_TOPIC)
class IntegerDistanceM1(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(-25, -1), rng.randint(-20, 25)
        if rng.random() < 0.5:
            ans = abs(a - b)
            return MathDraw(rf"{a},\ {b}", str(ans), prompt="บนเส้นจำนวน จำนวนสองจำนวนนี้อยู่ห่างกันกี่หน่วย",
                            distractors=_story.keep(abs(a + b), a + b, ans + 1, answer=ans,
                                                    lo=-99))
        ans = abs(a) + abs(b)
        return MathDraw(rf"|{a}| + |{b}|", str(ans), prompt="จงหาค่า",
                        distractors=_story.keep(a + b, abs(a + b), -ans, answer=ans, lo=-99))


@question_type("math.integer_addsub",
               display_name={"th": "บวก-ลบจำนวนเต็ม (มีจำนวนลบ)"},
               level={"th": "ม.1"}, topic="จำนวนเต็ม")
class IntegerAddSub(MathType):
    def expr(self, rng: Random, lo: int = -12, hi: int = 12):
        while True:
            a, b = rng.randint(lo, hi), rng.randint(lo, hi)
            if a < 0 or b < 0:
                break
        op = rng.choice("+-")
        return rf"{a} {op} {paren(b)}", rf"{a + b if op == '+' else a - b}"


@question_type("math.integer_muldiv",
               display_name={"th": "คูณ-หารจำนวนเต็ม (มีจำนวนลบ)"},
               level={"th": "ม.1"}, topic="จำนวนเต็ม")
class IntegerMulDiv(MathType):
    def expr(self, rng: Random, lo: int = -9, hi: int = 9):
        if rng.random() < 0.5:
            while True:
                a, b = rng.randint(lo, hi), rng.randint(lo, hi)
                if a and b and (a < 0 or b < 0):
                    break
            return MathDraw(rf"{paren(a)} \times {paren(b)}", rf"{a * b}",
                            topic="คูณจำนวนเต็ม")
        while True:
            q, d = rng.randint(lo, hi), rng.randint(2, 9)
            if q and (q < 0 or rng.random() < 0.5):
                break
        if rng.random() < 0.5:
            d = -d
        return MathDraw(rf"{paren(q * d)} \div {paren(d)}", rf"{q}",
                        topic="หารจำนวนเต็ม")


@question_type("math.integer_four_ops",
               display_name={"th": "จำนวนเต็ม: โจทย์สองขั้นตอน"},
               level={"th": "ม.1"}, topic="จำนวนเต็ม")
class IntegerFourOps(MathType):
    def expr(self, rng: Random, lo: int = -9, hi: int = 9):
        while True:
            a, b, c = (rng.randint(lo, hi) for _ in range(3))
            if a and b and c and (a < 0 or b < 0):
                break
        op = rng.choice("+-")
        prod = a * b
        if rng.random() < 0.5:
            tex = rf"{paren(a)} \times {paren(b)} {op} {paren(c)}"
            val = prod + c if op == "+" else prod - c
        else:
            tex = rf"{a} {op} {paren(b)} \times {paren(c)}"
            val = a + b * c if op == "+" else a - b * c
        return MathDraw(tex, rf"{val}", hint=r"\text{multiply first}")


@question_type("math.integer_word_problem_m1",
               display_name={"th": "โจทย์ปัญหาจำนวนเต็ม (อุณหภูมิ ระดับน้ำทะเล บัญชี)"},
               level=LEVEL, topic=_INT_TOPIC)
class IntegerWordProblemM1(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(4)
        if kind == 0:
            start, rise = rng.randint(-15, -1), rng.randint(3, 25)
            city = rng.choice(("กรุงโซล", "โตเกียว", "มอสโก", "ปักกิ่ง"))
            ans = start + rise
            return MathDraw("", str(ans),
                            prompt=(f"ตอนเช้าอุณหภูมิที่{city}เป็น {start} องศาเซลเซียส ตอนบ่ายอุณหภูมิ"
                                    f"สูงขึ้น {rise} องศาเซลเซียส ตอนบ่ายอุณหภูมิเป็นกี่องศาเซลเซียส"),
                            # The sign of the start dropped, and the rise taken away.
                            distractors=_story.keep(-start + rise, start - rise, -ans, rise,
                                                    answer=ans, lo=-99))
        if kind == 1:
            high, low = rng.randint(200, 3000), -rng.randint(50, 900)
            ans = high - low
            return MathDraw("", str(ans),
                            prompt=(f"ยอดเขาสูงจากระดับน้ำทะเล {grouped(high)} เมตร เรือดำน้ำอยู่ที่ระดับ "
                                    f"{low} เมตร เทียบกับระดับน้ำทะเล ทั้งสองอยู่สูงต่างกันกี่เมตร"),
                            distractors=_story.keep(high + low, -ans, high, answer=ans, lo=-9999))
        if kind == 2:
            bal, spend, dep = rng.randint(100, 900), rng.randint(500, 1500), rng.randint(100, 800)
            ans = bal - spend + dep
            return MathDraw("", str(ans),
                            prompt=(f"บัญชีของร้านค้ามีเงิน {bal} บาท จ่ายค่าสินค้า {grouped(spend)} บาท "
                                    f"(ยอดติดลบได้) แล้วฝากเพิ่ม {dep} บาท ยอดเงินในบัญชีเป็นเท่าใด"),
                            distractors=_story.keep(bal + spend + dep, spend - bal + dep,
                                                    bal - spend - dep, answer=ans, lo=-9999))
        a, b = rng.randint(-20, -2), rng.randint(-20, -2)
        if a == b:
            b -= 3
        higher = max(a, b)
        x, y = rng.sample(("ห้องแช่แข็งช่องที่หนึ่ง", "ห้องแช่แข็งช่องที่สอง"), 2)
        return MathDraw("", str(abs(a - b)),
                        prompt=(f"{x}มีอุณหภูมิ {a} องศาเซลเซียส {y}มีอุณหภูมิ {b} องศาเซลเซียส "
                                f"อุณหภูมิของสองช่องต่างกันกี่องศาเซลเซียส"),
                        distractors=_story.keep(abs(a + b), a + b, higher, answer=abs(a - b),
                                                lo=-99))
