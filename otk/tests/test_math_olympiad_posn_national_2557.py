"""Independent checks for the sets adapted from the 2557 national paper."""

import itertools
import math
import random
from math import factorial, gcd
from random import Random

import pytest
import sympy

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.cyclic_ratio_product_bound import largest_k, root_tex
from otk.sets.math.olympiad.exponential_divisor_polynomials import (
    common_divisor,
    polynomial_count,
)
from otk.sets.math.olympiad.factorial_card_cover import fewest_cards
from otk.sets.math.olympiad.isosceles_extension_angles import ASKED, extension_angle
from otk.sets.math.olympiad.lattice_walk_signed_distances import recorded_sum
from otk.sets.math.olympiad.parallel_chord_circumcenters import circumcenter_distance
from otk.sets.math.olympiad.prime_quadratic_cube import (
    LIMIT,
    PAIRS,
    coefficients,
    cube_primes,
)
from otk.sets.math.olympiad.two_solution_functional import SOLUTIONS, possible_values

KEYS = (
    "math.isosceles_extension_angles_olympiad",
    "math.two_solution_functional_olympiad",
    "math.lattice_walk_signed_distances_olympiad",
    "math.exponential_divisor_polynomials_olympiad",
    "math.cyclic_ratio_product_bound_olympiad",
    "math.prime_quadratic_cube_olympiad",
    "math.parallel_chord_circumcenters_olympiad",
    "math.factorial_card_cover_olympiad",
)


def _angle(x, o, y):
    ux, uy = x[0] - o[0], x[1] - o[1]
    vx, vy = y[0] - o[0], y[1] - o[1]
    return math.degrees(math.acos((ux * vx + uy * vy) / math.hypot(ux, uy) / math.hypot(vx, vy)))


def test_isosceles_extension_by_coordinates_and_source_identity():
    for apex in range(20, 141, 4):
        t = math.radians(apex)
        a, b, c = (0.0, 0.0), (1.0, 0.0), (math.cos(t), math.sin(t))
        base = math.dist(b, c)
        e = (1 + base, 0.0)
        measured = {"BEC": _angle(b, e, c), "ACE": _angle(a, c, e), "CBE": _angle(c, b, e)}
        for asked in ASKED:
            assert math.isclose(measured[asked], extension_angle(asked, apex), abs_tol=1e-9)
    # the source configuration (apex 100°, AD = BC as well): BC·DE = BD·CE
    t = math.radians(100)
    b, c = (1.0, 0.0), (math.cos(t), math.sin(t))
    base = math.dist(b, c)
    d, e = (base, 0.0), (1 + base, 0.0)
    assert math.isclose(base * math.dist(d, e), math.dist(b, d) * math.dist(c, e))


def test_two_functional_solutions_by_sympy():
    x, y = sympy.symbols("x y")
    for f in (lambda v: v, lambda v: -v**2):
        assert sympy.expand(f(x * y - 1) + f(x) * f(y) - (2 * x * y - 1)) == 0
    # the two cases split at f(1) = ±1, and no affine or quadratic other solution
    a, b, c = sympy.symbols("a b c")
    g = lambda v: a * v**2 + b * v + c  # noqa: E731
    residual = sympy.Poly(sympy.expand(g(x * y - 1) + g(x) * g(y) - 2 * x * y + 1), x, y)
    solutions = sympy.solve(residual.coeffs(), [a, b, c], dict=True)
    assert sorted((s[a], s[b], s[c]) for s in solutions) == [(-1, 0, 0), (0, 1, 0)]
    for n in range(-5, 6):
        assert possible_values(n) == tuple(f(n) for f in SOLUTIONS)


def test_lattice_walks_by_simulation():
    rng = random.Random(3)
    for _ in range(300):
        x, y = rng.randint(0, 6), rng.randint(0, 6)
        start, total = (x, y), 0
        for _ in range(rng.randint(1, 40)):
            dx, dy = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            if x + dx < 0 or y + dy < 0:
                continue
            if dx:  # parallel to the X axis: distance to it is y
                total += y if abs(x + dx) > abs(x) else -y
            else:
                total += x if abs(y + dy) > abs(y) else -x
            x, y = x + dx, y + dy
        assert total == recorded_sum(start, (x, y))


def test_exponential_divisors_by_brute_force():
    for base in range(3, 41):
        for constant in range(2, 301, 7):
            brute = 0
            for n in range(1, 60):
                brute = gcd(brute, base**n + constant)
            assert common_divisor(base, constant) == brute
            assert polynomial_count(base, constant) == 2 * sympy.divisor_count(brute)
    # the source: 2557ⁿ + 213·2014 admits only P = ±1
    assert polynomial_count(2557, 213 * 2014) == 2


def test_cyclic_ratio_bound_numerically():
    rng = random.Random(9)

    def gap(k, scale, a, b, c):
        left = (k + a / b) * (k + b / c) * (k + c / a)
        right = scale * (a / b + b / c + c / a) * (b / a + c / b + a / c)
        return right - left

    for scale in (1, 2, 3, 7, 15, 30):
        k = largest_k(scale)
        for _ in range(20000):
            a, b, c = (math.exp(rng.uniform(-4, 4)) for _ in range(3))
            assert gap(k, scale, a, b, c) >= -1e-9 * (1 + k) ** 3
        assert gap(k + 1e-6, scale, 1, 1, 1) < 0
    # exact form of the answer
    assert root_tex(9, 3, minus=1) == r"\sqrt[3]{9}-1"
    assert root_tex(216, 3, minus=1) == "5"
    assert root_tex(72, 3, minus=1) == r"2\sqrt[3]{9}-1"


def test_prime_cubes_by_independent_search():
    for first, second in PAIRS:
        alpha, beta = coefficients(first, second)
        found = tuple(
            int(p)
            for p in sympy.primerange(2, LIMIT + 1)
            if (v := alpha * p * p - beta * p - 1) > 0 and sympy.integer_nthroot(v, 3)[1]
        )
        assert cube_primes(alpha, beta) == found
        assert {first, second} <= set(found)
    assert cube_primes(2, 3) == (2, 3)  # the source, 2p² − 3p − 1
    # beyond the bound the source has no more: p ≤ 10⁵
    assert [p for p in sympy.primerange(2, 10**5) if sympy.integer_nthroot(2 * p * p - 3 * p - 1, 3)[1]] == [2, 3]


def _circumcenter(p, q, r):
    ax, ay = p
    bx, by = q
    cx, cy = r
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return ux, uy


def test_parallel_chord_circumcenters_by_coordinates():
    rng = random.Random(4)
    for angle in (30, 45, 60, 90, 120, 135, 150):
        for _ in range(30):
            t = math.radians(angle)
            d = (0.0, 0.0)
            radius = rng.uniform(1, 3)
            a = (radius * math.cos(t), radius * math.sin(t))
            b = (a[0] + rng.uniform(0.5, 3), a[1] + rng.uniform(-0.5, 0.5))
            e = (b[0] - a[0] * b[1] / a[1], 0.0)  # BE ∥ AD
            side = math.dist(a, b)
            lengths = []
            for p in (0.3, 1.7, 4.1):
                o1 = _circumcenter(a, (p, 0.0), d)
                o2 = _circumcenter(b, (p, 0.0), e)
                lengths.append(math.dist(o1, o2))
            assert max(lengths) - min(lengths) < 1e-9
            q, r = circumcenter_distance(1, angle)
            assert math.isclose(lengths[0], side * float(q) * math.sqrt(r), rel_tol=1e-9)


def _covers(cards, target):
    reach = 1
    for card in cards:
        reach |= reach << card
    return all(reach >> t & 1 for t in range(1, target + 1))


def test_factorial_cards_by_exhaustive_search():
    for n in range(1, 6):
        values = [factorial(m) for m in range(1, n + 1)]
        best = next(
            size
            for size in itertools.count(1)
            if any(
                _covers(combo, factorial(n))
                for combo in itertools.combinations_with_replacement(values, size)
            )
        )
        assert best == fewest_cards(n)


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
