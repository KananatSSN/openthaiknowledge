"""Pin TPhO 12 (2556) readings and check draws.

The folder has no theory solution: theory values are the derived formulas
at each solver's constants; lab values come from the experiment solution."""

from math import exp, log, pi, radians, sin
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2556_physics"
SHEET = load_sheet(SID)
A_METEOR = 1.2 * pi / (2 * 10000 * 1.25e-4 * sin(radians(45)))
SOURCE_VALUES = {
    1: 2.0 * (1 - 0.75 * 0.25),  # u (1 - 3/4 cos^2 60)
    2: 3 * 2.0 * 0.5 / (2 * 0.5),  # 3u cos(theta)/(2l)
    3: 1.5 * 0.4 * 2.0 * (1 + 0.75),  # (3/2) m u (1 + sin^2 theta)
    4: 0.5 * 0.1 * 15e3**2 * pi * 0.25,
    5: 0.5 * 0.1 * 15e3**2 * pi * 0.25 / 1500,
    6: -A_METEOR,
    7: log(3 * A_METEOR) * 8.0,
    8: 1.2 * 20e3**2 * exp(-2 / 3) / (6 * A_METEOR) / 1e6,
    9: 5 * 9.8 / 50e-4 / 1e3,  # mg/a
    10: 5 * 9.8 / 2000 * 100 * 50,  # mga/k in cm^3
    11: 49**2 * 2.4 / (2 * 1.4 * 2000),
    12: 49**2 / (2 * 2000),
    13: 49**2 / (2 * 1.4 * 2000),
    14: 300 * 7 / 6,  # T_B/T_A = 2 gamma/(gamma + 1)
    15: 59.58,
    16: 42.52,
    17: 50.10,
    18: 3.0,  # the solution's mu (A m^2)
    19: 12.1,  # 0.46/0.0381 in the solution
    20: 0.133,  # gauss; the solution prints 0.13 T
    21: 17.9,  # the solution's inclination (degrees)
}
ROUGH = {15: 1e-4, 16: 1e-4, 17: 1e-4, 18: 5e-3, 19: 5e-3, 20: 5e-3, 21: 5e-3}


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 21
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2556_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    rel = ROUGH.get(item.number, 1e-9)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=rel)


def test_vertical_field_is_in_gauss_not_tesla():
    # The solution's numbers give 0.133 G = 1.33e-5 T; its "0.13 T" is a unit slip.
    bv = solver_module(SHEET, SHEET.items[19]).solve()
    assert bv * 1e-4 == pytest.approx(1.33e-5, rel=5e-3)
    assert bv * 1e-4 < 1e-3


def test_rods_reduce_to_rigid_motion_when_perpendicular():
    vy = solver_module(SHEET, SHEET.items[0])
    jerk = solver_module(SHEET, SHEET.items[2])
    assert vy.check(angle=90.0, speed=3.0) == pytest.approx(3.0)
    assert jerk.check(mass=1.0, speed=1.0, angle=90.0) == pytest.approx(3.0)
    assert jerk.check(mass=1.0, speed=1.0, angle=0.0) == pytest.approx(1.5)


def test_bows_leave_a_dark_band():
    primary = solver_module(SHEET, SHEET.items[15]).solve(index=1.33)
    secondary = solver_module(SHEET, SHEET.items[16]).solve(index=1.33)
    assert primary < secondary


def test_meteor_speed_matches_the_closed_form():
    from otk.sheets.tpho2556_physics._meteor import speed_at

    z = 15e3
    v = speed_at(z, 1.0, 1.0, 10000.0, radians(45), 20e3)
    assert v == pytest.approx(20e3 * exp(-A_METEOR * exp(-1.25e-4 * z)), rel=1e-9)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_valve_temperature_follows_gamma():
    for seed in range(60):
        q = generate("phys.tpho2556_q14", Random(seed))
        text = q.stem[0].text
        gamma = {"1.4": 1.4, "5/3": 5 / 3, "1.3": 1.3}[re.search(r"γ = ([\d./]+)\)", text)[1]]
        temp = int(re.search(r"อุณหภูมิคงตัว (\d+) K", text)[1])
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(temp * 2 * gamma / (gamma + 1), rel=5e-3)
