"""Pin TPhO 11 (2555) readings against the solution and check draws."""

from math import sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2555_physics"
SHEET = load_sheet(SID)
EPS0, E, MP = 8.85e-12, 1.6e-19, 1.67e-27
FIELD = 1e-6 / EPS0
# Solution formulas at each solver's constants (items 14-18 come from the
# experimental papers with synthetic readings).
SOURCE_VALUES = {
    1: 0.5 + 200 * 0.0093,  # A = a + L theta (mm)
    2: 0.5 + 200 * 0.0093 + 2 * 1.22 * 550e-9 * 0.2 / 5e-4 * 1e3,
    3: sqrt(2.44 * 550e-9 * 0.2) * 1e3,  # a = sqrt(2.44 lambda L)
    4: 2 * 20.0,  # H = 2h
    5: sqrt(2 * 0.04 / 0.2),  # u0^2 = 2E0/m
    6: 0.5 * 2e-6 * 0.8**2 * 1e6,  # dE = dm v^2/2
    7: 2e-6 * 0.04 / (2 * 0.2) * 1e6,  # dE = dm E0/(2m)
    8: 10 * 5e-6 / 0.04,  # d(omega) = omega0 dE/E0
    9: 40 * 8 / 10,  # E = E0 omega1/omega0
    10: FIELD / 1e3,  # E = sigma/eps0
    11: 0.5 / 1.0,  # E_r/E = r/d
    12: E * 0.5e-3 * FIELD / (MP * 1e5),  # v_r = e r E/(m u)
    13: 3 * MP * (1e5) ** 2 / (2 * E * FIELD) * 1e3,  # s = 3 m u^2/(2 e E)
    14: 3.083661065427244,
    15: 548.8436842105266,
    16: 2.95252427184466,
    17: 0.40219110499370797,
    18: (1 / 72 + 1 / 12) / (1 / 12 + 1 / 6),
}


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 18
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2555_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=1e-9)


def test_energy_tracks_frequency_linearly():
    # 2 (e): y = 1, so halving omega halves the energy.
    mod = solver_module(SHEET, SHEET.items[8])
    assert mod.check(energy=10.0, omega=20.0, later=10.0) == pytest.approx(5.0, rel=1e-4)


def test_effective_mass_of_a_uniform_spring_is_a_third():
    mod = solver_module(SHEET, SHEET.items[17])
    assert mod.solve(top=7.0, bottom=7.0) == pytest.approx(1 / 3)
    assert 1 / 3 < mod.solve(top=15.0, bottom=5.0) < 1 / 2


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_pinhole_image_follows_the_geometry():
    for seed in range(60):
        q = generate("phys.tpho2555_q01", Random(seed))
        a, L = (float(x) for x in re.findall(r"([\d.]+) (?:mm|cm)", q.stem[0].text)[:2])
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(a + L * 10 * 0.0093, rel=5e-3)
