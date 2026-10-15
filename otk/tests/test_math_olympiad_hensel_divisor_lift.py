"""Brute-force the lifted congruences and the divisor guarantee."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.hensel_divisor_lift import lifted_root


def test_unique_roots_by_direct_enumeration():
    for constant in (21, 70, 119, 203, 2023):
        for exponent in range(1, 5):
            modulus = 7**exponent
            roots = [
                value
                for value in range(0, modulus, 7)
                if (value * value + value + constant) % modulus == 0
            ]
            assert roots == [lifted_root(constant, exponent)]


def test_source_divisor_construction():
    for exponent in range(1, 9):
        modulus = 7**exponent
        positive_term = lifted_root(2023, exponent) + modulus
        value = positive_term * positive_term + positive_term + 2023
        assert value % modulus == 0
        assert len({7**power for power in range(exponent + 1)}) == exponent + 1
        assert all(value % (7**power) == 0 for power in range(exponent + 1))


def test_generated_draws():
    key = "math.hensel_divisor_lift_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
