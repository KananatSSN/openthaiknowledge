"""ระเบียบวิธีของนิวตัน

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, frac_tex

PROVENANCE = Provenance("original")


@question_type("math.newton_method",
               display_name={"th": "ระเบียบวิธีของนิวตัน"},
               level={"th": "แคลคูลัส 1"}, topic="ระเบียบวิธีของนิวตัน")
class NewtonMethod(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        return MathDraw(
            r"x_{1} = ?", r"x_{0} - \frac{f(x_{0})}{f'(x_{0})}",
            prompt="สูตรหนึ่งรอบของวิธีนิวตันคือข้อใด",
            distractors=[r"x_{0} + \frac{f(x_{0})}{f'(x_{0})}",
                         r"x_{0} - \frac{f'(x_{0})}{f(x_{0})}",
                         r"\frac{f(x_{0})}{f'(x_{0})}",
                         # Two slips at once: sign and fraction; a product.
                         r"x_{0} + \frac{f'(x_{0})}{f(x_{0})}",
                         r"x_{0} - f(x_{0})\,f'(x_{0})"])


@question_type("math.newton_first_step", display_name={"th": "นิวตัน: ค่าประมาณถัดไป"},
               level={"th": "แคลคูลัส 1"}, topic="ระเบียบวิธีของนิวตัน")
class NewtonFirstStep(MathType):
    def expr(self, rng: Random, c_lo: int = 2, c_hi: int = 30, x0_lo: int = 1,
             x0_hi: int = 6):
        c = rng.randint(c_lo, c_hi)
        x0 = rng.randint(x0_lo, x0_hi)
        # f(x) = x² − c,  x₁ = x₀ − (x₀² − c)/(2x₀)
        x1 = Fraction(x0) - Fraction(x0 * x0 - c, 2 * x0)
        return MathDraw(
            rf"f(x) = x^2 - {c}, \quad x_0 = {x0}", frac_tex(x1),
            prompt="จงหาค่าประมาณถัดไป x₁ ด้วยระเบียบวิธีของนิวตัน",
            hint=r"x_{1} = x_0 - \frac{f(x_0)}{f'(x_0)}",
            distractors=[frac_tex(Fraction(x0) + Fraction(x0 * x0 - c, 2 * x0)),
                         frac_tex(Fraction(x0 * x0 - c, 2 * x0)),
                         frac_tex(Fraction(c, 2 * x0))])


@question_type("math.newton_formula", display_name={"th": "สูตรของระเบียบวิธีนิวตัน"},
               level={"th": "แคลคูลัส 1"}, topic="ระเบียบวิธีของนิวตัน")
class NewtonFormula(ChoiceType):
    def compose(self, rng: Random):
        items = [
            ("สูตรวนซ้ำของระเบียบวิธีนิวตันคือข้อใด",
             "xₙ₊₁ = xₙ − f(xₙ) / f′(xₙ)",
             ["xₙ₊₁ = xₙ + f(xₙ) / f′(xₙ)", "xₙ₊₁ = xₙ − f′(xₙ) / f(xₙ)",
              "xₙ₊₁ = f(xₙ) / f′(xₙ)"]),
            ("ระเบียบวิธีนิวตันจะใช้ไม่ได้เมื่อใด", "เมื่อ f′(xₙ) = 0",
             ["เมื่อ f(xₙ) = 0", "เมื่อ xₙ เป็นจำนวนลบ",
              "เมื่อ f เป็นพหุนาม"]),
            ("ระเบียบวิธีนิวตันใช้หาสิ่งใด", "รากของสมการ f(x) = 0",
             ["พื้นที่ใต้เส้นโค้ง", "ค่าสูงสุดของฟังก์ชัน",
              "ลิมิตของฟังก์ชัน"]),
        ]
        return rng.choice(items)
