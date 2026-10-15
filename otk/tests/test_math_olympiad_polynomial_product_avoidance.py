"""Check low-degree collisions and high-degree modular witnesses."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.polynomial_product_avoidance import (
    count_product_avoiding_degrees,
)


def _constructive_polynomial(degree: int, x: int) -> int:
    return x ** (degree - 3) * (x**3 - x) + 2


def test_every_monic_quadratic_has_the_claimed_collision():
    for u in range(-12, 13):
        for v in range(-12, 13):
            def polynomial(x: int) -> int:
                return x * x + u * x + v

            assert polynomial(0) * polynomial(1 - u) == polynomial(-v)


def test_constructed_high_degree_polynomials_avoid_products_modulo_three():
    for degree in range(3, 13):
        values = [_constructive_polynomial(degree, x) for x in range(-20, 21)]
        assert all(value % 3 == 2 for value in values)
        assert all((a * b) % 3 == 1 for a in values for b in values)


def test_degree_count_matches_constructive_classification():
    for limit in range(1, 101):
        assert count_product_avoiding_degrees(limit) == sum(
            degree >= 3 for degree in range(1, limit + 1)
        )


def test_generated_choices_are_distinct_and_reproducible():
    key = "math.polynomial_product_avoidance_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(choices) == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
