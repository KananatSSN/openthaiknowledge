"""Pin TPhO 8 (2552) readings against the marking scheme and check draws."""

from fractions import Fraction
from math import sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2552_physics"
SHEET = load_sheet(SID)
# Marking-scheme values at each solver's constants (items 13-16 come from
# the experimental papers with synthetic readings).
SOURCE_VALUES = {
    1: 2.792 / 2.5,  # 1.12 m/s^2
    2: -7.2,  # 7.2 cm/s downward
    3: 1.76e11 * 0.01 * 0.1 * sqrt(3) / (2 * (1 + sqrt(3))),  # ~0.317 eBa/m
    4: sqrt((1 + 5 / sqrt(10)) ** 2 + 10),  # 4.08 m/s
    5: 9,
    6: 24.2857,  # 24.29 m/s
    7: 0.4847,  # 0.48 s in the scheme
    8: 0.9026,  # the scheme prints 0.82 m; its equations give 0.90 m
    9: (20e-6) ** 2 * 0.05 / (2 * 8.85e-12),
    10: (1000 / 0.008) ** 2 * 0.05 * 8.85e-12 / (2 * 0.002),
    11: sqrt(40 / 0.05 * (0.01 - 0.006) / 0.008),
    12: 4.0,  # D/3
    13: 5.5426,
    14: 5.0 / 5.5426,
    15: 672.0235,
    16: 9.3548,
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 16
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2552_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=1e-4)


def test_scheme_second_collision_height_is_a_slip():
    mod = solver_module(SHEET, SHEET.items[7])
    height = mod.solve(**mod.PARAMS)
    assert height == pytest.approx(0.90, abs=0.01)
    assert abs(height - 0.82) > 0.05


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_image_velocity_follows_the_lens():
    for seed in range(60):
        q = generate("phys.tpho2552_q02", Random(seed))
        focal, distance = (int(x) for x in re.findall(r"(\d+) cm", q.stem[0].text)[:2])
        speed = Fraction(re.search(r"ความเร็ว ([\d.]+) cm/s", q.stem[0].text)[1])
        image = 1 / (Fraction(1, focal) - Fraction(1, distance))
        assert _rational(q.choices[q.answer].content[0].tex) == -speed * image / distance


def test_generated_stability_limit_is_a_third():
    for seed in range(60):
        q = generate("phys.tpho2552_q12", Random(seed))
        gap = Fraction(re.search(r"ห่างแผ่นล่าง ([\d.]+) mm", q.stem[0].text)[1])
        assert _rational(q.choices[q.answer].content[0].tex) == gap / 3
