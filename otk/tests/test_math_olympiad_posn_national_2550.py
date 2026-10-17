"""Independent checks for the sets adapted from the 2550 national paper."""

import itertools
import math
import random
import re
from fractions import Fraction
from math import comb
from random import Random

import numpy as np
import pytest
import sympy

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.angle_chain_circle_radius import second_radius
from otk.sets.math.olympiad.arc_midpoint_chord import CASES as ARC_CASES
from otk.sets.math.olympiad.arc_midpoint_chord import chord_square
from otk.sets.math.olympiad.cevian_segment_ratio import segment_ratio
from otk.sets.math.olympiad.chord_arc_projection import chord_length
from otk.sets.math.olympiad.complex_power_sums import fourth_power_sum
from otk.sets.math.olympiad.constant_functional_value import forced_value
from otk.sets.math.olympiad.disjoint_subset_pairs import disjoint_pairs
from otk.sets.math.olympiad.fermat_quotient_square import BASES, square_quotient_primes
from otk.sets.math.olympiad.garland_average import average_garlands
from otk.sets.math.olympiad.incircle_vertex_ratio import semiperimeter_ratio
from otk.sets.math.olympiad.prime_power_tower_residue import MODULI, tower_sum
from otk.sets.math.olympiad.quadratic_square_values_product import CASES as QUAD_CASES
from otk.sets.math.olympiad.quadratic_square_values_product import square_solutions
from otk.sets.math.olympiad.radical_axis_point import radical_point
from otk.sets.math.olympiad.relay_team_count import team_counts
from otk.sets.math.olympiad.residue_sum_function_count import residue_counts
from otk.sets.math.olympiad.right_triangle_cube_root import cube_root_side
from otk.sets.math.olympiad.root_shift_reciprocal_sum import shifted_sum
from otk.sets.math.olympiad.smallest_with_divisor_count import COUNTS, least_with_divisors
from otk.sets.math.olympiad.sock_shoe_orders import dressing_orders
from otk.sets.math.olympiad.swapped_argument_functional import linear_value, rhs_tex
from otk.sets.math.olympiad.tangent_maximal_angle import ratio_square
from otk.sets.math.olympiad.unit_root_power_index import COEFFICIENTS, smallest_index
from otk.sets.math.olympiad.vandermonde_shifted_sum import binomial_sum
from otk.sets.math.olympiad.wilson_mixed_powers import PRIMES as WILSON_PRIMES
from otk.sets.math.olympiad.wilson_mixed_powers import terms

KEYS = tuple(
    f"math.{k}_olympiad"
    for k in (
        "chord_arc_projection arc_midpoint_chord angle_chain_circle_radius cevian_segment_ratio "
        "right_triangle_cube_root tangent_maximal_angle complex_power_sums root_shift_reciprocal_sum "
        "swapped_argument_functional unit_root_power_index residue_sum_function_count sock_shoe_orders "
        "disjoint_subset_pairs vandermonde_shifted_sum wilson_mixed_powers smallest_with_divisor_count "
        "quadratic_square_values_product prime_power_tower_residue constant_functional_value "
        "garland_average radical_axis_point fermat_quotient_square relay_team_count incircle_vertex_ratio"
    ).split()
)


def test_chord_arc_by_coordinates():
    for radius in (1.0, 2.5, 7.0):
        a = (radius, 0.0)
        c = (radius * math.cos(math.radians(120)), radius * math.sin(math.radians(120)))
        ac, od = math.dist(a, c), c[1]
        assert a[0] > 0 > c[0]  # the chord crosses OB (the y-axis)
        assert math.isclose(chord_length(ac - od), ac)
    assert chord_length(2) == 4  # the source


def test_arc_midpoint_chord_on_a_circle():
    rng = random.Random(1)
    for _ in range(200):
        tb, half, td = rng.uniform(0, 6.28), rng.uniform(0.2, 1.4), rng.uniform(0, 6.28)
        pt = lambda t: (math.cos(t), math.sin(t))  # noqa: E731
        a, b, c, d = pt(tb - half), pt(tb), pt(tb + half), pt(td)
        # D on the arc AC away from B
        if math.cos(td - tb) > math.cos(half):
            continue
        ad, bd, cd, ab = math.dist(a, d), math.dist(b, d), math.dist(c, d), math.dist(a, b)
        assert math.isclose(ab * ab, bd * bd - ad * cd, abs_tol=1e-9)
    assert chord_square(6, 4, 1) == 10  # the source
    for ad, bd, cd in ARC_CASES:
        assert chord_square(ad, bd, cd) > 0
        assert ad + cd < 2 * bd  # cos∠ADB < 1, so the quadrilateral exists


def test_angle_chain_by_tangency():
    for k in range(1, 13):
        ab, bc = k * math.sqrt(3), 3 * k
        angle_a = math.atan2(bc, ab)
        assert math.isclose(angle_a, math.pi / 3)
        # first circle: tangent to AB (x-axis) at B = (ab, 0), centre (ab, r1)
        r1 = ab * math.tan(angle_a / 2)
        # second circle: centre on the bisector at distance t from A, radius t·sin(A/2),
        # externally tangent to the first; solve by bisection
        u = (math.cos(angle_a / 2), math.sin(angle_a / 2))

        def gap(t):
            r2 = t * math.sin(angle_a / 2)
            return math.dist((t * u[0], t * u[1]), (ab, r1)) - (r1 + r2)

        lo, hi = 1e-9, math.hypot(ab, r1) * 0.999
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if gap(mid) > 0 else (lo, mid)
        assert math.isclose(lo * math.sin(angle_a / 2), float(second_radius(k)), rel_tol=1e-9)


def test_cevian_ratio_by_coordinates():
    rng = random.Random(2)
    for _ in range(100):
        ac, bc, k = rng.randint(5, 30), rng.randint(5, 30), rng.randint(2, 5)
        angle = rng.uniform(0.3, 2.8)
        c = np.zeros(2)
        a = np.array([ac, 0.0])
        b = bc * np.array([math.cos(angle), math.sin(angle)])
        cf = rng.uniform(0.5, min(bc, ac / k) - 0.1)
        e, f = c + (a - c) * (k * cf / ac), c + (b - c) * (cf / bc)
        m = (a + b) / 2
        # E + s(F − E) = t·M
        s, t = np.linalg.solve(np.column_stack([f - e, -m]), -e)
        g = e + s * (f - e)
        p, q = segment_ratio(ac, bc, k)
        assert math.isclose(np.linalg.norm(g - e) / np.linalg.norm(f - g), p / q, rel_tol=1e-9)
    assert segment_ratio(16, 12, 3) == (9, 4)  # the source


def test_cube_root_side_by_solving():
    x, y = sympy.symbols("x y", positive=True)
    for t in (1, 2, 5):
        # A = (0, 0), C = (x, 0), B = (0, y), D = (x − t, 0)
        sol = sympy.nsolve(
            [y**2 + (x - t) ** 2 - t**2, x**2 / sympy.sqrt(x**2 + y**2) - t],
            [x, y],
            [1.3 * t, 0.9 * t],
        )
        assert math.isclose(float(sol[0]), cube_root_side(t) * 2 ** (1 / 3), rel_tol=1e-9)


def test_tangent_maximal_angle_by_scan():
    for m, n in ((1, 1), (2, 5), (3, 1), (4, 3)):
        bm, bc = m, m + n
        alpha = math.radians(20)
        cx, cy = (bm + bc) / 2, (n / 2) / math.tan(alpha)
        rad = math.hypot(n / 2, cy)
        low = math.atan2(-cy, n / 2)  # C; the major arc runs from C over the top to M
        best = max(
            ((math.atan2(cy + rad * math.sin(th), cx + rad * math.cos(th)), th) for th in np.linspace(low, math.pi - low, 400001)),
        )
        th = best[1]
        ba = math.hypot(cx + rad * math.cos(th), cy + rad * math.sin(th))
        assert math.isclose((bc / ba) ** 2, float(ratio_square(m, n)), rel_tol=1e-4)  # the maximum is flat


def test_complex_power_sums_by_roots():
    for p1, p2, p3 in itertools.product(range(-3, 4), range(-3, 6), range(-4, 8)):
        e1 = Fraction(p1)
        e2 = (e1 * e1 - p2) / 2
        e3 = (p3 - e1 * p2 + e2 * p1) / 3
        roots = np.roots([1, -float(e1), float(e2), -float(e3)])
        for k, want in ((1, p1), (2, p2), (3, p3)):
            assert abs(sum(roots**k) - want) < 1e-6
        assert abs(sum(roots**4) - float(fourth_power_sum(p1, p2, p3))) < 1e-6
    assert fourth_power_sum(1, 2, 3) == Fraction(25, 6)  # the source


def test_shifted_sum_by_numeric_roots():
    rng = random.Random(3)
    for _ in range(30):
        n, a, b = rng.randint(3, 40), rng.randint(1, 12), rng.randint(1, 12)
        if 1 + a - b == 0:
            continue
        coeffs = [1] + [0] * (n - 2) + [a, -b]
        roots = np.roots(coeffs)
        total = sum(r / (r - 1) for r in roots)
        assert abs(total - float(shifted_sum(n, a, b))) < 1e-6
    assert shifted_sum(84, 7, 6) == Fraction(77, 2)  # the source


def test_swapped_functional_by_solving_the_system():
    x, u, f1, f2 = sympy.symbols("x u f1 f2")
    for alpha, beta, k in itertools.product(range(1, 5), range(-6, 7, 3), (2, 3, 4)):
        rhs = sympy.sympify(re.sub(r"(\d)x", r"\1*x", rhs_tex(alpha, beta, k)).replace("^", "**"))
        sol = sympy.solve([f1 + k * f2 - rhs, f2 + k * f1 - rhs.subs(x, 1 - x)], [f1, f2])
        # f1 is f(x² + x + 3); it must equal α(x² + x + 3) + β
        assert sympy.expand(sol[f1] - (alpha * (x**2 + x + 3) + beta)) == 0
        assert linear_value(alpha, beta, 85) == alpha * 85 + beta
    assert linear_value(2, -3, 85) == 167  # the source: f(t) = 2t − 3
    assert rhs_tex(2, -3, 2) == "6x^2-10x+17"


def test_unit_root_index_by_numeric_roots():
    values = {3: 1.0, 4: math.sqrt(2), 5: (1 + math.sqrt(5)) / 2, 6: math.sqrt(3)}
    for m, _ in COEFFICIENTS:
        a = values[m]
        on_circle = [
            n for n in range(1, 40) if any(abs(abs(z) - 1) < 1e-7 for z in np.roots([a, -1] + [0] * (n - 1) + [-1]))
        ]
        for above in (0, 3, 11, 20):
            assert smallest_index(m, above) == min(n for n in on_circle if n > above)
    assert smallest_index(6, 0) == 10  # the source


def test_residue_counts_by_brute_force():
    for values in ((61, 80, 84), (12, 15, 19), (13, 16, 20), (14, 17, 18)):
        for n in range(1, 7):
            counts = [0, 0, 0]
            for f in itertools.product(values, repeat=n):
                counts[sum(f) % 3] += 1
            assert residue_counts(values, n) == counts
    assert residue_counts((61, 80, 84), 9)[0] == 3**8  # the source pattern: 3^(N − 1)


def test_dressing_orders_by_enumeration():
    for feet in range(1, 5):
        actions = [(foot, kind) for foot in range(feet) for kind in (0, 1)]
        count = sum(
            all(order.index((f, 0)) < order.index((f, 1)) for f in range(feet))
            for order in itertools.permutations(actions)
        )
        assert dressing_orders(feet) == count
    assert dressing_orders(4) == 2520  # the source


def test_disjoint_pairs_by_enumeration():
    for n in range(1, 7):
        subsets = [frozenset(c) for r in range(1, n + 1) for c in itertools.combinations(range(n), r)]
        count = sum(1 for s, t in itertools.combinations(subsets, 2) if not s & t)
        assert disjoint_pairs(n) == count
    assert disjoint_pairs(8) == 3025  # the source


def test_vandermonde_by_direct_sum():
    rng = random.Random(4)
    for _ in range(40):
        a, b = rng.randint(0, 12), rng.randint(0, 12)
        n = rng.randint(a + b, 60)
        top, bottom = binomial_sum(n, a, b)
        assert sum(comb(k, a) * comb(n - k, b) for k in range(a, n - b + 1)) == comb(top, bottom)
    assert sum(comb(k, 84) * comb(8084 - k, 84) for k in range(84, 8001)) == comb(*binomial_sum(8084, 84, 84))
    assert binomial_sum(8084, 84, 84) == (8085, 169)  # the source


def test_wilson_terms_by_wilson_and_fermat():
    def by_theorems(p):
        h = (p - 1) // 2
        mod_p = [(-1) ** h % p, 1, 1, 1]  # Wilson, then Fermat (p − 1 divides each exponent; h! even)
        mod_9 = [0, 0 if h % 3 == 0 else 1, 0, 0 if (p - 1) % 3 == 0 else 1]  # 9 | (p−1)!, h!; 6 | exponents
        return sum(int(sympy.ntheory.modular.crt([p, 9], [r, s])[0]) for r, s in zip(mod_p, mod_9)) % (9 * p)

    for p in WILSON_PRIMES:
        assert sum(terms(p)) % (9 * p) == by_theorems(p)
    assert sum(terms(223)) % 2007 == 225  # the source


def test_least_with_divisors_by_scan():
    first = {}
    for n in range(1, 50001):
        first.setdefault(int(sympy.divisor_count(n)), n)
    for d in COUNTS:
        want = least_with_divisors(d)
        if want <= 50000:
            assert first[d] == want
        else:
            assert d not in first
            assert sympy.divisor_count(want) == d
    assert least_with_divisors(24) == 360  # the source


def test_square_values_by_scan():
    for b, c in QUAD_CASES[::7] + ((59, 881),):
        found = [n for n in range(-5000, 5001) if sympy.ntheory.primetest.is_square(n * n + b * n + c)]
        assert square_solutions(b, c) == found
    assert math.prod(square_solutions(59, 881)) == 760  # the source


def test_tower_sum_by_coprime_count():
    for modulus in MODULI:
        lam = sympy.reduced_totient(modulus)
        for last in (40, 517, 2550, 3000):
            primes = [sympy.prime(k) for k in range(2, last + 1)]
            special = [p for p in primes if modulus % p == 0]
            assert all((p**4 - 1) % lam == 0 for p in primes if modulus % p)
            want = (len(primes) - len(special) + sum(pow(p, p**4 - 1, modulus) for p in special)) % modulus
            assert tower_sum(last, modulus) == want
    assert tower_sum(2550, 2550) == 1273  # the source


def test_constant_functional_candidates():
    def holds(f, xs):
        left = sum(f(u + v) for u, v in zip(xs, xs[1:])) + f(sum(xs))
        return left <= sum(f(2 * u) for u in xs) + 1e-9

    rng = random.Random(5)
    for n in (4, 6, 2550):
        tests = [[a, a] + [0.0] * (n - 2) for a in (-2.0, -0.5, 0.7, 3.0)]
        tests += [[t if i % 2 == 0 else -t for i in range(n)] for t in (-1.5, 0.4, 2.0)]
        tests += [[0.0] + [3.0] + [0.0] * (n - 2), [1.0] + [0.0] * (n - 1)]
        for f in (lambda v: v, lambda v: v * v, lambda v: -v * v, abs, lambda v: -abs(v), math.sin, lambda v: v + 7):
            assert not all(holds(f, xs) for xs in tests)
        for c in (-3.0, 0.0, 11.0):
            for _ in range(20):
                assert holds(lambda v, c=c: c, [rng.uniform(-5, 5) for _ in range(n)])
    assert forced_value(10, 2550, 85) == 10


def test_garland_average_by_enumeration():
    rng = random.Random(6)
    for _ in range(15):
        n = rng.randint(3, 6)
        k = rng.randint(1, n - 1)
        couples = [rng.randint(1, n) for _ in range(rng.randint(2, 4))]
        boys, girls = [0] * n, [0] * n
        for c in couples:
            for i in rng.sample(range(n), c):
                boys[i] += 1
            for i in rng.sample(range(n), c):
                girls[i] += 1
        groups = [
            sum(boys[i] for i in bs) + sum(girls[j] for j in gs)
            for bs in itertools.combinations(range(n), k)
            for gs in itertools.combinations(range(n), n - k)
        ]
        assert Fraction(sum(groups), len(groups)) == average_garlands(couples, n, k)
        assert max(groups) >= len(couples)  # the source's claim


def test_radical_point_by_circle_intersection():
    rng = random.Random(7)
    for _ in range(200):
        ab = rng.randint(1, 12)
        ac = rng.randint(ab + 1, ab + 15)
        ad = rng.randint(ac + 1, ac + 15)
        o1, r1 = ac / 2, ac / 2
        o2, r2 = (ab + ad) / 2, (ad - ab) / 2
        # the common chord is x = x0 where the two circles meet
        x0 = (r1**2 - r2**2 + o2**2 - o1**2) / (2 * (o2 - o1))
        assert r1**2 - (x0 - o1) ** 2 > 0  # the circles do meet
        assert math.isclose(x0, float(radical_point(ab, ac, ad)))
        assert ab < x0 < ac  # P lies on BC


def test_fermat_quotients_by_sympy():
    for a in BASES:
        want = [
            p
            for p in sympy.primerange(2, 60)
            if a % p and sympy.ntheory.primetest.is_square((pow(a, p - 1) - 1) // p)
        ]
        assert square_quotient_primes(a) == want and want
    assert square_quotient_primes(2) == [3, 7]  # the source


def test_relay_teams_by_student_enumeration():
    rng = random.Random(8)
    for _ in range(12):
        rooms, seats = rng.randint(2, 4), rng.randint(2, 5)
        girls = [rng.randint(0, seats) for _ in range(rooms)]
        students = [(r, s, s <= girls[r]) for r in range(rooms) for s in range(1, seats + 1)]
        count = 0
        for four in itertools.combinations(students, 4):
            rs = sorted({x[0] for x in four})
            ss = sorted({x[1] for x in four})
            if len(rs) == 2 and len(ss) == 2 and sum(x[2] for x in four) % 2:
                count += 1
        one, three, _ = team_counts(girls, seats)
        assert one + three == count
        assert count % 2 == (rooms - 1) * (seats - 1) * sum(girls) % 2  # the source's parity
    assert (10 - 1) * (50 - 1) * 271 % 2 == 1  # the source: an odd number of teams


def test_incircle_ratio_by_coordinates():
    for a, b, c in itertools.combinations_with_replacement(range(2, 12), 3):
        if a + b <= c:
            continue
        # place the triangle and measure its area
        x = (b * b + c * c - a * a) / (2 * c)
        area = c * math.sqrt(b * b - x * x) / 2
        s = (a + b + c) / 2
        r = area / s
        assert math.isclose(s * s / (r * r), float(semiperimeter_ratio(a, b, c)), rel_tol=1e-9)
        assert semiperimeter_ratio(a, b, c) >= 27  # equality only when equilateral


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
