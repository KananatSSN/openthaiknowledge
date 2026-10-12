"""Harder application sets for the พื้นฐาน track: five situations each, four
distinct choices, and answers re-derived from the numbers in the question by
direct simulation or brute-force search."""

from __future__ import annotations

from otk.tests._origins import keys_from

import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import generate

SEEDS = range(300)
KEYS = keys_from("math_apply_basic")
_SUP = str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789")


def _text(q) -> str:
    return " ".join(b.text for b in q.stem if b.kind == "text")


def _answer(q) -> str:
    return " ".join(getattr(b, "tex", "") for b in q.choices[q.answer].content)


def _nums(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"-?\d+", s.replace("{,}", "").replace(",", ""))]


def _pos(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s.replace("{,}", "").replace(",", ""))]


def _value(tex: str) -> float:
    tex = tex.replace("{,}", "").strip()
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if m:
        return (-1 if m.group(1) else 1) * int(m.group(2)) / int(m.group(3))
    m = re.fullmatch(r"(\d*)\\sqrt\{(\d+)\}", tex)
    if m:
        return int(m.group(1) or 1) * math.sqrt(int(m.group(2)))
    m = re.fullmatch(r"([\d.]+) \\times 10\^\{(-?\d+)\}", tex)
    if m:
        return float(m.group(1)) * 10 ** int(m.group(2))
    m = re.fullmatch(r"(\d+)\\pi", tex)
    if m:
        return int(m.group(1)) * math.pi
    return float(tex)


def _poly_at(tex: str, x: float) -> float:
    expr = tex.replace("^{2}", "**2")
    expr = re.sub(r"(\d)x", r"\1*x", expr)
    return eval(expr, {}, {"x": x})


def test_ten_sets_five_situations_four_choices():
    assert len(KEYS) == 10
    for key in KEYS:
        openings = set()
        for seed in SEEDS:
            q = generate(key, Random(seed))
            choices = [" ".join(getattr(b, "tex", "") for b in c.content) for c in q.choices]
            assert len(set(choices)) == 4 == len(choices), (key, seed, choices)
            openings.add(re.sub(r"[-\d,]+", "#", _text(q))[:18])
        assert len(openings) >= 5, (key, len(openings))


def _check(key: str, q) -> None:
    t, ans = _text(q), _answer(q)
    v = _value(ans) if not re.search(r"x|<|\\times [\d(]|\(", ans) or "10^" in ans else None
    n = _pos(t)
    if key == "math.multiply_multistep_p4":
        if "ลัง" in t:
            assert v == n[0] * n[1] * n[2]
        elif "กล่อง" in t:
            boxes, cost, k, price = n[:4]
            assert v == boxes * k * price - boxes * cost
        elif "หนังสือ" in t:
            book, pages, weeks = n[:3]
            assert v == book - 7 * weeks * pages
        elif "มะม่วง" in t:
            assert v == n[0] * n[1] * n[2] * n[3]
        else:
            students, teachers, adult, child = n[:4]
            assert v == teachers * adult + students * child
    elif key == "math.fraction_remaining_p5":
        if "มีเงิน" in t:
            m, _, a, _, b = n[:5]
            left = Fraction(m) - Fraction(m, a)
            left -= left / b
        elif "เชือก" in t:
            left = Fraction(n[0]) * Fraction(3, 5) / 2
        elif "สูตรขนม" in t:
            people, num, den, target = n[:4]
            left = Fraction(num, den) * target / people
        elif "ถังน้ำ" in t:
            left = Fraction(n[0]) * Fraction(3, 4) * Fraction(1, 3)
        else:
            dist, _, a, _, b = n[:5]
            left = Fraction(dist) * (1 - Fraction(1, a))
            left -= left / b
        assert math.isclose(v, float(left)), (t, ans)
    elif key == "math.order_of_ops_word_p6":
        if "ประโยคสัญลักษณ์" in t:
            a, x, b, y, note = n[:5]
            assert eval(ans.replace(r"\times", "*")) == note - a * x - b * y
            assert "(" in ans
        elif "เงินทอน" in t:
            a, x, b, y, note = n[:5]
            assert v == note - a * x - b * y
        elif "แบ่งให้น้อง" in t:
            total, keep, kids = n[:3]
            assert v * kids + keep == total
        elif "บัตรชม" in t:
            price, adults, kids, disc = n[:4]
            assert v == adults * price + kids * price / 2 - disc
        else:
            s1, s2, target = n[:3]
            assert (s1 + s2 + v) / 3 == target
    elif key == "math.scientific_notation_word_m1":
        vals = [float(m) * 10 ** int(e.translate(_SUP))
                for m, e in re.findall(r"([\d.]+) × 10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)", t)]
        if "แสงจาก" in t:
            truth = vals[0] / vals[1]
        elif "เพิ่มขึ้นเป็น" in t:
            k = int(re.search(r"เป็น 10([⁰¹²³⁴⁵⁶⁷⁸⁹]+) เท่า", t).group(1).translate(_SUP))
            truth = vals[0] * 10 ** k
        else:
            truth = vals[0] * vals[1]
        assert math.isclose(v, truth, rel_tol=1e-9), (t, ans)
        mant = float(ans.split(" ")[0])
        assert 1 <= mant < 10
    elif key == "math.signed_number_context_m1":
        s = _nums(t)
        if "ตอนเช้า" in t:
            start, up, down = s[0], s[1], s[2]
            assert v == start + up - down
        elif "ยอดเขา" in t:
            assert v == s[0] - s[1]
        elif "บัญชี" in t:
            bal, w1, dep, w2 = _pos(t)[:4]
            assert v == bal - w1 + dep - w2
        elif "ระดับน้ำ" in t:
            start, num, den, days = _pos(t)[:4]
            assert math.isclose(v, start - Fraction(num, den) * days)
        elif "5 วัน" in t:
            temps = s[1:6]
            assert v == sum(temps) / 5
        else:
            raise AssertionError(t)
    elif key == "math.sqrt_measure_context_m2":
        if "จอภาพ" in t:
            assert math.isclose(v, math.hypot(n[0], n[1]))
        elif "ล้อมรั้ว" in t:
            assert math.isclose(v, 4 * math.sqrt(n[0]))
        elif "บันได" in t:
            assert math.isclose(v, math.sqrt(n[0] ** 2 - n[1] ** 2))
        elif "ตัดเฉียง" in t:
            assert math.isclose(v, n[0] * math.sqrt(2))
        else:
            lo, _, hi = map(int, re.findall(r"\d+", ans))
            assert lo < math.sqrt(n[0]) < hi == lo + 1
    elif key == "math.polynomial_area_m2":
        for x in (2, 3, 7):
            if "ยาว" in t and "กว้าง x +" in t:
                a, b, c = n[:3]
                truth = (a * x + b) * (x + c)
            elif "กรอบรูป" in t:
                w = n[0]
                truth = (x + 2 * w) ** 2 - x * x
            elif "ทางเดิน" in t:
                k = n[0]
                truth = (x + 2) * (x + k + 2) - x * (x + k)
            elif "กล่อง" in t:
                h, xv = n[1], n[-1]
                assert v == h * xv * (xv + 1)
                break
            else:
                big, small = n[0], n[1]
                truth = (x + big) ** 2 - small ** 2
            assert _poly_at(ans, x) == truth, (t, ans)
    elif key == "math.vertex_context_m3":
        grid = [i / 100 for i in range(0, 20001)]
        if "ลูกบอล" in t:
            b, c = n[1], n[2]
            best = max((-5 * x * x + b * x + c, x) for x in grid)
            assert math.isclose(v, best[1] if "เมื่อเวลา" in t.split("ลูกบอลขึ้น")[-1] else best[0], abs_tol=1e-6)
        elif "กำไร" in t:
            b, c = n[0], n[1]
            assert math.isclose(v, max(-x * x + b * x - c for x in grid))
        elif "ลวด" in t:
            wire = n[0]
            assert math.isclose(v, max(x * (wire / 2 - x) for x in grid if x < wire / 2))
        elif "ต้นทุน" in t:
            b, c = n[0], n[1]
            assert math.isclose(v, min(x * x - b * x + c for x in grid))
        else:
            m = re.search(r"y = -x² \+ (\d+)x(?: ([+-]) (\d+))?", t)
            b = int(m.group(1))
            c = 0 if not m.group(2) else int(m.group(3)) * (1 if m.group(2) == "+" else -1)
            assert math.isclose(v, max(-x * x + b * x + c for x in grid)), (t, ans)
    elif key == "math.linear_model_compare_m2":
        if "โปรโมชัน" in t:
            fa, ra, fb, rb = n[:4]
            assert fa + ra * v == fb + rb * v
        elif "แท็กซี่" in t:
            start, per, fare = n[0], n[1], n[2]
            assert start + per * (v - 1) == fare
        elif "เทียน" in t:
            h0, rate, left = n[:3]
            assert h0 - rate * v == left
        elif "ฟิตเนส" in t:
            fee, member, walk = n[:3]
            first = next(k for k in range(1, 1000) if fee + member * k < walk * k)
            assert v == first
        else:
            a0, a_in, b0, b_out = n[:4]
            assert a0 + a_in * v == b0 - b_out * v
    elif key == "math.composite_context_m4":
        if "ดอลลาร์" in t:
            rate, fee, usd = n[0], n[1], n[-1]
            assert v == rate * usd - fee
        elif "คูปอง" in t:
            coupon, pct = n[0], n[1]
            price = 4 * coupon
            assert math.isclose(v, abs((price - coupon) * (1 - pct / 100) - (price * (1 - pct / 100) - coupon)))
        elif "วงคลื่น" in t:
            speed, sec = n[0], n[-1]
            assert math.isclose(v, math.pi * (speed * sec) ** 2)
        elif "โวลต์" in t:
            volts = n[-1]
            assert v == (5 * volts + 10) * 9 / 5 + 32
        else:
            a, b, x = n[:3]
            assert v == (a * x + b) ** 2


@pytest.mark.parametrize("key", KEYS)
def test_answers_rederived_from_the_question(key):
    for seed in SEEDS:
        _check(key, generate(key, Random(seed)))
