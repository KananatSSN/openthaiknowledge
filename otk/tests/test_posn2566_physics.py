"""Pin source readings and check generated physics beyond solver agreement."""

from fractions import Fraction
from math import pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "posn2566_physics"
SHEET = load_sheet(SID)
# The printed answer of each item, evaluated at the solver's source constants.
SOURCE_VALUES = {
    1: 8,  # m(g - a), 2 kg, a = 6
    2: 40,  # 4Mg/7, M = 7 kg
    3: Fraction(1, 8),  # alpha v / u
    4: 4,  # m v^2/(2r)
    5: 10,  # sqrt(T/B)
    6: 6,  # M u/(M + N m)
    7: 4 * pi * 36e12 * 1e5 / (10 * 5e-26),  # ~ 10^44
    8: 8,  # r + R
    9: -2,  # -2 sin x at t = pi, x = pi/2
    10: 6,  # 2u
    11: 0,  # unchanged in pure water
    12: 10 / sqrt(2),
    13: "rise_then_decay",
    14: Fraction(4, 5),
    15: Fraction(2, 5),
    16: sqrt(2),
    17: -40,
    18: 6,
    19: 5,  # R/2 with R = 10
    20: 2 * 3.8e26 / 42e-13,  # ~ 2 x 10^38
    21: 8,  # lambda v^2
    22: Fraction(9, 2),  # M m/(2R)
    23: 4 * 5.5 / 222,
    24: 2490,
    25: sqrt(2) + 1,
    26: Fraction(9, 40),
    27: Fraction(1, 20),
    28: 1,  # m L/(b(M + 2m))
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
    assert len(SHEET.items) == len(SOURCE_VALUES) == 28
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.posn2566_")
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
        assert got == pytest.approx(float(expected), abs=1e-12)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_diagnostic_choices(item):
    labels = set()
    for seed in range(60):
        q = generate(item.generator, Random(seed))
        assert len(q.choices) == 4
        labels.update(label for label in q.mistakes if label)
    assert labels


def test_generated_pivot_reaction_from_rigid_body_dynamics():
    for seed in range(60):
        stem, tex = _answer("phys.posn2566_q02", seed)
        mass = int(re.search(r"มวล (\d+) kg", stem)[1])
        found = re.search(r"ห่างจากปลายซ้าย (\S+)L", stem)
        fraction = Fraction(found[1]) if found else Fraction(0)
        # Rod of length 1: torque about A, I_A by the parallel-axis theorem.
        d = Fraction(1, 2) - fraction
        inertia = mass * (Fraction(1, 12) + d * d)
        alpha = mass * 10 * d / inertia
        assert _rational(tex) == mass * (10 - alpha * d)


def test_generated_network_obeys_kirchhoff():
    for seed in range(40):
        stem, tex = _answer("phys.posn2566_q19", seed)
        aq, qs, sb, qb, as_, ab = map(int, re.findall(r"(\d+) Ω", stem)[:6])
        total = _rational(tex)
        # Drive 1 A in at A; with the claimed resistance A sits at `total` volts.
        # Solve the node potentials of Q and S and check the current balance.
        g = [Fraction(1, v) for v in (aq, qs, sb, qb, as_, ab)]
        a = total
        a11, a12, b1 = g[0] + g[1] + g[3], -g[1], g[0] * a
        a21, a22, b2 = -g[1], g[4] + g[1] + g[2], g[4] * a
        det = a11 * a22 - a12 * a21
        q = (b1 * a22 - a12 * b2) / det
        s = (a11 * b2 - b1 * a21) / det
        assert (a - q) * g[0] + (a - s) * g[4] + a * g[5] == 1


def test_generated_plate_tilt_balances_moments():
    for seed in range(60):
        stem, tex = _answer("phys.posn2566_q28", seed)
        plate = int(re.search(r"สม่ำเสมอมวล (\d+) kg", stem)[1])
        length = int(re.search(r"ยาว (\d+) cm", stem)[1])
        width = int(re.search(r"กว้าง (\d+) cm", stem)[1])
        hung = int(re.search(r"ห้อยมวล (\d+) kg", stem)[1])
        tan = _rational(tex)
        # Torque about A with cos = 1 and sin = tan (common factor cos theta).
        assert plate * Fraction(width, 2) * tan == hung * (Fraction(length, 2) - width * tan)
