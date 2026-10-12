"""Secondary gap sets: every answer re-derived from the question.

Factorisations are checked by evaluating both sides at several x and by
checking the answer is the only complete factorisation offered; counts and
probabilities by brute force; interval answers by testing points.
"""

from __future__ import annotations

from otk.tests._origins import keys_from

import itertools
import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m5.function import _MODELS

SEEDS = range(250)
KEYS = sorted(keys_from("math_gaps_secondary"))
XS = (-3, -1, 2, 5, 7)


def _choice(c) -> str:
    return " ".join(getattr(b, "text", "") or getattr(b, "tex", "") for b in c.content)


def _stem(q) -> str:
    return " ".join(getattr(b, "text", "") or getattr(b, "tex", "") for b in q.stem)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _ints(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s.replace(",", ""))]


def _number(tex: str) -> float:
    return float(tex.replace("{,}", "").replace(",", ""))


def _frac(tex: str) -> Fraction:
    tex = tex.strip()
    m = re.fullmatch(r"(\d*)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if m:
        return int(m.group(1) or 0) + Fraction(int(m.group(2)), int(m.group(3)))
    return Fraction(int(tex))


def _poly(tex: str):
    """A TeX polynomial or product of factors as a Python function of x."""
    s = tex.replace(" ", "").replace("−", "-").replace("²", "^{2}").replace("³", "^{3}")
    s = re.sub(r"\^\{(\d+)\}", r"**\1", s)
    s = re.sub(r"(?<=[\dx)])(?=[x(])", "*", s)
    return lambda x: eval(s, {"x": x})  # noqa: S307 - test-only, generated input


def _complete(tex: str) -> bool:
    """No factor of degree two left, and no linear factor with a common factor."""
    if re.search(r"\([^()]*x\^\{2\}[^()]*\)", tex):
        return False
    for a, b in re.findall(r"\((\d*)x [+-] (\d+)\)", tex):
        if math.gcd(int(a or 1), int(b)) > 1:
            return False
    return True


def test_twenty_four_sets_are_registered():
    assert len(KEYS) == 24


@pytest.mark.parametrize("key", KEYS)
def test_choices_are_distinct_and_full(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        texts = [_choice(c) for c in q.choices]
        assert len(texts) == len(set(texts)) == REGISTRY[key].max_choices, (seed, texts)


@pytest.mark.parametrize("key", ["math.factor_common_m2", "math.factor_trinomial_m2",
                                 "math.factor_cubic_common_m3", "math.factor_cubic_grouping_m3"])
def test_factorisations(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        f = _poly(q.stem[-1].tex)
        right = [_choice(c) for c in q.choices
                 if all(_poly(_choice(c))(x) == f(x) for x in XS) and _complete(_choice(c))]
        assert right == [_answer(q)], (seed, q.stem[-1].tex, [_choice(c) for c in q.choices])


def test_factorising_applied():
    for seed in SEEDS:
        q = generate("math.factor_apply_m2", Random(seed))
        s, ans = _stem(q), _answer(q)
        m = re.search(r"พื้นที่ (.+?) ตารางหน่วย", s)
        if m:
            area = _poly(m.group(1))
            side = re.search(r"ด้านหนึ่งยาว (.+?) หน่วย", s)
            other = _poly(side.group(1)) if side else _poly(ans)
            assert all(_poly(ans)(x) * other(x) == area(x) for x in XS), s
        else:
            a, b = map(int, re.findall(r"\d+", q.stem[-1].tex))
            assert _number(ans) == a * b


def test_counting():
    for seed in SEEDS:
        s, ans = _stem(q := generate("math.add_or_multiply_m4", Random(seed))), _number(_answer(q))
        n = _ints(s)
        if "หรือโดยรถไฟ" in s:
            want = n[0] + n[1]
        elif "ผ่าน B" in s:
            want = n[0] * n[1]
        elif "ร้านอาหาร" in s:
            want = n[0] * n[1] * n[2]
        else:
            cards, digits = n[0], n[2]
            want = sum(1 for _ in itertools.permutations(range(cards), digits))
        assert ans == want, s

        s, ans = _stem(q := generate("math.arrange_in_row_m4", Random(seed))), _number(_answer(q))
        n = _ints(s)
        if "หัวแถว" in s:
            want = math.factorial(n[0] - 1)
        elif "ประธาน" in s:
            want = math.perm(n[1], 2)
        elif "หน้ากระดาน" in s:
            want = math.perm(n[1], n[0])
        else:
            want = math.factorial(n[0])
        assert ans == want, s

        s, ans = _stem(q := generate("math.choose_group_m4", Random(seed))), _number(_answer(q))
        r, n = sorted(_ints(s)[:2])
        teams = [t for t in itertools.combinations(range(n), r) if "หัวหน้าห้อง" not in s or 0 in t]
        assert ans == len(teams), s


def test_sample_spaces_and_probabilities():
    for seed in SEEDS:
        q = generate("math.sample_space_m4", Random(seed))
        s = _stem(q)
        coins = 2 if "เหรียญ 2" in s else 3 if "เหรียญ 3" in s else 1 if "เหรียญ" in s else 0
        dice = 2 if "ลูกเต๋า 2" in s else 1 if "ลูกเต๋า" in s else 0
        if "วงล้อ" in s:
            want = _ints(s)[0] ** 2
        elif "ลูกบอล" in s:
            _, _, n, coins = _ints(s)
            want = n * 2 ** coins
        else:
            want = 2 ** coins * 6 ** dice * (10 if "บัตร" in s else 1)
        assert _number(_answer(q)) == want, s

        q = generate("math.event_probability_m4", Random(seed))
        s = _stem(q)
        n = _ints(s)
        if "ลูกเต๋า" in s:
            rolls = list(itertools.product(range(1, 7), repeat=2))
            hit = (lambda r: sum(r) >= n[-1]) if "อย่างน้อย" in s else (lambda r: sum(r) == n[-1])
            want = Fraction(sum(map(hit, rolls)), len(rolls))
        else:
            tosses = list(itertools.product((0, 1), repeat=n[0]))
            want = Fraction(sum(sum(t) == n[1] for t in tosses), len(tosses))
        assert _frac(_answer(q)) == want, s

        q = generate("math.probability_by_choosing_m4", Random(seed))
        s = _stem(q)
        boys, girls = _ints(s)[:2]
        kids = "b" * boys + "g" * girls
        pairs = list(itertools.combinations(kids, 2))
        want_pair = ("g", "g") if "ทั้ง 2" in s else None
        hits = sum((p == want_pair) if want_pair else (sorted(p) == ["b", "g"]) for p in pairs)
        assert _frac(_answer(q)) == Fraction(hits, len(pairs)), s


def _surd_value(tex: str) -> float:
    total = 0.0
    for k, n in re.findall(r"(\d*)\\sqrt\{(\d+)\}", tex):
        total += int(k or 1) * math.sqrt(int(n))
    return total


def test_radicals_and_rational_powers():
    for seed in SEEDS:
        q = generate("math.radical_to_power_m5", Random(seed))
        tex, ans = q.stem[-1].tex, _answer(q)
        m = re.fullmatch(r"(\d+)\^\{\\frac\{(\d+)\}\{(\d+)\}\}", tex)
        if m:
            a, p, n = map(int, m.groups())
            assert _number(ans) == round(a ** (p / n)), tex
        else:
            m = re.fullmatch(r"\\sqrt(?:\[(\d)\])?\{(\d+)(?:\^\{(\d+)\})?\}", tex)
            n, a, p = int(m.group(1) or 2), int(m.group(2)), int(m.group(3) or 1)
            got = re.fullmatch(r"(\d+)\^\{(.+)\}", ans)
            assert int(got.group(1)) == a and _frac(got.group(2)) == Fraction(p, n), (tex, ans)

        q = generate("math.simplify_radicals_m5", Random(seed))
        tex, ans = q.stem[-1].tex, _answer(q)
        if tex.startswith("("):
            a, b = _ints(tex)[:2]
            assert _number(ans) == a * a - b
        else:
            assert math.isclose(_surd_value(ans), _surd_value(tex)), (tex, ans)
            k = re.match(r"(\d*)\\sqrt\{(\d+)\}", ans)
            n = int(k.group(2))
            assert all(n % (d * d) for d in range(2, n)), ans   # nothing left to take out

        q = generate("math.power_laws_rational_m5", Random(seed))
        tex = q.stem[-1].tex
        exps = [_frac(e) for e in re.findall(r"\\frac\{\d+\}\{\d+\}", tex)]
        want = exps[0] + exps[1] if r"\cdot" in tex else exps[0] * exps[1]
        ans = _answer(q)
        got = Fraction(1) if ans == "x" else _frac(re.fullmatch(r"x\^\{(.+)\}", ans).group(1))
        assert got == want, (tex, ans)


def test_functions_in_context():
    kind_of = dict(_MODELS)
    for seed in SEEDS:
        q = generate("math.function_model_type_m5", Random(seed))
        situation = re.search(r"“(.+)”", _stem(q)).group(1)
        assert _answer(q) == kind_of[situation]

        q = generate("math.function_context_value_m5", Random(seed))
        s, ans = _stem(q), _number(_answer(q))
        n = _ints(s)
        if "ลานจอดรถ" in s:
            rate, hours, mins = n
            assert ans == rate * math.ceil(hours + mins / 60), s
        elif "แท็กซี่" in s:
            start, per, _, _, km = n
            assert ans == start + per * (km - 1), s
        else:
            start, hours = n[0], n[-1]
            assert ans == start * 2 ** hours, s

        q = generate("math.function_interpret_m5", Random(seed))
        s, ans = _stem(q), _number(_answer(q))
        if "ลูกบอล" in s:
            v, h0 = re.search(r"h\(t\) = −5t² \+ (\d+)t(?: \+ (\d+))? เมตร", s).groups()
            v, h0 = int(v), int(h0 or 0)
            best = max(-5 * t * t + v * t + h0 for t in [i / 100 for i in range(0, 1000)])
            assert ans == best, s
        else:
            start, per, target = _ints(s)[:3]
            assert start + per * ans == target, s


def test_interest():
    for seed in SEEDS:
        q = generate("math.simple_interest_years_m5", Random(seed))
        s, ans = _stem(q), _number(_answer(q))
        p, r, n = _ints(s)[:3]
        interest = p * r * n / 100
        assert ans == (interest if "ดอกเบี้ยรวม" in s else p + interest), s

        q = generate("math.future_present_value_m5", Random(seed))
        s, ans = _stem(q), _number(_answer(q))
        factor = float(re.search(r"≈ ([\d.]+)", s).group(1))
        money = _ints(s)[0]
        want = money * factor if s.startswith("ฝากเงิน") else money / factor
        assert abs(ans - want) < 0.006, s

        q = generate("math.compare_offers_m5", Random(seed))
        s = _stem(q)
        p, n = _ints(s)[:2]
        r1 = int(re.search(r"คงต้นร้อยละ (\d+)", s).group(1))
        factor = float(re.search(r"≈ ([\d.]+)", s).group(1))
        a, b = p * (1 + r1 * n / 100), p * factor
        best = "ธนาคาร ก" if a > b else "ธนาคาร ข"
        assert _answer(q) == f"{best} ได้มากกว่าประมาณ {abs(a - b):,.2f} บาท", s


def _linear(tex: str) -> tuple[int, int]:
    """x + b or x - b → (1, b)."""
    m = re.fullmatch(r"x(?: ([+-]) (\d+))?", tex.strip())
    return 1, (int(m.group(2)) * (-1 if m.group(1) == "-" else 1)) if m.group(1) else 0


def test_rational_equations():
    for seed in SEEDS:
        q = generate("math.rational_equation_m4", Random(seed))
        num, den, k = re.fullmatch(r"\\frac\{(.+)\}\{(.+)\} = (-?\d+)", q.stem[-1].tex).groups()
        a, b = _linear(num)[1], _linear(den)[1]
        x = int(_answer(q).removeprefix("x = "))
        assert x + b != 0 and Fraction(x + a, x + b) == int(k)
        for c in q.choices:
            y = int(_choice(c).removeprefix("x = "))
            if y != x:
                assert y + b == 0 or Fraction(y + a, y + b) != int(k)

        q = generate("math.rational_equation_extraneous_m4", Random(seed))
        num, den, rhs = re.fullmatch(r"\\frac\{(.+)\}\{(.+)\} = \\frac\{(\d+)\}\{.+\}", q.stem[-1].tex).groups()
        top, bottom = _poly(num), _poly(den)
        roots = sorted(x for x in range(-20, 21) if bottom(x) != 0 and top(x) == int(rhs))
        want = r"\varnothing" if not roots else r"\{" + ", ".join(map(str, roots)) + r"\}"
        assert _answer(q) == want, q.stem[-1].tex


def _in(interval: str, x: Fraction) -> bool:
    for part in interval.split(r" \cup "):
        lb, lo, hi, rb = re.fullmatch(r"([\[(])(.+), (.+)([\])])", part.strip()).groups()
        lo_ok = lo == r"-\infty" or (x >= int(lo) if lb == "[" else x > int(lo))
        hi_ok = hi == r"\infty" or (x <= int(hi) if rb == "]" else x < int(hi))
        if lo_ok and hi_ok:
            return True
    return False


def test_rational_inequalities():
    for seed in SEEDS:
        q = generate("math.rational_inequality_m4", Random(seed))
        num, den, op = re.fullmatch(r"\\frac\{(.+)\}\{(.+)\} (\\geq|\\leq) 0", q.stem[-1].tex).groups()
        p, qq = -_linear(num)[1], -_linear(den)[1]
        for x in [Fraction(n, 2) for n in range(-20, 21)]:
            want = x != qq and ((x - p) / (x - qq) >= 0 if op == r"\geq" else (x - p) / (x - qq) <= 0)
            assert _in(_answer(q), x) == want, (q.stem[-1].tex, _answer(q), x)


def test_uniform_distribution():
    for seed in SEEDS:
        q = generate("math.uniform_distribution_m6", Random(seed))
        s = _stem(q)
        n = 6 if "ลูกเต๋า" in s else 4 if "วงล้อ" in s else _ints(s)[2]
        values = range(1, n + 1)
        if "E(X)" in s:
            want = Fraction(sum(values), n)
        elif "≤" in s:
            a, b = map(int, re.search(r"P\((\d+) ≤ X ≤ (\d+)\)", s).groups())
            want = Fraction(sum(a <= v <= b for v in values), n)
        else:
            want = Fraction(1, n)
        assert _frac(_answer(q)) == want, s
