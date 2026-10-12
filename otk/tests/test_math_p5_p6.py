"""ป.5 and ป.6 enrichment: answers re-derived from what the learner is shown."""

from __future__ import annotations

from otk.tests._origins import keys_from

import math
import re
from decimal import Decimal
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate

SEEDS = range(300)
P5 = keys_from("math_p5")
P6 = keys_from("math_p6")
ENRICHED = ["math.discount", "math.simple_interest", "math.pie_chart",
            "math.rectangular_prism_volume", "math.line_graph_change", "math.lcm_word"]


def _stem(q) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in q.stem)


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _numbers(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s.replace(",", ""))]


def _frac(tex: str) -> Fraction:
    m = re.fullmatch(r"(\d*)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if not m:
        return Fraction(int(tex))
    whole, n, d = m.groups()
    return int(whole or 0) + Fraction(int(n), int(d))


def _eval(tex: str) -> float:
    return eval(tex.replace(r"\times", "*").replace(r"\div", "/"))


def test_module_sizes():
    assert len(P5) == 20 and all(REGISTRY[k].level_for() == "ป.5" for k in P5)
    assert len(P6) == 17 and all(REGISTRY[k].level_for() == "ป.6" for k in P6)


@pytest.mark.parametrize("key", P5 + P6 + ENRICHED)
def test_four_distinct_choices(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        assert len(q.choices) == REGISTRY[key].max_choices, (key, seed, _stem(q))
        assert len({_choice(c) for c in q.choices}) == REGISTRY[key].max_choices


# ── ป.5 ──────────────────────────────────────────────────────────────────────

def test_fraction_of_amount():
    for seed in SEEDS:
        q = generate("math.fraction_of_amount_p5", Random(seed))
        f = _frac(q.stem[1].tex)
        n = _numbers(q.stem[0].text)[0]
        ans = int(_answer(q))
        s = _stem(q)
        if "ชาย" in s:
            assert ans == n - n * f
        elif "ทั้งเล่ม" in s:
            assert ans * f == n
        else:
            assert ans == n * f


def test_fraction_word_problems():
    for seed in SEEDS:
        q = generate("math.fraction_word_addsub_p5", Random(seed))
        given = [_frac(b.tex) for b in q.stem if getattr(b, "tex", None)]
        s = _stem(q)
        if len(given) == 3:
            want = given[0] + given[1] - given[2]
        elif "เหลือ" in s:
            want = given[0] - given[1]
        else:
            want = given[0] + given[1]
        values = [_frac(_choice(c)) for c in q.choices]
        assert values[q.answer] == want and values.count(want) == 1, s
        q = generate("math.fraction_word_muldiv_p5", Random(seed))
        given = [_frac(b.tex) for b in q.stem if getattr(b, "tex", None)]
        s = _stem(q)
        if "ตัดเป็นเส้นละ" in s:
            want = given[0] / given[1]
        elif "แบ่งใส่แก้ว" in s:
            want = given[0] / _numbers(q.stem[-1].text)[0]
        elif "เค้กเหลือ" in s:
            want = given[0] * given[1]
        elif "ชั่วโมงละ" in s:
            want = _numbers(q.stem[0].text)[0] * given[0]
        elif "วันละ" in s:
            want = given[0] * _numbers(q.stem[-1].text)[0]
        else:
            want = _numbers(q.stem[0].text)[0] * given[0]
        values = [_frac(_choice(c)) for c in q.choices]
        assert values[q.answer] == want and values.count(want) == 1, s


def test_decimal_multiply_divide_and_conversion():
    for seed in SEEDS:
        q = generate("math.decimal_multiply_p5", Random(seed))
        a, b = q.stem[-1].tex.split(r" \times ")
        assert Decimal(_answer(q)) == Decimal(a) * Decimal(b)
        q = generate("math.decimal_divide_p5", Random(seed))
        a, b = q.stem[-1].tex.split(r" \div ")
        assert Decimal(_answer(q)) == Decimal(a) / Decimal(b)
        q = generate("math.fraction_to_decimal_p5", Random(seed))
        f = _frac(q.stem[-1].tex)
        assert Decimal(_answer(q)) == Decimal(f.numerator) / Decimal(f.denominator)
        values = [Decimal(_choice(c)) for c in q.choices]
        assert values.count(Decimal(_answer(q))) == 1


def test_rule_of_three():
    for seed in SEEDS:
        q = generate("math.unit_price_p5", Random(seed))
        a, price, b = _numbers(_stem(q))
        assert int(_answer(q)) * a == price * b
        q = generate("math.rate_word_problem_p5", Random(seed))
        x, y, z = _numbers(_stem(q))
        ans = int(_answer(q))
        # "a ชั่วโมง ได้ amount" or "amount ใน a นาที": either order in the story.
        assert ans * x == y * z or ans * y == x * z
        q = generate("math.recipe_scaling_p5", Random(seed))
        people, amount, want = _numbers(_stem(q))
        assert int(_answer(q)) * people == amount * want


def test_percent_problems():
    for seed in SEEDS:
        q = generate("math.percent_of_quantity_p5", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = _numbers(s)
        whole, pct = (n[0], n[1]) if "คะแนน" not in s else (n[1], n[0])
        part = whole * pct // 100
        assert ans == (whole - part if "ที่เหลือ" in s or "ไม่แตก" in s else part)
        q = generate("math.find_percent_p5", Random(seed))
        whole, part = _numbers(_stem(q))
        assert int(_answer(q)) * whole == part * 100
        q = generate("math.percent_two_step_p5", Random(seed))
        n = _numbers(_stem(q))
        after = n[0] - n[0] * n[1] // 100
        want = after - n[2] if "คูปอง" in _stem(q) else after * n[2]
        assert int(_answer(q)) == want


def test_volume_and_area_p5():
    for seed in SEEDS:
        q = generate("math.volume_capacity_p5", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = _numbers(s)
        if "จุน้ำได้กี่ลิตร" in s:
            assert ans * 1000 == n[0] * n[1] * n[2]
        elif "มีน้ำกี่" in s:
            assert ans == n[0] * n[1] * n[2]
        else:
            assert ans * n[1] * n[2] == n[0]
        q = generate("math.rhombus_kite_area_p5", Random(seed))
        n, ans = _numbers(_stem(q)), int(_answer(q))
        if "เส้นทแยงมุมอีกเส้น" in _stem(q):
            assert n[1] * ans == 2 * n[0]
        else:
            assert 2 * ans == n[0] * n[1]
        q = generate("math.parallelogram_perimeter_p5", Random(seed))
        n, ans = _numbers(_stem(q)), int(_answer(q))
        assert ans == (2 * (n[0] + n[1]) if len(n) == 2 else n[0] // 4)


def _table(q):
    lines = q.stem[0].text.split("\n")
    cols = [c.strip() for c in lines[1].split("|")[1:]]
    cells = {}
    for ln in lines[2:]:
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) == len(cols) + 1:
            for c, v in zip(cols, parts[1:]):
                cells[parts[0], c] = int(v)
    return cells, cols, lines[-1]


def test_two_way_tables():
    for seed in SEEDS:
        q = generate("math.two_way_table_read_p5", Random(seed))
        cells, cols, ask = _table(q)
        hit = [v for (r, c), v in cells.items() if ask.startswith(f"{r} {c} ")]
        assert hit == [int(_answer(q))]
        q = generate("math.two_way_table_total_p5", Random(seed))
        cells, cols, ask = _table(q)
        rows = {r for r, _ in cells}
        head = ask.split(" รวม")[0]
        if head in rows:
            assert int(_answer(q)) == sum(cells[head, c] for c in cols)
        else:
            assert int(_answer(q)) == sum(cells[r, head] for r in rows)


# ── ป.6 ──────────────────────────────────────────────────────────────────────

def test_gcd_problems():
    for seed in SEEDS:
        q = generate("math.gcd_word_problem_p6", Random(seed))
        x, y = _numbers(_stem(q))[:2]
        g = math.gcd(x, y)
        want = ((x + y) // g if "กี่ท่อน" in _stem(q)
                else x * y // (g * g) if "กี่แผ่น" in _stem(q) else g)
        assert int(_answer(q)) == want
        q = generate("math.gcd_lcm_relation_p6", Random(seed))
        g, lcm, x = _numbers(_stem(q))[:3]
        y = int(_answer(q))
        assert math.gcd(x, y) == g and x * y // g == lcm


def test_lcm_word():
    for seed in SEEDS:
        q = generate("math.lcm_word", Random(seed))
        a, b = _numbers(_stem(q))[:2]
        assert int(_answer(q)) == a * b // math.gcd(a, b)


def test_ratios():
    for seed in SEEDS:
        q = generate("math.equivalent_ratio_p6", Random(seed))
        left, right = q.stem[-1].tex.split("=")
        a, b = [Fraction(int(x)) for x in left.split(":")]
        c, d = [x.strip() for x in right.split(":")]
        v = int(_answer(q))
        c, d = (v, int(d)) if c == r"\square" else (int(c), v)
        assert a * d == b * c
        q = generate("math.ratio_share_p6", Random(seed))
        n = _numbers(_stem(q))
        total, a, b = (n[0], n[1], n[2]) if "แบ่งเงิน" in _stem(q) or "ห้องเรียน" in _stem(q) \
            else (n[2], n[0], n[1])
        unit = total // (a + b)
        s = _stem(q)
        want = a * unit if "แบ่งเงิน" in s else b * unit if "หญิง" in s else abs(a - b) * unit
        assert int(_answer(q)) == want, s
        q = generate("math.ratio_word_problem_p6", Random(seed))
        a, b, given = _numbers(_stem(q))[:3]
        s, ans = _stem(q), int(_answer(q))
        if "ดินสอ" in s:
            a, price, b = _numbers(s)[:3]
            assert ans * a == price * b
        elif "ทราย" in s or "ไข่" in s:
            assert ans * b == given * a
        elif "นักเรียนหญิง" in s:
            assert ans * b == given * (a + b)
        elif "ทั้งหมด" in s:
            assert ans * a == given * (a + b)
        else:
            assert ans * a == given * b


def test_profit_loss_and_change():
    for seed in SEEDS:
        q = generate("math.profit_loss_p6", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = _numbers(s)
        if "ต้องขายราคา" in s:
            assert ans == n[0] + n[0] * n[1] // 100
        elif "ขาดทุนร้อยละ" in s:
            assert ans == n[0] - n[0] * n[1] // 100
        elif "กำไรร้อยละเท่าใด" in s:
            assert ans * n[0] == (n[1] - n[0]) * 100
        else:
            assert ans == n[0] - n[1]
        q = generate("math.percent_change_p6", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = [x for x in _numbers(s) if x != 1]
        if "ร้อยละเท่าใด" in s:
            assert ans * n[0] == abs(n[1] - n[0]) * 100
        else:
            sign = 1 if "เพิ่มขึ้น" in s else -1
            assert ans == n[0] + sign * n[0] * n[1] // 100


def test_patterns_p6():
    for seed in SEEDS:
        q = generate("math.pattern_nth_term_p6", Random(seed))
        terms = [int(t) for t in q.stem[-1].tex.split(r",\ ")[:4]]
        n = _numbers(q.stem[0].text)[0]
        assert int(_answer(q)) == terms[0] + (terms[1] - terms[0]) * (n - 1)
        q = generate("math.matchstick_pattern_p6", Random(seed))
        nums = _numbers(_stem(q))
        i = next(i for i in range(len(nums)) if nums[i:i + 3] == [1, 2, 3])
        first, second, n = nums[i + 3], nums[i + 4], nums[-1]
        assert int(_answer(q)) == first + (second - first) * (n - 1)
        q = generate("math.pattern_rule_expression_p6", Random(seed))
        terms = [int(t) for t in q.stem[1].tex.split(r",\ ")[:4]]
        for i, c in enumerate(q.choices):
            rule = re.sub(r"(\d)n", r"\1*n", _choice(c))
            fits = all(eval(rule, {"n": k}) == t for k, t in enumerate(terms, 1))
            assert fits == (i == q.answer), (terms, _choice(c))


def test_circles_use_22_over_7():
    for seed in SEEDS:
        q = generate("math.circle_word_problem_p6", Random(seed))
        s, ans = _stem(q), Fraction(int(_answer(q)))
        n = _numbers(s)
        pi = Fraction(22, 7)
        if "ล้อ" in s:
            assert ans == 2 * pi * n[0] * n[1]
        elif "รั้ว" in s:
            assert ans == 2 * pi * n[0] * n[1]
        elif "นาฬิกา" in s:
            assert ans == 2 * pi * n[0]
        elif "ปูหญ้า" in s:
            assert ans == pi * n[0] ** 2 * n[1]
        elif "ลวด" in s:
            assert ans == n[0] / (2 * pi)
        else:
            assert ans == pi * (Fraction(n[0], 2)) ** 2


def test_volume_and_area_p6():
    for seed in SEEDS:
        q = generate("math.composite_box_volume_p6", Random(seed))
        n, ans = _numbers(_stem(q)), int(_answer(q))
        v1, v2 = n[0] * n[1] * n[2], n[3] * n[4] * n[5]
        assert ans == (v1 - v2 if "เจาะ" in _stem(q) else v1 + v2)
        q = generate("math.water_level_p6", Random(seed))
        n, ans = _numbers(_stem(q)), int(_answer(q))
        if "ระดับน้ำสูงขึ้น" in _stem(q):
            assert ans == n[0] * n[1] * n[2]
        else:
            assert ans * n[1] * n[2] == n[0] * 1000
        q = generate("math.triangle_missing_side_p6", Random(seed))
        area, base = _numbers(_stem(q))
        assert base * int(_answer(q)) == 2 * area
        q = generate("math.composite_area_p6", Random(seed))
        n, s, ans = _numbers(_stem(q)), _stem(q), int(_answer(q))
        if "หลังคา" in s:
            assert ans == n[0] * n[1] + n[2] * n[3] // 2
        elif "ตัดมุม" in s:
            assert ans == n[0] * n[1] - n[2] * n[3] // 2
        else:
            assert ans == n[0] * n[1] + n[2] * n[3]


def _pie(q):
    lines = q.stem[0].text.split("\n")
    total = _numbers(lines[0])[0]
    data = {ln.split(":")[0]: ln.split("ร้อยละ ")[1] for ln in lines[1:] if ": ร้อยละ" in ln}
    return total, data, lines[-1]


def test_pie_charts():
    for seed in SEEDS:
        q = generate("math.pie_chart_amount_p6", Random(seed))
        total, data, ask = _pie(q)
        named = sorted((k for k in data if k in ask), key=ask.index)
        if "มากกว่า" in ask:
            want = total * (int(data[named[0]]) - int(data[named[1]])) // 100
        else:
            want = total * int(data[named[0]]) // 100
        assert int(_answer(q)) == want
        q = generate("math.pie_chart_missing_p6", Random(seed))
        total, data, ask = _pie(q)
        if "?" in data.values():
            known = sum(int(v) for v in data.values() if v != "?")
            assert int(_answer(q)) == 100 - known
        else:
            name = [k for k in data if k in ask][0]
            assert int(_answer(q)) * 100 == 360 * int(data[name])
