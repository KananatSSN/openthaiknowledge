"""Pin source readings and check generated physics beyond solver agreement."""

from fractions import Fraction
from math import pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "posn2567_physics"
SHEET = load_sheet(SID)
# The printed answer of each item, evaluated at the solver's source constants.
SOURCE_VALUES = {
    1: sqrt(2),
    2: (20, 30),  # 2u^2/g with u = 10, phi = 30 deg
    3: (4, 4),  # u/2 each, u = 8
    4: 8,  # M g sin I/(I + M R^2), solid cylinder, 4 kg, sin = 0.6
    5: 4e-7 * pi * 100 * 0.1 / 0.002,  # mu0 I^2 R/d, attracting
    6: 4 * 9 * 3 / (3 * sqrt(3) * 0.09),
    7: 2,  # 2 eps0 A/d
    8: 1,  # R1 C1 = R2 C2
    9: 15,  # (1/2)(1/R1 - 1/R2), out of the page
    10: Fraction(245, 2),
    11: 1000 / 5.183,  # ~ 193 ohm
    12: 40,  # 4 theta - 2 i
    13: 5,  # 4 gamma / R
    14: Fraction(-1, 50),
    15: 478,
    16: Fraction(1, 32),
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
    assert len(SHEET.items) == len(SOURCE_VALUES) == 16
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.posn2567_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    expected = SOURCE_VALUES[item.number]
    got = mod.solve(**mod.PARAMS)
    if isinstance(expected, tuple):
        assert got == pytest.approx(tuple(float(x) for x in expected))
    elif item.number == 15:
        assert round(got) == expected
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


def test_generated_collision_keeps_momentum_and_the_stated_energy():
    for seed in range(60):
        stem, tex = _answer("phys.posn2567_q03", seed)
        speed = int(re.search(r"อัตราเร็ว (\d+) m/s", stem)[1])
        fraction = Fraction(re.search(r"พลังงานจลน์ของระบบเหลือ (\S+) ของ", stem)[1])
        first, second = tex.removeprefix(r"\left(").removesuffix(r"\right)").split(r",\ ")
        slow, fast = _rational(first), _rational(second)
        assert slow + fast == speed
        assert slow * slow + fast * fast == fraction * speed * speed
        assert slow <= fast


def test_generated_ladder_node_obeys_charge_balance():
    for seed in range(60):
        stem, tex = _answer("phys.posn2567_q16", seed)
        emf = int(re.search(r"แหล่งกำเนิด (\d+) V", stem)[1])
        series = int(re.search(r"อนุกรม (\d+) μF", stem)[1])
        node = int(re.search(r"ต่อเรียงกัน (\d+) ตัว", stem)[1])
        shunt, tail = map(int, re.findall(r"มีตัวเก็บประจุ (\d+) μF ต่อลงดิน", stem))
        # Back-substitute exactly: from the last node, each node voltage is a
        # fixed fraction of the previous one; build them from E and check.
        voltages = [Fraction(emf)]
        # Equivalent capacitance looking right from node k (k = node .. 1).
        right = Fraction(tail)
        looking = [right]
        for _ in range(node - 1):
            right = shunt + series * right / (series + right)
            looking.append(right)
        looking.reverse()
        for k in range(node):
            voltages.append(voltages[-1] * series / (series + looking[k]))
        assert _rational(tex) == voltages[-1]
