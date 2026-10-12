"""The exponents-chapter sets built from the sheet bank's knowledge units.

Each family is checked with SymPy, including real roots of negative numbers
and numeric equality of denested radicals. The source exams' answers are
pinned.
"""

from __future__ import annotations

import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m4 import exponential as mp
from otk.sets.math.m5.radicals_and_exponents import order_tex, rational_power
from otk.sets._support.math_bank_powers import _ROOT_FACTS
from otk.sets.math.m4.simplifying_radicals import denest

sympy = pytest.importorskip("sympy")
X = sympy.Symbol("x", real=True)

KEYS = ("math.exponential_equation_advanced_m4", "math.rational_power_evaluate_m5",
        "math.root_sign_properties_m5", "math.power_compare_m5", "math.radical_denest_m4")


def test_factored_and_substitution_solvers_match_sympy():
    for a in (2, 3, 5):
        for x in range(2, 6):
            total = a ** (x + 1) + a ** x + a ** (x - 1)
            assert mp.solve_factored(a, total) == x
    for a in (2, 3):
        for m in range(5):
            for n in range(m + 1, 5):
                eq = a ** (2 * X) - (a ** m + a ** n) * a ** X + a ** (m + n)
                theirs = sorted(int(v) for v in sympy.solveset(eq, X, sympy.S.Reals))
                assert theirs == mp.substitution_solutions(a, m, n)


def test_rational_powers_match_sympy_real_roots():
    for n in (2, 3, 5):
        for sign in ((1, -1) if n % 2 else (1,)):
            for p, q in ((1, 2), (1, 3), (2, 3), (1, 5), (2, 1), (3, 1)):
                for m in [v for v in range(-3, 4) if v and v % n]:
                    base = sympy.Rational(sign * p ** n, q ** n)
                    theirs = sympy.real_root(base, n) ** m
                    assert sympy.nsimplify(theirs) == sympy.Rational(*_pair(rational_power(sign, p, q, n, m)))


def _pair(f: Fraction) -> tuple[int, int]:
    return f.numerator, f.denominator


def test_root_sign_verdicts_hold_numerically():
    samples = {"a เป็นจำนวนจริงลบ": (-2, -sympy.Rational(1, 3), -7),
               "a เป็นจำนวนจริงบวก": (2, sympy.Rational(1, 3), 7)}
    def value(claim: str, v):
        lhs, rhs = claim.split(" = ")
        return _eval(lhs, v), _eval(rhs, v)
    for premise, claims in _ROOT_FACTS:
        for claim, verdict in claims:
            holds = all(sympy.simplify(lhs - rhs) == 0 for lhs, rhs in (value(claim, v) for v in samples[premise]))
            assert holds == verdict, (premise, claim)


def _eval(tex: str, v):
    """The handful of TeX shapes the claims use, evaluated with real roots."""
    rr = sympy.real_root
    table = {
        r"\sqrt{a^{2}}": lambda: rr(v ** 2, 2), r"\sqrt[3]{a^{3}}": lambda: rr(v ** 3, 3),
        r"\sqrt[4]{a^{4}}": lambda: rr(v ** 4, 4), r"\sqrt[5]{-a^{5}}": lambda: rr(-v ** 5, 5),
        r"\sqrt[3]{(-a)^{3}}": lambda: rr((-v) ** 3, 3), r"\sqrt{(-a)^{2}}": lambda: rr((-v) ** 2, 2),
        r"a^{\frac{1}{2}} \cdot a^{\frac{1}{3}}": lambda: rr(v, 2) * rr(v, 3),
        r"(-a)^{\frac{2}{3}}": lambda: rr(-v, 3) ** 2, r"a^{\frac{5}{6}}": lambda: rr(v, 6) ** 5,
        r"a^{\frac{1}{6}}": lambda: rr(v, 6), r"a^{\frac{2}{3}}": lambda: rr(v, 3) ** 2,
        "a": lambda: v, "-a": lambda: -v, "|a|": lambda: abs(v),
    }
    return table[tex]()


def test_power_order_matches_big_integers():
    assert order_tex([2 ** 50, 3 ** 30, 5 ** 20]) == "c < b < a"      # กสพท คณิต2 (มี.ค. 2563/14)
    assert order_tex([6 ** 12, 2 ** 9 * 3 ** 14, 2 ** 15 * 3 ** 10]) == "c < a < b"  # O-NET (มี.ค. 2561/4)


@pytest.mark.parametrize("m,n", [(m, n) for m in range(2, 13) for n in range(1, m)])
def test_denest_matches_sympy(m, n):
    for plus in (True, False):
        inner = m + n + (2 if plus else -2) * sympy.sqrt(m * n)
        ours = sympy.sqrt(m) + (1 if plus else -1) * sympy.sqrt(n)
        assert sympy.simplify(sympy.sqrt(inner) - ours) == 0


def test_exam_answers_reproduce():
    # กสพท คณิต2 (ธ.ค. 2558/2): √(3 + 2√2) = 1 + √2.
    assert denest(2, 1, True) == r"\sqrt{2} + 1"
    # กสพท คณิต2 (มี.ค. 2563/2): (−1/32)^(−3/5) = −8.
    assert rational_power(-1, 1, 2, 5, -3) == -8
    # กสพท คณิต2 (ธ.ค. 2559/4) shape: 5^(x+1) + 5^x + 5^(x−1) with x = 3.
    assert mp.solve_factored(5, 5 ** 4 + 5 ** 3 + 5 ** 2) == 3


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(80):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()


@pytest.mark.parametrize("a", [Fraction(1, 2), Fraction(1, 3), Fraction(2), Fraction(3)])
def test_exponential_inequality_matches_sympy(a):
    rng = random.Random(int(a * 6))
    base = sympy.Rational(a.numerator, a.denominator)
    for _ in range(40):
        p, q, r, s = rng.randint(1, 4), rng.randint(-5, 5), rng.randint(-3, 3), rng.randint(-5, 5)
        if p == r:
            continue
        t, greater = mp.solve_exp_inequality(a, p, q, r, s)
        theirs = sympy.solveset(base ** (p * X + q) > base ** (r * X + s), X, sympy.S.Reals)
        t_s = sympy.Rational(t.numerator, t.denominator)
        # SymPy may leave the endpoint as a log expression; compare it simplified.
        assert theirs.is_Interval
        end = theirs.inf if greater else theirs.sup
        assert sympy.simplify(end - t_s) == 0
        assert (theirs.sup == sympy.oo) == greater and (theirs.inf == -sympy.oo) == (not greater)
