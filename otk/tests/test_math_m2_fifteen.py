"""The ม.2 sets that take every unit to fifteen: each answer worked out again from the stem alone.

SymPy for the factorising, coordinates for the geometry that has a natural picture (the trapezoid, the
rhombus, the shared leg, the parallel-line bisectors, the bisecting diagonals), and exact arithmetic for the
rest. No check reuses a set's own formula.
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
x, y = sp.symbols("x y")


def _text(blocks) -> str:
    return "".join(getattr(b, "text", None) or getattr(b, "tex", None) or "" for b in blocks)


def _q(key: str, seed: int):
    q = generate(f"math.{key}", Random(seed))
    texts = [_text(c.content) for c in q.choices]
    assert len(set(texts)) == len(texts), (key, seed, texts)
    return _text(q.stem), texts[q.answer], texts


def _ints(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"-?\d+", s.replace(",", "").replace("−", "-"))]


def _num(s: str) -> Fraction:
    return Fraction(s.replace("{,}", "").replace(",", ""))


def _lin(s: str) -> tuple[int, int]:
    m = re.fullmatch(r"(\d*)x(?: ([+−]) (\d+))?", s.strip())
    assert m, s
    return int(m.group(1) or 1), int(m.group(3) or 0) * (-1 if m.group(2) == "−" else 1)


def _sym(tex: str):
    s = tex.replace("{,}", "").replace("−", "-").replace("^{", "**(").replace("}", ")")
    s = re.sub(r"(\d)\s*([xy(])", r"\1*\2", s)
    s = re.sub(r"\)\s*([xy(\d])", r")*\1", s)
    s = re.sub(r"([xy])\s*([xy(])", r"\1*\2", s)
    s = re.sub(r"([xy])\s*([xy(])", r"\1*\2", s)
    return sp.sympify(s, locals={"x": x, "y": y})


def _angle(at, p, q) -> float:
    a1 = math.atan2(p[1] - at[1], p[0] - at[0])
    a2 = math.atan2(q[1] - at[1], q[0] - at[0])
    d = abs(math.degrees(a1 - a2)) % 360
    return min(d, 360 - d)


# ── เลขยกกำลัง, จำนวนจริง ──

def test_exponents():
    for seed in SEEDS:
        stem, right, _ = _q("exponent_equation_m2", seed)
        lhs, rhs = stem.split("จงหาค่า x")[1].split(" = ")
        base = int(re.match(r"(\d+)\^", lhs).group(1))
        shift = int(re.search(r"x \+ (\d+)", lhs).group(1)) if "+" in lhs else 0
        target = sp.Integer(int(rhs)) if "^" not in rhs else sp.Integer(int(rhs.split("^")[0])) ** int(re.search(r"\{(\d+)\}", rhs).group(1))
        assert sp.Integer(base) ** (int(right) + shift) == target, stem
        stem, right, texts = _q("exponent_compare_m2", seed)
        value = {t: sp.Integer(int(t.split("^")[0])) ** int(re.search(r"\{(\d+)\}", t).group(1)) for t in texts}
        pick = max(value, key=value.get) if "มากที่สุด" in stem else min(value, key=value.get)
        assert right == pick


def _surd(t: str) -> float:
    m = re.fullmatch(r"(\d*)\\sqrt\{(\d+)\}", t)
    return int(m.group(1) or 1) * math.sqrt(int(m.group(2)))


def test_real_numbers():
    for seed in SEEDS:
        stem, right, texts = _q("compare_surds_m2", seed)
        pick = (max if "มากที่สุด" in stem else min)(texts, key=_surd)
        assert right == pick
        stem, right, _ = _q("sqrt_of_square_m2", seed)
        expr = stem.removeprefix("จงหาค่าของ").replace("\\left", "").replace("\\right", "")
        expr = re.sub(r"\\sqrt\{", "sqrt(", expr).replace("{", "(").replace("}", ")").replace("^", "**")
        assert sp.sympify(expr) == int(right), stem
        stem, right, _ = _q("cube_root_between_m2", seed)
        n = int(re.search(r"\\sqrt\[3\]\{(\d+)\}", stem).group(1))
        lo = int(right.split(" <")[0])
        assert lo ** 3 < n < (lo + 1) ** 3
        stem, right, texts = _q("square_roots_both_m2", seed)
        n = Fraction(re.search(r"ของ (\S+) คือ", stem).group(1))
        r = Fraction(right.split(" และ")[0])
        assert r * r == n and right == f"{right.split(' และ')[0]} และ −{right.split(' และ')[0]}"
        _q("real_number_facts_m2", seed)


# ── การแยกตัวประกอบ ──

def _is_product(tex: str) -> bool:
    depth, outside = 0, ""
    for ch in tex:
        depth += ch == "("
        depth -= ch == ")"
        if depth == 0:
            outside += ch
    return not re.search(r"\S\s*[+-]\s*\S", outside.replace("^{2}", ""))


def _complete(tex: str) -> bool:
    """No bracket left with a common factor in its terms (8(7x²y + 4xy²) still has xy to take out)."""
    for inner in re.findall(r"\(([^()]+)\)", tex):
        terms = sp.Add.make_args(_sym(inner))
        if len(terms) > 1 and sp.gcd_list(list(terms)) != 1:
            return False
    return True


def test_factorising():
    for key in ("factor_four_terms_m2", "factor_square_minus_square_m2", "factor_two_variable_m2"):
        for seed in SEEDS:
            q = generate(f"math.{key}", Random(seed))
            problem = next(b.tex for b in q.stem if b.kind == "math")
            stem, right, texts = _q(key, seed)
            target = sp.expand(_sym(problem))
            assert sp.expand(_sym(right)) == target and _is_product(right), (key, right)
            assert _complete(right), (key, right)
            for t in texts:
                if t != right:
                    assert sp.expand(_sym(t)) != target or not _is_product(t) or not _complete(t), (key, t)
    for seed in SEEDS:
        stem, right, texts = _q("factor_perfect_square_check_m2", seed)
        for t in texts:
            poly = sp.Poly(_sym(t), x)
            a, b, c = poly.all_coeffs()
            assert (b * b - 4 * a * c == 0) == (t == right), t
        stem, right, _ = _q("factor_perfect_square_k_m2", seed)
        k = int(right)
        poly = stem.split("ถ้า ")[1].split(" เป็น")[0].replace("²", "^{2}").replace("k", f"({k})")
        a, b, c = sp.Poly(_sym(poly), x).all_coeffs()
        assert b * b == 4 * a * c and k > 0, stem


# ── พื้นที่ผิวและปริมาตร ──

PI = Fraction(22, 7)


def test_volumes():
    for seed in SEEDS:
        stem, right, _ = _q("cube_area_volume_m2", seed)
        n = _ints(stem)[0]
        if "พื้นที่ผิวทั้งหมด" in stem.split("มี")[1]:
            e = round((n / 6) ** 0.5)
            assert 6 * e * e == n and int(right) == e ** 3
        else:
            e = round(n ** (1 / 3))
            assert e ** 3 == n and int(right) == 6 * e * e
        stem, right, _ = _q("prism_lateral_area_m2", seed)
        n = _ints(stem)
        h = n[-1]
        if "ผืนผ้า" in stem:
            per = 2 * (n[0] + n[1])
        elif "มุมฉาก" in stem:
            per = n[0] + n[1] + n[2]
        else:
            per = n[0] * n[1]
        assert int(right) == per * h
        stem, right, _ = _q("cups_to_fill_m2", seed)
        w, d, h = _ints(stem)[:3]
        assert Fraction(w * d * h) / (PI * 49 * 10) == int(right)
        stem, right, _ = _q("paint_room_m2", seed)
        width, length, height = _ints(stem)[:3]
        walls = 2 * (width + length) * height
        expected = walls if "พื้นที่รวม" in stem else walls * _ints(stem)[3]
        assert _num(right) == expected
        stem, right, _ = _q("melt_recast_m2", seed)
        n = _ints(stem.replace("22/7", ""))
        if "ลูกบาศก์เล็ก" in stem:
            assert Fraction(n[0] * n[1] * n[2], n[3] ** 3) == int(right)
        else:
            r, h, w, d = n[:4]
            assert PI * r * r * h == w * d * int(right)


# ── เส้นขนาน ──

def _parallel_points(u: float) -> dict:
    """AB on y = 1, CD on y = 0, EF through G = (0, 1) with ∠EGB = u."""
    d = (math.cos(math.radians(u)), math.sin(math.radians(u)))
    G, H = (0.0, 1.0), (-d[0] / d[1], 0.0)
    return {"A": (-9, 1), "B": (9, 1), "C": (-9, 0), "D": (9, 0), "G": G, "H": H,
            "E": (d[0], 1 + d[1]), "F": (H[0] - d[0], -d[1])}


def _named(pts, name: str) -> float:
    return _angle(pts[name[1]], pts[name[0]], pts[name[2]])


def test_parallel_lines():
    for seed in SEEDS:
        stem, right, _ = _q("parallel_ratio_m2", seed)
        p, q = (int(v) for v in re.search(r"= (\d+) : (\d+)", stem).groups())
        assert Fraction(180 * p, p + q) == int(right)
        stem, right, _ = _q("parallel_difference_m2", seed)
        d = int(re.search(r"อยู่ (\d+) องศา", stem).group(1))
        big = Fraction(180 + d, 2)
        assert int(right) == (big if stem.endswith("∠BGH (องศา)") else 180 - big)
        stem, right, _ = _q("parallel_name_pair_m2", seed)
        first, second = re.findall(r"∠\w{3}", stem)
        pts = _parallel_points(63)
        a, b = _named(pts, first[1:]), _named(pts, second[1:])
        if right == "มุมภายในที่อยู่บนข้างเดียวกันของเส้นตัด" or right == "มุมประกอบกันเป็นมุมตรง":
            assert round(a + b) == 180
        else:
            assert round(a) == round(b)
        stem, right, _ = _q("parallel_bisectors_m2", seed)
        u = int(re.search(r"∠BGH = (\d+)°", stem).group(1))
        pts = _parallel_points(180 - u)  # ∠BGH = u is the supplement of ∠EGB
        G, H = pts["G"], pts["H"]
        # P where the bisector from G (halfway between GB and GH) meets the one from H (between HD and HG).
        def unit(p, q):
            v = (q[0] - p[0], q[1] - p[1])
            n = math.hypot(*v)
            return v[0] / n, v[1] / n
        g1, g2 = unit(G, pts["B"]), unit(G, H)
        h1, h2 = unit(H, pts["D"]), unit(H, G)
        dg, dh = (g1[0] + g2[0], g1[1] + g2[1]), (h1[0] + h2[0], h1[1] + h2[1])
        t = ((H[0] - G[0]) * dh[1] - (H[1] - G[1]) * dh[0]) / (dg[0] * dh[1] - dg[1] * dh[0])
        P = (G[0] + t * dg[0], G[1] + t * dg[1])
        asked = re.search(r"ขนาดของ ∠(\w+)", stem).group(1)
        got = {"PGH": _angle(G, P, H), "PHG": _angle(H, P, G), "GPH": _angle(P, G, H)}[asked]
        assert round(got) == int(right), stem
        stem, right, _ = _q("parallel_two_unknowns_m2", seed)
        a = int(re.search(r"∠AGE = (\d+)°", stem).group(1))
        pts = _parallel_points(180 - a)
        xn, yn = re.findall(r"∠(\w{3}) = [xy]", stem)
        assert round(_named(pts, xn) - _named(pts, yn)) == int(right)


# ── การแปลงทางเรขาคณิต ──

def _pt(s: str) -> tuple[int, int]:
    a, b = _ints(s)
    return a, b


def _turn(p, deg):
    c, s = round(math.cos(math.radians(deg))), round(math.sin(math.radians(deg)))
    return c * p[0] - s * p[1], s * p[0] + c * p[1]


def test_transformations():
    for seed in SEEDS:
        stem, right, _ = _q("rotate_origin_m2", seed)
        p = _pt(re.search(r"A = (\(.+?\))", stem).group(1))
        deg = int(re.search(r"(\d+)°", stem).group(1)) * (-1 if "ตามเข็ม" in stem else 1)
        assert _pt(right) == _turn(p, deg)
        stem, right, _ = _q("reflect_twice_m2", seed)
        p = _pt(re.search(r"A = (\(.+?\))", stem).group(1))
        if "แกน x" in stem:
            assert _pt(right) == (-p[0], -p[1])
        else:
            a, b = (int(v) for v in re.findall(r"x = (-?\d+)", stem))
            once = (2 * a - p[0], p[1])
            assert _pt(right) == (2 * b - once[0], once[1])
        stem, right, _ = _q("name_the_move_m2", seed)
        p = _pt(re.search(r"A = (\(.+?\))", stem).group(1))
        q = _pt(re.search(r"A′ = (\(.+?\))", stem).group(1))
        moves = {"การสะท้อนข้ามแกน X": (p[0], -p[1]), "การสะท้อนข้ามแกน Y": (-p[0], p[1]),
                 "การหมุนรอบจุดกำเนิด 180°": _turn(p, 180), "การหมุนรอบจุดกำเนิด 90° ทวนเข็มนาฬิกา": _turn(p, 90),
                 "การหมุนรอบจุดกำเนิด 90° ตามเข็มนาฬิกา": _turn(p, -90)}
        assert [n for n, v in moves.items() if v == q] == [right]
        stem, right, _ = _q("reflection_distance_m2", seed)
        p = _pt(re.search(r"A = (\(.+?\))", stem).group(1))
        k = int(re.search(r"y = (-?\d+)", stem).group(1))
        image = (p[0], 2 * k - p[1])
        expected = abs(image[1] - p[1]) if "อยู่ห่างกัน" in stem else abs(image[1] - k)
        assert int(right) == expected
        stem, right, _ = _q("translate_then_turn_m2", seed)
        p = _pt(re.search(r"A = (\(.+?\))", stem).group(1))
        u, v = _pt(re.search(r"เวกเตอร์ (\(.+?\))", stem).group(1))
        assert _pt(right) == _turn((p[0] + u, p[1] + v), 180)


# ── ความเท่ากันทุกประการ ──

def test_congruence():
    for seed in SEEDS:
        stem, right, _ = _q("congruence_perimeter_m2", seed)
        first, second = re.search(r"△(\w{3}) ≅ △(\w{3})", stem).groups()
        ab, bc, ca = _ints(stem.split("ถ้า")[1])[:3]
        side = {frozenset("AB"): ab, frozenset("BC"): bc, frozenset("CA"): ca}
        if "รอบรูป" in stem:
            assert int(right) == ab + bc + ca
        else:
            asked = re.search(r"แล้ว (\w\w) ยาว", stem).group(1)
            back = {s: f for f, s in zip(first, second)}
            assert int(right) == side[frozenset(back[c] for c in asked)]
        stem, right, _ = _q("congruence_name_case_m2", seed)
        facts = stem.split(" มี ")[1].split(" สรุป")[0].split(", ")
        sides = [f for f in facts if not f.startswith("∠")]
        angles = [f.split(" = ")[0][1] for f in facts if f.startswith("∠")]
        if "90°" in stem:
            assert right == "ฉ.ด.ด."
        elif not angles:
            assert right == "ด.ด.ด."
        elif len(angles) == 1:
            assert right == "ด.ม.ด." and all(angles[0] in s.split(" = ")[0] for s in sides)
        else:
            between = set(angles) == set(sides[0].split(" = ")[0])
            assert right == ("ม.ด.ม." if between else "ม.ม.ด.")
        stem, right, _ = _q("congruence_right_triangle_m2", seed)
        c, a = _ints(stem.split("90°")[1])[:2]
        b = math.isqrt(c * c - a * a)
        assert b * b + a * a == c * c
        assert int(right) == (b if "EF ยาว" in stem else a * b // 2)
        stem, right, _ = _q("congruence_bisecting_diagonals_m2", seed)
        p, q = (int(v) for v in re.findall(r"= (\d+)°", stem))
        # Build A, B with O at the origin, then C = −A and D = −B (the diagonals bisect each other).
        # P is the crossing O of the diagonals.
        A = (0.0, 0.0)
        B = (1.0, 0.0)
        P = (math.cos(math.radians(p)) * math.sin(math.radians(q)) / math.sin(math.radians(p + q)),
             math.sin(math.radians(p)) * math.sin(math.radians(q)) / math.sin(math.radians(p + q)))
        C, D = (2 * P[0] - A[0], 2 * P[1] - A[1]), (2 * P[0] - B[0], 2 * P[1] - B[1])
        asked = re.search(r"ขนาดของ ∠(\w+)", stem).group(1)
        got = {"OCD": _angle(C, P, D), "ODC": _angle(D, P, C), "COD": _angle(P, C, D)}[asked]
        assert round(got) == int(right), stem
        stem, right, _ = _q("congruence_isosceles_median_m2", seed)
        apex = int(re.search(r"= (\d+)°", stem).group(1))
        A, B, C = (0.0, math.cos(math.radians(apex / 2))), (-math.sin(math.radians(apex / 2)), 0.0), (math.sin(math.radians(apex / 2)), 0.0)
        M = (0.0, 0.0)
        asked = re.search(r"ขนาดของ ∠(\w+)", stem).group(1)
        got = {"BAM": _angle(A, B, M), "ABM": _angle(B, A, M), "AMB": _angle(M, A, B)}[asked]
        assert round(got) == int(right)


# ── ทฤษฎีบทพีทาโกรัส ──

def test_pythagoras():
    for seed in SEEDS:
        stem, right, _ = _q("pythagoras_square_areas_m2", seed)
        n = _ints(stem)
        if "ด้านตรงข้ามมุมฉากยาว" in stem:
            assert int(right) ** 2 == n[0] + n[1]
        elif "บนด้านตรงข้ามมุมฉากมีพื้นที่ " in stem:
            assert int(right) == n[0] - n[1]
        else:
            assert int(right) == n[0] + n[1]
        stem, right, _ = _q("pythagoras_rhombus_m2", seed)
        n = _ints(stem)
        if "เส้นทแยงมุมยาว" in stem:
            d1, d2 = n[:2]
            assert int(right) ** 2 * 4 == d1 * d1 + d2 * d2
        else:
            side, d1 = n[:2]
            d2 = 2 * math.isqrt(side * side - (d1 // 2) ** 2)
            assert (d1 // 2) ** 2 + (d2 // 2) ** 2 == side * side
            assert int(right) == (d2 if "อีกเส้น" in stem else d1 * d2 // 2)
        stem, right, _ = _q("pythagoras_triangle_perimeter_m2", seed)
        n = _ints(stem)
        if "รอบรูป" in stem:
            a, b = n[:2]
            c = math.isqrt(a * a + b * b)
            assert c * c == a * a + b * b and int(right) == a + b + c
        else:
            c, a = n[:2]
            b = math.isqrt(c * c - a * a)
            assert Fraction(a * b, 2) == int(right)
        stem, right, _ = _q("pythagoras_trapezoid_m2", seed)
        small, big, leg = _ints(stem)[:3]
        # Coordinates: the long base on y = 0, the short base centred above at the height h.
        h = math.sqrt(leg * leg - ((big - small) / 2) ** 2)
        assert abs(h - round(h)) < 1e-9
        assert int(right) == (round(h) if "สูงกี่" in stem else (small + big) * round(h) // 2)
        stem, right, _ = _q("pythagoras_two_step_m2", seed)
        ab, ac, ad = _ints(stem)[:3]
        bc, bd = math.sqrt(ac * ac - ab * ab), math.sqrt(ad * ad - ab * ab)
        assert round(bd - bc, 9) == int(right)


# ── สถิติ ──

def test_statistics():
    for seed in SEEDS:
        stem, right, _ = _q("mean_missing_value_m2", seed)
        n = _ints(stem)[0]
        known = _ints(stem.split("ได้แก่")[1].split("และ x")[0])
        mean = int(re.search(r"เท่ากับ (\d+)", stem).group(1))
        assert Fraction(sum(known) + int(right), n) == mean and len(known) == n - 1
        stem, right, _ = _q("median_even_m2", seed)
        data = _ints(stem.split("ได้แก่")[1].split("มัธยฐาน")[0])
        assert Fraction(right) == Fraction(median(data))
        stem, right, _ = _q("class_interval_m2", seed)
        classes = [tuple(int(v) for v in c.split("–")) for c in re.findall(r"\d+–\d+", stem.split("อันตรภาคชั้น ")[1])]
        if "กว้าง" in stem:
            assert int(right) == classes[1][0] - classes[0][0]
        else:
            lo, hi = (int(v) for v in re.search(r"ชั้น (\d+)–(\d+) เท่ากับ", stem).groups())
            expected = Fraction(lo + hi, 2) if "จุดกึ่งกลาง" in stem else Fraction(hi) + Fraction(1, 2)
            assert Fraction(right) == expected
        stem, right, _ = _q("combined_mean_m2", seed)
        n1, m1, n2, m2 = _ints(stem)[:4]
        assert Fraction(n1 * m1 + n2 * m2, n1 + n2) == int(right)
        stem, right, _ = _q("frequency_percent_m2", seed)
        total = _ints(stem)[0]
        if "คิดเป็นร้อยละ" in stem:
            f = _ints(stem)[1]
            assert Fraction(f * 100, total) == int(right)
        else:
            pct = int(re.search(r"ร้อยละ (\d+)", stem).group(1))
            assert Fraction(pct * total, 100) == int(right)


# ── การให้เหตุผลทางเรขาคณิต ──

def test_reasoning():
    for seed in SEEDS:
        stem, right, _ = _q("right_triangle_acute_m2", seed)
        (m1, c1), (m2, c2) = (_lin(e) for e in re.findall(r"\(?(\d*x(?: [+−] \d+)?)\)?°", stem))
        xv = Fraction(90 - c1 - c2, m1 + m2)
        assert xv.denominator == 1
        assert int(right) == (xv if "ค่า x" in stem else m1 * xv + c1)
        stem, right, _ = _q("triangle_exterior_sum_m2", seed)
        ea, eb = (int(v) for v in re.findall(r"(\d+)°", stem)[:2])
        ec = 360 - ea - eb
        assert int(right) == (ec if "มุมภายนอกที่จุด C" in stem else 180 - ec)
        stem, right, _ = _q("perpendicular_bisector_m2", seed)
        e1, e2 = re.search(r"PA = (.+?) เซนติเมตร และ PB = (.+?) เซนติเมตร", stem).groups()
        (m1, c1), (m2, c2) = _lin(e1), _lin(e2)
        xv = Fraction(c2 - c1, m1 - m2)
        assert int(right) == (xv if "ค่า x" in stem else m1 * xv + c1)
        stem, right, _ = _q("largest_angle_side_m2", seed)
        ab, bc, ca = _ints(stem)[:3]
        # Lay the triangle out and measure every angle.
        B, C = (0.0, 0.0), (float(bc), 0.0)
        ax = (ab * ab + bc * bc - ca * ca) / (2 * bc)
        A = (ax, math.sqrt(ab * ab - ax * ax))
        size = {"∠A": _angle(A, B, C), "∠B": _angle(B, A, C), "∠C": _angle(C, A, B)}
        pick = (max if "ใหญ่ที่สุด" in stem else min)(size, key=size.get)
        assert right == pick
        stem, right, _ = _q("complement_supplement_algebra_m2", seed)
        n = _ints(stem)[0]
        a = int(right)
        if "มุมประกอบมุมฉาก" in stem:
            assert a == n * (90 - a)
        elif "เท่าของมุมประกอบมุมตรง" in stem:
            assert a == n * (180 - a)
        else:
            assert a - (180 - a) == n
