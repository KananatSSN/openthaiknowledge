"""Acceptance tests for the Phase 3 change-of-state learning-path pilot."""

from __future__ import annotations

import csv
import random
from pathlib import Path

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_PILOT_KEYS
from otk.sets.chemistry.p5.changes_of_state import PHASE_CHANGE_EXAMPLES


PILOT_KEYS = (
    "chem.phase_change_foundation",
    "chem.phase_change_fluency",
    "chem.phase_change_application",
)
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_phase_change_pilot_is_additive_and_preserves_the_baseline():
    assert set(PILOT_KEYS) <= SCIENCE_PILOT_KEYS
    assert len(SCIENCE_BASELINE_KEYS) == 95
    assert "chem.phase_change" in SCIENCE_BASELINE_KEYS
    assert not set(PILOT_KEYS) & SCIENCE_BASELINE_KEYS


def test_phase_change_pilot_shares_one_curriculum_node_with_three_real_stages():
    rows = {row["key"]: row for row in catalog()}
    pilot = [rows[key] for key in PILOT_KEYS]
    assert [row["learning_stage"] for row in pilot] == [1, 2, 3]
    assert len({row["curriculum_node_id"] for row in pilot}) == 1
    assert all(row["indicator_codes"] == ["ว 2.1 ป.5/1"] for row in pilot)
    assert pilot[1]["mapping_status"] == pilot[2]["mapping_status"] == "exact"


def test_phase_change_outcome_is_complete_with_all_contributing_keys():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        row = next(item for item in csv.DictReader(handle) if item["outcome_code"] == "ว 2.1 ป.5/1")
    assert row["coverage_state"] == "complete"
    assert row["current_set_count"] == "5"
    assert set(row["current_set_keys"].split("; ")) == {
        "chem.matter_change", "chem.phase_change", *PILOT_KEYS,
    }


def test_foundation_covers_every_authored_event_and_heat_direction():
    stems = []
    answers = []
    for seed in range(400):
        question = generate(PILOT_KEYS[0], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
    for example in PHASE_CHANGE_EXAMPLES:
        assert any(example.event in stem for stem in stems)
    assert any(answer == "สสารได้รับความร้อน" for answer in answers)
    assert any(answer == "สสารสูญเสียความร้อน" for answer in answers)


def test_fluency_uses_observations_as_evidence():
    stems = []
    answers = []
    for seed in range(300):
        question = generate(PILOT_KEYS[1], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
        assert question.hint
    assert any("น้ำเหลวมากกว่า" in stem for stem in stems)
    assert any("หยดน้ำใต้ฝา" in stem for stem in stems)
    assert any("อุณหภูมิลด" in stem for stem in stems)
    assert any("ถ่ายโอนความร้อน" in answer for answer in answers)


def test_application_interprets_data_and_experimental_controls():
    stems = []
    answers = []
    for seed in range(400):
        question = generate(PILOT_KEYS[2], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
        assert question.hint
    assert any("อุณหภูมิคงที่ที่ 0 °C" in stem and "น้ำแข็งลด" in stem for stem in stems)
    assert any("น้ำแข็งเกิดขึ้น" in stem for stem in stems)
    assert any("ตัวแปร" in answer or "เปลี่ยนเฉพาะอุณหภูมิ" in answer for answer in answers)
    assert any("ควบแน่นบนแผ่นแก้ว" in answer for answer in answers)


def test_two_hundred_seed_quality_gate_has_four_distinct_choices_each():
    for key in PILOT_KEYS:
        signatures = set()
        for seed in range(200):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4
            assert choices[question.answer]
            signatures.add((_text(question.stem), choices[question.answer]))
        minimum = 12 if key == PILOT_KEYS[0] else 20 if key == PILOT_KEYS[1] else 100
        assert len(signatures) >= minimum
