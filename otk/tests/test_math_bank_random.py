"""The random-variable sets built from the sheet bank's knowledge units.

Table entries are checked against math.erf, inverse normal problems by
substituting back, game values by enumerating every draw, and the source
exams' answers are pinned.
"""

from __future__ import annotations

import math
import random
from decimal import Decimal
from fractions import Fraction
from itertools import combinations

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m6 import probability_distributions as mr

KEYS = ("math.normal_z_table_m6", "math.expected_game_value_m6", "math.random_variable_variance_m6")


def test_phi_table():
    for z in mr.Z_STEPS:
        exact = 0.5 * (1 + math.erf(float(z) / math.sqrt(2)))
        assert abs(float(mr.phi(z)) - exact) <= 0.00005 + 1e-12
    assert mr.phi(Decimal("1.00")) == Decimal("0.8413")
    assert mr.phi(Decimal("1.04")) == Decimal("0.8508")


def test_between_symmetry():
    for z in mr.Z_STEPS[:20]:
        assert mr.between(-z, z) == 2 * mr.phi(z) - 1


def test_equal_z_score():
    for m1, s1, m2, s2 in ((60, 8, 65, 6), (55, 10, 70, 4)):
        for d in range(-10, 11):
            x1 = mr.equal_z_score(m1, s1, m2, s2, d)
            x2 = x1 + d
            assert (x1 - m1) / s1 == (x2 - m2) / s2


def test_mean_sd_from_tails():
    for z in mr.Z_STEPS[:20]:
        mu, sd = Decimal("8.88"), Decimal("0.04")
        a, b = mu - z * sd, mu + z * sd
        assert mr.mean_sd_from_tails(a, b, z) == (mu, sd)


def test_expected_profit_by_enumeration():
    for n in range(5, 11):
        pairs = list(combinations(range(1, n + 1), 2))
        p = Fraction(sum(a * b % 2 == 0 for a, b in pairs), len(pairs))
        assert mr.even_product_probability(n) == p


def test_exam_answers_reproduce():
    assert 80 + Decimal("1.04") * 3 == Decimal("83.12")                                          # กสพท คณิต1 (เม.ย. 2564/4)
    assert mr.equal_z_score(60, 8, 65, 6, 2) == 72                                               # กสพท คณิต1 (มี.ค. 2561/23)
    mu, sd = mr.mean_sd_from_tails(Decimal("8.86"), Decimal("8.90"), Decimal("0.5"))
    assert mu + 2 * sd == Decimal("8.96")                                                        # A-level 1 (มี.ค. 2566/28)
    assert mr.expected_profit(9, 90, 180) == 40                                                  # กสพท คณิต1 (เม.ย. 2564/21)
    assert 1 - mr.phi(Decimal("1.00")) == Decimal("0.1587")                                      # กสพท คณิต1 (ธ.ค. 2559/21)


def test_variance_matches_sympy():
    from sympy import Rational
    from sympy.stats import FiniteRV, variance
    rng = random.Random(7)
    for i in range(40):
        counts = {x: rng.randint(0, 9) for x in rng.sample(range(-3, 10), 4)}
        if sum(counts.values()) == 0:
            continue
        dist = mr.from_counts(counts)
        X = FiniteRV(f"X{i}", {x: Rational(p.numerator, p.denominator) for x, p in dist.items()})
        assert Rational(*mr.mean_var(dist)[1].as_integer_ratio()) == variance(X)
    for p, d in mr.SQUARE_SPREADS:
        var = mr.mean_var({-d: p, 0: 1 - 2 * p, d: p})[1]
        assert math.isqrt(var.numerator) ** 2 == var.numerator and math.isqrt(var.denominator) ** 2 == var.denominator


def test_textbook_variance_answers_reproduce():
    quiz = mr.from_counts(dict(zip(range(11), (0, 1, 2, 5, 6, 3, 8, 7, 3, 3, 2))))
    mu, var = mr.mean_var(quiz)
    assert mu == Fraction(227, 40) and round(float(var), 2) == 5.07                  # 4.2ข item 1 (X)
    days = mr.from_counts(dict(zip(range(8), (1, 7, 10, 12, 6, 3, 4, 1))))
    mu, var = mr.mean_var(days)
    assert mu == Fraction(133, 44) and round(float(var), 2) == 2.66                  # ท้ายบท item 2
    assert mr.mean_var({0: Fraction(4, 9), 1: Fraction(4, 9), 2: Fraction(1, 9)}) == (Fraction(2, 3), Fraction(4, 9))  # ท้ายบท item 3


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(150):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
