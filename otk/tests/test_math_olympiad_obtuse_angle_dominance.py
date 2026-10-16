"""Check the sharp angle bound against the original sight-angle condition."""

from math import atan, atan2, degrees, radians, sqrt, tan
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.obtuse_angle_dominance import _ANGLES, least_foot_angle


def _angles_for_interval(theta: float, u: float, v: float, midpoint: float):
    """Choose A,B on the line so that their angle at R is exactly theta."""
    c = -1 / tan(radians(theta))
    h = v * c + sqrt((midpoint - u) ** 2 + v * v * (1 + c * c))
    a, b = midpoint - h, midpoint + h
    at_r = degrees(atan((b - u) / v) - atan((a - u) / v))
    at_q = degrees(atan(b) - atan(a))
    return at_r, at_q


def test_boundary_attains_angle_and_satisfies_sight_condition():
    for theta in _ANGLES:
        c = -1 / tan(radians(theta))
        for height in (1.1, 1.5, 3.0):
            for u in (-c * (height - 1), 0, c * (height - 1)):
                target = degrees(atan2(abs(u), -(height - 1)))
                assert target + 1e-10 >= least_foot_angle(theta)
                for midpoint in (-100, -7, -1, 0, 1, 7, 100):
                    at_r, at_q = _angles_for_interval(theta, u, height, midpoint)
                    assert abs(at_r - theta) < 1e-9
                    assert at_q >= theta - 1e-9
            attained = degrees(atan2(c * (height - 1), -(height - 1)))
            assert abs(attained - least_foot_angle(theta)) < 1e-9


def test_outside_wedge_violates_condition():
    for theta in _ANGLES:
        c = -1 / tan(radians(theta))
        for u, v, midpoint in (
            (1.1 * c, 2.0, 1e6),
            (-1.1 * c, 2.0, -1e6),
            (0.0, 0.9, 1e6),
        ):
            at_r, at_q = _angles_for_interval(theta, u, v, midpoint)
            assert abs(at_r - theta) < 1e-7
            assert at_q < theta - 1e-7


def test_generated_draws():
    key = "math.obtuse_angle_dominance_olympiad"
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
