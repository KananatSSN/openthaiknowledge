"""Pin source readings and check generated physics beyond solver agreement."""

from fractions import Fraction
from math import sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "posn2564_physics"
SHEET = load_sheet(SID)
# The printed answer of each item, evaluated at the solver's source constants.
SOURCE_VALUES = {
    1: 2,  # a - mu g, slipping since mu g = 3 < 5
    2: 4,
    3: sqrt(3 / 2),  # sqrt(2(1 - R/x)) with x = 4R
    4: Fraction(1, 2),  # m/M = e
    5: 14,  # mg/k = 10 cm, plus a = 4 cm
    6: 40,  # (rho V/m - 1) h = (5 - 1) 10
    7: 50,
    8: Fraction(4, 125),
    9: Fraction(1, 5),
    10: 15,
    11: Fraction(2, 21),
    12: Fraction(9, 4),
    13: 16,
    14: -50,
    15: sqrt(7 / 8),
    16: Fraction(-7, 2),
    17: sqrt(10 / 4),
    18: Fraction(5, 2),
    19: Fraction(13, 15) ** 3,
    20: 47,
    21: Fraction(2, 5),
    22: 30,
    23: Fraction(13, 24),
    24: 8,
    25: Fraction(2, 3),
    26: 3,
    27: 7,
    28: 4,
    29: Fraction(4, 5),
    30: (Fraction(3, 4), Fraction(2500, 3)),
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
        key for key in REGISTRY if key.startswith("phys.posn2564_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


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


def test_generated_mixing_balances_heat():
    for seed in range(60):
        stem, tex = _answer("phys.posn2564_q07", seed)
        hot, cold = map(int, re.findall(r"อุณหภูมิ (\d+) °C", stem))
        ratio = Fraction(re.search(r"m_A S_A = (\S+) m_B S_B", stem)[1])
        final = _rational(tex)
        assert ratio * (hot - final) == final - cold


def test_generated_bridge_charge_from_kirchhoff():
    for seed in range(60):
        stem, tex = _answer("phys.posn2564_q11", seed)
        r1, r2, r3, r4 = map(int, re.findall(r"(\d+)R", stem)[:4])
        emf = int(re.search(r"อุดมคติ (\d+) V", stem)[1])
        cap = int(re.search(r"ตัวเก็บประจุ (\d+) μF", stem)[1])
        # Current through each branch, then the drop across the left resistors.
        left_top = Fraction(emf, r1 + r2) * r1
        left_bottom = Fraction(emf, r3 + r4) * r3
        assert _rational(tex) == cap * abs(left_top - left_bottom)


def test_generated_ladder_reduces_to_the_target():
    for seed in range(60):
        stem, tex = _answer("phys.posn2564_q20", seed)
        half, total = map(int, re.findall(r"อนุกรมตัวต้านทาน (\d+) Ω แล้วมีตัวต้านทาน (\d+) Ω", stem)[0])
        last = int(re.search(r"ต่ออนุกรม (\d+) Ω กับตัวต้านทาน R", stem)[1])
        tail = Fraction(last + int(tex))
        for _ in range(2):
            tail = half + tail * total / (tail + total)
        assert tail == total


def test_generated_wall_hit_is_the_apex():
    for seed in range(60):
        stem, tex = _answer("phys.posn2564_q30", seed)
        width = int(re.search(r"ตามแนวระดับ (\d+) m", stem)[1])
        height = int(re.search(r"ความสูง (\d+) m", stem)[1])
        first, second = tex.removeprefix(r"\left(").removesuffix(r"\right)").split(r",\ ")
        slope, speed2 = _rational(first), _rational(second)
        # u_x^2 = u^2/(1 + tan^2), u_y = u_x tan; apex at (u_x u_y/g, u_y^2/(2g)).
        ux2 = speed2 / (1 + slope * slope)
        uy2 = ux2 * slope * slope
        assert uy2 / 20 == height
        assert (ux2 * uy2) == (width * 10) ** 2
