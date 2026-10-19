"""Source readings and independent checks of the generated 2561 stems."""

from fractions import Fraction
from math import hypot, sqrt
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate
from otk.tools.sheetpipe.spec import load_sheet, solver_module

SID = "posn2561_physics"
SHEET = load_sheet(SID)


def _answer(q):
    tex = q.choices[q.answer].content[0].tex
    match = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if match:
        sign = -1 if match[1] else 1
        return sign * Fraction(int(match[2]), int(match[3]))
    return Fraction(tex)


def test_completed_items_have_no_missing_or_orphaned_generator():
    assert len(SHEET.items) == 30
    claimed = {it.generator for it in SHEET.items}
    assert claimed == {key for key in REGISTRY if key.startswith("phys.posn2561_")}
    assert all(it.source and it.page and it.answer for it in SHEET.items)


@pytest.mark.parametrize("item", SHEET.items, ids=lambda it: f"q{it.number:02d}")
def test_each_authored_set_has_diagnostic_labels(item):
    labels = set()
    for seed in range(20):
        question = generate(item.generator, Random(seed))
        labels.update(label for label in question.mistakes if label)
        assert "mistakes" not in question.model_dump()
    assert labels


SOURCE_VALUES = {
    1: (1, 2, -1),
    2: 6,
    3: 3.675,
    4: 7,
    5: sqrt(8 * 9.8 / 5),
    6: Fraction(1, 9),
    7: 380,
    8: 5.2,
    9: Fraction(1, 3),
    10: sqrt(3400),
    11: -4 + sqrt(2),
    12: sqrt(2),
    13: 10,
    14: 192,
    15: 0.4,
    16: 8,
    17: 240,
    18: 0.000025,
    19: 320,
    20: 10,
    21: 980,
    22: 2 + 9.8 / sqrt(3),
    23: 1 / sqrt(3),
    24: 7,
    25: 32,
    26: 51,
    27: Fraction(-3, 4),
    28: Fraction(9, 5),
    29: 54,
    30: 8,
}


@pytest.mark.parametrize(
    "item",
    [it for it in SHEET.items if it.number in SOURCE_VALUES],
    ids=lambda it: f"q{it.number:02d}",
)
def test_source_values_pin_the_reading_of_each_item(item):
    module = solver_module(SHEET, item)
    result = module.solve(**module.PARAMS)
    assert result == pytest.approx(SOURCE_VALUES[item.number])


def test_both_source_hinge_force_branches_obey_equilibrium():
    # This catches the unstated sign condition in the source, not only algebra.
    for sign, lower_squared in ((1, 3400), (-1, 17800)):
        upper_horizontal, upper_vertical = -30, sign * 40
        lower_horizontal, lower_vertical = 30, 90 - upper_vertical
        assert upper_horizontal + lower_horizontal == 0
        assert upper_vertical + lower_vertical == 90
        assert 30 * 1.5 == 90 * 0.5
        assert hypot(upper_horizontal, upper_vertical) == 50
        assert lower_horizontal**2 + lower_vertical**2 == lower_squared


def test_generated_spring_scale_obeys_each_block_equation():
    for seed in range(60):
        q = generate("phys.posn2561_q04", Random(seed))
        stem = q.stem[0].text
        left_mass, right_mass = map(int, re.findall(r"มวล (\d+) kg", stem))
        left_force, right_force = map(int, re.search(r"ออกแรง (\d+) N.*และ (\d+) N", stem).groups())
        tension = _answer(q)
        a_left = (left_force + tension) / left_mass
        a_right = (right_force - tension) / right_mass
        assert a_left == a_right


def test_generated_delayed_throws_meet_above_the_launch_point():
    for seed in range(60):
        q = generate("phys.posn2561_q03", Random(seed))
        stem = q.stem[0].text
        speed = Fraction(re.search(r"ต้น (\d+) m/s", stem)[1])
        delay = Fraction(re.search(r"ถัดไป ([\d.]+) s", stem)[1])
        # Find time since the second ball was thrown from equal heights.
        t = speed / 10 - delay / 2
        newer = speed * t - 5 * t * t
        older = speed * (t + delay) - 5 * (t + delay) ** 2
        assert newer == older == _answer(q) and newer > 0


def test_generated_lid_temperature_predicts_the_required_lift():
    for seed in range(60):
        q = generate("phys.posn2561_q19", Random(seed))
        stem = q.stem[0].text
        height = Fraction(int(re.search(r"สูง (\d+) cm", stem)[1]), 100)
        area = Fraction(int(re.search(r"หน้าตัด (\d+) cm²", stem)[1]), 10000)
        force = int(re.search(r"ขึ้น (\d+) N", stem)[1])
        pressure = Fraction(1, 10) * _answer(q) / (area * height)
        assert (100000 - pressure) * area == force


def test_switched_ammeter_is_a_branch_current_with_signed_change():
    for seed in range(60):
        q = generate("phys.posn2561_q27", Random(seed))
        stem = q.stem[0].text
        voltage = int(re.search(r"อุดมคติ (\d+) V", stem)[1])
        series = int(re.search(r"อนุกรมกับ (\d+) Ω", stem)[1])
        before = Fraction(voltage, series + 10)
        # KCL at the common node after the switch closes, independently.
        node = Fraction(voltage, series) / (Fraction(1, series) + Fraction(1, 5))
        after = node / 10
        assert after - before == _answer(q) < 0
