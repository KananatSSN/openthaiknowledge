"""Check all three tangencies with exact equilateral coordinates."""

from random import Random

from sympy import Line, Point, simplify, sqrt

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.three_semicircles_triangle import equilateral_area_from_semicircle_radius


def test_exact_three_center_configuration():
    for radius in range(1, 13):
        side = 2 * sqrt(3) * radius
        a = Point(0, 0)
        b = Point(side, 0)
        c = Point(side / 2, -sqrt(3) * side / 2)
        p = Point(2 * radius / sqrt(3), 0)
        q = Point(side - radius / sqrt(3), -radius)
        r = Point(side / 2 - radius / sqrt(3), -sqrt(3) * side / 2 + radius)
        for first, second in ((p, q), (q, r), (r, p)):
            assert simplify(first.distance(second) ** 2 - (2 * radius) ** 2) == 0
        assert simplify(Line(a, c).distance(p) - radius) == 0
        assert simplify(Line(a, b).distance(q) - radius) == 0
        assert simplify(Line(b, c).distance(r) - radius) == 0
        assert simplify(sqrt(3) * side**2 / 4 - equilateral_area_from_semicircle_radius(radius) * sqrt(3)) == 0


def test_checked_source_case():
    assert equilateral_area_from_semicircle_radius(3) == 27


def test_generated_draws():
    key = "math.three_tangent_semicircles_triangle_area_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
