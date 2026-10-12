"""The complex-number sets built from the sheet bank's knowledge units.

Powers, bases and counts are checked with SymPy's I; every equation's
solutions are substituted back (and the rejected ones shown to fail);
polynomials are rebuilt from their roots; the statement bank is checked on
random numbers; the source exams' answers are pinned.
"""

from __future__ import annotations

import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets._support.math_bank_complex import c as cplx
from otk.sets.math.m5 import complex_numbers as mc

sympy = pytest.importorskip("sympy")
IU = sympy.I
KEYS = ("math.complex_power_cycle_m5", "math.complex_equation_parts_m5", "math.complex_conjugate_root_m5",
        "math.complex_modulus_rules_m5", "math.complex_polynomial_solve_m5")


def R(v):
    v = Fraction(v)
    return sympy.Rational(v.numerator, v.denominator)


def Z(z):
    return R(z[0]) + R(z[1]) * IU


def test_i_powers_and_bases():
    for n in range(0, 40):
        assert Z(mc.i_power(n)) == IU ** n
    bases = [(1 + IU) / (1 - IU), (1 - IU) / (1 + IU), ((1 + IU) / sympy.sqrt(2)) ** 2, (1 - IU) ** 2 / 2]
    for (_, e), b in zip(mc.BASES, bases):
        assert sympy.simplify(b - IU ** e) == 0


def test_count_matching():
    for p in range(1, 5):
        for r in range(1, 5):
            for q in (-5, 0, 3):
                for s in (-2, 4):
                    brute = sum(sympy.simplify(((1 + IU) / (1 - IU)) ** (p * x + q) - IU ** (r * x + s)) == 0
                                for x in range(1, 25))
                    assert mc.count_matching(24, p, q, r, s) == brute


def test_ctex():
    assert mc.ctex(cplx(1, 1)) == "1 + i"
    assert mc.ctex(cplx(0, -1)) == "-i"
    assert mc.ctex(cplx(12, Fraction(7, 2))) == r"12 + \frac{7}{2}i"
    assert mc.ctex(cplx(-3, 0)) == "-3"


def test_conj_plus_i_modulus():
    for a in range(-6, 7):
        for b in range(1, 7):
            z = Z(mc.conj_plus_i_modulus(a, b))
            assert sympy.simplify(sympy.conjugate(z) + IU * sympy.Abs(z) - (a + b * IU)) == 0


def test_z_plus_modulus_shift():
    for a in range(-6, 7):
        for b in range(-4, 5):
            for s in range(-3, 4):
                sol = mc.z_plus_modulus_shift(a, b, s)
                if sol is None:
                    continue
                z = Z(sol)
                assert sympy.simplify(z + sympy.Abs(z - s) - (a + b * IU)) == 0


def test_imaginary_axis_roots():
    for m in range(1, 6):
        for k in (-3, -1, 1, 2):
            for d in range(-4, 12):
                valid, rejected = mc.imaginary_axis_roots(m, k, d)
                for y in valid:
                    z = y * IU
                    assert sympy.simplify(sympy.Abs(z ** 2 - m) - (k * IU * z + d)) == 0
                for y in rejected:
                    z = y * IU
                    assert sympy.simplify(sympy.Abs(z ** 2 - m) - (k * IU * z + d)) != 0


def test_square_roots():
    for x in range(-4, 5):
        for y in range(1, 5):
            assert sympy.expand((x + y * IU) ** 2) == Z(mc.square_root_of(x, y))


def test_polynomials_from_roots():
    X = sympy.Symbol("x")
    for p in range(-4, 5):
        for q in range(1, 4):
            a, b = mc.quadratic_from_root(p, q)
            assert sympy.expand((X ** 2 + a * X + b).subs(X, p + q * IU)) == 0
            f = mc.quartic_with_rational_root(p, q)
            poly = sum(cf * X ** (4 - i) for i, cf in enumerate(f))
            assert sympy.expand(poly.subs(X, p + q * IU)) == 0
            assert poly.subs(X, 1) == 0 and f[-1] == -(p * p + q * q)
            for x0 in (2, 3, -2, 0):
                assert mc.poly_eval(f, x0) == poly.subs(X, x0)


def test_polar_distance():
    for delta in mc.COS_DELTA:
        m = mc.COS_DELTA[delta][1]
        for r1 in range(1, 4):
            for r2 in range(1, 5):
                beta = sympy.pi / 8
                z1 = r1 * sympy.sqrt(m) * sympy.exp(IU * (beta + R(delta) * sympy.pi))
                z2 = r2 * sympy.exp(IU * beta)
                # SymPy leaves (−1)^(1/4) forms unsimplified; 50 digits are decisive for integers.
                d2 = sympy.Abs(z1 - z2) ** 2
                assert abs(sympy.N(d2 - R(mc.polar_distance_sq(r1, r2, delta)), 50)) < 1e-40


def test_complex_fact_bank():
    rng = random.Random(3)
    seen_false = set()
    re = sympy.re
    for _ in range(30):
        z = rng.choice([-3, -1, 1, 2]) + rng.choice([-2, 1, 3]) * IU
        w = rng.choice([-2, 1, 4]) + rng.choice([-3, -1, 2]) * IU
        cz, cw = sympy.conjugate(z), sympy.conjugate(w)
        checks = [z * cz - sympy.Abs(z) ** 2, sympy.Abs(z * w) - sympy.Abs(z) * sympy.Abs(w), sympy.Abs(cz) - sympy.Abs(z),
                  sympy.Abs(1 / z) - 1 / sympy.Abs(z), z + cz - 2 * re(z), sympy.conjugate(z * w) - cz * cw,
                  sympy.Abs(z ** 3) - sympy.Abs(z) ** 3,
                  sympy.Abs(z + w) - sympy.Abs(z) - sympy.Abs(w), z ** 2 - sympy.Abs(z) ** 2,
                  sympy.Abs(z - w) - (sympy.Abs(z) - sympy.Abs(w)), re(z * w) - re(z) * re(w), cz / z - 1,
                  sympy.Abs(z + cz) - 2 * sympy.Abs(z)]
        for (tex, true), e in zip(mc.COMPLEX_FACTS, checks):
            zero = sympy.simplify(sympy.expand(e)) == 0
            if true:
                assert zero, tex
            elif not zero:
                seen_false.add(tex)
    assert seen_false == {t for t, true in mc.COMPLEX_FACTS if not true}


def test_exam_answers_reproduce():
    assert Z(mc.i_power(101)) + 1 == 1 + IU                                           # กสพท คณิต1 (มี.ค. 2561/2)
    assert mc.count_matching(155, 2, -5, 1, -2) == 39                                # กสพท คณิต1 (ธ.ค. 2558/28)
    assert mc.conj_plus_i_modulus(12, 9)[1] == Fraction(7, 2)                        # กสพท คณิต1 (มี.ค. 2565/10)
    valid, _ = mc.imaginary_axis_roots(1, 1, 3)                                      # กสพท คณิต1 (มี.ค. 2561/13)
    assert sum(valid) == -1                                                          # the sum is −i
    a, b = mc.quadratic_from_root(3, -1)
    assert a + b == 4                                                                # กสพท คณิต1 (เม.ย. 2564/10)
    assert mc.poly_eval(mc.quartic_with_rational_root(1, 2), 2) == 15                # กสพท คณิต1 (มี.ค. 2563/26)
    assert mc.polar_distance_sq(1, 3, Fraction(1, 4)) == 5                           # กสพท คณิต1 (มี.ค. 2562/29): √5


def test_polynomial_solutions_match_sympy():
    x = sympy.symbols("x")
    ints = [Fraction(v) for v in range(-3, 4) if v] + [Fraction(u, 2) for u in (-3, -1, 1, 3)]
    for b in range(-4, 5):
        for c in range(b * b // 4 + 1, b * b // 4 + 7):
            for rats in ([ints[0]], [ints[2], ints[2]], [ints[7], ints[4]], [ints[5], ints[1]]):
                f = mc.factor_roots_poly(rats, b, c)
                p = sum(sympy.Integer(a) * x ** k for a, k in zip(f, range(len(f) - 1, -1, -1)))
                re, im, m = mc.complex_pair(b, c)
                mine = {R(r) for r in rats} | {R(re) + s * R(im) * sympy.sqrt(m) * IU for s in (1, -1)}
                theirs = set(sympy.roots(sympy.Poly(p, x)))
                assert {sympy.nsimplify(sympy.expand(v)) for v in mine} ==                        {sympy.nsimplify(sympy.expand(v)) for v in theirs}, (rats, b, c)


def test_textbook_polynomial_answers_reproduce():
    F = Fraction
    # แบบฝึกหัด 1.7 ข้อ 1.5: x⁴ − 6x³ + 15x² − 22x + 12 = 0 → {1, 3, 1 ± √3i}
    assert mc.factor_roots_poly([F(1), F(3)], -2, 4) == [1, -6, 15, -22, 12]
    assert mc.solution_set_tex([F(1), F(3)], mc.complex_pair(-2, 4)) == \
        r"\left\{1, 3, 1 + \sqrt{3}i, 1 - \sqrt{3}i\right\}"
    # แบบฝึกหัดท้ายบท ข้อ 28: x⁵ + 9x⁴ + 33x³ + 55x² + 42x + 12 = 0 → {−1, −3 ± √3i}
    assert mc.factor_roots_poly([F(-1)] * 3, 6, 12) == [1, 9, 33, 55, 42, 12]
    assert mc.complex_pair(6, 12) == (F(-3), F(1), 3)
    # แบบฝึกหัดท้ายบท ข้อ 21.6: 2x⁴ + x³ + 2x² − 19x − 10 = 0 → {−1/2, 2, −1 ± 2i}
    assert mc.factor_roots_poly([F(2), F(-1, 2)], 2, 5) == [2, 1, 2, -19, -10]
    assert mc.solution_set_tex([F(2), F(-1, 2)], mc.complex_pair(2, 5)) == \
        r"\left\{-\frac{1}{2}, 2, -1 + 2i, -1 - 2i\right\}"


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(120):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
