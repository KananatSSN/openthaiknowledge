"""The analytic-geometry sets built from the sheet bank's knowledge units.

General forms are re-derived by expanding the standard forms with SymPy.
Focal definitions are checked on sample points, and tangency and
nearest-point answers by SymPy distance computations. The source exams'
answers are pinned.
"""

from __future__ import annotations

import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m4 import conic_sections as mc
from otk.sets.math.m4.circle_equations import (
    _NORMALS,
    radius_tangent_at_point,
    radius_tangent_to_axes_and_line,
    tangent_slope_from_origin,
)
from otk.sets.math.m4.equations_of_lines import foot_of_perpendicular
from otk.sets._support.math_bank_conics import line_tex

sympy = pytest.importorskip("sympy")
x, y = sympy.symbols("x y", real=True)
KEYS = ("math.conic_general_form_m4", "math.conic_focal_definition_m4",
        "math.circle_tangency_m4", "math.line_closest_point_m4")


def R(v):
    v = Fraction(v)
    return sympy.Rational(v.numerator, v.denominator)


@pytest.mark.parametrize("kind", ("ellipse", "hyperbola"))
def test_general_form_expands_the_standard_form(kind):
    triples = mc.ELLIPSE if kind == "ellipse" else mc.HYPERBOLA
    for a, b, c in triples:
        for h in (-3, 0, 2):
            for k in (-2, 1):
                for horizontal in (True, False):
                    A, B, D, E, F = mc.general_coefficients(kind, h, k, a, b, horizontal)
                    general = A * x ** 2 + B * y ** 2 + D * x + E * y + F
                    if kind == "ellipse":
                        p, q = (a * a, b * b) if horizontal else (b * b, a * a)
                        std = (x - h) ** 2 / p + (y - k) ** 2 / q - 1
                    elif horizontal:
                        std = (x - h) ** 2 / a ** 2 - (y - k) ** 2 / b ** 2 - 1
                    else:
                        std = (y - k) ** 2 / a ** 2 - (x - h) ** 2 / b ** 2 - 1
                    assert sympy.simplify(general / std).is_constant()
                    # Vertices lie on the curve; foci satisfy the focal definition at a vertex.
                    for vx, vy in mc.vertices(h, k, a, horizontal):
                        assert general.subs({x: vx, y: vy}) == 0
                    f1, f2 = mc.vertices(h, k, c, horizontal)
                    v = mc.vertices(h, k, a, horizontal)[1]
                    d1 = sympy.sqrt((v[0] - f1[0]) ** 2 + (v[1] - f1[1]) ** 2)
                    d2 = sympy.sqrt((v[0] - f2[0]) ** 2 + (v[1] - f2[1]) ** 2)
                    target = 2 * a
                    assert sympy.simplify((d1 + d2 if kind == "ellipse" else abs(d1 - d2)) - target) == 0


def test_foci_distance():
    for a in range(3, 10):
        for d in range(2, a):
            k, m = mc.ellipse_foci_distance(2 * a, d)
            assert sympy.simplify(k * sympy.sqrt(m) - 2 * sympy.sqrt(a * a - d * d)) == 0


def test_circle_tangent_to_axes_and_line():
    for a, b, n in _NORMALS:
        for sa in (1, -1):
            for r_true in range(2, 10):
                for sign in (1, -1):
                    aa = a * sa
                    c = sign * n * r_true - (aa + b) * r_true
                    for r in radius_tangent_to_axes_and_line(aa, b, c):
                        dist = abs(aa * r + b * r + c) / sympy.sqrt(aa ** 2 + b ** 2)
                        assert sympy.simplify(dist - R(r)) == 0


def test_circle_tangent_at_point():
    for u, v, w in ((4, 3, 5), (3, 4, 5), (12, 5, 13), (5, 12, 13)):
        for t in range(1, 4):
            r = R(radius_tangent_at_point(u, v, w, t))
            cx, cy = t * u - r * v / w, t * v + r * u / w
            assert cx == r and cy > 0
            # The centre is at distance r from the line vx − uy = 0 (tangent there).
            assert sympy.simplify(abs(v * cx - u * cy) / w - r) == 0


def test_tangent_slope_from_origin():
    m = sympy.Symbol("m")
    for r in range(1, 5):
        for k in range(1, 7):
            if k == r:
                continue
            ours = R(tangent_slope_from_origin(r, k))
            sols = sympy.solve(sympy.Eq((m * r - k) ** 2, r ** 2 * (1 + m ** 2)), m)
            assert ours in sols


def test_foot_of_perpendicular():
    rng = random.Random(4)
    for _ in range(80):
        a, b = rng.choice([1, 2, 3, -1, -2]), rng.choice([1, 2, -3, 4])
        c, x0, y0 = rng.randint(-9, 9), rng.randint(-6, 6), rng.randint(-6, 6)
        fx, fy = foot_of_perpendicular(a, b, c, x0, y0)
        assert a * fx + b * fy + c == 0
        # PF is parallel to the normal (a, b).
        assert (fx - x0) * b - (fy - y0) * a == 0


def test_exam_answers_reproduce():
    assert radius_tangent_to_axes_and_line(3, -4, 24) == [4]           # กสพท คณิต1 (ธ.ค. 2558/16)
    assert line_tex(-4, -3, 28) == "4x + 3y - 28 = 0"                  # …its line CP
    assert radius_tangent_at_point(4, 3, 5, 1) == Fraction(5, 2)       # กสพท คณิต1 (มี.ค. 2562/15)
    assert tangent_slope_from_origin(1, 2) == Fraction(3, 4)           # A-level 1 (มี.ค. 2566/29)
    assert foot_of_perpendicular(2, -1, 5, 0, 0) == (-2, 1)           # กสพท คณิต1 (มี.ค. 2563/3)
    assert mc.ellipse_foci_distance(12, 4) == (4, 5)                      # กสพท คณิต1 (มี.ค. 2561/14): 4√5


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(80):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
