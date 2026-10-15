"""Independent rational-scaling and draw checks for the kite identity."""

from fractions import Fraction
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.tangential_quadrilateral_additivity import (
    rational_function_value,
)


def test_rational_scaling_by_repeated_addition():
    for denominator in range(1, 10):
        for numerator in range(1, 14):
            for unit_value in range(1, 9):
                # Additivity gives q*f(p/q) = p*f(1); compare via exact fractions.
                value = rational_function_value(unit_value, numerator, denominator)
                assert sum((value for _ in range(denominator)), Fraction()) == sum(
                    (Fraction(unit_value) for _ in range(numerator)), Fraction()
                )
    assert rational_function_value(12, 5, 3) == 20


def test_generated_draws():
    key = "math.tangential_quadrilateral_additivity_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
