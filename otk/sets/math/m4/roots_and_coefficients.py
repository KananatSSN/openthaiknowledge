"""ความสัมพันธ์ราก-สัมประสิทธิ์

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/1

Sets moved here from: math, math_algebra.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.vieta",
               display_name={"th": "ความสัมพันธ์ราก-สัมประสิทธิ์"}, level={"th": "ม.4"},
               topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class Vieta(MathType):
    def expr(self, rng: Random):
        p = rng.choice([n for n in range(-6, 7) if n])
        q = rng.choice([n for n in range(-8, 9) if n])
        eq = poly_tex((1, "x^{2}"), (-p, "x"), (q, ""))
        kind = rng.choice(["sumsq", "diffsq", "prodsum", "recip"])
        if kind == "sumsq":
            expr, val = r"\alpha^{2} + \beta^{2}", rf"{p * p - 2 * q}"
        elif kind == "diffsq":
            expr, val = r"(\alpha - \beta)^{2}", rf"{p * p - 4 * q}"
        elif kind == "prodsum":
            expr, val = r"\alpha^{2}\beta + \alpha\beta^{2}", rf"{p * q}"
        else:
            expr, val = r"\frac{1}{\alpha} + \frac{1}{\beta}", frac_tex(Fraction(p, q))
        return MathDraw(rf"{eq} = 0: \quad {expr}", val,
                        hint=rf"\alpha + \beta = {p}, \; \alpha\beta = {q}",
                        prompt="ให้แอลฟาและเบตาเป็นรากของสมการ จงหาค่า")


@question_type("math.vieta_build", display_name={"th": "หาสัมประสิทธิ์จากผลบวก/ผลคูณของราก"},
               level={"th": "ม.4"}, topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class VietaBuild(MathType):
    def expr(self, rng: Random, sum_hi: int = 12, product_hi: int = 20):
        s = rng.randint(-sum_hi, sum_hi)
        p = _nonzero(rng, -product_hi, product_hi)
        return MathDraw(
            rf"r_1 + r_2 = {s}, \quad r_1 r_2 = {p}",
            poly_tex((1, "x^2"), (-s, "x"), (p, "")) + " = 0",
            prompt="สมการกำลังสองใดมีรากตามเงื่อนไขนี้",
            distractors=[poly_tex((1, "x^2"), (s, "x"), (p, "")) + " = 0",
                         poly_tex((1, "x^2"), (-s, "x"), (-p, "")) + " = 0",
                         poly_tex((1, "x^2"), (s, "x"), (-p, "")) + " = 0"])


@question_type("math.vieta_expressions",
               display_name={"th": "ค่าของนิพจน์จากผลบวกและผลคูณของราก"},
               level={"th": "ม.4"}, topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class VietaExpressions(MathType):
    """The point of Vieta: symmetric expressions in the roots, without the roots."""

    def expr(self, rng: Random, coef_hi: int = 9):
        b = _nonzero(rng, -coef_hi, coef_hi)
        c = _nonzero(rng, -coef_hi, coef_hi)
        s, p = -b, c                              # r1 + r2, r1·r2
        kind = rng.choice(["squares", "reciprocals"])
        if kind == "squares":
            ask, value = r"r_1^2 + r_2^2", s * s - 2 * p
            wrong = [str(s * s), str(s * s + 2 * p), str(s * s - p)]
        else:
            ask = r"\frac{1}{r_1} + \frac{1}{r_2}"
            value_f = Fraction(s, p)
            ask_value = frac_tex(value_f)
            return MathDraw(
                poly_tex((1, "x^2"), (b, "x"), (c, "")) + " = 0", ask_value,
                prompt=f"ถ้า r₁ และ r₂ เป็นรากของสมการนี้ จงหาค่าของ {ask}",
                distractors=[frac_tex(Fraction(p, s)), frac_tex(-value_f),
                             frac_tex(Fraction(1, p))])
        return MathDraw(
            poly_tex((1, "x^2"), (b, "x"), (c, "")) + " = 0", str(value),
            prompt=f"ถ้า r₁ และ r₂ เป็นรากของสมการนี้ จงหาค่าของ {ask}",
            distractors=wrong)
