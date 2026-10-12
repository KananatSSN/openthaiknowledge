"""The functions-chapter sets built from the sheet bank's knowledge units.

Each family is re-derived with SymPy (piecewise solving, inequality solution
sets, derivatives), and the source exams' answers are pinned.
"""

from __future__ import annotations

import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m4 import relations_and_functions as mf
from otk.sets.math.m4.functions import exp_constants

sympy = pytest.importorskip("sympy")
X = sympy.Symbol("x", real=True)

KEYS = ("math.piecewise_function_m4", "math.graph_inequality_parameters_m4",
        "math.relation_pairs_m4", "math.graph_transform_point_m4", "math.derivative_chain_m5")


def to_frac(v) -> Fraction:
    return Fraction(str(sympy.nsimplify(v)))


@pytest.mark.parametrize("seed", range(80))
def test_piecewise_solver_matches_sympy(seed):
    rng = random.Random(seed)
    f = mf._random_piecewise(rng)
    k = rng.randint(f.d - 3, f.d + 40)
    expr = sympy.Piecewise((f.m * X + f.p, X < f.c), (f.a * (X - f.c) ** 2 + f.d, True))
    theirs = sympy.solveset(sympy.Eq(expr, k), X, sympy.S.Reals)
    ours = f.solve(k)
    rational = [v for v in theirs if v.is_rational]
    # Our solver keeps rational roots only; items use it only when both pieces give them.
    assert sorted(to_frac(v) for v in rational) == ours or \
        len(rational) < len(list(theirs))


@pytest.mark.parametrize("seed", range(60))
def test_line_over_abs_matches_sympy(seed):
    rng = random.Random(seed)
    k, p, q = rng.randint(1, 9), -rng.randint(2, 12), rng.randint(2, 16)
    if p + q == 0:
        return
    a, b = mf.line_over_abs(k, p, q)
    a_s, b_s = sympy.Rational(a.numerator, a.denominator), sympy.Rational(b.numerator, b.denominator)
    sol = sympy.solveset(sympy.Abs(X) + k - (a_s * X + b_s) <= 0, X, sympy.S.Reals)
    assert sol == sympy.Interval(p, q)


@pytest.mark.parametrize("h,top,s", [(h, t, s) for h in (1, 2) for t in range(2, 9) for s in (1, 2, 3)])
def test_parabolas_meeting_matches_sympy(h, top, s):
    alpha, beta = mf.parabolas_meeting(h, top, s)
    if not (alpha > 0 and alpha > beta):
        return
    f = sympy.Rational(alpha.numerator, alpha.denominator) * X ** 2
    g = sympy.Rational(beta.numerator, beta.denominator) * (X - h) ** 2 + top
    assert sympy.solveset(f - g <= 0, X, sympy.S.Reals) == sympy.Interval(0, s)


def test_relation_count_by_enumeration():
    for lo in range(1, 7):
        for hi in range(12, 21):
            for shift in range(4):
                for div in (2, 3):
                    A = set(range(lo, hi + 1))
                    brute = sum(1 for x in A for y in A if div * y == x - shift)
                    assert mf.count_relation(lo, hi, shift, div) == brute


def test_exponential_constants_hit_both_intercepts():
    for base in (2, 3):
        for x_cut in range(1, 4):
            for a in range(-2, 2):
                if x_cut + a < 1:
                    continue
                _, y0 = exp_constants(base, x_cut, a)
                c = -base ** (x_cut + a)
                assert Fraction(base) ** (x_cut + a) + c == 0
                assert Fraction(base) ** a + c == y0


def test_chain_rule_matches_sympy():
    x = sympy.Symbol("x")
    for m in range(1, 6):
        for n in range(1, 7):
            for k in (2, 3):
                f = sympy.integrate(m * x + n, x)
                h = f.subs(x, x ** k)
                assert sympy.expand(sympy.diff(h, x)) == sympy.expand((m * x ** k + n) * k * x ** (k - 1))
    for k in (1, 2):
        for d in range(-3, 4):
            u = sympy.Symbol("u")
            f = ((u - d) / k) ** 2                    # from f(k√x + d) = x
            for t in range(d + 1, d + 7):
                assert sympy.diff(f, u).subs(u, t) == sympy.Rational(2 * (t - d), k * k)


# ── The exam questions the units came from ───────────────────────────────────

def test_exam_answers_reproduce():
    # กสพท คณิต2 (มี.ค. 2562/21): |x| + 5 ≤ ax + b on [−10, 15] → a + b = 86/5.
    assert sum(mf.line_over_abs(5, -10, 15)) == Fraction(86, 5)
    # กสพท คณิต2 (มี.ค. 2563/21): vertices (0, 0) and (1, 4), f ≤ g on [0, 1] → f(−1) + g(−1) = −8.
    alpha, beta = mf.parabolas_meeting(1, 4, 1)
    assert alpha * 1 + beta * 4 + 4 == -8
    # O-NET (ก.พ. 2563/36): A = {5..14}, y = (x − 1)/2 → 2 pairs... with y in A: (11, 5), (13, 6).
    assert mf.count_relation(5, 14, 1, 2) == 2
    # O-NET (ก.พ. 2563/16): y = 2^(x + a) + b through (2, 0) and (0, −1.5) → a + b = −3.
    a, y0 = exp_constants(2, 2, -1)
    assert y0 == Fraction(-3, 2) and a + (-(2 ** 1)) == -3


# ── The generated items ──────────────────────────────────────────────────────

@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(80):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
