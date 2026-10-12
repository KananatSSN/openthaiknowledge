"""The trigonometry sets built from the sheet bank's knowledge units.

Identities and unit-circle values are checked with SymPy, inverse-trig
compositions against SymPy's exact values, solution counts by scanning the
interval numerically, triangle kinds and obtuse counts by brute force, and the
source exams' answers are pinned.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m5 import trigonometric_functions as mt
from otk.sets._support.math_bank_trig import TRIPLES, pi_tex, surd_tex
from otk.sets.math.m5.inverse_trig import (
    TAN_PAIRS,
    angle_sum_from_tans,
    complement_solution,
    compose,
    inverse_sin_cos,
)
from otk.sets.math.m5.trig_equation import (
    LAMBDAS,
    cos_or_tan_solution_count,
    sine_solution_count,
    tan_shift_count,
)
from otk.sets.math.m5.law_of_cosines import obtuse_third_sides, triangle_kind
from otk.sets.math.m5.trigonometric_ratios import (
    TAN_HYPOTENUSE,
    area_from_hypotenuse_and_tan,
    area_from_scaled_sines,
    sine_sum_from_area,
)

sympy = pytest.importorskip("sympy")
th = sympy.Symbol("theta")
KEYS = ("math.trig_radian_arc_m5", "math.trig_identity_reduce_m5", "math.inverse_trig_sum_m5",
        "math.trig_equation_count_m5", "math.triangle_side_type_m5", "math.right_triangle_relations_m5",
        "math.trig_reduction_m5", "math.trig_product_sum_m5")


def R(v):
    v = Fraction(v)
    return sympy.Rational(v.numerator, v.denominator)


def surd(cm):
    c, m = cm
    return R(c) * sympy.sqrt(m)


def test_unit_circle_table():
    for t, (cos, sin) in mt.UNIT_CIRCLE.items():
        assert sympy.simplify(sympy.cos(R(t) * sympy.pi) - surd(cos)) == 0
        assert sympy.simplify(sympy.sin(R(t) * sympy.pi) - surd(sin)) == 0


def test_tex_helpers():
    assert surd_tex(Fraction(-1, 2), 3) == r"-\frac{\sqrt{3}}{2}"
    assert surd_tex(Fraction(3, 4), 3) == r"\frac{3\sqrt{3}}{4}"
    assert mt.root_tex(Fraction(9, 16)) == r"\frac{3}{4}"
    assert mt.root_tex(Fraction(1, 8)) == r"\frac{\sqrt{2}}{4}"
    assert pi_tex(Fraction(5, 3)) == r"\frac{5\pi}{3}"
    assert pi_tex(Fraction(-1)) == r"-\pi"


FUNCS = {"sin": sympy.sin(th), "cos": sympy.cos(th), "tan": sympy.tan(th),
         "cosec": 1 / sympy.sin(th), "sec": 1 / sympy.cos(th), "cot": 1 / sympy.tan(th)}


@pytest.mark.parametrize("tex, f", mt.REDUCIBLE)
def test_reducible_expressions(tex, f):
    assert sympy.simplify(_expr(tex) - FUNCS[f]) == 0


def _expr(tex: str):
    """The REDUCIBLE entries rewritten by hand in SymPy (no LaTeX parser dependency)."""
    s, c, t = sympy.sin(th), sympy.cos(th), sympy.tan(th)
    csc, sec, cot = 1 / s, 1 / c, 1 / t
    table = {
        r"\sin\theta + \cos\theta\cot\theta": s + c * cot,
        r"\cos\theta + \sin\theta\tan\theta": c + s * t,
        r"\cot\theta\sec\theta": cot * sec,
        r"\tan\theta\operatorname{cosec}\theta": t * csc,
        r"\sin\theta\sec\theta": s * sec,
        r"\cos\theta\operatorname{cosec}\theta": c * csc,
        r"\frac{1 - \cos^{2}\theta}{\sin\theta}": (1 - c ** 2) / s,
        r"(1 - \sin^{2}\theta)\sec\theta": (1 - s ** 2) * sec,
        r"\sec\theta - \sin\theta\tan\theta": sec - s * t,
        r"\operatorname{cosec}\theta - \cos\theta\cot\theta": csc - c * cot,
        r"\frac{\sec^{2}\theta - 1}{\tan\theta}": (sec ** 2 - 1) / t,
        r"(1 + \tan^{2}\theta)\cos\theta": (1 + t ** 2) * c,
        r"(\operatorname{cosec}^{2}\theta - 1)\tan\theta": (csc ** 2 - 1) * t,
        r"\frac{\tan\theta}{\sec\theta}": t / sec,
    }
    return table[tex]


def test_power_forms_reduce_to_cos_2a():
    A = th
    exprs = [sympy.cos(A) ** 4 - sympy.sin(A) ** 4, sympy.sin(A) ** 4 - sympy.cos(A) ** 4,
             (sympy.cos(A) - sympy.sin(A)) * (sympy.cos(A) + sympy.sin(A))]
    for (_, sign), e in zip(mt.POWER_FORMS, exprs):
        assert sympy.simplify(e - sign * sympy.cos(2 * A)) == 0


def test_triple_angle_ratio():
    e = sympy.sin(3 * th) ** 2 / sympy.sin(th) ** 2 - sympy.cos(3 * th) ** 2 / sympy.cos(th) ** 2
    assert sympy.simplify(sympy.expand_trig(e) - 8 * sympy.cos(2 * th)) == 0
    for k in range(-7, 8):
        assert mt.triple_angle_cos(k) == Fraction(k, 8)


def test_angle_sum_from_tans():
    for p, q in TAN_PAIRS:
        for a, b in ((p, q), (q, p)):
            total = sympy.atan(R(a)) + sympy.atan(R(b))
            # SymPy leaves atan sums unsimplified; 50 digits settle which multiple of π it is.
            assert abs(sympy.N(total - R(angle_sum_from_tans(a, b)) * sympy.pi, 50)) < 1e-40


def test_inverse_compositions():
    fns = {"arcsin": sympy.asin, "arccos": sympy.acos, "arctan": sympy.atan}
    outs = {"sin": sympy.sin, "cos": sympy.cos, "tan": sympy.tan}
    for f1 in fns:
        for f2 in fns:
            for t1 in TRIPLES[:4]:
                for t2 in TRIPLES[2:6]:
                    s1, c1, a1 = inverse_sin_cos(f1, *t1)
                    s2, c2, a2 = inverse_sin_cos(f2, *t2)
                    angle = fns[f1](R(a1)) + fns[f2](R(a2))
                    for outer, fn in outs.items():
                        ours = compose(outer, s1, c1, s2, c2)
                        if ours is None:
                            continue
                        # SymPy leaves these unsimplified; 50 digits are decisive for small rationals.
                        assert abs(sympy.N(fn(angle) - R(ours), 50)) < 1e-40, (f1, f2, t1, t2, outer)


def test_complement_solution():
    for p in range(1, 5):
        for r in range(1, 5):
            for q in range(-4, 5):
                for s in range(-4, 5):
                    x = complement_solution(p, q, r, s)
                    if x is None:
                        continue
                    lhs = sympy.asin(R(p * x + q)) + sympy.acos(R(r * x + s))
                    assert abs(sympy.N(lhs - sympy.pi / 2, 50)) < 1e-40, (p, q, r, s)


def _count_roots(f, lo: float, hi: float, steps: int = 200000) -> int:
    """Sign changes of a continuous f on [lo, hi] (no tangential roots in these families)."""
    count, prev = 0, f(lo)
    for i in range(1, steps + 1):
        cur = f(lo + (hi - lo) * i / steps)
        if prev == 0 or prev * cur < 0:
            count += 1
        prev = cur
    return count + (cur == 0)


def test_sine_counts():
    for k in range(2, 7):
        for n in range(1, 4):
            for c in (0.75, -0.4):
                seen = _count_roots(lambda t: math.sin(k * t) - c, 0, n * math.pi)
                assert seen == sine_solution_count(k, n, c > 0), (k, n, c)


def test_cos_and_tan_counts():
    for k in range(2, 7):
        for n in range(1, 4):
            assert _count_roots(lambda t: math.cos(k * t) - 0.6, 0, n * math.pi) == cos_or_tan_solution_count(k, n)
            # tan kθ = c ⇔ sin kθ − c cos kθ = 0 away from the poles.
            for c in (2.0, -0.5):
                seen = _count_roots(lambda t: math.sin(k * t) - c * math.cos(k * t), 0, n * math.pi)
                assert seen == cos_or_tan_solution_count(k, n), (k, n, c)


def test_tan_shift_counts_and_stated_approximations():
    for _, approx, lam in LAMBDAS:
        for m in range(1, 4):
            seen = _count_roots(lambda x: math.sin(lam * x - lam * math.pi), 0, m * math.pi)
            # sin(λx − λπ) = 0 ⇔ tan(λx) = tan(λπ).
            assert seen == tan_shift_count(lam, m), (approx, m)
            assert tan_shift_count(float(approx), m) == tan_shift_count(lam, m)


def test_triangle_kinds_and_obtuse_counts():
    for a in range(1, 13):
        for b in range(a, 13):
            brute = sum(triangle_kind(a, b, x) == "obtuse" for x in range(1, a + b + 1))
            assert obtuse_third_sides(a, b) == brute, (a, b)
    assert triangle_kind(1, 2, 3) == "none"
    assert triangle_kind(3, 4, 5) == "right"
    assert triangle_kind(4, 5, 6) == "acute"


def test_right_triangle_formulas():
    for (p, q), cs in TAN_HYPOTENUSE.items():
        assert cs, (p, q)
        for c in cs:
            a = c * p / sympy.sqrt(p * p + q * q)
            b = c * q / sympy.sqrt(p * p + q * q)
            assert sympy.simplify(a * b / 2 - R(area_from_hypotenuse_and_tan(c, p, q))) == 0
    for p, q, r in TRIPLES:
        for k in (1, 2, 3):
            assert sine_sum_from_area(k * r, Fraction(k * k * p * q, 2)) == Fraction(p + q, r)


def test_exam_answers_reproduce():
    assert sine_solution_count(5, 3, True) == 16                          # กสพท คณิต1 (มี.ค. 2565/26)
    assert tan_shift_count(2.71, 2) == 5                                  # A-level 1 (มี.ค. 2567/15)
    assert angle_sum_from_tans(Fraction(2), Fraction(3)) == Fraction(3, 4)  # กสพท คณิต1 (ธ.ค. 2559/3)
    s1, c1, _ = inverse_sin_cos("arccos", 5, 12, 13)
    s2, c2, _ = inverse_sin_cos("arcsin", 3, 4, 5)
    assert compose("tan", s1, c1, s2, c2) == Fraction(-63, 16)           # A-level 1 (มี.ค. 2566/7)
    assert mt.triple_angle_cos(1) == Fraction(1, 8)                          # กสพท คณิต1 (มี.ค. 2563/14): cos θ = 3/4
    assert mt.root_tex((1 + mt.triple_angle_cos(1)) / 2) == r"\frac{3}{4}"
    assert triangle_kind(2, 3, 4) == "obtuse"                             # กสพท คณิต1 (มี.ค. 2561/16)
    assert area_from_hypotenuse_and_tan(10, 1, 3) == 15                   # กสพท คณิต2 (มี.ค. 2562/15)
    assert sine_sum_from_area(10, Fraction(24)) == Fraction(7, 5)        # กสพท คณิต2 (มี.ค. 2561/15)
    assert area_from_scaled_sines(Fraction(3), Fraction(27)) == Fraction(27, 16)  # (มี.ค. 2563/15): 3√3/4
    assert mt.arc_to_point(2, Fraction(5, 6)) == Fraction(5, 3)             # กสพท คณิต1 (เม.ย. 2564/23)
    # cos⁴(5π/12) − sin⁴(5π/12) = cos(5π/6) = −√3/2           กสพท คณิต1 (มี.ค. 2562/3)
    assert mt.UNIT_CIRCLE[Fraction(5, 6)][0] == (Fraction(-1, 2), 3)


# ── Reduction and product/sum sets (from the (rath) notes) ────────────────────

def _val(terms):
    return sum(float(c) * math.sqrt(m) for c, m in terms)


def test_reductions_match_sympy():
    fns = {"sin": sympy.sin, "cos": sympy.cos, "tan": sympy.tan, "cot": sympy.cot, "sec": sympy.sec,
           "cosec": sympy.csc}
    for fn in fns:
        for k in range(0, 5):
            for sign in (1, -1):
                s, g = mt.reduce_angle(fn, k, sign)
                lhs = fns[fn](k * sympy.pi / 2 + sign * th)
                assert sympy.simplify(lhs - s * fns[g](th)) == 0, (fn, k, sign)


def test_special_table():
    for d in (0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330):
        (c, cm), (s, sm) = mt.special(d)
        assert abs(float(c) * math.sqrt(cm) - math.cos(math.radians(d))) < 1e-12
        assert abs(float(s) * math.sqrt(sm) - math.sin(math.radians(d))) < 1e-12


def test_product_and_sum_formulas():
    r = math.radians
    for a in range(15, 180, 15):
        for b in range(15, a, 15):
            if (a + b) in mt.SPECIAL_DEGREES + (360,) and (a - b) in mt.SPECIAL_DEGREES:
                assert abs(_val(mt.product_to_sum("cc", a, b)) - 2 * math.cos(r(a)) * math.cos(r(b))) < 1e-12
                assert abs(_val(mt.product_to_sum("ss", a, b)) - 2 * math.sin(r(a)) * math.sin(r(b))) < 1e-12
                assert abs(_val(mt.product_to_sum("sc", a, b)) - 2 * math.sin(r(a)) * math.cos(r(b))) < 1e-12
            if (a + b) % 2 == 0 and (a + b) // 2 in mt.SPECIAL_DEGREES and (a - b) // 2 in mt.SPECIAL_DEGREES:
                for form, f in (("s+", math.sin(r(a)) + math.sin(r(b))), ("c+", math.cos(r(a)) + math.cos(r(b))),
                                ("c-", math.cos(r(a)) - math.cos(r(b)))):
                    assert abs(_val([mt.sum_to_product(form, a, b)]) - f) < 1e-12, (form, a, b)
    exprs = [math.cos(r(20)) * math.cos(r(40)) * math.cos(r(80)), math.cos(r(36)) * math.cos(r(72)),
             math.sin(r(10)) * math.sin(r(50)) * math.sin(r(70)),
             math.cos(math.pi / 7) * math.cos(2 * math.pi / 7) * math.cos(4 * math.pi / 7)]
    for (_, v), e in zip(mt.COS_PRODUCTS, exprs):
        assert abs(float(v) - e) < 1e-12


def test_surd_sum_tex():
    assert mt.surd_sum_tex([(Fraction(1, 2), 3), (Fraction(-1, 2), 1)]) == r"\frac{\sqrt{3} - 1}{2}"
    assert mt.surd_sum_tex([(Fraction(1, 4), 6), (Fraction(1, 4), 2)]) == r"\frac{\sqrt{6} + \sqrt{2}}{4}"
    assert mt.surd_sum_tex([(Fraction(1, 2), 1), (Fraction(1, 2), 1)]) == "1"


def test_rath_answers_reproduce():
    assert mt.surd_sum_tex(mt.product_to_sum("cc", 75, 15)) == r"\frac{1}{2}"   # (rath) 6: 2cos75°cos15° = 1/2
    assert mt.sum_to_product("c+", 75, 15) == (Fraction(1, 2), 6)                # (rath) 6: cos15° + cos75° = √6/2
    assert mt.reduce_angle("cos", 2, -1) == (-1, "cos")                          # (rath) 2: cos(π − θ) = −cos θ


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(120):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
