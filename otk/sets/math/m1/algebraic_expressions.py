"""นิพจน์พีชคณิต

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.1/*

Sets moved here from: math, math_algebra, math_apply_stage.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_m4 import maths

PROVENANCE = Provenance("original")


@question_type("math.evaluate_expression",
               display_name={"th": "แทนค่าในนิพจน์"}, level={"th": "ม.1"},
               topic="นิพจน์พีชคณิต")
class EvaluateExpression(MathType):
    def expr(self, rng: Random, x_lo: int = -9, x_hi: int = 9):
        while True:
            x = rng.randint(x_lo, x_hi)
            if x:
                break
        if rng.random() < 0.3:
            b = rng.randint(-9, 9)
            tex, val = poly_tex((1, "x^{2}"), (b, "")), x * x + b
        else:
            a = rng.choice([n for n in range(-5, 6) if n not in (-1, 0, 1)])
            b = rng.randint(-9, 9)
            tex, val = poly_tex((a, "x"), (b, "")), a * x + b
        return MathDraw(tex, rf"{val}", prompt=f"จงหาค่าเมื่อ x = {x}")


@question_type("math.evaluate_two_variables", display_name={"th": "แทนค่าสองตัวแปร"},
               level={"th": "ม.1"}, topic="นิพจน์พีชคณิต")
class EvaluateTwoVariables(MathType):
    def expr(self, rng: Random, coef_hi: int = 6, value_hi: int = 8):
        a, b, c = (_nonzero(rng, -coef_hi, coef_hi) for _ in range(3))
        x, y = (_nonzero(rng, -value_hi, value_hi) for _ in range(2))
        value = a * x * x + b * x * y + c * y
        shown = poly_tex((a, "x^2"), (b, "xy"), (c, "y"))
        return MathDraw(
            shown, str(value),
            prompt=f"จงหาค่าของนิพจน์ เมื่อ x = {x} และ y = {y}",
            # Squaring a negative x wrongly, and swapping x with y.
            distractors=[str(-a * x * x + b * x * y + c * y),
                         str(a * y * y + b * x * y + c * x),
                         str(a * x + b * x * y + c * y)])


@question_type("math.simplify_linear",
               display_name={"th": "กระจายวงเล็บและรวมพจน์"}, level={"th": "ม.1"},
               topic="นิพจน์พีชคณิต")
class SimplifyLinear(MathType):
    def expr(self, rng: Random):
        u, v = rng.choice([("a", "b"), ("x", "y")])
        c1 = rng.randint(1, 5)
        k = rng.randint(2, 4)
        s = rng.choice([1, -1])
        su = rng.choice([1, -1])
        p = rng.randint(1, 5)
        q = rng.choice([1, -1]) * rng.randint(1, 5)
        ru = c1 + s * k * su * p
        rv = s * k * q
        inner = poly_tex((su * p, u), (q, v))
        tex = rf"{c1}{u} {'+' if s > 0 else '-'} {k}({inner})"
        return MathDraw(tex, poly_tex((ru, u), (rv, v)),
                        hint=r"\text{distribute, then collect}")


@question_type("math.expression_word_m1", display_name={"th": "นิพจน์พีชคณิตในสถานการณ์"},
               level={"th": "ม.1"}, topic="นิพจน์พีชคณิต")
class ExpressionWordM1(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            a, b, c, d = rng.randint(1, 5), rng.randint(1, 9), rng.randint(1, 5), rng.randint(1, 9)
            w, ell = poly_tex((a, "x"), (b, "")), poly_tex((c, "x"), (d, ""))
            stem = [text("รูปสี่เหลี่ยมผืนผ้ากว้าง"), content_math(w), text("หน่วย ยาว"), content_math(ell),
                    text("หน่วย ความยาวรอบรูปเขียนเป็นนิพจน์ในรูปอย่างง่ายได้อย่างไร")]
            right = poly_tex((2 * (a + c), "x"), (2 * (b + d), ""))
            # Only half the perimeter, the sides multiplied, and the 2 applied to x only.
            wrongs = [poly_tex((a + c, "x"), (b + d, "")), poly_tex((a * c, "x^{2}"), (a * d + b * c, "x"), (b * d, "")),
                      poly_tex((2 * (a + c), "x"), (b + d, "")), poly_tex((4 * (a + c), "x"), (4 * (b + d), ""))]
            return maths(stem, right, wrongs, self.topic)
        if kind == 1:
            a, b = rng.choice((12, 15, 20, 25)), rng.choice((5, 8, 10))
            note = rng.choice((200, 500, 1000))
            stem = [text(f"ซื้อสมุด x เล่ม ราคาเล่มละ {a} บาท และปากกา y ด้าม ราคาด้ามละ {b} บาท "
                         f"จ่ายด้วยธนบัตร {note} บาท นิพจน์ใดแทนเงินทอน")]
            right = rf"{note} - {a}x - {b}y"
            wrongs = [rf"{note} - {a}x + {b}y", rf"{a}x + {b}y - {note}", rf"{note} - {a + b}xy",
                      rf"{note} - {a}y - {b}x"]
            return maths(stem, right, wrongs, self.topic)
        start, per = rng.choice((20, 30, 40)), rng.choice((10, 15, 25))
        h = rng.randint(2, 9)
        stem = [text(f"ร้านให้เช่าจักรยานคิดค่าเช่า {start} + {per}h บาท เมื่อ h คือจำนวนชั่วโมงที่เช่า "
                     f"ถ้าเช่า {h} ชั่วโมง ต้องจ่ายกี่บาท")]
        cost = start + per * h
        return maths(stem, str(cost), _nums(cost, (start + per) * h, start * h + per, per * h, lo=1), self.topic)
