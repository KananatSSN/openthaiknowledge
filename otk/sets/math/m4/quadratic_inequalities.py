"""อสมการกำลังสอง

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/1

Sets moved here from: math, math_algebra, math_apply_add, math_bank_real, math_pictures_add.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import (
    ChoiceType,
    MathDraw,
    MathType,
    WordProblem,
    binomial_tex,
    poly_tex,
)
from otk.sets._support.math_apply_add import M4 as M4_math_apply_add
from otk.sets._support.math_apply_add import _c
from otk.sets._support.math_bank_real import M4, _count_q, count_integers
from otk.sets._support.math_m4 import maths as _num_maths
from otk.sets._support.math_pictures_add import QUAD_INEQS, _q


def _interval(lo, hi, closed=True) -> str:
    op = r"\leq" if closed else "<"
    return f"{lo} {op} x {op} {hi}"


def _ineq_family(rng: Random):
    """(TeX, predicate on an integer x, a named-mistake predicate, SymPy-readable text).

    The text form lets the tests solve the same inequality independently.
    """
    kind = rng.randrange(4)
    if kind == 0:
        p, q = sorted(rng.sample(range(-9, 10), 2))
        rel = rng.choice(("<", r"\le"))
        tex = rf"{binomial_tex(-p)}{binomial_tex(-q)} {rel} 0"
        strict = rel == "<"
        pred = (lambda x: (x - p) * (x - q) < 0) if strict else (lambda x: (x - p) * (x - q) <= 0)
        # The other strictness: forgetting (or wrongly adding) the endpoints.
        mistake = (lambda x: (x - p) * (x - q) <= 0) if strict else (lambda x: (x - p) * (x - q) < 0)
        return tex, pred, mistake, f"(x - ({p}))*(x - ({q})) {'<' if strict else '<='} 0"
    if kind == 1:
        # x²(k − 2x)(x + m) ≥ 0: the square never changes sign, but x = 0 is a solution.
        k, m = rng.choice((3, 5, 7, 9)), rng.randint(3, 12)
        tex = rf"x^{{2}}({k} - 2x)(x + {m}) \ge 0"
        pred = lambda x: x * x * (k - 2 * x) * (x + m) >= 0
        mistake = lambda x: (k - 2 * x) * (x + m) >= 0 and x != 0
        return tex, pred, mistake, f"x**2*({k} - 2*x)*(x + {m}) >= 0"
    if kind == 2:
        a, b = rng.sample(range(-8, 9), 2)
        rel = rng.choice(("<", r"\le"))
        tex = rf"\frac{{{poly_tex((1, 'x'), (-a, ''))}}}{{{poly_tex((1, 'x'), (-b, ''))}}} {rel} 0"
        strict = rel == "<"

        def pred(x):
            if x == b:
                return False
            v = Fraction(x - a, x - b)
            return v < 0 if strict else v <= 0
        # Multiplying through by the denominator keeps x = b.
        mistake = lambda x: (x - a) * (x - b) < 0 if strict else (x - a) * (x - b) <= 0
        return tex, pred, mistake, f"(x - ({a}))/(x - ({b})) {'<' if strict else '<='} 0"
    # −L < x(x + k) < U
    k = rng.randint(2, 7)
    lo, hi = rng.randint(3, 8), rng.randint(10, 30)
    tex = rf"-{lo} < x(x + {k}) < {hi}"
    pred = lambda x: -lo < x * (x + k) < hi
    mistake = lambda x: x * (x + k) < hi
    return tex, pred, mistake, f"({-lo} < x*(x + {k})) & (x*(x + {k}) < {hi})"


QI_ALT = "กราฟพาราโบลา y = f(x) บนระนาบพิกัดฉาก ตัดแกน X สองจุด"


_QI_OPS = {">": (True, False), "<": (False, False), r"\geq": (True, True), r"\leq": (False, True)}


def _between(r1: int, r2: int, closed: bool) -> str:
    op = r"\leq" if closed else "<"
    return f"{r1} {op} x {op} {r2}"


def _outside(r1: int, r2: int, closed: bool) -> str:
    lo, hi = (r"\leq", r"\geq") if closed else ("<", ">")
    return rf"x {lo} {r1} \;,\; x {hi} {r2}"


@question_type("math.quadratic_inequality_sign",
               display_name={"th": "เครื่องหมายของพหุนามกำลังสอง"},
               level={"th": "ม.4"}, topic="อสมการกำลังสอง")
class QuadraticInequalitySign(ChoiceType):
    def compose(self, rng: Random):
        r1, r2 = sorted(rng.sample(range(-8, 9), 2))
        test = rng.choice(["between", "left", "right"])
        point = {"between": (r1 + r2) / 2, "left": r1 - 2, "right": r2 + 2}[test]
        positive = test != "between"
        shown = poly_tex((1, "x^2"), (-(r1 + r2), "x"), (r1 * r2, ""))
        stem = (f"ให้ f(x) = {shown.replace('^2', '²')} "
                f"ค่าของ f({point:g}) เป็นอย่างไร")
        answer = "เป็นบวก" if positive else "เป็นลบ"
        return stem, answer, ["เป็นลบ" if positive else "เป็นบวก",
                              "เป็นศูนย์", "หาค่าไม่ได้"]
QuadraticInequalitySign.PROVENANCE = Provenance("original")


@question_type("math.quadratic_inequality_graph_m4",
               display_name={"th": "อ่านเซตคำตอบของอสมการกำลังสองจากกราฟ"},
               level={"th": "ม.4"}, topic="อสมการกำลังสอง")
class QuadraticInequalityGraphM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(QUAD_INEQS)
        op = rng.choice(list(_QI_OPS))
        positive, closed = _QI_OPS[op]
        outside = positive == (s.a > 0)          # a > 0: positive outside the roots
        pick = _outside if outside else _between
        other = _between if outside else _outside
        correct = pick(s.r1, s.r2, closed)
        wrongs = [pick(s.r1, s.r2, not closed), other(s.r1, s.r2, closed),
                  other(s.r1, s.r2, not closed)]
        return _q([text("จากกราฟของ y = f(x) ในภาพ จงหาเซตคำตอบของอสมการ"),
                   content_math(f"f(x) {op} 0"), image(s.asset_id, alt=QI_ALT)],
                  correct, wrongs, self.topic, [])
QuadraticInequalityGraphM4.PROVENANCE = Provenance("original")


@question_type("math.quadratic_inequality",
               display_name={"th": "อสมการกำลังสอง"}, level={"th": "ม.4"},
               topic="อสมการกำลังสอง")
class QuadraticInequality(MathType):
    def expr(self, rng: Random, root_hi: int = 6):
        r1, r2 = sorted(rng.sample(range(-root_hi, root_hi + 1), 2))
        less = rng.random() < 0.5
        tex = poly_tex((1, "x^{2}"), (-(r1 + r2), "x"), (r1 * r2, ""))
        answer = rf"{r1} < x < {r2}" if less else rf"x < {r1} \;,\; x > {r2}"
        return MathDraw(rf"{tex} {'<' if less else '>'} 0", answer,
                        hint=r"\text{sketch the parabola}", prompt="จงแก้อสมการ")
QuadraticInequality.PROVENANCE = Provenance("original")


@question_type("math.inequality_integer_count_m4",
               display_name={"th": "จำนวนเต็มที่สอดคล้องกับอสมการพหุนามและเศษส่วน"},
               level=M4, topic="อสมการกำลังสอง")
class InequalityIntegerCountM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            tex, pred, mistake, _ = _ineq_family(rng)
            right = count_integers(pred)
            if 1 <= right <= 60:
                break
        wrongs = [count_integers(mistake), right + 1, right - 1]
        stem = [text("จำนวนเต็ม x ที่สอดคล้องกับอสมการ"), content_math(tex), text("มีทั้งหมดกี่จำนวน")]
        return _count_q(stem, right, wrongs, self.topic)
InequalityIntegerCountM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/3 จำนวนจริง',))


@question_type("math.quadratic_inequality_interval",
               display_name={"th": "อสมการกำลังสอง: ช่วงคำตอบ"},
               level={"th": "ม.4"}, topic="อสมการกำลังสอง")
class QuadraticInequalityInterval(MathType):
    def expr(self, rng: Random, root_hi: int = 9):
        r1, r2 = sorted(rng.sample(range(-root_hi, root_hi + 1), 2))
        b, c = -(r1 + r2), r1 * r2
        shown = poly_tex((1, "x^2"), (b, "x"), (c, ""))
        if rng.random() < 0.5:
            # Opens upward and is negative strictly between the roots.
            return MathDraw(
                f"{shown} < 0", f"{r1} < x < {r2}",
                prompt="จงหาคำตอบของอสมการ",
                distractors=[f"x < {r1} \\;\\vee\\; x > {r2}",
                             f"{r2} < x < {r1}", f"x > {r2}"])
        return MathDraw(
            f"{shown} > 0", f"x < {r1} \\;\\vee\\; x > {r2}",
            prompt="จงหาคำตอบของอสมการ",
            distractors=[f"{r1} < x < {r2}", f"x > {r1}",
                         f"x < {r2} \\;\\vee\\; x > {r1}"])
QuadraticInequalityInterval.PROVENANCE = Provenance("original")


@question_type("math.quadratic_inequality_word_m4",
               display_name={"th": "โจทย์ปัญหาอสมการกำลังสอง"},
               level=M4_math_apply_add, topic="อสมการกำลังสอง")
class QuadraticInequalityWordM4(WordProblem):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            t1, t2 = rng.choice(((1, 3), (1, 4), (2, 3), (1, 5), (2, 4)))
            v, base = 5 * (t1 + t2), rng.choice((0, 5, 10))
            height = base + 5 * t1 * t2
            h = f"{base} + {v}t - 5t²" if base else f"{v}t - 5t²"
            return MathDraw("", str(t2 - t1),
                            prompt=(f"โยนลูกบอลขึ้นในแนวดิ่ง ความสูงเมื่อเวลา t วินาที คือ h = {h} เมตร "
                                    f"ลูกบอลอยู่สูงไม่น้อยกว่า {height} เมตร เป็นเวลานานกี่วินาที"),
                            distractors=_story.keep(t2, t1 + t2, t1 * t2, answer=t2 - t1, lo=1))
        if kind == 1:
            r1, r2 = rng.choice(((2, 8), (3, 9), (4, 10), (5, 11), (2, 12), (4, 8)))
            gain = rng.choice([g for g in (5, 10, 20) if g < r1 * r2])
            b, c = r1 + r2, r1 * r2 - gain                 # P = -x² + bx - c ≥ gain
            return MathDraw("", _interval(r1, r2),
                            prompt=(f"ร้านค้าผลิตสินค้า x ร้อยชิ้น มีกำไร P = -x² + {b}x - {c} พันบาท "
                                    f"ต้องผลิตสินค้ากี่ร้อยชิ้นจึงจะได้กำไรอย่างน้อย {gain} พันบาท"),
                            distractors=[rf"x \leq {r1} \;,\; x \geq {r2}", _interval(r1, r2, False),
                                         _interval(r1 - 1, r2 + 1)])
        if kind == 2:
            s = rng.choice((20, 24, 30, 36, 40))
            r1 = rng.randint(2, s // 2 - 2)
            area = r1 * (s - r1)
            return MathDraw("", _interval(r1, s - r1),
                            prompt=(f"ต้องการล้อมรั้วที่ดินรูปสี่เหลี่ยมผืนผ้าด้วยรั้วยาว {2 * s} เมตร "
                                    f"ให้มีพื้นที่อย่างน้อย {area} ตารางเมตร ถ้าด้านหนึ่งยาว x เมตร x ต้องอยู่ในช่วงใด"),
                            distractors=[_interval(r1, s // 2), _interval(0, r1),
                                         _interval(r1, 2 * s - r1)])
        if kind == 3:
            n, k = rng.choice(((600, 10), (800, 10), (900, 15), (1200, 20)))
            p1 = rng.randint(n // k // 5, n // k // 2 - 3)
            p2 = n // k - p1
            revenue = p1 * (n - k * p1)
            return MathDraw("", _interval(p1, p2).replace("x", "p"),
                            prompt=(f"ถ้าตั้งราคาบัตร p บาท จะขายบัตรได้ {n} - {k}p ใบ "
                                    f"ต้องการรายได้อย่างน้อย {_c(revenue)} บาท ราคาบัตรต้องอยู่ในช่วงใด"),
                            distractors=[_interval(p1, n // (2 * k)).replace("x", "p"),
                                         rf"p \leq {p1} \;,\; p \geq {p2}",
                                         _interval(p1, n // k).replace("x", "p")])
        r = rng.choice((40, 50, 60, 80, 100))
        dist = r * (r + 20) // 20
        return MathDraw("", str(r),
                        prompt=(f"รถที่วิ่งด้วยอัตราเร็ว v กิโลเมตรต่อชั่วโมง ต้องใช้ระยะหยุดรถ "
                                f"d = v + v²/20 เมตร ถ้าถนนมีระยะให้หยุดรถได้ไม่เกิน {dist} เมตร "
                                f"รถวิ่งได้เร็วที่สุดกี่กิโลเมตรต่อชั่วโมง"),
                        distractors=_story.keep(r + 10, dist // 2, isqrt(20 * dist), answer=r, lo=1))
QuadraticInequalityWordM4.PROVENANCE = Provenance("original")


@question_type("math.inequality_parameters_m4",
               display_name={"th": "หาค่าคงตัวจากเซตคำตอบของอสมการ"},
               level=M4, topic="อสมการกำลังสอง")
class InequalityParametersM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.6:
            r1, r2 = sorted(rng.sample(range(-9, 10), 2))
            b, c = -(r1 + r2), r1 * r2
            ask = rng.choice(("b + c", "b - c", "bc"))
            right = {"b + c": b + c, "b - c": b - c, "bc": b * c}[ask]
            # Using the endpoints' sum and product with the wrong signs.
            wrongs = [{"b + c": -b + c, "b - c": -b - c, "bc": -b * c}[ask],
                      {"b + c": b - c, "b - c": b + c, "bc": b + c}[ask],
                      {"b + c": r1 + r2 + c, "b - c": r1 + r2 - c, "bc": (r1 + r2) * c}[ask]]
            stem = [text("ถ้าเซตคำตอบของอสมการ"), content_math(r"x^{2} + bx + c < 0"),
                    text("คือช่วง"), content_math(f"({r1}, {r2})"),
                    text("เมื่อ b และ c เป็นค่าคงตัว แล้ว"), content_math(ask), text("เท่ากับเท่าใด")]
            return _num_maths(stem, str(right), [str(w) for w in wrongs if w != right], self.topic)
        k = rng.choice([v for v in range(-8, 9) if v])
        # (x + a)/(x + b)² ≥ 0 has solution set (k, ∞) exactly when a = b = −k:
        # the numerator gives [−a, ∞), and x = −b is excluded, removing −a itself.
        a = b = -k
        right = a + b
        stem = [text("ถ้า a และ b เป็นค่าคงตัว ซึ่งอสมการ"),
                content_math(r"\frac{x + a}{(x + b)^{2}} \ge 0"),
                text("มีเซตคำตอบคือช่วง"), content_math(rf"({k}, \infty)"),
                text("แล้ว a + b เท่ากับเท่าใด")]
        # Signs flipped; one endpoint only; forgetting the excluded point.
        wrongs = [2 * k, -k, k]
        return _num_maths(stem, str(right), [str(w) for w in wrongs if w != right], self.topic)
InequalityParametersM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/3 จำนวนจริง',))
