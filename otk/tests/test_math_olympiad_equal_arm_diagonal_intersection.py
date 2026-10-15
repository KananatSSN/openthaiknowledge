"""Check the directed intersection parameter with exact coordinates."""

from fractions import Fraction
from random import Random

from sympy import Line, Point, Rational

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.equal_arm_diagonal_intersection import diagonal_intersection_parameter


def test_coordinate_intersections():
    for ab in range(4, 11):
        for ad in range(4, 11):
            if ab == ad:
                continue
            arm = min(ab, ad) - 1
            b = Point(ab, 0)
            d = Point(Rational(3 * ad, 5), Rational(4 * ad, 5))
            t = Point(arm, 0)
            s = Point(Rational(3 * arm, 5), Rational(4 * arm, 5))
            p = Line(s, t).intersection(Line(b, d))[0]
            coordinate_ratio = p.y / d.y
            assert coordinate_ratio == diagonal_intersection_parameter(ab, ad, arm)


def test_directed_parameter_is_not_unsigned_ratio():
    assert diagonal_intersection_parameter(5, 7, 2) == Fraction(-3, 2)
    assert diagonal_intersection_parameter(7, 5, 2) == Fraction(5, 2)


def test_generated_draws():
    key = "math.equal_arm_diagonal_intersection_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
