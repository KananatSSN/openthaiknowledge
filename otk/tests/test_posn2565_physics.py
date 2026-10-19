"""Pin source readings and check generated physics beyond solver agreement."""

from fractions import Fraction
from math import pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "posn2565_physics"
SHEET = load_sheet(SID)
# The printed answer of each item, evaluated at the solver's source constants.
SOURCE_VALUES = {
    1: (1, 2, -2),  # joule
    2: 1,  # E/(4R) with E = 4 V, R = 1 ohm
    3: Fraction(1, 3),
    4: 300,  # kQ(1/R1 - 1/R2), 2 nC, 3 cm, 6 cm
    5: 50,  # Mg/(2 sin), 6 kg, sin = 0.6
    6: Fraction(5, 2),
    7: sqrt(5),
    8: 40,  # Mg cot, 3 kg, sin = 0.6
    9: 5 * sqrt(3),
    10: 40,
    11: Fraction(35, 2),
    12: 2,  # one tau with R = 10 m
    13: "BC",
    14: 373 / 18 * 8.314 / 1.01325e5 * 1e6,
    15: 4,
    16: 2,
    17: 2 * pi * 0.05 * 0.2 / 0.001,
    18: 2,  # 1/mu
    19: 40,
    20: 2,
    21: 20,
    22: Fraction(7, 5),
    23: 3,
    24: Fraction(1, 25),
    25: 10,
    26: 24000,
    27: Fraction(1, 200),
    28: 20,
    29: 12 / pi,
    30: Fraction(4, 5),
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def _answer(key, seed):
    q = generate(key, Random(seed))
    return q.stem[0].text, q.choices[q.answer].content[0].tex


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 30
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.posn2565_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    expected = SOURCE_VALUES[item.number]
    got = mod.solve(**mod.PARAMS)
    if isinstance(expected, (tuple, str)):
        assert got == expected
    else:
        assert got == pytest.approx(float(expected))


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_branch_current_obeys_kcl():
    for seed in range(60):
        stem, tex = _answer("phys.posn2565_q02", seed)
        emfs = list(map(int, re.search(r"แรงเคลื่อน ([\d V,]+) ตามลำดับ", stem)[1].replace(" V", "").split(", ")))
        resistance = int(re.search(r"ตัวต้านทาน (\d+) Ω", stem)[1])
        branch = int(re.search(r"แขนงที่ (\d+)", stem)[1]) - 1
        current = _rational(tex)
        # Currents sum to zero with the rail at the potential that branch implies.
        for rail in (emfs[branch] - current * resistance, emfs[branch] + current * resistance):
            if sum(Fraction(e) - rail for e in emfs) == 0:
                break
        else:
            raise AssertionError(stem)


def test_generated_mirror_returns_the_ray_to_the_object():
    for seed in range(60):
        stem, tex = _answer("phys.posn2565_q10", seed)
        focal = int(re.search(r"โฟกัส (\d+) cm", stem)[1])
        distance = int(re.search(r"ห่างเลนส์ (\d+) cm", stem)[1])
        gap = int(re.search(r"ห่างจากเลนส์ (\d+) cm", stem)[1])
        radius = _rational(tex)
        # The lens's virtual image (signed lens equation) must sit at the centre.
        image = 1 / (Fraction(-1, focal) - Fraction(1, distance))
        assert gap - image == radius


def test_generated_echo_times_are_consistent():
    for seed in range(60):
        stem, tex = _answer("phys.posn2565_q28", seed)
        first, tau, second = (_rational(re.sub(r"(\d+)/(\d+)", r"\\frac{\1}{\2}", t)) for t in re.findall(r"([\d./]+) s", stem)[:3])
        sound = int(re.search(r"อากาศนิ่ง (\d+) m/s", stem)[1])
        speed = _rational(tex)
        start = (sound + speed) * first / 2
        assert 2 * (start - speed * tau) / (sound + speed) == second
