"""Pin source readings and check generated physics beyond solver agreement."""

from fractions import Fraction
from math import pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "posn2569_physics"
SHEET = load_sheet(SID)
# The printed answer of each item, evaluated at the solver's source constants.
# Items 11-30 are Part 2's items 1-20 (Part 2 restarts at 1 in the source).
SOURCE_VALUES = {
    1: (sqrt(2) + 1) / sqrt(8),
    2: (sqrt(2) + 1) / sqrt(8),
    3: 5,  # (M - rho V) g / beta
    4: 6,  # a / (1 - sqrt beta)
    5: 3.5,  # L sin(i - theta)/cos theta
    6: 17,
    7: 12.8,  # A K (T1 - T2)/L
    8: (0, 10),  # 0 and 2u
    9: -1.44,
    10: Fraction(27, 125),
    11: 20,  # 2F
    12: 40,  # 4f
    13: 7.5,  # g tan beta
    14: 15,  # (Mg/2) tan theta
    15: 2,  # R/6
    16: 400,  # rho A v^2
    17: 2 * 36 / (2 * pi * 0.5),
    18: Fraction(3, 4),  # tan theta
    19: 16,  # L1 + L2
    20: 8.3 * 300 / 0.029,
    21: 18,  # E^2/(4r)
    22: 75,  # 100 C1/(C1 + C2)
    23: 8,
    24: Fraction(1, 6),  # m/(M + 2m)
    25: 2 * 2999 / 1001,  # -> 3u as M/m grows
    26: 3320,
    27: 8,  # (T/2) sqrt(v^2 - u^2)
    28: 1 / sqrt(12),  # m / sqrt(M(M + m))
    29: Fraction(1, 3),
    30: 30,  # 3f with f = 10
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def _answer(key, seed):
    q = generate(key, Random(seed))
    return q.stem[0].text, q.choices[q.answer].content[0].tex


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 30
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.posn2569_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)
    # Part 2 keeps its printed numbering in the provenance.
    assert SHEET.items[10].source.startswith("ตอนที่ 2 ข้อ 1:")


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    expected = SOURCE_VALUES[item.number]
    got = mod.solve(**mod.PARAMS)
    if isinstance(expected, tuple):
        assert got == pytest.approx(tuple(float(x) for x in expected))
    else:
        assert got == pytest.approx(float(expected))


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_null_point_cancels_the_fields():
    for seed in range(60):
        stem, tex = _answer("phys.posn2569_q04", seed)
        beta = Fraction(re.search(r"−(\S+)Q อยู่ที่", stem)[1])
        gap = int(re.search(r"x = (\d+) cm บนแกน", stem)[1])
        x = _rational(tex)
        assert x > gap
        assert 1 / x**2 == beta / (x - gap) ** 2


def test_generated_explosion_keeps_momentum_and_energy():
    for seed in range(60):
        stem, tex = _answer("phys.posn2569_q08", seed)
        speed = int(re.search(r"อัตราเร็ว (\d+) m/s", stem)[1])
        ratio = Fraction(re.search(r"เป็น (\S+) เท่า", stem)[1])
        first, second = tex.removeprefix(r"\left(").removesuffix(r"\right)").split(r",\ ")
        slow, fast = _rational(first), _rational(second)
        assert slow + fast == 2 * speed
        assert (slow * slow + fast * fast) / 2 == ratio * speed * speed
        assert 0 <= slow <= fast


def test_generated_lens_pair_focuses_where_stated():
    for seed in range(60):
        stem, tex = _answer("phys.posn2569_q30", seed)
        a = int(re.search(r"โฟกัส −(\d+) cm", stem)[1])
        b = int(re.search(r"เลนส์นูนความยาวโฟกัส (\d+) cm", stem)[1])
        d = int(re.search(r"ที่ระยะ (\d+) cm", stem)[1])
        gap = _rational(tex)
        # The diverging lens's virtual image (a in front of it) is the object.
        u = gap + a
        assert 1 / u + Fraction(1, d) == Fraction(1, b)


def test_resistor_count_matches_a_direct_enumeration():
    for seed in range(30):
        stem, tex = _answer("phys.posn2569_q06", seed)
        a, b, c = (Fraction(v) for v in re.findall(r"(\d+) Ω", stem))
        par = lambda *rs: 1 / sum(1 / r for r in rs)
        values = {a, b, c, a + b, a + c, b + c, par(a, b), par(a, c), par(b, c), a + b + c, par(a, b, c)}
        for p, q, r in ((a, b, c), (b, a, c), (c, a, b)):
            values |= {p + par(q, r), par(p, q + r)}
        assert int(tex) == len(values)
