"""Check the chord formula against exact coordinate circles."""

from fractions import Fraction
from random import Random

from sympy import Point
from sympy.geometry import Circle

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.perpendicular_chords import perpendicular_chord_radius_squared


def test_matches_circles_through_four_endpoints():
    for first in (2, 4, 6, 8):
        for second in (4, 8, 12):
            for third in (2, 4, 6, 8):
                fourth = Fraction(first * second, third)
                circle = Circle(Point(-first, 0), Point(second, 0), Point(0, -third))
                assert Point(0, fourth) in circle
                assert perpendicular_chord_radius_squared(first, second, third) == circle.radius**2


def test_checked_source_case():
    assert perpendicular_chord_radius_squared(4, 12, 8) == 65


def test_generated_draws():
    key = "math.perpendicular_chord_circle_area_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
