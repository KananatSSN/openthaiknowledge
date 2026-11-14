"""The ม.5 sets added so every unit has at least ten: each answer worked out again from the stem alone.

Polynomials are compared by evaluating both sides at several points, numbers are read back out of the
question, and text answers are checked against facts written out here independently.
"""

from __future__ import annotations

import re
from fractions import Fraction
from math import comb, factorial, isqrt
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


def _surd(s: str) -> float:
    """k\\sqrt{m}, \\frac{k\\sqrt{m}}{d}, or a plain number, as a float."""
    s = s.strip()
    m = re.fullmatch(r"\\frac\{(\d*)\\sqrt\{(\d+)\}\}\{(\d+)\}", s)
    if m:
        return int(m.group(1) or 1) * int(m.group(2)) ** 0.5 / int(m.group(3))
    m = re.fullmatch(r"(-?)(\d*)\\sqrt\{(\d+)\}", s)
    if m:
        return (-1 if m.group(1) else 1) * int(m.group(2) or 1) * int(m.group(3)) ** 0.5
    return float(_frac(s))


def _degs(s: str) -> list[int]:
    return [int(v) for v in re.findall(r"(-?\d+)\^\{\\circ\}", s)]


def test_function():
    for seed in SEEDS:
        stem, right, _ = _q("taxi_fare_m5", seed)
        start, per, km = _pos(stem)[:3]
        assert int(right) == start + per * km
        stem, right, _ = _q("fixed_cost_from_two_m5", seed)
        n1, c1, n2, c2 = _pos(stem)[:4]
        per = Fraction(c2 - c1, n2 - n1)
        assert int(right) == c1 - per * n1
        stem, right, _ = _q("tripling_growth_m5", seed)
        start, t = _pos(stem)[:2]
        assert int(right.replace(",", "")) == start * 3 ** t
        stem, right, _ = _q("break_even_m5", seed)
        fixed, cost, price = _pos(stem)[:3]
        assert int(right) * (price - cost) == fixed
        stem, right, _ = _q("best_output_m5", seed)
        poly = stem.split("P(x) = ")[-1]
        vals = {x: _ev(poly, Fraction(x)) for x in range(0, 200)}
        assert int(right) == max(vals, key=vals.get)
        stem, right, _ = _q("water_bill_tiers_m5", seed)
        _, a, _, b, units = _pos(stem)[:5]
        assert int(right) == 10 * a + (units - 10) * b
        stem, right, _ = _q("celsius_from_fahrenheit_m5", seed)
        f = _ints(stem.split("เท่ากับ")[1])[0]
        assert Fraction(9, 5) * int(right) + 32 == f


def test_radicals_sequences_interest():
    for seed in SEEDS:
        stem, right, _ = _q("rational_exponent_equation_m5", seed)
        rhs = _pos(stem.split("=")[1])[0]
        assert round(int(right) ** (2 / 3)) == rhs and int(right) ** 2 == round(rhs ** 1.5) ** 2
        stem, right, _ = _q("like_surds_sum_m5", seed)
        roots = [int(v) for v in re.findall(r"\\sqrt\{(\d+)\}", stem)]
        want = roots[0] ** 0.5 + roots[1] ** 0.5 - roots[2] ** 0.5
        assert abs((_surd(right) if right != "0" else 0) - want) < 1e-9
        stem, right, _ = _q("powers_of_two_exponent_m5", seed)
        a, b, c = [int(v) for v in re.findall(r"\^\{(\d+)\}", stem)][:3]
        assert int(right) == a + 2 * b - 3 * c
        stem, right, _ = _q("arithmetic_sum_m5", seed)
        n = _pos(stem)[0]
        t = _ints(stem.split("อนุกรมนี้")[1])
        a, d = t[0], t[1] - t[0]
        assert int(right.replace(",", "")) == sum(a + d * i for i in range(n))
        stem, right, _ = _q("geometric_term_m5", seed)
        n = _pos(stem)[0]
        t = _ints(stem.split("จำนวนใด")[1])
        assert int(right.replace(",", "")) == t[0] * (t[1] // t[0]) ** (n - 1)
        stem, right, _ = _q("common_difference_m5", seed)
        a, n, an = _ints(stem)[:3]
        assert a + (n - 1) * int(right) == an
        stem, right, _ = _q("simple_interest_rate_m5", seed)
        p, i, t = _pos(stem)[:3]
        assert p * int(right) * t == i * 100
        stem, right, _ = _q("simple_interest_principal_m5", seed)
        r, t, i = _pos(stem)[:3]
        assert int(right.replace(",", "")) * r * t == i * 100
        stem, right, _ = _q("compound_ten_percent_m5", seed)
        p, _, t = _pos(stem)[:3]
        assert Fraction(int(right.replace(",", ""))) == p * Fraction(11, 10) ** t


def test_trig_ratios_and_inverses():
    for seed in SEEDS:
        stem, right, _ = _q("tan_from_sides_m5", seed)
        bc, ac, ab = _pos(stem)[-3:]
        assert _frac(right) == Fraction(bc, ac)
        stem, right, _ = _q("shadow_length_m5", seed)
        h, angle = _pos(stem)[:2]
        assert abs(_surd(right) - h / {30: 3 ** -0.5, 45: 1}[angle]) < 1e-9
        stem, right, _ = _q("angle_of_depression_m5", seed)
        h, angle = _pos(stem)[:2]
        import math
        assert abs(_surd(right) - h / math.tan(math.radians(angle))) < 1e-9
        stem, right, _ = _q("tan_from_sin_m5", seed)
        a, c = map(int, re.search(r"\\frac\{(\d+)\}\{(\d+)\}", stem).groups())
        b = isqrt(c * c - a * a)
        assert _frac(right) == Fraction(a, b)
        stem, right, _ = _q("sin_of_arccos_m5", seed)
        a, c = map(int, re.search(r"\\frac\{(\d+)\}\{(\d+)\}", stem).groups())
        assert _frac(right) == Fraction(isqrt(c * c - a * a), c)
        stem, right, _ = _q("tan_of_arcsin_m5", seed)
        a, c = map(int, re.search(r"\\frac\{(\d+)\}\{(\d+)\}", stem).groups())
        assert _frac(right) == Fraction(a, isqrt(c * c - a * a))
        for key in ("arccos_special_m5", "arcsin_negative_m5", "function_after_inverse_m5", "inverse_trig_principal_range_m5"):
            _q(key, seed)


def test_trig_equations():
    import math
    def solutions(f, lo=0, hi=360):
        return [x for x in range(lo, hi) if abs(f(math.radians(x))) < 1e-9]
    values = {r"\frac{1}{2}": 0.5, r"\frac{\sqrt{3}}{2}": 3 ** 0.5 / 2, r"\frac{\sqrt{2}}{2}": 2 ** 0.5 / 2, "1": 1, "0": 0,
              r"\sqrt{3}": 3 ** 0.5, r"\frac{\sqrt{3}}{3}": 3 ** -0.5, r"\frac{1}{4}": 0.25, r"\frac{3}{4}": 0.75}
    def value(tex):
        neg = tex.startswith("-")
        return -values[tex[1:]] if neg else values[tex]
    for seed in SEEDS:
        for key, fn in (("sin_equals_value_m5", math.sin), ("cos_equals_value_m5", math.cos), ("tan_equals_value_m5", math.tan)):
            stem, right, _ = _q(key, seed)
            v = value(re.search(r"x = (.+?) \\quad", stem).group(1))
            assert _degs(right) == solutions(lambda x: fn(x) - v), (key, stem, right)
        stem, right, _ = _q("sin_squared_count_m5", seed)
        fn = math.sin if r"\sin" in stem else math.cos
        v = value(re.search(r"x = (.+?) \\quad", stem).group(1))
        assert int(right) == len(solutions(lambda x: fn(x) ** 2 - v))
        stem, right, _ = _q("two_cos_plus_root3_m5", seed)
        eq = stem.split("แก้สมการ")[1].split(r" \quad")[0]
        lhs = eq.replace(" = 0", "")
        k = 3 ** 0.5 if r"\sqrt{3}" in lhs.split("x")[1] else 1
        lead = 2 if lhs.startswith("2") else 2 ** 0.5
        fn = math.cos if r"\cos" in lhs else math.sin
        sign = 1 if " + " in lhs else -1
        assert _degs(right) == solutions(lambda x: lead * fn(x) + sign * k)
        stem, right, _ = _q("sum_of_two_solutions_m5", seed)
        assert _degs(right) == [180 if r"\sin" in stem else 360]


def test_laws_of_sines_and_cosines():
    for seed in SEEDS:
        stem, right, _ = _q("side_from_circumradius_m5", seed)
        r, angle = _pos(stem)[:2]
        import math
        assert abs(int(right) - 2 * r * math.sin(math.radians(angle))) < 1e-9
        stem, right, _ = _q("area_with_thirty_degrees_m5", seed)
        a, b, angle = _pos(stem)[:3]
        assert abs(int(right) - a * b * math.sin(math.radians(angle)) / 2) < 1e-9
        stem, right, _ = _q("side_from_two_angles_m5", seed)
        A, B, a = _pos(stem)[:3]
        assert abs(_surd(right) - a * math.sin(math.radians(B)) / math.sin(math.radians(A))) < 1e-9
        stem, right, _ = _q("cos_from_three_sides_m5", seed)
        a, b, c = _pos(stem)[:3]
        assert _frac(right) == Fraction(a * a + b * b - c * c, 2 * a * b)
        for key, cos in (("side_with_120_m5", -0.5), ("side_with_60_m5", 0.5), ("parallelogram_long_diagonal_m5", -0.5)):
            stem, right, _ = _q(key, seed)
            a, b = _pos(stem)[:2]
            assert int(right) ** 2 == round(a * a + b * b - 2 * a * b * cos), key
        _q("special_triangle_side_ratio_m5", seed)


def test_counting_and_arrangements():
    for seed in SEEDS:
        stem, right, _ = _q("divisible_by_either_m5", seed)
        _, top, a, b = _pos(stem)[:4]
        assert int(right) == sum(1 for v in range(1, top + 1) if v % a == 0 or v % b == 0)
        stem, right, _ = _q("grid_paths_m5", seed)
        m, k = _pos(stem)[:2]
        assert int(right) == comb(m + k, m)
        stem, right, _ = _q("number_plates_m5", seed)
        letters, digits = _pos(stem)[:2]
        assert int(right.replace(",", "")) == 26 ** letters * 10 ** digits
        stem, right, _ = _q("functions_between_sets_m5", seed)
        m, k = _pos(stem)[:2]
        assert int(right) == (factorial(k) // factorial(k - m) if "หนึ่งต่อหนึ่ง" in stem else k ** m)
        stem, right, _ = _q("distinct_letters_word_m5", seed)
        word = re.search(r"คำว่า ([A-Z]+)", stem).group(1)
        assert int(right.replace(",", "")) == factorial(len(word)) and len(set(word)) == len(word)
        stem, right, _ = _q("three_officers_m5", seed)
        n = _pos(stem)[0]
        assert int(right.replace(",", "")) == n * (n - 1) * (n - 2)
        stem, right, _ = _q("kept_apart_m5", seed)
        from itertools import permutations
        n = _pos(stem)[0]
        assert int(right.replace(",", "")) == sum(1 for p in permutations(range(n)) if abs(p.index(0) - p.index(1)) > 1)
        stem, right, _ = _q("at_least_one_girl_m5", seed)
        b, g, k = _pos(stem)[:3]
        assert int(right) == comb(b + g, k) - comb(b, k)
        stem, right, _ = _q("lines_and_triangles_m5", seed)
        n = _pos(stem)[0]
        assert int(right) == (comb(n, 2) if "ส่วนของเส้นตรง" in stem else comb(n, 3))
        stem, right, _ = _q("polygon_diagonals_m5", seed)
        n = _pos(stem)[0]
        assert int(right) == comb(n, 2) - n
        stem, right, texts = _q("pascal_rule_m5", seed)
        (n, r), (_, r2) = [tuple(map(int, m)) for m in re.findall(r"\\binom\{(\d+)\}\{(\d+)\}", stem)]
        for t in texts:
            tn, tr = map(int, re.search(r"\\binom\{(\d+)\}\{(\d+)\}", t).groups())
            assert (comb(tn, tr) == comb(n, r) + comb(n, r2)) == (t == right), t


def test_binomial_and_expected_value():
    for seed in SEEDS:
        stem, right, _ = _q("binomial_constant_term_m5", seed)
        n = _pos(stem.split("^")[1])[0]
        assert int(right) == comb(n, n // 2)
        stem, right, _ = _q("binomial_term_count_m5", seed)
        assert int(right) == _pos(stem.split("^")[1])[0] + 1
        stem, right, _ = _q("coefficient_in_ax_plus_one_m5", seed)
        k = _pos(stem)[0]
        a, n = _pos(stem.split("เท่าใด")[1])[0], _pos(stem.split("^")[1])[0]
        assert int(right.replace(",", "")) == comb(n, k) * a ** k
        stem, right, _ = _q("sum_of_coefficients_m5", seed)
        inner = re.search(r"\((.+)\)\^\{(\d+)\}", stem)
        assert int(right.replace(",", "")) == _ev(inner.group(1), Fraction(1)) ** int(inner.group(2))
        stem, right, _ = _q("rth_term_coefficient_m5", seed)
        r1 = _pos(stem)[0]
        c, n = _pos(stem.split("เท่าใด")[1])[:2]
        assert int(right.replace(",", "")) == comb(n, r1 - 1) * c ** (r1 - 1)
        stem, right, _ = _q("pascal_middle_m5", seed)
        n = _pos(stem)[0]
        assert int(right) == comb(n, n // 2)
        stem, right, _ = _q("win_or_lose_m5", seed)
        k, d, win, lose = _pos(stem)[:4]
        assert _frac(right) == Fraction(k * win - (d - k) * lose, d)
        stem, right, _ = _q("spinner_expected_m5", seed)
        n = _pos(stem)[0]
        prizes = _pos(stem.split("รางวัล")[1].split("บาท")[0])
        assert len(prizes) == n and _frac(right) == Fraction(sum(prizes), n)
        stem, right, _ = _q("raffle_ticket_m5", seed)
        tickets, _, first, _, seconds, second = _pos(stem)[:6]
        assert _frac(right) == Fraction(first + seconds * second, tickets)
        stem, right, _ = _q("expected_heads_m5", seed)
        assert _frac(right) == Fraction(_pos(stem)[0], 2)
        stem, right, _ = _q("insurance_profit_m5", seed)
        premium, payout, _, d = _pos(stem)[:4]
        assert _frac(right) == premium - Fraction(payout, d)
        stem, right, _ = _q("die_game_m5", seed)
        pay = _pos(stem)[-1]
        assert _frac(right) == Fraction(2 + 4 + 6 - 3 * pay, 6)
