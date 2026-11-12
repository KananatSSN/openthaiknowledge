"""The ป.6 sets added so every unit has at least ten: each answer worked out again from the stem alone.

Numbers are read back out of the question (decimals, fractions and grouped thousands included) and the answer
recomputed here by its own route; text answers are checked against facts written out here independently.
"""

from __future__ import annotations

import re
from fractions import Fraction
from math import gcd, isqrt
from random import Random

from otk.core import generate

SEEDS = range(300)
PI = Fraction(22, 7)


def _text(blocks) -> str:
    return "".join(getattr(b, "text", None) or getattr(b, "tex", None) or "" for b in blocks)


def _q(key: str, seed: int):
    q = generate(f"math.{key}", Random(seed))
    texts = [_text(c.content).replace("{,}", ",") for c in q.choices]
    assert len(set(texts)) == len(texts), (key, seed, texts)
    return _text(q.stem).replace("{,}", ","), texts[q.answer], texts


def _nums(s: str) -> list[Fraction]:
    """Every number in the text, mixed numbers (2 1/3), fractions (3/4) and TeX \\frac read whole."""
    s = re.sub(r"(\d*)\\frac\{(\d+)\}\{(\d+)\}", lambda m: f" {m.group(1) or ''} {m.group(2)}/{m.group(3)} ", s)
    out = []
    for m in re.finditer(r"(\d+) +(\d+)/(\d+)|(\d+)/(\d+)|\d[\d,]*(?:\.\d+)?", s):
        if m.group(1):
            out.append(int(m.group(1)) + Fraction(int(m.group(2)), int(m.group(3))))
        elif m.group(4):
            out.append(Fraction(int(m.group(4)), int(m.group(5))))
        else:
            out.append(Fraction(m.group(0).replace(",", "")))
    return out


def _ints(s: str) -> list[int]:
    return [int(v) for v in re.findall(r"\d+", s.replace(",", ""))]


def _v(s: str) -> Fraction:
    """One answer: a whole number, a decimal, or TeX \\frac with an optional whole part."""
    s = s.replace(",", "").strip()
    m = re.fullmatch(r"(\d*)\\frac\{(\d+)\}\{(\d+)\}", s)
    if m:
        return int(m.group(1) or 0) + Fraction(int(m.group(2)), int(m.group(3)))
    return Fraction(s)


def _is_prime(n: int) -> bool:
    return n > 1 and all(n % k for k in range(2, isqrt(n) + 1))


def _factors(n: int) -> list[int]:
    return [k for k in range(1, n + 1) if n % k == 0]


def _expr(tex: str) -> Fraction:
    """Evaluate +, −, ×, ÷ and brackets with Python's own precedence, on exact fractions."""
    s = tex.replace("\\times", "*").replace("\\div", "/").replace("[", "(").replace("]", ")")
    s = re.sub(r"(\d+(?:\.\d+)?)", r"Fraction('\1')", s)
    assert re.fullmatch(r"[Fraction('\d.)\s+\-*/()]+", s), s
    return eval(s, {"Fraction": Fraction})  # noqa: S307 - numbers and operators only, checked above


def test_circles():
    for seed in SEEDS:
        stem, right, _ = _q("radius_diameter_p6", seed)
        v = _ints(stem)[0]
        assert int(right) == (2 * v if "รัศมียาว" in stem.split("เส้นผ่าน")[0] else v // 2)
        stem, right, _ = _q("circumference_from_diameter_p6", seed)
        assert _v(right) == PI * _ints(stem)[0]
        stem, right, _ = _q("semicircle_area_p6", seed)
        r = _ints(stem)[0]
        assert _v(right) == PI * r * r / 2
        stem, right, _ = _q("semicircle_perimeter_p6", seed)
        d = _ints(stem)[0]
        assert _v(right) == PI * d / 2 + d
        stem, right, _ = _q("wheel_turns_p6", seed)
        r, dist = _ints(stem)[:2]
        assert _v(right) == dist / (2 * PI * r)
        stem, right, _ = _q("ring_area_p6", seed)
        big, r = _ints(stem)[:2]
        assert _v(right) == PI * (big * big - r * r)


def test_decimals():
    for seed in SEEDS:
        stem, right, _ = _q("decimal_missing_factor_p6", seed)
        b, p = _nums(stem.split("=")[0].replace("\\square", ""))[0], _nums(stem.split("=")[1])[0]
        assert _v(right) * b == p
        stem, right, _ = _q("round_quotient_p6", seed)
        a, b = _ints(stem)[:2]
        want = (Fraction(a, b) * 100 + Fraction(1, 2)).__floor__()
        assert right == f"{want // 100}.{want % 100:02d}"
        stem, right, _ = _q("price_per_kilo_p6", seed)
        kg, paid = _nums(stem)[:2]
        assert _v(right) == paid / kg
        stem, right, _ = _q("decimal_rectangle_area_p6", seed)
        w, length = _nums(stem)[:2]
        assert _v(right) == w * length


def test_fractions_and_mixed_numbers():
    for seed in SEEDS:
        stem, right, _ = _q("mixed_times_whole_p6", seed)
        m, k = _nums(stem.removeprefix("จงหาผลคูณ"))[:2]
        assert _v(right) == m * k
        stem, right, _ = _q("mixed_divide_whole_p6", seed)
        m, k = _nums(stem.removeprefix("จงหาผลหาร"))[:2]
        assert _v(right) == m / k
        stem, right, _ = _q("part_of_part_p6", seed)
        f1, f2 = _nums(stem)[:2]
        assert _v(right) == f1 * f2
        stem, right, texts = _q("largest_fraction_p6", seed)
        assert _v(right) == (max if "มากที่สุด" in stem else min)(_v(t) for t in texts)
        stem, right, _ = _q("reciprocal_p6", seed)
        assert _v(right) * _nums(stem.removeprefix("ส่วนกลับของจำนวนนี้คือข้อใด"))[0] == 1
        stem, right, _ = _q("fraction_missing_factor_p6", seed)
        left, prod = stem.removeprefix("จำนวนใดเติมใน □ แล้วทำให้ประโยคเป็นจริง").split("=")
        assert _v(right) * _nums(left)[0] == _nums(prod)[0]
        stem, right, _ = _q("mixed_to_improper_p6", seed)
        m = re.fullmatch(r"\\frac\{(\d+)\}\{(\d+)\}", right)
        assert m and Fraction(int(m.group(1)), int(m.group(2))) == _nums(stem.removeprefix("เขียนจำนวนคละนี้เป็นเศษเกิน"))[0]


def test_gcd_and_lcm():
    for seed in SEEDS:
        stem, right, _ = _q("common_factors_count_p6", seed)
        a, b = _ints(stem)[:2]
        assert int(right) == len(_factors(gcd(a, b)))
        stem, right, texts = _q("common_multiple_p6", seed)
        a, b = _ints(stem)[:2]
        assert [int(t) % a == 0 and int(t) % b == 0 for t in texts].count(True) == 1
        assert int(right) % a == 0 and int(right) % b == 0
        stem, right, _ = _q("tiles_to_square_p6", seed)
        a, b = _ints(stem)[:2]
        side = a * b // gcd(a, b)
        assert int(right) == (side // a) * (side // b)
        stem, right, _ = _q("buses_together_p6", seed)
        a, b, h = _ints(stem)[:3]
        lcm = a * b // gcd(a, b)
        hh, mm = divmod(h * 60 + lcm, 60)
        assert right == f"{hh}.{mm:02d} น."


def test_order_of_ops():
    for seed in SEEDS:
        for key in ("ooo_decimal_p6", "ooo_division_first_p6", "ooo_nested_p6"):
            stem, right, _ = _q(key, seed)
            assert _v(right) == _expr(stem.removeprefix("จงหาค่าของนิพจน์"))
        stem, right, texts = _q("ooo_true_statement_p6", seed)
        for t in texts:
            lhs, rhs = t.replace("×", "\\times").split(" = ")
            assert (_expr(lhs) == int(rhs)) == (t == right), t
        stem, right, _ = _q("ooo_missing_number_p6", seed)
        k, c, total = _ints(stem)[:3]
        assert k * int(right) + c == total
        stem, right, _ = _q("change_after_shopping_p6", seed)
        n1, p1, n2, p2, paid = _ints(stem)[:5]
        assert int(right) == paid - n1 * p1 - n2 * p2 > 0


def test_patterns():
    for seed in SEEDS:
        stem, right, _ = _q("pattern_next_term_p6", seed)
        v = _ints(stem.split("...")[0])
        assert int(right) == v[-1] + (v[1] - v[0])
        stem, right, _ = _q("pattern_missing_middle_p6", seed)
        parts = stem.split(" จำนวนใน")[0].split(", ")
        i = parts.index("□")
        nums = [int(p) if p != "□" else None for p in parts]
        known = [(j, x) for j, x in enumerate(nums) if x is not None]
        (j0, x0), (j1, x1) = known[0], known[1]
        step = (x1 - x0) // (j1 - j0)
        assert int(right) == x0 + step * (i - j0)
        stem, right, _ = _q("pattern_multiply_p6", seed)
        v = _ints(stem.split("...")[0])
        assert _v(right) == v[-1] * (v[1] // v[0])
        stem, right, _ = _q("pattern_which_term_p6", seed)
        v = _ints(stem.split("...")[0])
        value = _ints(stem.split("จำนวน")[-1])[0]
        assert v[0] + (v[1] - v[0]) * (int(right) - 1) == value
        stem, right, _ = _q("square_numbers_p6", seed)
        assert int(right) == _ints(stem.split("พจน์ที่")[1])[0] ** 2
        stem, right, _ = _q("growing_difference_p6", seed)
        v = _ints(stem.split("...")[0])
        d = [b - a for a, b in zip(v, v[1:])]
        assert all(y - x == 1 for x, y in zip(d, d[1:])) and int(right) == v[-1] + d[-1] + 1
        stem, right, _ = _q("repeating_colour_p6", seed)
        shown = stem.split("ซ้ำ ")[1].split(", ...")[0].split(", ")
        cycle = shown[: len(shown) // 2]
        n = _ints(stem.split("ลูกที่")[1])[0]
        assert right == cycle[(n - 1) % len(cycle)]


def test_percentages():
    for seed in SEEDS:
        stem, right, _ = _q("whole_from_percent_p6", seed)
        part, r = _ints(stem)[:2]
        assert int(right) * r == part * 100
        stem, right, _ = _q("vat_p6", seed)
        assert _v(right) == _ints(stem)[0] * Fraction(107, 100)
        stem, right, _ = _q("discount_percent_p6", seed)
        price, sale = _ints(stem)[:2]
        assert int(right) == (price - sale) * 100 // price and (price - sale) * 100 % price == 0
        stem, right, _ = _q("cost_from_profit_p6", seed)
        sale, r = _ints(stem)[:2]
        assert _v(right) * (100 + r) == sale * 100
        stem, right, _ = _q("compare_offers_p6", seed)
        price, r, off = _ints(stem)[:3]
        a, b = price * Fraction(100 - r, 100), price - off
        assert right == (f"ร้านแรก จ่าย {int(a):,} บาท" if a < b else f"ร้านที่สอง จ่าย {b:,} บาท")


def test_pie_chart():
    def rows(stem: str) -> dict[str, int]:
        return {m.group(1): int(m.group(2)) for m in re.finditer(r"^(\S+): (?:ร้อยละ )?(\d+)", stem, flags=re.M)}
    for seed in SEEDS:
        stem, right, _ = _q("pie_angle_from_percent_p6", seed)
        assert int(right) == _ints(stem)[0] * Fraction(360, 100)
        stem, right, _ = _q("pie_percent_from_angle_p6", seed)
        assert int(right) == _ints(stem)[0] * Fraction(100, 360)
        stem, right, _ = _q("pie_total_from_part_p6", seed)
        sport = re.search(r"ชอบ(\S+?)มี (\d+) คน", stem)
        p = rows(stem)[sport.group(1)]
        assert sum(rows(stem).values()) == 100 and int(right) * p == int(sport.group(2)) * 100
        stem, right, _ = _q("pie_missing_percent_p6", seed)
        assert int(right) + sum(rows(stem).values()) == 100
        stem, right, _ = _q("pie_largest_part_p6", seed)
        r = rows(stem)
        assert sum(r.values()) == 360 and r[right] == (max if "มากที่สุด" in stem else min)(r.values())
        stem, right, _ = _q("pie_two_parts_p6", seed)
        r = rows(stem)
        total = _ints(stem.split("ทั้งหมด")[-1])[0]
        x, y = re.search(r"ชอบ(\S+?)และ(\S+?)รวมกัน", stem).groups()
        assert int(right) * 100 == total * (r[x] + r[y])


def test_prime_numbers():
    def factorise(n: int) -> list[int]:
        out, k = [], 2
        while n > 1:
            while n % k == 0:
                out.append(k)
                n //= k
            k += 1
        return out
    for seed in SEEDS:
        stem, right, texts = _q("prime_factorisation_p6", seed)
        n = _ints(stem)[0]
        for t in texts:
            fs = _ints(t)
            ok = all(_is_prime(f) for f in fs) and eval("*".join(map(str, fs))) == n  # noqa: S307
            assert ok == (t == right), t
        stem, right, _ = _q("largest_prime_factor_p6", seed)
        assert int(right) == max(factorise(_ints(stem)[0]))
        stem, right, _ = _q("sum_of_primes_p6", seed)
        a, b = _ints(stem)[:2]
        assert int(right) == sum(k for k in range(a, b + 1) if _is_prime(k))
        stem, right, _ = _q("next_prime_p6", seed)
        n = _ints(stem)[0]
        assert int(right) == next(k for k in range(n + 1, 10 * n) if _is_prime(k))
        stem, right, _ = _q("count_factors_p6", seed)
        assert int(right) == len(_factors(_ints(stem)[0]))


def test_ratio_and_scale():
    for seed in SEEDS:
        stem, right, _ = _q("scale_to_km_p6", seed)
        scale, cm = _ints(stem.split(":")[1])[:2]
        assert _v(right) == Fraction(cm * scale, 100_000)
        stem, right, _ = _q("scale_to_map_p6", seed)
        scale, metres = _ints(stem.split(":")[1])[:2]
        assert int(right) * scale == metres * 100
        stem, right, texts = _q("ratio_lowest_terms_p6", seed)
        a, b = _ints(stem)[:2]
        for t in texts:
            x, y = _ints(t)
            assert (gcd(x, y) == 1 and Fraction(x, y) == Fraction(a, b)) == (t == right), t
        stem, right, _ = _q("ratio_other_part_p6", seed)
        a, b, boys = _ints(stem)[:3]
        assert int(right) * a == boys * b
        stem, right, _ = _q("share_three_ways_p6", seed)
        total, *parts = _ints(stem)[:4]
        names = re.search(r"ให้(\S+) (\S+) และ(\S+?)ในอัตราส่วน", stem).groups()
        who = re.search(r"\d+ : \d+ : \d+ (\S+?)ได้เงิน", stem).group(1)
        i = names.index(who)
        assert _v(right) * sum(parts) == total * parts[i]


def test_solids():
    sides = {"สามเหลี่ยม": 3, "สี่เหลี่ยม": 4, "ห้าเหลี่ยม": 5, "หกเหลี่ยม": 6, "แปดเหลี่ยม": 8}
    for seed in SEEDS:
        stem, right, _ = _q("pyramid_counts_p6", seed)
        n = next(v for k, v in sides.items() if f"ฐาน{k}มี" in stem)
        want = 2 * n if "มีสัน" in stem else n + 1
        assert int(right) == want
        stem, right, _ = _q("euler_missing_count_p6", seed)
        given = dict(re.findall(r"มี(หน้า|จุดยอด|สัน) (\d+)", stem))
        f, v, e = (int(given[k]) if k in given else None for k in ("หน้า", "จุดยอด", "สัน"))
        if f is None:
            assert int(right) == 2 + e - v
        elif v is None:
            assert int(right) == 2 + e - f
        else:
            assert int(right) == f + v - 2
        for key in ("solid_from_description_p6", "curved_surface_p6", "objects_as_solids_p6", "cross_section_p6"):
            _q(key, seed)


def test_triangle_area():
    for seed in SEEDS:
        stem, right, _ = _q("right_triangle_area_p6", seed)
        a, b = _ints(stem)[:2]
        assert 2 * int(right) == a * b
        stem, right, texts = _q("largest_triangle_area_p6", seed)

        def area(t: str) -> Fraction:
            b, h = _ints(t)
            return Fraction(b * h, 2)
        assert area(right) == (max if "มากที่สุด" in stem else min)(area(t) for t in texts)
        stem, right, _ = _q("rectangle_minus_triangle_p6", seed)
        h, w, base, h2 = _ints(stem)[:4]
        assert h == h2 and int(right) == w * h - base * h // 2
        stem, right, _ = _q("two_triangles_one_base_p6", seed)
        base, h1, h2 = _ints(stem)[:3]
        assert 2 * int(right) == base * (h2 - h1)


def test_types_of_triangles():
    for seed in SEEDS:
        stem, right, _ = _q("classify_by_sides_p6", seed)
        a, b, c = _ints(stem)[:3]
        kinds = {1: "รูปสามเหลี่ยมด้านเท่า", 2: "รูปสามเหลี่ยมหน้าจั่ว", 3: "รูปสามเหลี่ยมด้านไม่เท่า"}
        assert right == kinds[len({a, b, c})] and max(a, b, c) < a + b + c - max(a, b, c)
        stem, right, _ = _q("isosceles_base_angle_p6", seed)
        assert 2 * int(right) + _ints(stem)[0] == 180
        stem, right, _ = _q("isosceles_top_angle_p6", seed)
        assert int(right) + 2 * _ints(stem)[0] == 180
        stem, right, _ = _q("right_triangle_other_angle_p6", seed)
        assert int(right) + _ints(stem)[0] == 90
        stem, right, _ = _q("isosceles_side_from_perimeter_p6", seed)
        n = _ints(stem)
        if "ด้านเท่า" in stem:
            assert 3 * int(right) == n[0]
        else:
            assert n[0] + 2 * int(right) == n[1] and 2 * int(right) > n[0]
        _q("triangle_facts_p6", seed)


def test_volume_and_surface_area():
    for seed in SEEDS:
        stem, right, _ = _q("box_surface_area_p6", seed)
        w, length, h = _ints(stem)[:3]
        assert _v(right) == 2 * (w * length + w * h + length * h)
        stem, right, _ = _q("cube_edge_from_volume_p6", seed)
        assert int(right) ** 3 == _ints(stem)[0]
        stem, right, _ = _q("open_box_surface_p6", seed)
        w, length, h = _ints(stem)[:3]
        assert _v(right) == w * length + 2 * (w * h + length * h)
        stem, right, _ = _q("box_doubled_p6", seed)
        w, length, h = _ints(stem)[:3]
        assert _v(right) == 8 * w * length * h
        stem, right, _ = _q("height_from_base_area_p6", seed)
        base, v = _ints(stem)[:2]
        assert int(right) * base == v
        stem, right, _ = _q("cube_edge_from_surface_p6", seed)
        assert 6 * int(right) ** 2 == _ints(stem)[0]
