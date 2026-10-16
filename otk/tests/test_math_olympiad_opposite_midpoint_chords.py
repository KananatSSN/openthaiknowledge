"""Check midpoint vector identity and strict triangle from convex examples."""

from math import isclose, sqrt
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.opposite_midpoint_chords import opposite_midpoint_chord_square


def _difference(first, second):
    return second[0] - first[0], second[1] - first[1]


def _norm(vector):
    return sqrt(vector[0] ** 2 + vector[1] ** 2)


def test_midpoint_identity_and_triangle():
    base = ((2, 0), (1, 2), (-1, 2), (-2, 0), (-1, -2), (1, -2))
    for matrix in ((1, 0, 0, 1), (2, 1, -1, 2), (3, 2, 1, 1), (1, -2, 2, 1)):
        a, b, c, d = matrix
        vertices = [(a * x + b * y, c * x + d * y) for x, y in base]
        doubled_midpoints = [
            (vertices[i][0] + vertices[(i + 1) % 6][0], vertices[i][1] + vertices[(i + 1) % 6][1])
            for i in range(6)
        ]
        u, v, w, x, y, z = doubled_midpoints
        ux = _difference(u, x)
        wz = _difference(w, z)
        vy = _difference(v, y)
        assert tuple(ux[i] + wz[i] for i in (0, 1)) == vy
        lengths = sorted((_norm(ux), _norm(wz), _norm(vy)))
        assert lengths[0] + lengths[1] > lengths[2]


def test_cosine_calculation():
    for ux in range(3, 17):
        for wz in range(3, 17):
            for angle in (60, 120):
                expected = ux**2 + wz**2 + 2 * ux * wz * (0.5 if angle == 60 else -0.5)
                assert isclose(opposite_midpoint_chord_square(ux, wz, angle), expected)


def test_generated_draws():
    key = "math.opposite_midpoint_chord_square_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
