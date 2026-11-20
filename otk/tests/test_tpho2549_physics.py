"""Pin TPhO 5 (2549) readings against the bound marking scheme and check draws."""

from fractions import Fraction
from math import pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2549_physics"
SHEET = load_sheet(SID)
E, ME, EPS0, C = 1.6e-19, 9.1e-31, 8.85e-12, 3.0e8
# Marking-scheme formulas at each solver's constants (items 12-14 come from
# the experimental paper with synthetic readings).
SOURCE_VALUES = {
    1: 20 * 15 / 5 + 5,  # f(f - L)/L + L
    2: 0.75 / 3,  # mu >= tan(theta)/3 for a cylinder
    3: 2.7,  # h = 2.7R
    4: 0.2 * 10 * 17 / 7,  # N = (17/7) mg at h = 2.7R
    5: 14.13,  # h = L/2 + Pa/(rho g)
    6: 1.3949,  # extra air 1.39 x the original
    7: 40e3,  # rho L A
    8: sqrt(E * E / (4 * pi * EPS0 * ME * (0.1e-9) ** 3)),
    # The scheme prints ~0.28 nm; its formula with the paper's constants:
    9: (E * E / (4 * pi * EPS0 * ME * (2 * pi * C / 656e-9) ** 2)) ** (1 / 3) * 1e9,
    10: 0.2 / 2,  # (e/(4Q))^(1/3) R with Q = 2e
    11: sqrt(3 * 2 * E * E / (4 * pi * EPS0 * ME * (0.2e-9) ** 3)) / (2 * pi),
    12: 1.50942,
    13: 50,
    14: 0.8,
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 14
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2549_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=1e-4)


def test_scheme_radius_does_not_follow_from_its_formula():
    mod = solver_module(SHEET, SHEET.items[8])
    assert mod.solve(wavelength=656) == pytest.approx(0.313, abs=0.001)
    assert abs(mod.solve(wavelength=656) - 0.28) > 0.02


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_steelyard_balances_torques():
    for seed in range(60):
        q = generate("phys.tpho2549_q13", Random(seed))
        stem = q.stem[0].text
        hook = Fraction(re.search(r"จุดหมุน ([\d.]+) cm ตุ้ม", stem)[1])
        slider = int(re.search(r"ตุ้มเลื่อนมวล (\d+) g", stem)[1])
        zero, mark = (int(x) for x in re.findall(r"อยู่ห่างจุดหมุน (\d+) cm", stem))
        m = _rational(q.choices[q.answer].content[0].tex)
        # beam torque fixed by the empty balance: B b = -M x0
        assert -slider * zero + slider * mark - m * hook == 0


def test_generated_lens_pair_focus_traces_a_ray():
    for seed in range(60):
        q = generate("phys.tpho2549_q01", Random(seed))
        focal, gap = (int(x) for x in re.findall(r"(\d+) cm", q.stem[0].text))
        h, angle = Fraction(1), Fraction(0)
        angle -= h / focal
        h += gap * angle
        angle += h / focal
        assert _rational(q.choices[q.answer].content[0].tex) == gap - h / angle
