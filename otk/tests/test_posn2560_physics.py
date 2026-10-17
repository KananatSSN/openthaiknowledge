"""Source-reading regressions and independent checks of generated stems."""

from fractions import Fraction
from math import isclose
from random import Random
import re

import numpy as np
import pytest

from otk.core import REGISTRY, generate
from otk.core.provenance import provenance
from otk.sheets.posn2560_physics import q14, q20
from otk.tools.sheetpipe.spec import load_sheet


def _tex_value(tex):
    fraction = re.fullmatch(r"\\frac\{(-?\d+)\}\{(\d+)\}", tex)
    return Fraction(int(fraction[1]), int(fraction[2])) if fraction else Fraction(tex)


def _answer(question):
    return _tex_value(question.choices[question.answer].content[0].tex)


def test_all_thirty_items_are_present_and_registered():
    sheet = load_sheet("posn2560_physics")
    assert [it.number for it in sheet.items] == list(range(1, 31))
    claimed = {it.generator for it in sheet.items}
    assert claimed == {k for k in REGISTRY if k.startswith("phys.posn2560_")}
    assert all(it.source and it.page for it in sheet.items)
    assert all(sheet.item(n).note for n in (2, 5, 20, 30))


@pytest.mark.parametrize("number", range(1, 31))
def test_each_set_exposes_named_diagnostic_mistakes(number):
    observed = set()
    for seed in range(20):
        question = generate(f"phys.posn2560_q{number:02d}", Random(seed))
        observed.update(label for label in question.mistakes if label)
        assert "mistakes" not in question.model_dump()
    assert observed


@pytest.mark.parametrize("printed_number", range(1, 11))
def test_written_item_citation_uses_the_printed_section_and_number(printed_number):
    found = provenance(f"phys.posn2560_q{20 + printed_number:02d}")
    assert f"ตอนที่ 2 ข้อ {printed_number} " in found.sources[0]


@pytest.mark.parametrize("focal,orientation", [(12.0, -1), (30 / 7, 1)])
def test_both_offered_source_lens_mirror_answers_really_image_the_object(focal, orientation):
    # Trace two separate paraxial rays with physical height/slope updates,
    # independent of the solver's ABCD-matrix check.
    for height, slope in ((0.0, 0.01), (0.1, -0.02)):
        y, angle = height + 30 * slope, slope
        angle -= y / focal
        y += 5 * angle
        angle += 2 * y / 15
        y += 5 * angle
        angle -= y / focal
        y += 30 * angle
        assert isclose(y, orientation * height, abs_tol=1e-12)
    assert np.isclose(q20.round_trip(focal, 30, 5, 15)[0, 1], 0)


def test_parallel_capacitor_does_not_change_steady_series_charge():
    for capacitance in (0.5, 2, 8, 100):
        assert q14.solve(cp=capacitance) == pytest.approx(6.4)
        assert q14.check(cp=capacitance) == pytest.approx(6.4)


def test_generated_lens_screen_motion_satisfies_both_imaging_equations():
    for seed in range(60):
        question = generate("phys.posn2560_q30", Random(seed))
        stem = question.stem[0].text
        image, lens_move, screen_move = map(int, re.findall(r"(\d+) cm", stem))
        focal = _answer(question)
        # Infer object distance from the first image, then check the second.
        u = 1 / (1 / focal - Fraction(1, image))
        u2, v2 = u + lens_move, image - lens_move - screen_move
        assert 1 / u2 + Fraction(1, v2) == 1 / focal


def test_generated_circuit_obeys_signed_kirchhoff_equations():
    for seed in range(60):
        question = generate("phys.posn2560_q27", Random(seed))
        stem = question.stem[0].text
        e1, e2 = map(int, re.findall(r"แบตเตอรี่ (\d+) V", stem))
        i1 = int(re.search(r"I₁ = (\d+) A", stem)[1])
        i3 = _answer(question)
        i2 = i1 + i3
        voltage_from_top = e1 - i1
        voltage_from_middle = 2 * i2 - e2
        assert voltage_from_top == voltage_from_middle
        # A positive right-facing bottom source exists for every draw.
        assert voltage_from_top + 4 * i3 > 0


def test_generated_capacitor_charge_uses_voltage_divider_and_neutral_midpoint():
    for seed in range(60):
        question = generate("phys.posn2560_q14", Random(seed))
        stem = question.stem[0].text
        supply = int(re.search(r"แหล่งจ่าย (\d+) V", stem)[1])
        c1, c2 = map(int, re.search(r"\((\d+) µF อนุกรม (\d+) µF\)", stem).groups())
        charge = _answer(question)
        # Steady resistor current from a direct loop equation, then capacitor voltages.
        current = Fraction(supply, 6)
        assert charge / Fraction(c1) + charge / Fraction(c2) == 4 * current
