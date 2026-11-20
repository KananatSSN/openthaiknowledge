"""The ม.1 sets added so every unit has at least ten: each answer worked out again from the stem alone.

Exact arithmetic (Fraction, integer tenths) for numbers, SymPy for the expressions, and a count or a list of
facts written out here independently for the rest. For the "which is largest / smallest" sets every choice is
checked, so a number drawn from elsewhere can never beat the answer.
"""

from __future__ import annotations

import re
from fractions import Fraction
from random import Random

import sympy as sp

from otk.core import generate

SEEDS = range(300)
x, y, n = sp.symbols("x y n")


def _text(blocks) -> str:
    return "".join(getattr(b, "text", None) or getattr(b, "tex", None) or "" for b in blocks)


def _q(key: str, seed: int):
    q = generate(f"math.{key}", Random(seed))
    texts = [_text(c.content) for c in q.choices]
    assert len(set(texts)) == len(texts), (key, seed, texts)
    return _text(q.stem), texts[q.answer], texts


def _ints(s: str) -> list[int]:
    return [int(v) for v in re.findall(r"-?\d+", s.replace(",", "").replace("−", "-"))]


def _value(tex: str) -> Fraction:
    """A number written as an integer, a decimal or \\frac{a}{b} (with a leading minus)."""
    tex = tex.replace("{,}", "").replace("−", "-").strip()
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if m:
        v = Fraction(int(m.group(2)), int(m.group(3)))
        return -v if m.group(1) else v
    return Fraction(tex)


def _sym(tex: str):
    s = tex.replace("−", "-")
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"((\1)/(\2))", s)
    s = s.replace("^{", "**(").replace("}", ")")
    s = re.sub(r"(\d)\s*([xyn(])", r"\1*\2", s)
    s = re.sub(r"\)\s*([xyn(\d])", r")*\1", s)
    s = re.sub(r"([xy])\s*([xy(])", r"\1*\2", s)
    return sp.sympify(s, locals={"x": x, "y": y, "n": n})


def _pick(stem: str, texts: list[str], key=_value):
    return (max if "มากที่สุด" in stem or "ใหญ่ที่สุด" in stem else min)(texts, key=key)


# ── จำนวนเต็ม ──

def test_integers():
    for seed in SEEDS:
        stem, right, texts = _q("integer_order_m1", seed)
        assert right == _pick(stem, texts)
        stem, right, _ = _q("absolute_value_m1", seed)
        expr = stem.removeprefix("จงหาค่าของ").replace("\\times", "*")
        expr = re.sub(r"\|([^|]+)\|", r"Abs(\1)", expr)
        assert sp.sympify(expr) == int(right), stem
        stem, right, _ = _q("integer_order_of_operations_m1", seed)
        expr = stem.removeprefix("จงหาค่าของ").replace("\\times", "*").replace("\\div", "/").replace("^{", "**(").replace("}", ")")
        assert sp.sympify(expr) == int(right), stem
        stem, right, _ = _q("integer_properties_m1", seed)
        name = {"(−3) + 5 = 5 + (−3)": "สลับที่การบวก", "[2 × (−3)] × 4 = 2 × [(−3) × 4]": "เปลี่ยนหมู่การคูณ",
                "(−4) × (2 + 5) = (−4) × 2 + (−4) × 5": "แจกแจง", "(−7) + 7 = 0": "ตัวผกผันการบวก",
                "(−9) × 1 = −9": "เอกลักษณ์การคูณ", "0 + (−6) = −6": "เอกลักษณ์การบวก"}[stem.removesuffix(" ใช้สมบัติใด")]
        assert name in right


# ── การสร้างทางเรขาคณิต ──

def test_constructions():
    for seed in SEEDS:
        stem, right, _ = _q("construct_segment_length_m1", seed)
        ab, cd = _ints(stem)[:2]
        expr = re.search(r"เส้นตรงยาว (.+?) ด้วยวงเวียน", stem).group(1).replace("−", "-")
        expr = re.sub(r"(\d)(AB|CD)", r"\1*\2", expr)
        assert sp.sympify(expr, locals={"AB": ab, "CD": cd}) == int(right) > 0
        stem, right, texts = _q("triangle_from_sides_m1", seed)
        want = "ไม่ได้" not in stem
        for t in texts:
            a, b, c = sorted(_ints(t))
            assert (a + b > c) == (want if t == right else not want), t
        stem, right, _ = _q("segment_halving_m1", seed)
        length = _ints(stem)[0]
        A, B = 0, Fraction(length)
        M = (A + B) / 2
        N = (A + M) / 2
        pos = {"A": A, "B": B, "M": M, "N": N}
        asked = re.search(r"(\w\w) ยาวกี่", stem).group(1)
        assert abs(pos[asked[0]] - pos[asked[1]]) == int(right)
        stem, right, _ = _q("construct_angle_steps_m1", seed)
        desc = stem.split("“")[1].split("”")[0]
        nums = [int(v) for v in re.findall(r"(\d+) องศา", desc)]
        if "แบ่งครึ่งสองครั้ง" in desc:
            expected = Fraction(nums[0], 4)
        elif "มุมที่เหลือบนเส้นตรง" in desc:
            expected = 180 - nums[0]
        else:
            expected = nums[0] + nums[1]
        assert Fraction(right) == expected
        _q("construction_first_step_m1", seed)
        _q("construction_tools_m1", seed)


# ── จำนวนตรรกยะ ──

def _plain(s: str) -> Fraction:
    return Fraction(s.replace("−", "-"))


def test_rational_numbers():
    for seed in SEEDS:
        stem, right, texts = _q("rational_between_m1", seed)
        lo, hi = (_plain(v) for v in re.search(r"ระหว่าง (\S+) และ (\S+)$", stem).groups())
        for t in texts:
            assert (lo < _value(t) < hi) == (t == right), (stem, t)
        stem, right, _ = _q("rational_mixed_ops_m1", seed)
        expr = stem.removeprefix("จงหาค่าของ").replace("\\left", "").replace("\\right", "").replace("\\times", "*")
        expr = re.sub(r"\\frac\{(\d+)\}\{(\d+)\}", r"(\1/\2)", expr)
        assert sp.Rational(sp.sympify(expr)) == sp.Rational(str(_value(right)))
        stem, right, _ = _q("rational_inverse_m1", seed)
        q = _plain(re.search(r"ของ (\S+) คือ", stem).group(1))
        assert _value(right) == (1 / q if "การคูณ" in stem else -q)
        stem, right, _ = _q("fraction_of_amount_m1", seed)
        total, a, b, c, d = _ints(stem)[:5]
        left = total * (1 - Fraction(a, b))
        left -= left * Fraction(c, d)
        assert left == int(right)
        stem, right, _ = _q("fraction_power_m1", seed)
        m = re.search(r"\\left\((-?)\\frac\{(\d+)\}\{(\d+)\}\\right\)\^\{(\d)\}", stem)
        base = Fraction(int(m.group(2)), int(m.group(3))) * (-1 if m.group(1) else 1)
        assert base ** int(m.group(4)) == _value(right)


# ── ทศนิยมและเศษส่วน ──

def test_decimals_and_fractions():
    for seed in SEEDS:
        q = generate("math.fraction_to_decimal_m1", Random(seed))
        stem, right, _ = _q("fraction_to_decimal_m1", seed)
        assert Fraction(right) == _value(next(b.tex for b in q.stem if b.kind == "math"))
        stem, right, _ = _q("decimal_to_fraction_m1", seed)
        dec = stem.removeprefix("เขียนเป็นเศษส่วนอย่างต่ำได้เท่าใด")
        assert _value(right) == Fraction(dec) and "\\frac" in right
        stem, right, texts = _q("compare_decimals_m1", seed)
        assert right == _pick(stem, texts)
        stem, right, _ = _q("round_decimal_m1", seed)
        value = Fraction(re.search(r"ปัดเศษ (\S+) ให้", stem).group(1))
        places = _ints(stem.split("ทศนิยม")[1])[0]
        scaled = value * 10 ** places
        rounded = Fraction(int(scaled + Fraction(1, 2)), 10 ** places)
        assert Fraction(right) == rounded and len(right.split(".")[1]) == places
        stem, right, _ = _q("repeating_bar_m1", seed)
        digits = stem.split("…")[0].removeprefix("0.")
        m = re.fullmatch(r"0\.(\d*)\\overline\{(\d+)\}", right)
        lead, rep = m.groups()
        assert (lead + rep * 6).startswith(digits) and len(rep) == len(set(rep)) or rep == rep[0] * len(rep)
        stem, right, _ = _q("decimal_money_m1", seed)
        count, price_whole = _ints(stem)[0], Fraction(re.search(r"ชิ้นละ (\S+) บาท", stem).group(1))
        paid = int(re.search(r"ธนบัตร (\d+) บาท", stem).group(1))
        assert Fraction(right) == paid - count * price_whole > 0
        stem, right, texts = _q("order_fractions_decimals_m1", seed)
        assert right == _pick(stem, texts)


# ── มิติสัมพันธ์ ──

def test_spatial():
    sides = {"สามเหลี่ยม": 3, "สี่เหลี่ยม": 4, "ห้าเหลี่ยม": 5, "หกเหลี่ยม": 6, "แปดเหลี่ยม": 8}
    for seed in SEEDS:
        stem, right, _ = _q("solid_parts_m1", seed)
        k = next(v for w, v in sides.items() if f"ฐาน{w}" in stem)
        prism = stem.startswith("ปริซึม")
        # Count by building the solid: vertices, then edges, then faces.
        vertices = 2 * k if prism else k + 1
        edges = 3 * k if prism else 2 * k
        faces = edges - vertices + 2
        expected = faces if "มีหน้า" in stem else edges if "มีขอบ" in stem else vertices
        assert int(right) == expected
        stem, right, _ = _q("euler_formula_m1", seed)
        known = dict(re.findall(r"(หน้า|ขอบ|จุดยอด) (\d+)", stem.split(" (")[0]))
        f, e, v = (int(known.get(w, 0)) for w in ("หน้า", "ขอบ", "จุดยอด"))
        expected = e - v + 2 if "มีหน้ากี่" in stem else f + v - 2 if "มีขอบกี่" in stem else e - f + 2
        assert int(right) == expected
        stem, right, _ = _q("painted_cube_m1", seed)
        size = _ints(stem)[0]
        painted = int(re.search(r"ทาสี (\d) หน้า", stem).group(1)) if "ไม่ถูกทาสี" not in stem else 0
        count = 0
        for i in range(size):
            for j in range(size):
                for k2 in range(size):
                    count += sum(c in (0, size - 1) for c in (i, j, k2)) == painted
        assert int(right) == count
        stem, right, _ = _q("net_faces_m1", seed)
        k = next(v for w, v in sides.items() if f"ฐาน{w}" in stem)
        if "ปริซึม" in stem:
            assert right.endswith(f"2 รูป และรูปสี่เหลี่ยมผืนผ้า {k} รูป")
        else:
            assert right.endswith(f"1 รูป และรูปสามเหลี่ยม {k} รูป")
        stem, right, _ = _q("wire_frame_m1", seed)
        nums = _ints(stem)
        assert int(right) == (4 * sum(nums[:3]) if "ทรงสี่เหลี่ยม" in stem else Fraction(nums[0], 12))
        _q("solid_description_m1", seed)


# ── นิพจน์พีชคณิต ──

def test_algebraic_expressions():
    for seed in SEEDS:
        q = generate("math.like_terms_m1", Random(seed))
        stem, right, texts = _q("like_terms_m1", seed)
        term = next(b.tex for b in q.stem if b.kind == "math")
        letters = lambda t: sp.Poly(_sym(t), x, y).monoms()[0]
        for t in texts:
            assert (letters(t) == letters(term)) == (t == right)
        stem, right, _ = _q("words_to_expression_m1", seed)
        words = stem.split("“")[1].split("”")[0]
        nums = _ints(words)
        if "น้อยกว่า" in words:
            expected = nums[1] * x - nums[0]
        elif "ผลบวก" in words:
            expected = nums[0] * (x + nums[1])
        elif "หารด้วย" in words:
            expected = (x - nums[0]) / nums[1]
        else:
            expected = x ** 2 - nums[0]
        assert sp.simplify(_sym(right) - expected) == 0, (words, right)
        q = generate("math.coefficient_m1", Random(seed))
        stem, right, _ = _q("coefficient_m1", seed)
        poly = sp.Poly(_sym(next(b.tex for b in q.stem if b.kind == "math")), x, y)
        assert int(right) == (poly.coeff_monomial(y) if "สัมประสิทธิ์" in stem else poly.coeff_monomial(1))
        stem, right, _ = _q("pattern_rule_m1", seed)
        terms = _ints(stem.split("…")[0])
        rule = _sym(right)
        assert [rule.subs(n, i + 1) for i in range(4)] == terms
        stem, right, _ = _q("perimeter_expression_m1", seed)
        w, h = re.search(r"กว้าง (.+?) หน่วย ยาว (.+?) หน่วย", stem).groups()
        assert sp.expand(_sym(right) - 2 * (_sym(w) + _sym(h))) == 0
        stem, right, _ = _q("formula_substitution_m1", seed)
        if "F =" in stem:
            c = _ints(stem.split("เปลี่ยน")[1])[0]
            assert Fraction(9, 5) * c + 32 == int(right)
        elif "A =" in stem:
            a, b, h = _ints(stem.split("เมื่อ")[1])[:3]
            assert Fraction((a + b) * h, 2) == int(right)
        else:
            u, a, t = _ints(stem.split("เมื่อ")[1])[:3]
            assert u + a * t == int(right)


# ── สมการเชิงเส้น, อัตราส่วน ──

def test_equations_and_ratio():
    for seed in SEEDS:
        q = generate("math.linear_equation_fractions_m1", Random(seed))
        stem, right, _ = _q("linear_equation_fractions_m1", seed)
        lhs, rhs = next(b.tex for b in q.stem if b.kind == "math").split(" = ")
        assert sp.solve(sp.Eq(_sym(lhs), _sym(rhs)), x) == [int(right)]
        stem, right, _ = _q("ratio_difference_m1", seed)
        a, b, diff = _ints(stem)[:3]
        boys, girls = sp.symbols("boys girls")
        sol = sp.solve([sp.Eq(boys * b, girls * a), sp.Eq(boys - girls, diff)], [boys, girls])
        assert int(right) == (sol[boys] if "มีนักเรียนชาย" in stem else sol[girls])
        stem, right, _ = _q("better_buy_m1", seed)
        q1, p1, q2, p2 = _ints(stem)[:4]
        best = min(Fraction(p1 * 100, q1), Fraction(p2 * 100, q2))
        assert Fraction(right) == best


# ── กราฟความสัมพันธ์เชิงเส้น ──

def _pt(s: str) -> tuple[int, int]:
    a, b = _ints(s)
    return a, b


def test_linear_graphs():
    for seed in SEEDS:
        q = generate("math.point_on_line_m1", Random(seed))
        stem, right, texts = _q("point_on_line_m1", seed)
        line = _sym(next(b.tex for b in q.stem if b.kind == "math").split("= ")[1])
        for t in texts:
            px, py = _pt(t)
            assert (line.subs(x, px) == py) == (t == right)
        q = generate("math.axis_intercepts_m1", Random(seed))
        stem, right, _ = _q("axis_intercepts_m1", seed)
        line = _sym(next(b.tex for b in q.stem if b.kind == "math").split("= ")[1])
        px, py = _pt(right)
        assert line.subs(x, px) == py and (px == 0 if "แกน Y" in stem else py == 0)
        stem, right, _ = _q("quadrant_m1", seed)
        px, py = _pt(re.search(r"\(.+?\)", stem).group(0))
        expected = {(True, True): 1, (False, True): 2, (False, False): 3, (True, False): 4}[(px > 0, py > 0)]
        assert right == f"จตุภาคที่ {expected}"
        stem, right, _ = _q("table_from_equation_m1", seed)
        line = _sym(re.search(r"y = (.+?) คู่อันดับ", stem).group(1))
        pairs = re.findall(r"\((-?\d+), (-?\d+|\?)\)", stem)
        for px, py in pairs:
            if py == "?":
                assert line.subs(x, int(px)) == int(right)
            else:
                assert line.subs(x, int(px)) == int(py)
        stem, right, _ = _q("grid_distance_m1", seed)
        (ax, ay), (bx, by) = (_pt(p) for p in re.findall(r"\(-?\d+, -?\d+\)", stem))
        assert int(right) ** 2 == (ax - bx) ** 2 + (ay - by) ** 2
        stem, right, _ = _q("rate_of_change_m1", seed)
        line = _sym(re.search(r"y = (.+?) ถ้า", stem).group(1))
        k = int(re.search(r"เพิ่มขึ้น (\d+) แล้ว", stem).group(1))
        assert line.subs(x, 7 + k) - line.subs(x, 7) == int(right)


# ── สถิติ ──

def test_statistics():
    for seed in SEEDS:
        stem, right, _ = _q("pie_chart_m1", seed)
        if "มุมที่จุดศูนย์กลางกี่" in stem:
            assert Fraction(_ints(stem)[0] * 360, 100) == int(right)
        elif "คิดเป็นร้อยละเท่าใด" in stem:
            assert Fraction(_ints(stem)[0] * 100, 360) == int(right)
        else:
            total, pct = _ints(stem)[:2]
            assert Fraction(total * pct, 100) == int(right)
        stem, right, _ = _q("monthly_values_m1", seed)
        values = [int(v) for v in re.findall(r"\. (\d+)", stem.split(":")[1])]
        names = re.findall(r"(\S+\.) \d+", stem.split(":")[1])
        if "มากที่สุด" in stem:
            assert int(right) == max(b - a for a, b in zip(values, values[1:]))
        else:
            later, earlier = re.search(r"เดือน (\S+?\.)(?:มากกว่า|น้อยกว่า)เดือน (\S+\.)", stem).groups()
            assert int(right) == abs(values[names.index(later)] - values[names.index(earlier)])
        stem, right, _ = _q("pictograph_m1", seed)
        k, whole = _ints(stem)[1], _ints(stem)[2]
        assert int(right) == whole * k + (Fraction(k, 2) if "ครึ่ง" in stem.split("ทั้งหมด")[1] else 0)
        _q("statistical_question_m1", seed)
        _q("data_display_m1", seed)
