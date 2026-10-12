"""The real-numbers-chapter sets built from the sheet bank's knowledge units.

Every family is re-solved with SymPy, a route that shares nothing with the
generators' exact scans and piecewise solver. The source exams' answers are
pinned.
"""

from __future__ import annotations

import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m4 import polynomial_division as mr
from otk.sets._support.math_bank_real import count_integers
from otk.sets.math.m4.absolute_value import _abs_family, solve_abs_linear, solve_abs_via_square
from otk.sets.math.m4.quadratic_inequalities import _ineq_family
from otk.sets.math.m3.inequality import _ORDER_CLAIMS, always_order
from otk.sets.math.m3.quadratic import largest_negative_no_real, pairs_with_real_roots

sympy = pytest.importorskip("sympy")
X = sympy.Symbol("x", real=True)

KEYS = ("math.inequality_integer_count_m4", "math.inequality_parameters_m4",
        "math.absolute_value_multi_equation_m4", "math.absolute_value_integer_count_m4",
        "math.polynomial_unknown_coefficients_m4", "math.inequality_order_properties_m3",
        "math.quadratic_discriminant_m3", "math.remainder_arithmetic_m4")


def sympy_integer_count(plain: str) -> int:
    rel = sympy.sympify(plain, locals={"x": X})
    parts = rel.args if isinstance(rel, sympy.And) else (rel,)
    solution = sympy.S.Reals
    for part in parts:                     # solveset takes one relation at a time
        solution = solution.intersect(sympy.solveset(part, X, sympy.S.Reals))
    hits = solution.intersect(sympy.Range(-400, 401))
    return len(list(hits))


@pytest.mark.parametrize("seed", range(60))
def test_integer_count_families_match_sympy(seed):
    rng = random.Random(seed)
    tex, pred, _, plain = _ineq_family(rng)
    assert count_integers(pred) == sympy_integer_count(plain), (tex, plain)
    family = None
    while family is None:
        family = _abs_family(rng)
    tex, pred, _, plain = family
    assert count_integers(pred) == sympy_integer_count(plain), (tex, plain)


@pytest.mark.parametrize("seed", range(80))
def test_piecewise_solver_matches_sympy(seed):
    rng = random.Random(seed)
    a, k, b, c = rng.randint(-3, 9), rng.choice((1, 2, 3, 4)), rng.randint(-5, 9), rng.randint(0, 24)
    terms = [(Fraction(1), Fraction(1), Fraction(-a)), (Fraction(1), Fraction(k), Fraction(-b))]
    ours = solve_abs_linear(terms, Fraction(0), Fraction(c))
    theirs = sympy.solveset(sympy.Abs(X - a) + sympy.Abs(k * X - b) - c, X, sympy.S.Reals)
    if ours is None:
        assert not theirs.is_FiniteSet
    else:
        assert theirs.is_FiniteSet
        assert sorted(Fraction(str(v)) for v in theirs) == ours


@pytest.mark.parametrize("n", [m * (m + 1) for m in range(3, 13)])
def test_abs_square_solver_matches_sympy(n):
    theirs = sympy.solveset(sympy.Abs(X ** 2 - n) - X, X, sympy.S.Reals)
    assert sorted(Fraction(str(v)) for v in theirs) == solve_abs_via_square(n)


def test_coefficient_solvers_match_sympy():
    x = sympy.Symbol("x")
    rng = random.Random(3)
    for _ in range(40):
        lead, roots = rng.choice((1, 2, 3)), rng.sample(range(-5, 6), 3)
        poly = sympy.Poly(lead * sympy.prod([x - r for r in roots]), x)
        assert mr.solve_sum_from_roots(lead, roots) == sum(poly.all_coeffs()[1:])
        s, t = rng.randint(-6, 6), rng.randint(2, 9)
        m = rng.choice([v for v in range(-6, 7) if v])
        a, b = mr.solve_quadratic_factor(s, t, t * m)
        assert sympy.rem(x ** 3 + a * x ** 2 + b * x + t * m, x ** 2 - s * x + t, x) == 0
        coeffs = [rng.randint(-5, 5) for _ in range(4)]
        p = coeffs[0] * x ** 5 + coeffs[1] * x ** 3 + coeffs[2] * x + coeffs[3]
        assert mr.solve_odd_remainder(int(p.subs(x, 1)), coeffs[3]) == p.subs(x, -1)


def test_order_properties_known_verdicts():
    lt = lambda a, b, c: a < b
    neg_c = lambda a, b, c: a < b and c < 0
    claims = dict(_ORDER_CLAIMS)
    assert always_order(lt, claims[r"a + c < b + c"])
    assert not always_order(lt, claims[r"a^{2} < b^{2}"])
    assert not always_order(lt, claims[r"|a| < |b|"])
    assert always_order(neg_c, claims[r"ac > bc"])
    assert always_order(lambda a, b, c: 0 < a < b, claims[r"\frac{1}{a} > \frac{1}{b}"])
    assert always_order(lt, claims[r"a^{3} < b^{3}"])


def test_discriminant_counts():
    for n in range(2, 9):
        brute = sum(1 for b in range(1, n + 1) for c in range(1, n + 1)
                    if sympy.discriminant(X ** 2 + b * X + c, X) >= 0)
        assert pairs_with_real_roots(n) == brute


# ── The exam questions the units came from ───────────────────────────────────

def test_exam_answers_reproduce():
    # กสพท คณิต1 (ธ.ค. 2558/1): 6|x − 3| < 5x has 16 integer solutions.
    assert count_integers(lambda x: 6 * abs(x - 3) < 5 * x) == 16
    # กสพท คณิต2 (ธ.ค. 2559/13): (x − 5)² − |x − 5| < 30 has 11.
    assert count_integers(lambda x: (x - 5) ** 2 - abs(x - 5) < 30) == 11
    # กสพท คณิต2 (มี.ค. 2563/12): x²(3 − 2x)(x + 11) ≥ 0 has 13.
    assert count_integers(lambda x: x * x * (3 - 2 * x) * (x + 11) >= 0) == 13
    # กสพท คณิต2 (มี.ค. 2562/13): −6 < x(x + 5) < 24 has 8.
    assert count_integers(lambda x: -6 < x * (x + 5) < 24) == 8
    # กสพท คณิต1 (มี.ค. 2562/11): |x² − 72| = x, the solutions sum to 17.
    assert sum(solve_abs_via_square(72)) == 17
    # กสพท คณิต2 (มี.ค. 2563/11): |x − 7| + |4x − 3| = 18 with 1 < x < 5 gives 14/3.
    sols = solve_abs_linear([(Fraction(1), Fraction(1), Fraction(-7)),
                                (Fraction(1), Fraction(4), Fraction(-3))], Fraction(0), Fraction(18))
    assert [s for s in sols if 1 < s < 5] == [Fraction(14, 3)]
    # กสพท คณิต1 (ธ.ค. 2559/1): 2x³ + … with factors x + 1, x + 2, x + 3 → a + b + c = 46.
    assert mr.solve_sum_from_roots(2, [-1, -2, -3]) == 46
    # กสพท คณิต1 (ธ.ค. 2558/2): P(1) = 10, P(0) = 6 → P(−1) = 2.
    assert mr.solve_odd_remainder(10, 6) == 2
    # กสพท คณิต1 (เม.ย. 2564/9): x² − 4x + 5 | x³ + ax² + bx + 30 → a + b = −17.
    assert sum(mr.solve_quadratic_factor(4, 5, 30)) == -17
    # กสพท คณิต2 (มี.ค. 2563/20): (b, c) ∈ {1..4}² with real roots → 7.
    assert pairs_with_real_roots(4) == 7
    # กสพท คณิต1 (มี.ค. 2565/5): largest negative a with a²x² + 9x + 1 having no real root → −5.
    assert largest_negative_no_real(9) == -5


# ── The generated items ──────────────────────────────────────────────────────

def test_remainders_by_brute_force():
    import math
    for m in range(2, 14):
        for n in range(1, 25):
            total = sum(math.factorial(k) for k in range(1, n + 1))
            assert mr.factorial_sum_mod(n, m) == total % m
            assert mr.factorial_sum_mod(n, m, 2) == total ** 2 % m
        for a in range(2, 14):
            if math.gcd(a, m) == 1:
                cyc = mr.power_cycle(a, m)
                for n in range(1, 60):
                    assert cyc[(n - 1) % len(cyc)] == pow(a, n, m)
        for ra in range(m):
            for rb in range(m):
                a, b, c = ra + 3 * m, rb + 5 * m, (ra + rb) % m + 7 * m
                assert mr.combined_remainder(ra, rb, (ra + rb) % m, m) == (a * a * b + c) % m


def test_remainder_exam_answer():
    assert mr.factorial_sum_mod(10, 5, 2) == 4          # วิชาสามัญ คณิตศาสตร์ 1 (มี.ค. 2562/12)


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(60):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
