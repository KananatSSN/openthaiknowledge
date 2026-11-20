"""Pin TPhO 18 (2562) readings derived from the paper and check draws."""

from math import log, pi
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2562_physics"
SHEET = load_sheet(SID)
# The folder has no solutions: these are the values derived here at each
# solver's constants, rounded as an answer sheet would give them.
SOURCE_VALUES = {
    1: 1000 * 0.5 * 0.02 * 3.0**2,  # rho L h1 v1^2
    2: 0.5 * 1000 * 9.8 * 0.5 * (0.06**2 - 0.02**2),
    3: 1.0 * ((1 + 8 * 9 / (9.8 * 0.02)) ** 0.5 - 1),  # cm
    4: 3652.19,  # J/m^3 with k = 1/4
    5: 7.35,  # cm
    6: 0.207,
    7: 0.790,  # mH
    8: 3.16,  # mH
    9: 0.574,  # A
    10: 2.07e-7,
    11: 5.80e3,  # K
    12: 6.67e-11 * 1e60 / 4e11,
    13: -2.29e41,  # J
    14: 4.61e6,  # K
    15: -2.48e34,  # J/K
    16: 1.33e14,  # Pa
    17: 4.36e32,  # m^-3
    18: 2.0e29,  # kg
    19: 3.0,  # synthetic n
    20: 4e-17,  # synthetic I0 (A)
    21: 0.970,  # ohm
    22: 850.0,  # nm
    23: 0.685,
    24: 38.0,  # kilohm
}
ROUGH = {4: 1e-6, 5: 1e-3, 6: 5e-3, 7: 1e-3, 8: 1e-3, 9: 1e-3, 10: 5e-3, 11: 1e-3, 13: 5e-3,
         14: 1e-3, 15: 1e-3, 16: 5e-3, 17: 1e-3, 18: 2e-3, 19: 1e-3, 20: 5e-3, 21: 1e-3,
         22: 1e-3, 23: 1e-3, 24: 2e-3}


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 24
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2562_")
    }
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_source_reading(item):
    mod = solver_module(SHEET, item)
    rel = ROUGH.get(item.number, 1e-9)
    assert mod.solve(**mod.PARAMS) == pytest.approx(SOURCE_VALUES[item.number], rel=rel)


def _item(number):
    return solver_module(SHEET, SHEET.items[number - 1])


def test_jump_loss_constant_is_a_quarter():
    # 1.5 counts the potential energy at the layer's centre of mass, h/2: that
    # gives the paper's form with k = 1/4. The energy head h + v^2/2g instead
    # gives the textbook (h2 - h1)^3/(4 h1 h2), which does not have that form.
    h1, h2 = 0.02, _item(3).solve() * 1e-2
    loss = _item(4).check()
    assert loss == pytest.approx(0.25 * 1000 * 9.8 * (h2 - h1) * (h2**2 + h1**2) / (h1 * h2))
    assert loss != pytest.approx(1000 * 9.8 * (h2 - h1) ** 3 / (4 * h1 * h2), rel=1e-2)


def test_star_constants():
    # 3.4 b = 2, 3.5 A = 3/5, 3.9 alpha = 1/2, each from a numerical check
    g, m, r = 6.67e-11, 2.0e30, 7.0e8
    assert _item(13).check() == pytest.approx(-0.6 * g * m * m / r, rel=1e-6)
    rho = 3 * m / (4 * pi * r**3)
    assert _item(16).check() == pytest.approx(0.5 * g * m * rho / r, rel=1e-6)
    assert _item(12).check() == pytest.approx(g * 1e60 / 4e11)


def test_lightest_igniting_cloud_peaks_where_pressures_balance():
    # at the 3.10 density P_deg = P_ideal, and the 3.11 mass peaks at 1e7 K there
    kt = 1.38e-23 * 1e7
    n = _item(17).solve()
    assert 2.4e-38 * n ** (5 / 3) == pytest.approx(n * kt)
    mass = _item(18).solve()
    c = 0.5 * 6.67e-11 * (4 * pi / 3) ** (1 / 3) * 1.67e-27 ** (4 / 3) * mass ** (2 / 3)
    assert c * n ** (1 / 3) - 2.4e-38 * n ** (2 / 3) == pytest.approx(kt)
    assert mass / 2.0e30 == pytest.approx(0.1, abs=1e-3)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_line_loss():
    for seed in range(60):
        q = generate("phys.tpho2562_q06", Random(seed))
        text = q.stem[0].text
        power = float(re.search(r"([\d.]+) kW", text).group(1))
        voltage = float(re.search(r"(\d+) V", text).group(1))
        wire = float(re.search(r"(\d+) Ω", text).group(1))
        expected = power * 1e3 * wire / voltage**2
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(expected, rel=5e-3)


def test_generated_ideality_factor():
    from statistics import linear_regression

    for seed in range(40):
        q = generate("phys.tpho2562_q19", Random(seed))
        pairs = re.findall(r"\(([\d.]+) V, ([\d.]+)(?:×10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+))? A\)", q.stem[0].text)
        assert len(pairs) == 4
        digits = str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789")
        volts = [float(v) for v, _, _ in pairs]
        amps = [float(m) * 10 ** int(p.translate(digits)) if p else float(m) for _, m, p in pairs]
        slope, _ = linear_regression(volts, [log(i) for i in amps])
        expected = 1.60e-19 / (1.38e-23 * 300 * slope)
        assert float(q.choices[q.answer].content[0].tex) == pytest.approx(expected, rel=5e-3)
