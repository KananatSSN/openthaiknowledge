"""Pin TPhO 7 (2551) readings against the marking scheme and check draws."""

from fractions import Fraction
from math import acos, asin, degrees, radians, sin, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2551_physics"
SHEET = load_sheet(SID)
_ALPHA = degrees(asin(sin(radians(60)) * 3 / 4))
# Marking-scheme values at each solver's constants (items 14-15 come from
# the experimental papers with synthetic readings).
SOURCE_VALUES = {
    1: 8,  # L' = R/(2n - 1) = 12 cm: 8 cm closer
    2: 180 - 4 * _ALPHA + 2 * 60,
    3: degrees(acos(sqrt((16 / 9 - 1) / 3))),
    4: sqrt(9 + 2 * 8 * (1 - 1 / 4)),  # v_B
    5: -4.0 / (2 * 0.5),  # -kqQ/(2R)
    6: sqrt(9 + 8),  # v_O
    7: sqrt(1 / 8) * acos(3 / sqrt(17)),
    8: 4.704,  # 3.1.2 (4.70 m/s^2)
    9: 4.704,  # 3.1.1 (4.70 N)
    10: 1.40,
    11: 7.00,
    12: 1.0789,  # 1.08 in the scheme
    13: 28.7706,  # 28.8 N
    14: 1000 * 9.8 * 2.0 / 0.1935,
    15: 1.43,
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 15
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2551_")
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


def test_generated_work_and_centre_speed_agree():
    # v_O^2 - v_B^2 = 2|W|/m with W = -kqQ/(2R): K/R from both items' forms.
    for seed in range(60):
        q = generate("phys.tpho2551_q05", Random(seed))
        stem = q.stem[0].text
        radius = Fraction(re.search(r"รัศมี ([\d.]+) m", stem)[1])
        product = Fraction(re.search(r"kqQ = ([\d.]+) J", stem)[1])
        assert _rational(q.choices[q.answer].content[0].tex) == -product / (2 * radius)


def test_generated_potentiometer_ratio():
    for seed in range(60):
        q = generate("phys.tpho2551_q15", Random(seed))
        standard, unknown = (int(x) for x in re.findall(r"(\d+) Ω", q.stem[0].text))
        assert _rational(q.choices[q.answer].content[0].tex) == Fraction(33, 20) * unknown / standard
