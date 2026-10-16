"""Check the reciprocal solution by exact substitution."""

from fractions import Fraction
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.reciprocal_function_equation import reciprocal_function_value


def test_exact_substitution_and_requested_values():
    for root in range(2, 21):
        f = lambda value: Fraction(root, 1) / value
        for x in (Fraction(1, 3), Fraction(2, 5), Fraction(1), Fraction(3, 2), Fraction(7)):
            for y in (Fraction(1, 4), Fraction(2), Fraction(5, 3)):
                assert x * x * f(x * f(y)) * f(x) * f(y) == root * root
            assert reciprocal_function_value(root * root, x.numerator) == f(x.numerator)


def test_generated_draws():
    key = "math.reciprocal_function_equation_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
