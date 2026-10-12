"""แยกตัวประกอบ

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/1

Sets moved here from: math, math_algebra.
"""

from __future__ import annotations

import math as _math
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, binomial_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero, _signed

PROVENANCE = Provenance("original")


@question_type("math.factor_by_grouping", display_name={"th": "แยกตัวประกอบโดยจัดกลุ่ม"},
               level={"th": "ม.4"}, topic="แยกตัวประกอบ")
class FactorByGrouping(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 6):
        # gcd(a, b) = 1, or (ax + b) still has a common factor to pull out and
        # the "fully factored" answer would not be fully factored.
        while True:
            a, b = rng.randint(1, coef_hi), _nonzero(rng, -coef_hi, coef_hi)
            if _math.gcd(a, abs(b)) == 1:
                break
        c = _nonzero(rng, -coef_hi, coef_hi)
        # (ax + b)(x^2 + c) = ax^3 + bx^2 + acx + bc
        shown = poly_tex((a, "x^3"), (b, "x^2"), (a * c, "x"), (b * c, ""))
        answer = rf"({poly_tex((a, 'x'), (b, ''))})(x^2{_signed(c)})"
        return MathDraw(
            shown, answer, prompt="จงแยกตัวประกอบโดยการจัดกลุ่ม",
            distractors=[rf"({poly_tex((a, 'x'), (-b, ''))})(x^2{_signed(c)})",
                         rf"({poly_tex((a, 'x'), (b, ''))})(x^2{_signed(-c)})",
                         rf"(x^2{_signed(c)})({poly_tex((b, 'x'), (a, ''))})"])


@question_type("math.factor_cubes", display_name={"th": "ผลบวก/ผลต่างกำลังสาม"},
               level={"th": "ม.4"}, topic="แยกตัวประกอบ")
class FactorCubes(MathType):
    def expr(self, rng: Random, a_hi: int = 4, b_hi: int = 5):
        a = rng.randint(1, a_hi)
        b = rng.randint(1, b_hi)
        ax = "x" if a == 1 else f"{a}x"
        if rng.random() < 0.5:
            shown = poly_tex((a ** 3, "x^3"), (b ** 3, ""))
            answer = (rf"({ax} + {b})({poly_tex((a * a, 'x^2'), (-a * b, 'x'), (b * b, ''))})")
            wrong = [rf"({ax} + {b})({poly_tex((a * a, 'x^2'), (a * b, 'x'), (b * b, ''))})",
                     rf"({ax} - {b})({poly_tex((a * a, 'x^2'), (a * b, 'x'), (b * b, ''))})",
                     rf"({ax} + {b})^3"]
        else:
            shown = poly_tex((a ** 3, "x^3"), (-(b ** 3), ""))
            answer = (rf"({ax} - {b})({poly_tex((a * a, 'x^2'), (a * b, 'x'), (b * b, ''))})")
            wrong = [rf"({ax} - {b})({poly_tex((a * a, 'x^2'), (-a * b, 'x'), (b * b, ''))})",
                     rf"({ax} + {b})({poly_tex((a * a, 'x^2'), (-a * b, 'x'), (b * b, ''))})",
                     rf"({ax} - {b})^3"]
        return MathDraw(shown, answer, prompt="จงแยกตัวประกอบ", distractors=wrong)


@question_type("math.factor_advanced",
               display_name={"th": "แยกตัวประกอบขั้นสูง (จัดกลุ่ม, กำลังสาม)"},
               level={"th": "ม.4"}, topic="แยกตัวประกอบ")
class FactorAdvanced(MathType):
    def expr(self, rng: Random):
        kind = rng.choice(["group", "cubes", "biquad"])
        if kind == "group":
            a = rng.choice([1, -1]) * rng.randint(1, 5)
            b = rng.randint(2, 9)
            tex = poly_tex((1, "x^{3}"), (a, "x^{2}"), (b, "x"), (a * b, ""))
            return MathDraw(tex, rf"{binomial_tex(a)}(x^{{2}} + {b})",
                            hint=r"\text{group in pairs}", prompt="จงแยกตัวประกอบ")
        if kind == "cubes":
            a = rng.randint(1, 5)
            if rng.random() < 0.5:
                return MathDraw(
                    rf"x^{{3}} + {a ** 3}",
                    rf"(x + {a})({poly_tex((1, 'x^{2}'), (-a, 'x'), (a * a, ''))})",
                    hint=r"a^3 + b^3 = (a+b)(a^2 - ab + b^2)", prompt="จงแยกตัวประกอบ")
            return MathDraw(
                rf"x^{{3}} - {a ** 3}",
                rf"(x - {a})({poly_tex((1, 'x^{2}'), (a, 'x'), (a * a, ''))})",
                hint=r"a^3 - b^3 = (a-b)(a^2 + ab + b^2)", prompt="จงแยกตัวประกอบ")
        a, b = rng.sample(range(1, 5), 2)
        a, b = min(a, b), max(a, b)
        tex = poly_tex((1, "x^{4}"), (-(a * a + b * b), "x^{2}"), (a * a * b * b, ""))
        return MathDraw(
            tex,
            rf"{binomial_tex(a)}{binomial_tex(-a)}{binomial_tex(b)}{binomial_tex(-b)}",
            hint=r"\text{treat } x^2 \text{ as the variable}",
            prompt="จงแยกตัวประกอบให้สมบูรณ์")
