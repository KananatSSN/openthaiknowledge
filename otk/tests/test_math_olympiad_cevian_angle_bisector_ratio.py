"""Independently check the circle reduction and the variable cevian ratio."""

from __future__ import annotations

from fractions import Fraction
from math import hypot, isclose
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.cevian_angle_bisector_ratio import cevian_segment_ratio


def _cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def _difference(u, v):
    return u[0] - v[0], u[1] - v[1]


def _line_intersection(p, q, r, s):
    pq, rs = _difference(q, p), _difference(s, r)
    factor = _cross(_difference(r, p), rs) / _cross(pq, rs)
    return p[0] + factor * pq[0], p[1] + factor * pq[1]


def _circle_point(t: Fraction):
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def _tangent_intersection(t: Fraction, u: Fraction):
    return (1 - t * u) / (1 + t * u), (t + u) / (1 + t * u)


def test_circle_tangent_line_meets_both_chords_exactly():
    parameter_triples = (
        (Fraction(-1, 2), Fraction(2, 3), Fraction(3)),
        (Fraction(-1, 3), Fraction(1, 2), Fraction(4)),
        (Fraction(-2, 3), Fraction(3, 4), Fraction(2)),
        (Fraction(-3, 4), Fraction(2, 5), Fraction(5)),
    )
    for a, c, d in parameter_triples:
        A, B, C, D = _circle_point(a), _circle_point(Fraction(0)), _circle_point(c), _circle_point(d)
        P, R = _tangent_intersection(a, d), _tangent_intersection(Fraction(0), c)
        T = _line_intersection(P, R, A, B)
        assert _cross(_difference(T, C), _difference(D, C)) == 0

        M = _line_intersection(P, R, B, C)
        mt = hypot(float(T[0] - M[0]), float(T[1] - M[1]))
        mb = hypot(float(B[0] - M[0]), float(B[1] - M[1]))
        N = ((float(T[0]) * mb + float(B[0]) * mt) / (mt + mb),
             (float(T[1]) * mb + float(B[1]) * mt) / (mt + mb))
        bf = tuple(map(float, B))
        cf = tuple(map(float, C))
        mf = tuple(map(float, M))
        tf = tuple(map(float, T))
        K = _line_intersection(cf, N, tf, mf)
        H = _line_intersection(bf, K, cf, tf)
        mn, mh = _difference(N, mf), _difference(H, mf)
        assert isclose(mn[0] * mh[0] + mn[1] * mh[1], 0.0, abs_tol=1e-10)


def test_variable_ratio_by_exact_coordinate_intersections():
    for x, y, ac in ((3, 4, 5), (5, 12, 13), (8, 15, 17), (-3, 4, 5)):
        for ab in (4, 7, 11):
            for ad in (2, 6, 9):
                A, B, C, D = (Fraction(0), Fraction(0)), (Fraction(ab), Fraction(0)), (
                    Fraction(x), Fraction(y)), (Fraction(-ad), Fraction(0))
                N = ((ac * B[0] + ab * C[0]) / (ab + ac),
                     (ac * B[1] + ab * C[1]) / (ab + ac))
                E = _line_intersection(D, N, A, C)
                F = _line_intersection(B, E, C, D)
                cf_fraction = (F[1] - C[1]) / (D[1] - C[1])
                assert cf_fraction / (1 - cf_fraction) == cevian_segment_ratio(ac, ad)
                assert F[0] * N[0] + F[1] * N[1] == 0


def test_generated_draws():
    key = "math.cevian_angle_bisector_ratio_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
