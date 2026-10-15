"""Check reciprocal root counts, six-sector packing, and generated choices."""

from cmath import exp
from fractions import Fraction
from math import comb, pi
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.reciprocal_roots_sectors import sector_pair_lower_bound


def _independent_minimum_pairs(inside: int) -> int:
    dp = {0: 0}
    for _ in range(6):
        updated = {}
        for already, cost in dp.items():
            for added in range(inside - already + 1):
                total = already + added
                candidate = cost + comb(added, 2)
                updated[total] = min(updated.get(total, candidate), candidate)
        dp = updated
    return dp[inside]


def test_reciprocal_pairing_and_independent_occupancy_search():
    for degree in range(13, 36):
        pairs = degree // 2
        roots = [Fraction(2 + n) for n in range(pairs)]
        roots += [1 / root for root in roots]
        if degree % 2:
            roots.append(Fraction(-1))
        assert len(set(roots)) == degree
        inside = sum(abs(root) <= 1 for root in roots)
        assert inside == (degree + 1) // 2
        assert sector_pair_lower_bound(degree) == _independent_minimum_pairs(inside)


def test_same_sector_points_are_strictly_close():
    rng = Random(2564)
    for sector in range(6):
        for _ in range(100):
            theta_1 = (sector + rng.random()) * pi / 3
            theta_2 = (sector + rng.random()) * pi / 3
            radius_1 = rng.uniform(0.05, 1.0)
            radius_2 = rng.uniform(0.05, 1.0)
            z = radius_1 * exp(1j * theta_1)
            w = radius_2 * exp(1j * theta_2)
            assert abs(z - w) < 1


def test_generated_draws():
    key = "math.reciprocal_roots_sectors_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
