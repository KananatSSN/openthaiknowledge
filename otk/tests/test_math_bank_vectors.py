"""The vector sets built from the sheet bank's knowledge units.

Products, triple-product forms and point formulas are checked against SymPy
matrices; the statement bank on random vectors; the source exams' answers
are pinned.
"""

from __future__ import annotations

import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m5 import vectors as mv
from otk.sets._support.math_bank_vectors import cross, dot, triple

sympy = pytest.importorskip("sympy")
KEYS = ("math.vector_triple_product_m5", "math.vector_identity_m5", "math.vector_points_m5")


def V(v):
    return sympy.Matrix(v)


def R(v):
    v = Fraction(v)
    return sympy.Rational(v.numerator, v.denominator)


def _vecs(rng, n=3):
    return [tuple(rng.randint(-5, 5) for _ in range(3)) for _ in range(n)]


def test_products_match_sympy():
    rng = random.Random(1)
    for _ in range(100):
        u, v, w = _vecs(rng)
        assert dot(u, v) == V(u).dot(V(v))
        assert V(cross(u, v)) == V(u).cross(V(v))
        assert triple(u, v, w) == V(u).dot(V(v).cross(V(w)))


def test_triple_forms():
    a, b, c = sympy.symbols("a1:4"), sympy.symbols("b1:4"), sympy.symbols("c1:4")
    A, B, C = sympy.Matrix(a), sympy.Matrix(b), sympy.Matrix(c)
    D = A.dot(B.cross(C))
    exprs = [A.cross(C).dot(A + B + C), A.cross(B).dot(A + C), C.cross(A).dot(B - A), B.cross(A).dot(2 * C),
             B.dot(A.cross(C)), (A + B).dot(B.cross(C))]
    for (_, mult), e in zip(mv.TRIPLE_FORMS, exprs):
        assert sympy.expand(e - mult * D) == 0


def test_perpendicular_parameter():
    rng = random.Random(2)
    for _ in range(100):
        u, v = _vecs(rng, 2)
        w1, w2 = rng.randint(-4, 5), rng.randint(-4, 5)
        a = mv.perpendicular_parameter(u, v, w1, w2)
        if a is not None:
            assert V(u).cross(V(v)).dot(sympy.Matrix([w1, w2, R(a)])) == 0


def test_cos_from_sum_ratio():
    c = sympy.Symbol("c")
    for k in (3, 4, 5, 6, 8, 10):
        for minus in (False, True):
            lhs = 2 - 2 * c if minus else 2 + 2 * c           # |u ± v|² for unit vectors
            sols = [s for s in sympy.solve(sympy.Eq(lhs, k * (1 - c ** 2)), c) if abs(s) < 1]
            assert sols == [R(mv.cos_from_sum_ratio(k, minus))]


def test_vector_fact_bank():
    rng = random.Random(3)
    seen_false = set()
    for _ in range(40):
        u, v, w = (V(x) for x in _vecs(rng))
        checks = {
            0: lambda: u.cross(v).dot(w) == u.dot(v.cross(w)),
            1: lambda: (u - v).dot(u + v) == u.dot(u) - v.dot(v),
            2: lambda: (u - v).cross(u + v) == 2 * u.cross(v),
            3: lambda: u.dot(u.cross(v)) == 0,
            4: lambda: u.dot(v) ** 2 + u.cross(v).dot(u.cross(v)) == u.dot(u) * v.dot(v),
            5: lambda: (u + v).cross(w) == u.cross(w) + v.cross(w),
            6: lambda: u.cross(v) == -v.cross(u),
            7: lambda: u.cross(v).cross(w) == u.cross(v.cross(w)),
            8: lambda: (u + v).cross(u - v) == 2 * u.cross(v),
            9: lambda: u.cross(v) == v.cross(u),
            10: lambda: u.cross(v).norm() == u.norm() * v.norm(),
            11: lambda: (u + v).norm() == u.norm() + v.norm(),
            12: lambda: u.dot(v) * w == u * v.dot(w),
        }
        for i, (tex, true) in enumerate(mv.VECTOR_FACTS):
            ok = bool(checks[i]())
            if true:
                assert ok, tex
            elif not ok:
                seen_false.add(tex)
    assert seen_false == {t for t, true in mv.VECTOR_FACTS if not true}


def test_point_formulas():
    rng = random.Random(4)
    for _ in range(80):
        a, b, c = _vecs(rng)
        n2 = mv.triangle_area_sq4(a, b, c)
        AB, AC = V(b) - V(a), V(c) - V(a)
        assert n2 == AB.cross(AC).dot(AB.cross(AC))
        rest = (rng.randint(-3, 6), rng.randint(-3, 6))
        x = mv.perpendicular_x(a, b, c, rest)
        if x is not None:
            D = sympy.Matrix([R(x), *rest])
            assert AB.dot(D - V(c)) == 0
        d, n1, m2 = mv.angle_cos(a, b, c)
        BA, BC = V(a) - V(b), V(c) - V(b)
        if n1 and m2:
            ours = R(d) / sympy.sqrt(n1 * m2)
            assert sympy.simplify(ours - BA.dot(BC) / (BA.norm() * BC.norm())) == 0


def test_exam_answers_reproduce():
    v = (2, 3, 1)
    assert dot(cross(v, mv.E["i"]), (0, 1, 1)) == -2                                  # กสพท คณิต1 (มี.ค. 2563/4)
    assert -dot((2, -1, 1), (3, 2, -1)) == -3                                            # กสพท คณิต1 (ธ.ค. 2559/4)
    assert mv.perpendicular_parameter((2, -1, 2), (-1, -2, 3), 4, 3) == -4                  # A-level 1 (มี.ค. 2566/15)
    assert mv.cos_from_sum_ratio(3, False) == Fraction(1, 3)                                # กสพท คณิต1 (มี.ค. 2561/15)
    assert mv.length_tex(mv.triangle_area_sq4((-2, -4, -4), (0, -2, 0), (0, 0, 2)), half=True) == r"2\sqrt{3}"  # (เม.ย. 2564/15)
    x = mv.perpendicular_x((0, 3, 2), (1, -1, 0), (2, 1, 3), (5, 1))                        # กสพท คณิต1 (มี.ค. 2565/17)
    ad = mv.sub((int(x), 5, 1), (0, 3, 2))
    assert x == 14 and mv.length_tex(dot(ad, ad)) == r"\sqrt{201}"


def test_tex_helpers():
    assert mv.ijk_tex((2, -1, 1)) == r"2\vec{i} - \vec{j} + \vec{k}"
    assert mv.ijk_tex((0, 0, -3)) == r"-3\vec{k}"
    assert mv.cos_tex(1, 2, 8) == r"\frac{1}{4}"


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(120):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
