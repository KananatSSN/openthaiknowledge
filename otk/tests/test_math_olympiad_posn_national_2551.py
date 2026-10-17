"""Independent checks for the sets adapted from the 2551 national paper."""

import itertools
import math
import random
from fractions import Fraction
from math import comb, gcd, isqrt
from random import Random

import pytest
import sympy

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.almost_additive_scaling_bound import scaling_bound
from otk.sets.math.olympiad.alternating_harmonic_block import odd_reciprocal_sum
from otk.sets.math.olympiad.binomial_alternating_residue import alternating_sum, residue
from otk.sets.math.olympiad.equal_circles_inradius_ratio import CONFIGS, inradius_ratio
from otk.sets.math.olympiad.floor_equation_solutions import FAMILIES, floor_solutions
from otk.sets.math.olympiad.folded_angle_distance_equality import equality_b
from otk.sets.math.olympiad.gcd_lcm_square_sum import CASES as GL_CASES
from otk.sets.math.olympiad.gcd_lcm_square_sum import pairs_for
from otk.sets.math.olympiad.nested_subset_chain_count import chain_count
from otk.sets.math.olympiad.nonresidue_exponential_nonsquare import CASES as NR_CASES
from otk.sets.math.olympiad.nonresidue_exponential_nonsquare import witness_prime
from otk.sets.math.olympiad.polynomial_difference_equation import difference_value
from otk.sets.math.olympiad.right_triangle_cevian_cosine import cosine_parts, cosine_tex
from otk.sets.math.olympiad.same_sex_handshake_average import handshake_average
from otk.sets.math.olympiad.side_points_triangle_count import most_triangles
from otk.sets.math.olympiad.smallest_divisor_square_sum import divisor_square_sum
from otk.sets.math.olympiad.square_root_functional_iterate import iterated_value
from otk.sets.math.olympiad.tangent_midpoint_rhombus_area import CASES as RHOMBUS_CASES
from otk.sets.math.olympiad.tangent_midpoint_rhombus_area import rhombus_area

KEYS = tuple(
    f"math.{k}_olympiad"
    for k in (
        "right_triangle_cevian_cosine equal_circles_inradius_ratio floor_equation_solutions "
        "folded_angle_distance_equality polynomial_difference_equation almost_additive_scaling_bound "
        "gcd_lcm_square_sum nonresidue_exponential_nonsquare nested_subset_chain_count "
        "side_points_triangle_count tangent_midpoint_rhombus_area smallest_divisor_square_sum "
        "alternating_harmonic_block binomial_alternating_residue same_sex_handshake_average "
        "square_root_functional_iterate"
    ).split()
)


def test_cevian_cosine_by_coordinates():
    for angle_b in (30, 45, 60):
        for p, q in itertools.product(range(1, 7), repeat=2):
            if p == q:
                continue
            ac = math.tan(math.radians(angle_b))
            e = (q / (p + q), p * ac / (p + q))
            measured = e[1] / math.hypot(*e)
            k, s, d = cosine_parts(angle_b, p, q)
            assert math.isclose(measured, k * math.sqrt(s) / math.sqrt(d))
            tex = cosine_tex(k, s, d)
            value = sympy.nsimplify(k * sympy.sqrt(s) / sympy.sqrt(d))
            assert math.isclose(float(value), measured)
            assert tex.count(r"\sqrt") <= 1
    k, s, d = cosine_parts(60, 3, 2)
    assert math.isclose(k * math.sqrt(s) / math.sqrt(d), 3 * math.sqrt(3) / math.sqrt(31))  # the source


def test_equal_circles_by_coordinates():
    for h, m, e in CONFIGS:
        a, b, c, d = (0.0, float(h)), (-float(m), 0.0), (float(m), 0.0), (float(e), 0.0)

        def inradius(p, q, r):
            sides = [math.dist(p, q), math.dist(q, r), math.dist(r, p)]
            area = abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) / 2
            return area / (sum(sides) / 2)

        # equal circumradii of ABD and ACD (the equal circles through A, D)
        def circumradius(p, q, r):
            sides = [math.dist(p, q), math.dist(q, r), math.dist(r, p)]
            area = abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) / 2
            return sides[0] * sides[1] * sides[2] / (4 * area)

        assert math.isclose(circumradius(a, b, d), circumradius(a, c, d))
        assert math.isclose(inradius(a, b, d) / inradius(a, c, d), float(inradius_ratio(h, m, e)))
    assert inradius_ratio(12, 9, 5) == Fraction(8, 3)  # the source


def test_floor_equations_by_wide_search():
    for family in FAMILIES:
        a, b, c, d, e = family
        brute = [x for x in range(1, 5000) if x + x // a == (b * x) // c + (d * x) // e]
        assert floor_solutions(*family) == brute
    # non-integers never work for the source
    for x in [Fraction(k, 7) for k in range(1, 300) if k % 7]:
        assert x + (x / 3).__floor__() != (2 * x / 3).__floor__() + (3 * x / 5).__floor__()
    assert floor_solutions(3, 2, 3, 3, 5) == [2, 5]


def test_folded_distance_equality_numerically():
    rng = random.Random(1)
    for _ in range(2000):
        a, b, c = (rng.uniform(0.1, 10) for _ in range(3))
        lhs = math.sqrt(a * a + b * b - math.sqrt(2) * a * b) + math.sqrt(b * b + c * c - math.sqrt(2) * b * c)
        assert lhs >= math.hypot(a, c) - 1e-9
    for a, c in itertools.product(range(1, 8), repeat=2):
        b = float(equality_b(a, c)) * math.sqrt(2)
        lhs = math.sqrt(a * a + b * b - math.sqrt(2) * a * b) + math.sqrt(b * b + c * c - math.sqrt(2) * b * c)
        assert math.isclose(lhs, math.hypot(a, c))


def test_polynomial_difference_by_sympy():
    x = sympy.symbols("x")
    for a, b, c in itertools.product(range(0, 4), range(-3, 4), range(-3, 4)):
        p = sympy.Rational(a, 2) * x**2 + (b - sympy.Rational(a, 2)) * x + c
        assert sympy.expand(p.subs(x, x + 1) - p) == a * x + b
        for n in (3, 7, 12):
            assert difference_value(a, b, c, n) == p.subs(x, n)
    # the source: P(x + 1) − P(x) = 1 forces degree 1
    q = sympy.Poly(sympy.symbols("c0:5")[0] + sum(s * x**i for i, s in enumerate(sympy.symbols("c1:5"), start=1)), x)
    diff = sympy.Poly(sympy.expand(q.as_expr().subs(x, x + 1) - q.as_expr() - 1), x)
    sol = sympy.solve(diff.coeffs(), sympy.symbols("c1:5"), dict=True)[0]
    assert sol[sympy.Symbol("c1")] == 1 and all(sol.get(sympy.Symbol(f"c{i}"), 0) == 0 for i in (2, 3, 4))


def test_scaling_bound_examples():
    for n in (2, 5, 30):
        c = 0.999
        f = lambda t: c * math.floor(t)  # noqa: E731
        worst = max(abs(f(n * x) - n * f(x)) for x in [k / 1000 for k in range(1, 1000)])
        assert worst < scaling_bound(n) and worst > scaling_bound(n) * 0.99
        for x, y in itertools.product([k / 7 for k in range(-20, 20)], repeat=2):
            assert abs(f(x + y) - f(x) - f(y)) < 1


def test_gcd_lcm_cases_by_brute_force():
    for s, t, answer in GL_CASES:
        brute = [(m, n) for m in range(1, isqrt(s) + 1) for n in range(m, isqrt(s) + 1) if m * m + n * n == s and gcd(m, n) + m * n // gcd(m, n) == t]
        assert len(brute) == 1 and sum(brute[0]) == answer
    assert pairs_for(3789, 633) == [(42, 45)]  # the source: 87


def test_witness_primes_and_nonsquares():
    for a, b, c, d, p in NR_CASES:
        assert witness_prime(a, b, c, d) == p
        for n in range(1, 8):
            v = a * b**n - c * d**n
            assert v < 0 or isqrt(v) ** 2 != v
    for n in range(1, 30):
        v = 2551 * 543**n - 2008 * 7**n
        assert isqrt(v) ** 2 != v and v % 7 in (3, 5, 6)


def test_subset_chains_by_enumeration():
    for n in range(1, 6):
        subsets = [frozenset(s) for size in range(n + 1) for s in itertools.combinations(range(n), size)]
        assert sum(1 for x, y in itertools.product(subsets, repeat=2) if x <= y) == chain_count(n, 2)
        assert sum(1 for x, y, z in itertools.product(subsets, repeat=3) if x <= y <= z) == chain_count(n, 3)
    assert chain_count(10, 2) == 3**10  # the source


def test_side_points_by_distribution_search():
    for extra in range(1, 30):
        total = extra + 3
        best = max(
            comb(total, 3) - sum(comb(k, 3) for k in (k1, k2, extra + 6 - k1 - k2))
            for k1 in range(2, extra + 5) for k2 in range(2, extra + 5) if extra + 6 - k1 - k2 >= 2
        )
        assert most_triangles(extra) == best
    assert most_triangles(17) == 993  # the source


def test_rhombus_by_construction():
    for t, c in RHOMBUS_CASES[::15]:
        # tangent points A, B symmetric about the x-axis, P on the axis
        half = c / 2
        height = math.sqrt(t * t - half * half)
        p, a, b = (0.0, 0.0), (height, half), (height, -half)
        m = ((p[0] + a[0]) / 2, (p[1] + a[1]) / 2)
        n = ((a[0] + b[0]) / 2, 0.0)
        # circle tangent to PA at A and PB at B: centre on the axis
        cx = t * t / height
        r = math.dist((cx, 0.0), a)
        dx, dy = n[0] - m[0], n[1] - m[1]
        fx, fy = m[0] - cx, m[1]
        aa, bb, cc = dx * dx + dy * dy, 2 * (fx * dx + fy * dy), fx * fx + fy * fy - r * r
        tc = (-bb + math.sqrt(bb * bb - 4 * aa * cc)) / (2 * aa)
        cpt = (m[0] + tc * dx, m[1] + tc * dy)
        dx2, dy2 = cpt[0] - p[0], cpt[1] - p[1]
        aa2, bb2, cc2 = dx2 * dx2 + dy2 * dy2, 2 * ((p[0] - cx) * dx2 + p[1] * dy2), (p[0] - cx) ** 2 + p[1] ** 2 - r * r
        roots = sorted(((-bb2 - math.sqrt(bb2 * bb2 - 4 * aa2 * cc2)) / (2 * aa2), (-bb2 + math.sqrt(bb2 * bb2 - 4 * aa2 * cc2)) / (2 * aa2)))
        dpt = (p[0] + roots[0] * dx2, p[1] + roots[0] * dy2)
        # O = ND ∩ PB
        ex, ey = dpt[0] - n[0], dpt[1] - n[1]
        gx, gy = b[0] - p[0], b[1] - p[1]
        det = ex * (-gy) - ey * (-gx)
        s = ((p[0] - n[0]) * (-gy) - (p[1] - n[1]) * (-gx)) / det
        o = (n[0] + s * ex, n[1] + s * ey)
        side = t / 2
        for u, v in ((m, n), (n, o), (o, p), (p, m)):
            assert math.isclose(math.dist(u, v), side, rel_tol=1e-9)
        area = abs(sum(q1[0] * q2[1] - q2[0] * q1[1] for q1, q2 in zip((m, n, o, p), (n, o, p, m)))) / 2
        assert math.isclose(area, float(rhombus_area(t, c)), rel_tol=1e-9)


def test_divisor_square_sums_and_source():
    def divisors(n):
        return sorted(d for d in range(1, n + 1) if n % d == 0)

    for n in range(12, 400):
        ds = divisors(n)
        if len(ds) >= 4:
            assert divisor_square_sum(n) == sum(d * d for d in ds[:4])
    hits = []
    for n in range(2, 20000):
        ds = divisors(n) if n < 2000 else [d for d in range(1, 200) if n % d == 0]
        if len(ds) >= 4 and sum(d * d for d in ds[:4]) == n and len(sympy.primefactors(n)) >= 2:
            hits.append(n)
    assert hits == [130]


def test_alternating_harmonic_block():
    for n in range(1, 12):
        direct = sum((Fraction(1, (2 * k - 1) * 2 * k) for k in range(1, n + 1)), Fraction(0))
        assert direct == odd_reciprocal_sum(n)
        assert direct >= Fraction(2 * n, 3 * n + 1)  # the key step of the source inequality
        lhs = sum(n ** (1 / ((2 * k - 1) * 2 * k)) for k in range(1, n + 1))
        a = lambda j: j * (j + 1)  # noqa: E731
        assert lhs >= n ** (a(3 * n + 2) / a(3 * n + 1)) - 1e-9


def test_binomial_residues_closed_form():
    for n in range(0, 25):
        assert residue(n, 2008, 19) != 0  # the source
        assert alternating_sum(n, 2008) % 19 == (6 ** (2 * n + 1) + 4 ** (2 * n + 1)) * pow(10, -1, 19) % 19
    assert residue(1, 2008, 19) == (3 - 2008) % 19


def test_handshake_average_by_enumeration():
    for m in range(1, 6):
        for n in range(1, 6):
            rows = set(itertools.permutations("B" * m + "G" * n))
            total = sum(sum(1 for u, v in zip(r, r[1:]) if u == v) for r in rows)
            assert Fraction(total, len(rows)) == handshake_average(m, n)


def test_square_root_functional_values():
    for f1 in range(1, 4):
        for fb in range(1, 5):
            values = {0: Fraction(fb)}
            for j in range(1, 4):
                values[j] = values[j - 1] ** 2 / f1
                assert values[j] == iterated_value(f1, fb, j)
    # f(x) = c·x^k satisfies the equation everywhere
    for c, k in ((2, 1), (3, 2), (1, -1)):
        for x, y in ((1.5, 2.0), (0.3, 7.0)):
            assert math.isclose((c * (x * y) ** k) ** 2, c * (x * x) ** k * c * (y * y) ** k)


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
