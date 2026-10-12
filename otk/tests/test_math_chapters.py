"""Chapters that had no set (math_chapters): answers re-derived from what the
learner is shown, and every named mistake checked to be wrong."""

from __future__ import annotations

from otk.tests._origins import keys_from

import cmath
import math
import re
from decimal import Decimal
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.p2.money import _COINS, _NOTES, _SATANG
from otk.sets.math.m2.geometric_reasoning import _CONVERSES
from otk.sets.math.p2.shapes import _POLY, _SOLIDS

SEEDS = range(300)
KEYS = keys_from("math_chapters")
_NAMED = {name: v for v, name in (_COINS | _NOTES).items()}
_NAMED |= {name: Fraction(v, 100) for v, name in _SATANG.items()}


def _b(block) -> str:
    return getattr(block, "text", None) or getattr(block, "tex", "") or ""


def _stem(q) -> str:
    return " ".join(_b(b) for b in q.stem)


def _choices(q) -> list[str]:
    return [" ".join(_b(b) for b in c.content) for c in q.choices]


def _answer(q) -> str:
    return _choices(q)[q.answer]


def _wrongs(q) -> list[str]:
    return [c for i, c in enumerate(_choices(q)) if i != q.answer]


def _each(key):
    for seed in SEEDS:
        yield seed, generate(key, Random(seed))


def _n(s: str) -> Fraction:
    return Fraction(s.replace("{,}", "").replace(",", ""))


def test_module_size():
    assert len(KEYS) == 23


@pytest.mark.parametrize("key", KEYS)
def test_four_distinct_choices(key):
    for seed, q in _each(key):
        assert len(q.choices) == REGISTRY[key].max_choices and len(set(_choices(q))) == REGISTRY[key].max_choices, (key, seed, _stem(q))


# ── A small TeX evaluator for the answers these sets print ──────────────────

def _group(s: str, i: int) -> tuple[str, int]:
    """The brace group starting at s[i] == '{' and the index after it."""
    depth = 0
    for j in range(i, len(s)):
        depth += {"{": 1, "}": -1}.get(s[j], 0)
        if depth == 0:
            return s[i + 1:j], j + 1
    raise ValueError(s)


def _py(tex: str) -> str:
    out, i = "", 0
    while i < len(tex):
        if tex.startswith(r"\frac", i):
            a, i = _group(tex, i + 5)
            b, i = _group(tex, i)
            out += f"(({_py(a)})/({_py(b)}))"
        elif tex.startswith(r"\sqrt", i):
            a, i = _group(tex, i + 5)
            out += f"sqrt({_py(a)})"
        elif tex[i] == "^":
            a, i = _group(tex, i + 1)
            out += f"**({_py(a)})"
        else:
            out += tex[i]
            i += 1
    # Implicit products: 3x, 2sqrt, )(, x(.
    out = re.sub(r"(\d|\))\s*(x|sqrt|\()", r"\1*\2", out)
    return out


def _val(tex: str, x=None):
    return eval(_py(tex), {"sqrt": math.sqrt, "x": x})


# ── เงิน ────────────────────────────────────────────────────────────────────

def _amounts(stem: str) -> list[Fraction]:
    """Each person's money, in the order the stem names them."""
    names = "|".join(sorted(map(re.escape, _NAMED), key=len, reverse=True))
    people, total = [], Fraction(0)
    for m in re.finditer(rf"({names}) (\d+) (?:เหรียญ|ฉบับ)|(มี)", stem):
        if m.group(3):
            if total:
                people.append(total)
            total = Fraction(0)
        else:
            total += _NAMED[m.group(1)] * int(m.group(2))
    return people + [total]


def test_money_count():
    for seed, q in _each("math.money_count_p2"):
        people = [p for p in _amounts(_stem(q)) if p]
        want = people[0] if len(people) == 1 else abs(people[0] - people[1])
        assert _n(_answer(q)) == want, (seed, _stem(q))


def test_money_exchange():
    names = "|".join(sorted(map(re.escape, _NAMED), key=len, reverse=True))
    for seed, q in _each("math.money_exchange_p2"):
        s, ans = _stem(q), _n(_answer(q))
        given = (int(re.match(r"นำเงิน (\d+)", s).group(1)) if s.startswith("นำเงิน")
                 else _amounts(s)[-1])
        if s.endswith("กี่บาท"):
            assert ans == given, s
        else:
            target = re.search(rf"แลกเป็น({names})", s).group(1)
            assert ans * _NAMED[target] == given, s


def test_baht_satang():
    for seed, q in _each("math.baht_satang_p2"):
        total = _amounts(_stem(q))[-1] * 100
        b, s = divmod(int(total), 100)
        m = re.fullmatch(r"(?:(\d+) บาท)? ?(?:(\d+) สตางค์)?", _answer(q))
        assert (int(m.group(1) or 0), int(m.group(2) or 0)) == (b, s), (seed, _stem(q))


# ── รูปเรขาคณิต ──────────────────────────────────────────────────────────────

_SIDES = dict(_POLY)


def test_shape_properties():
    for seed, q in _each("math.shape_properties_p2"):
        s, a = _stem(q), _answer(q)
        if s.startswith("รูปที่มี"):
            assert _SIDES[a] == int(re.search(r"\d+", s).group())
        elif s.startswith("รูปใดไม่มี"):
            assert a in ("วงกลม", "วงรี") and not any(w in ("วงกลม", "วงรี") for w in _wrongs(q))
        else:
            name = next(n for n in _SIDES if s.startswith(n))
            assert int(a.split()[0]) == _SIDES[name]


def test_solid_shapes():
    for seed, q in _each("math.solid_shapes_p2"):
        s, a = _stem(q), _answer(q)
        if "ลากเส้น" in s:
            assert any(o in s for o in _SOLIDS_BY_TRACE[a])
        else:
            objects, described, _ = _SOLIDS[a]
            assert described in s or any(s.startswith(o) for o in objects)


_SOLIDS_BY_TRACE: dict[str, list[str]] = {}
for _solid, (_objs, _, _trace) in _SOLIDS.items():
    if _trace:
        _SOLIDS_BY_TRACE.setdefault(_trace, []).extend(_objs)


def test_shape_count():
    for seed, q in _each("math.shape_count_p2"):
        s = _stem(q)
        parts = re.findall(r"(รูป\S+?เหลี่ยม) (\d+) รูป", s)
        want = sum(_SIDES[n] * int(c) for n, c in parts)
        assert _n(_answer(q)) == want, s


# ── การให้เหตุผลทางเรขาคณิต ───────────────────────────────────────────────────

def _deg(s: str) -> int:
    return int(re.match(r"(\d+)\^\{\\circ\}", s).group(1))


def test_isosceles_triangle():
    for seed, q in _each("math.isosceles_triangle_angle_m2"):
        s = _stem(q)
        given = int(re.search(r"= (\d+)°", s).group(1))
        a = _deg(_answer(q))
        if "∠ACD" in s:
            assert a == 180 - 2 * (180 - given)
        elif "∠A =" in s:
            assert 2 * a + given == 180
        else:
            assert a + 2 * given == 180


def test_exterior_angle():
    for seed, q in _each("math.exterior_angle_m2"):
        s = _stem(q)
        if "x" in s:
            p = int(re.search(r"∠A = \(2x \+ (\d+)\)", s).group(1))
            qq = int(re.search(r"∠B = \(x \+ (\d+)\)", s).group(1))
            ext = int(re.search(r"∠ACD = (\d+)", s).group(1))
            x = int(_answer(q))
            assert 2 * x + p + x + qq == ext
            continue
        angles = dict(re.findall(r"∠(ACD|A|B) = (\d+)°", s))
        a = _deg(_answer(q))
        if "ACD" in angles:
            assert int(angles["ACD"]) == int(angles["A"]) + a
        else:
            assert a == int(angles["A"]) + int(angles["B"])


def test_converse_bank_reverses_each_statement():
    for stmt, conv, _ in _CONVERSES:
        assert stmt.startswith("ถ้า") and conv.startswith("ถ้า") and stmt != conv
    assert sum(t for *_, t in _CONVERSES) >= 4 and sum(not t for *_, t in _CONVERSES) >= 4


def test_converse_statement():
    truth = {s: t for s, _, t in _CONVERSES}
    for seed, q in _each("math.converse_statement_m2"):
        s = _stem(q)
        if s.startswith("บทกลับ"):
            stmt = s.split("\n", 1)[1]
            assert _answer(q) == next(c for st, c, _ in _CONVERSES if st == stmt)
        else:
            want = "ไม่เป็นจริง" not in s
            assert truth[_answer(q)] is want and all(truth[w] is not want for w in _wrongs(q))


# ── ฟังก์ชัน ─────────────────────────────────────────────────────────────────

_XS = (-2.5, 0.5, 3.25, 7.0)


def test_inverse_function_formula():
    for seed, q in _each("math.inverse_function_formula_m4"):
        f = q.stem[1].tex.removeprefix("f(x) = ")

        def undoes(choice: str) -> bool:
            g = choice.removeprefix("f^{-1}(x) = ")
            try:
                return all(abs(_val(f, _val(g, x)) - x) < 1e-9 for x in _XS)
            except ZeroDivisionError:
                return False
        assert undoes(_answer(q)), (seed, f, _answer(q))
        assert not any(undoes(w) for w in _wrongs(q)), (seed, f)


def test_inverse_function_value():
    for seed, q in _each("math.inverse_function_value_m4"):
        texts = [_b(b) for b in q.stem]
        if texts[0].startswith("f = "):
            pairs = [tuple(map(int, p)) for p in re.findall(r"\((-?\d+), (-?\d+)\)", texts[0])]
            y = int(re.search(r"\((-?\d+)\)", texts[-1]).group(1))
            assert (int(_answer(q)), y) in pairs
        elif texts[0] == "กำหนดให้":
            f = texts[1].removeprefix("f(x) = ")
            c = int(re.search(r"\((-?\d+)\)", texts[3]).group(1))
            assert _val(f, int(_answer(q))) == c
        else:
            xs = (-3, -1, 0, 1, 2, 3, 4)

            def one_to_one(eq: str) -> bool:
                body = eq.removeprefix("y = ").replace("|x|", "abs(x)")
                if r"\log" in body or r"\sqrt" in body:     # increasing on x > 0
                    return True
                vals = [_val(body, x) for x in xs]
                return len(set(vals)) == len(vals)
            want = "ไม่เป็น" not in texts[0]
            assert one_to_one(_answer(q)) is want and all(one_to_one(w) is not want for w in _wrongs(q))


def _hk(eq: str) -> tuple[int, int]:
    """y = f(x − h) + k as printed -> (h, k)."""
    m = re.search(r"x ([+-]) (\d+)\S* ([+-]) (\d+)$", eq)
    return (int(m.group(2)) * (1 if m.group(1) == "-" else -1),
            int(m.group(4)) * (1 if m.group(3) == "+" else -1))


def _moved(h: int, k: int) -> str:
    return (f"ไปทาง{'ขวา' if h > 0 else 'ซ้าย'} {abs(h)} หน่วย "
            f"และเลื่อน{'ขึ้น' if k > 0 else 'ลง'} {abs(k)} หน่วย")


def test_graph_shift():
    for seed, q in _each("math.graph_shift_m4"):
        texts = [_b(b) for b in q.stem]
        a = _answer(q)
        if texts[0] == "เลื่อนกราฟของ":
            assert texts[2] == _moved(*_hk(a)) + " จะได้กราฟของฟังก์ชันใด"
            assert not any(texts[2].startswith(_moved(*_hk(w))) for w in _wrongs(q))
            continue
        h, k = _hk(texts[1])
        if a.startswith("("):
            assert a == f"({h}, {k})"
        else:
            assert a == "เลื่อน" + _moved(h, k)


def test_exp_log_graph():
    for seed, q in _each("math.exp_log_graph_m4"):
        texts = [_b(b) for b in q.stem]
        a = _answer(q)
        if "ตัดแกน Y" in texts[-1] or "เส้นกำกับ" in texts[0]:
            eq = texts[1].removeprefix("y = ")
            if "ตัดแกน Y" in texts[-1]:
                assert a == f"(0, {round(_val(eq, 0))})"
            else:
                far = _val(eq, -60)
                assert a == f"y = {round(far)}"
        elif texts[0].startswith("ฟังก์ชันใดเป็น"):
            def falls(eq: str) -> bool:
                return any(b in eq for b in (r"\frac{1}{2}", r"\frac{2}{3}", "0.4", "0.1"))
            want = "ลด" in texts[0]
            assert falls(a) is want and all(falls(w) is not want for w in _wrongs(q))
        elif texts[0].startswith("โดเมน"):
            h = -int(re.search(r"x ([+-] \d+)", texts[1]).group(1).replace(" ", ""))
            assert a == rf"({h}, \infty)"
        else:
            base = re.search(r"\\log_\{(\d+)\}", texts[1])
            b = int(base.group(1)) if base else 10
            x, y = map(int, re.findall(r"\d+", a))
            assert b ** y == x
            for w in _wrongs(q):
                wx, wy = map(int, re.findall(r"\d+", w))
                assert b ** wy != wx


# ── กฎของไซน์ ────────────────────────────────────────────────────────────────

def _sin(d: int) -> float:
    return math.sin(math.radians(d))


def test_sine_rule_side():
    for seed, q in _each("math.sine_rule_side_m5"):
        A, B, a = map(int, re.findall(r"= (\d+)", _stem(q)))
        want = a * _sin(B) / _sin(A)
        assert math.isclose(_val(_answer(q)), want), (seed, _stem(q))
        assert not any(math.isclose(_val(w), want) for w in _wrongs(q))


def test_sine_rule_angle():
    for seed, q in _each("math.sine_rule_angle_m5"):
        cond = q.stem[1].tex
        A = int(re.search(r"\\angle A = (\d+)", cond).group(1))
        a = int(re.search(r"a = (\d+)", cond).group(1))
        b = _val(re.search(r"b = (.+)$", cond).group(1))
        B = _deg(_answer(q))
        assert math.isclose(a / _sin(A), b / _sin(B)) and A + B < 180
        which = _stem(q)
        assert ("แหลม" in which) == (B < 90) and ("ป้าน" in which) == (B > 90)
        for w in _wrongs(q):
            wb = _deg(w)
            same_kind = (wb < 90) == (B < 90) and (wb > 90) == (B > 90)
            assert not (math.isclose(_sin(wb), _sin(B)) and same_kind and A + wb < 180)


def test_triangle_area_sine():
    for seed, q in _each("math.triangle_area_sine_m5"):
        a, b, C = map(int, re.findall(r"= (\d+)", _stem(q)))
        want = a * b * _sin(C) / 2
        assert math.isclose(_val(_answer(q)), want)
        assert not any(math.isclose(_val(w), want) for w in _wrongs(q))


# ── เวกเตอร์ และจำนวนเชิงซ้อน ──────────────────────────────────────────────────

def _vecs(tex: str) -> list[list[int]]:
    return [list(map(int, re.findall(r"-?\d+", m)))
            for m in re.findall(r"\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}", tex)]


def test_vector_cross_product():
    for seed, q in _each("math.vector_cross_product_m5"):
        u, v = _vecs(q.stem[1].tex)
        c = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
        if "พื้นที่" in _stem(q):
            want = math.sqrt(sum(x * x for x in c)) / (2 if "สามเหลี่ยม" in _stem(q) else 1)
            assert math.isclose(_val(_answer(q)), want)
            assert not any(math.isclose(_val(w), want) for w in _wrongs(q))
        else:
            assert _vecs(_answer(q)) == [c]


def _polar(tex: str) -> complex:
    m = re.fullmatch(r"(\d*)\(?\\cos (\d+)\^\{\\circ\} \+ i\\sin \d+\^\{\\circ\}\)?", tex)
    return int(m.group(1) or 1) * cmath.exp(1j * math.radians(int(m.group(2))))


def _complex(tex: str) -> complex:
    if r"\cos" in tex:
        return _polar(tex)
    sign = -1 if tex.startswith("-") else 1
    body = tex.lstrip("-")
    if body.endswith("i"):
        return sign * 1j * int(body[:-1] or 1)
    return sign * int(body)


def test_complex_nth_roots():
    for seed, q in _each("math.complex_nth_roots_m5"):
        s = _stem(q)
        n = int(re.search(r"รากที่ (\d+)", s).group(1))
        w = _complex(q.stem[1].tex)
        a = _answer(q)
        if "ค่าสัมบูรณ์" in s:
            assert math.isclose(float(_n(a)) ** n, abs(w))
        elif "ทำมุม" in s:
            assert _deg(a) == 360 // n
        else:
            assert cmath.isclose(_polar(a) ** n, w, abs_tol=1e-9)
            assert not any(cmath.isclose(_polar(x) ** n, w, abs_tol=1e-9) for x in _wrongs(q))


# ── มูลค่าปัจจุบันและค่างวด ─────────────────────────────────────────────────────

def _factor(q) -> tuple[Decimal, int, Decimal]:
    m = re.fullmatch(r"\((\d\.\d+)\)\^\{(\d+)\} = ([\d.]+)", q.stem[1].tex)
    return Decimal(m.group(1)) - 1, int(m.group(2)), Decimal(m.group(3))


def test_present_value():
    for seed, q in _each("math.present_value_m5"):
        rate, n, g = _factor(q)
        assert (1 + rate) ** n == g
        later = Decimal(re.search(r"(?:มีเงิน|จ่ายเงิน) ([\d,.]+) บาท", _stem(q)).group(1).replace(",", ""))
        now = Decimal(_answer(q).replace("{,}", ""))
        assert (now * g).quantize(Decimal("0.01")) == later


def test_loan_instalment():
    for seed, q in _each("math.loan_instalment_m5"):
        rate, n, g = _factor(q)
        loan = Decimal(re.search(r"กู้เงิน ([\d,]+) บาท", _stem(q)).group(1).replace(",", ""))
        pay = Decimal(_answer(q).replace("{,}", ""))
        # The payments, discounted back to today, repay the loan.
        owed = loan
        for _ in range(n):
            owed = owed * (1 + rate) - pay
        assert abs(owed) < n, (seed, owed)


# ── การนำเสนอข้อมูลเชิงปริมาณ ─────────────────────────────────────────────────

def _table(q):
    rows = [tuple(map(int, r)) for r in re.findall(r"(\d+) – (\d+) \| (\d+)", _b(q.stem[0]))]
    return rows, sum(f for *_, f in rows)


def test_class_boundaries():
    for seed, q in _each("math.class_boundaries_m6"):
        ask = _b(q.stem[1])
        lo, hi = map(int, re.search(r"(\d+) – (\d+)", ask).groups())
        want = {"จุดกึ่งกลางชั้น": Fraction(lo + hi, 2), "ขอบล่าง": lo - Fraction(1, 2),
                "ขอบบน": hi + Fraction(1, 2)}[ask.split("ของ")[0]]
        assert _n(_answer(q)) == want


def test_relative_frequency():
    for seed, q in _each("math.relative_frequency_m6"):
        rows, total = _table(q)
        ask = _b(q.stem[1])
        lo = int(re.search(r"(\d+) –", ask).group(1))
        f = next(f for a, _, f in rows if a == lo)
        want = Fraction(f, total) * (100 if "ร้อยละ" in ask else 1)
        assert _n(_answer(q)) == want


def test_cumulative_frequency():
    for seed, q in _each("math.cumulative_frequency_m6"):
        rows, total = _table(q)
        ask = _b(q.stem[1])
        if "ความถี่สะสมของ" in ask:
            hi = int(re.search(r"– (\d+)", ask).group(1))
            want = Fraction(sum(f for _, b, f in rows if b <= hi))
        else:
            cut = Fraction(re.search(r"(\d+\.5)", ask).group(1))
            below = sum(f for _, b, f in rows if b < cut)
            want = Fraction(total - below) if "มากกว่า" in ask else Fraction(100 * below, total)
        assert _n(_answer(q)) == want
