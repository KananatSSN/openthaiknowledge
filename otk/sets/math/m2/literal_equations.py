"""แก้สมการหลายตัวแปร

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: —

Sets moved here from: math, math_algebra, math_formats_hi.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, poly_tex
from otk.sets._support.math_diagrams import _math_q

PROVENANCE = Provenance("original")


@question_type("math.literal_equation",
               display_name={"th": "แก้สมการหลายตัวแปร (หา y)"}, level={"th": "ม.2"},
               topic="แก้สมการหลายตัวแปร")
class LiteralEquation(MathType):
    def expr(self, rng: Random):
        b = rng.randint(2, 5)
        k = rng.choice([1, -1]) * rng.randint(1, 4)
        m = rng.choice([1, -1]) * rng.randint(1, 9)
        lhs = poly_tex((b * k, "x"), (b, "y"))
        return MathDraw(rf"{lhs} = {b * m}",
                        rf"y = {poly_tex((-k, 'x'), (m, ''))}", prompt="จงแก้หา y")


@question_type("math.literal_equation_linear",
               display_name={"th": "แก้สมการหลายตัวแปร (เชิงเส้น)"},
               level={"th": "ม.2"}, topic="แก้สมการหลายตัวแปร")
class LiteralEquationLinear(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 9):
        a = rng.randint(2, coef_hi)
        b = rng.randint(2, coef_hi)
        c = rng.randint(2, coef_hi)
        return MathDraw(
            rf"{a}x + {b}y = {c}", rf"y = \frac{{{c} - {a}x}}{{{b}}}",
            prompt="จงเขียน y ในรูปของ x",
            distractors=[rf"y = \frac{{{c} + {a}x}}{{{b}}}",
                         rf"y = \frac{{{a}x - {c}}}{{{b}}}",
                         rf"y = {c} - \frac{{{a}x}}{{{b}}}",
                         # Two slips at once.
                         rf"y = {c} + \frac{{{a}x}}{{{b}}}",
                         *([rf"y = \frac{{{c} - {b}x}}{{{a}}}"] if a != b else [])])


@question_type("math.literal_equation_area",
               display_name={"th": "แก้สูตรหาตัวแปรที่ต้องการ"},
               level={"th": "ม.2"}, topic="แก้สมการหลายตัวแปร")
class LiteralEquationArea(MathType):
    FORMULAS = [
        (r"A = \frac{1}{2}bh", "h", r"h = \frac{2A}{b}",
         [r"h = \frac{A}{2b}", r"h = \frac{b}{2A}", r"h = 2Ab"]),
        (r"P = 2(l + w)", "w", r"w = \frac{P - 2l}{2}",
         [r"w = \frac{P}{2} - 2l", r"w = P - 2l", r"w = \frac{P - l}{2}"]),
        (r"V = \pi r^2 h", "h", r"h = \frac{V}{\pi r^2}",
         [r"h = \frac{\pi r^2}{V}", r"h = \frac{V}{\pi r}", r"h = V\pi r^2"]),
        (r"C = 2\pi r", "r", r"r = \frac{C}{2\pi}",
         [r"r = \frac{2\pi}{C}", r"r = \frac{C}{\pi}", r"r = 2\pi C"]),
        (r"F = \frac{9}{5}C + 32", "C", r"C = \frac{5(F - 32)}{9}",
         [r"C = \frac{5F}{9} - 32", r"C = \frac{9(F - 32)}{5}",
          r"C = \frac{F - 32}{9}"]),
        (r"A = lw", "w", r"w = \frac{A}{l}",
         [r"w = \frac{l}{A}", r"w = A - l", r"w = Al"]),
        (r"d = vt", "t", r"t = \frac{d}{v}",
         [r"t = \frac{v}{d}", r"t = dv", r"t = d - v"]),
        (r"V = lwh", "h", r"h = \frac{V}{lw}",
         [r"h = \frac{lw}{V}", r"h = V - lw", r"h = \frac{V}{l + w}"]),
        (r"A = \frac{1}{2}(a + b)h", "h", r"h = \frac{2A}{a + b}",
         [r"h = \frac{A}{2(a + b)}", r"h = \frac{2A}{a} + b", r"h = 2A - (a + b)"]),
        (r"I = Prt", "r", r"r = \frac{I}{Pt}",
         [r"r = \frac{Pt}{I}", r"r = I - Pt", r"r = \frac{IP}{t}"]),
        (r"y = mx + c", "x", r"x = \frac{y - c}{m}",
         [r"x = \frac{y}{m} - c", r"x = \frac{y + c}{m}", r"x = m(y - c)"]),
        (r"V = \frac{1}{3}\pi r^2 h", "h", r"h = \frac{3V}{\pi r^2}",
         [r"h = \frac{V}{3\pi r^2}", r"h = \frac{3\pi r^2}{V}", r"h = 3V\pi r^2"]),
    ]

    def expr(self, rng: Random):
        formula, target, answer, wrong = rng.choice(self.FORMULAS)
        return MathDraw(formula, answer,
                        prompt=f"จงแก้สมการนี้เพื่อหา {target}",
                        distractors=list(wrong))


@question_type("math.formula_context_m2", display_name={"th": "ใช้สูตรหาค่าตัวแปรที่ต้องการ"},
               level={"th": "ม.2"}, topic="แก้สมการหลายตัวแปร")
class FormulaContextM2(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(5)
        if kind == 0:
            c = rng.randrange(-20, 101, 5)
            f = c * 9 // 5 + 32
            stem = (f"อุณหภูมิ F องศาฟาเรนไฮต์ และ C องศาเซลเซียส สัมพันธ์กันตามสูตร "
                    f"F = 9C/5 + 32 ถ้า F = {f} แล้ว C เท่ากับเท่าใด")
            ans, wrongs = c, [(f - 32) * 9 // 5, f * 5 // 9, (f + 32) * 5 // 9]
        elif kind == 1:
            a, b, h = rng.randint(4, 15), rng.randint(4, 15), rng.randint(2, 12)
            area = (a + b) * h
            if area % 2:
                h += 1
                area = (a + b) * h
            stem = (f"พื้นที่รูปสี่เหลี่ยมคางหมู A = ½(a + b)h ถ้าพื้นที่ {area // 2} ตารางเซนติเมตร "
                    f"ด้านคู่ขนานยาว {a} และ {b} เซนติเมตร สูงกี่เซนติเมตร")
            # Forgetting the ½; subtracting instead of dividing.
            ans, wrongs = h, [2 * h, area // 2 - a - b, h + 2]
        elif kind == 2:
            u, t, acc = rng.randint(0, 10), rng.randint(2, 9), rng.randint(2, 6)
            v = u + acc * t
            stem = (f"ความเร็ว v = u + at ถ้าความเร็วต้น u = {u} เมตรต่อวินาที ความเร่ง a = {acc} "
                    f"เมตรต่อวินาที² และความเร็ว v = {v} เมตรต่อวินาที ใช้เวลา t กี่วินาที")
            ans, wrongs = t, [v // acc if v % acc == 0 else t + 1, (v + u) // acc, v - u]
        elif kind == 3:
            w, length = rng.randint(3, 20), rng.randint(21, 40)
            p = 2 * (w + length)
            stem = (f"ความยาวรอบรูปสี่เหลี่ยมผืนผ้า P = 2(w + l) ถ้า P = {p} เซนติเมตร "
                    f"และ l = {length} เซนติเมตร แล้ว w เท่ากับกี่เซนติเมตร")
            ans, wrongs = w, [p - length, p // 2, p - 2 * length]
        else:
            principal = rng.choice((5000, 8000, 10000, 20000, 25000))
            r, t = rng.randint(2, 8), rng.randint(2, 5)
            i = principal * r * t // 100
            stem = (f"ดอกเบี้ย I = PRT/100 ฝากเงิน P = {principal:,} บาท เป็นเวลา T = {t} ปี "
                    f"ได้ดอกเบี้ย I = {i:,} บาท อัตราดอกเบี้ย R เป็นร้อยละเท่าใดต่อปี")
            ans, wrongs = r, [r * t, i * 100 // principal, r + t]
        wrongs = [str(x) for x in dict.fromkeys(wrongs + [ans + 1, ans - 1, ans + 2]) if x != ans]
        return _math_q([text(stem)], str(ans), wrongs, self.topic)
