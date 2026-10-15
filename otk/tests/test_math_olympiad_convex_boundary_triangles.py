"""Check the boundary formula with exact-coordinate collinearity tests."""

from fractions import Fraction
from itertools import combinations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.convex_boundary_triangles import count_boundary_triangles


def _marked_edges(vertices: tuple[tuple[int, int], ...], marks: int):
    points = []
    for index, (x1, y1) in enumerate(vertices):
        x2, y2 = vertices[(index + 1) % len(vertices)]
        for j in range(1, marks + 1):
            portion = Fraction(j, marks + 1)
            points.append((x1 + portion * (x2 - x1), y1 + portion * (y2 - y1)))
    return points


def _noncollinear(a, b, c) -> bool:
    return (b[0] - a[0]) * (c[1] - a[1]) != (b[1] - a[1]) * (c[0] - a[0])


def test_matches_exact_coordinate_enumeration():
    triangle = ((0, 0), (10, 0), (0, 10))
    square = ((0, 0), (10, 0), (10, 10), (0, 10))
    for vertices in (triangle, square):
        for marks in range(1, 7):
            points = _marked_edges(vertices, marks)
            direct = sum(_noncollinear(*triple) for triple in combinations(points, 3))
            assert count_boundary_triangles(len(vertices), marks) == direct


def test_reproduces_checked_square_case():
    square = ((0, 0), (10, 0), (10, 10), (0, 10))
    points = _marked_edges(square, 8)
    direct = sum(_noncollinear(*triple) for triple in combinations(points, 3))
    assert count_boundary_triangles(4, 8) == direct == 4736


def test_generated_choices_are_distinct_and_reproducible():
    key = "math.convex_boundary_triangles_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(choices) == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
