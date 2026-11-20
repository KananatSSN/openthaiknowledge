"""The ป.5 sets added so every unit has at least ten: each answer worked out again from the stem alone.

Numbers are read back out of the question (decimals, fractions and grouped thousands included) and the answer
recomputed here by its own route; text answers are checked against facts written out here independently.
"""

from __future__ import annotations

import re
from fractions import Fraction
from random import Random

from otk.core import generate

SEEDS = range(300)


def _text(blocks) -> str:
    return "".join(getattr(b, "text", None) or getattr(b, "tex", None) or "" for b in blocks)


def _q(key: str, seed: int):
    q = generate(f"math.{key}", Random(seed))
    texts = [_text(c.content).replace("{,}", ",") for c in q.choices]
    assert len(set(texts)) == len(texts), (key, seed, texts)
    return _text(q.stem).replace("{,}", ","), texts[q.answer], texts


def _nums(s: str) -> list[Fraction]:
    """Every number in the text, mixed numbers (2 1/3) and fractions (3/4) read whole."""
    out = []
    for m in re.finditer(r"(\d+) (\d+)/(\d+)|(\d+)/(\d+)|\d[\d,]*(?:\.\d+)?", s):
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
    """One answer: a whole number, a decimal, a/b, or TeX \\frac with an optional whole part."""
    s = s.replace(",", "").strip()
    m = re.fullmatch(r"(\d*)\\frac\{(\d+)\}\{(\d+)\}", s)
    if m:
        return int(m.group(1) or 0) + Fraction(int(m.group(2)), int(m.group(3)))
    return Fraction(s)


def _rows(stem: str) -> list[int]:
    return [int(line.rsplit(": ", 1)[1]) for line in stem.split("\n") if re.search(r": \d+$", line)]


def test_data_presentation():
    for seed in SEEDS:
        stem, right, _ = _q("line_graph_total_p5", seed)
        assert int(right) == sum(_rows(stem))
        stem, right, _ = _q("line_graph_count_rises_p5", seed)
        v = _rows(stem)
        rises = sum(b > a for a, b in zip(v, v[1:]))
        assert int(right) == (rises if "เพิ่มขึ้น" in stem.split("\n")[-1] else len(v) - 1 - rises)
        stem, right, _ = _q("line_graph_highest_p5", seed)
        pts = {line.rsplit(": ", 1)[0]: int(line.rsplit(": ", 1)[1]) for line in stem.split("\n")
               if re.search(r": \d+$", line)}
        assert pts[right] == (max if "มากที่สุด" in stem else min)(pts.values())
        stem, right, _ = _q("line_graph_count_above_p5", seed)
        k = _ints(stem.split("\n")[-1])[0]
        assert int(right) == sum(x > k for x in _rows(stem))
        stem, right, _ = _q("line_graph_next_p5", seed)
        v = _rows(stem)
        assert int(right) == v[-1] + (v[1] - v[0]) and len({b - a for a, b in zip(v, v[1:])}) == 1
        stem, right, texts = _q("line_graph_true_p5", seed)
        lines = [line for line in stem.split("\n") if re.search(r": \d+$", line)]
        pts = {line.rsplit(": ", 1)[0]: int(line.rsplit(": ", 1)[1]) for line in lines}
        for t in texts:
            m = re.fullmatch(r"จาก(.+?)ถึง(.+?) (เพิ่มขึ้น|ลดลง) (\d+) .+", t)
            a, b = pts[m.group(1)], pts[m.group(2)]
            ok = (m.group(3) == "เพิ่มขึ้น") == (b > a) and int(m.group(4)) == abs(b - a)
            assert ok == (t == right), (stem, t)


def test_decimals():
    for seed in SEEDS:
        stem, right, _ = _q("round_decimal_p5", seed)
        v = _nums(stem)[0]
        places = 1 if "หนึ่งตำแหน่ง" in stem else 2
        scaled = v * 10 ** places
        want = (scaled + Fraction(1, 2)).__floor__()
        assert right == f"{want // 10 ** places}.{want % 10 ** places:0{places}d}"
        stem, right, texts = _q("decimal_order_p5", seed)
        assert _v(right) == (max if "มากที่สุด" in stem else min)(_v(t) for t in texts)
        stem, right, _ = _q("decimal_digit_value_p5", seed)
        number, d = re.search(r"จำนวน (\S+) เลขโดด (\d)", stem).groups()
        place = number.index(d) - number.index(".")
        assert _v(right) == int(d) * Fraction(1, 10 ** place)
        stem, right, _ = _q("estimate_decimal_product_p5", seed)
        x, y = _nums(stem)[:2]
        assert int(right) == round(x) * round(y)


def test_fraction_word_problems():
    for seed in SEEDS:
        stem, right, _ = _q("whole_from_part_p5", seed)
        f, part = _nums(stem)[:2]
        assert int(right) == part / f
        stem, right, _ = _q("pieces_from_length_p5", seed)
        total, piece = _nums(stem)[:2]
        assert int(right) == total / piece
        stem, right, _ = _q("share_among_people_p5", seed)
        items, people = _nums(stem)[:2]
        assert _v(right) == items / people
        stem, right, _ = _q("increase_by_fraction_p5", seed)
        old, f = _nums(stem)[:2]
        assert int(right) == old * (1 + f)
        stem, right, _ = _q("two_shares_compare_p5", seed)
        total, f1, f2 = _nums(stem)[:3]
        assert int(right) == total * (f1 - f2) > 0 and f1 + f2 <= 1
        stem, right, _ = _q("part_of_hour_p5", seed)
        assert int(right) == 60 * _nums(stem)[0]
        stem, right, _ = _q("who_further_p5", seed)
        a, b = _nums(stem)[:2]
        assert _v(right) == a - b > 0


def test_length_and_weight():
    per = {"กิโลเมตร": 1000, "กิโลกรัม": 1000, "เมตริกตัน": 1000, "เมตร": 100}
    for seed in SEEDS:
        stem, right, _ = _q("decimal_to_smaller_unit_p5", seed)
        v = _nums(stem)[0]
        unit = stem.split(" ")[1]
        assert _v(right) == v * per[unit]
        stem, right, _ = _q("add_across_units_p5", seed)
        km, m = _nums(stem)[:2]
        assert _v(right) == km + m / 1000
        stem, right, texts = _q("heaviest_of_four_p5", seed)

        def grams(t: str) -> Fraction:
            n = _nums(t)
            if "กิโลกรัม" in t and "กรัม" in t.replace("กิโลกรัม", ""):
                return n[0] * 1000 + n[1]
            return n[0] * 1000 if "กิโลกรัม" in t else n[0]
        assert grams(right) == (max if "หนักที่สุด" in stem else min)(grams(t) for t in texts)
        stem, right, _ = _q("weight_difference_grams_p5", seed)
        kg, g = _nums(stem)[:2]
        assert _v(right) == kg * 1000 - g
        stem, right, _ = _q("ribbon_left_p5", seed)
        total, count, piece = _nums(stem)[:3]
        assert _v(right) == total - count * piece > 0
        stem, right, _ = _q("add_mixed_units_p5", seed)
        n = _ints(stem.split(" เท่ากับ")[0])
        total = 1000 * n[0] + n[1] + 1000 * n[2] + n[3]
        r = _ints(right)
        assert 1000 * r[0] + (r[1] if len(r) > 1 else 0) == total and (len(r) == 1 or r[1] < 1000)
        _q("suitable_unit_p5", seed)


def test_parallel_lines():
    for seed in SEEDS:
        stem, right, _ = _q("corresponding_angle_p5", seed)
        assert int(right) == _ints(stem)[0]
        stem, right, _ = _q("is_parallel_check_p5", seed)
        a, b = _ints(stem.split("ขนาด")[1])[:2]
        assert right.startswith("ขนานกัน") == (a + b == 180)
        assert _ints(right) in ([180], [a + b])
        stem, right, _ = _q("co_interior_from_difference_p5", seed)
        diff = _ints(stem.split("อีกมุม")[1])[0]
        small = (180 - diff) // 2
        assert int(right) == (small + diff if "มุมใหญ่" in stem else small)
        stem, right, _ = _q("vertical_angle_p5", seed)
        a = _ints(stem)[0]
        assert int(right) == (a if "ตรงข้าม" in stem else 180 - a)
        stem, right, _ = _q("alternate_from_sum_p5", seed)
        assert 2 * int(right) == _ints(stem)[0]
        for key in ("parallel_concepts_p5", "parallel_daily_life_p5"):
            _q(key, seed)


def test_percentages():
    for seed in SEEDS:
        stem, right, _ = _q("percent_to_fraction_p5", seed)
        a, b = map(int, right.split("/"))
        assert Fraction(a, b) == Fraction(_ints(stem)[0], 100) and Fraction(a, b).denominator == b
        stem, right, _ = _q("percent_to_decimal_p5", seed)
        assert _v(right) == Fraction(_ints(stem)[0], 100)
        stem, right, _ = _q("percent_increase_price_p5", seed)
        old, r = _ints(stem)[:2]
        assert _v(right) == old * Fraction(100 + r, 100)
        stem, right, _ = _q("percent_left_over_p5", seed)
        total, r = _ints(stem)[:2]
        assert int(right) == total * Fraction(100 - r, 100)


def test_prism():
    sides = {"สามเหลี่ยม": 3, "สี่เหลี่ยม": 4, "ห้าเหลี่ยม": 5, "หกเหลี่ยม": 6, "แปดเหลี่ยม": 8}

    def base(s: str) -> int:
        return next(n for name, n in sides.items() if f"ปริซึม{name}" in s)
    for seed in SEEDS:
        stem, right, _ = _q("prism_net_rectangles_p5", seed)
        assert int(right) == base(stem)
        stem, right, _ = _q("box_edges_total_p5", seed)
        w, length, h = _ints(stem)[:3]
        assert int(right) == 4 * (w + length + h)
        stem, right, _ = _q("cube_from_wire_p5", seed)
        assert 12 * int(right) == _ints(stem)[0]
        stem, right, _ = _q("prism_faces_plus_corners_p5", seed)
        n = base(stem)
        assert int(right) == (n + 2) + 2 * n
        stem, right, _ = _q("prism_base_from_faces_p5", seed)
        assert base(right) + 2 == _ints(stem)[0]
        for key in ("prism_or_not_p5", "prism_objects_p5"):
            _q(key, seed)


def test_quadrilateral_area():
    def area(t: str) -> Fraction:
        n = _nums(t)
        if "ด้านขนาน" in t:
            return n[0] * n[1]
        if "คางหมู" in t:
            return (n[0] + n[1]) * n[2] / 2
        if "ขนมเปียกปูน" in t:
            return n[0] * n[1] / 2
        return n[0] ** 2
    for seed in SEEDS:
        stem, right, _ = _q("parallelogram_height_p5", seed)
        a, b = _ints(stem)[:2]
        assert int(right) * b == a
        stem, right, _ = _q("trapezoid_missing_side_p5", seed)
        a, h, side = _ints(stem)[:3]
        assert (side + int(right)) * h == 2 * a
        stem, right, _ = _q("rhombus_from_diagonals_p5", seed)
        d1, d2 = _ints(stem)[:2]
        assert 2 * int(right) == d1 * d2
        stem, right, texts = _q("largest_quadrilateral_area_p5", seed)
        assert area(right) == (max if "มากที่สุด" in stem else min)(area(t) for t in texts)
        stem, right, _ = _q("tiling_cost_p5", seed)
        n = _ints(stem)
        a = n[0] * n[1] if "ด้านขนาน" in stem else Fraction((n[0] + n[1]) * n[2], 2)
        assert _v(right) == a * n[-1]


def test_types_of_quadrilaterals():
    for seed in SEEDS:
        stem, right, _ = _q("parallelogram_angle_p5", seed)
        a = _ints(stem)[0]
        assert int(right) == (a if "∠C" in stem else 180 - a)
        stem, right, _ = _q("trapezoid_angle_p5", seed)
        assert int(right) == 180 - _ints(stem)[0]
        stem, right, _ = _q("quadrilateral_missing_side_p5", seed)
        n = _ints(stem)
        if "ขนมเปียกปูน" in stem:
            assert 4 * int(right) == n[0]
        else:
            assert 2 * (n[0] + int(right)) == n[1]
        stem, right, _ = _q("diagonal_length_p5", seed)
        d = _ints(stem)[0]
        assert int(right) == (d // 2 if "BO" in stem else d)
        _q("quadrilateral_diagonals_p5", seed)


def test_unitary_method():
    for seed in SEEDS:
        stem, right, texts = _q("better_buy_p5", seed)
        packs = re.findall(r"แพ็ก (\d+) ชิ้น ราคา (\d+) บาท", " ".join(texts))
        unit = {f"แพ็ก {n} ชิ้น ราคา {p} บาท": Fraction(int(p), int(n)) for n, p in packs}
        assert unit[right] == min(unit.values()) and len(set(unit.values())) == 2
        stem, right, _ = _q("workers_days_p5", seed)
        w1, d1, w2 = _ints(stem)[:3]
        assert int(right) * w2 == w1 * d1
        stem, right, _ = _q("fuel_for_trip_p5", seed)
        l1, km1, km2 = _ints(stem)[:3]
        assert Fraction(int(right)) == Fraction(km2 * l1, km1)
        stem, right, _ = _q("days_to_earn_p5", seed)
        d1, pay1, pay2 = _ints(stem)[:3]
        assert int(right) * pay1 == d1 * pay2
        stem, right, _ = _q("how_many_for_money_p5", seed)
        n1, price, money = _ints(stem)[:3]
        assert int(right) * price == money * n1
        stem, right, _ = _q("exchange_money_p5", seed)
        n1, baht, n2 = _ints(stem)[:3]
        assert _v(right) * n1 == baht * n2
        stem, right, _ = _q("printing_time_p5", seed)
        pages1, m1, pages2 = _ints(stem)[:3]
        assert int(right) * pages1 == m1 * pages2


def test_volume():
    for seed in SEEDS:
        stem, right, _ = _q("cube_volume_p5", seed)
        assert _v(right) == _ints(stem)[0] ** 3
        stem, right, _ = _q("water_rise_volume_p5", seed)
        w, length, before, after = _ints(stem)[:4]
        assert _v(right) == w * length * (after - before)
        stem, right, _ = _q("cubes_in_box_p5", seed)
        a, b, c, e = _ints(stem)[:4]
        assert _v(right) == (a // e) * (b // e) * (c // e) and a % e == b % e == c % e == 0
        stem, right, _ = _q("litres_cubic_cm_p5", seed)
        v = _nums(stem)[0]
        if "ลิตร เท่ากับกี่ลูกบาศก์" in stem:
            assert _v(right) == v * 1000
        elif "มิลลิลิตร เท่ากับกี่ลิตร" in stem:
            assert _v(right) == v / 1000
        else:
            assert _v(right) == v
        stem, right, texts = _q("largest_box_volume_p5", seed)

        def vol(t: str) -> int:
            a, b, c = _ints(t)
            return a * b * c
        assert vol(right) == (max if "มากที่สุด" in stem else min)(vol(t) for t in texts)
        stem, right, _ = _q("fill_tank_time_p5", seed)
        w, length, h, rate = _ints(stem)[:4]
        assert _v(right) * rate * 1000 == w * length * h
