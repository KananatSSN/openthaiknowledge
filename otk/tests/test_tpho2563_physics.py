"""Pin TPhO 19 (2563) readings against the solutions and check draws."""

from math import pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2563_physics"
SHEET = load_sheet(SID)
G, C, PC = 6.67e-11, 3.00e8, 3.086e16
# Solution values at each solver's constants; the symbolic answers are
# evaluated from the solution's formulas.
SOURCE_VALUES = {
    1: sqrt(2 * 9.8 * 0.2) * 1e-3 / 0.051 * 1e2,  # u' = sqrt(2gh) dt/(T0 + dt)
    2: 9.8 * (1 / 51) ** 2 * 1e3,  # a' = g (dt/(T0 + dt))^2
    3: 0.1 * 1e-4 / (0.02**2 * 2 * pi / 10) * 1e3,  # A = d0 tau/(T0^2 w)
    4: 2 * (0.5 / 1.5) * (3 / 50) * 1e3,  # delta = 2((n - 1)/n)(a - x)/R
    5: 10e-3 * 1064e-9 * 1e-9 / (6.63e-34 * C),  # P lambda dt/(hc)
    6: 2 * 10e-3 / C * (0.5 / 1.5) * (3 / 50) * 1e12,
    7: sqrt(4 * 10e-3 * 0.5 / (2500 * 4 / 3 * pi * 5e-6**3 * C * 5e-6 * 1.5)),
    8: 5.95,  # C
    9: 9.78,  # K/km
    10: 1.44e3,  # m
    11: -1.7,  # C, read off the graph
    12: -5.2,  # C/km
    13: sqrt(4 * G * 3.55e41 / C**2 * 2360 * 940 / 3300 * 1e6 * PC) / (1e3 * PC),
    14: 1.05,  # arcsec, the ring the solution measures
    15: 3.55,  # 1e41 kg
    16: 0.53,
    17: 0.6205,  # least squares; the solution's hand-drawn line gives 0.57
    18: -0.385,  # least squares; the solution reads -0.1 +- 0.2 N by hand
    19: 0.042,  # m
    20: 0.34,
}
ROUGH = {3: 1e-2, 4: 1e-2, 6: 1e-2, 7: 1e-2, 8: 2e-3, 9: 1e-3, 10: 3e-3, 11: 1e-2, 12: 1e-2,
         14: 1e-3, 15: 2e-3, 16: 1e-2, 17: 1e-3, 19: 3e-3, 20: 2e-2}


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 20
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2563_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    rel = ROUGH.get(item.number, 1e-6)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=rel)


def _item(number):
    return solver_module(SHEET, SHEET.items[number - 1])


def test_summit_height_and_station_kelvin():
    # 2.7: z2 = 2.90e3 m at 70.0 kPa, and T1 = 279 K
    assert _item(10).solve(station=70.0) == pytest.approx(2.90e3, rel=2e-3)
    assert _item(8).solve() + 273.15 == pytest.approx(279, abs=0.5)


def test_moist_line_matches_the_solution_graph_reading():
    # the solution's line beta(T2) x 1e3 = -0.402 T2 + 2.65 meets the graph at
    # -1.7 C; our straight beta(T) with s = 0.349e-3 passes through that point
    t2 = _item(11).solve()
    beta = 6.0e-3 + 0.349e-3 * (t2 - 5.95)
    assert beta * 1e3 == pytest.approx(-0.402 * t2 + 2.65, abs=0.02)


def test_hand_drawn_stack_slope():
    # the solution's line through (0, -0.1) and (8, 6.8) gives mu = 0.57
    w0 = 2 * 38.4e-3 * 9.81
    assert (6.8 + 0.1) / 8 / (2 * w0) == pytest.approx(0.57, abs=5e-3)
    assert _item(17).solve() > 0.6


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_paper_friction():
    for seed in range(60):
        q = generate("phys.tpho2563_q16", Random(seed))
        text = q.stem[0].text
        nuts = int(re.search(r"จำนวน (\d+) ตัว", text).group(1))
        pulls = [float(t) for t in re.search(r"ได้ ([\d., ]+) N", text).group(1).split(", ")]
        expected = sum(pulls) / len(pulls) / (2 * nuts * 38.4e-3 * 9.81)
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(expected, rel=5e-3)
