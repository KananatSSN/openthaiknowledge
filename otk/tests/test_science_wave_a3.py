"""Acceptance tests for Wave A slice 3 — the ม.1 matter and particle cluster."""

from __future__ import annotations

import csv
import random
import re
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_KEYS
from otk.sets.chemistry.m1.density import DENSITY_MATERIALS
from otk.sets.chemistry.m1.subatomic_particles import PARTICLE_FACTS
from otk.sets.chemistry.m1.particles_and_states_of_matter import STATE_MODELS


NEW_KEYS = {
    "chem.density_foundation": ("ว 2.1 ม.1/5", 1),
    "chem.density_application": ("ว 2.1 ม.1/5", 3),
    "chem.atom_particles_foundation": ("ว 2.1 ม.1/8", 1),
    "chem.atom_particles_application": ("ว 2.1 ม.1/8", 3),
    "chem.particle_state_fluency": ("ว 2.1 ม.1/9", 2),
    "chem.particle_state_application": ("ว 2.1 ม.1/9", 3),
}
COMPLETED = ("ว 2.1 ม.1/5", "ว 2.1 ม.1/8", "ว 2.1 ม.1/9")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_slice_three_is_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (indicator, stage) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [indicator], key


def test_each_completed_topic_holds_all_three_stages():
    rows = [row for row in catalog() if row["curriculum_node_id"]]
    for indicator in COMPLETED:
        node = next(r["curriculum_node_id"] for r in rows if indicator in r["indicator_codes"])
        stages = {r["learning_stage"] for r in rows if r["curriculum_node_id"] == node}
        assert stages == {1, 2, 3}, (indicator, sorted(stages))


def test_completed_outcomes_are_recorded_in_the_matrix():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        rows = {row["outcome_code"]: row for row in csv.DictReader(handle)}
    for indicator in COMPLETED:
        assert rows[indicator]["coverage_state"] == "complete", indicator


def test_density_answers_are_independently_correct():
    checked = 0
    for seed in range(800):
        question = generate("chem.density_application", random.Random(seed))
        stem = _text(question.stem)
        if "ความหนาแน่นของวัตถุนี้เป็นเท่าใด" not in stem:
            continue
        checked += 1
        mass = int(re.search(r"มีมวล (\d+) g", stem).group(1))
        volume = int(re.search(r"ปริมาตร (\d+) cm³", stem).group(1))
        assert mass % volume == 0
        assert _answer(question) == f"{mass // volume} g/cm³", stem
    assert checked


def test_density_identification_matches_the_reference_table():
    lookup = dict(DENSITY_MATERIALS)
    checked = 0
    for seed in range(800):
        question = generate("chem.density_application", random.Random(seed))
        stem = _text(question.stem)
        if "น่าจะเป็นสารใด" not in stem:
            continue
        checked += 1
        volume = int(re.search(r"ปริมาตร (\d+) cm³", stem).group(1))
        mass = float(re.search(r"มีมวล ([\d.]+) g", stem).group(1))
        answer = _answer(question)
        assert float(lookup[answer] * volume) == mass, stem
    assert checked


def test_float_and_sink_matches_the_reference_densities():
    lookup = dict(DENSITY_MATERIALS)
    checked = 0
    for seed in range(600):
        question = generate("chem.density_foundation", random.Random(seed))
        stem = _text(question.stem)
        if "เมื่อหย่อนลงในน้ำ" not in stem:
            continue
        checked += 1
        material = next(m for m in lookup if stem.startswith(m))
        expected = "ลอยอยู่บนน้ำ" if lookup[material] < 1 else "จมลงในน้ำ"
        assert _answer(question) == expected, (material, _answer(question))
    assert checked


def test_particle_charges_and_places_match_the_model():
    charges = {name: charge for name, charge, _ in PARTICLE_FACTS}
    places = {name: place for name, _, place in PARTICLE_FACTS}
    assert charges == {"โปรตอน": "บวก", "นิวตรอน": "เป็นกลาง", "อิเล็กตรอน": "ลบ"}
    assert places["อิเล็กตรอน"] == "รอบนิวเคลียส"
    assert places["โปรตอน"] == places["นิวตรอน"] == "นิวเคลียส"
    checked = 0
    for seed in range(600):
        question = generate("chem.atom_particles_foundation", random.Random(seed))
        stem = _text(question.stem)
        if "มีประจุไฟฟ้าชนิดใด" not in stem:
            continue
        checked += 1
        particle = next(p for p in charges if p in stem)
        assert _answer(question) == charges[particle], stem
    assert checked


def test_neutral_atom_electron_count_equals_the_proton_count():
    checked = 0
    for seed in range(800):
        question = generate("chem.atom_particles_application", random.Random(seed))
        stem = _text(question.stem)
        if "จะมีอิเล็กตรอนกี่อนุภาค" not in stem:
            continue
        checked += 1
        protons = int(re.search(r"โปรตอน (\d+) อนุภาค", stem).group(1))
        assert _answer(question) == f"{protons} อนุภาค", stem
    assert checked


def test_nucleus_count_is_protons_plus_neutrons():
    checked = 0
    for seed in range(800):
        question = generate("chem.atom_particles_application", random.Random(seed))
        stem = _text(question.stem)
        if "อนุภาคในนิวเคลียสมีทั้งหมดกี่อนุภาค" not in stem:
            continue
        checked += 1
        protons = int(re.search(r"โปรตอน (\d+) อนุภาค", stem).group(1))
        neutrons = int(re.search(r"นิวตรอน (\d+) อนุภาค", stem).group(1))
        assert _answer(question) == f"{protons + neutrons} อนุภาค", stem
    assert checked


def test_state_model_answers_come_from_the_authored_table():
    arrangements = {state: arrangement for state, arrangement, _, _ in STATE_MODELS}
    assert set(arrangements) == {"ของแข็ง", "ของเหลว", "แก๊ส"}
    checked = 0
    for seed in range(600):
        question = generate("chem.particle_state_fluency", random.Random(seed))
        stem = _text(question.stem)
        if "มีการจัดเรียงอนุภาคอย่างไร" not in stem:
            continue
        checked += 1
        state = next(s for s in arrangements if f"สถานะ{s}" in stem)
        assert _answer(question) == arrangements[state], stem
    assert checked


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "chem.density_foundation": 12,
        "chem.density_application": 30,
        "chem.atom_particles_foundation": 9,
        "chem.atom_particles_application": 100,
        "chem.particle_state_fluency": 9,
        "chem.particle_state_application": 5,
    }
    for key, minimum in minimums.items():
        signatures = set()
        for seed in range(1000):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            assert question.hint
            signatures.add((_text(question.stem), choices[question.answer]))
        assert len(signatures) >= minimum, (key, len(signatures))
