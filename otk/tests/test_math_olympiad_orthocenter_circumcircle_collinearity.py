"""Intersect exact circles and verify the common line through D."""

from fractions import Fraction
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.orthocenter_circumcircle_collinearity import orthocenter_collinearity_slope


def test_exact_source_construction():
    parameters = (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(1), Fraction(3, 2), Fraction(2))
    for parameter in parameters:
        u = 1 / (1 + 3 * parameter**2)
        v = 3 * parameter / (1 + 3 * parameter**2)
        h = u * (1 - u) / v
        assert v - h == 2 * h
        assert v * v > u * (1 - u)  # angle A is acute
        assert 0 < u < 1  # angles B and C are acute

        # The circumcircle is x^2+y^2-x-2hy=0. The two diameter circles
        # give lines BS and CT after subtraction; take their nontrivial roots.
        bs_slope = (u - 1) / h
        sx = (2 * u - 1) / (1 + bs_slope**2)
        sy = bs_slope * sx
        ct_slope = u / h
        tx = 1 + (2 * u - 1) / (1 + ct_slope**2)
        ty = ct_slope * (tx - 1)
        for x, y in ((sx, sy), (tx, ty)):
            assert x * x + y * y - x - 2 * h * y == 0
        assert sx * (sx - u) + sy * (sy - h) == 0
        assert (tx - 1) * (tx - u) + ty * (ty - h) == 0
        assert sy / (sx - u) == ty / (tx - u) == orthocenter_collinearity_slope(parameter)


def test_generated_draws():
    key = "math.orthocenter_circumcircle_collinearity_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
