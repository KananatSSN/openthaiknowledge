"""Gap sets found by the indicator-by-indicator check: every answer re-derived
from the question."""

from __future__ import annotations

from otk.tests._origins import keys_from

import math
import re
from collections import Counter
from decimal import Decimal
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate

SEEDS = range(250)
KEYS = sorted(keys_from("math_gaps_indicators"))


def _choice(c) -> str:
    return " ".join(getattr(b, "text", "") or getattr(b, "tex", "") for b in c.content)


def _stem(q) -> str:
    return " ".join(getattr(b, "text", "") or getattr(b, "tex", "") for b in q.stem)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _decs(s: str) -> list[Decimal]:
    return [Decimal(n) for n in re.findall(r"\d+(?:\.\d+)?", s.replace(",", ""))]


def test_thirteen_sets_are_registered():
    assert len(KEYS) == 13


@pytest.mark.parametrize("key", KEYS)
def test_choices_are_distinct_and_full(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        texts = [_choice(c) for c in q.choices]
        assert len(texts) == len(set(texts)) == REGISTRY[key].max_choices, (seed, texts)


def test_decimal_word_problems():
    for seed in SEEDS:
        q = generate("math.decimal_two_step_word_p4", Random(seed))
        s, ans = _stem(q), Decimal(_answer(q))
        n = _decs(s)
        if "เงินทอน" in s:
            assert ans == n[2] - n[0] - n[1], s
        elif "น้ำตาล" in s:
            assert ans == n[0] + n[1] - n[2], s
        else:
            assert ans == n[0] - n[1] - n[2], s
        assert ans > 0

        q = generate("math.decimal_three_step_word_p6", Random(seed))
        s, ans = _stem(q), Decimal(_answer(q))
        n = _decs(s)
        if "สมุด" in s:
            books, p, pens, r, paid = n
            assert ans == paid - books * p - pens * r, s
        elif "ผ้า" in s:
            total, a, pieces, parts = n
            assert ans == (total - pieces * a) / parts, s
        else:
            k, trays, p, d = n
            assert ans == (trays * p - d) / k, s
        assert ans > 0


def test_dividing_by_a_decimal():
    for seed in SEEDS:
        q = generate("math.divide_decimal_by_decimal_p6", Random(seed))
        a, b = q.stem[-1].tex.split(r" \div ")
        assert Decimal(_answer(q)) == Decimal(a) / Decimal(b)
        assert len(a.partition(".")[2]) <= 3 and len(_answer(q).partition(".")[2]) <= 3


def test_writing_ratios():
    for seed in SEEDS:
        q = generate("math.write_ratio_p6", Random(seed))
        s = _stem(q)
        (x, a), (y, b) = re.findall(r"(?:มี|และ)(\S+) (\d+) ", s)[:2]
        a, b = int(a), int(b)
        value = {x: a, y: b}
        first, second = re.search(r"อัตราส่วนของจำนวน(\S+?)ต่อจำนวน(\S+?)เขียน", s).groups()
        want = [value.get(first, a + b), value.get(second, a + b)]
        assert _answer(q) == f"{want[0]} : {want[1]}", s
        # No other choice is the same ratio.
        for c in q.choices:
            p, r = map(int, _choice(c).split(" : "))
            if _choice(c) != _answer(q):
                assert p * want[1] != r * want[0], (s, _choice(c))


def test_gcd_and_lcm_of_three():
    for seed in SEEDS:
        q = generate("math.gcd_lcm_three_p6", Random(seed))
        s = _stem(q)
        nums = [int(n) for n in re.findall(r"\d+", s)[:3]]
        lcm = "ค.ร.น." in s or "กะพริบ" in s
        want = math.lcm(*nums) if lcm else math.gcd(*nums)
        assert int(_answer(q)) == want, s


def test_writing_a_one_way_table():
    for seed in SEEDS:
        q = generate("math.tally_to_table_p3", Random(seed))
        s = _stem(q)
        listed = re.search(r"ได้คำตอบดังนี้: (.+?) (?:ถ้าเขียน|ตารางทางเดียวในข้อใด)", s).group(1).split()
        counts = Counter(listed)
        assert int(re.search(r"ถามนักเรียน (\d+) คน", s).group(1)) == len(listed)
        m = re.search(r"ที่ตอบ(\S+)ต้องเป็น", s)
        if m:
            assert int(_answer(q)) == counts[m.group(1)]
        else:
            got = dict(re.findall(r"(\S+) (\d+)", _answer(q)))
            assert {k: int(v) for k, v in got.items()} == dict(counts)


def test_naming_angles():
    for seed in SEEDS:
        q = generate("math.name_angle_p4", Random(seed))
        s, ans = _stem(q), _answer(q)
        m = re.search(r"มีจุด (\w) เป็นจุดยอด และมี (\w\w) กับ (\w\w)", s)
        if m:
            v, arm1, arm2 = m.groups()
            assert ans == f"∠{arm1[1]}{v}{arm2[1]}"
            continue
        a, v, c = re.search(r"∠(\w)(\w)(\w)", s).groups()
        assert ans == (f"จุด {v}" if "จุดยอด" in s else f"{v}{a} และ {v}{c}")


def test_the_next_protractor_step_is_the_real_next_step():
    spec = REGISTRY["math.construct_angle_protractor_p4"]
    for seed in SEEDS:
        q = generate("math.construct_angle_protractor_p4", Random(seed))
        goal, steps, faulty = spec.procedures(Random(seed))
        shown = re.search(r"“(.+)”", _stem(q)).group(1)
        assert _answer(q) == steps[steps.index(shown) + 1]
        assert not set(faulty) & set(steps)


def _poly(tex: str):
    """A TeX polynomial or product of factors as a Python function of x."""
    t = tex.replace(" ", "")
    t = re.sub(r"\^\{(\d+)\}", r"**\1", t)
    t = re.sub(r"(?<=[\dx)])(?=[x(])", "*", t)
    return lambda x: eval(t, {"x": x})  # noqa: S307 - test-only, generated input


def _frac(tex: str) -> Fraction:
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if m:
        return Fraction(int(m.group(2)), int(m.group(3))) * (-1 if m.group(1) else 1)
    return Fraction(int(tex))


def test_function_arithmetic():
    for seed in SEEDS:
        q = generate("math.function_arithmetic_m4", Random(seed))
        f = _poly(q.stem[1].tex.removeprefix("f(x) = "))
        g = _poly(q.stem[3].tex.removeprefix("g(x) = "))
        name = q.stem[5].tex
        k = int(re.search(r"\((-?\d+)\)$", name).group(1))
        fk, gk = Fraction(f(k)), Fraction(g(k))
        want = (fk + gk if "+" in name else fk - gk if "(f - g)" in name
                else fk * gk if r"\cdot" in name else fk / gk)
        assert _frac(_answer(q)) == want, name


def test_polynomial_equations():
    for seed in SEEDS:
        q = generate("math.polynomial_equation_m4", Random(seed))
        f = _poly(q.stem[-1].tex.removesuffix(" = 0"))
        roots = [int(n) for n in re.findall(r"-?\d+", _answer(q))]
        assert all(f(r) == 0 for r in roots)
        degree = 4 if "x^{4}" in q.stem[-1].tex else 3
        assert len(set(roots)) == degree


def _in(interval: str, x: Fraction) -> bool:
    for part in interval.split(r" \cup "):
        lb, lo, hi, rb = re.fullmatch(r"([\[(])(.+), (.+)([\])])", part.strip()).groups()
        lo_ok = lo == r"-\infty" or (x >= int(lo) if lb == "[" else x > int(lo))
        hi_ok = hi == r"\infty" or (x <= int(hi) if rb == "]" else x < int(hi))
        if lo_ok and hi_ok:
            return True
    return False


def test_polynomial_inequalities():
    for seed in SEEDS:
        q = generate("math.polynomial_inequality_m4", Random(seed))
        factors, op = re.fullmatch(r"(.+) (>|<|\\geq|\\leq) 0", q.stem[-1].tex).groups()
        f = _poly(factors)
        test = {">": lambda v: v > 0, "<": lambda v: v < 0,
                r"\geq": lambda v: v >= 0, r"\leq": lambda v: v <= 0}[op]
        for x in [Fraction(n, 2) for n in range(-20, 21)]:
            assert _in(_answer(q), x) == test(f(x)), (q.stem[-1].tex, _answer(q), x)


def _matrix(tex: str) -> list[list[int]]:
    body = re.search(r"\\begin\{pmatrix\} (.+) \\end\{pmatrix\}", tex).group(1)
    return [[int(v) for v in row.split(" & ")] for row in body.split(r" \\ ")]


def test_transpose():
    for seed in SEEDS:
        q = generate("math.matrix_transpose_m5", Random(seed))
        m = _matrix(q.stem[1].tex)
        assert _matrix(_answer(q)) == [list(col) for col in zip(*m)]


def test_row_operations():
    for seed in SEEDS:
        q = generate("math.matrix_row_operations_m5", Random(seed))
        aug = _matrix(q.stem[1].tex)
        if len(q.stem) > 3:
            op = q.stem[3].tex
            sign, k = re.search(r"R_\{2\} ([+-]) (\d*)R_\{1\}", op).groups()
            k = int(k or 1) * (1 if sign == "+" else -1)
            want = [b + k * a for a, b in zip(*aug)]
            assert _matrix(_answer(q))[0] == want
        else:
            (a1, b1, c1), (_, e, f) = aug
            y = Fraction(f, e)
            assert int(_answer(q)) == (c1 - b1 * y) / a1
