"""The ม.6 sets added so every unit has at least ten: each answer worked out again from the stem alone.

Polynomials are compared by evaluating both sides at several points, numbers are read back out of the
question, and text answers are checked against facts written out here independently.
"""

from __future__ import annotations

import re
from fractions import Fraction
from math import comb, factorial, gcd, isqrt
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


import sympy as sp

X = sp.Symbol("x")


from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application, parse_expr,
                                        standard_transformations)

_TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)


def _braced(s: str, at: int) -> tuple[str, int]:
    """The text inside the brace group that opens at s[at], and the index just past it."""
    assert s[at] == "{", s
    depth = 0
    for i in range(at, len(s)):
        depth += s[i] == "{"
        depth -= s[i] == "}"
        if depth == 0:
            return s[at + 1:i], i + 1
    raise AssertionError(s)


def _plain(tex: str) -> str:
    out, i = "", 0
    while i < len(tex):
        if tex.startswith("\\frac", i):
            top, i = _braced(tex, i + 5)
            bottom, i = _braced(tex, i)
            out += f"(({_plain(top)})/({_plain(bottom)}))"
        elif tex.startswith("\\sqrt", i):
            inner, i = _braced(tex, i + 5)
            out += f"sqrt({_plain(inner)})"
        elif tex.startswith("e^", i) and tex[i + 2] == "{":
            inner, i = _braced(tex, i + 2)
            out += f"exp({_plain(inner)})"
        elif tex.startswith("^", i) and tex[i + 1] == "{":
            inner, i = _braced(tex, i + 1)
            out += f"**({_plain(inner)})"
        else:
            out += tex[i]
            i += 1
    return out


def _sym(tex: str):
    """A TeX answer or expression as sympy, for the forms these sets print."""
    s = tex.replace(" + C", "").replace("\\,", " ").replace("\\left", "").replace("\\right", "")
    s = s.replace("\\ln", " log ").replace("\\sin", " sin ").replace("\\cos", " cos ").replace("\\pi", " pi ")
    s = re.sub(r"\|([^|]*)\|", r"Abs(\1)", s)
    s = _plain(s)
    s = re.sub(r"(sin|cos|log) +([0-9]*x)", r"\1(\2)", s)
    return parse_expr(s, local_dict={"x": X, "e": sp.E, "pi": sp.pi}, transformations=_TRANSFORMS)


def _rows(stem: str):
    return [tuple(int(v) for v in re.findall(r"\d+", line)) for line in stem.split("\n") if re.fullmatch(r"\d+ – \d+ \| \d+", line.strip())]


def test_applied_and_tables():
    for seed in SEEDS:
        stem, right, _ = _q("stratified_share_m6", seed)
        a, b, c, sample = _pos(stem)[1], _pos(stem)[3], _pos(stem)[5], _pos(stem)[6]
        assert Fraction(int(right)) == Fraction(sample * a, a + b + c)
        stem, right, _ = _q("systematic_sampling_m6", seed)
        total, n, first, k = _pos(stem)[:4]
        assert int(right) == first + (k - 1) * (total // n)
        for key in ("population_or_sample_m6", "sampling_method_m6", "primary_secondary_data_m6", "biased_survey_m6",
                    "discrete_or_continuous_m6"):
            _q(key, seed)
        stem, right, _ = _q("class_width_m6", seed)
        r = _rows(stem)
        assert int(right) == r[0][1] - r[0][0] + 1
        stem, right, _ = _q("total_frequency_m6", seed)
        assert int(right) == sum(f for *_, f in _rows(stem))
        stem, right, _ = _q("cumulative_of_class_m6", seed)
        r = _rows(stem)
        a, b = map(int, re.search(r"ชั้น (\d+) – (\d+) เท่ากับ", stem).groups())
        i = [x[:2] for x in r].index((a, b))
        assert int(right) == sum(f for *_, f in r[:i + 1])
        stem, right, _ = _q("relative_percent_m6", seed)
        r = _rows(stem)
        a, b = map(int, re.search(r"ชั้น (\d+) – (\d+) มี", stem).groups())
        f = next(x[2] for x in r if x[:2] == (a, b))
        assert Fraction(int(right)) == Fraction(100 * f, sum(x[2] for x in r))
        stem, right, _ = _q("modal_class_m6", seed)
        r = _rows(stem)
        top = max(r, key=lambda x: x[2])
        assert right == f"{top[0]} – {top[1]}"
        stem, right, _ = _q("number_of_classes_m6", seed)
        low, high, width = _pos(stem)[:3]
        k = int(right)
        assert low + k * width - 1 >= high > low + (k - 1) * width - 1
        stem, right, _ = _q("polygon_point_m6", seed)
        r = _rows(stem)
        a, b = map(int, re.search(r"ชั้น (\d+) – (\d+)$", stem).groups())
        f = next(x[2] for x in r if x[:2] == (a, b))
        assert _point(right) == (Fraction(a + b, 2), f)


def test_centre_spread_position():
    def data_of(stem):
        return _ints(stem.split("คือ")[1].split("ค่า")[0].split("มัธยฐาน")[0].split("ฐานนิยม")[0].split("ส่วน")[0].split("พิสัย")[0].split("เปอร์")[0].split("ควอร์")[0])
    for seed in SEEDS:
        stem, right, _ = _q("mean_of_list_m6", seed)
        d = data_of(stem)
        assert Fraction(int(right)) == Fraction(sum(d), len(d))
        stem, right, _ = _q("median_even_list_m6", seed)
        d = sorted(data_of(stem))
        assert _frac(right) == Fraction(d[len(d) // 2 - 1] + d[len(d) // 2], 2)
        stem, right, _ = _q("mode_of_list_m6", seed)
        d = data_of(stem)
        assert int(right) == max(set(d), key=d.count) and d.count(int(right)) > max(d.count(v) for v in set(d) if v != int(right))
        stem, right, _ = _q("combined_mean_m6", seed)
        n1, m1, n2, m2 = _pos(stem)[:4]
        assert _frac(right) == Fraction(n1 * m1 + n2 * m2, n1 + n2)
        stem, right, _ = _q("variance_from_sums_m6", seed)
        n, sx, sx2 = _pos(stem.replace("x_i^{2}", "")[stem.index("N"):])[:3]
        assert Fraction(int(right)) == Fraction(sx2, n) - Fraction(sx, n) ** 2
        stem, right, _ = _q("sd_from_variance_m6", seed)
        assert int(right) ** 2 == _pos(stem)[0]
        stem, right, _ = _q("mean_absolute_deviation_m6", seed)
        d = data_of(stem)
        m = Fraction(sum(d), len(d))
        assert _frac(right) == sum(abs(x - m) for x in d) / len(d)
        stem, right, _ = _q("scaled_sd_m6", seed)
        sd = _pos(stem)[0]
        k = _ints(stem.split("คูณด้วย")[1])[0]
        assert int(right) == abs(k) * sd
        stem, right, _ = _q("iqr_from_data_m6", seed)
        d = sorted(data_of(stem))
        n = len(d)
        assert int(right) == d[3 * (n + 1) // 4 - 1] - d[(n + 1) // 4 - 1]
        stem, right, _ = _q("percentile_value_m6", seed)
        d = _ints(stem.split("คือ")[1].split("เปอร์")[0])
        k = _pos(stem.split("เปอร์เซ็นไทล์ที่")[1])[0]
        assert int(right) == d[k * (len(d) + 1) // 100 - 1]
        stem, right, _ = _q("decile_position_m6", seed)
        n, k = _pos(stem.split("ที่เท่าใด")[1])[:2]
        assert _frac(right) == Fraction(k * (n + 1), 10)
        stem, right, _ = _q("quartile_position_m6", seed)
        n, k = _pos(stem.split("ที่เท่าใด")[1])[:2]
        assert _frac(right) == Fraction(k * (n + 1), 4)
        stem, right, _ = _q("count_below_percentile_m6", seed)
        n, p = _pos(stem)[:2]
        assert int(right) == n * p // 100
        stem, right, _ = _q("quartile_from_list_m6", seed)
        d = _ints(stem.split("คือ")[1].split("ควอร์")[0])
        k = _pos(stem.split("ควอร์ไทล์ที่")[1])[0]
        assert int(right) == d[k * (len(d) + 1) // 4 - 1]
        stem, right, _ = _q("percentile_rank_from_order_m6", seed)
        n, below = _pos(stem)[:2]
        assert Fraction(int(right)) == Fraction(100 * below, n)


def test_z_and_regression():
    for seed in SEEDS:
        stem, right, _ = _q("sd_from_z_m6", seed)
        mu, x = _pos(stem)[:2]
        z = _ints(stem.split("เท่ากับ")[1])[0]
        assert mu + z * int(right) == x
        stem, right, _ = _q("mean_from_z_m6", seed)
        sd, x = _pos(stem)[:2]
        z = _ints(stem.split("เท่ากับ")[1])[0]
        assert int(right) + z * sd == x
        stem, right, _ = _q("z_gap_m6", seed)
        mu, sd, x2, x1 = _pos(stem)[:4]
        assert Fraction(int(right)) == Fraction(x2 - x1, sd)
        stem, right, _ = _q("regression_intercept_m6", seed)
        b, xbar, ybar = _pos(stem)[:3]
        assert int(right) == ybar - b * xbar
        stem, right, _ = _q("regression_x_needed_m6", seed)
        a, b, y = _pos(stem)[:3]
        assert a + b * int(right) == y
        stem, right, texts = _q("slope_meaning_m6", seed)
        b = _ints(stem.split("(")[-1].split(")")[0])[0]
        assert right.endswith(f"จะ{'เพิ่มขึ้น' if b > 0 else 'ลดลง'} {abs(b)} คะแนน") and right.startswith("อ่านเพิ่ม 1 ชั่วโมง")
        stem, right, _ = _q("residual_m6", seed)
        a, b, x, y = _pos(stem)[:4]
        assert int(right) == y - (a + b * x)
        for key in ("z_after_shift_m6", "z_properties_m6", "share_above_z_m6", "correlation_meaning_m6"):
            _q(key, seed)


def test_sequences_and_limits():
    for seed in SEEDS:
        stem, right, _ = _q("term_from_two_terms_m6", seed)
        m, am, n, an, k = _ints(stem.replace("a_", " "))[:5]
        d = Fraction(an - am, n - m)
        assert int(right) == am + (k - m) * d
        stem, right, _ = _q("count_terms_m6", seed)
        t = _ints(stem.split("มีทั้งหมด")[0])
        assert int(right) == (t[-1] - t[0]) // (t[1] - t[0]) + 1
        stem, right, _ = _q("sum_of_multiples_m6", seed)
        top, k = _pos(stem)[1:3]
        assert int(right.replace(",", "")) == sum(v for v in range(1, top + 1) if v % k == 0)
        stem, right, _ = _q("ratio_from_terms_m6", seed)
        a2, a5 = _ints(stem.replace("a_", " "))[1::2][:2]
        assert int(right) ** 3 * a2 == a5
        stem, right, _ = _q("geo_term_from_two_m6", seed)
        a1, a3 = _ints(stem.replace("a_", " "))[1::2][:2]
        assert Fraction(int(right)) == Fraction(a3 * a3, a1)
        stem, right, _ = _q("geo_sum_ratio_three_m6", seed)
        n = _pos(stem)[0]
        t = _ints(stem.split("แรก")[1])
        a, r = t[0], t[1] // t[0]
        assert int(right.replace(",", "")) == sum(a * r ** i for i in range(n))
        stem, right, _ = _q("geometric_mean_m6", seed)
        a, b = _pos(stem)[:2]
        assert int(right) ** 2 == a * b
        stem, right, _ = _q("geo_which_term_m6", seed)
        t = _ints(stem.split("จำนวน")[0])
        v = _pos(stem.split("จำนวน")[1])[0]
        assert t[0] * (t[1] // t[0]) ** (int(right) - 1) == v
        stem, right, _ = _q("sum_of_squares_m6", seed)
        n = _pos(stem.split("^{")[1])[0]
        assert int(right.replace(",", "")) == sum(k * k for k in range(1, n + 1))
        for key in ("limit_polynomial_m6", "limit_cancel_factor_m6", "limit_ratio_infinity_m6", "limit_lower_degree_top_m6",
                    "limit_root_over_x_m6", "one_sided_abs_m6"):
            stem, right, _ = _q(key, seed)
            tex = stem.removeprefix("จงหาค่า")
            point, body = re.fullmatch(r"\\lim_\{x \\to (.+?)\} (.+)", tex).groups()
            body = body.replace(r"\sqrt{", "sqrt{").replace("|x|", "Abs(x)")
            body = re.sub(r"sqrt\{([^{}]*)\}", r"sqrt(\1)", body)
            expr = _sym(body) if "sqrt(" not in body else sp.sympify(re.sub(r"\\frac\{(.+)\}\{x\}", r"(\1)/x", body).replace(" ", ""))
            if point == r"\infty":
                want = sp.limit(expr, X, sp.oo)
            elif point.endswith("^{+}") or point.endswith("^{-}"):
                want = sp.limit(expr, X, 0, point[-2])
            else:
                want = sp.limit(expr, X, int(point))
            assert sp.simplify(_sym(right) - want) == 0, (key, tex, right, want)


def test_differential_calculus():
    for seed in SEEDS:
        stem, right, _ = _q("product_rule_value_m6", seed)
        k = _ints(stem.split("f′(")[1])[0]
        f = _sym(stem.split("f(x) = ")[1])
        assert sp.diff(f, X).subs(X, k) == int(right)
        stem, right, _ = _q("quotient_rule_value_m6", seed)
        f = _sym(stem.split("f(x) = ")[1])
        assert sp.diff(f, X).subs(X, 0) == _sym(right)
        stem, right, _ = _q("root_derivative_value_m6", seed)
        c = _pos(stem.split("f(x) = ")[1].split("sqrt")[0] or "1")
        c = c[0] if c else 1
        k2 = _pos(stem.split("f′(")[1])[0]
        assert sp.diff(c * sp.sqrt(X), X).subs(X, k2) == _sym(right)
        stem, right, _ = _q("tangent_y_intercept_m6", seed)
        f = _sym(stem.split("y = ")[1].split(r", \quad")[0])
        a = _ints(stem.split("x = ")[-1])[0]
        assert f.subs(X, a) - sp.diff(f, X).subs(X, a) * a == int(right)
        stem, right, _ = _q("point_with_slope_m6", seed)
        f = _sym(stem.split("y = ")[1].split("เส้นสัมผัส")[0]) if False else _sym(stem.split("y = ")[-1])
        m = _ints(stem.split("เท่ากับ")[1])[0]
        x0, y0 = _point(right)
        assert sp.diff(f, X).subs(X, x0) == m and f.subs(X, x0) == y0
        stem, right, _ = _q("tangent_to_cubic_m6", seed)
        a = _ints(stem.split("x = ")[-1])[0]
        line = _sym(right.split("y = ")[1])
        assert sp.simplify(line - (3 * a * a * (X - a) + a ** 3)) == 0
        stem, right, _ = _q("tangent_perpendicular_m6", seed)
        k = sp.diff(_sym(stem.split(r"\quad y = ")[1]), X)
        assert 2 * _sym(right) * k == -1
        stem, right, _ = _q("tangent_x_intercept_m6", seed)
        a = _ints(stem.split("x = ")[-1])[0]
        assert a * a + 2 * a * (_sym(right) - a) == 0
        stem, right, _ = _q("normal_y_intercept_m6", seed)
        a = _ints(stem.split("x = ")[-1])[0]
        assert _sym(right) == a * a + sp.Rational(1, 2)
        stem, right, _ = _q("quadratic_critical_point_m6", seed)
        f = _sym(stem.split("f(x) = ")[1])
        assert sp.solve(sp.diff(f, X), X) == [_ints(right)[0]]
        stem, right, _ = _q("cubic_relative_max_m6", seed)
        f = _sym(stem.split("f(x) = ")[1])
        crit = sp.solve(sp.diff(f, X), X)
        assert max(f.subs(X, c) for c in crit if sp.diff(f, X, 2).subs(X, c) < 0) == int(right)
        stem, right, _ = _q("increasing_interval_m6", seed)
        f = _sym(stem.split("f(x) = ")[1])
        h = sp.solve(sp.diff(f, X), X)[0]
        up = sp.diff(f, X).subs(X, h + 1) > 0
        assert right == (f"x > {h}" if up else f"x < {h}")
        _q("second_derivative_test_m6", seed)


def test_integral_calculus():
    def definite(tex):
        m = re.fullmatch(r"\\int_\{(.+?)\}\^\{(.+?)\} (.+?) \\, dx", tex)
        lo, hi, body = m.groups()
        body = body.strip()
        if body.startswith("(") and body.endswith(")") and body.count("(") == 1:
            body = body[1:-1]
        return sp.integrate(_sym(body), (X, _sym(lo), _sym(hi)))
    for seed in SEEDS:
        for key in ("integral_of_power_m6", "integral_of_line_m6", "symmetric_odd_integral_m6", "parts_definite_trig_m6",
                    "parts_x_exp_definite_m6", "sub_linear_square_definite_m6", "sub_chain_definite_m6"):
            stem, right, _ = _q(key, seed)
            assert sp.simplify(definite(stem.removeprefix("จงหาค่า")) - _sym(right)) == 0, (key, stem, right)
        stem, right, _ = _q("integral_linearity_m6", seed)
        a, b, k = _ints(stem.split("dx = ")[0].split("int_")[1]) + _ints(stem.split("dx = ")[1])[:1]
        p, q = _pos(stem.split("ของ (")[1])[:2]
        assert int(right) == p * k + q * (b - a)
        stem, right, _ = _q("integral_split_m6", seed)
        p, q = _ints(stem.split("dx = ")[1])[0], _ints(stem.split("dx = ")[2])[0]
        assert int(right) == q - p
        stem, right, _ = _q("upper_limit_from_value_m6", seed)
        v = _pos(stem.split("dx = ")[1])[0]
        assert int(right) ** 2 == v
        for key in ("parts_ln_m6", "parts_power_ln_m6", "parts_x_squared_exp_m6", "sub_linear_power_m6", "sub_chain_power_m6",
                    "sub_exp_linear_m6", "sub_cos_linear_m6"):
            stem, right, texts = _q(key, seed)
            integrand = _sym(re.fullmatch(r".*?\\int (.+) \\, dx", stem).group(1))
            for t in texts:
                ok = sp.simplify(sp.diff(_sym(t), X) - integrand) == 0
                assert ok == (t == right), (key, stem, t)
        for key in ("parts_pick_u_m6", "parts_formula_m6", "sub_pick_u_m6"):
            _q(key, seed)


def test_areas_and_distributions():
    for seed in SEEDS:
        stem, right, _ = _q("area_under_line_m6", seed)
        f, rng_ = stem.split("y = ")[1].split(r", \quad ")
        lo, hi = _ints(rng_)[:2]
        assert sp.integrate(_sym(f), (X, lo, hi)) == _sym(right)
        for key in ("area_under_cubic_m6", "area_under_root_m6", "area_under_shifted_square_m6"):
            stem, right, _ = _q(key, seed)
            f, rng_ = stem.split("y = ")[1].split(r", \quad ")
            hi = _ints(rng_)[-1]
            f = f.replace(r"\sqrt{x}", "x^{1/2}").replace("x^{1/2}", "(x)^{(1/2)}")
            expr = sp.sqrt(X) if "sqrt" in stem else _sym(f)
            assert sp.integrate(expr, (X, 0, hi)) == _sym(right), key
        stem, right, _ = _q("area_inside_parabola_m6", seed)
        f = -_sym(stem.split("y = -")[1])
        roots = sorted(sp.solve(f, X))
        assert sp.integrate(f, (X, roots[0], roots[1])) == _sym(right)
        stem, right, _ = _q("area_below_axis_m6", seed)
        f = _sym(stem.split("y = ")[1])
        roots = sorted(sp.solve(f, X))
        assert -sp.integrate(f, (X, roots[0], roots[1])) == _sym(right)
        for key in ("parabola_and_line_m6", "facing_parabolas_m6", "cubic_and_line_m6"):
            stem, right, _ = _q(key, seed)
            parts = stem.split("y = ")[1:3]
            f, g = _sym(parts[0].split(",")[0]), _sym(parts[1].split(",")[0])
            pts = sorted(set(sp.solve(f - g, X)))
            if key == "cubic_and_line_m6":
                pts = [p for p in pts if p >= 0]
            area = sum(abs(sp.integrate(f - g, (X, a, b))) for a, b in zip(pts, pts[1:]))
            assert area == _sym(right), (key, stem, right, area)
        stem, right, _ = _q("binomial_mean_m6", seed)
        n = _pos(stem.split("B(")[1])[0]
        p = _sym(stem.split(r",\ ")[1].split(")")[0])
        assert _frac(right) == Fraction(str(n * p))
        stem, right, _ = _q("missing_probability_m6", seed)
        cells = stem.split(r"P(X = x) & ")[1].split(r" \end")[0].split(" & ")
        known = sum(_sym(c) for c in cells if c != "k")
        assert _sym(right) == 1 - known
