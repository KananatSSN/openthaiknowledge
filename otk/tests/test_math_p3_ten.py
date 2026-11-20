"""The ป.3 sets added so every unit has at least ten: each answer worked out again from the stem alone.

Numbers are read back out of the question and the answer recomputed here by its own route; text answers are
checked against facts written out here independently (place names, weekdays, axes of symmetry).
"""

from __future__ import annotations

import re
from random import Random

from otk.core import generate

SEEDS = range(300)


def _text(blocks) -> str:
    return "".join(getattr(b, "text", None) or getattr(b, "tex", None) or "" for b in blocks)


def _q(key: str, seed: int):
    q = generate(f"math.{key}", Random(seed))
    texts = [_text(c.content) for c in q.choices]
    assert len(set(texts)) == len(texts), (key, seed, texts)
    return _text(q.stem), texts[q.answer], texts


def _ints(s: str) -> list[int]:
    return [int(v) for v in re.findall(r"\d+", s.replace(",", ""))]


def _eval(expr: str) -> int:
    expr = expr.replace("×", "*").replace("÷", "//").replace("−", "-").replace("\\times", "*").replace("\\div", "//")
    assert re.fullmatch(r"[\d\s+\-*/()]+", expr), expr
    return eval(expr)  # noqa: S307 - digits and operators only, checked above


def _table(stem: str) -> dict[str, int]:
    rows = {}
    for line in stem.split("\n")[2:]:
        if " | " in line:
            label, value = line.split(" | ")
            rows[label.strip()] = int(value)
    return rows


PLACES = ["หลักหน่วย", "หลักสิบ", "หลักร้อย", "หลักพัน", "หลักหมื่น"]
WEEKDAYS = ["วันอาทิตย์", "วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์"]
AXES = {"รูปสี่เหลี่ยมจัตุรัส": 4, "รูปสี่เหลี่ยมผืนผ้า": 2, "รูปสามเหลี่ยมด้านเท่า": 3, "รูปสามเหลี่ยมหน้าจั่ว": 1,
        "รูปหกเหลี่ยมด้านเท่า": 6, "รูปห้าเหลี่ยมด้านเท่า": 5, "รูปสี่เหลี่ยมขนมเปียกปูน": 2}


def _thai_number(words: str) -> int:
    """Read a Thai number up to 99,999 back (the inverse of story.thai_words, written out independently)."""
    digits = {"หนึ่ง": 1, "เอ็ด": 1, "สอง": 2, "ยี่": 2, "สาม": 3, "สี่": 4, "ห้า": 5, "หก": 6, "เจ็ด": 7,
              "แปด": 8, "เก้า": 9}
    places = {"หมื่น": 10000, "พัน": 1000, "ร้อย": 100, "สิบ": 10}
    total, pending, i = 0, None, 0
    while i < len(words):
        for word in sorted([*digits, *places], key=len, reverse=True):
            if words.startswith(word, i):
                if word in digits:
                    pending = digits[word]
                else:
                    total += (pending if pending is not None else 1) * places[word]
                    pending = None
                i += len(word)
                break
        else:
            raise AssertionError(words[i:])
    return total + (pending or 0)


def test_place_value():
    for seed in SEEDS:
        stem, right, _ = _q("more_less_thousand_p3", seed)
        n, step = _ints(stem)
        assert int(right) == (n + step if "มากกว่า" in stem else n - step)
        stem, right, texts = _q("number_from_digits_p3", seed)
        digits = _ints(stem.split("หลักละ")[0])
        from itertools import permutations
        made = [int("".join(map(str, p))) for p in permutations(digits) if p[0] != 0]
        assert int(right) == (max(made) if "มากที่สุด" in stem else min(made))
        stem, right, _ = _q("number_between_p3", seed)
        a, b = _ints(stem)
        assert a < int(right) < b
        stem, right, _ = _q("digit_place_p3", seed)
        n, d = _ints(stem)
        assert right == PLACES[len(str(n)) - 1 - str(n).index(str(d))]
        stem, right, _ = _q("zeros_in_number_p3", seed)
        words = stem.removeprefix("จำนวน").split(" เขียนเป็น")[0]
        assert int(right) == str(_thai_number(words)).count("0")


def test_add_and_subtract():
    for seed in SEEDS:
        stem, right, _ = _q("add_three_four_digit_p3", seed)
        assert int(right) == sum(_ints(stem))
        stem, right, texts = _q("check_addsub_p3", seed)
        checked = stem.removeprefix("ข้อใดใช้ตรวจคำตอบของ ")
        lhs = checked.split(" = ")[0]
        for t in texts:
            tl, tr = t.split(" = ")
            ok = _eval(tl) == int(tr) and ("+" in lhs) != ("+" in tl) and set(_ints(t)) == set(_ints(checked))
            assert ok == (t == right), (stem, t)
        stem, right, _ = _q("how_many_more_p3", seed)
        a, b = _ints(stem)
        assert int(right) == a - b
        stem, right, _ = _q("missing_digit_add_p3", seed)
        left, s = stem.split(" = ")
        shown, b = left.split(" + ")
        s = _ints(s)[0]
        a = str(s - int(b))
        assert len(a) == len(shown) and all(x == y or x == "□" for x, y in zip(shown, a))
        assert right == a[shown.index("□")]
        stem, right, texts = _q("largest_result_p3", seed)
        assert _eval(right) == (max if "มากที่สุด" in stem else min)(_eval(t) for t in texts)
        stem, right, _ = _q("money_left_two_buys_p3", seed)
        have, a, b = _ints(stem)
        assert int(right) == have - a - b
        stem, right, _ = _q("compare_two_sums_p3", seed)
        a, b, c, d = _ints(stem)
        assert int(right) == a + b - c - d > 0


def test_patterns():
    for seed in SEEDS:
        stem, right, _ = _q("pattern_next_p3", seed)
        terms = _ints(stem)
        d = terms[1] - terms[0]
        assert all(y - x == d for x, y in zip(terms, terms[1:])) and int(right) == terms[-1] + d
        stem, right, _ = _q("pattern_far_term_p3", seed)
        nums = _ints(stem)
        terms, n = nums[:4], nums[4]
        d = terms[1] - terms[0]
        assert int(right) == terms[0] + d * (n - 1)
        stem, right, _ = _q("pattern_two_missing_p3", seed)
        parts = stem.split(": ")[1].split(", ")
        known = [(i, int(p)) for i, p in enumerate(parts) if p != "□"]
        (i0, v0), (i1, v1) = known[0], known[1]
        step = (v1 - v0) // (i1 - i0)
        gaps = [v0 + step * (i - i0) for i, p in enumerate(parts) if p == "□"]
        assert right == f"{gaps[0]} และ {gaps[1]}"
        stem, right, _ = _q("pattern_four_shapes_p3", seed)
        shapes = stem.split("แบบรูป ")[1].split("...")[0].split()
        assert right == shapes[(_ints(stem)[-1] - 1) % 4]
        stem, right, _ = _q("pattern_spending_p3", seed)
        have, per, days = _ints(stem)
        assert int(right) == have - per * days
        stem, right, texts = _q("pattern_member_p3", seed)
        terms = _ints(stem)
        d = terms[1] - terms[0]
        members = [int(t) for t in texts if (int(t) - terms[0]) % d == 0 and int(t) >= terms[0]]
        assert members == [int(right)]


def test_multiply_and_divide():
    for seed in SEEDS:
        stem, right, _ = _q("multiply_by_tens_p3", seed)
        assert int(right) == _eval(stem.removeprefix("จงหาผลคูณ"))
        stem, right, texts = _q("largest_product_p3", seed)
        assert _eval(right) == (max if "มากที่สุด" in stem else min)(_eval(t) for t in texts)
        stem, right, _ = _q("divide_by_ten_p3", seed)
        assert int(right) == _eval(stem.removeprefix("จงหาผลหาร"))
        stem, right, _ = _q("missing_divisor_p3", seed)
        n, q = _ints(stem)
        assert int(right) * q == n
        stem, right, _ = _q("share_equally_p3", seed)
        n, b = _ints(stem)
        assert int(right) * b == n
        stem, right, texts = _q("divides_evenly_p3", seed)
        b = _ints(stem)[0]
        assert [int(t) % b == 0 for t in texts].count(True) == 1 and int(right) % b == 0
        stem, right, texts = _q("largest_quotient_p3", seed)
        assert _eval(right) == (max if "มากที่สุด" in stem else min)(_eval(t) for t in texts)
        stem, right, _ = _q("half_of_p3", seed)
        assert 2 * int(right) == _ints(stem)[0]


def test_tables():
    for seed in SEEDS:
        stem, right, _ = _q("table_range_p3", seed)
        rows = _table(stem)
        assert int(right) == max(rows.values()) - min(rows.values())
        stem, right, _ = _q("table_order_p3", seed)
        rows = _table(stem)
        ordered = sorted(rows, key=rows.get, reverse="มากไปน้อย" in stem)
        assert right == ordered[1 if stem.endswith("สอง") else 2]
        stem, right, _ = _q("table_count_above_p3", seed)
        rows = _table(stem)
        k = _ints(stem.split("\n")[-1])[0]
        assert int(right) == sum(v > k for v in rows.values())
        stem, right, _ = _q("table_two_rows_p3", seed)
        rows = _table(stem)
        question = stem.split("\n")[-1]
        named = sorted((r for r in rows if r in question), key=question.index)
        x, y, z = named
        assert int(right) == rows[x] + rows[y] - rows[z]
        stem, right, texts = _q("table_true_statement_p3", seed)
        rows = _table(stem)
        for t in texts:
            first, second = t.split("มากกว่า")
            x = next(r for r in rows if r in first)
            y = next(r for r in rows if r in second)
            assert (rows[x] - rows[y] == _ints(second.split(y)[-1])[0]) == (t == right), t


def test_money_and_time():
    for seed in SEEDS:
        stem, right, _ = _q("unit_price_p3", seed)
        n, total = _ints(stem)
        assert int(right) * n == total
        stem, right, _ = _q("buy_several_p3", seed)
        n, each = _ints(stem)
        assert int(right) == n * each
        stem, right, _ = _q("daily_saving_p3", seed)
        per, days = _ints(stem)
        assert int(right) == per * days
        stem, right, _ = _q("baht_satang_add_p3", seed)

        def satang(s: str) -> int:
            n = _ints(s)
            return 100 * n[0] + (n[1] if len(n) > 1 else 0)
        parts = re.findall(r"\d+ บาท(?: \d+ สตางค์)?", stem)
        assert satang(right) == satang(parts[0]) + satang(parts[1])
        stem, right, _ = _q("minutes_to_hours_p3", seed)
        total = _ints(stem)[0]
        h, m = _ints(right)
        assert 60 * h + m == total and m < 60
        stem, right, _ = _q("hours_to_minutes_p3", seed)
        h, m = _ints(stem)
        assert int(right) == 60 * h + m
        stem, right, _ = _q("days_to_hours_p3", seed)
        nums = _ints(stem)
        assert int(right) == 24 * nums[0] + (nums[1] if len(nums) > 1 else 0)
        stem, right, texts = _q("longest_activity_p3", seed)
        spans = {}
        for line in stem.split("\n")[:-1]:
            name, times = line.split(" ", 1)
            h1, m1, h2, m2 = _ints(times)
            spans[name] = (60 * h2 + m2) - (60 * h1 + m1)
        assert spans[right] == (max if "นานที่สุด" in stem else min)(spans.values())
        stem, right, _ = _q("calendar_date_weekday_p3", seed)
        d1, d2 = _ints(stem)
        start = next(w for w in WEEKDAYS if f"ตรงกับ{w}" in stem)
        assert right == WEEKDAYS[(WEEKDAYS.index(start) + d2 - d1) % 7]
        _q("year_facts_p3", seed)


def test_measures():
    for seed in SEEDS:
        stem, right, _ = _q("km_m_to_m_p3", seed)
        km, m = _ints(stem)
        assert int(right) == 1000 * km + m
        stem, right, _ = _q("cm_mm_to_mm_p3", seed)
        cm, mm = _ints(stem)
        assert int(right) == 10 * cm + mm
        stem, right, _ = _q("route_distance_p3", seed)
        a, b = _ints(stem)
        assert int(right) == (a + b if "ผ่าน" in stem else abs(a - b))
        stem, right, _ = _q("bottles_total_ml_p3", seed)
        n, each = _ints(stem)
        assert int(right) == n * each
        stem, right, _ = _q("l_ml_to_ml_p3", seed)
        litres, ml = _ints(stem)
        assert int(right) == 1000 * litres + ml
        stem, right, _ = _q("pours_to_fill_p3", seed)
        tank, jug = _ints(stem)
        assert int(right) * jug == tank
        stem, right, texts = _q("largest_capacity_p3", seed)

        def ml(t: str) -> int:
            n = _ints(t)
            return 1000 * n[0] + sum(n[1:]) if t.split()[1] == "ลิตร" else n[0]
        assert ml(right) == (max if "มากที่สุด" in stem else min)(ml(t) for t in texts)
        stem, right, _ = _q("pour_left_p3", seed)
        litres, cups, cup = _ints(stem)
        assert int(right) == 1000 * litres - cups * cup
        _q("capacity_unit_p3", seed)


def test_fractions_and_two_steps():
    for seed in SEEDS:
        stem, right, _ = _q("unit_fraction_of_p3", seed)
        n, d = _ints(stem)[:2]
        assert int(right) * d == n
        stem, right, _ = _q("fraction_left_p3", seed)
        d, a, d2 = _ints(stem)
        assert d == d2 and right == f"{d - a}/{d}"
        stem, right, _ = _q("fraction_who_more_p3", seed)
        a, d, b, d2 = _ints(stem)
        p, q = stem.split("กิน")[0], stem.split("ของลูก ")[1].split("กิน")[0]
        assert right == (p if a > b else q)
        stem, right, _ = _q("buy_two_kinds_p3", seed)
        m, a, n, b = _ints(stem)
        assert int(right) == m * a + n * b
        stem, right, _ = _q("buy_then_share_p3", seed)
        boxes, per_box, people = _ints(stem)
        assert int(right) * people == boxes * per_box
        stem, right, _ = _q("save_then_spend_p3", seed)
        per, days, spend = _ints(stem)
        assert int(right) == per * days - spend
        stem, right, _ = _q("empty_seats_p3", seed)
        rows, per, people = _ints(stem)
        assert int(right) == rows * per - people
        stem, right, _ = _q("loads_delivered_p3", seed)
        per, trips, left = _ints(stem)
        assert int(right) == per * trips + left
        stem, right, _ = _q("two_rooms_compare_p3", seed)
        a, b, c, d = _ints(stem)
        assert int(right) == a * b - c * d > 0
        stem, right, _ = _q("pages_left_p3", seed)
        total, per, days = _ints(stem)
        assert int(right) == total - per * days


def test_symmetry():
    for seed in SEEDS:
        stem, right, _ = _q("symmetry_total_axes_p3", seed)
        x, y = stem.removesuffix(" มีแกนสมมาตรรวมกันกี่แกน").split("และ", 1)
        assert int(right) == AXES[x] + AXES[y]
        stem, right, texts = _q("most_axes_p3", seed)
        assert AXES[right] == (max if "มากที่สุด" in stem else min)(AXES[t] for t in texts)
        for key in ("symmetric_shape_p3", "symmetry_fold_p3", "symmetry_axis_direction_p3"):
            _q(key, seed)
