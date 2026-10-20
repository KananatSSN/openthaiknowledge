"""Pin TPhO 6 (2550) readings against the bound marking scheme and check draws."""

from fractions import Fraction
from math import log, pi
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2550_physics"
SHEET = load_sheet(SID)
S37, C37 = 0.6018150231520483, 0.7986355100472928  # sin, cos of 37 degrees
# Marking-scheme values at each solver's constants (items 13-16 come from
# the experimental papers with synthetic readings).
SOURCE_VALUES = {
    1: 1 / 4,  # L1/L2
    2: 5.0,  # R = (n - 1)(D - t)
    3: 1.0,  # x = (R/2 - t)/n
    4: 5 * (2**0.4 - 1) - 1,  # M'/M ~ 0.6
    5: 4 * 0.5 * 0.2,  # vBl
    6: 0.5 * 20 * 0.3**2 / 2,  # B omega l^2/2
    7: 20 * 0.5 * 0.2**2 / 4,  # omega B r0^2/(2R)
    8: 4 * 0.1 * 10 * 2 / (0.25 * 0.008),  # 4MgR/(B^2 r0^3)
    9: 5 * 10 * S37 - 0.4 * 3 * 10 * C37,
    10: 5 * 10 * S37 + 0.4 * 3 * 10 * C37,
    11: 10 * (8 - 5 * S37 - 0.2 * 3 * C37) / (3 + 3 + 8),
    12: 10 * (8 - 5 * S37 - 0.2 * 3 * C37) / 14 / (2 * 10 * C37),
    13: log(32.6 / 3.6) / (1 / 273.15 - 1 / 323.15),
    14: 4 * pi**2 / 0.8,
    15: 0.02 / 0.8,
    16: 3 * 40 * 0.25 / (4 * pi**2),
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 16
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2550_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=1e-4)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_bars_take_equal_times():
    for seed in range(60):
        q = generate("phys.tpho2550_q01", Random(seed))
        stem = q.stem[0].text
        y1, y2 = (Fraction(x) for x in re.search(r"เป็น ([\d/.]+) เท่าและ ([\d/.]+) เท่าของชนิดที่ 3 ความ", stem).groups())
        r1, r2 = (Fraction(x) for x in re.search(r"ความหนาแน่นเป็น ([\d/.]+) เท่าและ ([\d/.]+) เท่า", stem).groups())
        ratio = _rational(q.choices[q.answer].content[0].tex)
        # times squared stay rational: s = sqrt(rho/Y)
        s1, s2 = r1 / y1, r2 / y2
        # L1 sqrt(s1) + L2 sqrt(s2) = L1 + L2 with L2 = 1
        assert float(ratio) * float(s1) ** 0.5 + float(s2) ** 0.5 == pytest.approx(float(ratio) + 1)


def test_generated_rolling_friction_matches_the_acceleration_item():
    for seed in range(60):
        a = generate("phys.tpho2550_q11", Random(seed))
        mu = generate("phys.tpho2550_q12", Random(seed))
        assert a.stem[0].text.split(" ความเร่ง")[0] == mu.stem[0].text.split(" สัมประสิทธิ์ความเสียดทานสถิตระหว่างทรง")[0]
        cos_ = Fraction(4, 5) if "sin θ = 0.6" in a.stem[0].text else Fraction(3, 5)
        accel = _rational(a.choices[a.answer].content[0].tex)
        assert _rational(mu.choices[mu.answer].content[0].tex) == accel / (20 * cos_)
