"""Pin TPhO 16 (2560) readings against the solutions and check draws."""

from math import pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2560_physics"
SHEET = load_sheet(SID)
# Solution values at each solver's constants (the lab items use the
# solution's own tables where it gives them).
SOURCE_VALUES = {
    1: (sqrt(5e3**2 + 2 * 9.8 * 6.4e6) - 5e3) / 1e3,
    2: 7.5,  # atm
    3: 4.8,  # percent
    4: 5.0,  # percent
    5: 336.0,  # microradians
    6: 42.0,  # microradians
    7: 101.0,  # um
    8: 377.0,  # ppm
    9: 2 * 0.9030487627 / 2 * 1.0,
    10: 12.0,  # ppm
    11: 6.0,  # ppm
    12: 2.77,  # 1e7 m/s
    13: 11.4,  # kA
    14: 9.11089998,
    15: 5.94,  # 1e-7 per metre
    16: 2 * 4e-7 * pi * 100 / (pi * 0.02**2),
    17: 2.8896366553599786,
    18: 20.0 * 18.0 / 2.0,
    19: -3.97258503,
    20: 0.256749,
}
ROUGH = {2: 1e-9, 3: 5e-3, 5: 2e-3, 6: 1e-2, 7: 5e-3, 8: 1e-3, 9: 1e-6, 10: 1e-2, 11: 1e-2, 12: 2e-3, 13: 5e-3, 14: 1e-6, 15: 2e-3, 19: 1e-6, 20: 1e-5}


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 20
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2560_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    rel = ROUGH.get(item.number, 1e-9)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=rel)


def test_solution_tables():
    # Part 1: 13 readings give n = -3.92 (printed -3.9); part 2: slope
    # 27.0 g s over 1.01 m gives k = 0.262 kg/s, not the printed 0.265.
    n = solver_module(SHEET, SHEET.items[18]).solve(
        distances=(26.05, 26.68, 27.72, 28.56, 29.81, 30.65, 31.49, 33.16, 34.41, 35.88, 37.55, 39.43, 41.10),
        masses=(63.8, 56.3, 51.6, 44.9, 41.1, 34.4, 27.6, 25.3, 21.5, 17.1, 14.8, 13.2, 10.9))
    assert n == pytest.approx(-3.92, abs=0.01)
    k = solver_module(SHEET, SHEET.items[19]).solve(
        masses=(7.60, 8.54, 9.48, 10.42, 11.36, 12.30, 13.24, 14.18, 15.12, 16.06, 17.00),
        times=(3.82, 3.47, 3.06, 2.88, 2.65, 2.53, 2.38, 2.18, 2.07, 1.91, 1.84))
    assert k == pytest.approx(0.262, abs=2e-3)
    assert 27.05e-3 * 9.78 / 1.01 == pytest.approx(0.262, abs=1e-3)


def test_doublet_focuses_both_planes():
    mod = solver_module(SHEET, SHEET.items[17])
    assert mod.solve(focal=20.0, gap=2.0) > 0
    # the y plane (defocusing lens first) is the same formula with f -> -f
    assert mod.check(focal=-20.0, gap=2.0) == pytest.approx(20.0 * 22.0 / 2.0)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_low_pressure_follows_the_isochore():
    for seed in range(60):
        q = generate("phys.tpho2560_q02", Random(seed))
        text = q.stem[0].text
        p = float(re.search(r"ความดัน (\d+) atm", text)[1])
        hot = float(re.search(r"อุณหภูมิ (\d+) K", text)[1])
        cold = float(re.search(r"ต่ำสุด (\d+) K", text)[1])
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(p * cold / hot, rel=5e-3)
