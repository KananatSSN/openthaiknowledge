"""Independent checks for the sets adapted from the 2555 national paper."""

import itertools
import math
import random
from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb, gcd
from random import Random

import pytest
import sympy

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.cyclic_ratio_integer_triples import integer_triples
from otk.sets.math.olympiad.distinct_factor_product_minimum import smallest_product
from otk.sets.math.olympiad.euler_power_sum_remainder import PAIRS, euler_remainder, totient
from otk.sets.math.olympiad.fifth_power_residue_square import PRIMES, square_root_of_m
from otk.sets.math.olympiad.irrational_multiple_window import NONSQUARES, first_multiple
from otk.sets.math.olympiad.linear_composite_functional import linear_solution
from otk.sets.math.olympiad.real_rooted_coefficient_minimum import (
    coefficient_minimum,
    value_minimum,
)
from otk.sets.math.olympiad.right_triangle_diameter_circle import chord_products
from otk.sets.math.olympiad.square_incenter_quadrilateral import (
    area_tex,
    incenter_area_parts,
)
from otk.sets.math.olympiad.tangent_polar_altitude_foot import TRIANGLES, foot_distance
from otk.sets.math.olympiad.tie_heavy_round_robin import draw_fraction
from otk.sets.math.olympiad.tournament_top_bottom_threshold import threshold

KEYS = (
    "math.right_triangle_diameter_circle_olympiad",
    "math.distinct_factor_product_minimum_olympiad",
    "math.euler_power_sum_remainder_olympiad",
    "math.square_incenter_quadrilateral_olympiad",
    "math.linear_composite_functional_olympiad",
    "math.tournament_top_bottom_threshold_olympiad",
    "math.fifth_power_residue_square_olympiad",
    "math.tie_heavy_round_robin_olympiad",
    "math.real_rooted_coefficient_minimum_olympiad",
    "math.irrational_multiple_window_olympiad",
    "math.tangent_polar_altitude_foot_olympiad",
    "math.cyclic_ratio_integer_triples_olympiad",
)


def _line_circle(p, q, centre, radius):
    dx, dy = q[0] - p[0], q[1] - p[1]
    fx, fy = p[0] - centre[0], p[1] - centre[1]
    aa, bb, cc = dx * dx + dy * dy, 2 * (fx * dx + fy * dy), fx * fx + fy * fy - radius * radius
    disc = math.sqrt(max(bb * bb - 4 * aa * cc, 0.0))
    return [(p[0] + t * dx, p[1] + t * dy) for t in ((-bb - disc) / (2 * aa), (-bb + disc) / (2 * aa))]


def test_diameter_circle_products_by_coordinates():
    for ab, bp, pc in itertools.product((2, 5, 9), (1, 3, 7), (1, 4, 8)):
        a, c = (0.0, float(ab)), (float(bp + pc), 0.0)
        p = (float(bp), 0.0)
        centre, radius = ((p[0] + c[0]) / 2, 0.0), pc / 2
        q = min(_line_circle(a, c, centre, radius), key=lambda pt: math.dist(pt, a))
        r = max(_line_circle(a, p, centre, radius), key=lambda pt: math.dist(pt, a))
        products = chord_products(bp, pc)
        assert math.isclose(math.dist(a, c) * math.dist(c, q), products["AC·CQ"])
        assert math.isclose(math.dist(a, p) * math.dist(p, r), products["AP·PR"])
        assert math.isclose(pc**2, products["AC·CQ"] - products["AP·PR"])  # the source identity


def test_distinct_products_and_single_root_by_search():
    for count in range(2, 7):
        values = [v for v in range(-6, 7) if v]
        best = min(abs(math.prod(c)) for c in itertools.combinations(values, count))
        assert best == smallest_product(count)
    # the source with 2k = 4: Π(x − aᵢ) = (2!)² has at most one integer root
    for a in itertools.combinations(range(-5, 6), 4):
        roots = [x for x in range(-12, 13) if math.prod(x - v for v in a) == 4]
        assert len(roots) <= 1


def test_euler_remainder_and_even_floor():
    for m, n in PAIRS[::5]:
        total = pow(m, totient(n) + 1) + pow(n, totient(m) + 1)
        assert total % (m * n) == euler_remainder(m, n)
        if m % 2 and n % 2:
            assert (total // (m * n)) % 2 == 0  # the source statement
    assert totient(36) == sympy.totient(36)


def _incenter(p, q, r):
    a, b, c = math.dist(q, r), math.dist(r, p), math.dist(p, q)
    s = a + b + c
    return ((a * p[0] + b * q[0] + c * r[0]) / s, (a * p[1] + b * q[1] + c * r[1]) / s)


def _apex(p, q, angle_at_p):
    """Right angle at the apex, outside the unit square (counter-clockwise)."""
    t = math.radians(angle_at_p)
    length = math.dist(p, q) * math.cos(t)
    ux, uy = (q[0] - p[0]) / math.dist(p, q), (q[1] - p[1]) / math.dist(p, q)
    vx, vy = ux * math.cos(t) + uy * math.sin(t), -ux * math.sin(t) + uy * math.cos(t)
    return p[0] + length * vx, p[1] + length * vy


def test_square_incenter_area_by_coordinates():
    corners = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    for angles in itertools.product((30, 60), repeat=4):
        centres = []
        for i, angle in enumerate(angles):
            p, q = corners[i], corners[(i + 1) % 4]
            apex = _apex(p, q, angle)
            assert apex[0] < -1e-9 or apex[0] > 1 + 1e-9 or apex[1] < -1e-9 or apex[1] > 1 + 1e-9
            centres.append(_incenter(p, q, apex))
        area = abs(sum(centres[i][0] * centres[i - 1][1] - centres[i - 1][0] * centres[i][1] for i in range(4))) / 2
        zeros, thirties = incenter_area_parts(angles)
        assert math.isclose(area, zeros / 4 + thirties * math.sqrt(3) / 8)
        assert area <= 1 + 1e-12
        assert sympy.nsimplify(sympy.sympify(area_tex(zeros, thirties).replace(r"\frac", "").replace("{", "(").replace("}", ")").replace(")(", ")/(").replace(r"\sqrt", "sqrt"))) == sympy.nsimplify(sympy.Rational(zeros, 4) + sympy.Rational(thirties, 8) * sympy.sqrt(3))


def test_linear_solution_by_sympy():
    x, y, p, q = sympy.symbols("x y p q")
    for a in range(2, 8):
        f = lambda v: p * v + q  # noqa: E731
        residual = sympy.Poly(sympy.expand(f(f(x) + x * f(y)) - (a + 1) * f(x) - a * a * x * y), x, y)
        solutions = sympy.solve(residual.coeffs(), [p, q], dict=True)
        assert solutions == [{p: a, q: 1}]
        assert linear_solution(a) == (a, 1)


def _condition_and_distinct(n, k, results):
    """results[(i, j)] for i < j: 1 i wins, 0 draw, −1 j wins."""
    def beats(i, j):
        return results[(i, j)] == 1 if i < j else results[(j, i)] == -1

    for group in itertools.combinations(range(n), k):
        if not any(all(beats(u, v) for v in group if v != u) for u in group):
            return None
        if not any(all(beats(v, u) for v in group if v != u) for u in group):
            return None
    scores = [0] * n
    for (i, j), r in results.items():
        scores[i] += 1 + r
        scores[j] += 1 - r
    return len(set(scores)) == n


def test_tournament_threshold_by_exhaustion():
    k = 4
    pairs = list(itertools.combinations(range(5), 2))
    for outcome in itertools.product((1, 0, -1), repeat=len(pairs)):
        verdict = _condition_and_distinct(5, k, dict(zip(pairs, outcome)))
        assert verdict in (None, True)
    pairs4 = list(itertools.combinations(range(4), 2))
    assert any(
        _condition_and_distinct(4, k, dict(zip(pairs4, outcome))) is False
        for outcome in itertools.product((1, 0, -1), repeat=len(pairs4))
    )
    assert threshold(4) == 5 and threshold(100) == 197


def test_square_root_of_m_by_search():
    rng = random.Random(6)
    for p in PRIMES:
        for _ in range(30):
            a, b = rng.randint(1, 4 * p), rng.randint(1, 4 * p)
            if gcd(a, b) != 1 or a % p == 0 or b % p == 0:
                continue
            m = next(v for v in range(p) if (v * a * a + b * b) % p == 0)
            assert square_root_of_m(p, a, b) == next(n for n in range(1, p) if (m - n * n) % p == 0)
    # the source (p = 5): every m with 5 | ma² + b², gcd(a, b) = 1, is a square mod 5
    for a, b, m in itertools.product(range(1, 11), range(1, 11), range(5)):
        if gcd(a, b) == 1 and (m * a * a + b * b) % 5 == 0:
            assert any((m - n * n) % 5 == 0 for n in range(5))


def test_tie_fraction_by_enumeration_and_construction():
    # n = 1: two boys (0, 1), two girls (2, 3); enumerate every result
    def points(i, j, result):
        """result 1: i wins, 0: draw, −1: j wins; returns (points i, points j)."""
        girl_i, girl_j = i >= 2, j >= 2
        if girl_i == girl_j:
            return {1: (3, 0), 0: (1, 1), -1: (0, 3)}[result]
        if girl_i:
            return {1: (3, 0), 0: (2, 0), -1: (0, 2)}[result]
        return {1: (2, 0), 0: (0, 2), -1: (0, 3)}[result]

    pairs = list(itertools.combinations(range(4), 2))
    fractions = set()
    for outcome in itertools.product((1, 0, -1), repeat=6):
        scores = [0] * 4
        for (i, j), r in zip(pairs, outcome):
            pi, pj = points(i, j, r)
            scores[i] += pi
            scores[j] += pj
        if max(scores) == 3:
            fractions.add(Fraction(outcome.count(0), 6))
    assert fractions == {draw_fraction(1)}
    # n ≥ 2: girls draw boys n..2n−1 (cyclically) and lose to the rest
    for n in range(2, 6):
        girls = range(2 * n)
        score_b, score_g = [2 * n - 1] * (2 * n), [2 * n - 1] * (2 * n)
        draws = 2 * n * (2 * n - 1)
        for g in girls:
            for t in range(2 * n):
                b = (g + t) % (2 * n)
                if t < n:
                    score_g[g] += 2
                    draws += 1
                else:
                    score_b[b] += 2
        assert set(score_b) == set(score_g) == {4 * n - 1}
        assert Fraction(draws, comb(4 * n, 2)) == draw_fraction(n)


def test_real_rooted_minima_by_sampling():
    rng = random.Random(4)
    x = sympy.symbols("x")
    for n in range(3, 8):
        for _ in range(30):
            free = [math.exp(rng.uniform(-2, 2)) for _ in range(n - 1)]
            roots = free + [1 / math.prod(free)]
            coeffs = [1.0]
            for r in roots:
                coeffs = [a + r * b for a, b in zip(coeffs + [0.0], [0.0] + coeffs)]
            # coeffs[k] is the coefficient of x^(n−k)
            for k in range(1, n):
                assert coeffs[n - k] >= coefficient_minimum(n, k) * (1 - 1e-9)
            for t in (1, 2, 3):
                assert math.prod(t + r for r in roots) >= value_minimum(n, t) * (1 - 1e-9)
        poly = sympy.Poly((x + 1) ** n, x)
        assert [int(c) for c in reversed(poly.all_coeffs())] == [coefficient_minimum(n, k) for k in range(n + 1)]


def test_irrational_window_by_decimals():
    getcontext().prec = 60
    for d in NONSQUARES[::3]:
        for high, low in ((4, 7), (10, 14), (15, 23)):
            m = first_multiple(d, low, high)
            root = Decimal(d).sqrt()

            def frac(k):
                value = k * root
                return value - int(value)

            assert Decimal(1) / low < frac(m) < Decimal(1) / high
            assert all(not (Decimal(1) / low < frac(k) < Decimal(1) / high) for k in range(1, m))


def _intersect(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])


def _angle(x, o, y):
    u, v = (x[0] - o[0], x[1] - o[1]), (y[0] - o[0], y[1] - o[1])
    return math.acos((u[0] * v[0] + u[1] * v[1]) / math.hypot(*u) / math.hypot(*v))


def test_tangent_configuration_by_coordinates():
    for a, b, c in TRIANGLES[::40]:
        x = (a * a + c * c - b * b) / (2 * a)
        apex, bb, cc = (x, math.sqrt(c * c - x * x)), (0.0, 0.0), (float(a), 0.0)
        centre, radius = (a / 2, 0.0), a / 2
        dist = math.dist(apex, centre)
        if dist <= radius:
            continue
        base = math.atan2(centre[1] - apex[1], centre[0] - apex[0])
        half, length = math.asin(radius / dist), math.sqrt(dist * dist - radius * radius)
        d, e = ((apex[0] + length * math.cos(base + s * half), apex[1] + length * math.sin(base + s * half)) for s in (1, -1))
        m, n = _intersect(apex, d, bb, cc), _intersect(apex, e, bb, cc)
        if not min(m[0], a) < 0 < max(m[0], a):
            d, e, m, n = e, d, n, m
        ux, uy = bb[0] - apex[0], bb[1] - apex[1]
        t = ((cc[0] - apex[0]) * ux + (cc[1] - apex[1]) * uy) / (ux * ux + uy * uy)
        p = (apex[0] + t * ux, apex[1] + t * uy)
        q = _intersect(cc, p, d, e)
        r = _intersect(m, e, n, d)
        s = _intersect(q, r, bb, cc)
        assert math.isclose(s[0], float(foot_distance(a, b, c)), abs_tol=1e-7)
        assert math.isclose(_angle(d, s, q), _angle(q, s, e), abs_tol=1e-7)  # the source


def test_cyclic_ratio_triples_by_fractions():
    for limit in (5, 12, 30):
        brute = [
            (a, b, c)
            for a in range(1, limit + 1) for b in range(1, limit + 1) for c in range(1, limit + 1)
            if gcd(gcd(a, b), c) == 1 and (Fraction(a, b) + Fraction(b, c) + Fraction(c, a)).denominator == 1
        ]
        assert integer_triples(limit) == brute
        for a, b, c in brute:
            assert sympy.integer_nthroot(a * b * c, 3)[1]  # the source statement


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
