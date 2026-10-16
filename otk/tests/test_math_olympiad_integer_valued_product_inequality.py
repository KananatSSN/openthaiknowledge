"""Enumerate finite-function restrictions and check generated choices."""

from itertools import product
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.integer_valued_product_inequality import (
    possible_sample_sums,
)


def test_finite_domain_classification():
    domain = (-1, 0, 1)
    solutions = []
    for values in product(range(-2, 3), repeat=3):
        function = dict(zip(domain, values))
        if all(
            function[x] ** 2 + function[y] ** 2 <= 2 * function[x * y]
            for x in domain
            for y in domain
        ):
            solutions.append(function)
    assert solutions == [
        {-1: 0, 0: 0, 1: 0},
        {-1: 0, 0: 1, 1: 0},
        {-1: 1, 0: 1, 1: 1},
    ]
    for zeros in range(1, 8):
        for nonzeros in range(1, 8):
            brute = tuple(
                sorted(
                    {
                        zeros * function[0] + nonzeros * function[1]
                        for function in solutions
                    }
                )
            )
            assert possible_sample_sums(zeros, nonzeros) == brute


def test_generated_draws():
    key = "math.integer_valued_product_inequality_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
