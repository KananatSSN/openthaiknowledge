"""Construct the circles independently and verify the inner chord length."""

from fractions import Fraction
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.tangent_circles_inner_chord import inner_chord_length


def _add(p, q):
    return p[0] + q[0], p[1] + q[1]


def _sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def _scale(t, p):
    return t * p[0], t * p[1]


def _dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def _cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def _intersect(p, r, q, s):
    return _add(p, _scale(Fraction(_cross(_sub(q, p), s), _cross(r, s)), r))


def _circle_center(p, q, r):
    pq, pr = _sub(q, p), _sub(r, p)
    half_pq = Fraction(_dot(q, q) - _dot(p, p), 2)
    half_pr = Fraction(_dot(r, r) - _dot(p, p), 2)
    det = _cross(pq, pr)
    return (
        Fraction(half_pq * pr[1] - half_pr * pq[1], det),
        Fraction(pq[0] * half_pr - pr[0] * half_pq, det),
    )


def _second_intersection(p, toward, center):
    direction = _sub(toward, p)
    t = Fraction(-2 * _dot(_sub(p, center), direction), _dot(direction, direction))
    return _add(p, _scale(t, direction))


def _construct(a: int, u: int, v: int):
    a_point, b_point, c_point = (-a, 0), (a, 0), (u, v)
    center = _circle_center(a_point, b_point, c_point)
    # Both tangent directions are perpendicular to the corresponding radii.
    tangent_a = (center[1], -a)
    tangent_b = (center[1], a)
    t_point = _intersect(a_point, tangent_a, b_point, tangent_b)
    d_point = _intersect(c_point, _sub(t_point, c_point), a_point, _sub(b_point, a_point))
    center_1 = _circle_center(c_point, a_point, d_point)
    center_2 = _circle_center(c_point, b_point, d_point)
    e_point = _second_intersection(a_point, t_point, center_1)
    f_point = _second_intersection(b_point, t_point, center_2)
    p_point = _intersect(e_point, _sub(f_point, e_point), a_point, _sub(c_point, a_point))
    q_point = _intersect(e_point, _sub(f_point, e_point), b_point, _sub(c_point, b_point))
    return a_point, b_point, e_point, f_point, p_point, q_point


def test_independent_circle_intersections():
    rng = Random(2566)
    for _ in range(100):
        a = rng.randint(2, 15)
        u = rng.randint(1 - a, a - 1)
        v = rng.randint(a + 1, 3 * a)
        a_point, b_point, e, f, p, q = _construct(a, u, v)
        assert e[1] == f[1] == p[1] == q[1]
        assert e[0] < p[0] < q[0] < f[0]
        assert q[0] - p[0] == inner_chord_length(a, u, v)
        assert f[0] - e[0] == (q[0] - p[0]) + (b_point[0] - a_point[0])


def test_generated_draws():
    key = "math.tangent_circles_inner_chord_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
