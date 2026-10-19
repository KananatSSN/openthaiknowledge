"""Independent checks for the sets adapted from the 2549 national paper."""

import itertools
import math
import random
from fractions import Fraction
from functools import reduce
from math import comb, factorial, gcd
from random import Random

import numpy as np
import pytest
import sympy

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.bisector_circumradius_angle import bisector_radius_angle
from otk.sets.math.olympiad.consecutive_product_square_kernel import square_multiplier
from otk.sets.math.olympiad.coprime_exponent_pair import solutions
from otk.sets.math.olympiad.cosine_addition_functional import function_value
from otk.sets.math.olympiad.cube_ratio_difference_floor import floor_value
from otk.sets.math.olympiad.cube_root_unity_divisibility import difference_at
from otk.sets.math.olympiad.exponential_sequence_gcd import CASES as GCD_CASES
from otk.sets.math.olympiad.exponential_sequence_gcd import sequence_gcd, term
from otk.sets.math.olympiad.human_pyramid_orders import SHAPES, orders, pyramid
from otk.sets.math.olympiad.integer_root_quadratic_count import root_count
from otk.sets.math.olympiad.inverse_power_congruence import PRIMES as INVERSE_PRIMES
from otk.sets.math.olympiad.inverse_power_congruence import least_solution
from otk.sets.math.olympiad.medians_shortest_side import side_square
from otk.sets.math.olympiad.monochromatic_rectangle_count import rectangle_counts
from otk.sets.math.olympiad.near_wilson_factorial_powers import PRIMES as WILSON_PRIMES
from otk.sets.math.olympiad.near_wilson_factorial_powers import residue
from otk.sets.math.olympiad.nonadjacent_days import spaced_choices
from otk.sets.math.olympiad.prime_square_exponent_product import product_residue
from otk.sets.math.olympiad.repunit_residue import repunit_mod
from otk.sets.math.olympiad.root_square_root_sum import CASES as ROOT_CASES
from otk.sets.math.olympiad.root_square_root_sum import quartic_value
from otk.sets.math.olympiad.set_union_cover_count import cover_base
from otk.sets.math.olympiad.side_centered_tangent_circle import radius_square
from otk.sets.math.olympiad.sum_of_squares_functional_seed import seed_value
from otk.sets.math.olympiad.symmedian_chord_ratio import segment_ab
from otk.sets.math.olympiad.symmetric_reciprocal_constant import CASES as CONSTANT_CASES
from otk.sets.math.olympiad.symmetric_reciprocal_constant import best_constant
from otk.sets.math.olympiad.tangent_diameter_sine import sine_square
from otk.sets.math.olympiad.weighted_square_minimiser import minimiser

KEYS = tuple(
    f"math.{k}_olympiad"
    for k in (
        "bisector_circumradius_angle side_centered_tangent_circle medians_shortest_side tangent_diameter_sine "
        "sum_of_squares_functional_seed cosine_addition_functional weighted_square_minimiser root_square_root_sum "
        "cube_ratio_difference_floor near_wilson_factorial_powers prime_square_exponent_product "
        "exponential_sequence_gcd repunit_residue inverse_power_congruence integer_root_quadratic_count "
        "set_union_cover_count human_pyramid_orders nonadjacent_days consecutive_product_square_kernel "
        "symmedian_chord_ratio cube_root_unity_divisibility monochromatic_rectangle_count coprime_exponent_pair "
        "symmetric_reciprocal_constant"
    ).split()
)


def _angle(p, q, r):
    v, w = np.subtract(p, q), np.subtract(r, q)
    return math.degrees(math.acos(np.dot(v, w) / np.linalg.norm(v) / np.linalg.norm(w)))


def _point(t):
    return (math.cos(t), math.sin(t))


def test_bisector_angle_on_the_circumcircle():
    for angle_b, angle_c in ((70, 50), (43, 71), (80, 40), (55, 85), (61, 61)):
        a_ = math.radians(180 - angle_b - angle_c)
        b_, c_ = math.radians(angle_b), math.radians(angle_c)
        # central angles: arc AB = 2C, arc BC = 2A, arc CA = 2B
        a, d = _point(0), _point(2 * c_ + a_)  # D: midpoint of arc BC away from A
        assert math.isclose(_angle(a, d, (0, 0)), float(bisector_radius_angle(angle_b, angle_c)), abs_tol=1e-7)
        assert b_ > 0
    assert bisector_radius_angle(70, 50) == 10  # the source


def test_side_centred_circle_by_coordinates():
    for a, b, c in itertools.product(range(3, 12), range(2, 10), range(2, 10)):
        if not (b + c > a and a + b > c and a + c > b):
            continue
        x = (c * c - b * b + a * a) / (2 * a)
        apex = np.array([x, math.sqrt(c * c - x * x)])  # B = (0, 0), C = (a, 0)
        centre = np.array([a * c / (b + c), 0.0])  # foot of the bisector from A
        distance = abs(apex[0] * centre[1] - apex[1] * centre[0]) / np.linalg.norm(apex)  # to line AB
        assert math.isclose(distance**2, float(radius_square(a, b, c)), rel_tol=1e-9)
    assert radius_square(4, 3, 2) == Fraction(135, 100)  # the source: (3√15/10)²


def test_medians_by_rebuilding_the_triangle():
    for m1, m2, m3 in itertools.combinations(range(2, 16), 3):
        if m1 + m2 <= m3:
            continue
        sides = [math.sqrt(side_square(m1, m2, m3)), math.sqrt(side_square(m2, m1, m3)), math.sqrt(side_square(m3, m1, m2))]
        a, b, c = sides
        medians = [math.sqrt(2 * b * b + 2 * c * c - a * a) / 2, math.sqrt(2 * a * a + 2 * c * c - b * b) / 2, math.sqrt(2 * a * a + 2 * b * b - c * c) / 2]
        assert np.allclose(medians, [m1, m2, m3])
        assert min(sides) == sides[2]
    assert side_square(5, 3, 4) == Fraction(100, 9)  # the source: 10/3


def test_tangent_diameter_sine_by_construction():
    def build(theta):
        a = np.array(_point(theta))
        b, c = np.array([0.0, -1.0]), np.array([0.0, 1.0])
        # tangent at A: points X with X·A = 1; P on y = −1, Q on x = 0
        p = np.array([(1 + a[1]) / a[0], -1.0])
        q = np.array([0.0, 1 / a[1]])
        return a, b, c, p, q

    for p_, q_ in ((2, 3), (1, 1), (3, 2), (5, 7), (1, 9)):
        lo, hi = 0.01, math.pi / 2 - 0.01
        for _ in range(200):
            mid = (lo + hi) / 2
            a, _, _, p, q = build(mid)
            if np.linalg.norm(q - a) / np.linalg.norm(p - a) > p_ / q_:
                lo = mid
            else:
                hi = mid
        a, b, c, p, q = build(lo)
        assert math.isclose(np.linalg.norm(q - a) / np.linalg.norm(p - a), p_ / q_, rel_tol=1e-9)
        assert math.isclose(math.sin(math.radians(_angle(c, a, q))) ** 2, float(sine_square(p_, q_)), rel_tol=1e-7)
    assert sine_square(2, 3) == Fraction(1, 5)  # the source: 1/√5


def test_functional_seed_by_the_two_families():
    m, n = sympy.symbols("m n")
    # f ≡ c and f(n) = n + c are the two branches f(1) − f(0) = 0, 1
    for f in (lambda x: 7, lambda x: x + 7):
        lhs = f(m**2 + n**2)
        rhs = (f(m) - f(n)) ** 2 + f(2 * m * n)
        assert sympy.expand(lhs - rhs) == 0
    rng = random.Random(1)
    for _ in range(300):
        alpha, beta, total = rng.randint(2, 12), rng.randint(2, 12), rng.randint(50, 4000)
        hits = [c for c in range(total + 1) for f1 in (c, c + 1) if alpha * c + beta * f1 == total]
        assert seed_value(alpha, beta, total) == (hits[0] if len(hits) == 1 else None)
    assert seed_value(8, 9, 2006) == 118  # the source


def test_cosine_functional_identity():
    rng = random.Random(2)
    for k in range(2, 10):
        f = lambda t, k=k: -t / k  # noqa: E731
        for _ in range(50):
            x, y = rng.uniform(-7, 7), rng.uniform(-7, 7)
            assert math.isclose(f(math.cos(x + y)), math.cos(x) * f(math.cos(y)) + k * f(math.sin(x)) * f(math.sin(y)), abs_tol=1e-12)
        assert f(1) < 0
    assert function_value(2, Fraction(2006, 2549)) == Fraction(-1003, 2549)  # the source


def test_minimiser_by_lagrange():
    x, y, lam = sympy.symbols("x y lam")
    for weights in itertools.permutations((1, 2, 3, 4, 7, 9), 3):
        for s in (1, 4):
            z = s - x - y
            g = weights[0] * x**2 + weights[1] * y**2 + weights[2] * z**2
            sol = sympy.solve([sympy.diff(g, x), sympy.diff(g, y)], [x, y], dict=True)[0]
            point = (sol[x], sol[y], s - sol[x] - sol[y])
            assert tuple(Fraction(str(v)) for v in point) == minimiser(weights, s)
    assert minimiser((2, 3, 4), 1)[0] == Fraction(6, 13)  # the source


def test_root_sum_by_numeric_roots():
    for p, q, w in ROOT_CASES[::5] + ((9, 11, 1),):
        roots = np.roots([1, -p, q, -w * w])
        assert np.all(np.abs(roots.imag) < 1e-9) and np.all(roots.real > 0)
        s = float(np.sum(np.sqrt(roots.real)))
        assert math.isclose(s**4 - 2 * p * s * s - 8 * w * s, quartic_value(p, q), abs_tol=1e-6)
    assert quartic_value(9, 11) == -37  # the source


def test_cube_ratio_floor_exactly():
    for d in range(1, 5):
        for n in list(range(d + 1, 60)) + [2548, 3000]:
            v = Fraction((n + d) ** 3, (n - d) * n) - Fraction((n - d) ** 3, n * (n + d))
            assert math.floor(v) == floor_value(n, d)
    assert floor_value(2548, 1) == 8  # the source


def test_near_wilson_by_theorem():
    for p in WILSON_PRIMES:
        half = pow(2, -1, p)
        for e1, e2 in ((2, 3), (p - 3, p - 2), (2 * p + 1, 7)):
            assert residue(p, e1, e2) == (pow(-half % p, e1, p) + 1) % p
    assert residue(29, 26, 27) == 5  # the source


def test_prime_exponent_product_directly():
    for m in (7, 13, 31):
        for last in (5, 40, 200):
            primes = [sympy.prime(k) for k in range(1, last + 1)]
            exponent = sum(p * p - 1 for p in primes)
            assert product_residue(2006, last, m) == pow(2006, exponent, m)
    assert product_residue(2006, 2549, 13) == 10  # the source


def test_sequence_gcd_against_whole_terms():
    for shifts in GCD_CASES:
        for last in (5, 9):
            assert sequence_gcd(shifts, last) == reduce(gcd, (term(n, shifts) for n in range(1, last + 1)))
    assert sequence_gcd((1, 2, 3), 2549) == 14  # the source


def test_repunit_by_integers():
    rng = random.Random(3)
    for _ in range(60):
        k, modulus = rng.randint(1, 3000), rng.randint(2, 3000)
        assert repunit_mod(k, modulus) == int("1" * k) % modulus
    assert repunit_mod(1862, 2006) == 781  # the source


def test_inverse_congruence_by_search():
    for p in INVERSE_PRIMES[::4] + (2549,):
        assert sympy.isprime(p) and (p - 1) % 3
        for j in range(2, 8):
            assert least_solution(p, j) == next(n for n in range(1, p) if pow(n, p - 4, p) == (p - j**3) % p)
    assert least_solution(2549, 2) == 1274  # the source


def test_integer_root_count_by_discriminant():
    for a in range(1, 10):
        for bound in (50, 777, 2549):
            count = 0
            for n in range(1, bound):
                disc = a * a + 4 * n
                count += sympy.ntheory.primetest.is_square(disc) and (math.isqrt(disc) - a) % 2 == 0
            assert root_count(a, bound) == count
    assert root_count(1, 2549) == 49  # the source


def test_cover_count_by_enumeration():
    for k in range(1, 4):
        for n in range(1, 4):
            universe = frozenset(range(n))
            subsets = [frozenset(c) for r in range(n + 1) for c in itertools.combinations(range(n), r)]
            count = sum(1 for sets in itertools.product(subsets, repeat=k) if frozenset().union(*sets) == universe)
            assert cover_base(k) ** n == count
    assert cover_base(3) == 7  # the source: 7^2549


def test_pyramid_orders_by_permutations():
    for top, rows in SHAPES:
        size, pairs = pyramid(top, rows)
        if size <= 9:
            count = sum(all(p.index(u) < p.index(v) for u, v in pairs) for p in itertools.permutations(range(size)))
            assert orders(size, pairs) == count
    assert orders(*pyramid(1, 3)) == 16  # the source


def test_spaced_days_by_enumeration():
    for days in range(1, 15):
        for k in range(1, min(7, days + 1)):
            count = sum(all(b - a > 1 for a, b in zip(c, c[1:])) for c in itertools.combinations(range(days), k))
            assert spaced_choices(days, k) == count
    assert spaced_choices(31, 10) == comb(22, 10) == 646646  # the source


def test_square_multiplier_and_no_square_products():
    for n in range(1, 400):
        value = n * (n + 1) * (n + 2)
        kernel = math.prod(p for p, e in sympy.factorint(value).items() if e % 2)
        assert square_multiplier(n) == kernel > 1
    assert not any(sympy.ntheory.primetest.is_square(n * (n + 1) * (n + 2)) for n in range(1, 100000))


def test_symmedian_ratio_by_construction():
    rng = random.Random(4)
    for _ in range(100):
        ta, tc = rng.uniform(0.2, 1.4), rng.uniform(1.8, 3.0)
        a, c = np.array(_point(ta)), np.array(_point(tc))
        mid = (a + c) / 2
        p = mid / np.dot(mid, mid)  # the pole of AC
        tq = rng.uniform(tc + 0.2, ta + 2 * math.pi - 0.2)  # Q on the far arc
        q = np.array(_point(tq))
        # B = AC ∩ PQ
        s, _ = np.linalg.solve(np.column_stack([c - a, -(q - p)]), p - a)
        b = a + s * (c - a)
        qa, qc = np.linalg.norm(q - a), np.linalg.norm(q - c)
        ab, bc = np.linalg.norm(b - a), np.linalg.norm(c - b)
        assert math.isclose(ab / bc, (qa / qc) ** 2, rel_tol=1e-7)
    for length, p_, q_ in ((12, 2, 5), (7, 3, 1)):
        ab = segment_ab(length, p_, q_)
        assert ab / (length - ab) == Fraction(p_ * p_, q_ * q_)


def test_unity_divisibility_by_sympy():
    x = sympy.symbols("x")
    for u, v, k in ((-5, 9, 1), (3, -2, 2), (0, 4, 3), (7, 7, 4)):
        a, b = -1 - u, -k - v
        p = x**2 + a * x + u
        q = k * x**2 + b * x + v
        expr = sympy.expand(2 * x * p.subs(x, x**3) + q.subs(x, -x - x**2))
        assert sympy.rem(expr, 1 + x + x**2, x) == 0
        bad = sympy.expand(2 * x * (p + 1).subs(x, x**3) + q.subs(x, -x - x**2))
        assert sympy.rem(bad, 1 + x + x**2, x) != 0
        for t in (2, 5, 9):
            assert difference_at(u, k, v, t) == (p - q).subs(x, t)
        assert sympy.rem(p - q, x - 1, x) == 0


def test_rectangles_by_student_enumeration():
    rng = random.Random(5)
    for _ in range(12):
        groups, seats = rng.randint(2, 4), rng.randint(2, 5)
        girls = [rng.randint(0, seats) for _ in range(groups)]
        students = [(r, s, s <= girls[r]) for r in range(groups) for s in range(1, seats + 1)]
        count = 0
        for four in itertools.combinations(students, 4):
            if len({x[0] for x in four}) == 2 and len({x[1] for x in four}) == 2 and len({x[2] for x in four}) == 1:
                count += 1
        g, b, _ = rectangle_counts(girls, seats)
        assert g + b == count
    # the source: every 4 × 7 two-colouring has a monochromatic rectangle
    # (no four pairwise compatible rows), while 4 × 6 can avoid one
    def compatible(r, s, width):
        same = [i for i in range(width) if (r >> i & 1) == (s >> i & 1)]
        return not any((r >> i & 1) == (r >> j & 1) for i, j in itertools.combinations(same, 2))

    def free_grid_exists(width):
        adj = {r: {s for s in range(1 << width) if s != r and compatible(r, s, width)} for r in range(1 << width)}
        return any(adj[a] & adj[b] & adj[c] for a in adj for b in adj[a] for c in adj[a] & adj[b])

    assert not free_grid_exists(7)
    assert free_grid_exists(6)


def test_coprime_pairs_by_brute_force():
    for p in (101, 103, 113, 211):
        for a, b in ((25, 49), (9, 16)):
            pairs = [(m + n, n, m) for m in range(1, 2 * p) for n in range(1, p) if gcd(m, n) == 1 and ((a * b) ** m + a**n - 2 * b**n) % p == 0]
            found = solutions(p, a, b)
            assert found and min(pairs)[0] == found[0][0]
    m, n = 1, 45
    assert ((25 * 49) ** m + 25**n - 2 * 49**n) % 2549 == 0  # the source has such a pair
    assert solutions(2549, 25, 49)[0] == (46, 45, 1)


def test_best_constant_by_sampling():
    rng = random.Random(6)
    for t, u in CONSTANT_CASES[::3] + ((1, 3),):
        k = best_constant(t, u)
        worst = min(
            (t + u / (a * b + b * c + c * a)) * (a + b + c)
            for a, b, c in ([rng.uniform(0.01, 5) for _ in range(3)] for _ in range(3000))
        )
        assert worst >= k - 1e-9
        x = math.sqrt(u / (3 * t))  # a = b = c = x attains the bound
        assert math.isclose((t + u / (3 * x * x)) * 3 * x, k)
    assert best_constant(1, 3) == 6  # the source


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()


def test_factorial_sanity():
    assert factorial(27) % 29 == 1  # Wilson for the source's 27!
