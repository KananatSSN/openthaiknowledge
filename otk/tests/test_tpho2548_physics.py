"""Pin TPhO 4 (2548) readings against the bound marking scheme and check draws."""

from fractions import Fraction
from math import log, pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2548_physics"
SHEET = load_sheet(SID)
KE2, ELECTRON = 2.307e-28, 9.109e-31
# Marking-scheme formulas at each solver's constants (items 17-19 come from
# the experimental papers with synthetic readings).
SOURCE_VALUES = {
    1: (2 * 2 * 5 + (3 - 2) * 1) / 5,  # (2 M_A u_A + (M_B - M_A) u_B)/(M_A + M_B)
    2: (2 * 3 * 1 + (2 - 3) * 5) / 5,
    3: 4 * 2 * 3 / 25,  # 4 M_A M_B/(M_A + M_B)^2
    4: 4,  # sqrt(M_A M_B)
    5: (4 * 2 * 4 / 36) * (4 * 4 * 8 / 144),  # the two single-collision factors at m = 4
    6: 18,  # -ln 2/(2 ln(99/101)) = 17.3: the 18th collision; the scheme's M/(8m) gives 12.5
    7: 4 + sqrt(2),  # (4 + sqrt 2) k e^2/a for the square
    8: 4 * sqrt(2) * 1.44e-9 / 0.2e-9,
    9: 4 * (1 + 1 / sqrt(5)),  # 5.789 ke^2/a at x = -0.5a
    10: 3.425 * sqrt(KE2 / (ELECTRON * 0.1e-9)),  # v0 ~ 3.425 sqrt(ke^2/(m_e a))
    11: sqrt(4 * sqrt(2) * KE2 / ((0.1e-9) ** 3 * ELECTRON)),
    12: 0.01**2 * 20 / (2 * 0.002 * 0.05),  # a^2 v0/(2 t r)
    13: 1.2 * (0.01**2 * 20 / 0.004) ** 2 / 2 * (1 / 0.1**2 - 1 / 0.05**2),
    14: pi * 1.2 * 0.5**2 * (log(10) - 0.5 + 0.01**2 / (2 * 0.1**2)),
    15: 1.2 * pi * 0.01**2 * 20**2,  # rho pi a^2 v0^2
    16: (pi * 1.2 * 0.5**2 * (log(10) - 0.5 + 0.005) - 1.2 * pi * 0.01**2 * 400) / 9.8,
    17: 5e-5 / (2 * pi * 50 * 10 * 0.06),
    18: 2e-7 * 100e-6 / 8.854e-12,
    19: 1e-3 * (2 / sqrt(4 + 0.2**2) - 2 / sqrt(4 + 0.2128**2)) * 1e9,
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 19
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2548_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    expected = SOURCE_VALUES[item.number]
    got = mod.solve(**mod.PARAMS)
    # Item 10's 3.425 is the scheme's rounded coefficient.
    assert got == pytest.approx(expected, rel=1e-3 if item.number == 10 else 1e-4)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_collision_conserves_momentum_and_energy():
    for seed in range(60):
        q = generate("phys.tpho2548_q01", Random(seed))
        a, ua, b, ub = map(int, re.findall(r"(-?\d+) (?:kg|m/s)", q.stem[0].text)[:4])
        vb = _rational(q.choices[q.answer].content[0].tex)
        va = Fraction(a * ua + b * ub - b * vb, a)
        assert a * ua**2 + b * ub**2 == a * va**2 + b * vb**2


def test_generated_halving_count_is_the_first_to_halve():
    for seed in range(60):
        q = generate("phys.tpho2548_q06", Random(seed))
        ratio = int(re.search(r"M/(\d+)", q.stem[0].text)[1])
        n = int(q.choices[q.answer].content[0].tex)
        keep = Fraction(ratio - 1, ratio + 1) ** 2
        assert keep**n <= Fraction(1, 2) < keep ** (n - 1)
