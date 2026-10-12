"""The ลอการิทึม sets built from the sheet bank's knowledge units.

Identities are checked with SymPy, every claimed solution is substituted
back into its equation, the inequality solvers are compared with SymPy's
solution sets, and the source exams' answers are pinned.
"""

from __future__ import annotations

import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m4 import logarithms as ml

sympy = pytest.importorskip("sympy")
X = sympy.Symbol("x", positive=True)
KEYS = ("math.log_mixed_bases_m5", "math.log_equation_advanced_m5", "math.log_inequality_m5")
log = sympy.log


def R(f: Fraction):
    return sympy.Rational(f.numerator, f.denominator)


def test_mixed_base_identities():
    for p in (2, 3):
        for k in range(1, 5):
            for c in (5, 7, 10, 11):
                v = log(p ** k * c, p) - log(c * c, p * p)
                assert sympy.simplify(v - ml.difference_with_squared_base(p, k, c)) == 0
    for a, b in ((2, 3), (2, 5), (3, 7), (5, 7)):
        for q in (1, 2, 3):
            N = (a * b) ** q
            v = 1 / log(N, a) + 1 / log(N, b)
            assert sympy.simplify(v - R(ml.reciprocal_sum(a, b, q))) == 0
    a, b = sympy.symbols("a b", positive=True)
    for m in (2, 3):
        for n in (2, 3):
            for v in range(2, 7):
                # log_(a^m) b = v means b = a^(m·v).
                assert sympy.simplify(log(a, (a ** (m * v)) ** n) - R(ml.swapped_power_bases(m, n, v))) == 0


def test_power_of_ten_solutions_satisfy_the_equation():
    for m in range(4):
        for n in range(m + 1, 4):
            for x in ml.power_of_ten_solutions(m, n):
                lx = log(x, 10)
                expr = 9 ** lx - (3 ** m + 3 ** n) * 3 ** lx + 3 ** (m + n)
                assert sympy.simplify(expr) == 0


def test_self_power_product():
    for b in (2, 3, 5):
        for j in range(1, 5):
            for k in range(1, 9):
                t = sympy.Symbol("t")
                roots = sympy.solve(t ** 2 - j * t - k, t)
                assert len(roots) == 2
                for r in roots:
                    xv = b ** r
                    assert sympy.simplify(xv ** log(xv, b) - b ** k * xv ** j) == 0
                assert sympy.simplify(b ** (roots[0] + roots[1]) - R(ml.self_power_product(b, k, j))) == 0


def _interval(iv):
    lo, hi = iv
    return sympy.Interval.open(R(lo), sympy.oo if hi is None else R(hi))


@pytest.mark.parametrize("below", (True, False))
def test_same_argument_inequality_matches_sympy(below):
    base, k = (sympy.Rational(1, 10), 2) if below else (sympy.Integer(3), 2)
    for c in range(-3, 6):
        xr = sympy.Symbol("x", real=True)
        sol = sympy.solveset(log(xr - c, base) < log(xr - c, base ** k), xr,
                             sympy.Interval.open(c, sympy.oo))
        assert sol == _interval(ml.same_argument_inequality(below, c))


@pytest.mark.parametrize("seed", range(60))
def test_linear_log_inequality_matches_sympy(seed):
    rng = random.Random(seed)
    a = rng.choice((Fraction(2), Fraction(3), Fraction(1, 2), Fraction(1, 3)))
    p, r = rng.randint(1, 4), rng.randint(1, 4)
    q, s = rng.randint(-6, 6), rng.randint(-6, 6)
    xr = sympy.Symbol("x", real=True)
    domain = sympy.Interval.open(max(sympy.Rational(-q, p), sympy.Rational(-s, r)), sympy.oo)
    # Compare arguments directly (monotonicity), then intersect with the domain.
    rel = (p * xr + q > r * xr + s) if a > 1 else (p * xr + q < r * xr + s)
    theirs = sympy.solveset(rel, xr, sympy.S.Reals).intersect(domain)
    ours = ml.linear_log_inequality(a, p, q, r, s)
    assert theirs == (sympy.S.EmptySet if ours is None else _interval(ours))


def test_exam_answers_reproduce():
    assert ml.difference_with_squared_base(2, 3, 5) == 3             # กสพท คณิต1 (มี.ค. 2563/5): log2 40 − log4 25
    assert ml.reciprocal_sum(2, 5, 2) == Fraction(1, 2)               # กสพท คณิต1 (มี.ค. 2561/6)
    assert ml.swapped_power_bases(2, 2, 5) == Fraction(1, 20)         # กสพท คณิต1 (ธ.ค. 2558/4)
    assert sum(ml.power_of_ten_solutions(0, 2)) == 101                # กสพท คณิต1 (ธ.ค. 2558/18)
    assert ml.same_argument_inequality(True, 1) == (Fraction(2), None)  # A-level 1 (มี.ค. 2567/7): x > 2


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(80):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
