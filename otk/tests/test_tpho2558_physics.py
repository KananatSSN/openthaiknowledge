"""Pin TPhO 14 (2558) readings against the solutions and check draws."""

from math import atan, cos, degrees, pi, sin, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2558_physics"
SHEET = load_sheet(SID)
QE, MG = 2e-6 * 10e3, 4e-3 * 9.8
T0 = atan(QE / MG)
# Solution formulas at each solver's constants (items 14-17 come from the
# experimental paper; 14-16 use the solution's own table).
SOURCE_VALUES = {
    1: degrees(2 * atan(QE / MG)),
    2: degrees(T0),
    3: sqrt((MG * cos(T0) + QE * sin(T0)) / (4e-3 * 0.5)) / (2 * pi),
    4: (-(150 / 9.8 - 15) + sqrt((150 / 9.8 - 15) ** 2 + 10 * 20 * 1.5**2 / 3)) / 10,
    5: 1.5 * sqrt(20 / 30),
    6: 100 * 373.15 / 300.15,
    7: 0.5613476713503127,
    8: 2.05402288363372,
    9: 30 * (10 / 20) ** (1 / 1.4),
    10: 25.203536810170906,
    11: 10.687299827512637,
    12: pi * 0.05**2 * 0.2 * 100 * 1e3,
    13: 1e-3 * pi * 0.05**4 * 0.1**2 * 100**2 / (16 * 1.7e-8),
    14: 0.425,  # the solution's r (mm)
    15: 2.896,  # the solution's eta (mPa s)
    16: 1.6,  # the solution's eta_c (mPa s)
    17: 85.39588016316767,
}
ROUGH = {14: 2e-3, 15: 5e-3, 16: 3e-2}  # the solution rounds eta_c = 1.568 to 1.6


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 17
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2558_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    rel = ROUGH.get(item.number, 1e-9)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=rel)


def test_drop_volume_slip():
    # 1.20 ml over 50 drops is 0.0240 ml each; the solution's 0.0235 ml gives
    # its 83.6 mN/m, the correct 0.0240 ml gives 85.4 mN/m.
    mod = solver_module(SHEET, SHEET.items[16])
    assert mod.solve(drops=1, volume=0.0235) == pytest.approx(83.6, abs=0.1)
    assert mod.solve() == pytest.approx(85.4, abs=0.1)


def test_best_barrel_is_where_the_push_falls_to_the_drag():
    from otk.sheets.tpho2558_physics._popgun import push, start_gap

    D = solver_module(SHEET, SHEET.items[10]).solve() * 1e-2
    gap = start_gap(0.30, 10.0, 1e-4)
    assert push(D, gap, 10.0, 1e-4, 0.5) == pytest.approx(0.0, abs=1e-9)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_gas_pressure_uses_kelvin():
    for seed in range(60):
        q = generate("phys.tpho2558_q06", Random(seed))
        p, t0, t1 = (float(x) for x in re.findall(r"([\d.]+) (?:kPa|°C)", q.stem[0].text)[:3])
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(p * (t1 + 273.15) / (t0 + 273.15), rel=5e-3)
