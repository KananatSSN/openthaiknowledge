"""Exact coordinate construction of altitudes, tangents, and intersections."""

from fractions import Fraction
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.altitude_tangent_midpoint import (
    altitude_tangent_midpoint_distance,
)


def _add(a, b):
    return a[0] + b[0], a[1] + b[1]


def _sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def _mul(scale, a):
    return scale * a[0], scale * a[1]


def _cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def _line_intersection(p, direction, q, other):
    ratio = Fraction(_cross(_sub(q, p), other), _cross(direction, other))
    return _add(p, _mul(ratio, direction))


def _foot(point, start, end):
    direction = _sub(end, start)
    relative = _sub(point, start)
    ratio = Fraction(
        relative[0] * direction[0] + relative[1] * direction[1],
        direction[0] ** 2 + direction[1] ** 2,
    )
    return _add(start, _mul(ratio, direction))


def test_exact_construction():
    checked = 0
    for left in range(1, 9):
        for right in range(1, 9):
            for height in range(1, 12):
                if height * height <= left * right:
                    continue
                a, b, c, d = (0, height), (-left, 0), (right, 0), (0, 0)
                e = _foot(b, a, c)
                f = _foot(c, a, b)
                p = _line_intersection(e, _sub(f, e), d, (0, 1))
                # Circumcentres of ADC and ADB are (v/2,h/2) and (-u/2,h/2).
                tangent_adc = (height, -right)
                tangent_adb = (height, left)
                assert tangent_adc[0] * right + tangent_adc[1] * height == 0
                assert tangent_adb[0] * -left + tangent_adb[1] * height == 0
                x = _line_intersection(d, tangent_adc, a, _sub(b, a))
                y = _line_intersection(d, tangent_adb, a, _sub(c, a))
                m = _line_intersection(x, _sub(y, x), d, (0, 1))
                answer = altitude_tangent_midpoint_distance(left, right, height)
                assert m == (0, answer)
                assert p == (0, 2 * answer)
                assert x[1] == y[1]
                checked += 1
    assert checked > 400


def test_generated_draws():
    key = "math.altitude_tangent_midpoint_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
