"""Pin TPhO 21 (2565) readings against the bound solutions and check draws."""

from math import cos, log, pi, radians, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2565_physics"
SHEET = load_sheet(SID)
K = 1 / (4 * pi * 8.854e-12)
P = 1e-9  # dipole moment at the solvers' constants (C m)
MU, KB = 9.274e-24, 1.38e-23
BETA = sqrt(2 * K * P * 1e-6 / (1e-3 * 0.05**4))
GAMMA_FLOW = 2 * 1.4 / 0.4 * (0.7 ** (2 / 1.4) - 0.7 ** (1 + 1 / 1.4))
STAR = (2 / 2.4) ** 3.5
# Solution values at each solver's constants; the symbolic answers are
# evaluated from the solution's formulas.
SOURCE_VALUES = {
    1: 2 * K * P / 0.05**3,
    2: K * P * sqrt(1 + 3 * cos(radians(60)) ** 2) / 0.05**3,
    3: sqrt(K * 4 / (3 * sqrt(3)) * P * 1e-6 * 1e-3) * 1e5,
    4: sqrt(2 * K * P * 1e-6 / (1e-3 * 0.05**2)),
    5: 10.3 / BETA,  # the solution's coefficient; the approximation gives 10.44
    6: 0.6,
    7: 0.5,
    8: 1e23 * MU**2 / (KB * 300),
    9: 2 * 1e-7 * MU / 1e-27 * 1e3,  # mT; the solution rounds to 2 mT
    10: 2.0,  # mK
    11: 2.53,  # 1e-24 J; the solution rounds to 3
    12: (200e3 - 0.05**2 / (2 * 2.32 * 1e-8)) / 1e3,
    13: 300 / (1 + 0.2 * 0.64),
    14: 200 * (1 + 0.2 * 0.64) ** -3.5,
    15: sqrt(200e3 * 2.32 * 1e-8 * GAMMA_FLOW) * 1e3,
    16: 200 * STAR,
    17: 1e-4 * sqrt(200e3 * 2.32 * 2 * 1.4 / 0.4 * (STAR ** (2 / 1.4) - STAR ** (1 + 1 / 1.4))) * 1e3,
    18: -2.86,  # the solution's drawn line; least squares -2.90
    19: 1.08,  # 1e6 A/m by least squares; the drawn line gives 1.2
    20: 26.9,  # mT
    21: 0.98,  # 1e6 A/m
    22: 8.90,  # 1e-5 Wb
}
ROUGH = {5: 2e-2, 6: 3e-2, 7: 3e-2, 11: 2e-3, 18: 2e-2, 19: 5e-3, 20: 2e-3, 21: 3e-3, 22: 1e-3}


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 22
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2565_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    rel = ROUGH.get(item.number, 1e-6)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=rel)


def _item(number):
    return solver_module(SHEET, SHEET.items[number - 1])


def test_swing_period_coefficient():
    # 1 g): the paper's approximation gives 10.44/beta (the solution writes
    # 10.3); the exact integral gives 10.49/beta
    period = _item(5)
    assert period.solve() * BETA == pytest.approx(10.44, abs=5e-3)
    assert period.check() * BETA == pytest.approx(10.49, abs=5e-3)


def test_cooling_roundings():
    # 2 i), k): 1.85 mT and 2.5e-24 J, rounded in the solution to 2 mT and 3e-24 J
    assert round(_item(9).solve()) == 2
    assert round(_item(11).solve()) == 3
    assert _item(7).solve(field=0.0) == pytest.approx(log(2))


def test_hand_drawn_axis_line():
    # 1 d): the solution's drawn line (n = -2.86, x0 = 36.3 mm) gives m = 0.38 A m^2
    n, x0 = -2.86, 36.3
    moment = 1000**n / 1000 * 2 * pi / (4e-7 * pi) / x0**n
    assert moment == pytest.approx(0.38, abs=5e-3)
    assert moment / (pi * 25e-6 * 4e-3) / 1e6 == pytest.approx(1.2, abs=0.05)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_critical_pressure():
    for seed in range(60):
        q = generate("phys.tpho2565_q16", Random(seed))
        text = q.stem[0].text
        gamma = re.search(r"γ = ([\d./]+)", text).group(1)
        gamma = 5 / 3 if gamma == "5/3" else float(gamma)
        pressure = float(re.search(r"ความดัน (\d+) kPa", text).group(1))
        expected = pressure * (2 / (gamma + 1)) ** (gamma / (gamma - 1))
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(expected, rel=5e-3)
