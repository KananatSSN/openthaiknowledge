"""Reflect bisector rays in coordinates to check both intersections."""

from math import hypot, sqrt
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.incircle_bisector_equal_segments import (
    _acute_sides,
    common_bisector_segment,
)


def _reflect_intersection(origin, first, bisector):
    vx, vy = first[0] - origin[0], first[1] - origin[1]
    ux, uy = bisector[0] - origin[0], bisector[1] - origin[1]
    length = hypot(ux, uy)
    ux, uy = ux / length, uy / length
    projection = vx * ux + vy * uy
    rx, ry = 2 * projection * ux - vx, 2 * projection * uy - vy
    scale = -origin[1] / ry
    assert scale > 0
    return origin[0] + scale * rx


def test_independent_coordinate_construction():
    checked = 0
    for x in range(2, 9):
        for y in range(2, 9):
            for z in range(2, 9):
                if not _acute_sides(x, y, z):
                    continue
                ab, ac, bc = x + y, x + z, y + z
                cx = (ab * ab + ac * ac - bc * bc) / (2 * ab)
                cy = sqrt(ac * ac - cx * cx)
                a, b = (0.0, 0.0), (float(ab), 0.0)
                f = (float(x), 0.0)
                e = (x * cx / ac, x * cy / ac)
                d = (b[0] + y * (cx - b[0]) / bc, y * cy / bc)
                k = _reflect_intersection(d, a, f)
                ell = _reflect_intersection(e, b, f)
                expected = float(common_bisector_segment(x, y))
                assert 0 < ell < x < k < ab
                assert abs((k - x) - expected) < 1e-8
                assert abs((x - ell) - expected) < 1e-8
                assert abs(ell / x - x / ab) < 1e-8  # △ALE ~ △AEB
                checked += 1
    assert checked > 100


def test_generated_draws():
    key = "math.incircle_bisector_equal_segments_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
