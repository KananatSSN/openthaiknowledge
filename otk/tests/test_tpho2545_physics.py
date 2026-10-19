"""Pin TPhO 1 (2545) readings against the official solution and check draws."""

from fractions import Fraction
from math import exp, log, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2545_physics"
SHEET = load_sheet(SID)
# Official-solution values at each solver's constants (items 15-17 come from
# the experimental paper's theory parts with synthetic readings).
SOURCE_VALUES = {
    1: 1.1,  # metres from the wall
    2: 0.4,  # v0 L B
    3: 4 * exp(-2),
    4: 10,  # (a + b)/2
    5: sqrt(10 * 10 * 0.9 * 0.5 / (7 * 0.01)),
    6: 2 * sqrt(1 - 0.48**2),
    7: -6,  # -M g (r + (R - r) cos 60)
    8: 2.88,  # M (R - r)^2 w^2
    9: -6.25,
    10: 2 * sqrt(0.08),  # T / pi
    11: 2 * sqrt(0.1),
    12: "left",
    13: 1.2 / (1200 * 9.8 * 0.01),
    14: 13.8298,  # 13.8 W in the official solution
    15: 30 + 60 * exp(-1),
    16: 600 / log(2),
    17: 30e-4 * (0.5 / 40) / 1.22 * 1e7,
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 17
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2545_")
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


def test_generated_spring_keeps_the_centre_of_mass():
    for seed in range(60):
        q = generate("phys.tpho2545_q01", Random(seed))
        stem = q.stem[0].text
        near, far = map(int, re.findall(r"(\d+) kg", stem))
        length, gap, later = (Fraction(x) for x in re.findall(r"([\d.]+) m", stem))
        a_now = _rational(q.choices[q.answer].content[0].tex)
        before = (near * gap + far * (gap + length)) / (near + far)
        after = (near * a_now + far * (a_now + later)) / (near + far)
        assert before == after


def test_generated_equal_images_have_equal_magnifications():
    for seed in range(60):
        q = generate("phys.tpho2545_q04", Random(seed))
        near, far = map(int, re.findall(r"(\d+) cm", q.stem[0].text))
        f = _rational(q.choices[q.answer].content[0].tex)
        assert near < f < far
        assert f / (f - near) == f / (far - f)


def test_generated_lever_level_balances_pressure():
    for seed in range(60):
        q = generate("phys.tpho2545_q13", Random(seed))
        stem = q.stem[0].text
        width = Fraction(re.search(r"b = ([\d.]+) cm", stem)[1]) / 100
        density = int(re.search(r"ความหนาแน่น (\d+)", stem)[1])
        current = Fraction(re.search(r"กระแส ([\d.]+) A", stem)[1])
        field = Fraction(re.search(r"สนามแม่เหล็ก ([\d.]+) T", stem)[1])
        level = _rational(q.choices[q.answer].content[0].tex) / 100
        assert density * 10 * level * width == current * field
