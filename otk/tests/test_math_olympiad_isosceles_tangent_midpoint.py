"""Check the base intersection from independently constructed tangencies."""

from math import hypot, sqrt
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.isosceles_tangent_midpoint import _TRIPLES, half_base


def _contact_points(external, center, radius):
    vx, vy = external[0] - center[0], external[1] - center[1]
    distance_squared = vx * vx + vy * vy
    along = radius * radius / distance_squared
    across = radius * sqrt(distance_squared - radius * radius) / distance_squared
    return (
        (center[0] + along * vx - across * vy, center[1] + along * vy + across * vx),
        (center[0] + along * vx + across * vy, center[1] + along * vy - across * vx),
    )


def test_direct_tangent_construction():
    for base_half, altitude, leg in _TRIPLES:
        for radius in range(1, leg):
            if radius == altitude:
                continue
            center, b, c = (0, altitude), (-base_half, 0), (base_half, 0)
            p_options = _contact_points(b, center, radius)
            q_options = _contact_points(c, center, radius)
            contacts = tuple((p, b) for p in p_options) + tuple((q, c) for q in q_options)
            for point, external in contacts:
                assert abs(hypot(point[0], point[1] - altitude) - radius) < 1e-9
                tangent_dot = point[0] * (external[0] - point[0])
                tangent_dot += (point[1] - altitude) * (external[1] - point[1])
                assert abs(tangent_dot) < 1e-8
            crossing = 0
            for p in p_options:
                for q in q_options:
                    if abs(p[1] - q[1]) < 1e-9:
                        continue
                    crossing += 1
                    intercept = (p[0] * q[1] - q[0] * p[1]) / (q[1] - p[1])
                    assert abs(intercept) < 1e-8
                    assert half_base(leg, altitude, radius) == base_half
            assert crossing == 2


def test_generated_draws():
    key = "math.isosceles_tangent_midpoint_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
