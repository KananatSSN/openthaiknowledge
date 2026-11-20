"""Pin TPhO 10 (2554) readings against the bound solution and check draws."""

from math import acos, cos, pi, radians, sin, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2554_physics"
SHEET = load_sheet(SID)
B0, ALPHA, BETA, R, L, M, G = 0.010, 2.0, 32.0, 0.005, 1.3e-8, 50e-6, 9.8
K = 2 * B0**2 * ALPHA * BETA * pi**2 * R**4 / L
BETA_SLIDE = acos(2 * cos(radians(30)) / 3)
# Solution formulas at each solver's constants (items 17-20 come from the
# experimental papers with synthetic readings).
SOURCE_VALUES = {
    1: pi * R**2 * ALPHA * B0 * 0.05 / L,
    2: K,
    3: M * G / K,
    4: sqrt(K / M),
    5: 19.5,  # the solution's I_max
    6: 0.25 * sin(radians(30)) * 2 - 2 / 3 * 0.5 * sin(radians(38.3)),
    7: 3 * G / cos(radians(30)),
    8: (2 / 3, 1.0, -1.0, 1.0),
    9: 2.0 * sqrt(1.5),
    10: 54.7356103172,
    11: 2 * sin(BETA_SLIDE) * (0.5 + sin(BETA_SLIDE)) / (0.5 * (2 * (0.5 + sin(BETA_SLIDE)) + sin(BETA_SLIDE))),
    12: 1.33,  # the solution's R1 in mm
    13: 0.072 / 1e-3,
    14: 13.2,  # micrometres; the solution's simplified form gives 13.4
    15: 8.42,  # cm; the solution prints 0.84 m
    16: 1.5 * 1.33,
    17: 0.65,
    18: 1200.0,
    19: 0.399,
    20: 0.40 / 1.3070,
}
ROUGH = {5: 1e-2, 12: 5e-3, 14: 5e-3, 15: 1e-3, 20: 1e-3}


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 20
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2554_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    rel = ROUGH.get(item.number, 1e-4)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=rel)


def test_solution_slips_are_pinned():
    # 3.5: the bound solution's 1.34e-5 m is its simplified form; the full
    # first-order correction is 1.32e-5 m.
    R0, v0, h, gamma, rho = 0.005, 0.10, 0.10, 0.072, 1000.0
    R1 = R0 * (1 + 2 * G * h / v0**2) ** -0.25
    simplified = gamma * (1 - R1 / R0) / (2 * rho * (v0**2 + 2 * G * h))
    assert simplified == pytest.approx(1.34e-5, rel=5e-3)
    # 3.6: t = 0.12 s gives 0.084 m, not the printed 0.84 m.
    t = 2.91 * sqrt(rho * R0**3 / gamma)
    assert t == pytest.approx(0.12, abs=5e-3)
    assert v0 * t + G * t * t / 2 == pytest.approx(0.084, abs=5e-4)
    # 1.6: the peak is at twice the equilibrium depth.
    z0 = M * G / K
    assert pi * R**2 * ALPHA * B0 * 2 * z0 / L == pytest.approx(19.5, rel=1e-3)


def test_jet_correction_tracks_the_exact_root():
    mod = solver_module(SHEET, SHEET.items[13])
    for h in (0.05, 0.10, 0.20):
        R0, v0, k = 0.005, 0.10, 2 * 0.072 / 1000
        R1 = R0 * (1 + 2 * G * h / v0**2) ** -0.25

        def residual(r):
            return R0**4 / r**4 * v0**2 + k / r - 2 * G * h - v0**2 - k / R0

        lo, hi = R1, 1.5 * R1
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if residual(mid) > 0 else (lo, mid)
        assert mod.solve(height=h) == pytest.approx((lo - R1) * 1e6, rel=0.05)


def test_drop_length_is_half_of_plateau_rayleigh():
    # Volume and side area kept: L = 9R/2, about half of 9.1R.
    r = solver_module(SHEET, SHEET.items[15]).solve(radius=1.0)
    length = 4 * r**3 / 3
    assert length == pytest.approx(4.5)
    assert 2 * pi * length == pytest.approx(4 * pi * r * r)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_diode_threshold_follows_the_two_branches():
    for seed in range(60):
        q = generate("phys.tpho2554_q17", Random(seed))
        forward, reverse = (float(x) for x in re.findall(r"([\d.]+) V", q.stem[0].text)[:2])
        each = (forward + reverse) / 5
        assert any(abs(forward - n * each) < 0.011 and abs(reverse - (5 - n) * each) < 0.011 for n in range(1, 5))
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(each, abs=6e-4)
