"""The ม.4 sets added so every unit has at least ten: each answer worked out again from the stem alone.

Polynomials are compared by evaluating both sides at several points, numbers are read back out of the
question, and text answers are checked against facts written out here independently.
"""

from __future__ import annotations

import re
from fractions import Fraction
from math import comb, factorial, isqrt
from random import Random

from otk.core import generate
from otk.kit.math_problems import frac_tex

SEEDS = range(300)
POINTS = [(Fraction(v), Fraction(w)) for v, w in ((2, 3), (-3, 5), (7, -2), (Fraction(1, 2), 4), (11, 13))]


def _text(blocks) -> str:
    return "".join(getattr(b, "text", None) or getattr(b, "tex", None) or "" for b in blocks)


def _q(key: str, seed: int):
    q = generate(f"math.{key}", Random(seed))
    texts = [_text(c.content).replace("{,}", ",") for c in q.choices]
    assert len(set(texts)) == len(texts), (key, seed, texts)
    return _text(q.stem).replace("{,}", ","), texts[q.answer], texts


def _ints(s: str) -> list[int]:
    return [int(v) for v in re.findall(r"-?\d+", s.replace(",", ""))]


def _pos(s: str) -> list[int]:
    return [int(v) for v in re.findall(r"\d+", s.replace(",", ""))]


def _py(tex: str) -> str:
    """A TeX polynomial as Python: implicit products made explicit, powers as **."""
    s = tex.replace(r"\times", "*").replace("−", "-").replace(" ", "")
    s = re.sub(r"\^\{?(\d+)\}?", r"**\1", s)
    s = re.sub(r"(\d)([xy(])", r"\1*\2", s)
    s = re.sub(r"([xy)])([xy(])", r"\1*\2", s)
    s = re.sub(r"(\d+)", r"Fraction(\1)", s)
    return s


def _ev(tex: str, x: Fraction, y: Fraction = Fraction(0)) -> Fraction:
    s = _py(tex)
    assert re.fullmatch(r"[Fraction\d()xy+\-*]+", s), s
    return eval(s, {"Fraction": Fraction, "x": x, "y": y})  # noqa: S307 - digits, x, y and operators only


def _same(a: str, b: str) -> bool:
    return all(_ev(a, x, y) == _ev(b, x, y) for x, y in POINTS)


def _frac(s: str) -> Fraction:
    s = s.strip().replace(",", "")
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", s)
    if m:
        return (-1 if m.group(1) else 1) * Fraction(int(m.group(2)), int(m.group(3)))
    return Fraction(s)


def _point(s: str) -> tuple[Fraction, Fraction]:
    inner = s.strip()[1:-1]
    depth, cut = 0, None
    for i, ch in enumerate(inner):
        depth += ch == "{"
        depth -= ch == "}"
        if ch == "," and depth == 0:
            cut = i
            break
    return _frac(inner[:cut]), _frac(inner[cut + 1:])


def _line_eval(rhs: str, x: Fraction) -> Fraction:
    """y = mx + k right-hand sides with \\frac coefficients."""
    s = re.sub(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", lambda m: f"({m.group(1)}{m.group(2)}/{m.group(3)})", rhs)
    s = s.replace(" ", "")
    s = re.sub(r"(\d|\))x", r"\1*x", s)
    s = re.sub(r"(\d+)", r"Fraction(\1)", s)
    return eval(s, {"Fraction": Fraction, "x": x})  # noqa: S307 - digits, x and operators only


def test_counting():
    for seed in SEEDS:
        stem, right, _ = _q("outfits_m4", seed)
        a, b, c = _pos(stem)[:3]
        assert int(right) == a * b * c
        stem, right, _ = _q("codes_with_repeats_m4", seed)
        k = _pos(stem)[0]
        assert int(right.replace(",", "")) == (10 ** k if "ซ้ำกันได้" in stem else factorial(10) // factorial(10 - k))
        stem, right, _ = _q("numbers_no_repeat_m4", seed)
        digits = _pos(stem.split("สร้าง")[0])
        k = _pos(stem.split("สร้างจำนวน")[1])[0]
        from itertools import permutations
        assert int(right.replace(",", "")) == sum(1 for p in permutations(digits, k) if p[0] != 0)
        stem, right, _ = _q("even_numbers_count_m4", seed)
        digits = _pos(stem.split("สร้าง")[0])
        assert int(right) == sum(1 for p in permutations(digits, 3) if p[2] % 2 == 0)
        stem, right, _ = _q("handshakes_m4", seed)
        assert int(right) == comb(_pos(stem)[0], 2)
        stem, right, _ = _q("round_trip_routes_m4", seed)
        a, b = _pos(stem.split("ถนน")[1])[0], _pos(stem.split("ถนน")[2])[0]
        assert int(right) == a * b * (a - 1) * (b - 1)
        stem, right, _ = _q("side_by_side_m4", seed)
        n = _pos(stem)[0]
        assert int(right.replace(",", "")) == 2 * factorial(n - 1)


def test_probability():
    for seed in SEEDS:
        stem, right, _ = _q("exactly_k_heads_m4", seed)
        n, k = _pos(stem)[:2]
        assert _frac(right) == Fraction(comb(n, k), 2 ** n)
        stem, right, _ = _q("card_from_deck_m4", seed)
        counts = {"ไพ่โพแดง": 13, "ไพ่หน้าคน (J, Q, K)": 12, "ไพ่เอซ": 4, "ไพ่สีแดง": 26, "ไพ่หมายเลข 7": 4,
                  "ไพ่โพแดงหรือไพ่เอซ": 16, "ไพ่สีดำที่เป็นหน้าคน": 6}
        what = stem.split("จะได้")[1].split("เท่ากับ")[0]
        assert _frac(right) == Fraction(counts[what], 52)
        stem, right, _ = _q("one_of_each_m4", seed)
        b, g = _pos(stem)[:2]
        assert _frac(right) == Fraction(b * g, comb(b + g, 2))
        stem, right, _ = _q("at_least_one_head_m4", seed)
        assert _frac(right) == 1 - Fraction(1, 2 ** _pos(stem)[0])
        stem, right, _ = _q("divisible_by_both_m4", seed)
        top, a, b = _pos(stem)[2:5]
        assert _frac(right) == Fraction(sum(1 for v in range(1, top + 1) if v % a == 0 and v % b == 0), top)
        stem, right, _ = _q("together_probability_m4", seed)
        assert _frac(right) == Fraction(2, _pos(stem)[0])
        stem, right, _ = _q("dice_total_above_m4", seed)
        s = _pos(stem)[-1]
        assert _frac(right) == Fraction(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b > s), 36)


def _root_value(tex: str) -> float:
    m = re.fullmatch(r"(\d*)\\sqrt\{(\d+)\}|(\d+)", tex)
    if m.group(3):
        return float(m.group(3))
    return (int(m.group(1)) if m.group(1) else 1) * int(m.group(2)) ** 0.5


def test_radicals_and_absolute_value():
    for seed in SEEDS:
        stem, right, texts = _q("simplify_root_m4", seed)
        n = _pos(stem)[0]
        m = re.fullmatch(r"(\d*)\\sqrt\{(\d+)\}", right)
        k, inner = int(m.group(1) or 1), int(m.group(2))
        assert k * k * inner == n and all(inner % (d * d) for d in range(2, isqrt(inner) + 1))
        stem, right, texts = _q("root_product_m4", seed)
        a, b = _pos(stem)[:2]
        assert abs(_root_value(right) - (a * b) ** 0.5) < 1e-9
        stem, right, _ = _q("conjugate_product_m4", seed)
        a, b = _pos(stem)[:2]
        assert int(right) == a * a - b
        stem, right, _ = _q("abs_distance_m4", seed)
        a, b = map(int, re.search(r"\\left\|(-?\d+) - \((-?\d+)\)", stem).groups())
        assert int(right) == abs(a - b)
        stem, right, _ = _q("abs_integers_within_m4", seed)
        sign, a, b = re.search(r"\|x ([+-]) (\d+)\| \\le (\d+)", stem).groups()
        c = int(a) if sign == "-" else -int(a)
        assert int(right) == sum(1 for x in range(-100, 100) if abs(x - c) <= int(b))
        stem, right, _ = _q("abs_sum_value_m4", seed)
        a, b, c = _ints(stem.removeprefix("จงหาค่า"))
        assert int(right) == abs(a) - abs(b) + abs(c)


def test_factorising():
    for seed in SEEDS:
        for key, prompt in (("sum_of_cubes_m4", "จงแยกตัวประกอบ"), ("common_then_squares_m4", "จงแยกตัวประกอบให้สมบูรณ์"),
                            ("biquadratic_m4", "จงแยกตัวประกอบให้สมบูรณ์"), ("cubic_three_roots_m4", "จงแยกตัวประกอบให้สมบูรณ์"),
                            ("four_terms_pairs_m4", "จงแยกตัวประกอบ")):
            stem, right, texts = _q(key, seed)
            poly = stem.removeprefix(prompt)
            for t in texts:
                assert _same(poly, t) == (t == right), (key, poly, t)
        stem, right, texts = _q("cubic_factor_test_m4", seed)
        poly = stem.removeprefix("ข้อใดเป็นตัวประกอบของ")
        for t in texts:
            sign, k = re.fullmatch(r"\(x ([+-]) (\d+)\)", t).groups()
            root = -int(k) if sign == "+" else int(k)
            assert (_ev(poly, Fraction(root)) == 0) == (t == right), t
        stem, right, _ = _q("cube_sum_from_sum_product_m4", seed)
        s, p = _ints(stem.split("จงหาค่าของ")[0] if False else stem.split("x³ + y³")[1])
        assert int(right) == s ** 3 - 3 * s * p


def test_polynomial_division():
    for seed in SEEDS:
        stem, right, _ = _q("coefficient_from_remainder_m4", seed)
        poly = stem.split("P(x) = ")[1].replace("kx", f"({right})x")
        sign, a = re.search(r"\(x ([+-]) (\d+)\) ได้เศษ (-?\d+)", stem).groups()[:2]
        r = int(re.search(r"ได้เศษ (-?\d+)", stem).group(1))
        root = int(a) if sign == "-" else -int(a)
        assert _ev(poly, Fraction(root)) == r
        stem, right, _ = _q("coefficient_from_factor_m4", seed)
        poly = stem.split("เท่าใด")[1].replace("kx", f"({right})x")
        sign, a = re.search(r"ถ้า \(x ([+-]) (\d+)\)", stem).groups()
        root = int(a) if sign == "-" else -int(a)
        assert _ev(poly, Fraction(root)) == 0


def _quad_coeffs(poly: str):
    c = _ev(poly, Fraction(0))
    b = (_ev(poly, Fraction(1)) - _ev(poly, Fraction(-1))) / 2
    a = _ev(poly, Fraction(1)) - b - c
    return a, b, c


def test_discriminant():
    for seed in SEEDS:
        stem, right, _ = _q("discriminant_value_m4", seed)
        a, b, c = _quad_coeffs(stem.split(")")[1].split(" = ")[0])
        assert int(right) == b * b - 4 * a * c
        for key, op in (("k_two_real_roots_m4", "<"), ("k_no_real_roots_m4", ">")):
            stem, right, _ = _q(key, seed)
            poly = stem.split("เท่าใด")[1].split(" = ")[0]
            m = re.fullmatch(r"k ([<>]) (.+)", right)
            bound = _frac(m.group(2))
            a, b, _ = _quad_coeffs(poly.replace("k", "0"))
            assert m.group(1) == op and bound == b * b / (4 * a)
        stem, right, texts = _q("rational_roots_which_m4", seed)
        for t in texts:
            a, b, c = _quad_coeffs(t.split(" = ")[0])
            d = b * b - 4 * a * c
            assert (d >= 0 and isqrt(int(d)) ** 2 == d) == (t == right), t
        stem, right, _ = _q("tangent_to_parabola_m4", seed)
        m = _ints(stem.split("y = ")[-1])[0]
        assert m * m + 4 * int(right) == 0
        stem, right, _ = _q("touch_x_axis_m4", seed)
        a, b, _ = _quad_coeffs(stem.split("y = ")[1].replace("c", "0"))
        assert b * b == 4 * a * int(right)
        stem, right, _ = _q("repeated_root_leading_m4", seed)
        b, c = _pos(stem.split("ax^{2}")[1])[:2]
        assert b * b == 4 * int(right) * c


def test_roots_and_coefficients():
    def roots(poly):
        a, b, c = _quad_coeffs(poly)
        d = b * b - 4 * a * c
        return a, b, c, d
    for seed in SEEDS:
        stem, right, _ = _q("vieta_sum_m4", seed)
        a, b, c, _ = roots(stem.split("เท่าใด")[1].split(" = ")[0])
        assert _frac(right) == -b / a
        for key, f in (("vieta_sum_of_squares_m4", lambda s, p: s * s - 2 * p), ("vieta_sum_of_cubes_m4", lambda s, p: s ** 3 - 3 * s * p),
                       ("vieta_ratio_sum_m4", lambda s, p: (s * s - 2 * p) / p)):
            stem, right, _ = _q(key, seed)
            poly = stem.split("ของ")[-1]
            poly = re.search(r"(x\^\{2\}.*?) = 0", stem).group(1)
            a, b, c, _ = roots(poly)
            assert _frac(right) == f(-b / a, c / a), key
        stem, right, _ = _q("vieta_root_gap_m4", seed)
        a, b, c, d = roots(re.search(r"(x\^\{2\}.*?) = 0", stem).group(1))
        assert int(right) ** 2 == d
        stem, right, _ = _q("vieta_other_root_m4", seed)
        r1 = _ints(stem.split("ถ้า")[1])[0]
        p = _ints(stem.split("bx")[1].replace("+ ", "").replace("- ", "-"))[0]
        assert int(right) * r1 == p
        stem, right, texts = _q("vieta_doubled_roots_m4", seed)
        a, b, c, _ = roots(re.search(r"(x\^\{2\}.*?) = 0", stem).group(1))
        for t in texts:
            ta, tb, tc, _ = roots(t.split(" = ")[0])
            ok = ta == 1 and -tb == 2 * (-b) and tc == 4 * c
            assert ok == (t == right), t


def test_quadratic_inequalities():
    for seed in SEEDS:
        stem, right, _ = _q("qineq_between_roots_m4", seed)
        poly = stem.removeprefix("จงหาคำตอบของอสมการ").split(r" \le 0")[0]
        sols = [x for x in range(-30, 31) if _ev(poly, Fraction(x)) <= 0]
        lo, hi = map(int, re.fullmatch(r"(-?\d+) \\le x \\le (-?\d+)", right).groups())
        assert sols == list(range(lo, hi + 1))
        stem, right, _ = _q("qineq_integer_count_m4", seed)
        poly = stem.split("นี้")[1].split(" < 0")[0]
        assert int(right) == sum(1 for x in range(-30, 31) if _ev(poly, Fraction(x)) < 0)
        stem, right, _ = _q("qineq_always_positive_m4", seed)
        a, b, _ = _quad_coeffs(stem.split("x เมื่อ k มีค่าเท่าใด")[1].split(" > 0")[0].replace("k", "0"))
        assert right == f"k > {int(b * b / 4)}"


def test_rational():
    for seed in SEEDS:
        stem, right, _ = _q("rational_simple_m4", seed)
        a, sign, b, c = re.search(r"\\frac\{(-?\d+)\}\{x ([+-]) (\d+)\} = (-?\d+)", stem).groups()
        x = _ints(right)[0]
        shift = int(b) if sign == "-" else -int(b)
        assert Fraction(int(a), x - shift) == int(c)
        stem, right, _ = _q("rational_cross_m4", seed)
        nums = re.findall(r"\\frac\{(\d+)\}\{(x[^}]*)\}", stem)
        x = Fraction(_ints(right)[0])
        (a, l1), (c, l2) = nums
        assert Fraction(int(a)) / _ev(l1, x) == Fraction(int(c)) / _ev(l2, x)
        stem, right, _ = _q("unit_fraction_sum_m4", seed)
        k = int(re.search(r"\\frac\{1\}\{(\d+)x\}", stem).group(1))
        rhs = _frac(stem.split("= ")[1])
        x = _ints(right)[0]
        assert Fraction(1, x) + Fraction(1, k * x) == rhs
        stem, right, texts = _q("rational_excluded_value_m4", seed)
        sign, a = re.search(r"\}\{x ([+-]) (\d+)\}", stem).groups()
        pole = int(a) if sign == "-" else -int(a)
        assert int(right) == pole and [int(t) == pole for t in texts].count(True) == 1
        stem, right, _ = _q("quotient_positive_m4", seed)
        lo, hi = map(int, re.fullmatch(r"x < (-?\d+) \\lor x > (-?\d+)", right).groups())
        top, bottom = re.search(r"\\frac\{(.+?)\}\{(.+?)\} > 0", stem).groups()
        sols = [x for x in range(-30, 31) if _ev(bottom, Fraction(x)) != 0 and _ev(top, Fraction(x)) / _ev(bottom, Fraction(x)) > 0]
        assert sols == [x for x in range(-30, 31) if x < lo or x > hi]
        stem, right, _ = _q("work_together_m4", seed)
        a, b = _pos(stem)[:2]
        assert Fraction(int(right)) == Fraction(a * b, a + b)


def test_functions():
    for seed in SEEDS:
        stem, right, _ = _q("quadratic_function_value_m4", seed)
        k = int(re.search(r"f\((-?\d+)\)", stem).group(1))
        poly = stem.split("f(x) = ")[1]
        assert int(right) == _ev(poly, Fraction(k))
        stem, right, _ = _q("inverse_point_m4", seed)
        a, b = _ints(stem)[:2]
        assert _ints(right) == [b, a]
        stem, right, _ = _q("inverse_scaled_shift_m4", seed)
        num, b = re.search(r"\\frac\{(.+?)\}\{(\d+)\}", stem).groups()
        inv = right.split(" = ")[1]
        assert all(_ev(num, _ev(inv, Fraction(x))) / int(b) == x for x in range(-3, 4))
        stem, right, texts = _q("even_function_m4", seed)
        for t in texts:
            f = t.split(" = ")[1]
            even = all(_ev(f, Fraction(x)) == _ev(f, Fraction(-x)) for x in range(1, 5))
            assert even == (t == right), t
        stem, right, _ = _q("reflected_point_m4", seed)
        a, b = _ints(stem)[:2]
        assert _ints(right) == ([a, -b] if "−f(x)" in stem else [-a, b])
        stem, right, _ = _q("stretched_point_m4", seed)
        a, b = _ints(stem)[:2]
        k = _pos(stem.split("y = ")[-1])[0]
        assert _ints(right) == [a, k * b]
        stem, right, _ = _q("inverse_cubic_value_m4", seed)
        poly = stem.split("f(x) = ")[1].split("จง")[0]
        y = _ints(stem.split("f⁻¹(")[1])[0]
        assert _ev(poly, Fraction(int(right))) == y


def test_composite():
    for seed in SEEDS:
        stem, right, _ = _q("composite_quadratic_value_m4", seed)
        f, g = re.search(r"f\(x\) = (.+?), \\quad g\(x\) = (.+)$", stem).groups()
        k = _ints(stem.split("∘ g)(")[1])[0]
        assert int(right) == _ev(f, _ev(g, Fraction(k)))
        stem, right, texts = _q("self_composite_m4", seed)
        f = stem.split("f(x) = ")[1].split("จง")[0]
        for t in texts:
            ff = t.split(" = ")[1]
            ok = all(_ev(ff, Fraction(x)) == _ev(f, _ev(f, Fraction(x))) for x in range(-3, 4))
            assert ok == (t == right), t
        stem, right, _ = _q("composite_from_tables_m4", seed)
        rows = {line.split(" | ")[0]: _ints(" ".join(line.split(" | ")[1:])) for line in stem.split("\n") if " | " in line}
        k = _ints(stem.split("f(g(")[1])[0]
        f, g = dict(zip(rows["x"], rows["f(x)"])), dict(zip(rows["x"], rows["g(x)"]))
        assert int(right) == f[g[k]]


def test_quadratic():
    for seed in SEEDS:
        stem, right, _ = _q("max_area_fence_m4", seed)
        fence = _pos(stem)[0]
        assert int(right) == max(w * (fence // 2 - w) for w in range(fence // 2 + 1))
        stem, right, _ = _q("max_area_wall_m4", seed)
        fence = _pos(stem)[0]
        assert int(right) == max(w * (fence - 2 * w) for w in range(fence // 2 + 1))
        stem, right, _ = _q("max_product_fixed_sum_m4", seed)
        s = _pos(stem)[0]
        assert int(right) == (s // 2) ** 2
        stem, right, _ = _q("argmin_quadratic_m4", seed)
        poly = stem.split("f(x) = ")[1].split("f มี")[0]
        vals = {x: _ev(poly, Fraction(x)) for x in range(-20, 21)}
        assert int(right) == min(vals, key=vals.get)


def test_exponential():
    for seed in SEEDS:
        stem, right, _ = _q("exp_equal_exponents_m4", seed)
        m = re.search(r"(\d)\^\{(.+?)\} = \d\^\{(-?\d+)\}", stem)
        assert _ev(m.group(2), _frac(right.split(" = ")[1])) == int(m.group(3))
        stem, right, _ = _q("exponent_from_laws_m4", seed)
        m, n, k = _pos(stem)[1:4]
        assert int(right) == m * n - k
        stem, right, _ = _q("doubling_growth_m4", seed)
        start, h, t = _pos(stem)[:3]
        assert int(right.replace(",", "")) == start * 2 ** (t // h)
        stem, right, _ = _q("exp_inequality_m4", seed)
        k = _pos(stem.split(">")[-1])
        if "frac{1}{2}" in stem:
            assert right == f"x < {isqrt(k[-1]) and int.bit_length(k[-1]) - 1}"
        else:
            assert right == f"x > {int.bit_length(k[0]) - 1}"
        stem, right, _ = _q("exp_with_coefficient_m4", seed)
        a, base, total = _pos(stem.split("แก้สมการ")[1])[:3]
        assert a * base ** _ints(right)[0] == total
        stem, right, _ = _q("sum_of_equal_powers_m4", seed)
        base = _pos(stem.split("แก้สมการ")[1])[0]
        k = _pos(stem.split("=")[1])[1]
        x = _ints(right)[0]
        assert base * base ** x == base ** k


def test_distance():
    for seed in SEEDS:
        stem, right, _ = _q("endpoint_from_midpoint_m4", seed)
        ax, ay, mx, my = _ints(stem.split("จงหาพิกัดของจุด B")[1])
        assert _point(right) == (2 * mx - ax, 2 * my - ay)
        stem, right, _ = _q("axis_triangle_perimeter_m4", seed)
        a, b = _pos(stem)[2], _pos(stem)[5]
        assert int(right) == a + b + isqrt(a * a + b * b) and isqrt(a * a + b * b) ** 2 == a * a + b * b
        stem, right, _ = _q("equidistant_on_axis_m4", seed)
        a, b, c, d = _ints(stem.split("จุด P คือจุดใด")[1])
        x, y = _point(right)
        assert y == 0 and (x - a) ** 2 + b * b == (x - c) ** 2 + d * d
        stem, right, _ = _q("coordinate_from_distance_m4", seed)
        x0, y0, y1, dist = _ints(stem.split("เท่าใด")[1].replace("k", ""))
        k = int(right)
        assert (k - x0) ** 2 + (y1 - y0) ** 2 == dist * dist and k > x0
        stem, right, _ = _q("centroid_m4", seed)
        v = _ints(stem.split("ดังนี้")[1])
        assert _point(right) == (Fraction(v[0] + v[2] + v[4], 3), Fraction(v[1] + v[3] + v[5], 3))
        stem, right, _ = _q("rectangle_diagonal_coords_m4", seed)
        x0, y0, x1, y1 = _ints(stem)[:4]
        assert int(right) ** 2 == (x1 - x0) ** 2 + (y1 - y0) ** 2
        stem, right, _ = _q("coordinate_from_midpoint_m4", seed)
        body = stem.split("เท่าใด")[1]
        a = _ints(body.split("A(")[1])[0]
        y2 = _ints(body.split("B(")[1])[1]
        my = _point("(" + body.split("M(")[1].rsplit(")", 1)[0] + ")")[1]
        assert Fraction(int(right) + y2, 2) == my


def test_lines():
    for seed in SEEDS:
        stem, right, texts = _q("slope_intercept_form_m4", seed)
        lhs, c = stem.removeprefix("เขียนสมการนี้ในรูป y = mx + c").split(" = ")
        rhs = right.split("y = ")[1]
        for xv in range(-3, 4):
            yv = _line_eval(rhs, Fraction(xv))
            assert _ev(lhs, Fraction(xv), yv) == int(c)
        stem, right, _ = _q("parallel_through_point_m4", seed)
        m = _ints(stem.split("y = ")[1])[0] if not stem.split("y = ")[1].startswith(("x", "-x")) else (1 if stem.split("y = ")[1].startswith("x") else -1)
        p, q = _ints(stem.split("P(")[1])[:2]
        rhs = right.split("y = ")[1]
        assert _line_eval(rhs, Fraction(p)) == q and _line_eval(rhs, Fraction(p + 1)) - _line_eval(rhs, Fraction(p)) == m
        stem, right, _ = _q("perpendicular_through_point_m4", seed)
        p, q = _ints(stem.split("P(")[1])[:2]
        rhs = right.split("y = ")[1]
        given = stem.split("y = ")[1].split(",")[0]
        m = _line_eval(given, Fraction(1)) - _line_eval(given, Fraction(0))
        assert _line_eval(rhs, Fraction(p)) == q and (_line_eval(rhs, Fraction(1)) - _line_eval(rhs, Fraction(0))) * m == -1
        stem, right, _ = _q("lines_meet_m4", seed)
        l1, l2 = stem.removeprefix("เส้นตรงสองเส้นนี้ตัดกันที่จุดใด").split(r", \;\; ")
        x, y = _point(right)
        assert _line_eval(l1.split("y = ")[1], x) == y == _line_eval(l2.split("y = ")[1], x)
        stem, right, _ = _q("x_intercept_point_slope_m4", seed)
        p, q, m = _ints(stem.split("จุดใด")[1])
        x, y = _point(right)
        assert y == 0 and q + m * (x - p) == 0


def test_analytic_geometry():
    for seed in SEEDS:
        stem, right, _ = _q("collinear_k_m4", seed)
        _, a, _, b, d = _ints(stem.split("เท่าใด")[1].replace("k", ""))
        assert int(right) == a + (b - a) * d
        stem, right, _ = _q("parallelogram_area_coords_m4", seed)
        a, c = _pos(stem)[2], _pos(stem)[5]
        assert int(right) == a * c
        stem, right, _ = _q("slope_from_intercepts_m4", seed)
        a, b = _ints(stem.split("เท่าใด")[1])[0], _ints(stem.split("เท่าใด")[1])[3]
        assert _frac(right) == Fraction(-b, a)
        stem, right, _ = _q("parallel_lines_k_m4", seed)
        a, b = (int(v or 1) for v in re.search(r"(\d*)x \+ (\d*)y = ", stem).groups())
        assert Fraction(a, b) == Fraction(6, int(right))
        stem, right, _ = _q("perpendicular_lines_k_m4", seed)
        given = stem.split("y = ")[1].split(",")[0]
        m = _line_eval(given, Fraction(1)) - _line_eval(given, Fraction(0))
        assert _frac(right) * m == -1
        _q("slope_angle_m4", seed)


def test_circles():
    def centre_r2(general: str):
        lhs = general.split(" = ")[0]
        f = lambda x, y: _ev(lhs, Fraction(x), Fraction(y))
        d = (f(1, 0) - f(-1, 0)) / 2
        e = (f(0, 1) - f(0, -1)) / 2
        h, k = -d / 2, -e / 2
        return h, k, h * h + k * k - f(0, 0)
    for seed in SEEDS:
        stem, right, _ = _q("circle_centre_general_m4", seed)
        h, k, _ = centre_r2(stem.removeprefix("วงกลมนี้มีจุดศูนย์กลางที่จุดใด"))
        assert _point(right) == (h, k)
        stem, right, _ = _q("circle_radius_general_m4", seed)
        _, _, r2 = centre_r2(stem.removeprefix("วงกลมนี้มีรัศมียาวกี่หน่วย"))
        assert int(right) ** 2 == r2
        stem, right, _ = _q("point_vs_circle_m4", seed)
        x, y = _ints(stem.split("(")[1].split(")")[0])
        eq = stem.split("วงกลม")[1]
        lhs, r2 = eq.split(" = ")
        v = _ev(lhs, Fraction(x), Fraction(y))
        assert right == ("อยู่ภายในวงกลม" if v < int(r2) else "อยู่บนวงกลม" if v == int(r2) else "อยู่ภายนอกวงกลม")
        stem, right, _ = _q("circle_from_diameter_m4", seed)
        a, b = stem.split("คือข้อใด")[1].split(r", \; ")
        (ax, ay), (bx, by) = _point(a[1:]), _point(b[1:])
        lhs, r2 = right.split(" = ")
        assert _ev(lhs, ax, ay) == int(r2) == _ev(lhs, bx, by)
        assert _ev(lhs, (ax + bx) / 2, (ay + by) / 2) == 0
        stem, right, _ = _q("circle_touching_x_axis_m4", seed)
        h, k = _ints(stem.split("C(")[1])[:2]
        lhs, r2 = right.split(" = ")
        assert _ev(lhs, Fraction(h), Fraction(k)) == 0 and int(r2) == k * k


def test_finding_parabolas():
    for seed in SEEDS:
        stem, right, _ = _q("parabola_a_from_point_m4", seed)
        h, k, x, y = _ints(stem.split("เท่าใด")[1])
        assert Fraction(int(right)) * (x - h) ** 2 + k == y
        stem, right, _ = _q("parabola_y_intercept_vertex_m4", seed)
        expr = stem.split("y = ")[1]
        assert int(right) == _ev(expr, Fraction(0))
        stem, right, _ = _q("vertex_from_roots_m4", seed)
        expr = stem.split("y = ")[1]
        h, k = _point(right)
        assert _ev(expr, h) == k and _ev(expr, h + 1) == _ev(expr, h - 1)
        stem, right, _ = _q("b_from_three_points_m4", seed)
        y1, y0, y2 = _ints(stem.split("เท่าใด")[1])[1::2]
        assert Fraction(int(right)) == Fraction(y2 - y1, 2)
        stem, right, _ = _q("axis_from_equal_heights_m4", seed)
        p, y, q, _ = _ints(stem.split("เส้นใด")[1])
        assert right == f"x = {(p + q) // 2}"
        stem, right, _ = _q("max_from_roots_m4", seed)
        expr = stem.split("y = -")[1]
        assert int(right) == max(-_ev(expr, Fraction(x, 2)) for x in range(-40, 41))
        stem, right, texts = _q("equation_from_vertex_m4", seed)
        h, k = _ints(stem.split("V(")[-1])[:2]
        expr = right.split("y = ")[1]
        assert _ev(expr, Fraction(h)) == k and _ev(expr, Fraction(h + 1)) == _ev(expr, Fraction(h - 1))


def test_conics():
    for seed in SEEDS:
        stem, right, _ = _q("parabola_focus_m4", seed)
        four_p = _ints(stem.split("= ")[1])[0]
        assert _point(right) == ((Fraction(four_p, 4), 0) if stem.lstrip("โฟกัสของพาราโบลานี้คือจุดใด").startswith("y") else (0, Fraction(four_p, 4)))
        stem, right, _ = _q("ellipse_major_axis_m4", seed)
        a2, b2 = _pos(stem.split("ยาวกี่หน่วย")[1])[1::2][:2]
        assert int(right) == 2 * isqrt(max(a2, b2))
        stem, right, _ = _q("hyperbola_asymptote_m4", seed)
        a2, b2 = _pos(stem.split("ข้อใด")[1])[1::2][:2]
        assert right == rf"y = \pm {frac_tex(Fraction(isqrt(b2), isqrt(a2)))}x"
        stem, right, _ = _q("conic_type_m4", seed)
        eq = stem.split("ชนิดใด")[1]
        if eq.startswith(("y =", "x =")):
            want = "พาราโบลา"
        elif " - " in eq:
            want = "ไฮเพอร์โบลา"
        else:
            a, b = _pos(eq)[0], _pos(eq)[2]
            want = "วงกลม" if a == b else "วงรี"
        assert right == want
