"""The sets for gaps the 🍰 lecture books exposed (Σ sums, radical equations,
stars and bars): sums term by term, roots substituted back, distributions
counted by enumeration."""

from __future__ import annotations

import math
import random
from itertools import product

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m6 import series as mn
from otk.sets.math.m4.simplifying_radicals import nested_value, radical_roots
from otk.sets.math.m5.counting_principles import distributions

KEYS = ("math.sigma_sums_m6", "math.radical_equation_m4", "math.stars_bars_m5")


def test_sum_formulas():
    for n in range(0, 40):
        assert mn.s1(n) == sum(range(1, n + 1))
        assert mn.s2(n) == sum(k * k for k in range(1, n + 1))
        assert mn.s3(n) == sum(k ** 3 for k in range(1, n + 1))
    for a, b, c in ((1, 0, 0), (3, -5, 6), (2, 4, -4)):
        for lo in range(1, 8):
            for hi in range(lo, 25):
                assert mn.poly_sum(a, b, c, lo, hi) == sum(a * k * k + b * k + c for k in range(lo, hi + 1))


def test_radical_roots_substitute_back():
    for a in range(-10, 20):
        for b in range(-10, 60):
            for c in range(-6, 7):
                valid, bad = radical_roots(a, b, c)
                for x in valid:
                    assert a * x + b >= 0 and math.isqrt(a * x + b) ** 2 == a * x + b
                    assert math.isqrt(a * x + b) == x + c
                for x in bad:
                    assert (x + c) ** 2 == a * x + b and x + c < 0      # squares fine, but √ ≠ negative


def test_nested_radical():
    for m in range(2, 10):
        a = m * (m - 1)
        x = 0.0
        for _ in range(200):
            x = math.sqrt(a + x)
        assert abs(x - nested_value(m)) < 1e-9


def test_stars_and_bars_by_enumeration():
    for n in range(0, 9):
        for k in range(1, 5):
            for low in (0, 1):
                brute = sum(sum(v) == n for v in product(range(low, n + 1), repeat=k))
                assert distributions(n, k, low) == brute


def test_book_answers_reproduce():
    assert nested_value(4) == 4          # √(12 + √(12 + ⋯)) = 4
    assert distributions(10, 3) == 66    # 10 identical sweets to 3 children
    assert mn.s1(100) == 5050


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    for seed in range(150):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
