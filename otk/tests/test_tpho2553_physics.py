"""Pin TPhO 9 (2553) readings against the bound solution and check draws."""

from fractions import Fraction
from math import atan, degrees, pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2553_physics"
SHEET = load_sheet(SID)
# Solution formulas at each solver's constants (items 12-14 come from the
# experimental papers with synthetic readings).
SOURCE_VALUES = {
    1: 2 * 5 * 3 / 6,  # v1 = 2M V0/(M + m)
    2: 1.4 * 6 / 14,  # l1 = l0 (M + m)/(3M - m)
    3: 0.663157894736842,
    4: 2.0 / 100,  # l0 sqrt(m/M)
    5: 1.0e5 + 20 * 9.8 / 0.04,
    6: 8.31 * 30 / (1.0e5 * 0.04 + 20 * 9.8),
    7: 1.049e5 * (5 / 3) * 0.04**2 * 0.001 / 0.002,
    8: 2 * pi * sqrt(3 * 20 * 0.002 / (5 * (1.0e5 + 196 / 0.04) * 0.04**2)),
    9: 1.25,  # Q at position 6: 5/4 C V0
    10: 550e-9 / 0.02 * 206264.806,
    11: 550e-9 / (2 * 5 / 206264.806) * 1e3,
    12: degrees(atan(1.3325)),  # 53.1 degrees
    13: 1.4281480067,
    14: 2 * pi * sqrt(0.51**2 / (12 * 9.8 * 0.05)),
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 14
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2553_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=1e-4)


def test_doubler_table_matches_the_solution():
    mod = solver_module(SHEET, SHEET.items[8])
    table = {
        4: {"Vb": 0, "Vd": 0.5, "q": 1, "Q": 0.5},
        5: {"Vb": 0.75, "Vd": 0.75, "q": 0.75, "Q": 0.75},
        6: {"Vb": 1.25, "Vd": 1.25, "q": 0.25, "Q": 1.25},
    }
    for position, row in table.items():
        for quantity, value in row.items():
            assert mod.solve(position=position, quantity=quantity) == pytest.approx(value)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_second_meeting_follows_the_wall_geometry():
    for seed in range(60):
        q = generate("phys.tpho2553_q02", Random(seed))
        big, speed, small = (int(x) for x in re.findall(r"(\d+) (?:kg|m/s)", q.stem[0].text)[:3])
        gap = Fraction(re.search(r"ห่างผนัง ([\d.]+) m", q.stem[0].text)[1])
        v1 = Fraction(2 * big * speed, big + small)
        V1 = Fraction((big - small) * speed, big + small)
        t1 = 2 * gap / (v1 + V1)
        assert _rational(q.choices[q.answer].content[0].tex) == gap - V1 * t1
