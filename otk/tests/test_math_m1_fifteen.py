"""The ม.1 sets that take every unit to fifteen: each answer worked out again from the stem alone.

SymPy for expressions and equations, exact fractions for numbers, a simulated die and cube row for the
spatial sets, and for every "which is largest / smallest" set a check of all four choices.
"""

from __future__ import annotations

import math
import re
from fractions import Fraction
from random import Random
from statistics import median

import sympy as sp

from otk.core import generate

SEEDS = range(300)
x, a_sym = sp.symbols("x a")


def _text(blocks) -> str:
    return "".join(getattr(b, "text", None) or getattr(b, "tex", None) or "" for b in blocks)


def _q(key: str, seed: int):
    q = generate(f"math.{key}", Random(seed))
    texts = [_text(c.content) for c in q.choices]
    assert len(set(texts)) == len(texts), (key, seed, texts)
    return _text(q.stem), texts[q.answer], texts, q


def _math(q) -> str:
    return next(b.tex for b in q.stem if b.kind == "math")


def _ints(s: str) -> list[int]:
    return [int(v) for v in re.findall(r"-?\d+", s.replace(",", "").replace("{,}", "").replace("−", "-"))]


def _tex_value(tex: str):
    """Evaluate a small TeX expression exactly."""
    s = tex.replace("{,}", "").replace("−", "-").replace("\\cdots", "")
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"((\1)/(\2))", s)
    s = re.sub(r"\\left\|(.+?)\\right\|", r"Abs(\1)", s)
    s = s.replace("\\left", "").replace("\\right", "").replace("\\times", "*").replace("\\div", "/")
    s = s.replace("^{", "**(").replace("}", ")").replace("{", "(")
    s = re.sub(r"(\d)\s*([xa(])", r"\1*\2", s)
    s = re.sub(r"\)\s*([xa(\d])", r")*\1", s)
    return sp.nsimplify(sp.sympify(s, locals={"x": x, "a": a_sym}), rational=True)


def _mixed(tex: str) -> Fraction:
    m = re.fullmatch(r"(-?)(\d*)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if not m:
        return Fraction(tex)
    v = int(m.group(2) or 0) + Fraction(int(m.group(3)), int(m.group(4)))
    return -v if m.group(1) else v


def _frac(tex: str) -> Fraction:
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if m:
        v = Fraction(int(m.group(2)), int(m.group(3)))
        return -v if m.group(1) else v
    return Fraction(tex.replace("{,}", "").replace(",", ""))


def _pick(stem: str, texts, key):
    return (max if "มากที่สุด" in stem else min)(texts, key=key)


# ── จำนวนเต็ม ──

def test_integers():
    for seed in SEEDS:
        stem, right, _, q = _q("integer_run_sum_m1", seed)
        lo, hi = re.search(r"\(-(\d+)\).*?(\d+)$", _math(q)).groups()
        assert sum(range(-int(lo), int(hi) + 1)) == int(right)
        stem, right, _, q = _q("integer_missing_number_m1", seed)
        box = sp.Symbol("box")
        lhs, rhs = _math(q).replace("\\square", "box").split(" = ")
        expr = lhs.replace("\\times", "*").replace("\\div", "/")
        assert sp.solve(sp.Eq(sp.sympify(expr, locals={"box": box}), int(rhs)), box) == [int(right)]
        stem, right, _, q = _q("integer_product_four_m1", seed)
        assert _tex_value(_math(q)) == int(right)
        stem, right, texts, _ = _q("integer_largest_expression_m1", seed)
        assert right == _pick(stem, texts, _tex_value)
        stem, right, _, _ = _q("number_line_moves_m1", seed)
        start, r, left = _ints(stem)[:3]
        assert start + r - left == int(right)


# ── การสร้างทางเรขาคณิต ──

def test_constructions():
    for seed in SEEDS:
        stem, right, _, _ = _q("copied_angles_m1", seed)
        a, b = _ints(stem)[:2]
        words = re.search(r"เท่ากับ (.+?) จะได้", stem).group(1)
        expected = {"∠A + ∠B": a + b, "2∠A": 2 * a, "∠A − ∠B": a - b}[words]
        assert int(right) == expected > 0
        stem, right, _, _ = _q("bisectors_on_line_m1", seed)
        aob = _ints(stem)[0]
        # Rays as angles measured from OA: OB at aob, OC at 180, OP and OQ halfway.
        rays = {"A": 0, "B": aob, "C": 180, "P": aob / 2, "Q": (aob + 180) / 2}
        asked = re.search(r"∠(\w)O(\w) มีขนาด", stem).groups()
        assert abs(rays[asked[0]] - rays[asked[1]]) == int(right)
        stem, right, texts, _ = _q("triangle_data_m1", seed)
        enough = {"ความยาวของด้านทั้งสามด้าน", "ความยาวของด้านสองด้านและขนาดของมุมระหว่างด้านทั้งสอง",
                  "ขนาดของมุมสองมุมและความยาวของด้านระหว่างมุมทั้งสอง"}
        want = "ไม่เพียงพอ" not in stem
        for t in texts:
            assert ((t in enough) == want) == (t == right)
        _q("construction_result_m1", seed)
        _q("parallel_construction_m1", seed)


# ── เลขยกกำลัง ──

def test_exponents():
    for seed in SEEDS:
        stem, right, _, q = _q("quotient_rule_m1", seed)
        base = re.match(r"(.+?)\^\{", _math(q)).group(1)
        m, n = (int(v) for v in re.findall(r"\^\{(\d+)\}", _math(q)))
        assert right == f"{base}^{{{m - n}}}"
        stem, right, _, q = _q("evaluate_powers_m1", seed)
        assert _tex_value(_math(q)) == int(right)
        stem, right, _, q = _q("powers_of_ten_m1", seed)
        if "10ⁿ" in stem:
            word = stem.split(" เขียน")[0]
            value = {"หนึ่งพัน": 10 ** 3, "หนึ่งหมื่น": 10 ** 4, "หนึ่งแสน": 10 ** 5, "หนึ่งล้าน": 10 ** 6,
                     "สิบล้าน": 10 ** 7, "หนึ่งพันล้าน": 10 ** 9}[word]
            assert 10 ** int(right) == value
        else:
            assert _tex_value(_math(q)) == int(right.replace("{,}", ""))
        stem, right, texts, _ = _q("compare_powers_m1", seed)
        assert right == _pick(stem, texts, _tex_value)
        stem, right, texts, q = _q("write_as_power_m1", seed)
        assert _tex_value(_math(q)) == _tex_value(right)
        assert sum(_tex_value(t) == _tex_value(right) and "^" in t for t in texts) == 1


# ── จำนวนตรรกยะ ──

def test_rational_numbers():
    for seed in SEEDS:
        stem, right, _, q = _q("rational_absolute_m1", seed)
        assert _tex_value(_math(q)) == sp.Rational(str(_frac(right)))
        stem, right, _, _ = _q("portions_m1", seed)
        amount = stem.split("น้ำผลไม้ ")[1].split(" ลิตร")[0].replace("−", "-")
        total = sum(Fraction(p) for p in amount.split(" "))
        p, d = _ints(stem.split("ขวดละ")[1])[:2]
        assert total / Fraction(p, d) == int(right)
        stem, right, _, q = _q("mixed_number_m1", seed)
        given = _math(q)
        if "เศษเกิน" in stem:
            assert _mixed(given) == _frac(right) and re.fullmatch(r"-?\\frac\{\d+\}\{\d+\}", right)
        else:
            assert _frac(given) == _mixed(right)
            m = re.fullmatch(r"-?(\d+)\\frac\{(\d+)\}\{(\d+)\}", right)
            assert int(m.group(2)) < int(m.group(3)) and math.gcd(int(m.group(2)), int(m.group(3))) == 1
        stem, right, _, q = _q("nearest_integer_m1", seed)
        f = _frac(_math(q))
        assert all(abs(f - int(right)) < abs(f - k) for k in range(-50, 51) if k != int(right))
        stem, right, _, _ = _q("mixed_number_sum_m1", seed)
        parts = re.findall(r"(\d+) (\d+)/(\d+)", stem)
        a, b = (int(w) + Fraction(int(n), int(d)) for w, n, d in parts)
        assert _frac(right) == (a + b if "รวม" in stem else a - b)


# ── ทศนิยมและเศษส่วน ──

def test_decimals():
    for seed in SEEDS:
        for key in ("decimal_multiply_m1", "decimal_divide_m1"):
            stem, right, _, q = _q(key, seed)
            a, b = (Fraction(v) for v in re.findall(r"\d+\.?\d*", _math(q)))
            assert Fraction(right) == (a * b if "times" in _math(q) else a / b)
        stem, right, _, _ = _q("decimal_place_value_m1", seed)
        number = re.search(r"ใน (\S+) ", stem).group(1)
        digits = number.split(".")[1]
        if "เลขโดดใดอยู่ใน" in stem:
            place = ("หลักส่วนสิบ", "หลักส่วนร้อย", "หลักส่วนพัน").index(stem.split("อยู่ใน")[1])
            assert right == digits[place]
        else:
            d = re.search(r"เลขโดด (\d) มีค่า", stem).group(1)
            assert Fraction(right) == int(d) * Fraction(1, 10 ** (digits.index(d) + 1))
        stem, right, _, _ = _q("decimal_measure_m1", seed)
        a, b = (Fraction(v) for v in re.findall(r"(\d+(?:\.\d+)?) เมตร", stem)[:2])
        assert Fraction(right) == (a + b if "รวมยาว" in stem else a - b)
        stem, right, _, q = _q("fraction_percent_m1", seed)
        if "คิดเป็นร้อยละ" in stem:
            assert _frac(_math(q)) * 100 == Fraction(right)
        else:
            pct = Fraction(re.search(r"ร้อยละ (\S+) เขียน", stem).group(1))
            assert _frac(right) == pct / 100


# ── มิติสัมพันธ์ ──

def test_spatial():
    sides = {"ห้าเหลี่ยม": 5, "หกเหลี่ยม": 6, "แปดเหลี่ยม": 8}
    for seed in SEEDS:
        stem, right, _, _ = _q("prism_rectangles_m1", seed)
        assert int(right) == next(v for w, v in sides.items() if w in stem)
        stem, right, _, _ = _q("cube_staircase_m1", seed)
        n, depth = _ints(stem)[0], _ints(stem)[-1]
        assert int(right) == sum(depth * h for h in range(1, n + 1))
        stem, right, _, _ = _q("glued_cubes_m1", seed)
        k = _ints(stem)[0]
        # Count faces of a row of unit cubes that touch no other cube.
        cubes = {(i, 0, 0) for i in range(k)}
        shown = sum((cx + dx, cy + dy, cz + dz) not in cubes for cx, cy, cz in cubes
                    for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)))
        assert int(right) == shown
        stem, right, _, q = _q("die_faces_m1", seed)
        top = int(re.search(r"หน้าบน(?:มี|เป็น) (\d) จุด", stem).group(1))
        die = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}
        if "หน้าล่าง" in stem:
            assert int(right) == die[top]
        else:
            assert int(right) == sum(range(1, 7)) - top
        stem, right, _, _ = _q("cylinder_net_m1", seed)
        r, h = _ints(stem)[:2]
        side = Fraction(22, 7) * 2 * r
        assert Fraction(int(right)) == (side if "ยาวกี่" in stem else side * h)


# ── นิพจน์พีชคณิต ──

def test_algebraic_expressions():
    for seed in SEEDS:
        for key in ("factor_out_number_m1", "equal_expressions_m1", "like_terms_two_letters_m1", "subtract_bracket_m1"):
            stem, right, texts, q = _q(key, seed)
            y = sp.Symbol("y")
            sym = lambda t: sp.sympify(re.sub(r"([xy\d])\s*\(", r"\1*(", re.sub(r"(\d)([xy])", r"\1*\2", t)),
                                       locals={"x": x, "y": y})
            given = sp.expand(sym(_math(q)))
            assert sp.expand(sym(right)) == given, (key, right)
            for t in texts:
                if t != right:
                    assert sp.expand(sym(t)) != given, (key, t)
        stem, right, _, q = _q("evaluate_square_m1", seed)
        x0 = int(re.search(r"x = (\S+) ", stem).group(1).replace("−", "-"))
        assert _tex_value(_math(q)).subs(x, x0) == int(right)


# ── สมการเชิงเส้น ──

def test_linear_equations():
    for seed in SEEDS:
        stem, right, texts, q = _q("check_solution_m1", seed)
        lhs, rhs = (_tex_value(side) for side in _math(q).split(" = "))
        for t in texts:
            assert (lhs.subs(x, int(t)) == rhs.subs(x, int(t))) == (t == right)
        stem, right, _, q = _q("decimal_equation_m1", seed)
        lhs, rhs = _math(q).split(" = ")
        lhs = re.sub(r"(\d)x", r"\1*x", lhs)
        assert sp.solve(sp.Eq(sp.nsimplify(sp.sympify(lhs, locals={"x": x}), rational=True),
                              sp.nsimplify(rhs, rational=True)), x) == [int(right)]
        stem, right, _, _ = _q("consecutive_numbers_m1", seed)
        count, total = _ints(stem)[:2]
        step = 2 if "จำนวนคู่" in stem else 1
        n = sp.Symbol("n")
        first = sp.solve(sp.Eq(sum(n + step * i for i in range(count)), total), n)[0]
        assert int(right) == (first if "น้อยที่สุด" in stem else first + step * (count - 1))
        stem, right, _, _ = _q("age_problem_m1", seed)
        k, t, total = _ints(stem)[:3]
        c = sp.Symbol("c")
        assert sp.solve(sp.Eq(k * c + t + c + t, total), c) == [int(right)]
        stem, right, _, _ = _q("rectangle_equation_m1", seed)
        d, per = _ints(stem)[:2]
        w = sp.solve(sp.Eq(2 * (x + x + d), per), x)[0]
        assert int(right) == (w if "กว้างกี่" in stem else w + d)


# ── อัตราส่วน ──

def test_ratio():
    for seed in SEEDS:
        stem, right, _, _ = _q("percent_of_m1", seed)
        if stem.startswith("ร้อยละ"):
            pct, base = _ints(stem)[:2]
            assert Fraction(pct * base, 100) == int(right)
        else:
            part, base = _ints(stem)[:2]
            assert Fraction(part * 100, base) == int(right)
        stem, right, _, _ = _q("discount_m1", seed)
        nums = _ints(stem)
        if "ต้องจ่าย" in stem:
            price, pct = nums[:2]
            assert Fraction(price * (100 - pct), 100) == int(right.replace(",", ""))
        else:
            pct, sale = nums[:2]
            assert Fraction(sale * 100, 100 - pct) == int(right.replace(",", ""))
        stem, right, _, _ = _q("speed_distance_time_m1", seed)
        nums = _ints(stem)
        if "ได้ระยะทาง" in stem:
            assert nums[0] * nums[1] == int(right)
        elif "ใช้เวลากี่" in stem:
            assert Fraction(nums[0], nums[1]) == int(right)
        else:
            assert Fraction(nums[0], nums[1]) == int(right)
        stem, right, _, _ = _q("map_distance_m1", seed)
        scale, cm = _ints(stem)[1:3]
        real_cm = scale * cm
        expected = Fraction(real_cm, 100_000) if "กิโลเมตร" in stem else Fraction(real_cm, 100)
        assert Fraction(right.replace(",", "")) == expected
        stem, right, texts, _ = _q("equivalent_ratio_m1", seed)
        a, b = _ints(stem)[:2]
        for t in texts:
            p, q2 = _ints(t)
            assert (Fraction(p, q2) == Fraction(a, b)) == (t == right)


# ── กราฟความสัมพันธ์เชิงเส้น ──

def test_linear_graphs():
    for seed in SEEDS:
        stem, right, texts, _ = _q("rising_line_m1", seed)
        rising = "เพิ่มขึ้น" in stem
        for t in texts:
            line = sp.sympify(re.sub(r"(\d)x", r"\1*x", t.split("= ")[1]), locals={"x": x})
            assert ((line.coeff(x) > 0) == rising) == (t == right)
        stem, right, _, _ = _q("cost_backwards_m1", seed)
        fixed, rate, total = _ints(stem)[:3]
        assert fixed + rate * int(right) == total
        stem, right, _, _ = _q("point_on_axis_m1", seed)
        px, py = re.search(r"\((.+?), (.+?)\)", stem).groups()
        coord = py if "แกน X" in stem else px
        expr = sp.sympify(re.sub(r"(\d)a", r"\1*a", coord.replace("−", "-")), locals={"a": a_sym})
        assert expr.subs(a_sym, int(right)) == 0
        stem, right, texts, _ = _q("table_fits_rule_m1", seed)
        line = sp.sympify(re.sub(r"(\d)x", r"\1*x", stem.split("= ")[1].replace("−", "-")), locals={"x": x})
        for t in texts:
            pairs = [tuple(int(v) for v in p) for p in re.findall(r"\((-?\d+), (-?\d+)\)", t)]
            fits = all(line.subs(x, px) == py for px, py in pairs)
            assert fits == (t == right)
        stem, right, _, _ = _q("intercept_triangle_m1", seed)
        line = sp.sympify(re.sub(r"(\d)x", r"\1*x", re.search(r"y = (.+?) ตัด", stem).group(1).replace("−", "-")),
                          locals={"x": x})
        x0 = sp.solve(line, x)[0]
        c = line.subs(x, 0)
        assert sp.Rational(abs(x0 * c), 2) == sp.nsimplify(right)


# ── สถิติ ──

def test_statistics():
    for seed in SEEDS:
        stem, right, _, _ = _q("median_m1", seed)
        data = _ints(stem.split("ข้อมูล ")[1].split(" มี")[0])
        assert median(data) == int(right)
        stem, right, _, _ = _q("mean_new_value_m1", seed)
        n, mean, new = _ints(stem)[:3]
        assert Fraction(n * mean + new, n + 1) == int(right)
        stem, right, _, _ = _q("mode_from_table_m1", seed)
        pairs = [(int(v), int(f)) for v, f in re.findall(r"(\d+) \((\d+) ครั้ง\)", stem)]
        assert int(right) == max(pairs, key=lambda p: p[1])[0]
        stem, right, _, _ = _q("total_from_mean_m1", seed)
        n, mean = _ints(stem)[:2]
        assert n * mean == int(right)
        _q("data_collection_m1", seed)
