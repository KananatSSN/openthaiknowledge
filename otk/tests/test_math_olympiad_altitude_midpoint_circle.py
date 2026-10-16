"""Verify the second intersection using an exact coordinate circle."""

from fractions import Fraction
from random import Random

from sympy import Line, Point, sqrt, simplify
from sympy.geometry import Circle

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.altitude_midpoint_circle import second_intersection_distance


def _coordinate_distance(base: int, opposite_midpoint: int, side: int):
    foot = Fraction(side**2 + base**2 - opposite_midpoint**2, 2 * base)
    a = Point(foot, sqrt(side**2 - foot**2))
    b = Point(0, 0)
    d = Point(foot, 0)
    m = Point(Fraction(base, 2), 0)
    circle = Circle(a, d, m)
    e = next(point for point in circle.intersection(Line(a, b)) if point != a)
    return simplify(a.distance(e))


def test_matches_exact_circle_intersections():
    cases = ((14, 15, 13), (5, 4, 3), (15, 13, 14), (13, 12, 5), (13, 15, 14))
    for base, opposite_midpoint, side in cases:
        try:
            predicted = second_intersection_distance(base, opposite_midpoint, side)
        except ValueError:
            continue
        assert predicted == _coordinate_distance(base, opposite_midpoint, side)


def test_checked_source_case():
    assert second_intersection_distance(14, 15, 13) == Fraction(134, 13)
    assert _coordinate_distance(14, 15, 13) == Fraction(134, 13)


def test_generated_draws():
    key = "math.altitude_midpoint_circle_intersection_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
