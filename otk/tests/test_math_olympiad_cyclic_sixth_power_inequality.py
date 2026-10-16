"""Exact rational grid checks for the cyclic inequality and generated draws."""

from fractions import Fraction
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.cyclic_sixth_power_inequality import (
    cyclic_sixth_power_minimum,
)


def _expression(a: Fraction, b: Fraction, c: Fraction, scale: int) -> Fraction:
    return (
        a**6 / (c**2 + Fraction(2, scale) * b**3)
        + b**6 / (a**2 + Fraction(2, scale) * c**3)
        + c**6 / (b**2 + Fraction(2, scale) * a**3)
    )


def test_exact_rational_samples_and_equality():
    for scale in range(1, 6):
        target = cyclic_sixth_power_minimum(scale)
        assert _expression(Fraction(scale), Fraction(scale), Fraction(scale), scale) == target
        for denominator in range(2, 11):
            total = 3 * denominator
            for i in range(1, total - 1):
                for j in range(1, total - i):
                    k = total - i - j
                    a, b, c = (
                        Fraction(scale * value, denominator) for value in (i, j, k)
                    )
                    value = _expression(a, b, c, scale)
                    assert value >= target
                    assert (value == target) == (a == b == c)
    assert cyclic_sixth_power_minimum(1) == 1


def test_generated_draws():
    key = "math.cyclic_sixth_power_inequality_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
