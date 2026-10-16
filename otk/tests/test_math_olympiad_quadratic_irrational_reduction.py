"""Check polynomial reduction at a quadratic irrational with SymPy."""

from random import Random

import sympy as sp

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.quadratic_irrational_reduction import (
    crafted_numerator,
    floor_quadratic_irrational,
)


def _value(coefficients: tuple[int, ...]):
    alpha = (sp.sqrt(3) - 1) / 2
    numerator = sum(coefficient * alpha ** (5 - index) for index, coefficient in enumerate(coefficients))
    return sp.simplify(numerator / (2 * alpha**3 - alpha))


def test_symbolic_reduction_and_floor():
    rng = Random(441)
    for _ in range(40):
        integer_part = rng.randint(2, 12)
        irrational_part = rng.randint(0, 8)
        coefficients = tuple(rng.randint(-5, 5) for _ in range(4))
        numerator = crafted_numerator(integer_part, irrational_part, coefficients)
        value = _value(numerator)
        assert sp.simplify(value - integer_part - irrational_part * (sp.sqrt(3) - 1) / 2) == 0
        assert floor_quadratic_irrational(integer_part, irrational_part) == sp.floor(value)


def test_checked_source_case():
    source = (4, 4, -4, -2, 11, -5)
    assert crafted_numerator(5, 0, (2, 0, -6, 5)) == source
    assert _value(source) == 5
    assert floor_quadratic_irrational(5, 0) == 5


def test_generated_draws():
    key = "math.quadratic_irrational_reduction_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
