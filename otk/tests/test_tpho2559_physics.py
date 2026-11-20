"""Pin TPhO 15 (2559) readings against the solutions and check draws."""

from math import pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2559_physics"
SHEET = load_sheet(SID)
# Solution values at each solver's constants (the lab items use the
# solution's own readings where it gives them).
SOURCE_VALUES = {
    1: sqrt(8 * 1000 * 9.8 * 0.05 / (15 * 1.2)),
    2: 100 * 2.0 / (1e-6 * 200e9) * 1e3,
    3: 1.47526368159204,
    4: 100 / 200e9 * (50e6 / (12e-6 * 200e9) - 1) * 1e6,
    5: 5.67e-8 * 50e-6 * (2500**4 - 300**4),
    6: 0.6,  # the solution's n
    7: 99.74,  # P'_N2 = 0.9974e5 Pa
    8: 77.33,  # m^3
    9: 236.1,  # kJ
    10: 777.6,  # g
    11: 1929.0,  # kJ
    12: 2506.0,  # kJ
    13: 77.0,  # percent
    14: 215.14774194546226,
    15: 2.353329305401025,
    16: 31.014032111840432,
    17: 8.978063404558396,
    18: 0.03244703296994792,
    19: 0.4 * 3.0 / 2,  # k = mu r/2
    20: 0.6373558363854258,
    21: 294.0,  # lm, as printed
    22: 573.0,  # nm at 21 degrees
    23: (0.0359 / 166) / (0.0204 / 56),
}
ROUGH = {7: 1e-4, 8: 1e-4, 9: 2e-3, 10: 1e-3, 11: 1e-3, 12: 1e-3, 13: 1e-3, 20: 1e-9, 21: 2e-3, 22: 1e-3}


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 23
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2559_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    value = mod.solve(**mod.PARAMS)
    if item.number == 20:
        value = -value
    assert value == pytest.approx(SOURCE_VALUES[item.number], rel=ROUGH.get(item.number, 1e-9))


def test_solution_gamma_from_its_own_table():
    # The solution's table of 14 readings fits a slope of 1.30 (gamma = -0.65);
    # its printed 1.2531 (gamma = -0.63) comes from a graph whose points start
    # at log x = 1.17, below the table's first reading (log 21 = 1.32).
    xs = (21, 23, 25, 27, 29, 31, 33, 35, 41, 47, 55, 62, 73, 78)
    rs = (846, 925, 1009, 1112, 1230, 1334, 1437, 1544, 1866, 2245, 2743, 3308, 4140, 4710)
    gamma = solver_module(SHEET, SHEET.items[19]).solve(distances=xs, resistances=rs)
    assert -2 * gamma == pytest.approx(1.302, abs=2e-3)


def test_wire_area_forms_agree_when_alpha_is_negligible():
    mod = solver_module(SHEET, SHEET.items[3])
    W, Y0, e, a = 100.0, 200e9, 50e6, 12e-6
    assert mod.solve() == pytest.approx(W * e / (a * Y0**2) * 1e6 - W / Y0 * 1e6)


def test_pump_drill_stops_after_n_turns():
    push = solver_module(SHEET, SHEET.items[16]).solve()
    b, n, k, M, g = 0.03, 5, 0.3e-3, 1.0, 9.8
    spun = push * b - 2 * n * pi * k * (M * g + push)
    assert spun == pytest.approx(2 * n * pi * k * M * g)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_grating_wavelength():
    from math import radians, sin

    for seed in range(60):
        q = generate("phys.tpho2559_q22", Random(seed))
        d, angle = (float(x) for x in re.findall(r"([\d.]+) ?(?:µm|°)", q.stem[0].text)[:2])
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(d * 1e3 * sin(radians(angle)), rel=5e-3)
