"""The statistics sets built from the sheet bank's knowledge units.

Measures are rechecked with the standard ``statistics`` module, hidden data
by brute force, and the source exams' answers are pinned.
"""

from __future__ import annotations

import random
import statistics
from fractions import Fraction
from itertools import product

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m6 import measures_of_central_tendency as ms
from otk.sets._support.math_bank_stats import median, modes
from otk.sets.math.m6.measures_of_dispersion import (
    pooled_variance,
    variance_from_shifted_squares,
    weighted_abs_min,
)

KEYS = ("math.stats_data_conditions_m6", "math.stats_transform_m6")


def test_measures_match_statistics_module():
    rng = random.Random(1)
    for _ in range(200):
        xs = [rng.randint(0, 12) for _ in range(rng.randint(3, 11))]
        assert ms.mean(xs) == Fraction(statistics.fmean(xs)).limit_denominator(1000)
        assert median(xs) == Fraction(statistics.median(xs))
        assert modes(xs) == sorted(statistics.multimode(xs))


def test_matching_sets_brute_force():
    for n, hi in ((4, 8), (5, 7)):
        for data in product(range(1, hi + 1), repeat=n):
            s = tuple(sorted(data))
            mo = ms.unique_mode(s)
            if mo is None:
                continue
            assert s in ms.matching_sets(n, hi, mo, median(s), s[-1] - s[0])
            break


def test_transform_formulas():
    rng = random.Random(2)
    for _ in range(50):
        xs = [Fraction(rng.randint(-10, 30)) for _ in range(rng.randint(5, 15))]
        n, m = len(xs), ms.mean(xs)
        var = sum((x - m) ** 2 for x in xs) / n
        c = Fraction(rng.randint(-5, 25))
        assert variance_from_shifted_squares(n, m, c, sum((x - c) ** 2 for x in xs)) == var
        ys = [Fraction(rng.randint(0, 20)) for _ in range(rng.randint(3, 9))]
        my = ms.mean(ys)
        both = xs + ys
        mb = ms.mean(both)
        pooled = pooled_variance([(n, m, sum((x - m) ** 2 for x in xs)),
                                     (len(ys), my, sum((y - my) ** 2 for y in ys))])
        assert pooled == sum((v - mb) ** 2 for v in both) / len(both)


def test_weighted_abs_min():
    rng = random.Random(3)
    for _ in range(100):
        pts = [(a, rng.choice((1, 2))) for a in sorted({rng.randint(-3, 9) for _ in range(6)})]
        _, best = weighted_abs_min(pts)
        grid = [Fraction(k, 4) for k in range(-20, 50)]
        assert best == min(sum(w * abs(a - x) for a, w in pts) for x in grid)


def test_exam_answers_reproduce():
    known = [Fraction(v) for v in ("12", "14", "12.5", "11", "9.5", "8", "10", "11.5", "10.5")]
    assert ms.x_for_mean_equals_mode(known) == [11]                                   # กสพท คณิต2 (ธ.ค. 2558/8)
    known = [10, 11, 10, 15, 12, 14, 10, 13, 16]
    xs = ms.x_for_median_minus_mode(known, 2, 1, 20)                                  # กสพท คณิต2 (ธ.ค. 2559/29)
    assert xs == [12] and ms.mean([*known, 12]) == Fraction(123, 10)
    sets = ms.matching_sets(4, 20, 6, Fraction(5), 4)                                 # O-NET (ก.พ. 2560/28)
    assert {sum(s) for s in sets} == {18}
    sets = ms.matching_sets(5, 15, 5, Fraction(6), 7)                                 # O-NET (มี.ค. 2564/31)
    assert max(s[-1] for s in sets) == 12
    assert variance_from_shifted_squares(11, Fraction(22), Fraction(24), Fraction(1034)) == 90  # A-level 2 (มี.ค. 2567/26)
    assert Fraction(11, 10) * 4 + Fraction(1, 4) == Fraction(465, 100)               # กสพท คณิต2 (มี.ค. 2563/9)


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(120):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
