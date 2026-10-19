"""Independent checks for the sets adapted from the 2554 national paper."""

import itertools
import math
import random
from fractions import Fraction
from math import factorial
from random import Random

import pytest
import sympy

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.bounded_variance_maximum import variance_sum_maximum
from otk.sets.math.olympiad.cevian_bisector_midpoint import PAIRS as CEVIAN_PAIRS
from otk.sets.math.olympiad.cevian_bisector_midpoint import midpoint_distance
from otk.sets.math.olympiad.divisor_fourth_power import NON_SOLUTIONS, SOLUTIONS, is_solution
from otk.sets.math.olympiad.excentral_centroid_ratio import TRIANGLES, collinear_ratio
from otk.sets.math.olympiad.factorial_minus_one_prime import factorial_minus_one_factor
from otk.sets.math.olympiad.odd_harmonic_three_adic import three_power
from otk.sets.math.olympiad.room_difference_pigeonhole import forcing_count
from otk.sets.math.olympiad.rotating_label_shift_count import shift_labelling_count
from otk.sets.math.olympiad.shift_additive_functional_existence import (
    CANDIDATES,
    has_solution,
    satisfies,
)
from otk.sets.math.olympiad.sum_dependent_product_function import geometric_value
from otk.sets.math.olympiad.symmetric_reciprocal_bound import reciprocal_maximum
from otk.sets.math.olympiad.tangent_centroid_circle_sides import PAIRS, tangent_side

KEYS = (
    "math.factorial_minus_one_prime_olympiad",
    "math.sum_dependent_product_function_olympiad",
    "math.cevian_bisector_midpoint_olympiad",
    "math.room_difference_pigeonhole_olympiad",
    "math.divisor_fourth_power_olympiad",
    "math.bounded_variance_maximum_olympiad",
    "math.symmetric_reciprocal_bound_olympiad",
    "math.tangent_centroid_circle_sides_olympiad",
    "math.odd_harmonic_three_adic_olympiad",
    "math.shift_additive_functional_existence_olympiad",
    "math.excentral_centroid_ratio_olympiad",
    "math.rotating_label_shift_count_olympiad",
)


def test_factorial_minus_one_factors_by_sympy():
    for n in range(4, 15):
        q = factorial_minus_one_factor(n)
        assert q == min(sympy.factorint(factorial(n - 1) - 1))
        assert q > n  # the source: every p | n! is below every such q


def test_geometric_function_from_sum_invariance():
    for first, ratio in itertools.product(range(1, 5), range(1, 5)):
        f = [None] + [geometric_value(first, ratio, k) for k in range(1, 12)]
        for m, n, m2, n2 in itertools.product(range(1, 6), repeat=4):
            if m + n == m2 + n2:
                assert f[m] * f[n] == f[m2] * f[n2]
    # the source equation f(2m + 2n) = f(m)f(n) over geometric candidates: only f ≡ 1
    survivors = [
        (first, ratio)
        for first in range(1, 6) for ratio in range(1, 6)
        if all(geometric_value(first, ratio, 2 * m + 2 * n) == geometric_value(first, ratio, m) * geometric_value(first, ratio, n)
               for m in range(1, 5) for n in range(1, 5))
    ]
    assert survivors == [(1, 1)]


def _intersect(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])


def _angle(x, o, y):
    u, v = (x[0] - o[0], x[1] - o[1]), (y[0] - o[0], y[1] - o[1])
    return math.acos((u[0] * v[0] + u[1] * v[1]) / math.hypot(*u) / math.hypot(*v))


def test_cevian_bisector_configuration_by_bisection():
    for cp, cq in CEVIAN_PAIRS:
        a = 2.0 * cp  # CB; search CA so that ∠BRP = ∠PRC

        def gap(b):
            c, bb, aa = (0.0, 0.0), (a, 0.0), (0.0, b)
            p, q = (float(cp), 0.0), (0.0, float(cq))
            d = _intersect(aa, p, bb, q)
            r = _intersect(c, d, aa, bb)
            return _angle(bb, r, p) - _angle(p, r, c), r

        grid = [cq * (1.001 + i * 0.05) for i in range(1, 2000)]
        lo = next(x for x, y in zip(grid, grid[1:]) if gap(x)[0] * gap(y)[0] < 0)
        hi = lo + cq * 0.05
        for _ in range(80):
            mid = (lo + hi) / 2
            if gap(lo)[0] * gap(mid)[0] <= 0:
                hi = mid
            else:
                lo = mid
        r = gap(lo)[1]
        m = (cp / 2, cq / 2)
        expected = float(midpoint_distance(cp, cq))
        assert math.isclose(math.dist(m, r), expected, rel_tol=1e-6)
        assert math.isclose(math.dist(m, (0.0, 0.0)), expected)


def test_room_differences_by_exhaustion():
    for rooms, seats in ((2, 3), (2, 4), (3, 3), (3, 4)):
        def shared(placement):
            diffs = []
            for chosen in placement:
                diffs.append({b - a for a, b in itertools.combinations(sorted(chosen), 2)})
            return any(diffs[i] & diffs[j] for i, j in itertools.combinations(range(rooms), 2))

        subsets = [s for k in range(seats + 1) for s in itertools.combinations(range(1, seats + 1), k)]
        threshold = min(
            n for n in range(1, rooms * seats + 1)
            if all(shared(pl) for pl in itertools.product(subsets, repeat=rooms) if sum(map(len, pl)) == n)
        )
        assert threshold == forcing_count(rooms, seats)


def test_divisor_fourth_power_by_search():
    assert [n for n in range(1, 2 * 10**5) if sympy.divisor_count(n) ** 4 == n] == [1, 625, 6561]
    assert sympy.divisor_count(4100625) ** 4 == 4100625
    assert all(is_solution(n) for n in SOLUTIONS)
    assert not any(sympy.divisor_count(n) ** 4 == n for n in NON_SOLUTIONS)


def test_variance_maximum_by_vertices():
    for n in range(2, 12):
        best = max(
            sum((x - Fraction(sum(v), n)) ** 2 for x in v)
            for v in itertools.product((0, 1), repeat=n)
        )
        assert best == variance_sum_maximum(n)
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(2, 9)
        xs = [rng.random() for _ in range(n)]
        mean = sum(xs) / n
        assert sum((x - mean) ** 2 for x in xs) <= float(variance_sum_maximum(n)) + 1e-12
    assert variance_sum_maximum(2011) == Fraction(1005 * 1006, 2011)  # the source


def test_symmetric_reciprocal_bound_by_sampling():
    rng = random.Random(3)
    for n in range(3, 8):
        bound = float(reciprocal_maximum(n))
        for _ in range(200):
            free = [math.exp(rng.uniform(-2, 2)) for _ in range(n - 1)]
            roots = free + [1 / math.prod(free)]
            e = [sum(math.prod(c) for c in itertools.combinations(roots, k)) for k in range(1, n)]
            assert sum(1 / v for v in e) <= bound + 1e-9
    assert reciprocal_maximum(5) == Fraction(3, 5)  # the source


def test_tangent_centroid_by_coordinates():
    for a, c in PAIRS:
        b = tangent_side(a, c)
        bb, cc = (0.0, 0.0), (float(a), 0.0)
        x = (a * a + c * c - b * b) / (2 * a)
        aa = (x, math.sqrt(c * c - x * x))
        g = ((aa[0] + bb[0] + cc[0]) / 3, (aa[1] + bb[1] + cc[1]) / 3)
        # circle through A, B, G; tangent at A must be along AC
        ax, ay = aa
        bx, by = bb
        gx, gy = g
        d = 2 * (ax * (by - gy) + bx * (gy - ay) + gx * (ay - by))
        ux = ((ax * ax + ay * ay) * (by - gy) + (bx * bx + by * by) * (gy - ay) + (gx * gx + gy * gy) * (ay - by)) / d
        uy = ((ax * ax + ay * ay) * (gx - bx) + (bx * bx + by * by) * (ax - gx) + (gx * gx + gy * gy) * (bx - ax)) / d
        radial = (aa[0] - ux, aa[1] - uy)
        along = (cc[0] - aa[0], cc[1] - aa[1])
        assert abs(radial[0] * along[0] + radial[1] * along[1]) < 1e-7 * math.hypot(*radial) * math.hypot(*along)
        assert a + c <= 2 * b  # the source inequality


def test_odd_harmonic_three_power_by_fractions():
    total = Fraction(0)
    for n in range(1, 400):
        total += Fraction(1, 2 * n - 1)
        assert sympy.multiplicity(3, total.denominator) == three_power(n)
        if n > 1:
            assert total.denominator > 1


def test_shift_additive_functional_candidates():
    for a in range(1, 5):
        for c in range(0, 4):
            assert satisfies(CANDIDATES["linear"](a, c), a, 0)
            for b in (1, 2):
                assert not has_solution(a, b)
                assert not any(satisfies(make(a, c), a, b) for make in CANDIDATES.values())
    # no solution among small affine or geometric functions for the source (a = b = 1)
    for k, c in itertools.product(range(0, 6), range(0, 6)):
        if k or c:
            assert not satisfies(lambda n, k=k, c=c: k * n + c, 1, 1)
    for base, start in itertools.product(range(1, 5), range(1, 5)):
        assert not satisfies(lambda n, base=base, start=start: start * base ** (n - 1), 1, 1)


def _point(weights, points):
    total = sum(weights)
    return (sum(w * p[0] for w, p in zip(weights, points)) / total, sum(w * p[1] for w, p in zip(weights, points)) / total)


def test_excentral_collinearity_by_coordinates():
    for a, b, c in TRIANGLES[::9]:
        s = (a + b + c) / 2
        bb, cc = (0.0, 0.0), (float(a), 0.0)
        x = (a * a + c * c - b * b) / (2 * a)
        aa = (x, math.sqrt(c * c - x * x))
        pts = [aa, bb, cc]
        incenter = _point([a, b, c], pts)
        excentres = [_point([-a, b, c], pts), _point([a, -b, c], pts), _point([a, b, -c], pts)]
        g = (sum(p[0] for p in excentres) / 3, sum(p[1] for p in excentres) / 3)
        tx = (s - b, 0.0)
        ty = (cc[0] + (s - c) / b * (aa[0] - cc[0]), cc[1] + (s - c) / b * (aa[1] - cc[1]))
        tz = (bb[0] + (s - b) / c * (aa[0] - bb[0]), bb[1] + (s - b) / c * (aa[1] - bb[1]))
        h = (tx[0] + ty[0] + tz[0] - 2 * incenter[0], tx[1] + ty[1] + tz[1] - 2 * incenter[1])  # I circumcentre of XYZ
        cross = (g[0] - incenter[0]) * (h[1] - incenter[1]) - (g[1] - incenter[1]) * (h[0] - incenter[0])
        assert abs(cross) < 1e-8 * (a + b + c) ** 2
        assert math.isclose(math.dist(incenter, g) / math.dist(incenter, h), float(collinear_ratio(a, b, c)), rel_tol=1e-9)


def test_rotating_labels_by_enumeration():
    def count(chairs):
        m = chairs // 3
        total = 0
        for f in itertools.product(range(3), repeat=chairs):
            if f.count(0) != m or f.count(1) != m:
                continue
            if any(all(f[(a + k) % chairs] == (f[a] - 1) % 3 for a in range(chairs)) for k in range(1, chairs)):
                total += 1
        return total

    for m in (1, 2, 4):
        assert count(3 * m) == shift_labelling_count(m)
    # the official key's pattern (3^d over the divisors d > 1 of m, as in
    # 3² + 3^1277 + 3^2554) already undercounts at m = 2: 9, not 18
    assert count(6) == 18 != 3**2


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
