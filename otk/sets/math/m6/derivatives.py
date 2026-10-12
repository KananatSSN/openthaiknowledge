"""อนุพันธ์

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม แคลคูลัส 1 ม.6/2

Sets moved here from: math, math_bank_calculus, math_bank_functions, math_calculus, math_m6.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import (
    MathDraw,
    MathType,
    frac_tex,
    poly_tex,
)
from otk.kit.math_problems import (
    poly_tex as poly_tex_math_bank_functions,
)
from otk.kit.math_problems import (
    poly_tex as poly_tex_math_calculus,
)
from otk.sets._support.math_bank_calculus import (
    M6,
    _num_q,
    peval,
)
from otk.sets._support.math_bank_calculus import (
    poly_tex as poly_tex_math_bank_calculus,
)
from otk.sets._support.math_bank_functions import M5, _frac_q, _tex_q
from otk.sets._support.math_calculus import _nonzero

DERIVATIVE = "อนุพันธ์"


def inverse_derivative(p: int, a: int) -> Fraction:
    """g′(f(a)) for g = f⁻¹, f(x) = x³ + px + q: 1/f′(a) = 1/(3a² + p)."""
    return Fraction(1, 3 * a * a + p)


def reverse_product(c: int, lo: int, hi: int, f_lo: Fraction, f_hi: Fraction) -> Fraction:
    """∫ₗₒʰⁱ (2x f(x) + (x² − c) f′(x)) dx = [(x² − c) f(x)] from lo to hi."""
    return (hi * hi - c) * f_hi - (lo * lo - c) * f_lo


def _pow(sym: str, e: int) -> str:
    """``x^{3}``, but plain ``x`` for e = 1 — nobody writes x^1."""
    return sym if e == 1 else f"{sym}^{{{e}}}"


@question_type("math.derivative_poly",
               display_name={"th": "อนุพันธ์ของพหุนาม"}, level={"th": "ม.5"},
               topic="อนุพันธ์")
class DerivativePoly(MathType):
    def expr(self, rng: Random):
        c3 = rng.randint(1, 3)
        c2, c1 = rng.randint(-5, 5), rng.randint(-6, 6)
        c0 = rng.randint(-9, 9)
        poly = poly_tex((c3, "x^{3}"), (c2, "x^{2}"), (c1, "x"), (c0, ""))
        deriv = poly_tex((3 * c3, "x^{2}"), (2 * c2, "x"), (c1, ""))
        return MathDraw(rf"y = {poly}", rf"y' = {deriv}", hint=r"(x^n)' = nx^{n-1}",
                        prompt="จงหา y′")
DerivativePoly.PROVENANCE = Provenance("original")


@question_type("math.derivative_evaluate_point",
               display_name={"th": "ค่าอนุพันธ์ของพหุนาม ณ จุดหนึ่ง"},
               level={"th": "ม.5"}, topic="อนุพันธ์")
class DerivativeEvaluatePoint(MathType):
    def expr(self, rng: Random, coef_hi: int = 5, point_hi: int = 4):
        a, b, c = (_nonzero(rng, -coef_hi, coef_hi) for _ in range(3))
        d = rng.randint(-9, 9)
        x0 = rng.randint(-point_hi, point_hi)
        # f = ax³ + bx² + cx + d  →  f′ = 3ax² + 2bx + c
        value = 3 * a * x0 * x0 + 2 * b * x0 + c
        shown = poly_tex_math_calculus((a, "x^3"), (b, "x^2"), (c, "x"), (d, ""))
        return MathDraw(
            rf"f(x) = {shown}", str(value), prompt=f"จงหาค่า f′({x0})",
            distractors=[str(a * x0 ** 3 + b * x0 * x0 + c * x0 + d),
                         str(3 * a * x0 * x0 + 2 * b * x0 + c + d),
                         str(a * x0 * x0 + b * x0 + c)])
DerivativeEvaluatePoint.PROVENANCE = Provenance("original")


@question_type("math.derivative_chain_m5",
               display_name={"th": "อนุพันธ์ของฟังก์ชันประกอบ (กฎลูกโซ่)"},
               level=M5, topic="อนุพันธ์")
class DerivativeChainM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.5:
            # f′(x) = mx + n and h(x) = f(xᵏ): h′(x) = (m·xᵏ + n)·k·xᵏ⁻¹.
            m, n, k = rng.randint(1, 5), rng.randint(1, 6), rng.choice((2, 3))
            lead, low = m * k, n * k                      # m·k·x^(2k−1) + n·k·x^(k−1)
            deg_hi, deg_lo = 2 * k - 1, k - 1
            term = lambda c, d: (c, "" if d == 0 else ("x" if d == 1 else f"x^{{{d}}}"))
            right = poly_tex_math_bank_functions(term(lead, deg_hi), term(low, deg_lo))
            wrongs = [poly_tex_math_bank_functions(term(m, k), term(n, 0)),                       # f′(xᵏ), no inner derivative
                      poly_tex_math_bank_functions(term(m * k, k), term(n * k, 0)),               # multiplied by k only
                      poly_tex_math_bank_functions(term(lead, deg_hi), term(n, deg_lo))]          # k lost on the constant
            stem = [text("ให้ f เป็นฟังก์ชัน โดยที่"), content_math(rf"f'(x) = {poly_tex_math_bank_functions((m, 'x'), (n, ''))}"),
                    text("ถ้า"), content_math(rf"h(x) = f(x^{{{k}}})"),
                    text("แล้ว h′(x) เท่ากับเท่าใด")]
            return _tex_q(stem, right, wrongs, self.topic)
        # f(k√x + d) = x: with u = k√x + d, x = ((u − d)/k)², so f′(t) = 2(t − d)/k².
        k, d = rng.choice((1, 2)), rng.randint(-3, 3)
        t = rng.randint(d + 1, d + 6)
        right = Fraction(2 * (t - d), k * k)
        inner = rf"{'' if k == 1 else k}\sqrt{{x}} {'+' if d >= 0 else '-'} {abs(d)}" if d else \
            rf"{'' if k == 1 else k}\sqrt{{x}}"
        stem = [text("กำหนดให้ f(x) เป็นฟังก์ชันพหุนาม ถ้า"), content_math(rf"f({inner}) = x"),
                text(f"เมื่อ x > 0 แล้ว f′({t}) มีค่าเท่ากับเท่าใด")]
        # Forgetting to divide by k²; using t + d; the value f(t) instead.
        named = [Fraction(2 * (t - d)), Fraction(2 * (t + d), k * k), Fraction((t - d) ** 2, k * k)]
        return _frac_q(stem, right, named, self.topic)
DerivativeChainM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/4 ฟังก์ชัน',))


@question_type("math.derivative_negative_power",
               display_name={"th": "อนุพันธ์ที่มีเลขชี้กำลังลบ"},
               level={"th": "ม.5"}, topic="อนุพันธ์")
class DerivativeNegativePower(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 6, power_hi: int = 4):
        a = _nonzero(rng, -coef_hi, coef_hi)
        n = rng.randint(1, power_hi)
        # d/dx (a·x^(−n)) = −a·n·x^(−n−1)
        coef = -a * n
        shown = rf"f(x) = \frac{{{a}}}{{{_pow('x', n)}}}"
        answer = rf"\frac{{{coef}}}{{{_pow('x', n + 1)}}}"
        return MathDraw(
            shown, answer, prompt="จงหา f′(x)",
            distractors=[rf"\frac{{{a * n}}}{{{_pow('x', n + 1)}}}",
                         rf"\frac{{{coef}}}{{{_pow('x', n - 1)}}}",
                         rf"\frac{{{a}}}{{{_pow('x', n + 1)}}}"])
DerivativeNegativePower.PROVENANCE = Provenance("original")


@question_type("math.derivative_transcendental",
               display_name={"th": "อนุพันธ์ sin, cos, e^x, ln"}, level={"th": "ม.6"},
               topic="อนุพันธ์")
class DerivativeTranscendental(MathType):
    def expr(self, rng: Random):
        k = rng.randint(2, 5)
        kind = rng.choice(["sin", "cos", "exp", "ln"])
        if kind == "sin":
            prob, ans = rf"y = \sin {k}x", rf"y' = {k}\cos {k}x"
        elif kind == "cos":
            prob, ans = rf"y = \cos {k}x", rf"y' = -{k}\sin {k}x"
        elif kind == "exp":
            prob, ans = rf"y = e^{{{k}x}}", rf"y' = {k}e^{{{k}x}}"
        else:
            prob, ans = rf"y = \ln {k}x", r"y' = \frac{1}{x}"
        return MathDraw(prob, ans, hint=r"\text{chain rule}", prompt="จงหา y′")
DerivativeTranscendental.PROVENANCE = Provenance("original")


@question_type("math.derivative_inverse_product_m6",
               display_name={"th": "อนุพันธ์ของฟังก์ชันผกผันและกฎผลคูณย้อนกลับ"},
               level=M6, topic=DERIVATIVE)
class DerivativeInverseProductM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            p, q = rng.randint(1, 6), rng.randint(-5, 6)
            a = rng.choice((-2, -1, 1, 2))
            b = a ** 3 + p * a + q
            fx = poly_tex_math_bank_calculus([Fraction(1), Fraction(0), Fraction(p), Fraction(q)])
            stem = [text("กำหนดให้"), content_math(f"f(x) = {fx}"), text("และ"), content_math(r"g(x) = f^{-1}(x)"),
                    text("เป็นฟังก์ชันผกผันของ f ค่าของ"), content_math(f"g'({b})"), text("เท่ากับเท่าใด")]
            # f′(a) itself; 1/f′(b); 1/f(a) (= 1/b).
            named = [Fraction(3 * a * a + p), Fraction(1, 3 * b * b + p), Fraction(1, b) if b else None]
            return _num_q(stem, inverse_derivative(p, a), named, self.topic)
        if kind == 1:
            m, n = rng.randint(1, 4), rng.randint(-6, 4)
            lo = rng.randint(1, 3)
            hi = lo + rng.randint(2, 4)
            c = rng.choice((1, 4, 0))
            f_lo, f_hi = Fraction(m * lo + n), Fraction(m * hi + n)
            line = poly_tex_math_bank_calculus([Fraction(m), Fraction(n)])
            poly = f"(x^{{2}} - {c})" if c else "x^{2}"
            stem = [text("ถ้า f(x) เป็นฟังก์ชันพหุนาม และกราฟของ y = f(x) ตัดกับกราฟของ"),
                    content_math(f"y = {line}"), text(f"ที่ x = {lo} และ x = {hi} แล้ว"),
                    content_math(rf"\int_{{{lo}}}^{{{hi}}} \left(2x f(x) + {poly} f'(x)\right) dx"),
                    text("มีค่าเท่ากับเท่าใด")]
            right = reverse_product(c, lo, hi, f_lo, f_hi)
            # Only the upper limit; the limits added; x² instead of x² − c.
            named = [(hi * hi - c) * f_hi, (hi * hi - c) * f_hi + (lo * lo - c) * f_lo,
                     reverse_product(0, lo, hi, f_lo, f_hi)]
            return _num_q(stem, right, named, self.topic)
        while True:                     # u′(x₀) = 0 would make every answer 0
            u = [Fraction(rng.randint(1, 3)), Fraction(rng.randint(-4, 4)), Fraction(rng.randint(-9, 5))]
            x0 = rng.randint(1, 3)
            du = 2 * u[0] * x0 + u[1]
            if du:
                break
        ux0 = peval(u, x0)
        v = Fraction(rng.randint(1, 4), rng.choice((1, 2, 3)))
        stem = [text("กำหนดให้ f เป็นฟังก์ชันที่หาอนุพันธ์ได้ และ"), content_math(f"f'({frac_tex(ux0)}) = {frac_tex(v)}"),
                text("อนุพันธ์ของ"), content_math(f"f\\left({poly_tex_math_bank_calculus(u)}\\right)"), text(f"ที่ x = {x0} มีค่าเท่ากับเท่าใด")]
        # Forgetting the inner derivative; the inner derivative alone; their sum.
        return _num_q(stem, v * du, [v, du, v + du], self.topic)
DerivativeInverseProductM6.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/15 แคลคูลัส',))


@question_type("math.motion_derivative_m6", display_name={"th": "ความเร็วและความเร่งจากอนุพันธ์"},
               level=M6, topic="อนุพันธ์")
class MotionDerivativeM6(MathType):
    def expr(self, rng: Random):
        a, b, c = rng.randint(1, 4), rng.randint(-8, 8), rng.randint(-10, 10)
        t = rng.randint(1, 5)
        s = rf"s(t) = {a if a > 1 else ''}t^{{3}} {'+' if b >= 0 else '-'} {abs(b)}t^{{2}} {'+' if c >= 0 else '-'} {abs(c)}t"
        v = 3 * a * t * t + 2 * b * t + c
        acc = 6 * a * t + 2 * b
        pos = a * t ** 3 + b * t * t + c * t
        if rng.random() < 0.6:
            return MathDraw(s, str(v), prompt=f"วัตถุเคลื่อนที่ตามตำแหน่ง s(t) (เมตร) จงหาความเร็วที่เวลา t = {t} วินาที",
                            # The position itself, and the acceleration.
                            distractors=_story.keep(pos, acc, 3 * a * t + 2 * b + c, answer=v, lo=-9999))
        return MathDraw(s, str(acc), prompt=f"วัตถุเคลื่อนที่ตามตำแหน่ง s(t) (เมตร) จงหาความเร่งที่เวลา t = {t} วินาที",
                        distractors=_story.keep(v, 6 * a + 2 * b, 3 * a * t * t, answer=acc, lo=-9999))
MotionDerivativeM6.PROVENANCE = Provenance("original")
