"""Pin source readings and check generated physics beyond solver agreement."""

from fractions import Fraction
from math import pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "posn2568_physics"
SHEET = load_sheet(SID)
# The printed answer of each item, evaluated at the solver's source constants.
SOURCE_VALUES = {
    1: Fraction(36, 60),  # u^2/(6g), u = 6
    2: 5,  # u/2
    3: 4,  # m u/(m + M)
    4: Fraction(-36, 25),  # -k Q L/(R^2 + L^2)^(3/2), 5 nC, 3, 4
    5: 20 / pi,  # Q omega/(2 pi)
    6: 8e-12,  # mu0 Q omega/(4 pi R)
    7: 3,  # R/4
    8: 3,
    9: Fraction(25, 4),  # L/(KA)
    10: 80,  # (4 T1 + T2)/5
    11: 106000,
    12: Fraction(4, 5),  # 2 sqrt(y(h - y))
    13: 4,
    14: 2,
    15: 0,
    16: 10,  # i R + q/C
    17: 120 / pi**2,  # 6 C1 E/pi^2
    18: Fraction(340 * 2, 22),
    19: 5e7,
    20: 9.83 - 4 * pi**2 * 6.37e6 / 86160**2,
    21: 9.796,  # 9.80 to three figures
    22: 2,
    23: 6,  # T/pi = 2 sqrt(D^3/(3GM)) with D = 3, GM = 1
    24: Fraction(1, 8),
    25: (1 + 2 / pi) / 0.2,
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
    assert len(SHEET.items) == len(SOURCE_VALUES) == 25
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.posn2568_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    got = mod.solve(**mod.PARAMS)
    assert got == pytest.approx(float(SOURCE_VALUES[item.number]), rel=1e-3, abs=1e-15)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_junction_balances_heat_flow():
    for seed in range(60):
        stem, tex = _answer("phys.posn2568_q10", seed)
        l1, a1, l2, a2 = map(int, re.findall(r"ยาว (\d+)L หน้าตัด (\d+)A", stem)[0] + re.findall(r"ยาว (\d+)L หน้าตัด (\d+)A", stem)[1])
        hot, cold = map(int, re.findall(r"คงที่ (\d+) °C", stem))
        junction = _rational(tex)
        assert (hot - junction) * a1 / l1 == (junction - cold) * a2 / l2


def test_generated_network_equals_its_load():
    for seed in range(60):
        stem, tex = _answer("phys.posn2568_q08", seed)
        first, second = map(int, re.findall(r"R[₁₂] = (\d+) Ω", stem))
        load = Fraction(tex)
        assert first + second * load / (second + load) == load


def test_generated_echo_away_is_consistent():
    for seed in range(60):
        stem, tex = _answer("phys.posn2568_q18", seed)
        start = int(re.search(r"t = (\d+) s", stem)[1])
        delay = int(re.search(r"หลังเปิดหวูด (\d+) s", stem)[1])
        speed = _rational(tex)
        assert 340 * delay == speed * start + speed * (start + delay)


def test_triangle_period_from_vector_forces():
    for seed in range(40):
        stem, tex = _answer("phys.posn2568_q23", seed)
        side = int(re.search(r"ยาวด้าน (\d+)", stem)[1])
        gm = Fraction(re.search(r"GM = (\S+) ", stem)[1])
        half = int(tex.removesuffix(r"\pi") or 1) / 2
        # omega^2 r = sqrt3 GM / side^2 with r = side/sqrt3 -> omega^2 = 3GM/side^3
        omega = sqrt(3 * gm / side**3)
        assert 2 * pi / omega == pytest.approx(2 * half * pi)
