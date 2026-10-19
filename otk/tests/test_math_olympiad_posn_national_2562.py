"""Independent checks for the sets adapted from the 2562 national paper."""

import math
import random
from fractions import Fraction
from itertools import permutations, product
from math import factorial, gcd
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.antipodal_bijection_maximum import (
    antipodal_maximizers,
    antipodal_maximum,
)
from otk.sets.math.olympiad.bilinear_bound_functional import bilinear_bound_value
from otk.sets.math.olympiad.coprime_square_difference_quotient import (
    coprime_quotient_pairs,
)
from otk.sets.math.olympiad.incircle_arc_midpoint_power import (
    TRIANGLES,
    touch_chord_product,
)
from otk.sets.math.olympiad.pentagon_bisector_circumcenter import (
    ASKED,
    pentagon_angle,
)
from otk.sets.math.olympiad.regular_vertex_triangle_dissection import most_sides
from otk.sets.math.olympiad.scaled_cyclic_fraction_inequality import (
    cyclic_fraction_sum,
    scaled_minimum,
)
from otk.sets.math.olympiad.signed_jump_paths import jump_paths, odd_endpoints
from otk.sets.math.olympiad.square_root_shift_functional import shifted_value
from otk.sets.math.olympiad.wilson_reflection_factorial import (
    PRIMES,
    wilson_reflection,
)

KEYS = (
    "math.pentagon_bisector_circumcenter_olympiad",
    "math.coprime_square_difference_quotient_olympiad",
    "math.square_root_shift_functional_olympiad",
    "math.signed_jump_paths_olympiad",
    "math.scaled_cyclic_fraction_inequality_olympiad",
    "math.bilinear_bound_functional_olympiad",
    "math.antipodal_bijection_maximum_olympiad",
    "math.incircle_arc_midpoint_power_olympiad",
    "math.regular_vertex_triangle_dissection_olympiad",
    "math.wilson_reflection_factorial_olympiad",
)


def _angle(x, o, y):
    ux, uy = x[0] - o[0], x[1] - o[1]
    vx, vy = y[0] - o[0], y[1] - o[1]
    cosine = (ux * vx + uy * vy) / math.hypot(ux, uy) / math.hypot(vx, vy)
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))


def _foot(point, origin, direction):
    t = (point[0] - origin[0]) * direction[0] + (point[1] - origin[1]) * direction[1]
    return origin[0] + t * direction[0], origin[1] + t * direction[1]


def _convex(points):
    signs = set()
    for i in range(len(points)):
        (ax, ay), (bx, by), (cx, cy) = points[i - 2], points[i - 1], points[i]
        signs.add((bx - ax) * (cy - by) - (by - ay) * (cx - bx) > 0)
    return len(signs) == 1


def test_pentagon_angles_by_coordinates():
    for half_a in range(10, 36):
        for half_c in range(10, 36):
            al, ga = math.radians(half_a), math.radians(half_c)
            a = (0.0, 0.0)
            b = (math.cos(al), math.sin(al))
            e = _foot(b, a, (math.cos(al), -math.sin(al)))
            c = (b[0] + b[1] / math.tan(ga), 0.0)
            d = _foot(b, c, (-math.cos(ga), -math.sin(ga)))
            assert _convex([a, b, c, d, e])
            # P is where the circle on diameter AB meets AC again.
            p = (b[0], 0.0)
            radius = math.dist(p, b)
            assert math.isclose(math.dist(p, d), radius)
            assert math.isclose(math.dist(p, e), radius)
            measured = {
                "BDE": _angle(b, d, e),
                "DEB": _angle(d, e, b),
                "DPE": _angle(d, p, e),
                "AED": _angle(a, e, d),
            }
            for asked in ASKED:
                assert math.isclose(measured[asked], pentagon_angle(asked, half_a, half_c), abs_tol=1e-7)


def test_coprime_quotient_pairs_by_unbounded_search():
    for k in range(1, 61):
        brute = sum(
            1
            for a in range(2, 200)
            for b in range(1, a)
            if gcd(a, b) == 1 and k * a * (a * a + b * b) % (a * a - b * b) == 0
        )
        assert coprime_quotient_pairs(k) == brute
    assert coprime_quotient_pairs(2) == 0  # the source statement


def test_shifted_functional_solution_satisfies_the_equation():
    rng = random.Random(7)
    for m in (1, 2, 3):
        for _ in range(40):
            a = rng.randint(1, 12)
            value = math.isqrt(4 * m * m * a - 1) + 1 + rng.randint(0, 6)
            constant = value * value - 4 * m * m * a
            assert constant >= 0

            def f(x):
                return math.sqrt(4 * m * m * x + constant)

            for _ in range(20):
                x, y = rng.uniform(0.01, 50), rng.uniform(0.01, 50)
                assert math.isclose(f(x + y * f(x) + m * m * y * y), f(x) + 2 * m * m * y)
            t = rng.randint(1, 3)
            b = a + t * (value + m * m * t)
            assert math.isclose(f(b), shifted_value(m, a, value, b))
    # the source equation (m = 1) is solved by 2√x, the constant-zero member
    assert math.isclose(2 * math.sqrt(9 + 2 * 3 * 4 + 16), 2 * 3 + 2 * 4)


def _enumerate_paths(total, end):
    count = 0

    def walk(remaining, position):
        nonlocal count
        if remaining == 0:
            count += position == end
            return
        for jump in range(1, remaining + 1):
            walk(remaining - jump, position + jump)
            walk(remaining - jump, position - jump)

    walk(total, 0)
    return count


def _odd_by_bitsets(total):
    rows = [1 << total]
    for length in range(1, total + 1):
        acc = 0
        for jump in range(1, length + 1):
            prev = rows[length - jump]
            acc ^= (prev << jump) ^ (prev >> jump)
        rows.append(acc)
    return tuple(i - total for i in range(2 * total + 1) if rows[total] >> i & 1)


def test_jump_paths_by_enumeration_and_parity():
    for total in range(1, 8):
        for end in range(-total, total + 1):
            assert jump_paths(total, end) == _enumerate_paths(total, end)
    for total in list(range(1, 80)) + [2019]:
        assert _odd_by_bitsets(total) == odd_endpoints(total)


def test_scaled_inequality_samples_and_scaling():
    rng = random.Random(11)
    for _ in range(100_000):
        a = math.exp(rng.uniform(-5, 5))
        b = math.exp(rng.uniform(-5, 5))
        assert cyclic_fraction_sum(a, b, 1 / (a * b)) >= 1 - 1e-12
    assert cyclic_fraction_sum(1, 1, 1) == 1
    for s in range(1, 10):
        for _ in range(20):
            a, b = Fraction(rng.randint(1, 30), rng.randint(1, 30)), Fraction(rng.randint(1, 30), rng.randint(1, 30))
            c = 1 / (a * b)
            scaled = cyclic_fraction_sum(s * a, s * b, s * c, s)
            assert scaled == cyclic_fraction_sum(a, b, c) / s
        assert cyclic_fraction_sum(*[Fraction(s)] * 3, s) == scaled_minimum(s)


def test_bilinear_bound_solution_and_perturbations():
    rng = random.Random(5)
    points = [rng.uniform(-20, 20) for _ in range(40)] + [0.0]
    for c in (-4, -2, 2, 3, 7):
        def f(x):
            return c * x / 2
        assert all(x * f(y) + y * f(x) <= c * x * y + 1e-9 for x in points for y in points)
        # any change at one point breaks the inequality at some pair
        for spot in (-3.0, 0.0, 2.5):
            for bump in (-0.5, 0.5):
                def g(x):
                    return f(x) + (bump if x == spot else 0)
                trial = points + [spot]
                assert any(
                    x * g(y) + y * g(x) > c * x * y + 1e-9 for x in trial for y in trial
                )
        assert bilinear_bound_value(c, 4) == Fraction(2 * c)


def test_antipodal_bijections_by_brute_force():
    for n in (1, 2, 3, 4):
        values = list(range(-n, n + 1))
        best, count = -1, 0
        for image in permutations(values):
            f = dict(zip(values, image))
            total = sum(abs(f[k] - f[-k]) for k in range(1, n + 1))
            if total > best:
                best, count = total, 1
            elif total == best:
                count += 1
                assert all(f[k] * f[-k] < 0 for k in range(1, n + 1))
        assert best == antipodal_maximum(n)
        assert count == antipodal_maximizers(n)


def _circumcircle(p, q, r):
    ax, ay = p
    bx, by = q
    cx, cy = r
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return (ux, uy), math.dist((ux, uy), p)


def _other_intersection(o1, r1, o2, r2, known):
    d = math.dist(o1, o2)
    along = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(r1 * r1 - along * along, 0.0))
    ex, ey = (o2[0] - o1[0]) / d, (o2[1] - o1[1]) / d
    mx, my = o1[0] + along * ex, o1[1] + along * ey
    candidates = [(mx - h * ey, my + h * ex), (mx + h * ey, my - h * ex)]
    return max(candidates, key=lambda point: math.dist(point, known))


def test_touch_chord_by_coordinates():
    for a, b, c in TRIANGLES:
        bb, cc = (0.0, 0.0), (float(a), 0.0)
        x = (a * a + c * c - b * b) / (2 * a)
        aa = (x, math.sqrt(c * c - x * x))
        s = (a + b + c) / 2
        incenter = ((a * aa[0] + b * bb[0] + c * cc[0]) / (2 * s), (a * aa[1]) / (2 * s))
        d = (s - b, 0.0)
        centre, radius = _circumcircle(aa, bb, cc)
        mid = ((aa[0] + incenter[0]) / 2, (aa[1] + incenter[1]) / 2)
        k = _other_intersection(centre, radius, mid, math.dist(aa, incenter) / 2, aa)
        dx, dy = incenter[0] - aa[0], incenter[1] - aa[1]
        t = -2 * ((aa[0] - centre[0]) * dx + (aa[1] - centre[1]) * dy) / (dx * dx + dy * dy)
        m = (aa[0] + t * dx, aa[1] + t * dy)
        cross = (d[0] - k[0]) * (m[1] - k[1]) - (d[1] - k[1]) * (m[0] - k[0])
        assert abs(cross) < 1e-7 * a * a
        assert math.isclose(math.dist(k, d) * math.dist(d, m), touch_chord_product(a, b, c), rel_tol=1e-9)


def test_dissection_bound_and_fan():
    for n in range(3, 40, 2):
        # largest m with corner multiples k_i ∈ [1, n−1] summing to (m − 2)n
        feasible = [m for m in range(3, 4 * n) if m <= (m - 2) * n <= m * (n - 1)]
        assert max(feasible) == most_sides(n)
        # centre fan of the regular 2n-gon: apex π/n, base angles (n − 1)π/2n
        apex = Fraction(1, n)
        base = (1 - apex) / 2
        assert (base * n).denominator == 1 and apex + 2 * base == 1
        # and its corners are two base angles
        assert 2 * base == Fraction(n - 1, n)
    with pytest.raises(ValueError):
        most_sides(4)


def test_wilson_reflection_by_direct_factorials():
    for p in PRIMES[:30]:
        for k in range(0, 8):
            n = p - 1 - k
            assert wilson_reflection(p, n) == factorial(n) % p


def test_wilson_reflection_source_argument():
    # odd n with n! + 1 composite, found by the reflection n ↔ p − 1 − n
    found = set()
    for k in range(3, 12, 2):
        value = factorial(k) + 1
        for p in range(k + 2, 2000):
            if value % p == 0 and all(p % q for q in range(2, int(p**0.5) + 1)):
                n = p - 1 - k
                assert n % 2 == 1 and (factorial(n) + 1) % p == 0
                found.add(n)
    assert any(factorial(n) + 1 > p for n in found)


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()


def test_small_cases_product_checks():
    # one extra exhaustive check of the coprime-pair lemma: a² − b² | 2k
    for k in range(1, 30):
        for a, b in product(range(1, 40), repeat=2):
            if a > b and gcd(a, b) == 1 and k * a * (a * a + b * b) % (a * a - b * b) == 0:
                assert (2 * k) % (a * a - b * b) == 0
