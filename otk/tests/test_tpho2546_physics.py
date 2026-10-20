"""Pin TPhO 2 (2546) readings against the marking scheme and check draws."""

from fractions import Fraction
from math import pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2546_physics"
SHEET = load_sheet(SID)
# Marking-scheme formulas at each solver's constants (items 17-21 come from
# the experimental paper's theory parts with synthetic readings).
SOURCE_VALUES = {
    1: sqrt(2 * 10 * 0.5 * 5 * 0.5 / (4 + 0.75)),  # v^2 = 2gR(M+m)(1-cos)/(M+m sin^2)
    2: sqrt(2 * 10 * 0.5 * 5 * 0.5 / (4 + 0.75)) * 0.5 / 5,  # V = m v cos/(M+m)
    3: 0.01 / 2 * 0.25,  # (m/2M) cos^2
    4: "smaller",  # theta < cos^-1(2/3)
    5: 64,
    6: 100 * 11.5e-6 / (pi**2 * 1e-4 * 0.23 * 7.3),  # 0.70 C/s in the marking scheme
    7: 100 * 11.5e-6 / (pi**2 * 1e-4 * 0.23 * 7.3) - 2 * 1e-4 * 50 / (0.23 * 0.1 * 7.3),
    8: 25 + 100 * 11.5e-6 / (2 * 1e-4 * pi**2 * 1e-3),
    9: pi * 0.1 * sqrt(2 * 1e-4 * 0.1 * 300 / 11.5e-6),
    10: 0.5 * 0.01,  # xi d xi
    11: (1 - 0.16) / 2,
    12: 0.16 / 3,
    13: (1 - 0.16 / 3) / 2,
    14: (3 - 0.16) / 6 - 0.125 / (3 * 0.7),
    15: 0.4 / 3 - 0.125 / (3 * 0.49),
    16: (3 * (4 / 3 * pi * 0.125) / (16 * pi)) ** (1 / 3),  # r0^3 = 3q'/(16 pi rho)
    17: 12 / sqrt(2) / sqrt(1 + 0.75**2),
    18: sqrt(2e-9 / 0.02) / (100 * pi),
    19: 500 * 978 * 16 * 0.81 / (16 * pi**2 * 30),
    20: "sphere",
    21: 1.0,  # the hidden radius behind I = 1397.26 g cm^2
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def _metres(stem, label):
    return Fraction(re.search(label + r" = ([\d.]+) m", stem)[1])


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 21
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2546_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    expected = SOURCE_VALUES[item.number]
    got = mod.solve(**mod.PARAMS)
    if isinstance(expected, str):
        assert got == expected
    else:
        assert got == pytest.approx(expected, rel=1e-4)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_ball_potential_is_work_against_gauss_field():
    # V(r) = integral of the outside field from R out plus the inside field
    # from r to R, both exact in rational arithmetic (rho = eps0 = 1).
    for seed in range(60):
        q = generate("phys.tpho2546_q13", Random(seed))
        stem = q.stem[0].text
        radius, point = _metres(stem, "R"), _metres(stem, "r")
        outside = radius**3 / 3 / radius  # Q/(4 pi R) with Q = 4/3 pi R^3
        inside = (radius**2 - point**2) / 6  # integral of s/3 from r to R
        assert _rational(q.choices[q.answer].content[0].tex) == outside + inside


def test_generated_equilibrium_balances_forces():
    for seed in range(60):
        q = generate("phys.tpho2546_q16", Random(seed))
        size = int(re.search(r"ทรงกลมรัศมี (\d+) cm ที่มี", q.stem[0].text)[1])
        assert q.choices[q.answer].content[0].tex == rf"\frac{{{size}}}{{\sqrt[3]{{4}}}}"
        r0 = size / 4 ** (1 / 3)
        charge = 4 / 3 * pi * size**3
        assert r0 / 3 * charge == pytest.approx(charge**2 / (4 * pi * (2 * r0) ** 2))


def test_generated_black_box_follows_the_measured_inertias():
    for seed in range(60):
        q = generate("phys.tpho2546_q20", Random(seed))
        first, second = re.findall(r"([\d.]+) g·cm²", q.stem[0].text)
        answer = q.choices[q.answer].content[0].text
        assert answer.startswith("ทรงกลม") == (first == second)
