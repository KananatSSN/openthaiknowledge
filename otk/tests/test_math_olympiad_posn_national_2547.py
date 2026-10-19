"""Independent checks for the sets adapted from the 2547 national paper."""

import itertools
import math
import random
import re
from fractions import Fraction
from math import comb, factorial, gcd
from random import Random

import numpy as np
import pytest
import sympy

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.absolute_sum_equality_set import solution_tex
from otk.sets.math.olympiad.alternating_recurrence_value import term
from otk.sets.math.olympiad.brahmagupta_max_area import max_area_square
from otk.sets.math.olympiad.cauchy_weighted_maximiser import CASES as CAUCHY_CASES
from otk.sets.math.olympiad.cauchy_weighted_maximiser import maximiser
from otk.sets.math.olympiad.circumradius_inradius_side import CASES as RADIUS_CASES
from otk.sets.math.olympiad.circumradius_inradius_side import radius_ratio
from otk.sets.math.olympiad.complex_cube_modulus import CASES as CUBE_CASES
from otk.sets.math.olympiad.complex_cube_modulus import fourth_power_sum
from otk.sets.math.olympiad.composed_linear_functional import value_at as composed_value
from otk.sets.math.olympiad.constrained_product_max import best_product
from otk.sets.math.olympiad.cos_eighth_power_difference import value_square
from otk.sets.math.olympiad.crossing_ropes_height import crossing_height
from otk.sets.math.olympiad.cubed_roots_polynomial import cubed_coefficients
from otk.sets.math.olympiad.cyclotomic_power_remainder import remainder_tex
from otk.sets.math.olympiad.divisor_count_prime_square import qualifying
from otk.sets.math.olympiad.incenter_sum_angle import angle_b
from otk.sets.math.olympiad.inversion_count_orders import orders_with_swaps
from otk.sets.math.olympiad.lifted_order_largest import PRIMES as LIFT_PRIMES
from otk.sets.math.olympiad.lifted_order_largest import largest
from otk.sets.math.olympiad.nested_root_equation import root_tex
from otk.sets.math.olympiad.nonincreasing_function_count import map_count
from otk.sets.math.olympiad.power_difference_gcd import power_gcd
from otk.sets.math.olympiad.power_sum_mod_prime_power import power_sum
from otk.sets.math.olympiad.power_tower_last_digits import last_three
from otk.sets.math.olympiad.product_sum_solution_count import solution_count
from otk.sets.math.olympiad.reciprocal_constraint_cube_min import cube_minimum
from otk.sets.math.olympiad.residue_triple_count import triple_count
from otk.sets.math.olympiad.shifted_additive_rational import value_at as shifted_value
from otk.sets.math.olympiad.squared_binomial_sum import factorial_sum
from otk.sets.math.olympiad.twin_prime_factorial_residue import PAIRS, residue

KEYS = tuple(
    f"math.{k}_olympiad"
    for k in (
        "cos_eighth_power_difference complex_cube_modulus cubed_roots_polynomial nested_root_equation "
        "absolute_sum_equality_set cyclotomic_power_remainder alternating_recurrence_value "
        "composed_linear_functional squared_binomial_sum residue_triple_count product_sum_solution_count "
        "nonincreasing_function_count twin_prime_factorial_residue power_difference_gcd lifted_order_largest "
        "power_tower_last_digits power_sum_mod_prime_power constrained_product_max cauchy_weighted_maximiser "
        "crossing_ropes_height circumradius_inradius_side incenter_sum_angle shifted_additive_rational "
        "inversion_count_orders brahmagupta_max_area divisor_count_prime_square reciprocal_constraint_cube_min"
    ).split()
)


def tex_value(tex: str) -> float:
    """Evaluate the small surd forms these sets print."""
    expr = re.sub(r"\\sqrt\{(\d+)\}", r"*(\1**0.5)", tex)
    expr = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", expr)
    expr = re.sub(r"(^|[(+\-])\*", r"\1", expr)
    return eval(expr)  # noqa: S307 - test-only, on strings the sets produced


def test_cos_eighth_by_angles():
    for q in range(2, 10):
        for p in range(-q + 1, q):
            c = Fraction(p, q)
            a = math.acos(float(c)) / 4  # in [0, π/4]
            for angle in (a, -a):
                value = math.cos(angle) ** 8 - math.sin(angle) ** 8
                assert math.isclose(value**2, float(value_square(c)), rel_tol=1e-9)
    assert value_square(Fraction(1, 3)) == Fraction(25 * 6, 324)  # the source: (5√6/18)²


def test_complex_cube_by_solving():
    for p, r, d, _, m in CUBE_CASES[::25] + ((3, 3, 2, "", 3),):
        q = r * math.sqrt(d)
        z = complex(p, q) ** (1 / 3)  # principal root, in the first quadrant
        a, b = math.sqrt(z.real), math.sqrt(z.imag)
        assert math.isclose(a**6 - 3 * a * a * b**4, p, abs_tol=1e-6)
        assert math.isclose(3 * a**4 * b * b - b**6, q, abs_tol=1e-6)
        assert math.isclose(a**4 + b**4, fourth_power_sum(p, r, d), rel_tol=1e-9) and m == fourth_power_sum(p, r, d)


def test_source_system_has_no_real_solution():
    # x = a², y = b² ≥ 0: y(3x² − y²) = −3√2 forces y² > 3x², and then
    # x(x² − 3y²) < 0 cannot equal 3; a fine grid finds nothing close
    best = min(
        abs(x**3 - 3 * x * y * y - 3) + abs(y**3 - 3 * x * x * y - 3 * math.sqrt(2))
        for x in np.linspace(0, 3, 301)
        for y in np.linspace(0, 3, 301)
    )
    assert best > 0.5


def test_cubed_roots_by_numeric_roots():
    for e1, e2, e3 in itertools.product(range(1, 6), range(-3, 6), range(1, 4)):
        roots = np.roots([1, -e1, e2, -e3])
        a, b, c = cubed_coefficients(e1, e2, e3)
        assert np.allclose(np.poly(roots**3).real, [1, -a, b, -c], atol=1e-6 * max(1, abs(a), abs(b), abs(c)))
    assert cubed_coefficients(5, 4, 3) == (74, -89, 27)  # the source: x³ − 74x² − 89x − 27


def test_nested_root_solution():
    for k in (1, 2, 3, 4, 5, 6, 7, 9, 10, 11):
        x = tex_value(root_tex(k))
        assert math.isclose(x, math.sqrt(x - k / x) + math.sqrt(k - k / x), rel_tol=1e-12)
        other = tex_value(root_tex(k, sign=-1))
        assert other < 0 and (other - k / other < 0 or k - k / other < 0 or not math.isclose(other, math.sqrt(max(other - k / other, 0)) + math.sqrt(max(k - k / other, 0))))
    assert root_tex(1) == r"\frac{1+\sqrt{5}}{2}"  # the source


def test_absolute_sum_set_by_sampling():
    for n in (1, 2, 5, 10):
        m = 2 * n
        for x in np.linspace(-5, m + 5, 401):
            lhs = sum(math.sqrt(x * x - 2 * k * x + k * k) for k in range(1, m + 1))
            holds = math.isclose(lhs, abs(2 * n * x - n - 2 * n * n), abs_tol=1e-9)
            assert holds == (x <= 1 + 1e-12 or x >= m - 1e-12)
        assert solution_tex(m) == rf"(-\infty,1]\cup[{m},\infty)"


def test_cyclotomic_remainder_by_sympy():
    x = sympy.symbols("x")
    for n in range(3, 11):
        f = sum(x**j for j in range(n))
        for m in range(1, 31):
            rem = sympy.rem(sympy.expand(f.subs(x, x**m)), f, x)
            tex = remainder_tex(n, m)
            if tex in ("0",) or tex.isdigit():
                assert rem == int(tex)
            else:
                g = gcd(m, n)
                assert sympy.expand(rem - g * sum(x ** (j * g) for j in range(n // g))) == 0
    assert remainder_tex(7, 7) == "7"  # the source


def test_recurrence_by_rsolve():
    n = sympy.symbols("n", integer=True)
    f = sympy.Function("f")
    for f0, f1 in ((0, 1), (-3, 4), (5, -2)):
        closed = sympy.rsolve(f(n) - 2 * f(n - 1) + f(n - 2) - (-1) ** n * (2 * n - 4), f(n), {f(0): f0, f(1): f1})
        for k in (0, 1, 2, 7, 42, 101):
            assert closed.subs(n, k) == term(k, f0, f1)
    assert all(term(k, 0, 1) == (k if k % 2 == 0 else 1) for k in range(60))  # the source


def test_composed_functional_identity():
    x, y = sympy.symbols("x y")
    for alpha in range(2, 6):
        for gamma in (2547, 100, 7):
            f = lambda t, alpha=alpha, gamma=gamma: alpha * t + sympy.Rational(gamma, alpha + 1)  # noqa: E731
            assert sympy.expand(f(x + f(y)) - (alpha * x + alpha**2 * y + gamma)) == 0
            assert composed_value(alpha, gamma, 0) == Fraction(gamma, alpha + 1)
    assert composed_value(2, 2547, 0) == 849  # the source


def test_squared_binomial_sum_directly():
    for n in range(1, 15):
        total = sum(Fraction(factorial(2 * n), factorial(k) ** 2 * factorial(n - k) ** 2) for k in range(n + 1))
        assert total == factorial_sum(n)


def test_residue_triples_by_enumeration():
    for n in range(1, 9):
        for r in range(3):
            count = sum(1 for t in itertools.combinations(range(1, 3 * n + 1), 3) if sum(t) % 3 == r)
            assert triple_count(n, r) == count
        assert triple_count(n, 0) == 3 * comb(n, 3) + n**3  # the source's formula


def test_product_sums_by_enumeration():
    def compositions(total, parts):
        return comb(total - 1, parts - 1) if total >= parts else 0

    for p, q in ((2, 2), (3, 4), (2, 5)):
        for total in range(1, 60):
            count = 0
            for xs in itertools.product(range(1, total + 1), repeat=p):
                s = sum(xs)
                if s <= total and total % s == 0:
                    count += compositions(total // s, q)
                if p == 3 and s > total:
                    continue
            assert solution_count(p, q, total) == count
    assert solution_count(3, 4, 91) == 4620  # the source


def test_nonincreasing_maps_by_enumeration():
    for m in range(1, 6):
        for n in range(1, 6):
            count = sum(1 for f in itertools.product(range(n), repeat=m) if all(a >= b for a, b in zip(f, f[1:])))
            assert map_count(m, n) == count


def test_twin_prime_residues_by_theorems():
    for p, q in PAIRS:
        value = residue(p, q)
        assert value % p == 1
        assert value * 2 % q == 3
    assert residue(29, 31) == 668  # the source


def test_power_gcd_directly():
    for a in (2, 3, 5):
        for m, n in ((12, 18), (35, 21), (40, 64)):
            assert power_gcd(a, m, n) == gcd(a**m - 1, a**n - 1)
    assert power_gcd(5, 2547, 2004) == 124 == gcd(5**2547 - 1, 5**2004 - 1)  # the source


def test_lifted_order_by_search():
    for q in LIFT_PRIMES:
        for bound in (500, 1234):
            want = max(n for n in range(1, bound + 1) if (pow(3, 3 * n + 3, q * q) - 27) % (q * q) == 0)
            assert largest(q, bound) == want
    assert largest(13, 2004) == 2002  # the source


def test_last_digits_by_crt():
    for base in (2, 3, 7):
        for k in (10, 57, 2004):
            exponent_mod_100 = pow(base, k, 100)
            mod_125 = pow(base, exponent_mod_100 + 100, 125)
            mod_8 = 0 if base % 2 == 0 else pow(base, pow(base, k, 2) + 2, 8)
            want = next(v for v in range(mod_125, 1000, 125) if v % 8 == mod_8)
            assert last_three(base, k) == want
    assert last_three(2, 2004) == 536  # the source


def test_power_sums_directly():
    rng = random.Random(1)
    for modulus in (25, 27, 49, 16):
        for _ in range(5):
            e, last = rng.randint(100, 3000), rng.randint(100, 1500)
            assert power_sum(last, e, modulus) == sum(pow(k, e, modulus) for k in range(1, last + 1)) % modulus
    assert power_sum(2547, 2547, 25) == 4  # the source


def test_constrained_product_by_search():
    rng = random.Random(2)
    for total in (12, 20, 33):
        best = 0.0
        for _ in range(20000):
            a = rng.uniform(0.01, 5)
            share = rng.uniform(0.01, 0.99)
            b = share * total / (a * a + 2)
            c = (1 - share) * total / (a + 2)
            best = max(best, a * b * c)
        assert best <= float(best_product(total)) + 1e-9
        assert best >= 0.99 * float(best_product(total))
        a, b, c = 1, Fraction(total, 6), Fraction(total, 6)
        assert b * (a * a + 2) + c * (a + 2) == total and a * b * c == best_product(total)
    assert best_product(12) == 4  # the source


def test_cauchy_maximiser_by_perturbation():
    rng = random.Random(3)
    for weights, coeffs, t, k in CAUCHY_CASES[::7] + (((9, 4, 1), (1, 2, 3), 3, 91),):
        point = maximiser(weights, coeffs, t)
        assert sum(w * v * v for w, v in zip(weights, point)) == k
        best = sum(c * float(v) for c, v in zip(coeffs, point))
        for _ in range(500):
            trial = [float(v) * rng.uniform(0.8, 1.2) for v in point]
            scale = math.sqrt(k / sum(w * v * v for w, v in zip(weights, trial)))
            assert sum(c * v * scale for c, v in zip(coeffs, trial)) <= best + 1e-9
    assert maximiser((9, 4, 1), (1, 2, 3), 3) == (Fraction(1, 3), Fraction(3, 2), Fraction(9))  # the source


def test_crossing_height_by_lines():
    for a, b in ((3, 6), (5, 5), (2, 29)):
        for distance in (1.0, 7.5):
            # rope 1 from (0, a) to (distance, 0); rope 2 from (distance, b) to (0, 0)
            x = a * distance / (a + b)
            assert math.isclose(b * x / distance, float(crossing_height(a, b)))


def test_radius_ratio_by_coordinates():
    for a, b, c, ratio in RADIUS_CASES[::30] + ((3, 7, 8, Fraction(7, 2)),):
        x = (a * a + c * c - b * b) / (2 * a)
        y = math.sqrt(c * c - x * x)
        area = a * y / 2
        r_big, r_small = a * b * c / (4 * area), area / ((a + b + c) / 2)
        assert math.isclose(r_big / r_small, float(ratio))
        assert radius_ratio(a, b, c) == ratio
    assert [z for z in range(5, 10) if radius_ratio(3, 7, z) == Fraction(7, 2)] == [8]  # the source


def test_incenter_angle_numerically():
    def gap(angle_a, angle_b_deg):
        a_, b_ = math.radians(angle_a), math.radians(angle_b_deg)
        c_ = math.pi - a_ - b_
        a, b, c = math.sin(a_), math.sin(b_), math.sin(c_)
        s = (a + b + c) / 2
        r = math.sqrt((s - a) * (s - b) * (s - c) / s)
        return b + r / math.sin(a_ / 2) - a  # CA + AI − BC

    for angle_a in range(30, 120, 4):
        b = float(angle_b(angle_a))
        assert abs(gap(angle_a, b)) < 1e-12
        assert gap(angle_a, b - 1) < 0 < gap(angle_a, b + 1)
    assert angle_b(70) == 35  # the source


def test_shifted_additive_values():
    for c, a, b in ((2547, 2004, 2547), (10, 3, 4)):
        k = Fraction(b + c, a)
        f = lambda t, k=k, c=c: k * t - c  # noqa: E731
        for x_, y_ in ((Fraction(1, 2), Fraction(3, 7)), (Fraction(-5), Fraction(11, 3))):
            assert f(x_ + y_) == f(x_) + f(y_) + c
        assert f(a) == b
        assert shifted_value(c, a, b, 17) == f(17)
    assert shifted_value(2547, 2004, 2547, 2547) == Fraction(1311705, 334)  # the source


def test_inversions_by_bubble_sort():
    for n in range(2, 8):
        tally = {}
        for perm in itertools.permutations(range(n)):
            line, swaps = list(perm), 0
            changed = True
            while changed:
                changed = False
                for i in range(n - 1):
                    if line[i] > line[i + 1]:
                        line[i], line[i + 1] = line[i + 1], line[i]
                        swaps += 1
                        changed = True
            tally[swaps] = tally.get(swaps, 0) + 1
        for swaps, count in tally.items():
            assert orders_with_swaps(n, swaps) == count
    assert orders_with_swaps(18, 150) == orders_with_swaps(18, 3) == 951  # the source


def test_quadrilateral_area_by_search():
    for sides in ((3, 4, 5, 6), (2, 7, 7, 4), (5, 5, 6, 8)):
        a, b, c, d = sides
        best = 0.0
        for angle in np.linspace(0.001, math.pi - 0.001, 20001):
            diag2 = a * a + b * b - 2 * a * b * math.cos(angle)  # AC², angle at B
            e = math.sqrt(diag2)
            if not (abs(c - d) < e < c + d):
                continue
            s = (c + d + e) / 2
            other = math.sqrt(max(s * (s - c) * (s - d) * (s - e), 0))
            best = max(best, a * b * math.sin(angle) / 2 + other)
        assert math.isclose(best**2, float(max_area_square(*sides)), rel_tol=1e-6)
        assert best <= sum(x * x for x in sides) / 4  # the source's bound


def test_divisor_counts_by_sympy():
    for k in (2543, 24 * 50 + 23, 24 * 123 + 23):
        for limit in (12, 16):
            want = [p for p in sympy.primerange(2, 200) if sympy.divisor_count(p * p + k) < limit]
            assert qualifying(k, limit) == want
    assert qualifying(2543, 16) == [2]  # the source (searched to 200 here; 20,000 in the note)


def test_cube_minimum_by_sampling():
    rng = random.Random(4)
    for n in range(2, 7):
        for q in (1, 2, 3):
            assert math.isclose(n * q**3, cube_minimum(n, q))
            for _ in range(300):
                a = [rng.uniform(0.1, 5) for _ in range(n)]
                need = q * q * sum(1 / v for v in a)
                scale = max(1.0, math.sqrt(need / sum(a)))  # scaling up keeps the constraint
                a = [v * scale for v in a]
                assert sum(a) >= q * q * sum(1 / v for v in a) - 1e-9
                assert sum(v**3 for v in a) >= cube_minimum(n, q) - 1e-6
    assert cube_minimum(3, 1) == 3  # the source: both sides are at least 3


@pytest.mark.parametrize("key", KEYS)
def test_generated_draws(key):
    for seed in range(80):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()


def test_printed_2547_q2_system_has_no_real_solution():
    """Day one ข้อ 2 as printed: a⁶ − 3a²b⁴ = 3, b⁶ − 3a⁴b² = 3√2.

    With x = a², y = b², (x + iy)³ = (x³ − 3xy²) − i(y³ − 3x²y) = 3 − 3√2 i, so
    x + iy is a cube root of 3 − 3√2 i. A real a, b needs x, y ≥ 0; no cube
    root has both, which is why the sheet's q02 verifies the corrected sign.
    """
    w = sympy.symbols("w")
    roots = sympy.Poly(w**3 - (3 - 3 * sympy.sqrt(2) * sympy.I), w).nroots(n=30)
    assert len(roots) == 3
    for root in roots:
        x, y = sympy.re(root), sympy.im(root)
        assert abs(x**3 - 3 * x * y**2 - 3) < 1e-20          # each root is a real
        assert abs(y**3 - 3 * x**2 * y - 3 * sympy.sqrt(2)) < 1e-20  # pair (x, y)
        assert x < 0 or y < 0
