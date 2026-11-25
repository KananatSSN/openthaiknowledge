"""Sets added for the maths entrance papers: each answer re-derived by another route."""

from __future__ import annotations

import math
import re
from fractions import Fraction
from random import Random

import sympy as sp

from otk.api import REGISTRY

SEEDS = range(40)


def _draw(key, seed):
    q = REGISTRY[key].generate(Random(seed))
    texts = [c.content[0].text for c in q.choices]
    assert len(set(texts)) == len(texts) == REGISTRY[key].max_choices
    return q.stem[0].text, texts[q.answer]


def _ints(s):
    return [int(n) for n in re.findall(r"\d+", s)]


def test_train_passing_by_equations():
    x, t = sp.symbols("x t", positive=True)
    for seed in SEEDS:
        stem, right = _draw("math.train_passing_m3", seed)
        value = sp.Rational(right.split()[0])
        if stem.startswith("รถไฟขบวนที่หนึ่ง"):
            lengths = re.findall(r"ยาว (\d*)x เมตร", stem)
            p, q = (int(n) if n else 1 for n in lengths)
            v1, v2 = (sp.Rational(n) * 1000 / 3600 for n in re.findall(r"(\d+) กิโลเมตรต่อชั่วโมง", stem))
            head_on = int(re.search(r"(\d+) วินาที", stem).group(1))
            (length,) = sp.solve(sp.Eq((p + q) * x, (v1 + v2) * head_on), x)
            (time,) = sp.solve(sp.Eq((p + q) * length, abs(v2 - v1) * t), t)
            assert time == value, (seed, stem)
        else:
            v1, v2 = (sp.Rational(n) * 1000 / 3600
                      for n in re.search(r"ความเร็ว (\d+) และ (\d+)", stem).groups())
            overtake = int(re.search(r"ใช้เวลา (\d+) วินาที", stem).group(1))
            k = int(re.search(r"เป็น (\d+) เท่า", stem).group(1))
            # the short train is x, the long one kx; overtaking covers both at the speed difference
            (short,) = sp.solve(sp.Eq(x + k * x, abs(v2 - v1) * overtake), x)
            assert short == value, (seed, stem)


def test_transfer_probability_by_enumeration():
    for seed in SEEDS:
        stem, right = _draw("math.probability_transfer_m5", seed)
        r1, k1, r2, k2 = _ints(stem)[:4]
        want = "แดง" if stem.endswith("สีแดงเท่ากับเท่าใด") else "ดำ"
        box1 = ["แดง"] * r1 + ["ดำ"] * k1
        box2 = ["แดง"] * r2 + ["ดำ"] * k2
        hits = total = 0
        for moved in range(len(box1)):          # every labelled ball equally likely
            after = box2 + [box1[moved]]
            for drawn in range(len(after)):
                weight = Fraction(1, len(box1)) * Fraction(1, len(after))
                total += weight
                hits += weight if after[drawn] == want else 0
        assert total == 1 and hits == Fraction(right), (seed, stem)


def test_tangential_trapezoid_by_coordinates():
    for seed in SEEDS:
        stem, right = _draw("math.tangential_trapezoid_m5", seed)
        area = int(re.search(r"พื้นที่ (\d+) ตารางหน่วย", stem).group(1))
        cos_a = Fraction(re.search(r"cos\(∠DAB\) = (\d+/\d+)", stem).group(1))
        asked = re.search(r"ด้าน (\w+) ยาวกี่หน่วย", stem).group(1)
        cos_q = sp.Rational(cos_a.numerator, cos_a.denominator)
        leg = sp.symbols("leg", positive=True)
        # A at the origin, AB on the x-axis; D and C one leg up at angle A on either side.
        dx, dy = leg * cos_q, leg * sp.sqrt(1 - cos_q ** 2)
        dc = leg - dx                                  # AB + DC = 2·leg with AB = DC + 2·dx
        ab = dc + 2 * dx
        shape = sp.Polygon((0, 0), (ab, 0), (ab - dx, dy), (dx, dy))
        (solved,) = sp.solve(sp.Eq(abs(shape.area), area), leg)
        sides = {"AB": ab, "CD": dc, "AD": leg}
        assert sp.simplify(sides[asked].subs(leg, solved) - int(right)) == 0, (seed, stem)


def test_conjugate_root_cubic_by_solving_for_coefficients():
    a, b, c = sp.symbols("a b c")
    x = sp.symbols("x")
    for seed in SEEDS:
        stem, right = _draw("math.conjugate_root_cubic_m4", seed)
        factor = re.search(r"ถ้า (x(?: [−+] \d+)?) เป็นตัวประกอบ", stem).group(1)
        r = 0 if factor == "x" else (int(factor.split()[-1]) * (1 if "−" in factor else -1))
        root_text = re.search(r"และ P\((.+?)\) = 0", stem).group(1).replace("−", "-").replace(" ", "")
        root = sp.sympify(root_text.replace("√", "sqrt(") + ")" * root_text.count("√"))
        poly = x ** 3 + a * x ** 2 + b * x + c
        at_root = sp.expand(poly.subs(x, root))
        rational, irrational = at_root.as_independent(sp.sqrt(sp.Integer(_ints(root_text)[-1])))
        solution = sp.solve([poly.subs(x, r), rational, irrational], [a, b, c], dict=True)
        assert len(solution) == 1
        total = sum(solution[0][v] for v in (a, b, c))
        assert all(solution[0][v].is_integer for v in (a, b, c))
        assert total == int(right.replace("−", "-")), (seed, stem)


def test_continued_fraction_by_brute_force():
    for seed in SEEDS:
        stem, right = _draw("math.continued_fraction_p6", seed)
        d = int(re.search(r"z < (\d+)", stem).group(1))
        whole, num, den = map(int, re.search(r"= (\d+) (\d+)/(\d+) ค่าของ", stem).groups())
        target = whole + Fraction(num, den)
        found = {(x, y, z) for x in range(1, 20) for y in range(1, 20) for z in range(1, d)
                 if x + 1 / (y + Fraction(z, d)) == target}
        assert len(found) == 1, (seed, stem)
        assert sum(found.pop()) == int(right), (seed, stem)


def test_work_backwards_by_forward_simulation():
    steps = {
        "ได้รับเงินเพิ่มอีก (\\d+) บาท": lambda m, n: m + n,
        "ใช้เงินไป (\\d+) บาท": lambda m, n: m - n,
        "ได้รับเงินเพิ่มจนมีเป็น 2 เท่าของที่มีอยู่": lambda m, n: 2 * m,
        "ใช้เงินไปครึ่งหนึ่งของที่มีอยู่": lambda m, n: m / 2,
        "ใช้เงินไป 1/3 ของที่มีอยู่": lambda m, n: m - m / 3,
    }
    for seed in SEEDS:
        stem, right = _draw("math.work_backwards_p6", seed)
        body = stem.split("จำนวนหนึ่ง ", 1)[1].split(" ทำให้เหลือเงิน")[0]
        end = Fraction(re.search(r"เหลือเงิน (\d+) บาท", stem).group(1))
        plan = []
        for part in body.split(" จากนั้น"):
            (pattern, step), = [(p, f) for p, f in steps.items() if re.fullmatch(p, part)]
            m = re.fullmatch(pattern, part)
            plan.append((step, int(m.group(1)) if m.groups() else 0))
        start = Fraction(int(right.split()[0]))
        amount = start
        for step, n in plan:
            amount = step(amount, n)
        assert amount == end, (seed, stem)


def test_number_group_rule_is_the_only_one_that_fits():
    from itertools import permutations
    ops = {"+": lambda p, q: p + q, "−": lambda p, q: p - q, "×": lambda p, q: p * q}
    for seed in SEEDS:
        stem, right = _draw("math.number_group_relation_p6", seed)
        shown = [tuple(map(int, g)) for g in re.findall(r"ชุดที่ \d: (\d+), (\d+), (\d+) → (-?\d+)", stem)]
        last = tuple(map(int, re.search(r"ชุดที่ 4: (\d+), (\d+), (\d+) → \?", stem).groups()))
        assert len(shown) == 3
        # Every rule (p o1 q) o2 r over every order of the three numbers that fits the examples
        # must give the stated answer for the fourth group.
        answers = set()
        for order in permutations(range(3)):
            for o1, f1 in ops.items():
                for o2, f2 in ops.items():
                    rule = lambda g: f2(f1(g[order[0]], g[order[1]]), g[order[2]])
                    if all(rule(g[:3]) == g[3] for g in shown):
                        answers.add(rule(last))
        assert answers == {int(right)}, (seed, stem, answers)


def _block_digit(kind, position):
    """The digit at ``position`` found by skipping whole blocks, not by building the string."""
    if kind == "count":
        length, start, size = 1, 1, 9
        while position > length * size:
            position -= length * size
            length, start, size = length + 1, start * 10, size * 10
        number = start + (position - 1) // length
        return str(number)[(position - 1) % length]
    n = 1
    while position > n * len(str(n)):
        position -= n * len(str(n))
        n += 1
    return str(n)[(position - 1) % len(str(n))]


def test_digit_position_by_block_counting():
    for seed in SEEDS:
        stem, right = _draw("math.digit_position_m1", seed)
        kind = "count" if "0.123456789101112" in stem else "repeat"
        position = int(re.search(r"ตำแหน่งที่ (\d+)", stem).group(1))
        assert _block_digit(kind, position) == right, (seed, stem)


def test_catch_up_time_by_equation():
    t = sp.symbols("t", positive=True)
    for seed in SEEDS:
        stem, right = _draw("math.catch_up_time_m1", seed)
        h, m = map(int, re.search(r"เวลา (\d+):(\d+) น\. ด้วย", stem).groups())
        slow, fast = map(int, re.findall(r"(\d+) กิโลเมตรต่อชั่วโมง", stem))
        delay = int(re.search(r"อีก (\d+) นาที", stem).group(1))
        # Distances from home in km with t in minutes after the younger one leaves.
        (meet,) = sp.solve(sp.Eq(sp.Rational(slow, 60) * (t + delay), sp.Rational(fast, 60) * t), t)
        total = h * 60 + m + delay + meet
        assert f"{int(total) // 60}:{int(total) % 60:02d} น." == right and total == int(total), (seed, stem)


def test_consecutive_product_by_search():
    for seed in SEEDS:
        stem, right = _draw("math.consecutive_product_m1", seed)
        step = 2 if stem.startswith("จำนวนคู่") else 1
        count = int(re.search(r" (\d) จำนวนที่เรียงติดกัน", stem).group(1))
        product = int(re.search(r"คูณกันได้ ([\d,]+)", stem).group(1).replace(",", ""))
        runs = [range(a, a + step * count, step) for a in range(1, 400)
                if all(n % 2 == 0 for n in range(a, a + step * count, step)) or step == 1]
        found = [r for r in runs if math.prod(r) == product]
        assert len(found) == 1 and sum(found[0]) == int(right), (seed, stem)


def test_number_base_by_python_conversion():
    for seed in SEEDS:
        stem, right = _draw("math.number_base_m1", seed)
        if "ค่า RGB เป็น (" in stem:
            rgb = map(int, re.search(r"\((\d+), (\d+), (\d+)\)", stem).groups())
            expected = sum(int(d, 16) for v in rgb for d in format(v, "02X"))
        elif "ค่า HEX เป็น #" in stem:
            code = re.search(r"#([0-9A-F]{6})", stem).group(1)
            a, b, c = (int(code[i:i + 2], 16) for i in (0, 2, 4))
            expected = a - b + c
        else:
            expected = format(int(re.search(r"เขียน (\d+) ใน", stem).group(1)), "b").count("1")
        assert expected == int(right), (seed, stem)


def test_defined_operation_by_sympy():
    a, b = sp.symbols("a b")
    for seed in SEEDS:
        stem, right = _draw("math.defined_operation_p6", seed)
        rule = re.search(r"a ⊕ b = (.+?) จงหาค่าของ", stem).group(1).replace("×", "*").replace("−", "-")
        x, y, z = map(int, re.search(r"\((\d+) ⊕ (\d+)\) ⊕ (\d+)", stem).groups())
        from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr,
                                                standard_transformations)
        expr = parse_expr(rule, transformations=standard_transformations + (implicit_multiplication_application,))
        op = lambda p, q: expr.subs({a: p, b: q})
        assert op(op(x, y), z) == int(right), (seed, stem)


def test_square_circle_radius_by_tangency():
    r = sp.symbols("r", positive=True)
    for seed in SEEDS:
        stem, right = _draw("math.square_circle_radius_m3", seed)
        s = int(re.search(r"ยาวด้านละ (\d+)", stem).group(1))
        # Centre on the perpendicular bisector of AD, at distance s − r from AD (tangent to BC).
        (solved,) = sp.solve(sp.Eq(r ** 2, (sp.Rational(s, 2)) ** 2 + (s - r) ** 2), r)
        assert solved == sp.Rational(right), (seed, stem)


def test_circle_petal_area_by_lens_formula():
    for seed in SEEDS:
        stem, right = _draw("math.circle_petal_area_p6", seed)
        r = int(re.search(r"รัศมี (\d+) เซนติเมตร", stem).group(1))
        petals = int(re.search(r"กลีบ (\d+) กลีบ", stem).group(1))
        d = r * sp.sqrt(2)               # quarter arcs: the centres are r√2 apart
        lens = 2 * r ** 2 * sp.acos(d / (2 * r)) - (d / 2) * sp.sqrt(4 * r ** 2 - d ** 2)
        value = sp.nsimplify(petals * lens).subs(sp.pi, sp.Rational(22, 7))
        assert sp.simplify(value - sp.Rational(right)) == 0, (seed, stem)


def test_real_power_roots_by_enumeration():
    v = sp.symbols("v")
    for seed in SEEDS:
        stem, right = _draw("math.real_power_roots_m2", seed)
        sixth, cube, fourth = (sp.Rational(s.replace("−", "-")) for s in
                               re.search(r"\(x²\)³ = (\S+), y³ = (\S+) และ z⁴ = (\S+) ", stem).groups())
        roots = lambda expr: [s for s in sp.solve(expr, v) if s.is_real]
        xs, ys, zs = roots(v ** 6 - sixth), roots(v ** 3 - cube), roots(v ** 4 - fourth)
        best = min(x + y - z for x in xs for y in ys for z in zs)
        assert best == sp.Rational(right.replace("−", "-")), (seed, stem)


def test_sum_quotient_numbers_by_search():
    for seed in SEEDS:
        stem, right = _draw("math.sum_quotient_numbers_m1", seed)
        s, q = map(int, re.search(r"เท่ากับ (\d+) และผลหาร.*?เท่ากับ (\d+)", stem).groups())
        (a, b), = [(a, s - a) for a in range(1, s) if (s - a) and a == q * (s - a)]
        expected = a * b if "ผลคูณ" in stem else a - b
        assert expected == int(right), (seed, stem)


def test_telescoping_product_by_multiplying_out():
    for seed in SEEDS:
        stem, right = _draw("math.telescoping_product_m1", seed)
        op = "−" if "(1 − 1/" in stem else "+"
        nums = [int(n) for n in re.findall(r"\(1 [−+] 1/(\d+)\)", stem)]
        start, end = nums[0], nums[-1]
        value = Fraction(1)
        for k in range(start, end + 1):
            value *= (k - 1 if op == "−" else k + 1) / Fraction(k)
        assert value == Fraction(right), (seed, stem)


def test_row_pattern_position_by_building_rows():
    for seed in SEEDS:
        stem, right = _draw("math.row_pattern_position_p6", seed)
        shown = [list(map(int, r.split())) for r in re.findall(r"แถว \d: ([\d ]+?)(?:;|$)", stem)]
        first, step = shown[0][0], shown[1][1] - shown[1][0]
        row, pos = map(int, re.search(r"แถวที่ (\d+) ตำแหน่งที่ (\d+)", stem).groups())
        numbers = iter(range(first, first + step * row * row + 1, step))
        rows = [[next(numbers) for _ in range(2 * r - 1)] for r in range(1, row + 1)]
        assert rows[:3] == shown and rows[row - 1][pos - 1] == int(right), (seed, stem)


def test_reciprocal_power_sum_by_sympy():
    x = sp.symbols("x")
    for seed in SEEDS:
        stem, right = _draw("math.reciprocal_power_sum_m3", seed)
        a = int(re.search(r"= (\d+) เมื่อ", stem).group(1))
        n = 2 if "x² + 1/x²" in stem else 3
        root = max(sp.solve(x + 1 / x - a, x), key=lambda r: float(r))
        assert sp.simplify(root ** n + root ** -n - int(right)) == 0, (seed, stem)


def test_ratio_after_removal_by_search():
    for seed in SEEDS:
        stem, right = _draw("math.ratio_after_removal_m1", seed)
        p, q, n, r, s = map(int, re.search(r"อัตราส่วน (\d+) : (\d+) หยิบออกไปอย่างละ (\d+) เม็ด เหลือ.*?เป็น (\d+) : (\d+)", stem).groups())
        found = [(g, red) for red in range(1, 500) for g in [Fraction(red * p, q)]
                 if g.denominator == 1 and red > n and (g - n) * s == (red - n) * r]
        assert [red for _, red in found] == [int(right)], (seed, stem)


def test_periodic_schedule_by_calendar_walk():
    days = ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์")
    for seed in SEEDS:
        stem, right = _draw("math.periodic_schedule_p4", seed)
        start = days.index(re.search(r"เป็นวัน(\S+?) ตลอด", stem).group(1))
        span = int(re.search(r"ตลอด (\d+) วัน", stem).group(1))
        each = int(re.search(r"วันละ (\d+) ฉบับ", stem).group(1))
        busy = {days.index(d) for d in re.findall(r"วัน(\S+?)(?= |$)", stem.split("เฉพาะ")[1].split(" น้อง")[0])}
        letters, today = 0, start
        for _ in range(span):
            letters += each if today in busy else 0
            today = (today + 1) % 7
        assert letters == int(right), (seed, stem)


def test_percent_after_adding_by_search():
    for seed in SEEDS:
        stem, right = _draw("math.percent_after_adding_p6", seed)
        total, old, new = (int(n.replace(",", "")) for n in re.findall(r"([\d,]+)", stem)[:3])
        white = total * old // 100
        (added,) = [k for k in range(0, 20000) if (white + k) * 100 == new * (total + k)]
        assert added == int(right), (seed, stem)


def test_count_multiples_by_enumeration():
    for seed in SEEDS:
        stem, right = _draw("math.count_multiples_either_p6", seed)
        lo, hi, a, b = map(int, re.search(r"ตั้งแต่ (\d+) ถึง (\d+) ที่หารด้วย (\d+) (?:และ|หรือ) (\d+)", stem).groups())
        test = (lambda n: n % a == 0 and n % b == 0) if "ทั้งคู่" in stem else (lambda n: n % a == 0 or n % b == 0)
        assert sum(1 for n in range(lo, hi + 1) if test(n)) == int(right), (seed, stem)


def test_british_flag_by_coordinates():
    xs, ys = sp.symbols("x y", positive=True)
    for seed in SEEDS:
        stem, right = _draw("math.british_flag_m2", seed)
        pa, pb, pc = map(int, re.search(r"PA = (\d+), PB = (\d+) และ PC = (\d+)", stem).groups())
        # A(0, 0), B(w, 0), C(w, h), D(0, h), P(x, y): PD² = x² + (h − y)² for any w, h that fit.
        w, h = sp.symbols("w h", positive=True)
        pd2 = (xs ** 2 + ys ** 2 + (w - xs) ** 2 + (h - ys) ** 2) - ((w - xs) ** 2 + ys ** 2)
        identity = sp.expand(pd2 - (xs ** 2 + (h - ys) ** 2))   # PA² + PC² − PB² equals PD²
        assert identity == 0
        assert pa ** 2 + pc ** 2 - pb ** 2 == int(right) ** 2, (seed, stem)
