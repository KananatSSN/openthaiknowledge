"""Check the three small perimeters with exact right-triangle coordinates."""

from random import Random

from sympy import Line, Point, Segment, simplify

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.incenter_parallel_perimeters import parallel_incenter_perimeter_sum


def _small_triangle_perimeter(u: int, v: int, hypotenuse: int):
    a, b, c = Point(0, 0), Point(u, 0), Point(0, v)
    radius = (u + v - hypotenuse) // 2
    o = Point(radius, radius)
    ab, ac, bc = Line(a, b), Line(a, c), Line(b, c)
    through_ac = Line(o, o + (c - a))
    through_ab = Line(o, o + (b - a))
    through_bc = Line(o, o + (c - b))
    p = through_ac.intersection(ab)[0]
    q = through_ac.intersection(bc)[0]
    m = through_ab.intersection(ac)[0]
    n = through_ab.intersection(bc)[0]
    r = through_bc.intersection(ab)[0]
    s = through_bc.intersection(ac)[0]

    def perimeter(x, y, z):
        return Segment(x, y).length + Segment(y, z).length + Segment(z, x).length

    return simplify(perimeter(o, p, r) + perimeter(o, n, q) + perimeter(o, m, s))


def test_matches_exact_coordinate_triangles():
    for u, v, hypotenuse in ((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)):
        for scale in (1, 2, 3):
            scaled = (u * scale, v * scale, hypotenuse * scale)
            area = scaled[0] * scaled[1] // 2
            radius = (scaled[0] + scaled[1] - scaled[2]) // 2
            assert parallel_incenter_perimeter_sum(area, radius) == _small_triangle_perimeter(*scaled)


def test_checked_source_case():
    assert parallel_incenter_perimeter_sum(60, 3) == 40
    assert _small_triangle_perimeter(15, 8, 17) == 40


def test_generated_draws():
    key = "math.incenter_parallel_perimeter_sum_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
