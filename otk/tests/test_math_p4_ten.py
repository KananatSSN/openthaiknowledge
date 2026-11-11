"""The ป.4 sets added so every unit has at least ten: each answer worked out again from the stem alone.

Numbers are read back out of the question (grouped thousands included) and the answer recomputed here by its
own route; text answers are checked against facts written out here independently.
"""

from __future__ import annotations

import re
from fractions import Fraction
from itertools import permutations
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


def _ints(s: str) -> list[int]:
    return [int(v) for v in re.findall(r"\d+", s.replace(",", ""))]


def _n(s: str) -> int:
    return int(s.replace(",", ""))


def _eval(expr: str) -> int:
    expr = expr.replace(",", "").replace("×", "*").replace("÷", "//").replace("−", "-")
    expr = expr.replace("\\times", "*").replace("\\div", "//")
    assert re.fullmatch(r"[\d\s+\-*/()]+", expr), expr
    return eval(expr)  # noqa: S307 - digits and operators only, checked above


def _thai_number(words: str) -> int:
    """Read a Thai number back, written out independently of story.thai_words."""
    digits = {"หนึ่ง": 1, "เอ็ด": 1, "สอง": 2, "ยี่": 2, "สาม": 3, "สี่": 4, "ห้า": 5, "หก": 6, "เจ็ด": 7,
              "แปด": 8, "เก้า": 9}
    places = {"ล้าน": 1_000_000, "แสน": 100_000, "หมื่น": 10_000, "พัน": 1000, "ร้อย": 100, "สิบ": 10}
    total, millions, pending, i = 0, 0, None, 0
    words_sorted = sorted([*digits, *places], key=len, reverse=True)
    while i < len(words):
        word = next(w for w in words_sorted if words.startswith(w, i))
        if word in digits:
            pending = digits[word]
        elif word == "ล้าน":
            millions = (total + (pending or 0)) * 1_000_000
            total, pending = 0, None
        else:
            total += (pending if pending is not None else 1) * places[word]
            pending = None
        i += len(word)
    return millions + total + (pending or 0)


def _rows(stem: str, start: int) -> dict[str, list[int]]:
    rows = {}
    for line in stem.split("\n")[start:]:
        if " | " in line:
            label, *cells = line.split(" | ")
            if all(re.fullmatch(r"\d+|\?", c.strip()) for c in cells):
                rows[label.strip()] = [int(c) if c.strip() != "?" else None for c in cells]
    return rows


def _bars(stem: str) -> dict[str, int]:
    scale = _ints(stem.split("แทน")[-1])[0]
    return {line.split(":")[0].strip(): line.count("■") * scale for line in stem.split("\n") if "■" in line and ":" in line}


def _round(n: int, place: int) -> int:
    return (n + place // 2) // place * place


def test_place_value():
    for seed in SEEDS:
        stem, right, _ = _q("more_less_large_p4", seed)
        n, step = _ints(stem)
        assert _n(right) == (n + step if "มากกว่า" in stem else n - step)
        stem, right, _ = _q("number_from_digits_p4", seed)
        digits = _ints(stem.split("หลักละ")[0])
        made = [int("".join(map(str, p))) for p in permutations(digits) if p[0] != 0]
        assert _n(right) == (max(made) if "มากที่สุด" in stem else min(made))
        stem, right, texts = _q("number_between_p4", seed)
        a, b = _ints(stem)
        assert [a < _n(t) < b for t in texts].count(True) == 1 and a < _n(right) < b
        stem, right, _ = _q("zeros_in_number_p4", seed)
        words = stem.removeprefix("จำนวน").split(" เขียนเป็น")[0]
        assert int(right) == str(_thai_number(words)).count("0")
        stem, right, _ = _q("expanded_to_number_p4", seed)
        assert _n(right) == sum(_ints(stem.removeprefix("ผลบวกนี้เท่ากับจำนวนใด").replace(" + ", " ")))
        stem, right, _ = _q("digit_count_p4", seed)
        words = stem.removeprefix("จำนวน").split(" เขียนเป็น")[0]
        assert int(right) == len(str(_thai_number(words)))


def test_add_and_subtract():
    for seed in SEEDS:
        stem, right, _ = _q("add_three_large_p4", seed)
        assert _n(right) == _eval(stem.removeprefix("จงหาผลบวก"))
        stem, right, texts = _q("check_addsub_p4", seed)
        checked = stem.removeprefix("ข้อใดใช้ตรวจคำตอบของ ")
        lhs = checked.split(" = ")[0]
        for t in texts:
            tl, tr = t.split(" = ")
            ok = _eval(tl) == _n(tr) and ("+" in lhs) != ("+" in tl) and set(_ints(t)) == set(_ints(checked))
            assert ok == (t == right), (stem, t)
        stem, right, _ = _q("how_many_more_p4", seed)
        a, b = _ints(stem)
        assert _n(right) == a - b
        stem, right, _ = _q("missing_digit_add_p4", seed)
        left, s = stem.split(" = ")
        shown, b = left.split(" + ")
        a = str(_ints(s)[0] - int(b))
        assert all(x == y or x == "□" for x, y in zip(shown, a)) and right == a[shown.index("□")]
        stem, right, texts = _q("largest_result_p4", seed)
        assert _eval(right) == (max if "มากที่สุด" in stem else min)(_eval(t) for t in texts)
        stem, right, _ = _q("budget_left_p4", seed)
        budget, a, b = _ints(stem)
        assert _n(right) == budget - a - b
        stem, right, _ = _q("compare_two_sums_p4", seed)
        a, b, c, d = _ints(stem)
        assert _n(right) == a + b - c - d > 0


def test_multiply_and_divide():
    for seed in SEEDS:
        for key in ("multiply_3x2_p4", "multiply_by_hundreds_p4"):
            stem, right, _ = _q(key, seed)
            assert _n(right) == _eval(stem.removeprefix("จงหาผลคูณ"))
        stem, right, texts = _q("largest_product_p4", seed)
        assert _eval(right) == (max if "มากที่สุด" in stem else min)(_eval(t) for t in texts)
        stem, right, _ = _q("missing_factor_p4", seed)
        b, p = _ints(stem.replace("\\square", ""))[-2:]
        assert _n(right) * b == p
        stem, right, _ = _q("boxes_total_p4", seed)
        per, boxes = _ints(stem)
        assert _n(right) == per * boxes
        stem, right, _ = _q("divide_by_hundreds_p4", seed)
        assert _n(right) == _eval(stem.removeprefix("จงหาผลหาร"))
        stem, right, _ = _q("missing_dividend_p4", seed)
        b, q = _ints(stem.replace("\\square", ""))[-2:]
        assert _n(right) == b * q
        stem, right, _ = _q("dividend_from_remainder_p4", seed)
        b, q, r = _ints(stem)
        assert _n(right) == b * q + r
        stem, right, _ = _q("share_large_p4", seed)
        n, b = _ints(stem)
        assert _n(right) * b == n
        stem, right, texts = _q("largest_quotient_p4", seed)
        assert _eval(right) == (max if "มากที่สุด" in stem else min)(_eval(t) for t in texts)
        stem, right, texts = _q("divides_evenly_p4", seed)
        b = _ints(stem)[0]
        assert [_n(t) % b == 0 for t in texts].count(True) == 1 and _n(right) % b == 0
        stem, right, _ = _q("remainder_only_p4", seed)
        n, b = _ints(stem)
        assert int(right) == n % b


def test_estimation():
    names = {"หลักสิบ": 10, "หลักร้อย": 100, "หลักพัน": 1000}
    for seed in SEEDS:
        stem, right, _ = _q("estimate_difference_p4", seed)
        a, b = _ints(stem)[:2]
        assert _n(right) == _round(a, 1000) - _round(b, 1000)
        stem, right, _ = _q("estimate_quotient_p4", seed)
        n, b = _ints(stem)[:2]
        assert _n(right) * b == _round(n, 100)
        stem, right, texts = _q("rounds_to_p4", seed)
        place = next(v for k, v in names.items() if k in stem)
        value = _ints(stem.split("ได้")[-1])[0]
        assert [_round(_n(t), place) == value for t in texts].count(True) == 1 and _round(_n(right), place) == value
        stem, right, _ = _q("largest_rounding_to_p4", seed)
        place = next(v for k, v in names.items() if k in stem)
        value = _ints(stem.split("ได้")[-1])[0]
        assert _round(_n(right), place) == value and _round(_n(right) + 1, place) != value
        stem, right, _ = _q("smallest_rounding_to_p4", seed)
        place = next(v for k, v in names.items() if k in stem)
        value = _ints(stem.split("ได้")[-1])[0]
        assert _round(_n(right), place) == value and _round(_n(right) - 1, place) != value
        stem, right, _ = _q("estimate_bill_p4", seed)
        prices = [int(p) for p in re.findall(r"ราคา (\d+) บาท", stem)]
        assert _n(right) == sum(_round(p, 100) for p in prices)


def test_two_step():
    for seed in SEEDS:
        stem, right, _ = _q("ticket_income_p4", seed)
        adult, a, child, c = _ints(stem)
        assert _n(right) == adult * a + child * c
        stem, right, _ = _q("buy_two_kinds_p4", seed)
        m, a, n, b = _ints(stem)
        assert _n(right) == m * a + n * b
        stem, right, _ = _q("cost_per_person_p4", seed)
        people, vans, rent = _ints(stem)
        assert _n(right) * people == vans * rent
        stem, right, _ = _q("yearly_saving_p4", seed)
        per, year, spend = _ints(stem)
        assert year == 1 and _n(right) == 12 * per - spend
        stem, right, _ = _q("full_trays_p4", seed)
        n, per = _ints(stem)
        assert int(right) == n // per
        stem, right, _ = _q("round_trips_p4", seed)
        km, days = _ints(stem)
        assert _n(right) == 2 * km * days


def test_bar_charts():
    for seed in SEEDS:
        stem, right, _ = _q("bar_range_p4", seed)
        bars = _bars(stem)
        assert int(right) == max(bars.values()) - min(bars.values())
        stem, right, _ = _q("bar_total_p4", seed)
        assert int(right) == sum(_bars(stem).values())
        stem, right, _ = _q("bar_order_p4", seed)
        bars = _bars(stem)
        ordered = sorted(bars, key=bars.get, reverse="มากไปน้อย" in stem)
        assert right == ordered[1 if stem.endswith("สอง") else 2]
        stem, right, _ = _q("bar_count_above_p4", seed)
        bars = _bars(stem)
        k = _ints(stem.split("\n")[-1])[0]
        assert int(right) == sum(v > k for v in bars.values())
        stem, right, texts = _q("bar_true_statement_p4", seed)
        bars = _bars(stem)
        for t in texts:
            first, second = t.split("มากกว่า")
            x = next(r for r in bars if r in first)
            y = next(r for r in bars if r in second)
            assert (bars[x] - bars[y] == _ints(second)[-1]) == (t == right), t
        stem, right, _ = _q("bar_two_rows_p4", seed)
        bars = _bars(stem)
        question = stem.split("\n")[-1]
        x, y, z = sorted((r for r in bars if r in question), key=question.index)
        assert int(right) == bars[x] + bars[y] - bars[z]


def test_two_way_tables():
    for seed in SEEDS:
        stem, right, _ = _q("two_way_grand_total_p4", seed)
        assert int(right) == sum(sum(v) for v in _rows(stem, 2).values())
        stem, right, _ = _q("two_way_column_diff_p4", seed)
        rows = _rows(stem, 2)
        cols = stem.split("\n")[1].split(" | ")[1:]
        totals = [sum(v[i] for v in rows.values()) for i in range(len(cols))]
        assert int(right) == max(totals) - min(totals)
        stem, right, _ = _q("two_way_row_most_p4", seed)
        rows = _rows(stem, 2)
        totals = {r: sum(v) for r, v in rows.items()}
        assert right == (max if "มากที่สุด" in stem else min)(totals, key=totals.get)
        stem, right, _ = _q("two_way_cell_diff_p4", seed)
        rows = _rows(stem, 2)
        row = next(r for r in rows if f"ใน{r} " in stem)
        assert int(right) == abs(rows[row][0] - rows[row][1])
        stem, right, _ = _q("two_way_two_rows_p4", seed)
        rows = _rows(stem, 2)
        cols = stem.split("\n")[1].split(" | ")[1:]
        question = stem.split("\n")[-1]
        col = next(i for i, c in enumerate(cols) if question.startswith(c))
        named = [r for r in rows if r in question]
        assert len(named) == 2 and int(right) == sum(rows[r][col] for r in named)
        stem, right, texts = _q("two_way_true_statement_p4", seed)
        rows = _rows(stem, 2)
        cols = stem.split("\n")[1].split(" | ")[1:]
        for t in texts:
            row = next(r for r in rows if t.startswith(r))
            col = next(i for i, c in enumerate(cols) if f"มี{c} " in t)
            v, total = _ints(t.removeprefix(row))[-2:]
            assert (rows[row][col] == v and sum(rows[row]) == total) == (t == right), t
        stem, right, _ = _q("two_way_missing_cell_p4", seed)
        rows = _rows(stem, 2)
        row = next(r for r, v in rows.items() if None in v)
        total = _ints(stem.split("\n")[-1].split("รวมทั้งหมด")[1])[0]
        assert int(right) == total - sum(v for v in rows[row] if v is not None)


def test_rectangles_fractions_decimals():
    for seed in SEEDS:
        stem, right, texts = _q("largest_area_p4", seed)

        def dims(t: str) -> tuple[int, int]:
            w, h = _ints(t)
            return w, h
        assert dims(right)[0] * dims(right)[1] == (max if "มากที่สุด" in stem else min)(
            dims(t)[0] * dims(t)[1] for t in texts)
        stem, right, texts = _q("largest_perimeter_p4", seed)
        assert sum(dims(right)) == (max if "มากที่สุด" in stem else min)(sum(dims(t)) for t in texts)
        stem, right, _ = _q("same_perimeter_area_p4", seed)
        p, w1, w2 = _ints(stem)
        half = p // 2
        assert int(right) == w2 * (half - w2) - w1 * (half - w1)
        stem, right, _ = _q("area_when_doubled_p4", seed)
        w, h = _ints(stem)
        assert int(right) == (4 if "ทั้งด้านกว้าง" in stem else 2) * w * h
        stem, right, _ = _q("l_shape_area_p4", seed)
        a, b, c, d = _ints(stem)
        assert int(right) == a * b - c * d
        stem, right, _ = _q("fraction_of_amount_p4", seed)
        n, d, total = _ints(stem)
        assert Fraction(int(right)) == Fraction(n, d) * total
        stem, right, _ = _q("equivalent_missing_p4", seed)
        n, d, d2 = _ints(stem.replace("\\square", ""))[:3]
        assert Fraction(int(right), d2) == Fraction(n, d)
        stem, right, _ = _q("amount_left_fraction_p4", seed)
        total, n, d = _ints(stem)
        assert int(right) == total - total * n // d
        stem, right, _ = _q("make_one_whole_p4", seed)
        n, d = _ints(stem)[:2]
        a, b = _ints(right)
        assert Fraction(n, d) + Fraction(a, b) == 1
        stem, right, _ = _q("decimal_as_fraction_p4", seed)
        dec = re.search(r"0\.\d+", stem).group()
        a, b = _ints(right)
        assert Fraction(a, b) == Fraction(dec)
        stem, right, _ = _q("round_decimal_whole_p4", seed)
        x = Fraction(re.search(r"\d+\.\d", stem).group())
        assert int(right) == int(x + Fraction(1, 2))
        stem, right, texts = _q("decimal_between_p4", seed)
        lo, hi = (Fraction(v) for v in re.findall(r"\d+\.\d+", stem))
        assert [lo < Fraction(t) < hi for t in texts].count(True) == 1 and lo < Fraction(right) < hi


def test_time():
    month_days = {"มกราคม": 31, "กุมภาพันธ์": 28, "มีนาคม": 31, "เมษายน": 30, "พฤษภาคม": 31, "มิถุนายน": 30,
                  "กรกฎาคม": 31, "สิงหาคม": 31, "กันยายน": 30, "ตุลาคม": 31, "พฤศจิกายน": 30, "ธันวาคม": 31}

    def seconds(s: str) -> int:
        n = _ints(s)
        return 60 * n[0] + n[1] if re.search(r"\d+ นาที", s) else n[0]
    for seed in SEEDS:
        stem, right, _ = _q("days_to_weeks_p4", seed)
        total = _ints(stem)[0]
        w, d = _ints(right)
        assert 7 * w + d == total and d < 7
        stem, right, texts = _q("longest_duration_p4", seed)

        def minutes(t: str) -> int:
            n = _ints(t)
            return 60 * n[0] + (n[1] if len(n) > 1 else 0) if "ชั่วโมง" in t else n[0]
        assert minutes(right) == (max if "นานที่สุด" in stem else min)(minutes(t) for t in texts)
        stem, right, _ = _q("race_times_p4", seed)
        parts = re.findall(r"ใช้เวลา ((?:\d+ นาที )?\d+ วินาที)", stem)
        assert int(right) == sum(seconds(p) for p in parts)
        stem, right, _ = _q("stopwatch_difference_p4", seed)
        parts = re.findall(r"ในเวลา ((?:\d+ นาที )?\d+ วินาที)", stem)
        assert int(right) == seconds(parts[0]) - seconds(parts[1])
        stem, right, _ = _q("days_between_dates_p4", seed)
        (d1, m1), (d2, m2) = re.findall(r"วันที่ (\d+) (\S+?) ", stem.replace("ของปี", " ของปี"))[:2]
        assert int(right) == month_days[m1] - int(d1) + int(d2)
        for key in ("decade_century_p4", "leap_year_p4"):
            _q(key, seed)
