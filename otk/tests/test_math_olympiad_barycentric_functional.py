"""Check the real-root classification and generated question variants."""

from random import Random

from sympy import Poly, symbols

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.barycentric_functional import count_barycentric_functions


def test_count_matches_independent_real_root_count():
    c = symbols("c")
    for arity in range(3, 8):
        for coefficient in (-4, -2, -1, 1, 2, 4):
            polynomial = Poly(coefficient * c**arity - c, c)
            assert count_barycentric_functions(arity, coefficient) == polynomial.count_roots(-5, 5)


def test_generated_choices_are_distinct_and_reproducible():
    key = "math.barycentric_functional_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(choices) == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
