"""Acceptance tests for Wave A slice 5 — atomic structure and the periodic table."""

from __future__ import annotations

import csv
import random
import re
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_KEYS
from otk.sets._support.chemistry import ELEMENTS, common_charges, iupac_group
from otk.sets.chemistry.m5.particles_in_atoms_and_ions import ION_POOL, SINGLE_ION_ELEMENTS
from otk.sets._support.science_wave_a5 import (
    METALLOID,
    NONMETAL,
    TABLE_POOL,
    block_class,
    metal_class,
    period_of,
)
from otk.sets.chemistry.m4.groups_and_periods import POSITIONS


NEW_KEYS = {
    "chem.nuclide_write_application": ("เคมีเพิ่มเติม 1 ม.4/2", 3),
    "chem.period_of_element_fluency": ("เคมีเพิ่มเติม 1 ม.4/4", 2),
    "chem.element_class_application": ("เคมีเพิ่มเติม 1 ม.4/4", 3),
    "chem.ion_particles_foundation": ("ว 2.1 ม.5/3", 1),
    "chem.ion_particles_application": ("ว 2.1 ม.5/3", 3),
}
COMPLETED = ("เคมีเพิ่มเติม 1 ม.4/2", "เคมีเพิ่มเติม 1 ม.4/4", "ว 2.1 ม.5/3")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _tex(blocks) -> str:
    return " ".join(block.tex for block in blocks if block.kind == "math")


def _answer(question) -> str:
    content = question.choices[question.answer].content
    return _text(content) or _tex(content)


def test_slice_five_is_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (indicator, stage) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [indicator], key


def test_each_completed_topic_holds_all_three_stages():
    rows = [row for row in catalog() if row["curriculum_node_id"]]
    for key, (indicator, _) in NEW_KEYS.items():
        node = next(row["curriculum_node_id"] for row in rows if row["key"] == key)
        stages = {r["learning_stage"] for r in rows if r["curriculum_node_id"] == node}
        assert stages == {1, 2, 3}, (indicator, sorted(stages))


def test_completed_outcomes_are_recorded_in_the_matrix():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        rows = {row["outcome_code"]: row for row in csv.DictReader(handle)}
    for indicator in COMPLETED:
        assert rows[indicator]["coverage_state"] == "complete", indicator
    for key, (indicator, _) in NEW_KEYS.items():
        assert key in rows[indicator]["current_set_keys"].split("; "), key


def test_period_boundaries_match_the_printed_table():
    """คาบ is derived from ``z``; check it against the row each period ends on."""
    by_z = {el.z: el for el in ELEMENTS}
    for z, period in ((1, 1), (2, 1), (3, 2), (10, 2), (11, 3), (18, 3),
                      (19, 4), (36, 4), (37, 5), (54, 5), (55, 6), (86, 6),
                      (87, 7), (118, 7)):
        assert period_of(by_z[z]) == period, z


def test_every_table_position_holds_exactly_one_element():
    """The Application set asks 'which element is here', so the map must be 1:1."""
    assert len(POSITIONS) == len(TABLE_POOL)
    for (group, period), el in POSITIONS.items():
        assert iupac_group(el) == group and period_of(el) == period


def test_metal_classes_place_the_staircase_where_ipst_draws_it():
    by_symbol = {el.symbol: el for el in ELEMENTS}
    for symbol in ("B", "Si", "Ge", "As", "Sb", "Te"):
        assert metal_class(by_symbol[symbol]) == METALLOID, symbol
    for symbol in ("H", "N", "O", "S", "Cl", "Ne", "Se"):
        assert metal_class(by_symbol[symbol]) == NONMETAL, symbol
    for symbol in ("Na", "Ca", "Fe", "Cu", "Al", "Sn", "Pb"):
        assert metal_class(by_symbol[symbol]) == "โลหะ", symbol
    for symbol in ("Sc", "Fe", "Zn", "Ag", "Au"):
        assert block_class(by_symbol[symbol]) == "ธาตุแทรนซิชัน", symbol
    for symbol in ("Na", "Mg", "Al", "C", "Cl", "Ar"):
        assert block_class(by_symbol[symbol]) == "ธาตุเรพรีเซนเททีฟ", symbol
    # The two elements textbooks disagree about must never be drilled.
    assert not any(el.symbol in {"At", "Po"} for el in TABLE_POOL)


def test_written_nuclides_use_protons_plus_neutrons_as_the_mass_number():
    """Re-derive both numbers from the counts in the stem, not from the generator."""
    checked = 0
    for seed in range(800):
        question = generate("chem.nuclide_write_application", random.Random(seed))
        stem = _text(question.stem)
        found = re.search(r"มีโปรตอน (\d+) อนุภาค และนิวตรอน (\d+) อนุภาค", stem)
        if not found:
            continue
        checked += 1
        protons, neutrons = (int(value) for value in found.groups())
        answer = _tex(question.choices[question.answer].content)
        mass, z = (int(value) for value in re.findall(r"\{(\d+)\}", answer)[:2])
        assert (mass, z) == (protons + neutrons, protons), stem
    assert checked


def test_isotope_choices_share_the_atomic_number_and_nothing_else_does():
    checked = 0
    for seed in range(800):
        question = generate("chem.nuclide_write_application", random.Random(seed))
        stem = _text(question.stem)
        if "ไอโซโทป" not in stem:
            continue
        checked += 1
        given = re.findall(r"\{(\d+)\}", _tex(question.stem))[:2]
        mass, z = (int(value) for value in given)
        for index, choice in enumerate(question.choices):
            numbers = re.findall(r"\{(\d+)\}", _tex(choice.content))[:2]
            other_mass, other_z = (int(value) for value in numbers)
            is_isotope = other_z == z and other_mass != mass
            assert is_isotope == (index == question.answer), (stem, other_mass, other_z)
    assert checked


def test_group_and_period_answers_match_the_named_element():
    names = {f"{el.th} ({el.en})": el for el in TABLE_POOL}
    seen = set()
    for seed in range(800):
        question = generate("chem.period_of_element_fluency", random.Random(seed))
        stem = _text(question.stem)
        name = next(key for key in names if f"ธาตุ {key} อยู่หมู่ใด" in stem)
        el = names[name]
        seen.add(el.symbol)
        assert _answer(question) == f"หมู่ {iupac_group(el)} คาบ {period_of(el)}", stem
    assert len(seen) > 40


def test_element_class_answers_are_the_element_that_sits_at_that_position():
    for seed in range(800):
        question = generate("chem.element_class_application", random.Random(seed))
        stem = _text(question.stem)
        group, period = (int(value) for value in re.search(
            r"หมู่ (\d+) และคาบ (\d+)", stem).groups())
        el = POSITIONS[(group, period)]
        assert _answer(question) == (
            f"{el.th} ({el.en}) จัดเป็น{metal_class(el)} "
            f"และอยู่ในกลุ่ม{block_class(el)}"
        ), stem


def test_ion_formation_answers_move_electrons_only():
    charges = {f"{el.th} ({el.en})": common_charges(el)[0]
               for el in SINGLE_ION_ELEMENTS}
    generic = 0
    for seed in range(800):
        question = generate("chem.ion_particles_foundation", random.Random(seed))
        stem = _text(question.stem)
        name = next((key for key in charges if f"ธาตุ {key} กลายเป็น" in stem), None)
        if name is None:
            generic += 1
            assert _answer(question) == "อิเล็กตรอน", stem
            continue
        charge = charges[name]
        verb = "เสีย" if charge > 0 else "รับ"
        assert _answer(question) == f"{verb}อิเล็กตรอน {abs(charge)} อนุภาค", stem
        # Every choice must talk about the same count; only the particle differs.
        for choice in question.choices:
            assert str(abs(charge)) in _text(choice.content), stem
    assert generic


def test_identified_ions_reconcile_all_three_particle_counts():
    checked = 0
    for seed in range(800):
        question = generate("chem.ion_particles_application", random.Random(seed))
        stem = _text(question.stem)
        found = re.search(
            r"มีโปรตอน (\d+) อนุภาค นิวตรอน (\d+) อนุภาค และอิเล็กตรอน (\d+) อนุภาค", stem)
        if not found:
            continue
        checked += 1
        protons, neutrons, electrons = (int(value) for value in found.groups())
        answer = _tex(question.choices[question.answer].content)
        mass, z = (int(value) for value in re.findall(r"\{(\d+)\}", answer)[:2])
        assert (mass, z) == (protons + neutrons, protons), stem
        charge = protons - electrons
        sign = "+" if charge > 0 else "-"
        size = abs(charge) if abs(charge) > 1 else ""
        assert answer.endswith(f"^{{{size}{{{sign}}}}}"), stem
    assert checked


def test_isoelectronic_answers_hold_the_noble_gas_electron_count():
    electrons = {f"{el.symbol}{abs(charge) if abs(charge) > 1 else ''}"
                 f"{'+' if charge > 0 else '-'}": el.z - charge
                 for el, charge in ION_POOL}
    checked = 0
    for seed in range(800):
        question = generate("chem.ion_particles_application", random.Random(seed))
        stem = _text(question.stem)
        found = re.search(r"ซึ่งมีอิเล็กตรอน (\d+) อนุภาค", stem)
        if not found:
            continue
        checked += 1
        target = int(found.group(1))
        for index, choice in enumerate(question.choices):
            ion = re.search(r"ไอออน (\S+) ของธาตุ", _text(choice.content)).group(1)
            assert (electrons[ion] == target) == (index == question.answer), stem
    assert checked


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "chem.nuclide_write_application": 80,
        "chem.period_of_element_fluency": 60,
        "chem.element_class_application": 60,
        "chem.ion_particles_foundation": 20,
        "chem.ion_particles_application": 40,
    }
    for key, minimum in minimums.items():
        signatures = set()
        for seed in range(1000):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) or _tex(choice.content)
                       for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            assert question.hint
            signatures.add((_text(question.stem) + _tex(question.stem),
                            choices[question.answer]))
        assert len(signatures) >= minimum, (key, len(signatures))
