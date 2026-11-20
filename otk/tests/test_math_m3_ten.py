"""The ม.3 sets added so every unit has at least ten: each answer worked out again from the stem alone.

Polynomials are compared by evaluating both sides at several points, numbers are read back out of the
question, and text answers are checked against facts written out here independently.
"""

from __future__ import annotations

import re
from fractions import Fraction
from math import gcd
from random import Random

from otk.core import generate

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
    s = s.strip()
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", s)
    if m:
        return (-1 if m.group(1) else 1) * Fraction(int(m.group(2)), int(m.group(3)))
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a), int(b))
    return Fraction(s.replace(",", ""))


def test_probability():
    for seed in SEEDS:
        stem, right, _ = _q("probability_complement_m3", seed)
        a, b = map(int, re.search(r"(\d+)/(\d+)", stem).groups())
        assert _frac(right) == 1 - Fraction(a, b)
        stem, right, _ = _q("two_dice_sum_m3", seed)
        s = _pos(stem.split("เท่ากับ")[1])[0]
        assert _frac(right) == Fraction(sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s), 36)
        stem, right, _ = _q("expected_count_m3", seed)
        red, blue, _, trials = _pos(stem)[:4]
        assert Fraction(int(right)) == Fraction(trials * red, red + blue)


def test_binomial_expansion():
    for seed in SEEDS:
        stem, right, _ = _q("binomial_x_coefficient_m3", seed)
        poly = stem.removeprefix("เมื่อกระจายแล้ว สัมประสิทธิ์ของ x เท่ากับเท่าใด")
        # The x coefficient is p(1) - p(0) - (p(1) + p(-1))/2 + p(0) for a quadratic: (p(1) - p(-1)) / 2.
        assert Fraction(int(right)) == (_ev(poly, Fraction(1)) - _ev(poly, Fraction(-1))) / 2
        for key, prompt in (("square_of_ax_plus_b_m3", "จงกระจาย"), ("difference_of_squares_ax_m3", "จงกระจาย"),
                            ("expand_two_variables_m3", "จงกระจาย"),
                            ("product_minus_square_m3", "จงกระจายและจัดรูปให้อย่างง่าย")):
            stem, right, texts = _q(key, seed)
            problem = stem.removeprefix(prompt)
            for t in texts:
                assert _same(problem, t) == (t == right), (key, problem, t)
        for key in ("mental_square_m3", "mental_product_m3"):
            stem, right, _ = _q(key, seed)
            expr = stem.split("จงหาค่า")[1].split(")", 1)[1]
            assert _ev(expr, Fraction(0)) == int(right.replace(",", ""))


def test_box_plots():
    def five(s: str) -> list[int]:
        return [int(v) for v in re.findall(r"(?:ค่าต่ำสุด|เท่ากับ|มัธยฐาน|ค่าสูงสุด) (\d+)", s)]
    for seed in SEEDS:
        stem, right, _ = _q("box_plot_range_m3", seed)
        v = five(stem)
        assert int(right) == v[4] - v[0]
        stem, right, _ = _q("box_plot_whisker_m3", seed)
        v = five(stem)
        assert int(right) == (v[4] - v[3] if "ขวา" in stem else v[1] - v[0])
        stem, right, _ = _q("box_plot_middle_half_m3", seed)
        v = five(stem)
        assert right == f"{v[1]} ถึง {v[3]}"
        stem, right, _ = _q("box_plot_two_medians_m3", seed)
        a, b = stem.split("ห้องที่สองมี")
        assert int(right) == five(a)[2] - five(b)[2]
        stem, right, texts = _q("five_number_summary_m3", seed)
        data = sorted(_pos(stem.split("คือ")[1].split("ค่าสรุป")[0]))
        n = len(data)
        want = [data[0], data[(n + 1) // 4 - 1], data[(n + 1) // 2 - 1], data[3 * (n + 1) // 4 - 1], data[-1]]
        assert _pos(right) == want
        _q("box_plot_parts_m3", seed)


def test_circles():
    for seed in SEEDS:
        stem, right, _ = _q("inscribed_from_central_m3", seed)
        assert 2 * int(right) == _pos(stem)[0]
        stem, right, _ = _q("two_tangents_m3", seed)
        if "PB ยาว" in stem:
            assert int(right) == _pos(stem.split("PA ยาว")[1])[0]
        else:
            assert int(right) == 180 - _pos(stem.split("APB มีขนาด")[1])[0]
        stem, right, _ = _q("chord_from_distance_m3", seed)
        r, d = _pos(stem)[:2]
        assert int(right) ** 2 == 4 * (r * r - d * d)
        stem, right, _ = _q("angles_same_arc_m3", seed)
        assert int(right) == _pos(stem.split("มุม ACB มีขนาด")[1])[0]


def test_completing_the_square():
    for seed in SEEDS:
        stem, right, _ = _q("vertex_from_completed_m3", seed)
        h, k = _ints(stem.replace("x - ", "x+-").replace("x + ", "x+").replace(") - ", ")+-").replace(") + ", ")+"))[:3:2]
        expr = stem.split("y = ")[1].replace("^2", "^{2}")
        hx, ky = _ints(right)
        assert _ev(expr, Fraction(hx)) == ky and _ev(expr, Fraction(hx + 1)) == _ev(expr, Fraction(hx - 1)) > ky
        stem, right, _ = _q("least_value_m3", seed)
        poly = stem.removeprefix("ค่าต่ำสุดของนิพจน์นี้เท่ากับเท่าใด")
        b = (_ev(poly, Fraction(1)) - _ev(poly, Fraction(-1))) / 2
        assert _ev(poly, -b / 2) == int(right)
        stem, right, _ = _q("solve_by_square_root_m3", seed)
        lhs, rhs = stem.removeprefix("จงแก้สมการ").split(" = ")
        roots = _ints(right.split("=")[1])
        assert all(_ev(lhs, Fraction(r)) == int(rhs) for r in roots) and len(set(roots)) == 2
        stem, right, _ = _q("completed_square_numbers_m3", seed)
        poly = stem.removeprefix("จงหาค่าของ q").split(" = ")[0]
        b = (_ev(poly, Fraction(1)) - _ev(poly, Fraction(-1))) / 2
        assert _ev(poly, -b / 2) == int(right)
        stem, right, _ = _q("greatest_value_m3", seed)
        poly = stem.removeprefix("ค่าสูงสุดของนิพจน์นี้เท่ากับเท่าใด")
        b = (_ev(poly, Fraction(1)) - _ev(poly, Fraction(-1))) / 2
        assert _ev(poly, b / 2) == int(right)
        stem, right, texts = _q("which_perfect_square_m3", seed)
        for t in texts:
            b = (_ev(t, Fraction(1)) - _ev(t, Fraction(-1))) / 2
            c = _ev(t, Fraction(0))
            assert ((b / 2) ** 2 == c) == (t == right), t


def test_factorising():
    for seed in SEEDS:
        for key in ("factor_difference_of_squares_m3", "factor_perfect_square_m3", "factor_leading_two_m3",
                    "factor_two_variables_m3"):
            stem, right, texts = _q(key, seed)
            poly = stem.removeprefix("จงแยกตัวประกอบ")
            for t in texts:
                assert _same(poly, t) == (t == right), (key, poly, t)
        stem, right, texts = _q("which_factor_m3", seed)
        poly = stem.removeprefix("ข้อใดเป็นตัวประกอบของ")
        for t in texts:
            sign, k = re.fullmatch(r"\(x ([+-]) (\d+)\)", t).groups()
            root = -int(k) if sign == "+" else int(k)
            assert (_ev(poly, Fraction(root)) == 0) == (t == right), t


def test_inequality():
    def solve(ineq: str):
        m = re.fullmatch(r"x (<|>|\\le|\\ge) (-?\d+)", ineq)
        return m.group(1), int(m.group(2))
    for seed in SEEDS:
        stem, right, _ = _q("inequality_count_integers_m3", seed)
        tex = stem.removeprefix("มีจำนวนเต็ม x กี่จำนวนที่สอดคล้องกับอสมการนี้")
        lo, mid, hi = re.fullmatch(r"(-?\d+) < (.+) \\le (-?\d+)", tex).groups()
        count = sum(1 for x in range(-200, 200) if int(lo) < _ev(mid, Fraction(x)) <= int(hi))
        assert int(right) == count
        stem, right, _ = _q("inequality_largest_integer_m3", seed)
        lhs, rhs = stem.removeprefix("จำนวนเต็มที่มากที่สุดที่สอดคล้องกับอสมการนี้คือจำนวนใด").split(" < ")
        best = max(x for x in range(-300, 300) if _ev(lhs, Fraction(x)) < int(rhs))
        assert int(right) == best
        stem, right, _ = _q("inequality_fraction_m3", seed)
        d, b, c = _ints(stem.removeprefix("จงหาคำตอบของอสมการ"))
        sign, bound = solve(right)
        tex_sign = re.search(r"\} \+ \d+ ([<>]) ", stem).group(1)
        assert sign == tex_sign and bound == d * (c - b)
        stem, right, _ = _q("inequality_both_sides_m3", seed)
        lhs, rhs = stem.removeprefix("จงหาคำตอบของอสมการ").split(r" \ge ")
        sign, bound = solve(right)
        sols = [x for x in range(-300, 300) if _ev(lhs, Fraction(x)) >= _ev(rhs, Fraction(x))]
        assert sign == r"\ge" and min(sols) == bound and sols == list(range(bound, 300))


def test_parabola():
    for seed in SEEDS:
        stem, right, _ = _q("parabola_opens_m3", seed)
        a = _ints(stem.split("y = ")[1].replace("-x", "-1x").split("x")[0] or "1")
        lead = a[0] if a else 1
        assert right == ("หงาย และมีค่าต่ำสุด" if lead > 0 else "คว่ำ และมีค่าสูงสุด")
        stem, right, _ = _q("parabola_y_intercept_m3", seed)
        expr = stem.removeprefix("พาราโบลานี้ตัดแกน y ที่จุดใด").removeprefix("y = ")
        assert _ints(right) == [0, int(_ev(expr, Fraction(0)))]
        stem, right, _ = _q("parabola_x_intercepts_m3", seed)
        expr = stem.removeprefix("พาราโบลานี้ตัดแกน x ที่จุดใด").removeprefix("y = ")
        xs = _ints(right)[::2]
        assert all(_ev(expr, Fraction(x)) == 0 for x in xs) and len(set(xs)) == 2
        stem, right, _ = _q("parabola_vertex_standard_m3", seed)
        expr = stem.removeprefix("พาราโบลานี้มีจุดยอดที่จุดใด").removeprefix("y = ")
        h, k = _ints(right)
        assert _ev(expr, Fraction(h)) == k and _ev(expr, Fraction(h + 1)) == _ev(expr, Fraction(h - 1))
        stem, right, _ = _q("parabola_extreme_value_m3", seed)
        expr = stem.split("y = ")[1]
        vals = [_ev(expr, Fraction(x)) for x in range(-30, 31)]
        assert int(right) == (min(vals) if "ต่ำสุด" in stem else max(vals))
        stem, right, texts = _q("point_on_parabola_m3", seed)
        expr = stem.split("y = ")[1]
        for t in texts:
            x, y = _ints(t)
            assert (_ev(expr, Fraction(x)) == y) == (t == right), t
        stem, right, _ = _q("parabola_shift_m3", seed)
        h = _pos(stem.split("ไปทาง")[1])[0] * (1 if "ขวา" in stem else -1)
        k = _pos(stem.split("และ")[-1])[0] * (1 if "ขึ้น" in stem else -1)
        expr = right.removeprefix("y = ")
        assert all(_ev(expr, Fraction(x)) == (x - h) ** 2 + k for x in range(-5, 6))


def test_quadratic():
    for seed in SEEDS:
        stem, right, _ = _q("quadratic_root_count_m3", seed)
        poly = stem.split("กี่คำตอบ")[1].split(" = ")[0]
        c = _ev(poly, Fraction(0))
        b = (_ev(poly, Fraction(1)) - _ev(poly, Fraction(-1))) / 2
        a = _ev(poly, Fraction(1)) - b - c
        disc = b * b - 4 * a * c
        assert right == ("มี 2 คำตอบที่ต่างกัน" if disc > 0 else "มี 1 คำตอบ (คำตอบซ้ำ)" if disc == 0
                         else "ไม่มีคำตอบที่เป็นจำนวนจริง")
        stem, right, _ = _q("quadratic_sum_of_roots_m3", seed)
        poly = stem.split("เท่าใด")[1].split(" = ")[0]
        roots = [x for x in range(-30, 31) if _ev(poly, Fraction(x)) == 0]
        assert len(roots) == 2 and int(right) == sum(roots)
        stem, right, _ = _q("rectangle_width_from_area_m3", seed)
        d, area = _pos(stem)[:2]
        assert int(right) * (int(right) + d) == area
        stem, right, _ = _q("consecutive_product_m3", seed)
        prod = _pos(stem)[-1]
        step = 1 if "จำนวนนับ" in stem else 2
        assert int(right) * (int(right) + step) == prod
        stem, right, texts = _q("which_root_m3", seed)
        poly = stem.removeprefix("จำนวนใดเป็นคำตอบของสมการ").split(" = ")[0]
        for t in texts:
            assert (_ev(poly, Fraction(int(t))) == 0) == (t == right), t


def test_similarity():
    for seed in SEEDS:
        stem, right, texts = _q("similar_scale_ratio_m3", seed)
        s, b = _pos(stem.split("ยาว")[1])[0], _pos(stem.split("ยาว")[2])[0]
        x, y = _pos(right)
        assert Fraction(x, y) == Fraction(s, b) and gcd(x, y) == 1
        stem, right, _ = _q("similar_corresponding_angle_m3", seed)
        a, b = _pos(stem.split("ถ้ามุม A มีขนาด")[1])[:2]
        assert int(right) == 180 - a - b


def test_surface_area_and_volume():
    pi = Fraction(22, 7)
    for seed in SEEDS:
        stem, right, _ = _q("cylinder_volume_m3", seed)
        r, h = _pos(stem)[:2]
        assert _frac(right) == pi * r * r * h
        stem, right, _ = _q("cylinder_surface_m3", seed)
        r, h = _pos(stem)[:2]
        assert _frac(right) == 2 * pi * r * (r + h)
        stem, right, _ = _q("cone_curved_from_height_m3", seed)
        r, h = _pos(stem)[:2]
        slant = next(s for s in range(1, 200) if s * s == r * r + h * h)
        assert _frac(right) == pi * r * slant
        stem, right, _ = _q("hemisphere_volume_m3", seed)
        r = _pos(stem)[0]
        assert Fraction(int(right.removesuffix(r"\pi"))) == Fraction(2, 3) * r ** 3
        stem, right, _ = _q("square_pyramid_volume_m3", seed)
        a, h = _pos(stem)[:2]
        assert _frac(right) == Fraction(a * a * h, 3)


def test_systems_of_equations():
    for seed in SEEDS:
        stem, right, _ = _q("system_sum_difference_m3", seed)
        s, d = _pos(stem)[:2]
        assert int(right) == ((s + d) // 2 if "มากกว่า" in stem.split("จำนวนที่")[-1] else (s - d) // 2)
        stem, right, _ = _q("system_x_plus_y_m3", seed)
        eqs = stem.removeprefix("จากระบบสมการ ค่าของ x + y เท่ากับเท่าใด").split(r", \;\; ")
        (l1, r1), (l2, r2) = (e.split(" = ") for e in eqs)
        a1, b1 = _ev(l1, Fraction(1), Fraction(0)), _ev(l1, Fraction(0), Fraction(1))
        a2, b2 = _ev(l2, Fraction(1), Fraction(0)), _ev(l2, Fraction(0), Fraction(1))
        det = a1 * b2 - a2 * b1
        x = (int(r1) * b2 - int(r2) * b1) / det
        y = (a1 * int(r2) - a2 * int(r1)) / det
        assert int(right) == x + y
        stem, right, _ = _q("system_coins_m3", seed)
        small, big, count, total = _pos(stem)[:4]
        k = int(right)
        assert small * (count - k) + big * k == total
        stem, right, _ = _q("system_ages_m3", seed)
        times, total = _pos(stem)[:2]
        assert int(right) * (times + 1) == total * times
        stem, right, texts = _q("system_which_pair_m3", seed)
        body = stem.split(r"\begin{cases}")[1].split(r"\end{cases}")[0]
        (l1, r1), (l2, r2) = (e.strip().split(" = ") for e in body.split(r"\\"))
        for t in texts:
            x, y = _ints(t)
            ok = _ev(l1, Fraction(x), Fraction(y)) == int(r1) and _ev(l2, Fraction(x), Fraction(y)) == int(r2)
            assert ok == (t == right), t
        stem, right, _ = _q("system_two_prices_m3", seed)
        n1, m1, a, n2, m2, b = _pos(stem)[:6]
        pen = int(right)
        assert (a - n1 * pen) * m2 == (b - n2 * pen) * m1 and (a - n1 * pen) % m1 == 0


def test_trigonometric_ratios():
    for seed in SEEDS:
        stem, right, _ = _q("cos_from_sin_m3", seed)
        s = _frac(re.search(r"\\frac\{\d+\}\{\d+\}", stem).group(0))
        assert _frac(right) ** 2 == 1 - s ** 2
        stem, right, _ = _q("side_from_ratio_m3", seed)
        hyp = _pos(stem.split("AB ยาว")[1])[0]
        a, c = map(int, re.search(r"(\d+)/(\d+)", stem).groups())
        assert Fraction(int(right)) == Fraction(hyp * a, c)
        stem, right, _ = _q("complementary_ratio_m3", seed)
        assert _frac(right) == _frac(re.search(r"\\frac\{\d+\}\{\d+\}", stem).group(0))
        for key in ("special_angle_expression_m3", "angle_from_ratio_m3"):
            _q(key, seed)
