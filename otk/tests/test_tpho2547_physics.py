"""Pin TPhO 3 (2547) readings against the bound marking scheme and check draws."""

from fractions import Fraction
from math import exp, pi, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "tpho2547_physics"
SHEET = load_sheet(SID)
# Marking-scheme formulas at each solver's constants (items 13-15 come from
# the experimental paper's theory parts with synthetic readings).
SOURCE_VALUES = {
    1: 2**2 * 1.5 / sqrt(3**2 + 4**2),  # v0^2 t/(H + y)
    2: 2**2 * 4**2 / 5**3,  # v0^2 H^2/(v0^2 t^2 + H^2)^(3/2)
    3: 2 * (10 + 2**2 / 4),  # m(g + v0^2/H)
    4: 2 * 10 + (2 * 0.01 + 0.01) * 4 / (4 * 0.01),  # mg + (m r^2 + I) v0^2/(H r^2)
    5: sqrt(6 * 20 / 0.5) / (2 * pi),
    6: 12 * 49 / (49 * 0.2 * 10),  # 12 V0^2/(49 mu g)
    7: 5 * 7 / (7 * 0.05),  # 5 V0/(7R)
    8: 0.5 * 0.2 * 4 / 4 * exp(-(0.1**2) * 0.4 / (0.01 * 4)),
    9: 320 * 0.1 / 360,  # (c - v) tau/(c + v)
    10: -2 * 340 * 0.1 * 0.5 / 360**2,
    11: 360 * 0.1 / 320,
    12: "overlap",
    13: 26 * 980 * 8 * 0.81 / (4 * pi**2) - 26 * 64,
    14: 150 / 50,
    15: 300 / (100 * pi),
}


def _rational(tex):
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        return (-1 if match[1] else 1) * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def test_every_authored_item_has_one_live_generator():
    assert len(SHEET.items) == len(SOURCE_VALUES) == 15
    assert {it.generator for it in SHEET.items} == {
        key for key in REGISTRY if key.startswith("phys.tpho2547_")
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


def test_generated_string_speed_keeps_the_string_length():
    # The mass's height from the generated answer must make the string 2H long
    # a moment later: d/dt of the slanted length equals v.
    for seed in range(60):
        q = generate("phys.tpho2547_q01", Random(seed))
        stem = q.stem[0].text
        height = Fraction(re.search(r"H = ([\d.]+) m", stem)[1])
        speed = int(re.search(r"ความเร็วคงที่ (\d+) m/s", stem)[1])
        time = Fraction(re.search(r"t = ([\d./]+) s", stem)[1])
        v = _rational(q.choices[q.answer].content[0].tex)
        slant_squared = (speed * time) ** 2 + height**2
        # v * slant = v0^2 t, squared to stay rational
        assert v * v * slant_squared == (speed**2 * time) ** 2


def test_generated_echo_intervals_are_reciprocal():
    for seed in range(60):
        towards = generate("phys.tpho2547_q09", Random(seed))
        away = generate("phys.tpho2547_q11", Random(seed))
        gap = Fraction(re.search(r"ทุก ๆ ([\d.]+) s", towards.stem[0].text)[1])
        a = _rational(towards.choices[towards.answer].content[0].tex)
        b = _rational(away.choices[away.answer].content[0].tex)
        assert a * b == gap * gap


def test_generated_supersonic_fate_matches_direction():
    for seed in range(60):
        q = generate("phys.tpho2547_q12", Random(seed))
        stem = q.stem[0].text
        wave = int(re.search(r"ความเร็ว (\d+) m/s ห่าง", stem)[1])
        speed = int(re.search(r"แหล่งกำเนิดด้วยความเร็ว (\d+) m/s", stem)[1])
        answer = q.choices[q.answer].content[0].text
        if speed < wave:
            assert answer.startswith("คลื่นสะท้อนกลับมาตามลำดับเดิม")
        elif "เข้าหา" in stem:
            assert answer.startswith("คลื่นสะท้อนซ้อนทับ")
        else:
            assert answer.startswith("ไม่มีคลื่นสะท้อน")
