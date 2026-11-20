"""Pin TPhO 17 (2561) readings against the solution and check draws."""

from math import pi, radians, sqrt, tan
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2561_physics"
SHEET = load_sheet(SID)
H, E = 6.626069e-34, 1.602177e-19
# Solution values at each solver's constants (lab items are derived here:
# the folder has no lab solution).
SOURCE_VALUES = {
    1: 2 * 9 * 0.5 / 9.8,  # L = 2 v^2 sin(theta0)/g
    2: 6 * 0.1 * 3.0 / (2.0 * 1.0),  # omega = 6 m v/(M L)
    3: radians(30) * tan(radians(30)) / 3,
    4: 5.50871675,
    5: 6.24,  # days
    6: 3 * 0.75 / (1 + 3 * 0.75),
    7: 6 * 0.75 / (1 + 3 * 0.75),
    8: 0.081,  # T
    9: 1.0,  # kg
    10: 1.0,  # kg
    11: 0.5 * 70e9 * H / E * 1e6,
    12: H / E**2 / 1e3,  # von Klitzing constant, kOhm
    13: 1.81,  # 1e-8
    14: 1.2 * 340 * 0.05,
    15: sqrt(1.4 * 101325 / 1.2),
    16: 1.2 * 0.05**2 / 4 * 1e3,
    17: 1.2 * 0.05**2 / (2 * 340) * 1e6,
    18: 20.0**2 / (4 * 1.2 * 340**2) * 1e3,
    19: 2.9,  # mN/m^2 at 120 dB
    20: 29.054604099,
    21: 72.2702776259925,
    22: 0.58,
}
ROUGH = {5: 1e-3, 8: 1e-3, 9: 1e-3, 10: 1e-3, 13: 1e-3, 19: 1e-2}


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 22
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2561_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    rel = ROUGH.get(item.number, 1e-9)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=rel)


def test_strings_go_slack_beyond_54_7_degrees():
    end = solver_module(SHEET, SHEET.items[6])
    assert end.solve(angle=54.7356103172) == pytest.approx(1.0)
    assert end.solve(angle=60.0) < 1.0 < end.solve(angle=50.0)


def test_lab_linearisation_coefficient():
    # The paper's 0.508 differs from the tangent of its own x_cm(eta)/R at
    # eta = 0, which is 16/(3 pi^2) = 0.540.
    from math import acos

    def xcm(eta):
        return 2 / 3 * (1 - eta * eta) ** 1.5 / (acos(eta) - eta * sqrt(1 - eta * eta))

    h = 1e-6
    tangent = (xcm(h) - xcm(-h)) / (2 * h)
    assert tangent == pytest.approx(16 / (3 * pi**2), rel=1e-6)
    assert tangent == pytest.approx(0.540, abs=1e-3)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_heap_angle():
    from math import atan, degrees

    for seed in range(60):
        q = generate("phys.tpho2561_q20", Random(seed))
        h, r = (float(x) for x in re.findall(r"([\d.]+) cm", q.stem[0].text)[:2])
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(degrees(atan(h / r)), rel=5e-3)
