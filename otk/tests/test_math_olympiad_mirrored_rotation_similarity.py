"""Check the mirrored-rotation similarity with independent coordinates."""

from __future__ import annotations

from math import cos, hypot, isclose, radians, sin, sqrt
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.mirrored_rotation_similarity import mirrored_rotation_ratio


def _configuration(ab: int, ac: int, angle: int, rotation: int, scale: float):
    theta, phi = radians(angle), radians(rotation)
    ct, st = cos(theta), sin(theta)
    cp, sp = cos(phi), sin(phi)
    b = (float(ab), 0.0)
    c = (ac * ct, ac * st)
    e = (-2.0 * ac, 0.0)
    f = (-2.0 * ab * ct, -2.0 * ab * st)
    p = (scale * (c[0] * cp - c[1] * sp), scale * (c[0] * sp + c[1] * cp))
    r = (scale * ab * cp, -scale * ab * sp)
    return b, c, e, f, p, r


def _second_circle_intersection(start, target, line_x, line_y):
    dx, dy = target[0] - start[0], target[1] - start[1]
    t = -(2 * start[0] * dx + 2 * start[1] * dy + line_x * dx + line_y * dy) / (
        dx * dx + dy * dy
    )
    return start[0] + t * dx, start[1] + t * dy


def test_similarity_ratio_by_direct_distances():
    for ab in range(3, 11):
        for ac in range(3, 11):
            for angle, rotation in ((30, 20), (45, 30), (60, 45), (70, 60)):
                _, _, e, f, p, r = _configuration(ab, ac, angle, rotation, 1.0)
                ep = hypot(p[0] - e[0], p[1] - e[1])
                fr = hypot(r[0] - f[0], r[1] - f[1])
                assert isclose(fr / ep, float(mirrored_rotation_ratio(ab, ac)), rel_tol=1e-12)


def test_source_right_isosceles_case_gives_equal_chords():
    for ab, ac, angle in ((3, 5, 30), (7, 4, 45), (8, 11, 60), (12, 9, 75)):
        b, c, e, f, p, r = _configuration(ab, ac, angle, 45, sqrt(2))
        # The circle through B,E has constant coefficient -2*AB*AC.
        line_x = 2 * ac - ab
        constant = -2 * ab * ac
        line_y = -(c[0] ** 2 + c[1] ** 2 + line_x * c[0] + constant) / c[1]
        x = _second_circle_intersection(e, p, line_x, line_y)
        y = _second_circle_intersection(f, r, line_x, line_y)
        bx = hypot(b[0] - x[0], b[1] - x[1])
        cy = hypot(c[0] - y[0], c[1] - y[1])
        assert isclose(bx, cy, rel_tol=1e-12, abs_tol=1e-12)


def test_generated_draws():
    key = "math.mirrored_rotation_similarity_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
