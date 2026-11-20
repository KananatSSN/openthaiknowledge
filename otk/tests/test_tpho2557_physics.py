"""Pin TPhO 13 (2557) readings against the solutions and check draws."""

from math import sqrt, tan
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.sheets.tpho2557_physics._shared import line
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2557_physics"
SHEET = load_sheet(SID)
# Solution formulas at each solver's constants (items 13-17 come from the
# experimental paper; 13 uses the solution's own table).
SOURCE_VALUES = {
    1: 550e-9 / (2 * 1.5 * tan(2e-3)) * 1e3,  # lambda/(2 n tan theta)
    2: 550e-9 * 10 / (2 * 1.5 * 0.10 * 50 * tan(20e-3)) * 1e6,
    3: 500 * 340**2 / (340**2 - 100**2) - 500,  # f0 v^2/(v^2 - u^2) - f0
    4: 50 * sqrt(100**2 + 340**2) / 340,  # L sqrt(u^2 + v^2)/v
    5: 2.0**2 * (1.0 - 0.3 * 0.6) / (1.0 * 9.8 * 0.3),
    6: 1.0 / (2 * 0.6),  # w/(2h)
    7: 1.0 * 0.5 / (0.6 * 2.5),  # w(n - 1)/(h(n + 1))
    8: 1000 * 1480 * sqrt(2 * 9.8 * 2.0) / 1e6,  # rho v u
    9: sqrt(2.2e9 / 1000),  # sqrt(B/rho)
    10: 1480 * sqrt(2 * 9.8 * 2.0) / 9.8 + 2 * 2.0,  # vu/g + 2 h0
    11: 2.0 * 0.5 * (1 - 1 / 4),  # vB(1 - 1/eps_r)
    12: 2.0 * 0.5 * 2.0 * (1 - 1 / 4),  # vBd(1 - 1/eps_r), mV
    13: 0.294,  # the solution's B
    14: 0.4961968776737271,
    15: 0.2000725469532395,
    16: 3.1,  # the solution's sigma, 1e7 S/m
    17: 0.48,  # the solution's k
}
ROUGH = {13: 1e-3, 16: 5e-3, 17: 5e-3}


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 17
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2557_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    rel = ROUGH.get(item.number, 1e-9)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=rel)


def test_solution_terminal_speed_columns():
    # The solution's v/cos and tan columns give slope 0.366 and intercept
    # -0.0666, so b = 0.466 kg/s and mu = 0.18 (its sin column implies a
    # 0.75 m incline rather than the stated 0.70 m).
    tans = [0.334, 0.353, 0.374, 0.394, 0.415, 0.436, 0.458]
    ratio = [0.057, 0.063, 0.070, 0.076, 0.085, 0.094, 0.102]
    slope, intercept = line(tans, ratio)
    assert slope == pytest.approx(0.366, abs=1e-3)
    assert 0.0174 * 9.8 / slope == pytest.approx(0.466, abs=2e-3)
    assert -intercept / slope == pytest.approx(0.18, abs=5e-3)


def test_table_tips_exactly_at_the_limit():
    from otk.sheets.tpho2557_physics._shared import table

    assert table(1.0, 0.6, 1.0 / 1.2, True)[2] == pytest.approx(0.0, abs=1e-12)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_tipping_limit_follows_the_table():
    for seed in range(60):
        q = generate("phys.tpho2557_q06", Random(seed))
        w, h = (float(x) for x in re.findall(r"([\d.]+) m", q.stem[0].text)[:2])
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(w / (2 * h), rel=5e-3)
