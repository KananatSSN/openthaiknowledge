"""Independently evaluate the reciprocal-sum power minimum."""

from fractions import Fraction
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.reciprocal_sum_power_minimum import (
    minimum_reciprocal_power_sum,
)


def test_integer_constraint_solutions_by_direct_evaluation():
    triples = [
        (a, b, c)
        for a in range(2, 19)
        for b in range(a, 19)
        for c in range(b, 19)
        if Fraction(1, a) + Fraction(1, b) + Fraction(1, c) == 1
    ]
    assert triples == [(2, 3, 6), (2, 4, 4), (3, 3, 3)]
    for scale in range(1, 6):
        direct = [
            (scale * a) ** (scale * a) * (scale * b) * (scale * c)
            + (scale * b) ** (scale * b) * (scale * c) * (scale * a)
            + (scale * c) ** (scale * c) * (scale * a) * (scale * b)
            for a, b, c in triples
        ]
        assert min(direct) == minimum_reciprocal_power_sum(scale)
        assert direct.index(min(direct)) == 2


def test_generated_draws():
    key = "math.reciprocal_sum_power_minimum_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
