"""The sequence, series and compounding sets built from the sheet bank's knowledge units.

Every closed form is recomputed term by term (or with SymPy's summation for
the infinite series), and the source exams' answers are pinned.
"""

from __future__ import annotations

import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m6 import arithmetic_sequences as ms
from otk.sets.math.m6.geometric import (
    infinite_from_blocks,
    ratio_from_alternating,
    ratio_from_two_conditions,
    squares_from_sums,
)
from otk.sets.math.m6.series import (
    fibonacci_like_sum,
    median_of_reciprocals,
    telescoping_infinite,
    weighted_power_sum_parts,
)
from otk.sets.math.m5.sequences_and_series import (
    RATE_PLANS,
    dec,
    interest_earned,
    money,
    per_period,
)

sympy = pytest.importorskip("sympy")
KEYS = ("math.arithmetic_series_tricks_m6", "math.sequence_patterns_m6", "math.geometric_series_tricks_m6",
        "math.telescoping_series_m6", "math.compounding_periods_m5", "math.sequence_terms_m6")


def R(v):
    v = Fraction(v)
    return sympy.Rational(v.numerator, v.denominator)


def _ap(a1, d, n):
    return [Fraction(a1) + k * Fraction(d) for k in range(n)]


def test_arithmetic_tricks():
    for a1 in (-3, 0, 5):
        for d in (Fraction(1, 2), Fraction(-4, 5), Fraction(2)):
            for n in range(2, 30):
                t = _ap(a1, d, n)
                assert ms.alternating_sum(Fraction(a1), d, n) == sum(v if k % 2 == 0 else -v for k, v in enumerate(t))
                if n % 2 == 0:
                    assert ms.alternating_square_sum(Fraction(a1), d, n) == \
                        sum(v * v if k % 2 == 0 else -v * v for k, v in enumerate(t))
                for p in range(1, n):
                    assert ms.range_sum(Fraction(a1), d, p, n) == sum(t[p - 1:n])
    for c, d, rho in ms.EXP_BASES:
        assert round(c ** float(d)) == rho
        for j in range(-3, 2):
            for n in range(5, 11):
                terms = [Fraction(rho) ** (j + k) for k in range(n)]        # bₖ = c^(aₖ), aₖ = (j + k − 1)d
                assert ms.exp_sum(rho, j, n) == sum(terms)


def test_patterns():
    for a1, d1, e in ((7, 2, 1), (1, 1, 1), (3, 4, 2)):
        seq = [a1]
        gap = d1
        for _ in range(60):
            seq.append(seq[-1] + gap)
            gap += e
        for n in range(1, 60):
            assert ms.second_difference_term(a1, d1, e, n) == seq[n - 1]
    for p in (1, 2, 3):
        for q in (-5, 0, 4):
            s = lambda n: p * n * n + q * n
            for k in range(2, 50):
                assert ms.term_from_partial_sums(p, q, k) == s(k) - s(k - 1)
    for s in (3, 10):
        for d in (1, 3):
            a = [None, 1, s - 1]
            for n in range(1, 60):
                a.append(a[n] + d)
            for m in range(1, 25):
                assert ms.paired_recurrence_sum(s, d, m) == sum(a[1:2 * m + 1])
    for a1 in (-6, 2, 9):
        for d in (1, 4):
            for m in range(6, 15):
                t = _ap(a1, d, m + 1)
                assert ms.previous_partial_sum(int(sum(t[:m])), int(sum(t)), m) == sum(t[:m - 1])
    nums = iter(range(1, 10_000))
    for k in range(1, 70):
        row = [next(nums) for _ in range(k)]
        assert ms.triangle_row(k) == (row[0], sum(row))


def _gp(a, r, n):
    return [Fraction(a) * Fraction(r) ** k for k in range(n)]


def test_geometric_tricks():
    for r in (2, 3, -2, 4):
        for a in (Fraction(25, 4), Fraction(3)):
            t = _gp(a, r, 10)
            assert ratio_from_two_conditions(t[6] - t[4], t[5] + t[4]) == r
    for r in (Fraction(-2, 15), Fraction(1, 3), Fraction(-1, 5)):
        t = _gp(Fraction(7), r, 12)
        total, alt = sum(t), sum(v if k % 2 == 0 else -v for k, v in enumerate(t))
        assert ratio_from_alternating(total, alt) == r
    n = sympy.Symbol("n", integer=True, positive=True)
    for a in (Fraction(1, 2), Fraction(3)):
        for r in (Fraction(1, 3), Fraction(-2, 3), Fraction(1, 4)):
            s = a / (1 - r)
            t = -a / (1 + r)
            sq = sympy.summation(R(a) ** 2 * R(r) ** (2 * (n - 1)), (n, 1, sympy.oo))
            assert R(squares_from_sums(s, t)) == sq
    for tt in (Fraction(1, 2), Fraction(2, 3), Fraction(-1, 2)):
        r = sympy.root(R(tt), 5) if tt > 0 else -sympy.root(R(-tt), 5)
        a = R(4) * (1 - r) / (1 - r ** 5)                  # S₅ = 4
        s15 = a * (r ** 5 - r ** 15) / (1 - r)
        assert sympy.simplify(s15 - 4 * R(tt) * (1 + R(tt))) == 0
        assert sympy.simplify(a / (1 - r) - R(infinite_from_blocks(Fraction(4), tt))) == 0


def test_telescoping():
    n = sympy.Symbol("n", integer=True, positive=True)
    for c in (1, 2, 6):
        for p in range(0, 4):
            for k in range(1, 4):
                exact = sympy.summation(R(c) / ((n + p) * (n + p + k)), (n, 1, sympy.oo))
                assert sympy.simplify(exact - R(telescoping_infinite(c, p, k))) == 0
    for a1, a2 in ((1, 3), (2, 5), (4, 7)):
        a = [a1, a2]
        while len(a) < 80:
            a.append(a[-1] + a[-2])
        partial = sum(Fraction(a[i], a[i - 1] * a[i + 1]) for i in range(1, 78))
        assert abs(float(partial - fibonacci_like_sum(a1, a2))) < 1e-12
    for m in range(8, 31, 2):
        data = sorted(Fraction(1, k * (k + 1)) for k in range(1, m + 1))
        assert median_of_reciprocals(m) == (data[m // 2 - 1] + data[m // 2]) / 2
        assert sum(data) / m == Fraction(1, m + 1)
    for N in (20, 50, 100):
        a, e, c = weighted_power_sum_parts(N)
        assert sum(k * 2 ** k for k in range(1, N + 1)) == a * 2 ** e + c


def test_money_helpers():
    assert dec(Fraction(1009, 1000)) == "1.009"
    assert money(Fraction(30601, 10)) == "3{,}060.1"
    assert money(Fraction(603)) == "603"
    assert interest_earned(30_000, per_period(Fraction(3), 3), 2) == 603
    for rate, k in RATE_PLANS:
        i = per_period(rate, k)
        assert len(dec(1 + i)) <= 7


def test_exam_answers_reproduce():
    assert ms.alternating_sum(Fraction(5), Fraction(1, 2), 21) == 10                   # กสพท คณิต2 (มี.ค. 2563/23)
    assert ms.alternating_square_sum(Fraction(5), Fraction(2), 50) == -5400           # กสพท คณิต1 (มี.ค. 2561/20)
    assert ms.range_sum(Fraction(19), Fraction(2), 7, 15) == 351                      # A-level 2 (มี.ค. 2566/27)
    assert ms.exp_sum(2, -3, 10) == Fraction(1023, 8)                                 # กสพท คณิต2 (ธ.ค. 2559/24)
    assert ms.second_difference_term(7, 2, 1, 40) == 826                              # กสพท คณิต2 (มี.ค. 2562/18)
    assert ms.second_difference_term(1, 1, 1, 50) == 1226                             # O-NET (ก.พ. 2560/15)
    assert ms.term_from_partial_sums(2, 0, 100) == 398                                # กสพท คณิต2 (มี.ค. 2565/9)
    assert ms.paired_recurrence_sum(10, 3, 20) == 1340                                # กสพท คณิต2 (ธ.ค. 2558/22)
    assert ms.previous_partial_sum(55, 77, 10) == 36                                  # กสพท คณิต2 (มี.ค. 2562/22)
    assert ms.triangle_row(50) == (1226, 62525)                                       # O-NET (ก.พ. 2560/24), (มี.ค. 2561/23)
    assert ratio_from_two_conditions(Fraction(50), Fraction(25)) == 3              # กสพท คณิต2 (ธ.ค. 2559/7)
    assert ratio_from_alternating(Fraction(13), Fraction(17)) == Fraction(-2, 15)  # กสพท คณิต2 (มี.ค. 2562/24)
    assert squares_from_sums(Fraction(1), Fraction(-2, 3)) == Fraction(2, 3)       # กสพท คณิต1 (มี.ค. 2562/20)
    assert infinite_from_blocks(Fraction(4), Fraction(1, 2)) == 8                  # กสพท คณิต1 (มี.ค. 2563/29)
    assert fibonacci_like_sum(1, 3) == Fraction(4, 3)                              # กสพท คณิต1 (เม.ย. 2564/24)
    assert median_of_reciprocals(20) == Fraction(1, 120)                           # กสพท คณิต1 (มี.ค. 2563/28): mean 1/21


def test_recursions_match_sympy():
    n = sympy.Symbol("n", integer=True)
    for a1 in (1, 4):
        for p, q in ((2, 3), (3, -1), (-2, 2)):
            closed = sympy.rsolve(sympy.Function("a")(n) - p * sympy.Function("a")(n - 1) - q,
                                  sympy.Function("a")(n), {sympy.Function("a")(1): a1})
            for k in range(1, 9):
                assert R(ms.recur_linear(Fraction(a1), Fraction(p), Fraction(q), k)) == closed.subs(n, k)
    for a1, a2, c in ((1, 2, 2), (2, 0, 1), (3, 4, -1), (1, 1, 3)):
        terms = [a1, a2]
        while len(terms) < 9:
            terms.append(terms[-1] + c * terms[-2])
        assert [ms.recur_two(a1, a2, c, k) for k in range(1, 10)] == terms
    for make in ms.GENERAL_TERMS:
        tex, f = make(2, 3)
        assert all(f(k) == f(k) for k in range(1, 6)) and tex


def test_textbook_recursions_reproduce():
    # (สสวท) 0 พื้นฐานลำดับ, แบบฝึกหัด 1.1.1 item 2
    assert [ms.recur_linear(Fraction(1000), Fraction(1, 20), Fraction(1), k) for k in range(1, 6)] ==         [1000, 51, Fraction(71, 20), Fraction(471, 400), Fraction(8471, 8000)]
    assert [ms.recur_linear(Fraction(2), Fraction(6), Fraction(0), k) for k in range(1, 6)] == [2, 12, 72, 432, 2592]
    assert [ms.recur_two(1, 2, 2, k) for k in range(1, 6)] == [1, 2, 4, 8, 16]
    assert [ms.recur_two(2, 0, 1, k) for k in range(1, 6)] == [2, 0, 2, 2, 4]


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(120):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
