"""ฟังก์ชันประกอบ

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.4/1

Sets moved here from: math, math_algebra, math_apply_basic.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_apply_add import _c

PROVENANCE = Provenance("original")


@question_type("math.composite_evaluate", display_name={"th": "หาค่าฟังก์ชันประกอบ"},
               level={"th": "ม.4"}, topic="ฟังก์ชันประกอบ")
class CompositeEvaluate(MathType):
    def expr(self, rng: Random, coef_hi: int = 5, value_hi: int = 6):
        a, b = _nonzero(rng, -coef_hi, coef_hi), rng.randint(-9, 9)
        c, d = _nonzero(rng, -coef_hi, coef_hi), rng.randint(-9, 9)
        x = rng.randint(-value_hi, value_hi)
        g = c * x + d
        fg = a * g + b
        gf = c * (a * x + b) + d
        return MathDraw(
            rf"f(x) = {poly_tex((a, 'x'), (b, ''))}, \quad "
            rf"g(x) = {poly_tex((c, 'x'), (d, ''))}",
            str(fg), prompt=f"จงหาค่าของ (f ∘ g)({x})",
            # (g ∘ f)(x) is the same two functions in the other order.
            distractors=[str(gf), str(g), str(a * x + b)])


@question_type("math.composite_function",
               display_name={"th": "ฟังก์ชันประกอบ"}, level={"th": "ม.4"},
               topic="ฟังก์ชันประกอบ")
class CompositeFunction(WordProblem):
    def expr(self, rng: Random):
        a = rng.choice([n for n in range(-4, 5) if n])
        b, c, d = rng.randint(-5, 5), rng.choice([n for n in range(-4, 5) if n]), \
            rng.randint(-5, 5)
        x0 = rng.randint(-4, 4)
        fg = a * (c * x0 + d) + b
        gf = c * (a * x0 + b) + d
        return MathDraw(
            "", str(fg),
            prompt=f"ถ้า f(x) = {poly_tex((a, 'x'), (b, ''))}, "
                   f"g(x) = {poly_tex((c, 'x'), (d, ''))} จงหา (f∘g)({x0})",
            distractors=[str(gf), str((a * x0 + b) * (c * x0 + d)),
                         str((a * x0 + b) + (c * x0 + d))])


@question_type("math.composite_formula", display_name={"th": "หาสูตรของฟังก์ชันประกอบ"},
               level={"th": "ม.4"}, topic="ฟังก์ชันประกอบ")
class CompositeFormula(MathType):
    def expr(self, rng: Random, coef_hi: int = 5):
        a, b = _nonzero(rng, -coef_hi, coef_hi), rng.randint(-9, 9)
        c, d = _nonzero(rng, -coef_hi, coef_hi), rng.randint(-9, 9)
        # f(g(x)) = a(cx + d) + b
        return MathDraw(
            rf"f(x) = {poly_tex((a, 'x'), (b, ''))}, \quad "
            rf"g(x) = {poly_tex((c, 'x'), (d, ''))}",
            poly_tex((a * c, "x"), (a * d + b, "")),
            prompt="จงหา (f ∘ g)(x)",
            distractors=[poly_tex((a * c, "x"), (c * b + d, "")),
                         poly_tex((a * c, "x"), (b + d, "")),
                         poly_tex((a + c, "x"), (b + d, ""))])


@question_type("math.composite_context_m4",
               display_name={"th": "ฟังก์ชันประกอบในสถานการณ์ (แลกเงิน ส่วนลด การแปลงหน่วย)"},
               level={"th": "ม.4"}, topic="ฟังก์ชันประกอบ")
class CompositeContextM4(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            rate, fee, usd = rng.choice((32, 34, 35, 36)), rng.choice((100, 150, 200)), rng.randint(2, 20) * 10
            thb = rate * usd - fee
            return MathDraw("", _c(thb),
                            prompt=(f"f(x) = {rate}x แปลงเงิน x ดอลลาร์เป็นบาท และ g(y) = y - {fee} คือเงินที่ได้รับหลังหักค่าธรรมเนียม "
                                    f"จงหา (g ∘ f)({usd}) ซึ่งเป็นเงินบาทที่ได้รับเมื่อแลก {usd} ดอลลาร์"),
                            distractors=[_c(rate * (usd - fee)) if usd > fee else _c(rate * usd + fee), _c(rate * usd),
                                         _c(rate * usd + fee)])
        if kind == 1:
            coupon, pct = rng.choice((100, 200, 300)), rng.choice((10, 20, 25))
            gap = coupon * pct // 100
            return MathDraw("", str(gap),
                            prompt=(f"ร้านค้ามีคูปองลด {coupon} บาท และส่วนลด {pct}% ถ้าใช้คูปองก่อนแล้วจึงลด {pct}% "
                                    f"กับลด {pct}% ก่อนแล้วจึงใช้คูปอง ราคาที่จ่ายสองวิธีต่างกันกี่บาท (ราคาสินค้าเกิน {coupon * 2} บาท)"),
                            distractors=_story.keep(coupon, pct, coupon - gap, answer=gap, lo=1))
        if kind == 2:
            speed, t = rng.choice((2, 3, 4, 5)), rng.randint(2, 6)
            return MathDraw("", rf"{(speed * t) ** 2}\pi",
                            prompt=(f"วงคลื่นบนผิวน้ำมีรัศมี r(t) = {speed}t เซนติเมตร เมื่อเวลา t วินาที และพื้นที่วงกลมคือ "
                                    f"A(r) = πr² จงหา (A ∘ r)({t}) ตารางเซนติเมตร"),
                            distractors=[rf"{speed * t * t}\pi", rf"{2 * speed * t}\pi", rf"{speed * speed * t}\pi"])
        if kind == 3:
            v = rng.randint(1, 10)
            c = 5 * v + 10
            f = 9 * c // 5 + 32                     # c is a multiple of 5
            return MathDraw("", str(f),
                            prompt=(f"เครื่องวัดแปลงแรงดัน V โวลต์เป็นอุณหภูมิ C = 5V + 10 องศาเซลเซียส "
                                    f"และ F = (9/5)C + 32 แปลงเป็นองศาฟาเรนไฮต์ ถ้าอ่านได้ {v} โวลต์ อุณหภูมิเป็นกี่องศาฟาเรนไฮต์"),
                            # stopping at Celsius; forgetting the +10; forgetting the +32
                            distractors=_story.keep(c, 9 * v + 32, 9 * c // 5, answer=f, lo=1))
        a, b, n = rng.randint(2, 4), rng.randint(1, 5), rng.randint(2, 6)
        out = (a * n + b) ** 2
        return MathDraw("", str(out),
                        prompt=(f"เครื่อง A คูณจำนวนที่ใส่เข้าไปด้วย {a} แล้วบวก {b} เครื่อง B ยกกำลังสองจำนวนที่ใส่เข้าไป "
                                f"ใส่ {n} เข้าเครื่อง A แล้วนำผลลัพธ์ใส่เครื่อง B จะได้เท่าใด"),
                        # B before A; squaring before adding; skipping B
                        distractors=_story.keep(a * n * n + b, (a * n) ** 2 + b, a * n + b, answer=out, lo=1))
