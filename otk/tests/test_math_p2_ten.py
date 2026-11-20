"""The ป.2 sets added so every unit has at least ten: each answer worked out again from the stem alone.

Numbers are read back out of the question and the answer recomputed here by its own route; text answers are
checked against facts written out here independently (months, faces of solids, sides of shapes).
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


def _pictograph(stem: str) -> tuple[dict[str, int], int]:
    key = _ints(stem.split("กำหนดให้")[1])[0]
    rows = {}
    for line in stem.split("\n"):
        if ":" in line and "●" in line:
            label, marks = line.split(":", 1)
            rows[label.strip()] = marks.count("●") * key
    return rows, key


MONTHS = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
          "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
POLY = {"รูปสามเหลี่ยม": 3, "รูปสี่เหลี่ยม": 4, "รูปห้าเหลี่ยม": 5, "รูปหกเหลี่ยม": 6}
FACES = {"ทรงสี่เหลี่ยมมุมฉาก": 6, "ลูกบาศก์": 6, "ทรงกระบอก": 2, "กรวย": 1, "ทรงกลม": 0}


def _minutes(clock: str) -> int:
    h, m = clock.removesuffix(" น.").split(".")
    return int(h) * 60 + int(m)


def test_numbers():
    for seed in SEEDS:
        stem, right, texts = _q("even_number_p2", seed)
        want = 0 if "คู่" in stem else 1
        assert [int(t) % 2 == want for t in texts].count(True) == 1 and int(right) % 2 == want
        stem, right, _ = _q("hundreds_tens_ones_p2", seed)
        h, t, o = _ints(stem)
        assert int(right) == 100 * h + 10 * t + o
        stem, right, _ = _q("more_less_100_p2", seed)
        n, step = _ints(stem)
        assert int(right) == (n + step if "มากกว่า" in stem else n - step)


def test_add_and_subtract():
    for seed in SEEDS:
        stem, right, _ = _q("add_word_three_digit_p2", seed)
        assert int(right) == sum(_ints(stem))
        stem, right, _ = _q("sub_word_three_digit_p2", seed)
        a, b = _ints(stem)
        assert int(right) == a - b
        stem, right, texts = _q("check_with_inverse_p2", seed)
        checked = stem.removeprefix("ข้อใดใช้ตรวจคำตอบของ ")
        lhs, total = checked.split(" = ")
        for t in texts:
            tl, tr = t.split(" = ")
            true = _eval(tl) == int(tr)
            uses_inverse = ("+" in lhs) != ("+" in tl) and set(_ints(t)) == set(_ints(checked))
            assert (true and uses_inverse) == (t == right), (stem, t)
        stem, right, _ = _q("add_three_two_digit_p2", seed)
        assert int(right) == sum(_ints(stem))
        stem, right, texts = _q("largest_sum_p2", seed)
        pick = max if "มากที่สุด" in stem else min
        assert _eval(right) == pick(_eval(t) for t in texts)
        stem, right, _ = _q("how_many_more_p2", seed)
        nums = _ints(stem)
        assert int(right) == nums[1] - nums[3]


def test_multiply_and_divide():
    for seed in SEEDS:
        for key in ("times_table_p2", "multiply_by_ten_p2", "multiply_zero_one_p2"):
            stem, right, _ = _q(key, seed)
            assert int(right) == _eval(stem.removeprefix("จงหาผลคูณ"))
        stem, right, texts = _q("largest_product_p2", seed)
        pick = max if "มากที่สุด" in stem else min
        assert _eval(right) == pick(_eval(t) for t in texts)
        stem, right, _ = _q("array_rows_p2", seed)
        rows, cols = _ints(stem)
        assert int(right) == rows * cols
        stem, right, texts = _q("division_check_p2", seed)
        n, b, q = _ints(stem)
        assert n == b * q and right == f"{q} × {b} = {n}"
        stem, right, _ = _q("division_leftover_word_p2", seed)
        n, b = _ints(stem)
        assert int(right) == n % b
        stem, right, _ = _q("missing_dividend_p2", seed)
        b, q = _ints(stem)
        assert int(right) == b * q
        stem, right, texts = _q("fact_family_p2", seed)
        a, b, n = _ints(stem)[-3:]
        for t in texts:
            tl, tr = t.split(" = ")
            ok = "+" not in tl and set(_ints(t)) == {a, b, n} and _eval(tl) == int(tr)
            assert ok == (t != right), (stem, t)
        stem, right, texts = _q("largest_quotient_p2", seed)
        pick = max if "มากที่สุด" in stem else min
        assert _eval(right) == pick(_eval(t) for t in texts)


def test_mixed():
    for seed in SEEDS:
        stem, right, texts = _q("mixed_true_sentence_p2", seed)
        for t in texts:
            tl, tr = t.split(" = ")
            assert (_eval(tl) == int(tr)) == (t == right)
        stem, right, _ = _q("legs_count_p2", seed)
        legs = {"ไก่": 2, "เป็ด": 2, "สุนัข": 4, "วัว": 4, "แมว": 4}
        found = re.findall(r"(ไก่|เป็ด|สุนัข|วัว|แมว) (\d+) ตัว", stem)
        assert int(right) == sum(legs[x] * int(n) for x, n in found)
        stem, right, _ = _q("wheels_count_p2", seed)
        wheels = {"จักรยาน": 2, "รถสามล้อ": 3, "รถยนต์": 4}
        found = re.findall(r"(จักรยาน|รถสามล้อ|รถยนต์) (\d+) คัน", stem)
        assert int(right) == sum(wheels[x] * int(n) for x, n in found)
        stem, right, _ = _q("compare_two_buys_p2", seed)
        a, p, b, q = _ints(stem)
        assert int(right) == a * p - b * q > 0
        stem, right, _ = _q("fill_bags_left_p2", seed)
        total, bags, per = _ints(stem)
        assert int(right) == total - bags * per


def test_patterns():
    for seed in SEEDS:
        stem, right, _ = _q("pattern_next_p2", seed)
        terms = _ints(stem)
        d = terms[1] - terms[0]
        assert all(y - x == d for x, y in zip(terms, terms[1:])) and int(right) == terms[-1] + d
        stem, right, _ = _q("pattern_two_missing_p2", seed)
        parts = stem.split(": ")[1].split(", ")
        known = [(i, int(p)) for i, p in enumerate(parts) if p != "□"]
        (i0, v0), (i1, v1) = known[0], known[1]
        step = (v1 - v0) // (i1 - i0)
        gaps = [v0 + step * (i - i0) for i, p in enumerate(parts) if p == "□"]
        assert right == f"{gaps[0]} และ {gaps[1]}"
        stem, right, _ = _q("pattern_nth_term_p2", seed)
        step, start, n = _ints(stem)
        assert int(right) == start + step * (n - 1)
        stem, right, _ = _q("pattern_three_nth_p2", seed)
        shapes = stem.split("แบบรูป ")[1].split("...")[0].split()
        k = _ints(stem)[-1]
        assert right == shapes[(k - 1) % 3]
        stem, right, _ = _q("pattern_growing_dots_p2", seed)
        _, first, step, n = _ints(stem)
        assert int(right) == first + step * (n - 1)
        stem, right, _ = _q("pattern_count_back_p2", seed)
        step, start, k = _ints(stem)
        assert int(right) == start - step * (k - 1)


def test_measuring():
    for seed in SEEDS:
        stem, right, _ = _q("cm_to_m_cm_p2", seed)
        cm = _ints(stem)[0]
        assert right == f"{cm // 100} เมตร {cm % 100} เซนติเมตร"
        stem, right, texts = _q("longest_mixed_units_p2", seed)
        values = {t: (100 * _ints(t)[0] + sum(_ints(t)[1:]) if t.split()[1] == "เมตร" else _ints(t)[0]) for t in texts}
        assert values[right] == (max if "ยาวที่สุด" in stem else min)(values.values())
        stem, right, _ = _q("kg_g_to_g_p2", seed)
        kg, g = _ints(stem)
        assert int(right) == 1000 * kg + g
        stem, right, _ = _q("length_compare_mixed_p2", seed)
        nums = _ints(stem)
        first = 100 * nums[0] + (nums[1] if len(nums) == 3 else 0)
        assert int(right) == first - nums[-1]


def test_shapes():
    for seed in SEEDS:
        stem, right, _ = _q("solid_faces_count_p2", seed)
        assert int(right) == FACES[stem.split("มีหน้า")[0]]
        stem, right, _ = _q("total_corners_p2", seed)
        found = re.findall(r"(รูป\S+?เหลี่ยม) (\d+) รูป", stem)
        assert int(right) == sum(POLY[x.removeprefix("และ")] * int(n) for x, n in found)
        stem, right, _ = _q("count_shapes_list_p2", seed)
        names = {"รูปสามเหลี่ยม": "△", "รูปสี่เหลี่ยม": "□", "รูปวงกลม": "○"}
        asked = names[stem.split("มี")[-1].removesuffix("กี่รูป")]
        assert int(right) == stem.split("มี")[0].count(asked)
        for key in ("curved_straight_p2", "line_kinds_p2", "circle_ellipse_p2"):
            _q(key, seed)


def test_money():
    for seed in SEEDS:
        stem, right, _ = _q("change_from_note_p2", seed)
        price, note = _ints(stem)
        assert int(right) == note - price
        stem, right, _ = _q("total_three_items_p2", seed)
        assert int(right) == sum(_ints(stem))
        stem, right, texts = _q("coins_make_amount_p2", seed)
        total = _ints(stem)[0]
        for t in texts:
            pairs = re.findall(r"(\d+) บาท (\d+)", t)
            assert (sum(int(u) * int(c) for u, c in pairs) == total) == (t == right), t
        stem, right, _ = _q("fifty_satang_p2", seed)
        coin, n = _ints(stem)
        assert int(right) * 100 == coin * n
        stem, right, _ = _q("cheaper_by_p2", seed)
        a, b = _ints(stem)
        assert int(right) == a - b


def test_time():
    for seed in SEEDS:
        stem, right, texts = _q("time_after_p2", seed)
        start = _minutes(re.search(r"\d+\.\d\d น\.", stem).group())
        add = int(re.search(r"ใช้เวลา (\d+) นาที", stem).group(1))
        assert _minutes(right) == start + add
        stem, right, _ = _q("time_before_p2", seed)
        end = _minutes(re.search(r"\d+\.\d\d น\.", stem).group())
        back = int(re.search(r"ก่อน (\d+) นาที", stem).group(1))
        assert _minutes(right) == end - back
        stem, right, texts = _q("months_p2", seed)
        if "ถัดจาก" in stem:
            asked = stem.split("ถัดจากเดือน")[1].removesuffix("คือเดือนใด")
            assert right == MONTHS[(MONTHS.index(asked) + 1) % 12]
        elif "ก่อนเดือน" in stem:
            asked = stem.split("ก่อนเดือน")[1].removesuffix("คือเดือนใด")
            assert right == MONTHS[(MONTHS.index(asked) - 1) % 12]
        else:
            days = 28 if "28 หรือ 29" in stem else _ints(stem)[0]
            assert [DAYS[MONTHS.index(t)] == days for t in texts].count(True) == 1
            assert DAYS[MONTHS.index(right)] == days
        stem, right, _ = _q("weeks_days_p2", seed)
        nums = _ints(stem)
        assert int(right) == 7 * nums[0] + (nums[1] if len(nums) > 1 else 0)


def test_pictographs():
    for seed in SEEDS:
        stem, right, _ = _q("pictograph_total_p2", seed)
        rows, _ = _pictograph(stem)
        assert int(right) == sum(rows.values())
        stem, right, _ = _q("pictograph_range_p2", seed)
        rows, _ = _pictograph(stem)
        assert int(right) == max(rows.values()) - min(rows.values())
        stem, right, _ = _q("pictograph_add_symbols_p2", seed)
        rows, key = _pictograph(stem)
        question = stem.split("\n")[-1]
        row = next(r for r in rows if f"ที่{r}อีก" in question)
        assert int(right) == rows[row] + key * _ints(question)[0]
        stem, right, _ = _q("pictograph_order_p2", seed)
        rows, _ = _pictograph(stem)
        ordered = sorted(rows, key=rows.get, reverse="มากไปน้อย" in stem)
        assert right == ordered[1 if stem.endswith("สอง") else 2]
        stem, right, texts = _q("pictograph_true_statement_p2", seed)
        rows, _ = _pictograph(stem)
        for t in texts:
            first, second = t.split("มากกว่า")
            x = next(r for r in rows if r in first)
            y = next(r for r in rows if r in second)
            assert (rows[x] - rows[y] == _ints(second)[-1]) == (t == right), t
        stem, right, _ = _q("pictograph_two_rows_p2", seed)
        rows, _ = _pictograph(stem)
        question = stem.split("\n")[-1]
        x, y, z = sorted((r for r in rows if r in question), key=question.index)
        assert int(right) == rows[x] + rows[y] - rows[z]
