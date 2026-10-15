"""Check power-sum cardinalities with independent direct enumeration."""

from itertools import product
from math import comb
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.base_power_sums import count_distinct_power_sums


def test_matches_direct_enumeration_at_and_below_carry_threshold():
    for base in range(2, 7):
        for labels in range(2, 7):
            for picks in range(1, min(base, 4) + 1):
                values = [base**exponent for exponent in range(labels)]
                direct = len({sum(draw) for draw in product(values, repeat=picks)})
                assert count_distinct_power_sums(base, labels, picks) == direct


def test_source_case_and_first_collision_above_threshold():
    assert count_distinct_power_sums(3, 6, 3) == comb(8, 3) == 56
    assert 1 + 1 + 1 + 9 == 3 + 3 + 3 + 3


def test_generated_choices_are_distinct_and_reproducible():
    key = "math.distinct_power_sums_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(choices) == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
