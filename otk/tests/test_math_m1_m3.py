"""ม.1–ม.3 enrichment: answers re-derived from what the learner is shown."""

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
M1 = keys_from("math_m1")
M2 = keys_from("math_m2")
M3 = keys_from("math_m3")
ENRICHED = ["math.system_word_problem", "math.trig_application_height", "math.similar_shadow"]


def _stem(q) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in q.stem)


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _numbers(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"-?\d+", s.replace(",", ""))]


def _pos(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s.replace(",", ""))]


def _frac(tex: str) -> Fraction:
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if not m:
        return Fraction(int(tex))
    sign, n, d = m.groups()
    return (-1 if sign else 1) * Fraction(int(n), int(d))


def test_module_sizes():
    assert (len(M1), len(M2), len(M3)) == (17, 10, 15)


@pytest.mark.parametrize("key", M1 + M2 + M3 + ENRICHED)
def test_four_distinct_choices(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        assert len(q.choices) == REGISTRY[key].max_choices, (key, seed, _stem(q))
        assert len({_choice(c) for c in q.choices}) == REGISTRY[key].max_choices


# ── ม.1 ──────────────────────────────────────────────────────────────────────

def test_integer_stories():
    for seed in SEEDS:
        q = generate("math.integer_word_problem_m1", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = _numbers(s)
        if "ตอนบ่าย" in s:
            assert ans == n[0] + n[1]
        elif "ยอดเขา" in s:
            assert ans == n[0] - n[1]
        elif "บัญชี" in s:
            assert ans == n[0] - n[1] + n[2]
        else:
            assert ans == abs(n[0] - n[1])
        q = generate("math.integer_distance_m1", Random(seed))
        a, b = _numbers(q.stem[-1].tex)
        want = abs(a - b) if "ห่างกัน" in _stem(q) else abs(a) + abs(b)
        assert int(_answer(q)) == want


def test_repeating_decimals():
    for seed in SEEDS:
        q = generate("math.repeating_decimal_to_fraction_m1", Random(seed))
        tex = q.stem[-1].tex
        m = re.fullmatch(r"0\.(\d?)((?:\\dot\{\d\})+)", tex)
        head, rep = m.group(1), "".join(re.findall(r"\d", m.group(2)))
        # x = 0.head(rep): value = (head rep − head) / (9…9 0…0).
        num = int(head + rep) - int(head or "0")
        den = int("9" * len(rep) + "0" * len(head))
        want = Fraction(num, den)
        values = [_frac(_choice(c)) for c in q.choices]
        assert values[q.answer] == want and values.count(want) == 1
        q = generate("math.terminating_or_repeating_m1", Random(seed))
        want_repeat = "ซ้ำ" in _stem(q)

        def terminates(f: Fraction) -> bool:
            d = f.denominator
            for p in (2, 5):
                while d % p == 0:
                    d //= p
            return d == 1
        flags = [terminates(_frac(_choice(c))) != want_repeat for c in q.choices]
        assert flags.count(True) == 1 and flags[q.answer]


def test_signed_decimals():
    for seed in SEEDS:
        q = generate("math.signed_decimal_ops_m1", Random(seed))
        expr = q.stem[-1].tex.replace(r"\times", "*").replace(r"\div", "/")
        nums = re.findall(r"-?\d+(?:\.\d+)?", expr)
        ops = re.findall(r"\s([+\-*/])\s", expr)
        a, b = Decimal(nums[0]), Decimal(nums[1])
        want = {"+": a + b, "-": a - b, "*": a * b, "/": a / b}[ops[0]]
        assert Decimal(_answer(q)) == want


def _solve(eq: str) -> Fraction:
    from otk.sets.math.m1.linear_equations import _solve_linear
    return _solve_linear(eq)


def test_equation_stories_and_setup():
    for seed in SEEDS:
        q = generate("math.linear_equation_setup_m1", Random(seed))
        right = _solve(_answer(q))
        for i, c in enumerate(q.choices):
            if i == q.answer:
                continue
            try:
                v = _solve(_choice(c))
            except Exception:
                v = None
            assert v != right, (_stem(q), _choice(c))
        w = generate("math.linear_word_problem_m1", Random(seed))
        assert w.stem[0].text == q.stem[0].text
        ans, s = int(_answer(w)), w.stem[0].text
        x = right
        if "มากที่สุด" in s:
            assert ans == x + 2
        elif "มุมที่ใหญ่ที่สุด" in s:
            assert ans == int(re.findall(r"(\d+)x องศา", s)[-1]) * x
        else:
            assert ans == x, s


def test_ratio_percent_m1():
    for seed in SEEDS:
        q = generate("math.three_term_ratio_m1", Random(seed))
        s = _stem(q)
        if "a : b : c" in s:
            a, b1 = map(int, re.search(r"a : b = (\d+) : (\d+)", s).groups())
            b2, c = map(int, re.search(r"b : c = (\d+) : (\d+)", s).groups())
            A, B, C = map(int, _answer(q).split(" : "))
            assert Fraction(A, B) == Fraction(a, b1) and Fraction(B, C) == Fraction(b2, c)
            assert math.gcd(math.gcd(A, B), C) == 1
        else:
            total, A, B, C = _pos(s)[:4]
            assert int(_answer(q)) * (A + B + C) == total * C
        q = generate("math.percent_word_problem_m1", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = _pos(s)
        if "ฝากเงิน" in s:
            assert ans * 100 == n[0] * (100 + n[1])
        elif "คอมมิชชัน" in s:
            assert ans * 100 == n[0] * n[1]
        elif "ข้อสอบ" in s:
            assert ans * n[0] == n[1] * 100
        elif "ภาษี" in s:
            assert ans == n[0] * 107 // 100
        elif "ราคาเดิม" in s:
            assert ans * (100 - n[0]) == n[1] * 100
        else:
            assert ans * n[0] == (n[1] - n[0]) * 100


def test_linear_relations():
    for seed in SEEDS:
        q = generate("math.linear_relation_context_m1", Random(seed))
        rule = q.stem[-1].tex
        c, sign, m = re.fullmatch(r"y = (\d+) ([+-]) (\d*)x", rule).groups()
        m = (int(m) if m else 1) * (1 if sign == "+" else -1)
        c = int(c)
        given = _pos(q.stem[0].text)[-1]
        if "แล้ว y" in q.stem[0].text:
            assert int(_answer(q)) == c + m * given
        else:
            assert c + m * int(_answer(q)) == given
        q = generate("math.table_to_linear_equation_m1", Random(seed))
        lines = q.stem[0].text.split("\n")
        xs = [int(v) for v in lines[1].split("|")[1:]]
        ys = [int(v) for v in lines[2].split("|")[1:]]
        for i, ch in enumerate(q.choices):
            # A unit coefficient is written bare: y = x + 3, y = -x + 3.
            k, sgn, b = re.fullmatch(r"y = (-?\d*)x ([+-]) (\d+)", _choice(ch)).groups()
            k = {"": "1", "-": "-1"}.get(k, k)
            b = int(b) * (1 if sgn == "+" else -1)
            fits = all(int(k) * x + b == y for x, y in zip(xs, ys))
            assert fits == (i == q.answer)


def test_statistics_m1():
    for seed in SEEDS:
        q = generate("math.mean_missing_value_m1", Random(seed))
        n = _pos(_stem(q))
        count, mean, known = n[0], n[1], n[3:]
        assert int(_answer(q)) + sum(known) == count * mean
        q = generate("math.frequency_table_m1", Random(seed))
        lines = q.stem[0].text.split("\n")
        rows = [tuple(map(int, ln.split(" | "))) for ln in lines[2:-1]]
        ask, ans = lines[-1], int(_answer(q))
        if "ฐานนิยม" in ask:
            assert ans == max(rows, key=lambda r: r[1])[0]
        elif "ทั้งหมด" in ask:
            assert ans == sum(f for _, f in rows)
        else:
            cut = _pos(ask)[0]
            assert ans == sum(f for s, f in rows if s >= cut)


def test_space_m1():
    for seed in SEEDS:
        q = generate("math.solid_nets_m1", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = {"สามเหลี่ยม": 3, "สี่เหลี่ยม": 4, "ห้าเหลี่ยม": 5, "หกเหลี่ยม": 6,
             "แปดเหลี่ยม": 8}[re.search(r"ฐาน(\S+?เหลี่ยม)", s).group(1)]
        if "หน้าข้าง" in s:
            assert ans == n
        elif "ปริซึม" in s and "รูปหลายเหลี่ยม" in s:
            assert ans == n + 2
        elif "พีระมิด" in s:
            assert ans == n + 1
        else:
            assert ans == 3 * n
        q = generate("math.cube_stack_m1", Random(seed))
        a, b, c = _pos(_stem(q))[:3]
        s, ans = _stem(q), int(_answer(q))
        cubes = [(i, j, k) for i in range(a) for j in range(b) for k in range(c)]
        faces = [sum(v in (0, top - 1) for v, top in zip(p, (a, b, c))) for p in cubes]
        if "ใช้ลูกบาศก์เล็กทั้งหมด" in s:
            assert ans == len(cubes)
        elif "3 ด้าน" in s:
            assert ans == faces.count(3)
        elif "ไม่ถูกทาสี" in s:
            assert ans == faces.count(0)
        else:
            assert ans == faces.count(2)


# ── ม.2 ──────────────────────────────────────────────────────────────────────

def test_pythagoras_m2():
    for seed in SEEDS:
        q = generate("math.pythagoras_word_problem_m2", Random(seed))
        x, y = _pos(_stem(q))[:2]
        ans = int(_answer(q))
        if "ยาวกี่" in _stem(q) and "ทางลาด" in _stem(q) or "เส้นทแยงมุม" in _stem(q) \
                or "จุดเริ่มต้น" in _stem(q):
            assert ans * ans == x * x + y * y
        else:
            assert ans * ans == x * x - y * y
        q = generate("math.pythagoras_grid_distance_m2", Random(seed))
        x1, y1, x2, y2 = _numbers(q.stem[-1].tex)
        assert int(_answer(q)) ** 2 == (x1 - x2) ** 2 + (y1 - y2) ** 2


def test_roots_m2():
    for seed in SEEDS:
        q = generate("math.roots_of_perfect_powers_m2", Random(seed))
        tex, ans = q.stem[-1].tex, _answer(q)
        if tex.startswith(r"\sqrt[3]"):
            inside = tex[len(r"\sqrt[3]{"):-1]
            v = _frac(inside) if "frac" in inside else Fraction(int(inside))
            assert _frac(ans) ** 3 == v
        elif r"\frac" in tex:
            n, d = _pos(tex)
            assert _frac(ans) ** 2 == Fraction(n, d)
        else:
            assert Decimal(ans) ** 2 == Decimal(tex[len(r"\sqrt{"):-1])


def test_surface_and_volume_m2():
    pi = Fraction(22, 7)
    for seed in SEEDS:
        q = generate("math.cylinder_surface_area_m2", Random(seed))
        r, h = _pos(_stem(q))[:2]
        ans = int(_answer(q))
        lateral = 2 * pi * r * h
        assert ans == (lateral if "ฉลาก" in _stem(q) else lateral + 2 * pi * r * r)
        q = generate("math.prism_surface_area_m2", Random(seed))
        n = _pos(_stem(q))
        if "สามเหลี่ยม" in _stem(q):
            a, b, c, length = n[:4]
            assert int(_answer(q)) == a * b + (a + b + c) * length
        else:
            w, span, h = n[:3]
            assert int(_answer(q)) == 2 * (w * span + span * h + w * h)


def test_statistics_m2():
    for seed in SEEDS:
        q = generate("math.stem_and_leaf_m2", Random(seed))
        lines = q.stem[0].text.split("\n")
        data = sorted(10 * int(st) + int(leaf) for ln in lines[1:-1]
                      for st, leaves in [ln.split(" | ")] for leaf in leaves.split())
        ask, ans = lines[-1], _answer(q)
        if "กี่คน" in ask and "ตั้งแต่" not in ask:
            assert int(ans) == len(data)
        elif "พิสัย" in ask:
            assert int(ans) == data[-1] - data[0]
        elif "ตั้งแต่" in ask:
            assert int(ans) == sum(1 for v in data if v >= _pos(ask)[0])
        else:
            n = len(data)
            med = data[n // 2] if n % 2 else (data[n // 2 - 1] + data[n // 2]) / 2
            assert float(ans) == med
        q = generate("math.dot_plot_m2", Random(seed))
        lines = q.stem[0].text.split("\n")
        rows = {int(ln.split(":")[0]): ln.count("●") for ln in lines[1:-1]}
        ask, ans = lines[-1], int(_answer(q))
        if "ฐานนิยม" in ask:
            assert ans == max(rows, key=rows.get)
        elif "กี่ค่า" in ask:
            assert ans == sum(rows.values())
        else:
            assert ans == sum(v * c for v, c in rows.items())


# ── ม.3 ──────────────────────────────────────────────────────────────────────

def test_probability():
    for seed in SEEDS:
        q = generate("math.probability_die_coin_m3", Random(seed))
        s = _stem(q)
        if "ลูกเต๋า" in s:
            tests = {"แต้มคู่": lambda n: n % 2 == 0, "แต้มคี่": lambda n: n % 2 == 1,
                     "มากกว่า 4": lambda n: n > 4, "น้อยกว่า 3": lambda n: n < 3,
                     "จำนวนเฉพาะ": lambda n: n in (2, 3, 5), "หารด้วย 3": lambda n: n % 3 == 0,
                     "แต้ม 7": lambda n: n == 7, "ไม่เกิน 6": lambda n: n <= 6}
            test = next(t for k, t in tests.items() if k in s)
            want = Fraction(sum(test(n) for n in range(1, 7)), 6)
        else:
            sectors, red = _pos(s)[:2]
            want = Fraction(red, sectors)
        assert _frac(_answer(q)) == want
        q = generate("math.probability_two_events_m3", Random(seed))
        s = _stem(q)
        if "ผลรวม" in s:
            t = _pos(s)[-1]
            want = Fraction(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == t), 36)
            assert _frac(_answer(q)) == want


def test_inequality_and_quadratic():
    for seed in SEEDS:
        q = generate("math.inequality_word_problem_m3", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = _pos(s)
        if "สมุด" in s:
            money, fixed, per = n[:3]
            assert fixed + per * ans <= money < fixed + per * (ans + 1)
        elif "ลิฟต์" in s:
            limit, person, box = n[:3]
            assert person + box * ans <= limit < person + box * (ans + 1)
        elif "คะแนนเฉลี่ย" in s:
            known, need = n[1:4], n[5]
            assert (sum(known) + ans) >= 4 * need > sum(known) + ans - 1
        else:
            cap = n[0]
            x = ans - 2
            assert 3 * x + 3 <= cap < 3 * (x + 1) + 3
        q = generate("math.quadratic_word_problem_m3", Random(seed))
        s, x = _stem(q), int(_answer(q))
        n = _pos(s)
        if "สนามรูปสี่เหลี่ยมผืนผ้า" in s:
            assert x * (x + n[0]) == n[1]
        elif "ผลคูณ" in s:
            assert x * (x + 1) == n[0]
        elif "ยกกำลังสอง" in s:
            assert x * x - n[0] * x == n[1]
        else:
            assert (x + 2 * n[0]) ** 2 == n[1]


def test_solids_m3():
    pi = Fraction(22, 7)
    for seed in SEEDS:
        q = generate("math.pyramid_volume_m3", Random(seed))
        n, ans = _pos(_stem(q)), int(_answer(q))
        if "พีระมิดสูงกี่" in _stem(q):
            assert Fraction(n[0] ** 2 * ans, 3) == n[1]
        else:
            assert Fraction(n[0] ** 2 * n[1], 3) == ans
        q = generate("math.cone_sphere_surface_area_m3", Random(seed))
        n, ans, s = _pos(_stem(q)), int(_answer(q)), _stem(q)
        if "ครึ่งทรงกลม" in s:
            assert ans == 2 * pi * n[0] ** 2
        elif "ทรงกลม" in s:
            assert ans == 4 * pi * n[0] ** 2
        elif "สูงเอียง" in s:
            assert ans == pi * n[0] * n[1]
        else:
            r, h = n[:2]
            length = math.isqrt(r * r + h * h)
            assert ans == pi * r * length + pi * r * r


def _trig_value(tex: str) -> float:
    """Evaluate a small TeX expression of special-angle trig values."""
    import math as m
    s = re.sub(r"\\(sin|cos|tan)\^\{2\} (\d+)\^\{\\circ\}", r"(m.\1(m.radians(\2))**2)", tex)
    s = re.sub(r"\\(sin|cos|tan) (\d+)\^\{\\circ\}", r"m.\1(m.radians(\2))", s)
    s = re.sub(r"\\sqrt\{(\d+)\}", r"m.sqrt(\1)", s)
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"((\1)/(\2))", s).replace(" ", "")
    s = re.sub(r"(?<=[\d)])(?=m\.|\()", "*", s)
    return eval(s, {"m": m})  # noqa: S307 - test-only, generated input


def test_trig_values():
    for seed in SEEDS:
        q = generate("math.trig_special_values_m3", Random(seed))
        want = _trig_value(q.stem[-1].tex)
        values = [_trig_value(_choice(c)) for c in q.choices]
        assert abs(values[q.answer] - want) < 1e-9
        assert sum(abs(v - want) < 1e-9 for v in values) == 1


def test_similarity_tangent_boxplot():
    for seed in SEEDS:
        q = generate("math.tangent_length_m3", Random(seed))
        n, s = _pos(_stem(q)), _stem(q)
        if "มุม" in s:
            assert _answer(q) == "90"
        else:
            r, d = n[:2]
            assert int(_answer(q)) ** 2 == d * d - r * r
        q = generate("math.box_plot_summary_m3", Random(seed))
        s = _stem(q)
        data = sorted(_pos(s.split("คือ ")[1].split(" ")[0] + "," + ",".join(
            s.split("คือ ")[1].split(", ")[1:]))[: 11])
        data = sorted(int(v) for v in re.findall(r"\d+", s.split("คือ ")[1].split(" ม")[0]
                                                 .split(" ค")[0].split(" พ")[0]))
        n = len(data)
        q1, med, q3 = data[(n + 1) // 4 - 1], data[(n + 1) // 2 - 1], data[3 * (n + 1) // 4 - 1]
        ans = int(_answer(q))
        if "มัธยฐาน" in s:
            assert ans == med
        elif "ที่ 1" in s:
            assert ans == q1
        elif "ที่ 3" in s:
            assert ans == q3
        else:
            assert ans == q3 - q1


def test_system_word_problem_solves():
    for seed in SEEDS:
        q = generate("math.system_word_problem", Random(seed))
        s, x = _stem(q), int(_answer(q))
        n = _pos(s)
        if "ผู้ใหญ่" in s:
            total, pa, pc, money = n[:4]
            assert pa * x + pc * (total - x) == money
        elif "กระต่าย" in s:
            heads, legs = n[:2]
            assert 4 * x + 2 * (heads - x) == legs
        elif "เหรียญ" in s:
            count, money = n[0], n[1]
            assert 10 * x + 5 * (count - x) == money
        else:
            total, diff = n[:2]
            assert 2 * x == total + diff
