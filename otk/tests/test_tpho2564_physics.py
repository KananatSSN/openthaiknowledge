"""Pin TPhO 20 (2564) readings against the bound solutions and check draws."""

from math import asin, atan, cos, degrees, pi, radians, sin, sqrt, tan
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2564_physics"
SHEET = load_sheet(SID)
G, K = 9.81, 4 / (3 * pi)
EPS0, E, ME = 8.854e-12, 1.602e-19, 9.109e-31
T30, P40 = radians(30), radians(40)
KP = 0.5 * K / 1.5  # k' for m' = 1 kg, m = 0.5 kg
# Solution values at each solver's constants; the symbolic answers are
# evaluated from the solution's formulas.
SOURCE_VALUES = {
    1: G * sin(T30) * cos(P40) / 2,
    2: 0.5 * tan(T30) * sqrt(1 + 3 * sin(P40) ** 2),
    3: 1.5 / 2.5 * G * sin(T30),
    4: degrees(T30 - atan(1 / 2.5 * tan(T30))),
    5: degrees(asin(KP * sin(2.33))),  # theta0 = 2.33 rad
    6: (1 + (0.75 - K) * 0.5) * 0.01 * 400,
    7: sqrt(((1 + (0.75 - K) * 0.5) * 0.01 * 400 - 2 * 1.5 * G * KP * 0.1) / ((1 + (0.75 + K) * 0.5) * 0.01)),
    8: None,  # from 7 below
    9: sqrt(2 * E * 5e-3 * 100 / (ME * 1e-2) + 1e10) / 1e3,
    10: 4 * EPS0 * 0.05**2 / (9 * 0.01**2) * sqrt(2 * E / ME) * 100**1.5 * 1e3,
    11: 100 * 0.5 ** (4 / 3),
    12: -4 / 3 * EPS0 * 0.05**2 * 100 / 0.01 * 1e9,
    13: 4 / 3 * EPS0 * 100 / 0.01 * 1e9,
    14: 2668.0,  # Pa (the solution's f)
    15: 2.7,  # J
    16: 30.9,  # kcal/day
    17: 22.1,  # J
    18: 24.8,  # J
    19: 32.6,  # the solution's w_O = -1.94 J; 31.0 at alpha_O = 3.35 L
    20: 60.0,  # cm
    21: 3.0,  # mm
    22: 780.0,  # cm
    23: 0.12,  # mm
    24: 162.5,
    25: 60.0,  # GPa
    26: 62.0,  # GPa from the solution's drawn line; least squares 60.5
    27: -12.31,  # %
    28: 75.8,  # GPa
    29: 0.33,
}
SOURCE_VALUES[8] = 1.5 * (G - KP * 0.1 * SOURCE_VALUES[7] ** 2)
ROUGH = {5: 2e-3, 14: 6e-3, 15: 5e-3, 16: 2e-3, 17: 5e-3, 18: 5e-3, 19: 6e-2, 25: 3e-3,
         26: 3e-2, 27: 1e-3, 28: 2e-3, 29: 2e-2}


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 29
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2564_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    rel = ROUGH.get(item.number, 1e-6)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=rel)


def _item(number):
    return solver_module(SHEET, SHEET.items[number - 1])


def test_anode_charge_balances_space_charge():
    # 2 g): sigma+ is positive; the solution's first method writes it negative
    sigma = _item(13).solve()
    charge = _item(12).solve()
    assert sigma > 0 > charge
    assert sigma * 0.05**2 == pytest.approx(-charge)


def test_exhale_work_sensitivity():
    # 3.1 h): the solution's w_O = -1.94 J needs alpha_O near 3.335 L; at the
    # tabulated 3.35 L it is -1.91 J
    lung = _item(15)
    assert lung.solve(alpha=3.35, k=1.644) == pytest.approx(1.906, abs=2e-3)
    assert lung.solve(alpha=3.335, k=1.644) == pytest.approx(1.94, abs=5e-3)


def test_turn_root_and_linear_range():
    # theta0 = tan(theta0/2) is 2.33 rad; for L = 90 cm |e_N| first exceeds 10% at N = 4
    from otk.sheets.tpho2564_physics._shared import bisect

    root = bisect(lambda x: x - tan(x / 2), 2.0, 3.0)
    assert root == pytest.approx(2.33, abs=5e-3)
    slip = _item(27)
    assert abs(slip.solve(washers=3)) <= 10 < abs(slip.solve(washers=4))


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_bilens_range():
    for seed in range(60):
        q = generate("phys.tpho2564_q22", Random(seed))
        text = q.stem[0].text
        height, focal, cut = re.search(r"สูง (\d+) mm ความยาวโฟกัส (\d+) cm ที่ตัดส่วนกลางสูง ([\d.]+) mm", text).groups()
        expected = float(focal) * (float(height) - float(cut)) / float(cut)
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(expected, rel=5e-3)
