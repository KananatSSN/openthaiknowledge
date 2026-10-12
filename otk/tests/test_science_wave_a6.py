"""Acceptance tests for Wave A slice 6 — the ม.5 ฟิสิกส์เพิ่มเติม electricity cluster."""

from __future__ import annotations

import csv
import random
import re
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_KEYS
from otk.sets.physics.m5.power_in_resistors import EMF_CIRCUITS, PowerEmfFoundation
from otk.sets.physics.m5.resistivity import WIRE_PAIRS, wire_resistance
from otk.sets.physics.m5.electric_potential import ElectricPotentialFoundation


NEW_KEYS = {
    "elec.resistance_network_application": ("ฟิสิกส์เพิ่มเติม 3 ม.5/8", 3),
    "elec.electric_potential_foundation": ("ฟิสิกส์เพิ่มเติม 3 ม.5/4", 1),
    "elec.electric_potential_application": ("ฟิสิกส์เพิ่มเติม 3 ม.5/4", 3),
    "elec.power_emf_foundation": ("ฟิสิกส์เพิ่มเติม 3 ม.5/9", 1),
    "elec.power_emf_application": ("ฟิสิกส์เพิ่มเติม 3 ม.5/9", 3),
}
COMPLETED = ("ฟิสิกส์เพิ่มเติม 3 ม.5/4", "ฟิสิกส์เพิ่มเติม 3 ม.5/8",
             "ฟิสิกส์เพิ่มเติม 3 ม.5/9")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer_of(choice) -> str:
    """One choice as a string, whichever kind of block it is made of."""
    return _text(choice.content) or " ".join(
        block.tex for block in choice.content if block.kind == "math")


def _answer(question) -> str:
    return _answer_of(question.choices[question.answer])


def test_slice_six_is_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key


def test_each_completed_topic_holds_all_three_stages():
    rows = [row for row in catalog() if row["curriculum_node_id"]]
    for key, (outcome, _) in NEW_KEYS.items():
        node = next(row["curriculum_node_id"] for row in rows if row["key"] == key)
        stages = {r["learning_stage"] for r in rows if r["curriculum_node_id"] == node}
        assert stages == {1, 2, 3}, (outcome, sorted(stages))


def test_completed_outcomes_are_recorded_in_the_matrix():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        rows = {row["outcome_code"]: row for row in csv.DictReader(handle)}
    for outcome in COMPLETED:
        assert rows[outcome]["coverage_state"] == "complete", outcome
    for key, (outcome, _) in NEW_KEYS.items():
        assert key in rows[outcome]["current_set_keys"].split("; "), key


def test_every_wire_pair_gives_whole_series_and_parallel_resistances():
    """The stems print only the geometry, so all four derived values must be whole."""
    for rho, l1, a1, l2, a2 in WIRE_PAIRS:
        assert rho * l1 % a1 == 0 and rho * l2 % a2 == 0, (rho, l1, a1, l2, a2)
        r1, r2 = wire_resistance(rho, l1, a1), wire_resistance(rho, l2, a2)
        assert r1 >= 2 and r2 >= 2
        # Equal wires would let a learner halve one resistance without combining.
        assert r1 != r2, (r1, r2)
        assert r1 * r2 % (r1 + r2) == 0, (r1, r2)


def test_equivalent_resistance_answers_are_rebuilt_from_the_stated_geometry():
    seen = {"อนุกรม": 0, "ขนาน": 0}
    for seed in range(800):
        question = generate("elec.resistance_network_application", random.Random(seed))
        stem = _text(question.stem)
        rho = int(re.search(r"สภาพต้านทาน (\d+)×", stem).group(1))
        wires = re.findall(r"ยาว (\d+) เมตร พื้นที่หน้าตัด (\d+)×", stem)
        assert len(wires) == 2, stem
        r1, r2 = (wire_resistance(rho, int(length), int(area))
                  for length, area in wires)
        if "อนุกรม" in stem:
            seen["อนุกรม"] += 1
            assert _answer(question) == str(r1 + r2), stem
        else:
            seen["ขนาน"] += 1
            assert _answer(question) == str(r1 * r2 // (r1 + r2)), stem
    assert all(seen.values()), seen


def test_work_on_a_charge_uses_the_difference_of_the_two_potentials():
    checked = 0
    for seed in range(800):
        question = generate("elec.electric_potential_application", random.Random(seed))
        stem = _text(question.stem)
        found = re.search(
            r"จุด A มีศักย์ไฟฟ้า (\d+) โวลต์ และจุด B มีศักย์ไฟฟ้า (\d+) โวลต์ "
            r"ต้องใช้งานเท่าใดในการเคลื่อนประจุ (\d+) ไมโครคูลอมบ์", stem)
        if not found:
            continue
        checked += 1
        start, end, charge = (int(value) for value in found.groups())
        assert end > start, stem
        assert _answer(question) == str(charge * (end - start)), stem
        # The destination potential alone is the mistake this item is built to
        # catch, so it has to be on offer.
        choices = {" ".join(block.tex for block in choice.content
                            if block.kind == "math")
                   for choice in question.choices}
        assert str(charge * end) in choices, stem
    assert checked


def test_the_other_two_potential_directions_invert_the_same_relation():
    checked = {"potential": 0, "charge": 0}
    for seed in range(800):
        question = generate("elec.electric_potential_application", random.Random(seed))
        stem = _text(question.stem)
        found = re.search(
            r"ใช้งาน (\d+) ไมโครจูล ในการเคลื่อนประจุ (\d+) ไมโครคูลอมบ์ "
            r"จากจุด A ซึ่งมีศักย์ไฟฟ้า (\d+) โวลต์", stem)
        if found:
            checked["potential"] += 1
            work, charge, start = (int(value) for value in found.groups())
            assert work % charge == 0, stem
            assert _answer(question) == str(start + work // charge), stem
            continue
        found = re.search(
            r"ต้องใช้งาน (\d+) ไมโครจูล .*?ศักย์ไฟฟ้า (\d+) โวลต์ "
            r"ไปยังจุดที่มีศักย์ไฟฟ้า (\d+) โวลต์", stem)
        if not found:
            continue
        checked["charge"] += 1
        work, start, end = (int(value) for value in found.groups())
        assert work % (end - start) == 0, stem
        assert _answer(question) == str(work // (end - start)), stem
    assert all(checked.values()), checked


def test_every_emf_circuit_draws_a_whole_current():
    for emf, internal, external in EMF_CIRCUITS:
        assert emf % (external + internal) == 0, (emf, internal, external)
        # A real cell's internal resistance is the smaller of the two, and a
        # current of 1 A would hide every dropped square in I²R.
        assert internal < external, (internal, external)
        assert emf // (external + internal) >= 2, (emf, internal, external)


def test_emf_answers_all_go_through_the_current_including_internal_resistance():
    seen = {"กำลังไฟฟ้าเท่าใด": 0, "ความต่างศักย์": 0, "สูญเสียไป": 0}
    for seed in range(800):
        question = generate("elec.power_emf_application", random.Random(seed))
        stem = _text(question.stem)
        emf, internal, external = (int(value) for value in re.search(
            r"อีเอ็มเอฟ (\d+) โวลต์ และความต้านทานภายใน (\d+) โอห์ม "
            r"ต่อเข้ากับตัวต้านทาน (\d+) โอห์ม", stem).groups())
        current = emf // (external + internal)
        if "สูญเสียไป" in stem:
            seen["สูญเสียไป"] += 1
            assert _answer(question) == str(current * current * internal), stem
        elif "ความต่างศักย์" in stem:
            seen["ความต่างศักย์"] += 1
            assert _answer(question) == str(emf - current * internal), stem
        else:
            seen["กำลังไฟฟ้าเท่าใด"] += 1
            assert _answer(question) == str(current * current * external), stem
    assert all(seen.values()), seen


def test_concept_banks_offer_three_distractors_and_no_repeated_stem():
    for cls in (ElectricPotentialFoundation, PowerEmfFoundation):
        stems = [item.stem for item in cls.ITEMS]
        assert len(stems) == len(set(stems)) >= 6, cls.__name__
        for item in cls.ITEMS:
            assert len(item.distractors) >= 3, item.stem
            assert item.correct not in item.distractors, item.stem
            assert len(set(item.distractors)) == len(item.distractors), item.stem


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "elec.resistance_network_application": 20,
        "elec.electric_potential_foundation": 7,
        "elec.electric_potential_application": 200,
        "elec.power_emf_foundation": 7,
        "elec.power_emf_application": 30,
    }
    for key, minimum in minimums.items():
        signatures = set()
        for seed in range(1000):
            question = generate(key, random.Random(seed))
            choices = [_answer_of(choice) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            signatures.add((_text(question.stem), choices[question.answer]))
        assert len(signatures) >= minimum, (key, len(signatures))
