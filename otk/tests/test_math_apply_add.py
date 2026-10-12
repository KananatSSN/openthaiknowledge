"""Harder application sets for the เพิ่มเติม track: five situations each, four
distinct choices, and answers re-derived by brute force from the numbers in
the question (simulating, integrating, or solving directly)."""

from __future__ import annotations

from otk.tests._origins import keys_from

import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import generate

SEEDS = range(300)
KEYS = keys_from("math_apply_add")


def _text(q) -> str:
    return " ".join(b.text for b in q.stem if b.kind == "text")


def _answer(q) -> str:
    return " ".join(getattr(b, "tex", "") for b in q.choices[q.answer].content)


def _nums(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s.replace("{,}", "").replace(",", ""))]


def _value(tex: str) -> float:
    tex = tex.replace("{,}", "")
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if m:
        return (-1 if m.group(1) else 1) * int(m.group(2)) / int(m.group(3))
    m = re.fullmatch(r"(\d*)\\sqrt\{(\d+)\}", tex)
    if m:
        return int(m.group(1) or 1) * math.sqrt(int(m.group(2)))
    m = re.fullmatch(r"\\frac\{(\d+)\\sqrt\{3\}\}\{(\d+)\}", tex)
    if m:
        return int(m.group(1)) * math.sqrt(3) / int(m.group(2))
    return float(tex)


def test_ten_sets_five_situations_four_choices():
    assert len(KEYS) == 10
    for key in KEYS:
        openings = set()
        for seed in SEEDS:
            q = generate(key, Random(seed))
            choices = [" ".join(getattr(b, "tex", "") for b in c.content) for c in q.choices]
            assert len(set(choices)) == 4 == len(choices), (key, seed, choices)
            openings.add(re.sub(r"[\d,]+", "#", _text(q))[:25])
        assert len(openings) >= 5, (key, openings)


def _check(key: str, q) -> None:
    t, ans = _text(q), _answer(q)
    n = _nums(t)
    if key == "math.cosine_rule_distance_m5":
        ang = 60 if "60 องศา" in t else 120
        c = math.cos(math.radians(ang))
        if "เรือสองลำ" in t:
            p, q_, h = n[1], n[2], n[3]
            assert math.isclose(_value(ans), h * math.sqrt(p * p + q_ * q_ - 2 * p * q_ * c))
        elif "ผู้สำรวจ" in t or "โดรน" in t:
            p, q_ = (n[0], n[1]) if "ผู้สำรวจ" in t else (n[0], n[1])
            assert math.isclose(_value(ans), math.sqrt(p * p + q_ * q_ - 2 * p * q_ * c))
        elif "ทางเดิน" in t:
            p, q_ = n[0], n[1]
            assert math.isclose(_value(ans), p + q_ - math.sqrt(p * p + q_ * q_ - 2 * p * q_ * c))
        else:
            p, q_, cost = n[0], n[1], n[3]
            d = math.sqrt(p * p + q_ * q_ - 2 * p * q_ * c)
            assert math.isclose(_value(ans), (p + q_ + d) * cost)
    elif key == "math.two_angle_height_m5":
        r3 = math.sqrt(3)
        if "เสาธง" in t:
            d = n[1]
            assert math.isclose(_value(ans), d / (r3 - 1 / r3))
        elif "แม่น้ำ" in t:
            d = n[1]
            assert math.isclose(_value(ans), d / (3 - 1))           # x·√3 = (x + d)/√3
        elif "ประภาคาร" in t:
            h = n[0]
            assert math.isclose(_value(ans), h * r3 - h / r3)
        elif "หอคอย" in t:
            H = n[0]
            assert math.isclose(_value(ans), H + (H / r3) / r3)
        else:
            h, sec = n[0], n[2]
            assert math.isclose(_value(ans), (h * r3 - h / r3) / sec)
    elif key == "math.vector_resultant_word_m5":
        if "กว้าง" in t:
            w, b, a = n[0], n[1], n[2]
            assert _value(ans) == a * w / b
        elif "ตะวันออก" in t and "นักสำรวจ" in t:
            e, north, back = n[0], n[1], n[2]
            assert math.isclose(_value(ans), math.hypot(e - back, north))
        elif "เครื่องบิน" in t:
            b, a, hrs = n[0], n[1], n[2]
            assert math.isclose(_value(ans), math.hypot(a, b) * hrs)
        else:
            x, y = n[0], n[1]
            assert math.isclose(_value(ans), math.hypot(x, y))
    elif key == "math.matrix_system_word_m5":
        if "เหรียญ" in t:
            total, money = n[-2], n[-1]
            tens = [k for k in range(total + 1) if 5 * (total - k) + 10 * k == money]
            assert tens == [int(ans)]
        elif "ฟาร์ม" in t:
            heads, legs = n[0], n[1]
            assert [k for k in range(heads + 1) if 2 * (heads - k) + 4 * k == legs] == [int(ans)]
        else:
            a1, c1, m1, a2, c2, m2 = n[:6]
            det = a1 * c2 - a2 * c1
            x = Fraction(m1 * c2 - m2 * c1, det)
            y = Fraction(a1 * m2 - a2 * m1, det)
            if "ครอบครัว" in t:
                assert _value(ans) == n[6] * x + n[7] * y
            elif "สมุด" in t:
                assert _value(ans) == x
            else:
                assert _value(ans) == abs(x - y)
    elif key == "math.expected_value_game_m5":
        if "ลูกเต๋า" in t:
            fee, big, small = n[0], n[2], n[5]
            ev = sum(Fraction(1, 6) * (big if f == 6 else small if f in (4, 5) else 0) for f in range(1, 7)) - fee
        elif "เหรียญสองเหรียญ" in t:
            big, small = n[0], n[1]
            outcomes = [(a, b) for a in (0, 1) for b in (0, 1)]
            ev = sum(Fraction(1, 4) * (big if a + b == 2 else small if a + b == 1 else 0) for a, b in outcomes)
        elif "สลาก" in t:
            tickets, price, first, n2, second = n[0], n[1], n[3], n[4], n[5]
            ev = Fraction(first + n2 * second, tickets) - price
        elif "ประกัน" in t:
            premium, claim, per = n[0], n[1], n[3]
            ev = premium - Fraction(claim, per)
        else:
            red, blue, win, lose = n[:4]
            ev = Fraction(red * win - blue * lose, red + blue)
        assert math.isclose(_value(ans), float(ev)), (t, ans)
    elif key == "math.quadratic_inequality_word_m4":
        m = re.fullmatch(r"(\d+) \\leq ([xp]) \\leq (\d+)", ans)
        if "ลูกบอล" in t:
            coeffs = n[:-2] if len(n) > 3 else n
            base, v = (0, n[0]) if len(n) == 3 else (n[0], n[1])
            height = n[-1]
            ts = [i / 100 for i in range(0, 2001)]
            above = [x for x in ts if base + v * x - 5 * x * x >= height - 1e-9]
            assert math.isclose(max(above) - min(above), _value(ans), abs_tol=0.02), coeffs
        elif "กำไร" in t:
            b, c, gain = n[0], n[1], n[2]
            ok = [x for x in range(0, 60) if -x * x + b * x - c >= gain]
            assert (int(m.group(1)), int(m.group(3))) == (min(ok), max(ok))
        elif "รั้ว" in t:
            fence, area = n[0], n[1]
            ok = [x for x in range(1, fence) if x * (fence // 2 - x) >= area]
            assert (int(m.group(1)), int(m.group(3))) == (min(ok), max(ok))
        elif "บัตร" in t:
            N, k, rev = n[0], n[1], n[2]
            ok = [p for p in range(1, N // k) if p * (N - k * p) >= rev]
            assert (int(m.group(1)), int(m.group(3))) == (min(ok), max(ok))
        else:
            limit = n[-1]
            ok = [v for v in range(1, 400) if v + v * v / 20 <= limit]
            assert max(ok) == int(ans)
    elif key == "math.geometric_series_word_m6":
        if "ครั้งที่" in t and "จนหยุด" not in t:
            H, hits = n[0], n[1]
            dist, h = 0.0, float(H)
            for i in range(hits):
                dist += h
                h /= 2
                if i < hits - 1:
                    dist += h
            assert math.isclose(_value(ans), dist)
        elif "จนหยุด" in t:
            first, num, den = n[0], n[1], n[2]
            r = num / den
            if "ลูกบอล" in t:
                total, h = 0.0, float(first)
                for _ in range(4000):
                    total += h
                    h *= r
                    total += h
                assert math.isclose(_value(ans), total, rel_tol=1e-6)
            else:
                assert math.isclose(_value(ans), sum(first * r ** i for i in range(4000)), rel_tol=1e-6)
        elif "ข้อความ" in t:
            r, rounds = n[0], n[2]
            assert _value(ans) == sum(r ** i for i in range(1, rounds + 1))
        else:
            a, months = n[0], n[1]
            assert _value(ans) == sum(a * 2 ** i for i in range(months))
    elif key == "math.arithmetic_series_word_m6":
        if "เก้าอี้" in t or "นักวิ่ง" in t:
            a, d, total = n[0], n[1], n[2]
            s, k = 0, 0
            while s < total:
                s += a + k * d
                k += 1
            assert s == total and k == int(ans)
        elif "กระป๋อง" in t:
            total = n[-1]
            s, k = 0, 0
            while s < total:
                k += 1
                s += k
            assert s == total and k == int(ans)
        elif "ออม" in t:
            x, d, b = n[0], n[1], n[2]
            day = next(k for k in range(2, 200) if k * (2 * x + (k - 1) * d) == 2 * k * b)
            assert day == int(ans)
        else:
            days, a, d, fixed = n[0], n[1], n[2], n[3]
            s = sum(a + i * d for i in range(days))
            assert _value(ans) == abs(s - days * fixed)
    elif key == "math.optimization_geometry_m6":
        grid = [i / 1000 for i in range(1, 200001)]
        if "สังกะสี" in t:
            s = n[0]
            best = max((x * (s - 2 * x) ** 2, x) for x in grid if x < s / 2)
            target = best[1] if "x ควรเป็น" in t else best[0]
            assert math.isclose(_value(ans), target, rel_tol=1e-4)
        elif "ริมแม่น้ำ" in t:
            L = n[0]
            assert math.isclose(_value(ans), max(x * (L - 2 * x) for x in grid if x < L / 2), rel_tol=1e-4)
        elif "พาราโบลา" in t:
            c = n[0]
            assert math.isclose(_value(ans), max(2 * x * (c - x * x) for x in grid if x * x < c), rel_tol=1e-4)
        elif "xy" in t:
            S = n[0]
            assert math.isclose(_value(ans), max((S - y) * y * y for y in grid if y < S), rel_tol=1e-4)
        else:
            N, k = n[0], n[1]
            best = max(((p * (N - k * p)), p) for p in range(1, N // k))
            assert _value(ans) == best[1]
    elif key == "math.integral_accumulation_m6":
        def integrate(f, a, b, steps=20000):
            h = (b - a) / steps
            return sum(f(a + (i + 0.5) * h) for i in range(steps)) * h

        if "อนุภาค" in t:
            a1, a0, T = n[1], n[2], n[-1]
            v = lambda x: 6 * x * x - a1 * x + a0          # noqa: E731
            assert n[0] == 6
            if "ระยะทาง" in t:
                assert math.isclose(_value(ans), integrate(lambda x: abs(v(x)), 0, T), rel_tol=1e-4)
            else:
                assert math.isclose(_value(ans), integrate(v, 0, T), abs_tol=1e-3)
        elif "เปิดน้ำ" in t:
            v0 = n[0] if "มีน้ำอยู่" in t else 0
            rest = n[1:] if v0 else n
            a, b, T = rest[0], rest[1], rest[2]
            assert math.isclose(_value(ans), v0 + integrate(lambda x: a * x + b, 0, T), rel_tol=1e-6)
        else:
            c, d = (n[0], n[1]) if "รั่ว" in t else (n[1], n[2])     # the brake stem opens with t = 0
            assert math.isclose(_value(ans), integrate(lambda x: c - d * x, 0, c / d), rel_tol=1e-6)


@pytest.mark.parametrize("key", KEYS)
def test_answers_rederived_by_brute_force(key):
    for seed in SEEDS:
        _check(key, generate(key, Random(seed)))
