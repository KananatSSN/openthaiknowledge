"""Pictures for the สสวท. เพิ่มเติม track: every answer re-derived from the spec
the picture was drawn from, by evaluating the chosen expression numerically."""

from __future__ import annotations

from otk.tests._origins import keys_from

import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.core.render.assets import is_diagram
from otk.sets._support import math_pictures_add as ma
from otk.sets.math.m6.limits import NO_LIMIT
from otk.sets.math.m6.relative_extrema import _LETTERS

SEEDS = range(250)
KEYS = keys_from("math_pictures_add")
SPECS = {s.asset_id: s for s in ma.ALL_ADD_PICTURES}


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _stem_math(q) -> str:
    return " ".join(b.tex for b in q.stem if b.kind == "math")


def _stem_text(q) -> str:
    return " ".join(b.text for b in q.stem if b.kind == "text")


def _spec(q):
    [img] = [b for b in q.stem if b.kind == "image"]
    return SPECS[img.asset_id], img


def _num(tex: str) -> float:
    """-\\frac{\\sqrt{3}}{2}, 2\\sqrt{5}, \\frac{32}{3}, 7 -> a float."""
    tex = tex.strip()
    sign = -1 if tex.startswith("-") else 1
    tex = tex.lstrip("-")
    m = re.fullmatch(r"\\frac\{(.+)\}\{(\d+)\}", tex)
    if m:
        return sign * _num(m.group(1)) / int(m.group(2))
    m = re.fullmatch(r"(\d*)\\sqrt\{(\d+)\}", tex)
    if m:
        return sign * int(m.group(1) or 1) * math.sqrt(int(m.group(2)))
    return sign * float(tex)


def _py(expr: str) -> str:
    """A polynomial in x, y from tex to Python."""
    expr = expr.replace("^{2}", "**2")
    return re.sub(r"(\d)([xy])", r"\1*\2", expr)


def test_ten_sets_every_picture_drawable_and_alt_free_of_numbers():
    assert len(KEYS) == 10
    for spec in ma.ALL_ADD_PICTURES:
        assert is_diagram(spec.asset_id), spec
    for key in KEYS:
        for seed in range(40):
            q = generate(key, Random(seed))
            _, img = _spec(q)
            assert not re.search(r"\d", img.alt), (key, img.alt)
            assert len({_choice(c) for c in q.choices}) == REGISTRY[key].max_choices == len(q.choices), (key, seed)


def _check_quad_ineq(q, s):
    op = re.search(r"f\(x\) (>|<|\\geq|\\leq) 0", _stem_math(q)).group(1)
    ans = _answer(q)
    grid = [x / 2 for x in range(-16, 17)]

    def holds(x):
        v = s.a * (x - s.r1) * (x - s.r2)
        return {">": v > 0, "<": v < 0, r"\geq": v >= 0, r"\leq": v <= 0}[op]

    def claimed(x):
        cmp = {"<": lambda a, b: a < b, r"\leq": lambda a, b: a <= b,
               ">": lambda a, b: a > b, r"\geq": lambda a, b: a >= b}
        m = re.fullmatch(r"(-?\d+) (<|\\leq) x (<|\\leq) (-?\d+)", ans)
        if m:
            return cmp[m.group(2)](int(m.group(1)), x) and cmp[m.group(3)](x, int(m.group(4)))
        m = re.fullmatch(r"x (<|\\leq) (-?\d+) \\;,\\; x (>|\\geq) (-?\d+)", ans)
        return cmp[m.group(1)](x, int(m.group(2))) or cmp[m.group(3)](x, int(m.group(4)))

    assert all(holds(x) == claimed(x) for x in grid), (s, op, ans)


def _check_abs(q, s):
    ans = _answer(q)
    f = lambda x: s.a * abs(x - s.h) + s.k            # noqa: E731
    if "f(x) =" in _stem_math(q):
        c = int(_stem_math(q).split("=")[1])
        xs = [int(v) for v in re.findall(r"x = (-?\d+)", ans)]
        assert len(xs) == 2 and all(f(x) == c for x in xs), (s, c, ans)
        return
    m = re.fullmatch(r"y = (-?\d*)\\left\|x(?: ([+-]) (\d+))?\\right\|(?: ([+-]) (\d+))?", ans)
    a = {"": 1, "-": -1}.get(m.group(1), None) or int(m.group(1))
    h = 0 if not m.group(2) else (int(m.group(3)) if m.group(2) == "-" else -int(m.group(3)))
    k = 0 if not m.group(4) else (int(m.group(5)) if m.group(4) == "+" else -int(m.group(5)))
    assert all(a * abs(x - h) + k == f(x) for x in range(-6, 7)), (s, ans)


def _check_circle(q, s):
    lhs, rhs = _py(_answer(q)).split("=")
    g = lambda x, y: eval(lhs, {}, {"x": x, "y": y}) - eval(rhs, {}, {"x": x, "y": y})  # noqa: E731
    for x, y in ((s.h + s.r, s.k), (s.h - s.r, s.k), (s.h, s.k + s.r), (s.h, s.k - s.r)):
        assert g(x, y) == 0, (s, _answer(q))
    assert g(s.h, s.k) != 0


def _check_exp_log(q, s):
    ans = _answer(q)
    m = re.fullmatch(r"y = (?:(\d)\^\{x\}|\\left\(\\frac\{1\}\{(\d)\}\\right\)\^\{x\}"
                     r"|\\log_\{(?:(\d)|\\frac\{1\}\{(\d)\})\} x)(?: ([+-]) (\d))?", ans)
    assert m, ans
    shift = 0 if not m.group(5) else int(m.group(6)) * (1 if m.group(5) == "+" else -1)
    if m.group(1) or m.group(2):
        base = int(m.group(1)) if m.group(1) else 1 / int(m.group(2))
        f = lambda x: base ** x + shift              # noqa: E731
        truth = lambda x: float(s.base) ** x + s.k  # noqa: E731
        assert s.kind == "exp"
    else:
        base = int(m.group(3)) if m.group(3) else 1 / int(m.group(4))
        f = lambda x: math.log(x, base) + shift      # noqa: E731
        truth = lambda x: math.log(x, float(s.base)) + s.k  # noqa: E731
        assert s.kind == "log"
    assert all(math.isclose(f(x), truth(x)) for x in (0.5, 1, 2, 3)), (s, ans)


def _check_vectors(q, s):
    expr, ans = _stem_math(q), _answer(q)
    u, v = (s.ux, s.uy), (s.vx, s.vy)
    if r"\cdot" in expr:
        assert int(ans) == u[0] * v[0] + u[1] * v[1]
    elif "+" in expr:
        assert ans == f"({u[0] + v[0]}, {u[1] + v[1]})"
    elif "-" in expr:
        assert ans == f"({u[0] - v[0]}, {u[1] - v[1]})"
    else:
        assert math.isclose(_num(ans), math.hypot(*u)), (s, ans)


def _check_unit(q, s):
    fn = re.search(r"\\(sin|cos|tan)", _stem_math(q)).group(1)
    truth = getattr(math, fn)(math.radians(s.deg))
    assert math.isclose(_num(_answer(q)), truth, abs_tol=1e-9), (s, fn, _answer(q))


def _check_cos(q, s):
    ans = _answer(q)
    law = Fraction(s.b ** 2 + s.c ** 2 - s.a ** 2, 2 * s.b * s.c)
    assert s.a < s.b + s.c and s.b < s.a + s.c and s.c < s.a + s.b
    if "x" in _stem_text(q):
        assert s.hide and abs(law.numerator) == 1 and law.denominator == 2
        assert int(ans) == s.a
    elif "องศา" in _stem_text(q):
        deg = int(ans.split("^")[0])
        assert math.isclose(math.cos(math.radians(deg)), float(law))
    else:
        assert not s.hide and math.isclose(_num(ans), float(law)), (s, ans)


def _check_limit(q, s):
    expr, ans = _stem_math(q), _answer(q)
    eps = 1e-7
    left = s.left + s.ml * ((s.c - eps) - s.c)
    right = s.right + s.mr * ((s.c + eps) - s.c)
    if "^{-}" in expr:
        assert math.isclose(float(ans), left, abs_tol=1e-6)
    elif "^{+}" in expr:
        assert math.isclose(float(ans), right, abs_tol=1e-6)
    elif r"\lim" in expr:
        assert ans == (str(s.left) if abs(left - right) < 1e-6 else NO_LIMIT)
    else:
        assert ans == str(s.at)


def _check_deriv(q, c):
    def f(x):
        return c.s * (x ** 3 / 3 - (c.p + c.q) / 2 * x ** 2 + c.p * c.q * x)

    def d(x, h=1e-5):
        return (f(x + h) - f(x - h)) / (2 * h)

    stem = _stem_text(q)
    i = _LETTERS.index(_answer(q))
    x = c.xs[i]
    if "สูงสุด" in stem:
        assert abs(d(x)) < 1e-6 and d(x - 0.1) > 0 > d(x + 0.1)
    elif "ต่ำสุด" in stem:
        assert abs(d(x)) < 1e-6 and d(x - 0.1) < 0 < d(x + 0.1)
    elif "> 0" in stem:
        assert d(x) > 1e-6 and sum(d(y) > 1e-6 for y in c.xs) == 1
    else:
        assert d(x) < -1e-6 and sum(d(y) < -1e-6 for y in c.xs) == 1


def _check_area(q, r):
    f, g = [b.tex for b in q.stem if b.kind == "math"]
    fx = lambda e: (lambda x: eval(_py(e.split("=")[1]), {}, {"x": x}))  # noqa: E731
    top_or, other = fx(f), fx(g)
    # intersections, numerically, on a fine grid
    xs = [i / 1000 for i in range(-5000, 5001)]
    roots = [x for a, x in zip(xs, xs[1:]) if (top_or(a) - other(a)) * (top_or(x) - other(x)) <= 0]
    lo, hi = min(roots), max(roots)
    n = 2000
    h = (hi - lo) / n
    area = sum(abs(top_or(lo + (i + 0.5) * h) - other(lo + (i + 0.5) * h)) for i in range(n)) * h
    assert math.isclose(_num(_answer(q)), area, rel_tol=1e-3), (r, _answer(q), area)


CHECKS = {ma.QuadIneq: _check_quad_ineq, ma.AbsGraph: _check_abs, ma.CircleGrid: _check_circle,
          ma.ExpLogGraph: _check_exp_log, ma.VectorGrid: _check_vectors, ma.UnitPoint: _check_unit,
          ma.CosTriangle: _check_cos, ma.LimitGraph: _check_limit, ma.DerivCurve: _check_deriv,
          ma.AreaRegion: _check_area}


@pytest.mark.parametrize("key", KEYS)
def test_answers_rederived_from_the_picture_spec(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        spec, _ = _spec(q)
        CHECKS[type(spec)](q, spec)


def test_the_curves_on_screen_fit_the_grid():
    for s in ma.CIRCLE_GRIDS:
        assert abs(s.h) + s.r <= 6 and abs(s.k) + s.r <= 6
    for v in ma.VECTOR_GRIDS:
        assert max(map(abs, v)) <= 4 and v.ux * v.vy != v.uy * v.vx
    for c in ma.DERIV_CURVES:
        assert c.p in c.xs and c.q in c.xs and list(c.xs) == sorted(c.xs)
