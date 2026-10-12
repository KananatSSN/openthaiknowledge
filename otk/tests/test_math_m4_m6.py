"""ม.4–ม.6 enrichment: answers re-derived from what the learner is shown."""

from __future__ import annotations

from otk.tests._origins import keys_from

import itertools
import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m4.logic import LogicEquivalenceM4

SEEDS = range(300)
M4 = keys_from("math_m4")
M5 = keys_from("math_m5")
M6 = keys_from("math_m6")


def _stem(q) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in q.stem)


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer]).replace("{,}", "")


def _ints(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"-?\d+", s.replace(",", ""))]


def _frac(tex: str) -> Fraction:
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if not m:
        return Fraction(tex)
    sign, n, d = m.groups()
    return (-1 if sign else 1) * Fraction(int(n), int(d))


def _each(key):
    for seed in SEEDS:
        yield seed, generate(key, Random(seed))


def test_module_sizes():
    assert (len(M4), len(M5), len(M6)) == (11, 16, 13)


@pytest.mark.parametrize("key", M4 + M5 + M6)
def test_four_distinct_choices(key):
    for seed, q in _each(key):
        assert len(q.choices) == REGISTRY[key].max_choices, (key, seed, _stem(q))
        assert len({_choice(c) for c in q.choices}) == REGISTRY[key].max_choices, (key, seed, _stem(q))


# ── ตรรกศาสตร์: every listed equivalence holds, every distractor fails ───────

def _truth(tex: str):
    """Evaluate a p/q formula written in the set's TeX over all four rows."""
    py = (tex.replace(r"{\sim}p", "(not p)").replace(r"{\sim}q", "(not q)").replace(r"{\sim}", " not ")
          .replace(r"\land", " and ").replace(r"\lor", " or ")
          .replace(r"\leftrightarrow", " == ").replace(r"\to", " <= "))
    return tuple(bool(eval(py, {}, {"p": p, "q": q}))
                 for p, q in itertools.product((False, True), repeat=2))


@pytest.mark.parametrize("form", LogicEquivalenceM4._FORMS)
def test_logic_equivalence_table(form):
    lhs, right, wrongs = form
    assert _truth(lhs) == _truth(right)
    assert all(_truth(w) != _truth(lhs) for w in wrongs)


# ── Counting and sets ────────────────────────────────────────────────────────

def test_three_set_counting():
    for _, q in _each("math.three_set_counting_m4"):
        s = _stem(q)
        a, b, c, ab, bc, ac, abc = _ints(s)[:7]
        if "อย่างน้อยหนึ่งอย่าง" in s:
            assert _answer(q) == str(a + b + c - ab - bc - ac + abc)
        elif "ฟุตบอลอย่างเดียว" in s:
            assert _answer(q) == str(a - ab - ac + abc)


def test_circular_permutation():
    for _, q in _each("math.circular_permutation_m5"):
        s = _stem(q)
        if s.startswith("จัดคน") and "รอบโต๊ะกลม จัดได้กี่วิธี" in s:
            assert _answer(q) == str(math.factorial(_ints(s)[0] - 1))


# ── Algebra ──────────────────────────────────────────────────────────────────

def _matrix(tex: str) -> list[list[int]]:
    body = re.search(r"\\begin\{pmatrix\}(.*)\\end\{pmatrix\}", tex).group(1)
    return [[int(x) for x in row.split("&")] for row in body.split(r"\\")]


def _det(m) -> int:
    (a, b, c), (d, e, f), (g, h, i) = m
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def test_determinant_3x3():
    for _, q in _each("math.determinant_3x3_m5"):
        assert _answer(q) == str(_det(_matrix(q.stem[-1].tex)))


def _coef(sign: str, mag: str) -> int:
    return (-1 if "-" in sign else 1) * (int(mag) if mag else 1)


def test_cramer_rule():
    pat = r"(-?)(\d*)x\s*([+-])\s*(\d*)y\s*=\s*(-?\d+)"
    for _, q in _each("math.cramer_rule_m5"):
        (s1, a, t1, b, e), (s2, c, t2, d, f) = re.findall(pat, q.stem[-1].tex)
        a, b, c, d = _coef(s1, a), _coef(t1, b), _coef(s2, c), _coef(t2, d)
        e, f = int(e), int(f)
        det = a * d - b * c
        x, y = Fraction(e * d - b * f, det), Fraction(a * f - e * c, det)
        want = x if "ค่า x" in _stem(q) else y
        assert _frac(_answer(q)) == want


def test_vector_perpendicular():
    for _, q in _each("math.vector_dot_product_m5"):
        if "ตั้งฉาก" not in _stem(q):
            continue
        u_tex, v_tex = q.stem[-1].tex.split(r",\ v")
        u, v = _ints(u_tex), _ints(v_tex) + [_frac(_answer(q))]
        assert sum(a * b for a, b in zip(u, v, strict=True)) == 0


# ── Sequences ────────────────────────────────────────────────────────────────

def test_arithmetic_sequence_word():
    for _, q in _each("math.arithmetic_sequence_word_m5"):
        s = _stem(q)
        if not s.startswith("หอประชุม"):
            continue
        a, d, n = _ints(s)[:3]
        want = a + (n - 1) * d if "มีเก้าอี้กี่ตัว" in s else n * (2 * a + (n - 1) * d) // 2
        assert _answer(q) == str(want)


# ── Statistics and probability ───────────────────────────────────────────────

def test_mean_frequency_table():
    for _, q in _each("math.mean_frequency_table_m6"):
        rows = [tuple(map(int, r.split("|"))) for r in q.stem[0].text.split("\n")[2:]]
        mean = Fraction(sum(x * f for x, f in rows), sum(f for _, f in rows))
        assert abs(Fraction(_answer(q)) - mean) <= Fraction(1, 20)


def test_binomial_probability():
    for _, q in _each("math.binomial_probability_m6"):
        s = _stem(q)
        n, k = _ints(s)[0], _ints(s)[-1]
        if "เหรียญ" in s:
            p = Fraction(1, 2)
        elif "ลูกเต๋า" in s:
            p = Fraction(1, 6)
        else:
            continue
        assert _frac(_answer(q)) == math.comb(n, k) * p ** k * (1 - p) ** (n - k)
