"""Check square/circle contact with exact coordinate distances."""

from fractions import Fraction
from random import Random

from sympy import Point, simplify, sqrt

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.square_corner_tangent_circle import square_area_from_corner_circle_scale


def test_matches_exact_coordinate_square():
    for numerator in range(1, 9):
        for denominator in range(1, 5):
            scale = Fraction(numerator, denominator)
            radius = scale * (sqrt(2) - 1)
            side = scale * sqrt(2)
            circle_center = Point(radius, radius)
            square_center = Point(side / 2, side / 2)
            assert radius < side / 2
            assert simplify(circle_center.distance(square_center) ** 2 - radius**2) == 0
            assert simplify(side**2 - square_area_from_corner_circle_scale(scale)) == 0


def test_checked_source_case():
    assert square_area_from_corner_circle_scale(Fraction(2)) == 8


def test_generated_draws():
    key = "math.square_center_corner_tangent_circle_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
