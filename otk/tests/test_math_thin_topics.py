"""Third sets for the topics that were held up by filler sets
(math_thin_topics): every answer re-derived from what the learner is shown."""

from __future__ import annotations

from otk.tests._origins import keys_from

import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.p1.solids import _OBJECTS_math_thin_topics as _OBJECTS
from otk.sets.math.m6.integration_by_substitution import _SUBSTITUTIONS

SEEDS = range(300)
KEYS = keys_from("math_thin_topics")


def _b(block) -> str:
    return getattr(block, "text", None) or getattr(block, "tex", "") or ""


def _stem(q) -> str:
    return " ".join(_b(b) for b in q.stem)


def _choices(q) -> list[str]:
    return [" ".join(_b(b) for b in c.content) for c in q.choices]


def _answer(q) -> str:
    return _choices(q)[q.answer]


def _wrongs(q) -> list[str]:
    return [c for i, c in enumerate(_choices(q)) if i != q.answer]


def _each(key):
    for seed in SEEDS:
        yield generate(key, Random(seed))


def _ints(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"-?\d+", s.replace(",", ""))]


def _frac(tex: str) -> Fraction:
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if m:
        return (-1 if m.group(1) else 1) * Fraction(int(m.group(2)), int(m.group(3)))
    return Fraction(tex)


def test_sixteen_sets_and_no_fillers_left():
    assert len(KEYS) == 16
    assert not [k for k in REGISTRY if k.startswith("math.ipst.")]


@pytest.mark.parametrize("key", KEYS)
def test_four_distinct_choices(key):
    for q in _each(key):
        assert len(q.choices) == REGISTRY[key].max_choices and len(set(_choices(q))) == REGISTRY[key].max_choices, (key, _stem(q))


def _poly(tex: str) -> dict[int, int]:
    """'y = -2x^{2} + 8x - 10' -> {2: -2, 1: 8, 0: -10}."""
    body = tex.removeprefix("y = ").replace(" ", "")
    out = {2: 0, 1: 0, 0: 0}
    for sign, coef, var, power in re.findall(r"([+-]?)(\d*)(x?)(?:\^\{(\d)\})?", body):
        if not (coef or var):
            continue
        c = int(coef or 1) * (-1 if sign == "-" else 1)
        out[int(power) if power else (1 if var else 0)] = c
    return out


def test_solid_count():
    shape_of = dict(_OBJECTS)
    for q in _each("math.solid_count_p1"):
        s = _stem(q)
        if s.startswith("สิ่งของใด"):
            shapes = [shape_of[c] for c in _choices(q)]
            assert shapes.count(shape_of[_answer(q)]) == 1
        else:
            listed = s.split("ดังนี้ ")[1].split(" สิ่งของที่")[0].split()
            shape = re.search(r"รูปทรงเป็น(\S+?)มีกี่ชิ้น", s).group(1)
            assert int(_answer(q)) == sum(shape_of[o] == shape for o in listed)


def test_division_context():
    for q in _each("math.division_context_p4"):
        s = _stem(q)
        n, d = _ints(s)[:2]
        want = -(-n // d) if "อย่างน้อย" in s else n // d if "ซื้อได้มากที่สุด" in s else n % d
        assert int(_answer(q)) == want, s


def test_box_plot_compare():
    for q in _each("math.box_plot_compare_m2"):
        lines = _b(q.stem[0]).split("\n")
        a = [int(v) for v in re.findall(r"\d+", lines[1].replace("ควอร์ไทล์ที่ 1", "").replace("ควอร์ไทล์ที่ 3", ""))]
        b = [int(v) for v in re.findall(r"\d+", lines[2].replace("ควอร์ไทล์ที่ 1", "").replace("ควอร์ไทล์ที่ 3", ""))]
        ask = _b(q.stem[1])
        if "มัธยฐาน" in ask:
            assert int(_answer(q)) == abs(a[2] - b[2])
        elif "ห้องใด" in ask:
            assert _answer(q) == ("ห้อง ก" if a[3] - a[1] > b[3] - b[1] else "ห้อง ข")
        else:
            assert int(_answer(q)) == max(a[3] - a[1], b[3] - b[1])


def test_parabola_from_roots():
    for q in _each("math.parabola_from_roots_m4"):
        r1, r2, x0, y0 = _ints(_stem(q))[:4]
        for choice in _choices(q):
            c = _poly(choice)
            f = lambda x: c[2] * x * x + c[1] * x + c[0]
            fits = f(r1) == 0 and f(r2) == 0 and f(x0) == y0
            assert fits == (choice == _answer(q)), (choice, _stem(q))


def test_parabola_three_points():
    for q in _each("math.parabola_three_points_m4"):
        pts = [tuple(map(int, p)) for p in re.findall(r"\((-?\d+), (-?\d+)\)", _stem(q))]
        if "ค่า a" in _stem(q):
            (_, ym), (_, y0), (_, yp) = pts
            assert int(_answer(q)) == (ym + yp) // 2 - y0
            continue
        for choice in _choices(q):
            c = _poly(choice)
            fits = all(c[2] * x * x + c[1] * x + c[0] == y for x, y in pts)
            assert fits == (choice == _answer(q))


def test_trig_ratio_triangle():
    for q in _each("math.trig_ratio_triangle_m5"):
        s = _b(q.stem[0])
        sides = dict(re.findall(r"(AB|BC|AC) = (\d+)", s))
        sides = {k: int(v) for k, v in sides.items()}
        if "AB" not in sides:
            sides["AB"] = math.isqrt(sides["BC"] ** 2 + sides["AC"] ** 2)
        elif "BC" not in sides:
            sides["BC"] = math.isqrt(sides["AB"] ** 2 - sides["AC"] ** 2)
        else:
            sides["AC"] = math.isqrt(sides["AB"] ** 2 - sides["BC"] ** 2)
        a, b, c = sides["BC"], sides["AC"], sides["AB"]
        assert a * a + b * b == c * c
        want = {r"\sin A": Fraction(a, c), r"\cos A": Fraction(b, c), r"\tan A": Fraction(a, b),
                r"\sin B": Fraction(b, c), r"\cos B": Fraction(a, c), r"\tan B": Fraction(b, a)}[q.stem[1].tex]
        assert _frac(_answer(q)) == want


def _surd(tex: str) -> float:
    m = re.fullmatch(r"\\frac\{(\d*)\\sqrt\{(\d+)\}\}\{(\d+)\}", tex)
    if m:
        return int(m.group(1) or 1) * math.sqrt(int(m.group(2))) / int(m.group(3))
    m = re.fullmatch(r"(\d*)\\sqrt\{(\d+)\}", tex)
    if m:
        return int(m.group(1) or 1) * math.sqrt(int(m.group(2)))
    return float(_frac(tex))


def test_angle_of_elevation():
    for q in _each("math.angle_of_elevation_m5"):
        s = _stem(q)
        n, theta = _ints(s)[:2]
        f = math.tan if "มุมเงย" in s else math.sin
        want = n * f(math.radians(theta))
        assert math.isclose(_surd(_answer(q)), want), s
        assert not any(math.isclose(_surd(w), want) for w in _wrongs(q))


def _cubic(tex: str):
    c = {3: 0, 2: 0, 1: 0, 0: 0}
    for sign, coef, var, power in re.findall(r"([+-]?)(\d*)(x?)(?:\^\{(\d)\})?", tex.replace(" ", "")):
        if coef or var:
            c[int(power) if power else (1 if var else 0)] = int(coef or 1) * (-1 if sign == "-" else 1)
    return lambda x: c[3] * x ** 3 + c[2] * x * x + c[1] * x + c[0]


def test_turning_point():
    for q in _each("math.turning_point_m5"):
        f = _cubic(q.stem[1].tex.removeprefix("f(x) = "))
        # Scan the whole-number grid for a strict local maximum and minimum.
        xs = range(-8, 9)
        maxima = [x for x in xs if f(x) > f(x - 1) and f(x) > f(x + 1)]
        minima = [x for x in xs if f(x) < f(x - 1) and f(x) < f(x + 1)]
        ask = _b(q.stem[2]) if len(q.stem) > 2 else ""
        if "สูงสุดสัมพัทธ์ที่" in ask:
            assert int(_answer(q)) == maxima[0]
        elif "ต่ำสุดสัมพัทธ์ที่" in ask:
            assert int(_answer(q)) == minima[0]
        else:
            assert int(_answer(q)) == f(maxima[0])


def test_integral_properties():
    for q in _each("math.integral_properties_m5"):
        given = q.stem[1].tex
        (a, b, P), (_, c, Q) = [tuple(map(int, t)) for t in
                                re.findall(r"\\int_\{(-?\d+)\}\^\{(-?\d+)\} f\(x\)\\,dx = (-?\d+)", given)]
        ask = q.stem[3].tex
        lo, hi = map(int, re.match(r"\\int_\{(-?\d+)\}\^\{(-?\d+)\}", ask).groups())
        if "left" in ask:
            k, m = map(int, re.search(r"\\left\((\d+)f\(x\) \+ (\d+)\\right\)", ask).groups())
            want = k * P + m * (b - a)
        elif (lo, hi) == (a, c):
            want = P + Q
        else:
            assert (lo, hi) == (b, a)
            want = -P
        assert int(_answer(q)) == want


def test_integral_distance():
    for q in _each("math.integral_distance_m5"):
        T = _ints(_b(q.stem[0]))[1]
        v = q.stem[1].tex.removeprefix("v(t) = ")
        m = re.fullmatch(r"(\d+)t(\^\{2\})?(?: \+ (\d+))?", v)
        k, sq, b = int(m.group(1)), bool(m.group(2)), int(m.group(3) or 0)
        want = Fraction(k * T ** 3, 3) + b * T if sq else Fraction(k * T * T, 2) + b * T
        assert int(_answer(q)) == want


def test_area_power_curve():
    for q in _each("math.area_power_curve_m5"):
        curve = q.stem[1].tex.removeprefix("y = ")
        if "-" in curve:
            c = math.isqrt(int(curve.split("- ")[1]))
            want = Fraction(4 * c ** 3, 3)
        else:
            k, n = re.fullmatch(r"(\d*)x\^\{(\d)\}", curve).groups()
            k, n = int(k or 1), int(n)
            b = _ints(_b(q.stem[2]))[-1]
            want = Fraction(k * b ** (n + 1), n + 1)
        assert _frac(_answer(q)) == want


def test_piecewise_limit():
    for q in _each("math.piecewise_limit_m6"):
        f = next(b.tex for b in q.stem if getattr(b, "tex", "").startswith("f(x)"))
        left, right = re.search(r"\\begin\{cases\} (.+?) & x < (-?\d+) \\\\ (.+?) & x", f).group(1, 3)
        c = int(re.search(r"x < (-?\d+)", f).group(1))
        lim_l = _cubic(left)(c)
        if "จงหาค่า k" in _stem(q):
            k = int(_answer(q))
            assert _cubic(right.replace("kx", f"{k}x" if k >= 0 else f"-{-k}x").replace("--", "+"))(c) == lim_l
        elif q.stem[1].tex.startswith(r"\lim"):
            assert int(_answer(q)) == lim_l
        else:
            lim_r = _cubic(right)(c)
            assert _answer(q) == (f"ลิมิตมีค่าเท่ากับ {lim_l}" if lim_l == lim_r
                                  else "ไม่มีลิมิต เพราะลิมิตซ้ายไม่เท่ากับลิมิตขวา")


def test_substitution_setup_is_the_inner_function():
    for q in _each("math.substitution_setup_m6"):
        integral = q.stem[1].tex
        assert "{{" not in integral and "@" not in integral
        n = (re.findall(r"\^\{(\d)\}", integral) or ["0"])[-1]
        template = next(t for t in _SUBSTITUTIONS if t[0].replace("@n", n) == integral)
        assert _answer(q) == template[1].replace("@n", n)
        # The chosen u, with its power stripped, sits inside the integrand.
        assert re.sub(r"\^\{\d\}", "", _answer(q).removeprefix("u = ")) in re.sub(r"\^\{\d\}", "", integral)


def test_substitution_definite():
    for q in _each("math.substitution_definite_m6"):
        tex = q.stem[1].tex
        a, b = map(int, re.match(r"\\int_\{(\d+)\}\^\{(\d+)\}", tex).groups())
        inner, n = re.search(r"\((.+)\)\^\{(\d)\}", tex).groups()
        g = _cubic(inner)
        # Numerically: a midpoint sum of g'(x) g(x)^n.
        steps = 4000
        dx = (b - a) / steps
        total = sum((g(a + (i + 0.5) * dx + 1e-6) - g(a + (i + 0.5) * dx - 1e-6)) / 2e-6
                    * g(a + (i + 0.5) * dx) ** int(n) * dx for i in range(steps))
        assert math.isclose(float(_frac(_answer(q))), total, rel_tol=1e-4)


def test_area_two_curves():
    for q in _each("math.area_two_curves_m6"):
        other = q.stem[3].tex.removeprefix("y = ")
        if other.endswith("x"):
            # y = kx meets y = x² at 0 and k.
            k = int(other[:-1] or 1)
            want = Fraction(k ** 3, 6)
        elif "x" in other:
            a = math.isqrt(int(other.split("+ ")[1]) // 2)
            want = Fraction(8 * a ** 3, 3)
        else:
            a = math.isqrt(int(other))
            want = Fraction(4 * a ** 3, 3)
        assert _frac(_answer(q)) == want


def test_area_integral_setup():
    for q in _each("math.area_integral_setup_m6"):
        other = q.stem[3].tex.removeprefix("y = ")
        lo, hi, upper, lower = re.fullmatch(
            r"\\int_\{(-?\d+)\}\^\{(-?\d+)\} \\left\((.+) - (.+)\\right\)dx", _answer(q)).groups()
        lo, hi = int(lo), int(hi)
        top = _cubic(upper)
        low = _cubic(lower)
        # The bounds are where the curves meet, and upper is above between them.
        assert top(lo) == low(lo) and top(hi) == low(hi)
        assert top((lo + hi) / 2) > low((lo + hi) / 2)
        assert lower == "x^{2}" and upper == other
