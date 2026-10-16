"""Independently intersect the cevians and compare powers of the two circles."""

from fractions import Fraction
from math import hypot
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.diameter_circles_median import (
    _RATIOS,
    median_intersection_height,
)


def _add(p, q):
    return p[0] + q[0], p[1] + q[1]


def _sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def _scale(scalar, p):
    return scalar * p[0], scalar * p[1]


def _dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def _cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def _intersection(p, r, q, s):
    parameter = Fraction(_cross(_sub(q, p), s), _cross(r, s))
    return _add(p, _scale(parameter, r))


def test_coordinate_construction_and_radical_axis():
    rng = Random(2564)
    for _ in range(100):
        left, right = rng.randint(2, 12), rng.randint(2, 12)
        altitude = rng.randint(max(left, right) + 1, 2 * max(left, right) + 4)
        ratio = rng.choice(_RATIOS)
        a, b, c = (0, altitude), (-left, 0), (right, 0)
        d = _add(a, _scale(ratio, _sub(c, a)))
        e = _add(a, _scale(ratio, _sub(b, a)))
        p = _intersection(b, _sub(d, b), c, _sub(e, c))
        midpoint = (Fraction(b[0] + c[0], 2), 0)
        assert _cross(_sub(p, a), _sub(midpoint, a)) == 0
        assert p[1] == median_intersection_height(altitude, ratio)

        # Power to a circle with diameter XY equals (A-X)·(A-Y).
        first_power = _dot(_sub(a, b), _sub(a, d))
        second_power = _dot(_sub(a, c), _sub(a, e))
        assert first_power == second_power

        center_1 = _scale(Fraction(1, 2), _add(b, d))
        center_2 = _scale(Fraction(1, 2), _add(c, e))
        radius_1 = hypot(float(b[0] - d[0]), float(b[1] - d[1])) / 2
        radius_2 = hypot(float(c[0] - e[0]), float(c[1] - e[1])) / 2
        separation = hypot(float(center_1[0] - center_2[0]), float(center_1[1] - center_2[1]))
        assert abs(radius_1 - radius_2) < separation < radius_1 + radius_2


def test_generated_draws():
    key = "math.diameter_circles_median_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
