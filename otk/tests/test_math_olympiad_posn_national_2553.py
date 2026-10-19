"""Independent checks for the sets adapted from the 2553 national paper."""

import itertools
import math
import random
from fractions import Fraction
from math import isqrt
from random import Random

import pytest
import sympy

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.ball_box_extremes_count import extreme_box_count
from otk.sets.math.olympiad.binomial_prime_lucas import binomial_primes
from otk.sets.math.olympiad.bisector_foot_midline import TRIANGLES as MIDLINE_TRIANGLES
from otk.sets.math.olympiad.bisector_foot_midline import feet_distance
from otk.sets.math.olympiad.circular_distance_pigeonhole import guaranteed_distance
from otk.sets.math.olympiad.diamond_sum_functional import cross_value
from otk.sets.math.olympiad.equilateral_cevian_angle import ANGLES, cevian_angle
from otk.sets.math.olympiad.fifth_power_ratio_minimum import ratio_minimum
from otk.sets.math.olympiad.forced_equal_roots import forced_root
from otk.sets.math.olympiad.prime_power_sum_divisibility import triple_count
from otk.sets.math.olympiad.quadratic_scaling_functional import polynomial_value, scaled_value
from otk.sets.math.olympiad.ramsey_class_threshold import RAMSEY, threshold
from otk.sets.math.olympiad.repdigit_sandwich_divisibility import TRIPLES, next_hit
from otk.sets.math.olympiad.shifted_square_pairs import PAIRS, square_pair_count
from otk.sets.math.olympiad.squared_side_triangle_area import combined, sixteen_area_sq
from otk.sets.math.olympiad.tournament_square_sums import random_scores, square_sums
from otk.sets.math.olympiad.trapezoid_circle_diameter import HERONIAN, diameter

KEYS = tuple(
    f"math.{k}_olympiad"
    for k in (
        "ball_box_extremes_count trapezoid_circle_diameter repdigit_sandwich_divisibility "
        "equilateral_cevian_angle tournament_square_sums quadratic_scaling_functional "
        "fifth_power_ratio_minimum circular_distance_pigeonhole forced_equal_roots "
        "binomial_prime_lucas shifted_square_pairs ramsey_class_threshold bisector_foot_midline "
        "squared_side_triangle_area diamond_sum_functional prime_power_sum_divisibility"
    ).split()
)


def _intersect(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])


def _angle(x, o, y):
    u, v = (x[0] - o[0], x[1] - o[1]), (y[0] - o[0], y[1] - o[1])
    return math.degrees(math.acos((u[0] * v[0] + u[1] * v[1]) / math.hypot(*u) / math.hypot(*v)))


def test_ball_boxes_by_enumeration():
    for balls in range(5, 20):
        brute = sum(
            1 for x in itertools.product(range(1, balls), repeat=5)
            if sum(x) == balls and x[0] + x[4] >= x[1] + x[2] + x[3]
        )
        assert extreme_box_count(balls) == brute
    assert extreme_box_count(11) == 55  # the source


def test_trapezoid_diameter_by_coordinates():
    rng = random.Random(2)
    for _ in range(50):
        k, h = rng.uniform(-0.5, 0.8), rng.uniform(1.5, 3)
        radius = math.hypot(1, k)

        def second(p, q):
            dx, dy = q[0] - p[0], q[1] - p[1]
            t = -2 * (p[0] * dx + (p[1] - k) * dy) / (dx * dx + dy * dy)
            return p[0] + t * dx, p[1] + t * dy

        b, c, a = (-1.0, 0.0), (1.0, 0.0), (0.0, h)
        d, e = second(b, a), second(c, a)
        dy = math.sqrt(radius * radius - e[0] ** 2)
        f = max([(e[0], k - dy), (e[0], k + dy)], key=lambda p: math.dist(p, e))
        assert math.isclose(math.dist(d, f), 2 * radius)  # DF is a diameter
        x, y, z = 2.0, math.dist(c, f), math.dist(b, f)
        area = abs((c[0] - b[0]) * (f[1] - b[1]) - (c[1] - b[1]) * (f[0] - b[0])) / 2
        assert math.isclose(math.dist(d, f), x * y * z / (2 * area))
    for x, y, z in HERONIAN[::25]:
        s = (x + y + z) / 2
        assert math.isclose(float(diameter(x, y, z)), x * y * z / (2 * math.sqrt(s * (s - x) * (s - y) * (s - z))))


def test_repdigit_hits_by_big_integers():
    for a, b, c, n in TRIPLES[::7]:
        modulus = int(f"{a}{b}{b}{c}")
        hits = [m for m in range(3, n + 1) if int(f"{a}{str(b) * m}{c}") % modulus == 0]
        assert hits[0] == n
    assert [m for m in range(1, 30) if int("2" + "5" * m + "3") % 2553 == 0] == [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]
    assert next_hit(2, 5, 3) == 5


def test_equilateral_cevian_angles_by_coordinates():
    a, b, c = (0.0, 0.0), (1.0, 0.0), (0.5, math.sqrt(3) / 2)
    for (p, q), _ in ANGLES.items():
        t = p / q
        m, n = (1 - t, 0.0), (t * c[0], t * c[1])  # BM = t·AB and AN = BM
        o = _intersect(c, m, b, n)
        for asked, measured in (("AOB", _angle(a, o, b)), ("AOC", _angle(a, o, c)), ("BOC", _angle(b, o, c))):
            assert math.isclose(measured, cevian_angle((p, q), asked), abs_tol=1e-9)


def test_tournament_square_sums_by_simulation():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(3, 10)
        wins = random_scores(n, rng)
        losses = [n - 1 - w for w in wins]
        assert sum(w * w for w in wins) == sum(b * b for b in losses) == square_sums(wins)["losses"]


def test_quadratic_functional_by_sympy():
    x, y = sympy.symbols("x y")
    coeffs = sympy.symbols("c0:7")
    f = lambda v: sum(c * v**i for i, c in enumerate(coeffs))  # noqa: E731
    residual = sympy.Poly(sympy.expand(f(3 * x + y) + f(3 * x - y) - f(x + y) - f(x - y) - 16 * f(x)), x, y)
    solution = sympy.solve(residual.coeffs(), coeffs, dict=True)[0]
    assert all(solution.get(c, c) == 0 for i, c in enumerate(coeffs) if i != 2)
    assert scaled_value(3, 2) == 3 * 256
    assert polynomial_value(2, 12, 5) == Fraction(75)
    # f(x) = x² satisfies it, so f(−x) = f(x) as the source asks
    assert sympy.expand((3 * x + y) ** 2 + (3 * x - y) ** 2 - (x + y) ** 2 - (x - y) ** 2 - 16 * x**2) == 0


def test_fifth_power_minimum_by_sampling():
    rng = random.Random(7)
    for total in (3, 6, 10, 20):
        for _ in range(3000):
            a, b = rng.uniform(0.01, total), rng.uniform(0.01, total)
            if a + b >= total:
                continue
            c = total - a - b
            s = a**5 / (b * c * c) + b**5 / (c * a * a) + c**5 / (a * b * b)
            assert s >= a * a + b * b + c * c - 1e-9 >= float(ratio_minimum(total)) - 1e-6


def test_circular_distance_by_search():
    for length in range(6, 16):
        for size in range(2, length + 1):
            best = 0
            for subset in itertools.combinations(range(length), size):
                gaps = [(subset[(i + 1) % size] - subset[i]) % length or length for i in range(size)]
                best = max(best, min(gaps))
            assert best == guaranteed_distance(length, size)
    assert guaranteed_distance(2553, 70) == 36  # the source


def test_forced_roots_by_cauchy_and_sympy():
    x = sympy.symbols("x")
    assert forced_root(5, 2, 5, 5) == Fraction(-1, 2)  # the source
    poly = sympy.Poly(2 * (x + sympy.Rational(1, 2)) ** 5, x)
    assert poly.all_coeffs()[:3] == [2, 5, 5]
    with pytest.raises(ValueError):
        forced_root(5, 2, 5, 4)


def test_binomial_primes_by_lucas():
    for n in range(30, 201, 7):
        for c in range(1, 21):
            lucas = [p for p in sympy.primerange(2, n + 1) if (n // p + c) % p == 0]
            assert binomial_primes(n, c) == lucas
    assert binomial_primes(100, 7) == [7]  # the source


def test_square_pairs_by_brute_force():
    for a, b in PAIRS:
        for limit in (10**3, 10**4):
            brute = sum(1 for x in range(1, limit + 1) if isqrt(a * x - 1) ** 2 == a * x - 1 and isqrt(b * x - 1) ** 2 == b * x - 1)
            assert square_pair_count(a, b, limit) == brute
    # the source: never all three
    for x in range(1, 2 * 10**5):
        assert not all(isqrt(y * x - 1) ** 2 == y * x - 1 for y in (2, 5, 13))


def test_ramsey_numbers():
    def mono_triangle(n, colours, colour_of):
        return any(colour_of(i, j) == colour_of(j, k) == colour_of(i, k) for i, j, k in itertools.combinations(range(n), 3))

    edges5 = list(itertools.combinations(range(5), 2))
    assert any(
        not mono_triangle(5, 2, lambda i, j, col=dict(zip(edges5, c)): col[(i, j)])
        for c in itertools.product((0, 1), repeat=len(edges5))
    )
    edges6 = list(itertools.combinations(range(6), 2))
    assert all(
        mono_triangle(6, 2, lambda i, j, col=dict(zip(edges6, c)): col[(i, j)])
        for c in itertools.product((0, 1), repeat=len(edges6))
    )

    # K16 without a one-colour triangle (Greenwood–Gleason): GF(16), colour by the
    # coset of the difference in the multiplicative group modulo cubes
    def mul(u, v):
        r = 0
        for i in range(4):
            if v >> i & 1:
                r ^= u << i
        for i in range(7, 3, -1):
            if r >> i & 1:
                r ^= 0b10011 << (i - 4)
        return r

    power, log = 1, {}
    for e in range(15):
        log[power] = e
        power = mul(power, 2)
    assert len(log) == 15
    assert not mono_triangle(16, 3, lambda i, j: log[i ^ j] % 3)
    assert threshold(120, 3) == 16 * 120 + 1 == 1921  # the source: 2010 ≥ 1921
    assert RAMSEY == {2: 6, 3: 17}


def test_bisector_feet_by_coordinates():
    for a, b, c in MIDLINE_TRIANGLES[::40]:
        bb, cc = (0.0, 0.0), (float(a), 0.0)
        x = (a * a + c * c - b * b) / (2 * a)
        aa = (x, math.sqrt(c * c - x * x))

        def foot(vertex, p, q):
            u = ((p[0] - vertex[0]) / math.dist(vertex, p) + (q[0] - vertex[0]) / math.dist(vertex, q),
                 (p[1] - vertex[1]) / math.dist(vertex, p) + (q[1] - vertex[1]) / math.dist(vertex, q))
            t = ((aa[0] - vertex[0]) * u[0] + (aa[1] - vertex[1]) * u[1]) / (u[0] ** 2 + u[1] ** 2)
            return vertex[0] + t * u[0], vertex[1] + t * u[1]

        d, e = foot(bb, aa, cc), foot(cc, aa, bb)
        m = _intersect(d, e, aa, bb)
        n = _intersect(d, e, aa, cc)
        assert math.isclose(math.dist(d, e), float(feet_distance(a, b, c)))
        assert math.isclose((b + c) / a, math.dist(d, e) / math.dist(m, n) + 1)  # the source


def test_squared_side_triangles_by_heron():
    rng = random.Random(9)
    for _ in range(300):
        t1 = sorted(rng.uniform(1, 10) for _ in range(3))
        t2 = sorted(rng.uniform(1, 10) for _ in range(3))
        if t1[2] >= t1[0] + t1[1] or t2[2] >= t2[0] + t2[1]:
            continue
        rng.shuffle(t1)
        rng.shuffle(t2)
        t3 = [math.sqrt(u * u + v * v) for u, v in zip(t1, t2)]
        assert max(t3) < sum(t3) - max(t3)  # a triangle
        areas = [math.sqrt(max(sixteen_area_sq(*(v * v for v in t)), 0)) / 4 for t in (t1, t2, t3)]
        for i in range(3):
            heights = [2 * area / t[i] for area, t in zip(areas, (t1, t2, t3))]
            assert heights[2] ** 2 >= heights[0] ** 2 + heights[1] ** 2 - 1e-9
    assert combined((3, 4, 5), (3, 4, 5)) == 16 * 4 * 36


def test_diamond_functional_constants():
    for dimension in (1, 2, 3):
        value = cross_value(2010, dimension)
        assert 2 * dimension * value == 2010
    assert cross_value(2010, 2) == Fraction(1005, 2)  # the source
    # among quadratic polynomials in the plane only constants work
    x, y, t = sympy.symbols("x y t")
    cs = sympy.symbols("c0:6")
    f = lambda u, v: cs[0] + cs[1] * u + cs[2] * v + cs[3] * u * u + cs[4] * u * v + cs[5] * v * v  # noqa: E731
    total = sympy.expand(f(x - t, y) + f(x + t, y) + f(x, y - t) + f(x, y + t))
    coefficients = sympy.Poly(total, x, y, t).coeffs()
    nonconstant = [c for c, m in zip(coefficients, sympy.Poly(total, x, y, t).monoms()) if m != (0, 0, 0)]
    solution = sympy.solve(nonconstant, cs[1:], dict=True)[0]
    assert all(solution.get(c, c) == 0 for c in cs[1:])


def test_prime_triples_by_exact_integers():
    for limit in (5, 7, 11, 13):
        primes = list(sympy.primerange(2, limit + 1))
        brute = sum(1 for p in primes for q in primes for r in primes if (r**p + r**q) % (p * q) == 0)
        assert triple_count(limit) == brute
    primes = list(sympy.primerange(2, 40))
    assert not any((r**p + r**q) % (p * q) == 0 for p in primes for q in primes for r in primes if p > r and q > r)


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()


