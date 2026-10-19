"""Pin source readings and check generated physics beyond solver agreement."""

from fractions import Fraction
from math import sqrt, pi
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "posn2562_physics"
SHEET = load_sheet(SID)
SOURCE_VALUES = {
    1: (1, 1),
    2: Fraction(1, 10),
    3: 10,
    4: sqrt(100 / 0.96),
    5: 1,
    6: sqrt(50),
    7: 80,
    8: sqrt(1.0016),
    9: Fraction(1, 4),
    10: Fraction(27, 10),
    11: Fraction(1, 8),
    12: 50 / sqrt(3),
    13: 0,
    14: 1,
    15: 30,
    16: 4,
    17: 12,
    18: -24,
    19: sqrt(15),
    20: 12,
    21: 3,
    22: 60,
    23: 6 * sqrt(3),
    24: pi / sqrt(10),
    25: 3 / (13 * sqrt(13)),
    26: (1, 2 * sqrt(3)),
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 26
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.posn2562_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number])


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_steady_temperature_has_equal_heat_fluxes():
    for seed in range(60):
        q = generate("phys.posn2562_q07", Random(seed))
        stem = q.stem[0].text
        hot, cold = map(Fraction, re.findall(r"คงที่ (\d+) °C", stem))
        distance = Fraction(re.search(r"ระยะ ([\d.]+)L", stem)[1])
        temperature = _rational(q.choices[q.answer].content[0].tex)
        assert (hot - temperature) / distance == (temperature - cold) / (1 - distance)


def test_generated_virtual_magnification_satisfies_signed_lens_equation():
    for seed in range(60):
        q = generate("phys.posn2562_q10", Random(seed))
        stem = q.stem[0].text
        focal = Fraction(re.search(r"โฟกัส (\d+) cm", stem)[1])
        distance = Fraction(re.search(r"เลนส์ (\d+) cm", stem)[1])
        magnification = _rational(q.choices[q.answer].content[0].tex)
        u = distance / magnification
        assert 0 < u < focal
        assert 1 / u - 1 / distance == 1 / focal


def test_generated_opposed_batteries_obey_kcl():
    for seed in range(60):
        q = generate("phys.posn2562_q13", Random(seed))
        stem = q.stem[0].text
        middle = int(re.search(r"r=(\d+) Ω", stem)[1])
        resistors = list(map(int, re.findall(r"ตัวต้านทาน (\d+) Ω", stem)))
        left = int(re.search(r"อุดมคติ (\d+) V", stem)[1])
        right = int(re.search(r"แบตเตอรี่ (\d+) V", stem)[1])
        current = _rational(q.choices[q.answer].content[0].tex)
        node = current * middle
        assert resistors[0] == resistors[1]
        assert (left - node) / resistors[0] + (-right - node) / resistors[1] == current


def _squared_positive_radical(tex):
    fraction = re.fullmatch(r"\\frac\{(.+)\}\{(\d+)\}", tex)
    body, denominator = (fraction[1], int(fraction[2])) if fraction else (tex, 1)
    radical = re.fullmatch(r"(\d*)\\sqrt\{(\d+)\}", body)
    if radical:
        return Fraction(int(radical[1] or 1) ** 2 * int(radical[2]), denominator**2)
    return Fraction(body) ** 2 / denominator**2


def test_ring_generator_keeps_the_exact_radical_from_its_geometry():
    for seed in range(60):
        q = generate("phys.posn2562_q25", Random(seed))
        stem = q.stem[0].text
        radius = int(re.search(r"รัศมี (\d+) m", stem)[1])
        distance = int(re.search(r"ทางบวก (\d+) m", stem)[1])
        actual = _squared_positive_radical(q.choices[q.answer].content[0].tex)
        # Coulomb field: total normalized charge R/2 and axial projection x/r.
        separation_squared = radius**2 + distance**2
        assert actual == Fraction(radius**2 * distance**2, 4 * separation_squared**3)


def test_generated_collision_pair_conserves_momentum_and_energy():
    for seed in range(60):
        q = generate("phys.posn2562_q26", Random(seed))
        speed = int(re.search(r"วิ่งด้วย (\d+) m/s", q.stem[0].text)[1])
        pair = q.choices[q.answer].content[0].tex.removeprefix(r"\left(").removesuffix(r"\right)")
        first, second = pair.split(r",\ ")
        rebound = _rational(first)
        target_squared = _squared_positive_radical(second)
        assert speed**2 == rebound**2 + 2 * target_squared
        assert (speed + rebound) ** 2 == 3 * target_squared
