"""อนุกรมเทย์เลอร์

คณิตศาสตร์ · แคลคูลัส 2 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

import math as _math
from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex, poly_tex
from otk.sets._support.math_calculus import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.taylor_coefficient",
               display_name={"th": "สัมประสิทธิ์เทย์เลอร์"},
               level={"th": "แคลคูลัส 2"}, topic="อนุกรมเทย์เลอร์")
class TaylorCoefficient(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        return MathDraw(
            r"f(x) = \sum c_{n}(x - a)^{n}", r"\frac{f^{(n)}(a)}{n!}",
            prompt="สัมประสิทธิ์ของพจน์ (x − a)ⁿ คือข้อใด",
            distractors=[r"f^{(n)}(a)", r"\frac{f(a)}{n!}",
                         r"\frac{f^{(n)}(a)}{n}",
                         r"\frac{f(a)}{n}", r"f^{(n)}(a)\,n!"])


@question_type("math.maclaurin_coefficient", display_name={"th": "สัมประสิทธิ์อนุกรมแมคลอริน"},
               level={"th": "แคลคูลัส 2"}, topic="อนุกรมเทย์เลอร์")
class MaclaurinCoefficient(MathType):
    SERIES = {
        "e^x": lambda n: Fraction(1, _math.factorial(n)),
        r"\sin x": lambda n: (Fraction(0) if n % 2 == 0 else
                              Fraction((-1) ** ((n - 1) // 2), _math.factorial(n))),
        r"\cos x": lambda n: (Fraction(0) if n % 2 else
                              Fraction((-1) ** (n // 2), _math.factorial(n))),
    }

    def expr(self, rng: Random, n_lo: int = 2, n_hi: int = 6):
        name = rng.choice(list(self.SERIES))
        n = rng.randint(n_lo, n_hi)
        value = self.SERIES[name](n)
        return MathDraw(
            rf"f(x) = {name}", frac_tex(value),
            prompt=f"จงหาสัมประสิทธิ์ของ x^{n} ในอนุกรมแมคลอรินของ f",
            distractors=[frac_tex(-value) if value else frac_tex(Fraction(1, _math.factorial(n))),
                         frac_tex(Fraction(1, n)),
                         frac_tex(Fraction(1, _math.factorial(n + 1)))])


@question_type("math.taylor_polynomial_value",
               display_name={"th": "พหุนามเทย์เลอร์อันดับหนึ่ง"},
               level={"th": "แคลคูลัส 2"}, topic="อนุกรมเทย์เลอร์")
class TaylorPolynomialValue(MathType):
    """The degree-1 Taylor polynomial is exactly the tangent line — worth seeing
    stated as a series."""

    def expr(self, rng: Random, coef_hi: int = 5, point_hi: int = 4):
        a = _nonzero(rng, -coef_hi, coef_hi)
        b = rng.randint(-9, 9)
        c = rng.randint(-9, 9)
        x0 = rng.randint(-point_hi, point_hi)
        f0 = a * x0 * x0 + b * x0 + c
        d0 = 2 * a * x0 + b
        term = poly_tex((d0, "x"), (f0 - d0 * x0, ""))
        shown = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        return MathDraw(
            rf"f(x) = {shown}, \quad a = {x0}", term,
            prompt="จงหาพหุนามเทย์เลอร์อันดับหนึ่งของ f รอบจุด a",
            distractors=[poly_tex((d0, "x"), (f0, "")),
                         poly_tex((f0, "x"), (d0, "")),
                         poly_tex((d0, "x"), (f0 + d0 * x0, ""))])
