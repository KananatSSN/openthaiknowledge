"""Independent checks for the sets adapted from the 2556 national paper."""

import itertools
import math
import random
from fractions import Fraction
from math import gcd
from random import Random

import pytest
import sympy

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.cube_root_unity_digit_sum import MODULI, smallest_digit_sum
from otk.sets.math.olympiad.equal_bisector_segments_triangle import extremal_value
from otk.sets.math.olympiad.mersenne_cube_quotient import unique_solution
from otk.sets.math.olympiad.nagel_cevian_ratios import TRIANGLES, nagel_quantity
from otk.sets.math.olympiad.parity_subset_game import average_share
from otk.sets.math.olympiad.power_sum_functional import solutions
from otk.sets.math.olympiad.prime_power_minus_one_gcd import universal_divisor
from otk.sets.math.olympiad.regular_polygon_right_triangles import (
    half_equilateral_triangles,
    right_triangles,
)
from otk.sets.math.olympiad.shifted_product_closed_roots import root_sets
from otk.sets.math.olympiad.symmetric_root_coefficient_product import coefficient_product
from otk.sets.math.olympiad.trapezoid_midpoint_distances import midpoint_distance
from otk.sets.math.olympiad.triangulation_triangle_count import triangle_count

KEYS = (
    "math.prime_power_minus_one_gcd_olympiad",
    "math.equal_bisector_segments_triangle_olympiad",
    "math.regular_polygon_right_triangles_olympiad",
    "math.shifted_product_closed_roots_olympiad",
    "math.cube_root_unity_digit_sum_olympiad",
    "math.power_sum_functional_olympiad",
    "math.triangulation_triangle_count_olympiad",
    "math.symmetric_root_coefficient_product_olympiad",
    "math.trapezoid_midpoint_distances_olympiad",
    "math.mersenne_cube_quotient_olympiad",
    "math.parity_subset_game_olympiad",
    "math.nagel_cevian_ratios_olympiad",
)


def test_prime_power_gcd_by_brute_force():
    for k in (2, 4, 6, 8, 12):
        for bound in range(3, k + 4):
            brute = 0
            for p in sympy.primerange(bound + 1, 20000):
                brute = gcd(brute, p**k - 1)
            assert universal_divisor(k, bound) == brute
    assert universal_divisor(4, 4) == 48  # the source: p = 5 is allowed


def _incircle_triangle(c_deg, b_deg):
    """B = (0, 0), C on the x-axis, inradius 1."""
    bb, cc = math.radians(b_deg), math.radians(c_deg)
    a = 1 / math.tan(bb / 2) + 1 / math.tan(cc / 2)
    b_pt, c_pt = (0.0, 0.0), (a, 0.0)
    side_c = a * math.sin(cc) / math.sin(bb + cc)
    a_pt = (side_c * math.cos(bb), side_c * math.sin(bb))
    return a_pt, b_pt, c_pt


def _segment_intersection(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])


def _pd_minus_pe(c_deg, b_deg):
    a_pt, b_pt, c_pt = _incircle_triangle(c_deg, b_deg)
    la, lb, lc = math.dist(b_pt, c_pt), math.dist(c_pt, a_pt), math.dist(a_pt, b_pt)
    total = la + lb + lc
    p = ((la * a_pt[0] + lb * b_pt[0] + lc * c_pt[0]) / total, (la * a_pt[1] + lb * b_pt[1] + lc * c_pt[1]) / total)
    d = _segment_intersection(b_pt, p, c_pt, a_pt)
    e = _segment_intersection(c_pt, p, a_pt, b_pt)
    return math.dist(p, d) - math.dist(p, e)


def test_equal_bisector_segments_force_sixty_and_extremum():
    for c_deg in (30, 35, 40, 45, 50):
        # PD − PE changes sign only where A = 60°, i.e. B = 120° − C
        roots = []
        b_values = [c_deg + 0.4 + i * 0.25 for i in range(int((179 - 2 * c_deg) / 0.25))]
        for b0, b1 in zip(b_values, b_values[1:]):
            if b0 + c_deg >= 179.5 or b1 + c_deg >= 179.5:
                break
            if _pd_minus_pe(c_deg, b0) * _pd_minus_pe(c_deg, b1) < 0:
                roots.append((b0 + b1) / 2)
        assert len(roots) == 1 and abs(roots[0] - (120 - c_deg)) < 0.3
    # BC = cot(B/2) + cot(C/2) on B + C = 120°, C ∈ [30°, 60°): largest at C = 30°
    values = [1 / math.tan(math.radians(60 - c / 2)) + 1 / math.tan(math.radians(c / 2)) for c in range(30, 60)]
    assert values[0] == max(values)
    a_pt, b_pt, c_pt = _incircle_triangle(30, 90)
    for radius in (1, 4):
        sides = {"BC": math.dist(b_pt, c_pt), "AB": math.dist(a_pt, b_pt), "CA": math.dist(c_pt, a_pt),
                 "area": abs(a_pt[1]) * math.dist(b_pt, c_pt) / 2}
        for asked, measured in sides.items():
            rational, root = extremal_value(asked, radius)
            scale = radius ** (2 if asked == "area" else 1)
            assert math.isclose(measured * scale, float(rational) + float(root) * math.sqrt(3))


def test_regular_polygon_triangles_by_enumeration():
    for sides in range(4, 31, 2):
        points = [(math.cos(2 * math.pi * i / sides), math.sin(2 * math.pi * i / sides)) for i in range(sides)]
        right = half = 0
        for p, q, r in itertools.combinations(points, 3):
            lengths = sorted([math.dist(p, q), math.dist(q, r), math.dist(r, p)])
            if math.isclose(lengths[0] ** 2 + lengths[1] ** 2, lengths[2] ** 2):
                right += 1
                if math.isclose(lengths[1], math.sqrt(3) * lengths[0]):
                    half += 1
        assert right == right_triangles(sides)
        assert half == half_equilateral_triangles(sides)


def test_closed_root_sets_by_grid_search():
    for k in (1, 2, 3):
        grid = [Fraction(m, 2 * k) for m in range(-8, 9)]
        closed = []
        for size in range(1, 5):
            for subset in itertools.combinations(grid, size):
                members = set(subset)
                if all(a + b + k * a * b in members for a in members for b in members):
                    closed.append(tuple(sorted(subset)))
        assert sorted(closed) == sorted(root_sets(k))


def test_cube_root_digit_sums_by_brute_force():
    for modulus in MODULI:
        for digits in (4, 5):
            brute = min(
                sum(map(int, str(n)))
                for n in range(10 ** (digits - 1), 10**digits)
                if (n**3 - 1) % modulus == 0
            )
            assert smallest_digit_sum(modulus, digits) == brute
    hits = [n for n in range(10000, 100000) if (n**3 - 1) % 2556 == 0 and sum(map(int, str(n))) == 7]
    assert hits == [21301]  # the source answer


def test_power_sum_functional_solutions_by_sympy():
    x, y = sympy.symbols("x y", real=True)
    for k in (1, 2, 3):
        for f in solutions(k):
            lhs = (x**2 + y**2) ** k * f(x * y)
            rhs = f(x) * f(y) * f(x**2 + y**2)
            for xv, yv in itertools.product((-2, -1, 0, 1, 3), repeat=2):
                assert sympy.simplify((lhs - rhs).subs({x: xv, y: yv})) == 0
    # a wrong power fails
    assert (2**2 + 1) * (2 * 1) ** 2 != (2**2) * (1**2) * ((2**2 + 1) ** 2)


def _in_triangle(p, a, b, c):
    def side(u, v, w):
        return (v[0] - u[0]) * (w[1] - u[1]) - (v[1] - u[1]) * (w[0] - u[0])

    s1, s2, s3 = side(a, b, p), side(b, c, p), side(c, a, p)
    return (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0)


def test_triangulation_count_by_construction():
    rng = random.Random(1)
    for corners in range(3, 10):
        polygon = [(math.cos(2 * math.pi * i / corners), math.sin(2 * math.pi * i / corners)) for i in range(corners)]
        triangles = [(polygon[0], polygon[i], polygon[i + 1]) for i in range(1, corners - 1)]
        inserted = 0
        while inserted < 40:
            p = (rng.uniform(-1, 1), rng.uniform(-1, 1))
            for idx, (a, b, c) in enumerate(triangles):
                if _in_triangle(p, a, b, c):
                    triangles[idx:idx + 1] = [(a, b, p), (b, c, p), (c, a, p)]
                    inserted += 1
                    break
        area = sum(abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) / 2 for a, b, c in triangles)
        polygon_area = corners * math.sin(2 * math.pi / corners) / 2
        assert math.isclose(area, polygon_area)
        assert len(triangles) == triangle_count(corners, inserted)
    # the source bound: regular hexagon of side 1, 2556 points
    assert 3 * math.sqrt(3) / 2 / triangle_count(6, 2556) < 1 / 1700


def test_symmetric_root_coefficients_by_sympy():
    x = sympy.symbols("x")
    rng = random.Random(2)
    for n in (2, 3, 4):
        for _ in range(5):
            roots = [Fraction(rng.randint(1, 6), rng.randint(1, 6)) for _ in range(n)]
            poly = sympy.Poly(x * sympy.prod([x**2 - sympy.Rational(b.numerator, b.denominator) ** 2 for b in roots]), x)
            coeffs = dict(zip(range(poly.degree(), -1, -1), poly.all_coeffs()))
            product = coeffs[3] * coeffs[2 * n - 1]
            assert product == sympy.Rational(coefficient_product(roots).numerator, coefficient_product(roots).denominator)
    # even n with Πb = 1: at least n², equality at b = 1
    for n in (2, 4):
        for _ in range(200):
            free = [math.exp(rng.uniform(-2, 2)) for _ in range(n - 1)]
            roots = free + [1 / math.prod(free)]
            squares = [b * b for b in roots]
            assert sum(squares) * sum(1 / s for s in squares) >= n * n - 1e-9
        assert coefficient_product([1] * n) == n * n


def _foot(p, a, b):
    t = ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / math.dist(a, b) ** 2
    return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])


def test_trapezoid_distances_by_coordinates():
    rng = random.Random(5)
    for _ in range(200):
        h = rng.uniform(1, 5)
        a, d = (rng.uniform(-2, 2), h), (rng.uniform(3, 6), h)
        b, c = (rng.uniform(-3, 0), 0.0), (rng.uniform(4, 8), 0.0)
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        n = ((c[0] + d[0]) / 2, (c[1] + d[1]) / 2)
        mp, nq = math.dist(m, _foot(m, c, d)), math.dist(n, _foot(n, a, b))
        assert math.isclose(nq, mp * math.dist(c, d) / math.dist(a, b))
        # tilt AD: the relation breaks
        d2 = (d[0], d[1] + 0.7)
        n2 = ((c[0] + d2[0]) / 2, (c[1] + d2[1]) / 2)
        mp2, nq2 = math.dist(m, _foot(m, c, d2)), math.dist(n2, _foot(n2, a, b))
        assert not math.isclose(nq2, mp2 * math.dist(c, d2) / math.dist(a, b), rel_tol=1e-6)
    assert midpoint_distance(9, 10, 2) == Fraction(20, 9)


def test_mersenne_quotient_by_search():
    for k, x_limit, y_limit in ((2, 400, 400), (3, 2000, 400), (5, 400, 200)):
        found = []
        for x in range(1, x_limit):
            for y in range(1, y_limit):
                value = x * y**k
                if value % (x + y) == 0:
                    root, exact = sympy.integer_nthroot(value // (x + y), k)
                    if exact and sympy.isprime(root):
                        found.append((x, y, root))
        assert found == [unique_solution(k)]
    assert unique_solution(3) == (2, 14, 7)  # the source


def test_parity_game_average_by_enumeration():
    rng = random.Random(8)
    for m in range(1, 6):
        for _ in range(10):
            piles = [rng.randint(1, 20) for _ in range(rng.randint(1, 6))]
            sets = [frozenset(x for x in range(m) if rng.randrange(2)) or frozenset({0}) for _ in piles]
            shares = []
            for mask in range(1, 2**m):
                s = {i for i in range(m) if mask >> i & 1}
                shares.append(sum(a for a, b in zip(piles, sets) if len(b & s) % 2))
            assert Fraction(sum(shares), len(shares)) == average_share(sum(piles), m)
            assert max(shares) * 2 > sum(piles)


def _line_circle_far(p, q, centre, radius):
    """Second intersection of line p→q with the circle, away from p."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    fx, fy = p[0] - centre[0], p[1] - centre[1]
    aa, bb, cc = dx * dx + dy * dy, 2 * (fx * dx + fy * dy), fx * fx + fy * fy - radius * radius
    disc = math.sqrt(max(bb * bb - 4 * aa * cc, 0.0))
    return [(p[0] + t * dx, p[1] + t * dy) for t in ((-bb - disc) / (2 * aa), (-bb + disc) / (2 * aa))]


def _area(points):
    return abs(sum(points[i][0] * points[i - 1][1] - points[i - 1][0] * points[i][1] for i in range(len(points)))) / 2


def test_nagel_configuration_by_coordinates():
    for a, b, c in TRIANGLES[::7]:
        s = (a + b + c) / 2
        b_pt, c_pt = (0.0, 0.0), (float(a), 0.0)
        x = (a * a + c * c - b * b) / (2 * a)
        a_pt = (x, math.sqrt(c * c - x * x))
        r = math.sqrt((s - a) * (s - b) * (s - c) / s)
        incenter = (s - b, r)
        p = (s - b, 2 * r)  # antipode of D = (s − b, 0)
        m = _segment_intersection(a_pt, p, b_pt, c_pt)
        t = (s - a) / b  # CN = s − a along CA
        n = (c_pt[0] + t * (a_pt[0] - c_pt[0]), c_pt[1] + t * (a_pt[1] - c_pt[1]))
        rr = _segment_intersection(b_pt, n, a_pt, m)
        assert math.isclose(math.dist(b_pt, m), float(nagel_quantity("BM", a, b, c)))
        assert math.isclose(math.dist(a_pt, n), float(nagel_quantity("AN", a, b, c)))
        assert math.isclose(math.dist(a_pt, rr) / math.dist(rr, m), float(nagel_quantity("AR:RM", a, b, c)))
        # the source claim: [ABR] = [PQMN], Q the intersection of BN with ω nearer B
        q = min(_line_circle_far(b_pt, n, incenter, r), key=lambda pt: math.dist(pt, b_pt))
        assert math.isclose(_area([a_pt, b_pt, rr]), _area([p, q, m, n]), rel_tol=1e-9)


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
