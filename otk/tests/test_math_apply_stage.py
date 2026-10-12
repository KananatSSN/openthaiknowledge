"""Application-stage sets: every answer re-derived from the question."""

from __future__ import annotations

from otk.tests._origins import keys_from

import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.p1.solids import _OBJECTS
from otk.sets.math.p3.symmetry import _SYMMETRIC
from otk.sets.math.p6.prime_numbers import _is_prime

SEEDS = range(250)
KEYS = sorted(keys_from("math_apply_stage"))


def _choice(c) -> str:
    return " ".join(getattr(b, "text", "") or getattr(b, "tex", "") for b in c.content)


def _stem(q) -> str:
    return " ".join(getattr(b, "text", "") or getattr(b, "tex", "") for b in q.stem)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _ints(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s.replace(",", ""))]


def _num(tex: str) -> Fraction:
    tex = tex.replace("{,}", "")
    m = re.fullmatch(r"\\frac\{(\d+)\}\{(\d+)\}", tex)
    return Fraction(int(m.group(1)), int(m.group(2))) if m else Fraction(tex)


def _surd(tex: str) -> float:
    m = re.fullmatch(r"(\d*)\\sqrt\{(\d+)\}", tex)
    return int(m.group(1) or 1) * math.sqrt(int(m.group(2))) if m else float(tex)


def _each(key):
    for seed in SEEDS:
        yield generate(key, Random(seed))


def test_nineteen_sets_are_registered():
    assert len(KEYS) == 19


@pytest.mark.parametrize("key", KEYS)
def test_choices_are_distinct_and_full(key):
    for q in _each(key):
        texts = [_choice(c) for c in q.choices]
        assert len(texts) == len(set(texts)) == REGISTRY[key].max_choices, texts


@pytest.mark.parametrize("key", KEYS)
def test_every_set_is_in_an_application_stage(key):
    assert REGISTRY[key].learning_stage == 3


def test_p1_word_problems():
    for q in _each("math.add_word_p1"):
        a, b = _ints(_stem(q))[:2]
        assert int(_answer(q)) == a + b <= 99
    for q in _each("math.subtract_word_p1"):
        a, b = _ints(_stem(q))[:2]
        assert int(_answer(q)) == a - b > 0


def test_patterns():
    for q in _each("math.pattern_word_p1"):
        s = _stem(q)
        if "ลูกปัด" in s:
            unit = re.search(r"แบบรูปซ้ำ (.+?) \.\.\.", s).group(1).split()
            k = _ints(s)[-1]
            period = next(n for n in range(1, len(unit)) if unit[n:] == unit[:-n])
            assert _answer(q) == unit[(k - 1) % period]
        else:
            n = _ints(s)
            step, k = n[3], n[-1]
            assert int(_answer(q)) == step * k
    for q in _each("math.pattern_word_p2"):
        s = _stem(q)
        n = _ints(s)
        k = n[-1]
        if "ถังมีน้ำ" in s:
            start, t1, t2 = n[0], n[4], n[5]
            step = t1 - t2
            assert int(_answer(q)) == start - step * k
        else:
            t1, t2 = (n[3], n[4]) if "ออมเงิน" in s else (n[0], n[1])
            assert int(_answer(q)) == t1 + (t2 - t1) * (k - 1)
        assert max(n) <= 1000 and int(_answer(q)) <= 1000


def test_solids_and_symmetry():
    solid_of = dict(_OBJECTS)
    for q in _each("math.solid_objects_p1"):
        s = _stem(q)
        m = re.match(r"(.+)มีรูปร่างคล้ายรูปเรขาคณิตสามมิติชนิดใด", s)
        if m:
            assert _answer(q) == solid_of[m.group(1)]
        elif s.startswith("สิ่งของใด"):
            solid = re.search(r"คล้าย(.+)$", s).group(1)
            assert solid_of[_answer(q)] == solid
            assert sum(solid_of.get(_choice(c)) == solid for c in q.choices) == 1
        else:
            listed = re.search(r"ดังนี้: (.+?) สิ่งของที่", s).group(1)
            solid = re.search(r"คล้าย(.+)มีกี่ชิ้น", s).group(1)
            count = sum(solid_of[t] == solid for t in listed.split(" ") if t in solid_of)
            assert int(_answer(q)) == count
    axes = dict(_SYMMETRIC)
    for q in _each("math.symmetry_word_p3"):
        s = _stem(q)
        m = re.match(r"(.+)มีแกนสมมาตรกี่แกน", s)
        if m:
            assert int(_answer(q)) == axes[m.group(1)]
        elif s.startswith("สิ่งใดไม่มี"):
            assert _answer(q) not in axes
            assert all(_choice(c) in axes for c in q.choices if _choice(c) != _answer(q))
        else:
            assert _answer(q) == "แกนสมมาตร"


def test_money():
    for q in _each("math.money_word_p2"):
        s = _stem(q)
        if "ใครมีเงินมากกว่า" in s:
            n = _ints(s)
            mine = 10 * n[1] + 5 * n[3] + n[5]
            theirs = 20 * n[7] + (5 * n[9] if "เหรียญ 5 บาท" in s.split("ธนบัตร")[1] else 0)
            more = re.match(r"(\S+) มากกว่า (\d+) บาท", _answer(q))
            assert int(more.group(2)) == abs(mine - theirs)
            assert more.group(1) == (s.split("มี")[0] if mine > theirs else re.search(r"(\S+)มีธนบัตร", s).group(1))
        elif "ต้องมีเงินเพิ่ม" in s:
            n = _ints(s)
            have = 20 * n[1] + (n[2] if "เหรียญรวมกัน" in s else 0)
            price = n[-1]
            assert int(_answer(q)) == price - have > 0
        else:
            n = _ints(s)
            satang = 50 * n[1] + 25 * n[3]
            got = _ints(_answer(q))
            baht = got[0] if "บาท" in _answer(q) else 0
            left = got[-1] if "สตางค์" in _answer(q) else 0
            assert baht * 100 + left == satang


def test_place_value():
    for key in ("math.place_value_word_p3", "math.place_value_word_p4"):
        for q in _each(key):
            s = _stem(q)
            if "เลขโดด" in s:
                number = int(re.search(r"(\d[\d,]*)", s).group(1).replace(",", ""))
                d = int(re.search(r"เลขโดด (\d)", s).group(1))
                places = ("หน่วย", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน")
                place = places.index(re.search(r"ในหลัก(\S+?)มีค่า", s).group(1))
                assert str(number)[::-1][place] == str(d)
                assert _num(_answer(q)) == d * 10 ** place
            elif "บัตรตัวเลข" in s:
                cards = [int(c) for c in re.search(r"บัตรตัวเลข ([\d, ]+) ใช้", s).group(1).split(", ")]
                got = str(int(_num(_answer(q))))
                assert sorted(got) == sorted(map(str, cards)) and got[0] != "0"
                best = "".join(sorted(map(str, cards), reverse=True))
                if "มากที่สุด" in s:
                    assert got == best
                else:
                    assert all(int(got) <= int("".join(p)) for p in _perms(cards) if p[0] != "0")
            else:
                pairs = re.findall(r"(\S+(?: \S)?) ([\d,]+)", s.split("ดังนี้: ")[1])
                values = {nm: int(v.replace(",", "")) for nm, v in pairs}
                pick = max if "มากที่สุด" in s else min
                assert _answer(q) == pick(values, key=values.get)


def _perms(cards):
    from itertools import permutations
    return ("".join(map(str, p)) for p in permutations(cards))


def test_primes_and_factors():
    for q in _each("math.prime_word_p6"):
        s = _stem(q)
        if s.startswith("จัดเก้าอี้"):
            n = _ints(s)[0]
            assert int(_answer(q)) == sum(1 for d in range(2, n) if n % d == 0)
        elif "แบ่งแบบนี้ไม่ได้" in s:
            assert _is_prime(_ints(_answer(q))[0])
            assert sum(_is_prime(_ints(_choice(c))[0]) for c in q.choices) == 1
        else:
            a, b = _ints(s)[:2]
            assert int(_answer(q)) == sum(_is_prime(n) for n in range(a, b + 1))
    for q in _each("math.prime_factor_word_m1"):
        s = _stem(q)
        n = _ints(s)
        if "กระเบื้อง" in s:
            k = int(_answer(q))
            assert math.isqrt(n[0] * k) ** 2 == n[0] * k
            assert not any(math.isqrt(n[0] * j) ** 2 == n[0] * j for j in range(1, k))
        elif "จัดนักเรียน" in s:
            assert int(_answer(q)) == sum(1 for d in range(1, n[0] + 1) if n[0] % d == 0)
        else:
            a, b = n[:2]
            g = math.gcd(a, b)
            assert int(_answer(q)) == a // g + b // g


def test_triangle_areas():
    for q in _each("math.triangle_area_word_p6"):
        s = _stem(q)
        n = _ints(s)
        ans = _num(_answer(q))
        if "สนามหญ้า" in s:
            b, h, price = n
            assert ans == Fraction(b * h, 2) * price
        elif "ธง" in s:
            b, h, flags = n
            assert ans == Fraction(b * h, 2) * flags
        else:
            area, b = n
            assert Fraction(b) * ans / 2 == area


def test_radicals_and_powers():
    for q in _each("math.radical_geometry_m4"):
        s = _stem(q)
        if "เส้นทแยงมุม" in s:
            a, b = _ints(s)[:2]
            assert math.isclose(_surd(_answer(q)), math.hypot(a, b))
            assert sum(math.isclose(_surd(_choice(c)), math.hypot(a, b)) for c in q.choices) == 1
        elif "ความยาวรอบรูป" in s:
            sides = [int(v) for v in re.findall(r"√(\d+)", s)]
            assert math.isclose(_surd(_answer(q)), sum(map(math.sqrt, sides)))
        else:
            a, b = _ints(s)[:2]
            assert int(_answer(q)) == a * a - b
    for q in _each("math.rational_power_context_m5"):
        s = _stem(q)
        if "ลูกบาศก์" in s:
            assert int(_answer(q)) ** 3 == _ints(s)[0]
        elif "แบคทีเรีย" in s:
            total, h = _ints(s)[:2]
            assert int(_answer(q)) ** h == total
        else:
            area = _ints(s)[0]
            assert math.isclose(_surd(_answer(q)) ** 2, area)


def test_interest_plans():
    for q in _each("math.interest_plan_m5"):
        s = _stem(q)
        n = _ints(s)
        ans = int(_num(_answer(q)))
        if "ต้องฝากกี่ปี" in s:
            p, r, target = n[0], n[1], n[2]
            assert p + p * r * ans / 100 == target
        elif "ร้อยละเท่าใดต่อปี" in s:
            p, years, target = n[0], n[1], n[2]
            assert p + p * ans * years / 100 == target
        else:
            price, disc, k, each = n
            assert ans == k * each - price * (100 - disc) // 100


def test_binomial_applications():
    for q in _each("math.binomial_apply_m5"):
        s = _stem(q)
        if "ท็อปปิง" in s:
            n = _ints(s)[0]
            assert int(_answer(q)) == sum(math.comb(n, k) for k in range(n + 1))
        elif "สองหลักสุดท้าย" in s:
            n = _ints(s)[1]
            assert int(_answer(q)) == 11 ** n % 100
        else:
            n = _ints(s)[-1]
            approx = sum(math.comb(n, k) * Fraction(1, 100) ** k for k in range(3))
            assert _num(_answer(q)) == approx


def test_means_and_series():
    for q in _each("math.mean_word_m6"):
        s = _stem(q)
        n = [Fraction(v) for v in re.findall(r"\d+(?:\.\d+)?", s)]
        ans = Fraction(_answer(q))
        if "เข้ามาเพิ่ม" in s:
            k, m, v = n[:3]
            want = (k * m + v) / (k + 1)
        elif "ตัดข้อมูล" in s:
            k, m, v = n[:3]
            want = (k * m - v) / (k - 1)
        else:
            tests, now, _, target = n[0], n[1], n[2], n[4]
            want = target * (tests + 1) - now * tests
            assert want <= 100
        assert abs(ans - want) <= Fraction(1, 200)
    for q in _each("math.infinite_series_word_m6"):
        s = _stem(q)
        n = _ints(s)
        ans = _num(_answer(q))
        if "ลูกบอล" in s:
            h, p, qq = n[0], n[1], n[2]
            r = Fraction(p, qq)
            assert ans == h + 2 * h * r / (1 - r)
        elif "สี่เหลี่ยมจัตุรัส" in s:
            side = n[0]
            assert ans == side * side / (1 - Fraction(1, 2))
        else:
            assert ans == n[0]


def test_expressions_in_context():
    for q in _each("math.expression_word_m1"):
        s = _stem(q)
        if "ความยาวรอบรูป" in s:
            w, ell = q.stem[1].tex, q.stem[3].tex
            for x in (1, 2, 5):
                ev = lambda t: eval(re.sub(r"(\d)x", r"\1*x", t), {"x": x})  # noqa: E731,S307
                assert ev(_answer(q)) == 2 * (ev(w) + ev(ell))
        elif "เงินทอน" in s:
            a, b, note = _ints(s)[:3]
            assert _answer(q) == rf"{note} - {a}x - {b}y"
        else:
            start, per, h = _ints(s)[0], _ints(s)[1], _ints(s)[-1]
            assert int(_answer(q)) == start + per * h
