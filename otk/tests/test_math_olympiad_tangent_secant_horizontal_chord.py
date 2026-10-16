"""Check tangent geometry and triangle area with exact coordinates."""

from random import Random

from sympy import Point, pi, simplify, sqrt

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.tangent_secant_horizontal_chord import circle_area_from_tangent_triangle_coefficient


def _triangle_area_for_radius(radius):
    b = Point(2 * radius, 0)
    d = Point(-radius, 0)
    center = Point(radius, 0)
    c = Point(radius / 2, sqrt(3) * radius / 2)
    e = Point(3 * radius / 2, sqrt(3) * radius / 2)
    assert simplify(c.distance(center) ** 2 - radius**2) == 0
    assert simplify(e.distance(center) ** 2 - radius**2) == 0
    assert simplify((c - center).dot(c - d)) == 0
    return simplify(abs((e.x - c.x) * (b.y - c.y) - (e.y - c.y) * (b.x - c.x)) / 2)


def test_matches_exact_coordinate_triangles():
    for radius in range(1, 11):
        assert simplify(_triangle_area_for_radius(radius) - sqrt(3) * radius**2 / 4) == 0


def test_checked_source_case():
    radius = sqrt(60 / pi)
    assert simplify(_triangle_area_for_radius(radius) - 15 * sqrt(3) / pi) == 0
    assert circle_area_from_tangent_triangle_coefficient(15) == 60


def test_generated_draws():
    key = "math.tangent_horizontal_chord_circle_area_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
