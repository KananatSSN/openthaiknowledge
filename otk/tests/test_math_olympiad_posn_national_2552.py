"""Independent checks for the sets adapted from the 2552 national paper."""

import itertools
import math
import random
from fractions import Fraction
from math import isqrt
from random import Random

import mpmath
import pytest
import sympy

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.centroid_angle_ratio import TABLE as ANGLE_TABLE
from otk.sets.math.olympiad.cevian_division_area import SPLITS, area_ratio
from otk.sets.math.olympiad.incircle_antipode_area import TRIANGLES, antipode_area_ratio
from otk.sets.math.olympiad.lifting_order_exponent import CASES, smallest_exponent
from otk.sets.math.olympiad.linear_shift_functional import shift_solution
from otk.sets.math.olympiad.log_injective_collision import collision_exponent
from otk.sets.math.olympiad.newton_power_sum import elementary, power_sums
from otk.sets.math.olympiad.odd_club_maximum import club_maximum
from otk.sets.math.olympiad.reciprocal_square_residue import reciprocal_square_residue
from otk.sets.math.olympiad.rectangle_free_grid import TABLE as GRID_TABLE
from otk.sets.math.olympiad.subset_range_count import range_count
from otk.sets.math.olympiad.sum_square_set_size import PAIRS, largest_set
from otk.sets.math.olympiad.trapezoid_bisector_point import bisector_distance
from otk.sets.math.olympiad.triangle_weighted_sum_minimum import weighted_minimum, weighted_sum
from otk.sets.math.olympiad.vieta_jump_chain import chain
from otk.sets.math.olympiad.zero_one_real_rooted import CANDIDATES, SOLUTIONS, distinct_real_roots

KEYS = tuple(
    f"math.{k}_olympiad"
    for k in (
        "sum_square_set_size subset_range_count odd_club_maximum cevian_division_area "
        "linear_shift_functional incircle_antipode_area newton_power_sum triangle_weighted_sum_minimum "
        "centroid_angle_ratio reciprocal_square_residue lifting_order_exponent log_injective_collision "
        "trapezoid_bisector_point vieta_jump_chain rectangle_free_grid zero_one_real_rooted"
    ).split()
)


def _square(v):
    return v >= 0 and isqrt(v) ** 2 == v


def test_sum_square_sets_by_search():
    for a, b, answer in PAIRS[::40]:
        third = [c for c in range(1, (b - a) ** 2 // 4 + 2) if c not in (a, b) and _square(c + a) and _square(c + b)]
        best = 2
        for size in (1, 2, 3):
            if any(all(_square(x + y) for x, y in itertools.combinations(g, 2)) for g in itertools.combinations(third, size)):
                best = 2 + size
        assert best == answer
    assert largest_set(2009, 2087) == 2  # the source: 78 ≡ 2 (mod 4)


def test_subset_ranges_and_clubs_by_enumeration():
    for n in range(2, 11):
        for k in range(1, n):
            brute = sum(
                1 for size in range(2, n + 1) for s in itertools.combinations(range(1, n + 1), size)
                if s[-1] - s[0] == k
            )
            assert range_count(n, k) == brute
    for n in range(2, 6):
        people = range(n)
        clubs = [frozenset(s) for size in range(1, n + 1) for s in itertools.combinations(people, size)]
        allowed = [c for c in clubs if 0 not in c or len(c) % 2 == 1]
        assert len(allowed) == club_maximum(n)
    assert club_maximum(19) == 2**18 - 1 + 2**17  # the source


def test_cevian_area_on_skewed_triangles():
    rng = random.Random(1)
    for f, e in SPLITS:
        a = (Fraction(rng.randint(-5, 5)), Fraction(rng.randint(-5, 5)))
        b = (Fraction(rng.randint(6, 12)), Fraction(rng.randint(-5, 5)))
        c = (Fraction(rng.randint(-5, 5)), Fraction(rng.randint(6, 12)))

        def at(t):
            return a[0] + t * (c[0] - a[0]), a[1] + t * (c[1] - a[1])

        def meet(p1, p2, p3, p4):
            d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
            t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
            return p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])

        def area(p, q, r):
            return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) / 2

        d = ((b[0] + c[0]) / 2, (b[1] + c[1]) / 2)
        g, h = meet(a, d, b, at(e)), meet(a, d, b, at(f))
        assert area(b, g, h) / area(a, b, c) == area_ratio(f, e)
    assert area_ratio(Fraction(1, 3), Fraction(2, 3)) == Fraction(3, 20)  # the source


def test_linear_shift_by_sympy():
    x, y, p, q = sympy.symbols("x y p q")
    for c in range(1, 6):
        for d in range(1, 7):
            f = lambda v: p * v + q  # noqa: E731
            lhs = f(x * y + (c + 1) * x + (c + 1) * y + c * c - d)
            rhs = f(x) * f(y) + f(y) + x - d
            solutions = sympy.solve(sympy.Poly(sympy.expand(lhs - rhs), x, y).coeffs(), [p, q], dict=True)
            assert solutions == [{p: 1, q: c}] == [{p: shift_solution(c)[0], q: shift_solution(c)[1]}]


def test_incircle_antipode_by_coordinates():
    for a, b, c in TRIANGLES[::60]:
        s = (a + b + c) / 2
        x = (a * a + c * c - b * b) / (2 * a)
        aa = (x, math.sqrt(c * c - x * x))  # B at the origin, C = (a, 0)
        r = math.sqrt((s - a) * (s - b) * (s - c) / s)
        d, e = (s - b, 0.0), (s - b, 2 * r)
        t = -aa[1] / (e[1] - aa[1])
        f = (aa[0] + t * (e[0] - aa[0]), 0.0)
        area_def = abs((e[0] - d[0]) * (f[1] - d[1]) - (e[1] - d[1]) * (f[0] - d[0])) / 2
        assert math.isclose(area_def / (aa[1] * a / 2), float(antipode_area_ratio(a, b, c)))


def test_newton_power_sums_against_roots():
    rng = random.Random(4)
    for _ in range(100):
        roots = [rng.uniform(-3, 3) for _ in range(3)]
        e1 = sum(roots)
        e2 = roots[0] * roots[1] + roots[1] * roots[2] + roots[0] * roots[2]
        e3 = roots[0] * roots[1] * roots[2]
        s = [sum(r**k for r in roots) for k in range(1, 7)]
        assert all(math.isclose(u, v, abs_tol=1e-6) for u, v in zip(power_sums(e1, e2, e3, 6), s))
    for e in itertools.product(range(-3, 4), repeat=3):
        s1, s2, s3 = power_sums(*e, 3)
        assert (5 * s1 - 3 * s2 - 2 * s3) % 6 == 0  # the source's condition holds
        assert elementary(s1, s2, s3) == tuple(Fraction(v) for v in e)


def test_weighted_sum_by_sampling_and_tangent():
    rng = random.Random(3)
    for _ in range(20000):
        a, b = rng.uniform(0.1, 10), rng.uniform(0.1, 10)
        c = rng.uniform(abs(a - b) + 1e-6, a + b - 1e-6)
        assert weighted_sum(a, b, c) >= (a + b + c) / 2 - 1e-9
    for i in range(1, 1000):
        x = i / 1000
        assert 2 * x * (2 * x - 1) / (2 - x) >= 1 / 3 + 11 / 4 * (x - 2 / 3) - 1e-12
    assert weighted_minimum(30) == 15


def test_centroid_angle_table_by_coordinates():
    mpmath.mp.dps = 30
    for (alpha, beta), (p, q, r) in ANGLE_TABLE.items():
        al, be = mpmath.radians(alpha), mpmath.radians(beta)
        t = 4 * mpmath.sin(be) / mpmath.sin(be - al)
        c = (t * mpmath.cos(al), t * mpmath.sin(al))
        b = (6 - c[0], -c[1])
        a, pt = (0, 0), (2, 0)

        def angle(x, o, y):
            u, v = (x[0] - o[0], x[1] - o[1]), (y[0] - o[0], y[1] - o[1])
            return mpmath.degrees(mpmath.acos((u[0] * v[0] + u[1] * v[1]) / mpmath.sqrt(u[0] ** 2 + u[1] ** 2) / mpmath.sqrt(v[0] ** 2 + v[1] ** 2)))

        assert abs(angle(c, a, (3, 0)) - alpha) < 1e-20
        assert abs(angle(a, pt, b) - beta) < 1e-20
        ratio_sq = (b[0] ** 2 + b[1] ** 2) / ((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2)
        assert abs(ratio_sq - (p + q * mpmath.sqrt(3)) / r) < 1e-20


def test_reciprocal_square_residues_by_fractions():
    for p in (7, 11, 13, 17, 19, 23):
        total = Fraction(0)
        for m in range(1, p):
            total += Fraction(1, m * m)
            assert total.numerator * pow(total.denominator, -1, p) % p == reciprocal_square_residue(p, m)
        half = sum((Fraction(1, (2 * k) ** 2) for k in range(1, (p - 1) // 2 + 1)), Fraction(0))
        assert half.numerator % p == 0  # the source


def test_lifting_exponents_by_direct_powers():
    for a, b, p in CASES[::23]:
        for k in (1, 2, 3):
            n = smallest_exponent(a, b, p, k)
            assert (a**n - b**n) % p**k == 0
            assert all((a**m - b**m) % p**k for m in range(1, n))
            first = smallest_exponent(a, b, p, 1)
            assert (a ** (first * p ** (k - 1)) - b ** (first * p ** (k - 1))) % p**k == 0  # the source's lifting


def test_log_collisions():
    rng = random.Random(6)
    for _ in range(200):
        f2 = Fraction(rng.randint(1, 9), rng.randint(1, 9))
        f3 = Fraction(rng.randint(1, 9), rng.randint(1, 9))
        if f2 == f3:
            continue
        a = collision_exponent(f2, f3)
        assert any(a * f2 == b * f3 for b in range(1, 100))
        assert not any(a2 * f2 == b * f3 for a2 in range(1, a) for b in range(1, 100))


def test_trapezoid_bisector_by_coordinates():
    rng = random.Random(8)
    for _ in range(100):
        ab, ac = rng.randint(3, 30), rng.randint(3, 30)
        h = rng.uniform(0.5, ac - 0.1)
        a, b = (0.0, h), (float(ab), h)
        c = (math.sqrt(ac * ac - h * h), 0.0)
        # convex A, B, C, D with A top-left, B top-right: D lies left of C
        u = ((a[0] - c[0]) / ac - 1.0, (a[1] - c[1]) / ac)  # bisector of ∠ACD (CD points along −x)
        t = (h - c[1]) / u[1]
        k = (c[0] + t * u[0], h)
        assert k[0] < a[0] + 1e-9 and math.isclose(math.dist(b, k), bisector_distance(ab, ac))


def test_vieta_chain_by_search():
    for k in (1, 2, 3):
        brute = sorted((m, n) for m in range(1, 3000) for n in range(1, m) if (m - n) ** 2 == k * m * n + m + n)
        assert [pair for pair in chain(k, 12) if pair[0] < 3000] == brute


def test_rectangle_free_grid_by_brute_force():
    for (rows, cols), answer in GRID_TABLE.items():
        if rows * cols > 16:
            continue
        cells = [(r, c) for r in range(rows) for c in range(cols)]
        best = 0
        for mask in range(1 << len(cells)):
            chosen = {cells[i] for i in range(len(cells)) if mask >> i & 1}
            if len(chosen) <= best:
                continue
            if not any(
                {(r1, c1), (r1, c2), (r2, c1), (r2, c2)} <= chosen
                for r1, r2 in itertools.combinations(range(rows), 2)
                for c1, c2 in itertools.combinations(range(cols), 2)
            ):
                best = len(chosen)
        assert best == answer


def test_zero_one_polynomials_by_sympy():
    x = sympy.symbols("x")
    found = []
    for n in range(1, 7):
        for coeffs in itertools.product((0, 1), repeat=n):
            if set(coeffs) != {0, 1}:
                continue
            poly = sympy.Poly((-1) ** n * x**n + sum(c * x ** (n - i) for i, c in enumerate(coeffs, start=1)), x)
            roots = sympy.real_roots(poly)
            if len(set(roots)) == n:
                found.append(coeffs)
    assert sorted(found) == sorted(SOLUTIONS)
    assert all(distinct_real_roots(c) for c in SOLUTIONS)
    assert not any(distinct_real_roots(c) for c in CANDIDATES)


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
