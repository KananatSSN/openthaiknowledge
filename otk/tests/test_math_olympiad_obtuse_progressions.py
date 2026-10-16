"""Cross-check the progression formula by classifying actual triples."""

from itertools import combinations
from math import comb
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.obtuse_progressions import obtuse_progression_probability


def test_matches_direct_triangle_classification():
    for limit in range(3, 23):
        for gap in range(1, 8):
            favorable = sum(
                b - a == c - b == gap and a + b > c and a * a + b * b < c * c
                for a, b, c in combinations(range(1, limit + 1), 3)
            )
            probability = obtuse_progression_probability(limit, gap)
            assert probability.numerator * comb(limit, 3) == favorable * probability.denominator


def test_checked_source_case():
    probability = obtuse_progression_probability(9, 1)
    assert (probability.numerator, probability.denominator) == (1, 84)


def test_generated_draws():
    key = "math.obtuse_progression_probability_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
