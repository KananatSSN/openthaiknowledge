"""Check the cyclic bound exactly on rational points and at equality."""

from fractions import Fraction
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.weighted_cyclic_inequality import minimum_cyclic_expression


def _expression(a: Fraction, b: Fraction, c: Fraction, x: int, y: int) -> Fraction:
    return (x + y) * (a * a + b * b + c * c) * (
        a**5 / (x * c + y * b)
        + b**5 / (x * a + y * c)
        + c**5 / (x * b + y * a)
    )


def test_exact_rational_samples_and_equality():
    rng = Random(2026)
    for product in (1, 2, 3, 8, 12, 27):
        for _ in range(80):
            a = Fraction(rng.randint(1, 9), rng.randint(1, 9))
            b = Fraction(rng.randint(1, 9), rng.randint(1, 9))
            c = Fraction(product, 1) / (a * b)
            x, y = rng.randint(1, 9), rng.randint(1, 9)
            assert _expression(a, b, c, x, y) >= minimum_cyclic_expression(product)
    for root in (1, 2, 3, 4):
        value = Fraction(root)
        assert _expression(value, value, value, 2, 7) == minimum_cyclic_expression(root**3)


def test_generated_draws():
    key = "math.weighted_cyclic_inequality_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
