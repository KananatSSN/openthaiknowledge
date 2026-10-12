"""The calculus sets built from the sheet bank's knowledge units.

Areas are integrated, critical points and sign charts re-derived, tangents
and inverse derivatives recomputed with SymPy; the source exams' answers are
pinned.
"""

from __future__ import annotations

import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets._support import math_bank_calculus as mc
from otk.sets.math.m6.relative_extrema import (
    critical_statements,
    cubic_from_critical,
    symmetric_statements,
)
from otk.sets.math.m6.tangent_lines import (
    line_form,
    quadratic_from_tangent,
    tangent_with_slope,
    triangle_with_axes,
)
from otk.sets.math.m6.derivatives import inverse_derivative, reverse_product

sympy = pytest.importorskip("sympy")
x = sympy.Symbol("x", real=True)
KEYS = ("math.parabola_area_m6", "math.cubic_critical_points_m6", "math.tangent_conditions_m6",
        "math.derivative_inverse_product_m6")


def R(v):
    v = Fraction(v)
    return sympy.Rational(v.numerator, v.denominator)


def P(coefs):
    n = len(coefs) - 1
    return sum(R(c) * x ** (n - i) for i, c in enumerate(coefs))


def test_poly_tex():
    assert mc.poly_tex([Fraction(1), Fraction(0), Fraction(-3), Fraction(2)]) == "x^{3} - 3x + 2"
    assert mc.poly_tex([Fraction(-1), Fraction(1, 2)]) == r"-x + \frac{1}{2}"


def test_parabola_areas():
    for c in (1, 4, 9, 16):
        for a in (1, 4, 16):
            try:
                ours = mc.parabola_area(Fraction(c), Fraction(a))
            except ValueError:
                continue
            r = sympy.sqrt(R(Fraction(c, a)))
            assert sympy.integrate(c - a * x ** 2, (x, -r, r)) == R(ours)
            assert mc.a_from_area(Fraction(c), ours) == a
    for s in (3, 6):
        area = Fraction(4, 3) * s ** 3
        assert mc.k_from_area(area) == s * s
        assert sympy.integrate(s * s - x ** 2, (x, -s, s)) == R(area)


def test_cubic_from_critical():
    for k in (1, -1, 2):
        for p, q in ((-1, 3), (-2, 2), (0, 4)):
            f = P(cubic_from_critical(k, p, q, Fraction(3)))
            assert sympy.factor(sympy.diff(f, x) - 3 * k * (x - p) * (x - q)) == 0
            for t in (-2, 1, 5):
                assert R(mc.peval(cubic_from_critical(k, p, q, Fraction(3)), t)) == f.subs(x, t)


def test_critical_statement_truths():
    for k in (1, -1):
        for p, q in ((-1, 2), (-3, 1)):
            f = P(cubic_from_critical(k, p, q, Fraction(0))) if (p + q) % 2 == 0 else \
                k * x ** 3 - sympy.Rational(3 * k * (p + q), 2) * x ** 2 + 3 * k * p * q * x
            df = sympy.diff(f, x)
            d2 = sympy.diff(f, x, 2)
            truth = {
                f"f มีค่าสูงสุดสัมพัทธ์ที่ x = {p}": d2.subs(x, p) < 0,
                f"f มีค่าต่ำสุดสัมพัทธ์ที่ x = {q}": d2.subs(x, q) > 0,
                f"f มีค่าต่ำสุดสัมพัทธ์ที่ x = {p}": d2.subs(x, p) > 0,
                f"f มีค่าสูงสุดสัมพัทธ์ที่ x = {q}": d2.subs(x, q) < 0,
                f"บนช่วง ({p}, {q}) f เป็นฟังก์ชันเพิ่ม": df.subs(x, R(Fraction(p + q, 2))) > 0,
                f"บนช่วง ({p}, {q}) f เป็นฟังก์ชันลด": df.subs(x, R(Fraction(p + q, 2))) < 0,
                f"บนช่วง (−∞, {p}) f เป็นฟังก์ชันลด": df.subs(x, p - 1) < 0,
                f"บนช่วง ({q}, ∞) f เป็นฟังก์ชันเพิ่ม": df.subs(x, q + 1) > 0,
            }
            for s, t in critical_statements(k, p, q):
                assert bool(truth[s]) == t, (k, p, q, s)


def test_symmetric_statement_truths():
    k, c = sympy.Rational(2), sympy.Rational(5)
    for p in range(1, 6):
        f = k * x ** 3 - 3 * k * p ** 2 * x + c
        d2 = sympy.diff(f, x, 2)
        truth = {
            f"f′′(−{p}) · f′′({p}) < 0": d2.subs(x, -p) * d2.subs(x, p) < 0,
            f"f(−{p}) + f({p}) = 2f(0)": f.subs(x, -p) + f.subs(x, p) == 2 * c,
            "ค่าเฉลี่ยเลขคณิตของ f(−2), f(−1), f(0), f(1), f(2) เท่ากับ f(0)": sum(f.subs(x, t) for t in range(-2, 3)) / 5 == c,
            f"f({p}√3) = f(0)": sympy.simplify(f.subs(x, p * sympy.sqrt(3)) - c) == 0,
            f"f({p}√3) = 2f(0)": sympy.simplify(f.subs(x, p * sympy.sqrt(3)) - 2 * c) == 0,
            f"f(−{p}) = f({p})": f.subs(x, -p) == f.subs(x, p),
            "f′(0) = 0": sympy.diff(f, x).subs(x, 0) == 0,
        }
        for s, t in symmetric_statements(p):
            assert bool(truth[s]) == t, (p, s)


def test_tangents():
    for c in (5, 17):
        for m in (-2, -4, 2):
            x0, b0 = tangent_with_slope(c, m)
            f = c - x ** 2
            assert sympy.diff(f, x).subs(x, R(x0)) == m
            assert f.subs(x, R(x0)) == m * R(x0) + R(b0)
            assert R(triangle_with_axes(m, b0)) == abs(R(b0) * (R(b0) / m)) / 2
    for a, h, big_m, x0 in ((2, 2, 18, 1), (1, -1, 5, 0), (3, 4, 7, 2)):
        f = a * (x - h) ** 2 - big_m
        m = sympy.diff(f, x).subs(x, x0)
        y0 = f.subs(x, x0)
        aa, hh = quadratic_from_tangent(big_m, x0, int(m), int(y0))
        assert (aa, hh) == (a, h)


def test_line_form():
    assert line_form(Fraction(3, 2), Fraction(1), Fraction(9, 2)) == "3x + 2y = 9"
    assert line_form(Fraction(-4), Fraction(-1), Fraction(12)) == "4x + y = -12"


def test_rational_tangent():
    for k in (2, 6):
        for d in (0, 1, 3):
            for x0 in (1, 2):
                f = sympy.Rational(k) / (x + d)
                m = sympy.diff(f, x).subs(x, x0)
                y0 = f.subs(x, x0)
                assert m == R(Fraction(-k, (x0 + d) ** 2)) and y0 == R(Fraction(k, x0 + d))


def test_inverse_and_reverse_product():
    y = sympy.Symbol("y", real=True)
    for p in range(1, 7):
        for q in (-3, 0, 3):
            for a in (-2, -1, 1, 2):
                f = x ** 3 + p * x + q
                b = f.subs(x, a)
                # Differentiate f(g(y)) = y implicitly: g′(y) = 1/f′(g(y)), with g(b) = a (f is increasing).
                g = sympy.Function("g")
                implicit = sympy.diff(f.subs(x, g(y)), y)
                gprime = sympy.solve(sympy.Eq(implicit, 1), sympy.Derivative(g(y), y))[0]
                assert gprime.subs(g(y), a).subs(y, b) == R(inverse_derivative(p, a))
    for c in (0, 1, 4):
        for lo, hi in ((2, 5), (1, 3)):
            fx = 3 * x ** 2 - 7 * x + 1 + (x - lo) * (x - hi) * (x + 2)   # any polynomial
            integral = sympy.integrate(2 * x * fx + (x ** 2 - c) * sympy.diff(fx, x), (x, lo, hi))
            ours = reverse_product(c, lo, hi, Fraction(int(fx.subs(x, lo))), Fraction(int(fx.subs(x, hi))))
            assert integral == R(ours)


def test_exam_answers_reproduce():
    assert mc.k_from_area(Fraction(36)) == 9                                         # กสพท คณิต1 (มี.ค. 2565/29): 2(9 − 1) = 16
    assert mc.a_from_area(Fraction(9), Fraction(9)) == 16                            # กสพท คณิต1 (มี.ค. 2563/22)
    a = mc.a_from_area(Fraction(9), Fraction(18))
    assert a * 4 - 9 == 7                                                            # กสพท คณิต1 (มี.ค. 2561/22)
    f = cubic_from_critical(-1, -1, 1, Fraction(3))
    assert mc.peval(f, 1) == 5                                                       # กสพท คณิต1 (เม.ย. 2564/22)
    x0, b0 = tangent_with_slope(17, -2)
    assert triangle_with_axes(-2, b0) == 81                                       # กสพท คณิต1 (เม.ย. 2564/26)
    assert quadratic_from_tangent(18, 1, -4, -16) == (2, 2)                       # A-level 1 (มี.ค. 2567/11)
    assert inverse_derivative(2, 1) == Fraction(1, 5)                            # กสพท คณิต1 (มี.ค. 2562/21)
    assert reverse_product(1, 2, 5, Fraction(2), Fraction(11)) == 258             # กสพท คณิต1 (ธ.ค. 2559/24)
    m = Fraction(-6, 4)                                                              # กสพท คณิต1 (มี.ค. 2561/9)
    assert line_form(-m, Fraction(1), 3 - m * 1) == "3x + 2y = 9"


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(200):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
