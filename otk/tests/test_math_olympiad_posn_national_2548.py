"""Independent checks for the sets adapted from the 2548 national paper."""

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
from otk.sets.math.olympiad.acquaintance_line_orders import order_tex
from otk.sets.math.olympiad.alternating_subset_sum import alternating_total
from otk.sets.math.olympiad.arbelos_tangent_circle import lengths
from otk.sets.math.olympiad.binomial_difference_gcd import difference_gcd
from otk.sets.math.olympiad.collapsing_operation_chain import chain_value as collapse_value
from otk.sets.math.olympiad.composition_count import composition_tex
from otk.sets.math.olympiad.cosine_difference_minimum import minimum
from otk.sets.math.olympiad.cyclic_ratio_square_sum import square_sum
from otk.sets.math.olympiad.dice_sum_count import roll_count
from otk.sets.math.olympiad.double_iterate_values import chain_value as iterate_value
from otk.sets.math.olympiad.golden_isosceles_power import golden_power_tex
from otk.sets.math.olympiad.inscribed_trapezoid_leg import leg_tex
from otk.sets.math.olympiad.linear_substitution_functional import rhs, solved_value
from otk.sets.math.olympiad.monic_interpolation_value import endpoint_sum
from otk.sets.math.olympiad.odd_power_root_mod_two_power import least_root_tex
from otk.sets.math.olympiad.odd_power_sum_mod_two_power import power_sum_residue
from otk.sets.math.olympiad.odd_step_sum_terms import CASES as STEP_CASES
from otk.sets.math.olympiad.odd_step_sum_terms import odd_starts
from otk.sets.math.olympiad.orthocenter_altitude_ratio import foot_ratio
from otk.sets.math.olympiad.orthocenter_circle_power import foot_distances
from otk.sets.math.olympiad.power_tower_divisible_count import divisible_count
from otk.sets.math.olympiad.quadratic_cauchy_functional import value_at
from otk.sets.math.olympiad.quartic_difference_pairs import good_pairs
from otk.sets.math.olympiad.right_incenter_product import TRIPLES, product_coefficient
from otk.sets.math.olympiad.squared_sum_solution_count import solution_count
from otk.sets.math.olympiad.symmetric_power_root_sum import root_sum
from otk.sets.math.olympiad.tangent_power_pair_sum import pair_sum
from otk.sets.math.olympiad.weighted_amgm_maximiser import WEIGHTS, maximiser

KEYS = tuple(
    f"math.{k}_olympiad"
    for k in (
        "inscribed_trapezoid_leg orthocenter_altitude_ratio golden_isosceles_power right_incenter_product "
        "dice_sum_count squared_sum_solution_count composition_count alternating_subset_sum binomial_difference_gcd "
        "odd_power_sum_mod_two_power odd_power_root_mod_two_power power_tower_divisible_count odd_step_sum_terms "
        "quadratic_cauchy_functional linear_substitution_functional symmetric_power_root_sum "
        "collapsing_operation_chain tangent_power_pair_sum monic_interpolation_value weighted_amgm_maximiser "
        "cosine_difference_minimum orthocenter_circle_power quartic_difference_pairs double_iterate_values "
        "arbelos_tangent_circle acquaintance_line_orders cyclic_ratio_square_sum"
    ).split()
)


def tex_value(tex: str) -> float:
    """Evaluate the small TeX forms these sets print (√, fractions, ·)."""
    expr = tex.replace(r"\cdot", "*")
    expr = re.sub(r"\\sqrt\{(\d+)\}", r"*(\1**0.5)", expr)
    expr = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", expr)
    expr = re.sub(r"\^\{(\d+)\}", r"**\1", expr)
    expr = re.sub(r"(^|[(+\-])\*", r"\1", expr)
    return eval(expr)  # noqa: S307 - test-only, on strings the sets produced


def test_trapezoid_leg_by_bisection():
    for k in range(1, 10):
        lo, hi = 0.0, 1.0  # c, the half-length of DC
        for _ in range(200):
            c = (lo + hi) / 2
            if 2 * c - k * math.sqrt(2 - 2 * c) > 0:
                hi = c
            else:
                lo = c
        assert math.isclose(tex_value(leg_tex(k)), math.sqrt(2 - 2 * lo), rel_tol=1e-9)
    assert leg_tex(4) == r"\sqrt{6}-2"  # the source


def test_orthocenter_ratio_by_coordinates():
    rng = random.Random(1)
    for _ in range(200):
        q = rng.randint(1, 9)
        t = Fraction(rng.randint(1, 2 * q - 1), q)
        angle_b = math.acos(float(t) / 2)
        angle_a = rng.uniform(max(0.05, math.pi / 2 - angle_b) + 0.01, math.pi / 2 - 0.01)
        angle_c = math.pi - angle_a - angle_b
        if not 0 < angle_c < math.pi / 2:
            continue
        b, c = np.array([0.0, 0.0]), np.array([math.sin(angle_a), 0.0])  # 2R = 1
        a = math.sin(angle_c) * np.array([math.cos(angle_b), math.sin(angle_b)])
        h = np.array([a[0], a[0] * (c[0] - a[0]) / a[1]])  # orthocentre: x = a_x, on altitude from B
        assert math.isclose(np.linalg.norm(h - b) / 0.5, float(t), rel_tol=1e-9)
        assert math.isclose(a[0] / np.linalg.norm(a), float(foot_ratio(t)), rel_tol=1e-9)
    assert foot_ratio(Fraction(1)) == Fraction(1, 2)  # the source


def test_golden_powers():
    phi = math.sin(math.radians(72)) / math.sin(math.radians(36))  # AB/BC by the sine rule
    for n in range(1, 10):
        assert math.isclose(tex_value(golden_power_tex(n)), phi**n, rel_tol=1e-12)


def test_incenter_product_by_coordinates():
    for b, c, a in TRIPLES:
        for scale in (1, 3):
            bb, cc, aa = b * scale, c * scale, a * scale
            pa, pb, pc = np.array([0.0, 0.0]), np.array([float(bb), 0.0]), np.array([0.0, float(cc)])
            incentre = (aa * pa + cc * pb + bb * pc) / (aa + bb + cc)
            product = np.linalg.norm(incentre - pb) * np.linalg.norm(incentre - pc)
            assert math.isclose(product, product_coefficient(bb, cc, aa) * math.sqrt(2), rel_tol=1e-9)
    assert product_coefficient(3, 4, 5) == 5  # the source: 5√2


def test_dice_by_enumeration():
    for dice in range(1, 6):
        totals = {}
        for roll in itertools.product(range(1, 7), repeat=dice):
            totals[sum(roll)] = totals.get(sum(roll), 0) + 1
        for s in range(dice, 6 * dice + 1):
            assert roll_count(dice, s) == totals[s]
    assert roll_count(6, 21) == 4332  # the source


def test_squared_sum_by_direct_count():
    for total in list(range(200, 420)) + [2548]:
        count = 0
        for x in itertools.product(range(1, math.isqrt(total)), repeat=3):
            s = sum(x)
            if total % (s * s) == 0:
                count += max(total // (s * s) - 1, 0)
        assert solution_count(total) == count
    assert solution_count(2548) == 1701  # the source


def test_compositions_by_bars():
    for n in range(2, 12):
        all_parts = [sum(1 for i in range(n - 1) if mask >> i & 1) + 1 for mask in range(1 << (n - 1))]
        assert tex_value(composition_tex(n, None)) == sum(1 for p in all_parts if p >= 2)
        for k in range(3, 6):
            assert comb(n - 1, k - 1) == sum(1 for p in all_parts if p == k)
            assert composition_tex(n, k) == rf"\binom{{{n - 1}}}{{{k - 1}}}"


def test_alternating_sums_by_enumeration():
    for n in range(1, 11):
        total = 0
        for r in range(1, n + 1):
            for subset in itertools.combinations(range(n, 0, -1), r):
                total += sum(v if i % 2 == 0 else -v for i, v in enumerate(subset))
        assert alternating_total(n) == total
    assert alternating_total(7) == 448  # the source


def test_difference_gcd_by_sympy():
    for m, e in ((45, 90), (11, 76), (7, 10), (30, 44)):
        square = (2 * m) ** 2
        assert difference_gcd(m, e) == sympy.gcd(sympy.Integer((3 * m) ** e - m**e) / square, square)
    assert difference_gcd(45, 90) == 4050  # the source


def test_power_sum_mod_two_power_directly():
    for m in range(3, 13):
        for last in range(1, 2**m):
            if last > 3 * m:
                break
            e = m * 2**m
            assert power_sum_residue(last, m) == sum(pow(k, e, 2**m) for k in range(1, last + 1)) % 2**m
    assert power_sum_residue(2005, 2005) == 1003  # the source


def test_least_root_by_search():
    for k in range(2, 13):
        for e in (1, 3, 5, 2005):
            x = next(x for x in range(1, 2**k + 1) if (pow(x, e, 2**k) + 1) % 2**k == 0)
            assert least_root_tex(k, e) == rf"2^{{{k}}}-1" and x == 2**k - 1


def test_divisible_count_by_residues():
    for last in (100, 257):
        even = sum(1 for n in range(0, last + 1, 2) if n % 5 in (2, 3))
        odd = sum(1 for n in range(1, last + 1, 2) if n % 5 in (1, 4))
        assert divisible_count(last, 0) == even
        assert divisible_count(last, 1) == odd
        assert divisible_count(last, None) == even + odd
    assert divisible_count(100, 0) == 20  # the source


def test_odd_starts_by_brute_force():
    for total, step in STEP_CASES[::40] + ((1372, 5),):
        found = sorted(
            k for k in range(1, total + 1, 2) for m in range(1, total + 1) if m * k + step * m * (m - 1) // 2 == total
        )
        assert odd_starts(total, step) == found
    assert odd_starts(1372, 5) == [181]  # the source


def test_quadratic_cauchy_by_substitution():
    for shift, c in ((2548, -2550), (555, 54), (17, -3)):
        f = lambda n, shift=shift, c=c: n * n + c * n + shift  # noqa: E731
        for m, n in itertools.product(range(1, 15), repeat=2):
            assert f(m + n) == f(m) + f(n) + 2 * m * n - shift
        for t in range(2, 9):
            assert value_at(shift, f(shift), t) == f(t)
    assert value_at(2548, -2548, 2) == -2548  # the source


def test_linear_substitution_by_sympy():
    x, y, t = sympy.symbols("x y t")
    for a, b, k in itertools.product((-3, -1, 2), (-4, 2), (2, 3, 4)):
        cx, cy, c0 = rhs(a, b, k)
        f = sympy.Lambda(t, a * t + b)
        assert sympy.expand(f(x + 2 * y) + k * f(y - 2 * x) - (cx * x + cy * y + c0)) == 0
        # uniqueness: y = 2x reads f(5x) = rhs − k f(0), and x = y = 0 gives f(0)
        f0 = sympy.Rational(c0, 1 + k)
        assert sympy.expand((cx * x + cy * 2 * x + c0 - k * f0).subs(x, t / 5) - f(t)) == 0
        assert solved_value(a, b, 100) == a * 100 + b
    assert rhs(-1, 2, 2) == (3, -4, 6) and solved_value(-1, 2, 2548) == -2546  # the source


def test_root_sum_by_coefficients():
    x = sympy.symbols("x")
    for c in (1, 2, 3, 7):
        for n in range(3, 16):
            poly = sympy.Poly(sympy.expand((c - x) ** n + x**n), x)
            coeffs = poly.all_coeffs()
            assert Fraction(int(-coeffs[1]), int(coeffs[0])) == root_sum(c, n)
    assert root_sum(2, 2005) == 2004  # the source


def test_collapsing_chain_from_the_end():
    for alpha, t in itertools.product(range(1, 5), range(2, 6)):
        beta = t * (t + alpha)
        for last in (t + 1, t + 7, 40):
            value = Fraction(last)
            for a in range(last - 1, -1, -1):
                value = (a + value + alpha) / (a * value + beta)
            assert value == collapse_value(alpha, t, last)
    assert collapse_value(1, 3, 2005) == Fraction(23, 233)  # the source


def test_tangent_pair_sum_in_log_space():
    for denominator, power in ((20, 3), (38, 2548), (2548, 2548), (802, 7)):
        total = 0.0
        for k in range(denominator // 2):
            angle = k * math.pi / denominator
            if k == 0:
                total += 1
                continue
            z = power * math.log(math.tan(angle))
            total += 1 / (1 + math.exp(z)) if z < 700 else 0.0
        assert math.isclose(total, float(pair_sum(denominator)), rel_tol=1e-9)
    assert pair_sum(2548) == Fraction(1275, 2)  # the source


def test_monic_interpolation_by_sympy():
    x, r = sympy.symbols("x r")
    for d in (2, 4, 6, 8):
        for alpha, beta in ((1, 0), (4, -7), (-2, 3)):
            p = alpha * x + beta + sympy.prod([x - k for k in range(1, d)]) * (x - r)
            assert sympy.Poly(p, x).LC() == 1
            for k in range(1, d):
                assert sympy.simplify(p.subs(x, k) - (alpha * k + beta)) == 0
            assert sympy.expand(p.subs(x, d) + p.subs(x, 0)) == endpoint_sum(d, alpha, beta)
    assert endpoint_sum(4, 1, 0) == 28  # the source


def test_weighted_maximiser_by_lagrange_and_perturbation():
    rng = random.Random(2)
    for coeffs, total in [((36, 4, 4, 3), 25)] + [(tuple(rng.randint(1, 40) for _ in range(4)), 50) for _ in range(20)]:
        point = maximiser(coeffs, total)
        assert sum(c * v for c, v in zip(coeffs, point)) == total
        value = lambda p: sum(float(w) * math.log(v) for w, v in zip(WEIGHTS, p))  # noqa: E731
        best = value(point)
        for _ in range(200):
            d = np.array([rng.uniform(-1, 1) for _ in range(4)])
            d -= np.dot(d, coeffs) / np.dot(coeffs, coeffs) * np.array(coeffs)  # stay on the plane
            trial = [float(v) + 0.01 * float(point[i]) * di for i, (v, di) in enumerate(zip(point, d))]
            if min(trial) > 0:
                trial_total = sum(c * v for c, v in zip(coeffs, trial))
                trial = [v * total / trial_total for v in trial]
                assert value(trial) <= best + 1e-12
    point = maximiser((36, 4, 4, 3), 25)
    assert point == (Fraction(1, 3), Fraction(3, 2), Fraction(1), Fraction(1))  # the source
    assert math.isclose(1 / 3 * math.sqrt(1.5), math.sqrt(6) / 6)


def test_cosine_minimum():
    rng = random.Random(3)
    for n in range(3, 13):
        spaced = [2 * math.pi * k / n for k in range(n)]
        s = lambda th: sum(math.cos(a - b) for a, b in itertools.combinations(th, 2))  # noqa: E731
        assert math.isclose(s(spaced), float(minimum(n, 1)), abs_tol=1e-9)
        assert all(s([rng.uniform(0, 7) for _ in range(n)]) >= float(minimum(n, 1)) - 1e-9 for _ in range(200))
    assert minimum(3, 1) == Fraction(-3, 2)  # the source


def test_orthocenter_power_by_coordinates():
    for bh, hc, ah in ((3, 4, 5), (1, 9, 4), (2, 2, 3), (5, 7, 12)):
        b, c, a = np.array([-bh, 0.0]), np.array([hc, 0.0]), np.array([0.0, ah])
        centre, radius = (b + c) / 2, (bh + hc) / 2

        def second_point(p, q):
            # the other intersection of line p→q with the circle (p on it)
            d = q - p
            s = -2 * np.dot(p - centre, d) / np.dot(d, d)
            return p + s * d

        d, e = second_point(b, a), second_point(c, a)
        s, _ = np.linalg.solve(np.column_stack([d - c, -(e - b)]), b - c)
        f = c + s * (d - c)
        g_height = math.sqrt(radius**2 - centre[0] ** 2)
        fh, gh_sq = foot_distances(bh, hc, ah)
        assert abs(f[0]) < 1e-9 and math.isclose(f[1], float(fh))
        assert math.isclose(g_height**2, float(gh_sq)) and math.isclose(ah * f[1], g_height**2)


def test_good_pairs_and_the_three_element_claim():
    rng = random.Random(4)
    for _ in range(300):
        values = rng.sample(range(-200, 201), 3)
        assert good_pairs(values) >= 1
    assert all(good_pairs(list(c)) >= 1 for c in itertools.combinations(range(-6, 13), 3))
    assert good_pairs([1, 2]) == 0 and good_pairs([1, 4]) == 1


def test_double_iterate_by_construction():
    for m, t in ((1, 3), (9, 37), (5, 7), (31, 1)):
        odds = [o for o in range(1, 400, 2) if o not in (m, t)]
        partner = {m: (t, 0), t: (m, 1)}
        for o1, o2 in zip(odds[::2], odds[1::2]):
            partner[o1], partner[o2] = (o2, 0), (o1, 1)

        def f(n):
            k = (n & -n).bit_length() - 1
            other, up = partner[n >> k]
            return other << (k + up)

        assert all(f(f(n)) == 2 * n for n in range(1, 300))
        assert f(m) == t
        for j in range(1, 5):
            assert f(2**j * m) == iterate_value(m, t, (j, 0))
            assert f(2**j * t) == iterate_value(m, t, (j, 1))



def test_source_example_for_double_iterate():
    def f(n):
        k = (n & -n).bit_length() - 1
        odd = n >> k
        return (odd + 2) << k if odd % 4 == 1 else (odd - 2) << (k + 1)

    assert all(f(f(n)) == 2 * n for n in range(1, 5000))

def test_arbelos_tangencies():
    for ab in (4, 12, 37):
        v = {k: float(x) for k, x in lengths(ab).items()}
        r = ab / 2
        o1, o2, o3 = np.zeros(2), np.array([0.0, r / 2]), np.array([v["O1O3"], 0.0])
        p = np.array([v["O1O3"], r / 2])
        assert math.isclose(np.linalg.norm(o3 - o1) + v["r3"], r)  # inside the big semicircle
        assert math.isclose(np.linalg.norm(o3 - o2), r / 2 + v["r3"])  # touches circle O₂
        assert math.isclose(np.linalg.norm(p - o1) + v["r"], r)
        assert math.isclose(np.linalg.norm(p - o2), r / 2 + v["r"])
        assert math.isclose(np.linalg.norm(p - o3), v["r3"] + v["r"])
        assert math.isclose(np.linalg.norm(p - o1), v["O1P"])


def test_acquaintance_orders_by_permutations():
    for n in range(2, 9):
        for circle in (False, True):
            def knows(a, b, n=n, circle=circle):
                return abs(a - b) == 1 or (circle and n > 2 and abs(a - b) == n - 1)

            count = sum(
                all(any(knows(p[i], p[j]) for j in range(i)) for i in range(1, n))
                for p in itertools.permutations(range(n))
            )
            if circle and n < 3:
                continue
            assert tex_value(order_tex(n, circle)) == count
    assert order_tex(50, False) == "2^{49}"  # the source


def test_cyclic_square_sum_identity():
    a, b, c = sympy.symbols("a b c")
    lhs = sum(((2 * x - y) / (x - y)) ** 2 for x, y in ((a, b), (b, c), (c, a)))
    s = a / (a - b) + b / (b - c) + c / (c - a)
    assert sympy.simplify(lhs - s**2 - 5) == 0
    for triple in itertools.permutations(range(-4, 5), 3):
        value = sum(Fraction(2 * x - y, x - y) ** 2 for x, y in zip(triple, triple[1:] + triple[:1]))
        assert value == square_sum(*triple) >= 5


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()

