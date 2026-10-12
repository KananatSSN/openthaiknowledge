"""Acceptance tests for the Phase 3 Ohm's law learning-path pilot."""

from __future__ import annotations

import csv
import random
from pathlib import Path

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_PILOT_KEYS
from otk.sets.physics.m3.ohms_law import OHM_EQUATION_TASKS, OHM_UNITS


PILOT_KEYS = (
    "elec.ohms_law_foundation",
    "elec.ohms_law_fluency",
    "elec.ohms_law_application",
)
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_ohms_law_pilot_is_additive_and_preserves_the_baseline():
    assert set(PILOT_KEYS) <= SCIENCE_PILOT_KEYS
    assert len(SCIENCE_BASELINE_KEYS) == 95
    assert "elec.ohms_law" in SCIENCE_BASELINE_KEYS
    assert not set(PILOT_KEYS) & SCIENCE_BASELINE_KEYS


def test_ohms_law_pilot_shares_one_curriculum_node_with_three_real_stages():
    rows = {row["key"]: row for row in catalog()}
    pilot = [rows[key] for key in PILOT_KEYS]
    assert [row["learning_stage"] for row in pilot] == [1, 2, 3]
    assert len({row["curriculum_node_id"] for row in pilot}) == 1
    assert rows["elec.ohms_law"]["curriculum_node_id"] == pilot[0]["curriculum_node_id"]
    assert all(row["indicator_codes"] == ["ว 2.3 ม.3/1"] for row in pilot)
    assert pilot[1]["mapping_status"] == pilot[2]["mapping_status"] == "exact"


def test_ohms_law_outcome_is_complete_with_all_contributing_keys():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        row = next(item for item in csv.DictReader(handle) if item["outcome_code"] == "ว 2.3 ม.3/1")
    assert row["coverage_state"] == "complete"
    assert row["current_set_count"] == "6"
    assert set(row["current_set_keys"].split("; ")) == {
        "elec.ohms_law", "elec.quantities", "elec.units_symbols", *PILOT_KEYS,
    }


def test_foundation_covers_equations_units_meters_and_single_variable_changes():
    stems = []
    answers = []
    for seed in range(400):
        question = generate(PILOT_KEYS[0], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
    for task, _, _ in OHM_EQUATION_TASKS:
        assert any(task in stem for stem in stems)
    for unit in OHM_UNITS:
        assert any(unit in stem for stem in stems)
    assert any("แอมมิเตอร์" in answer for answer in answers)
    assert any("โวลต์มิเตอร์" in answer for answer in answers)
    assert any("สัญลักษณ์" in stem for stem in stems)
    assert any(answer == "เพิ่มขึ้น" for answer in answers)
    assert any(answer == "ลดลง" for answer in answers)


def test_fluency_reads_one_measurement_table_or_graph():
    stems = []
    answers = []
    for seed in range(300):
        question = generate(PILOT_KEYS[1], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
        assert question.hint
    assert any("ครั้งที่ 3" in stem for stem in stems)
    assert any("ความชัน" in stem for stem in stems)
    assert any("แปรผันตรง" in answer for answer in answers)
    assert any(answer.endswith("โอห์ม") for answer in answers)
    assert any(answer.endswith(" A") for answer in answers)


def test_fluency_tables_are_internally_consistent_with_ohms_law():
    for seed in range(300):
        stem = _text(generate(PILOT_KEYS[1], random.Random(seed)).stem)
        rows = [
            line.replace(",", " ").split()
            for line in stem.splitlines() if line.startswith("ครั้งที่")
        ]
        ratios = {int(row[2]) / int(row[4]) for row in rows}
        assert len(ratios) <= 1


def test_application_compares_data_screens_outliers_and_controls_variables():
    stems = []
    answers = []
    for seed in range(400):
        question = generate(PILOT_KEYS[2], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
        assert question.hint
    assert any("ข้อสรุปใดใช้หลักฐานได้ถูกต้อง" in stem for stem in stems)
    assert any("น่าจะคลาดเคลื่อน" in stem for stem in stems)
    assert any("แผนการทดลองใด" in stem for stem in stems)
    assert any("ต้องเพิ่มความต้านทานรวมของวงจรอีกกี่โอห์ม" in stem for stem in stems)
    assert any("ปรับเฉพาะความต่างศักย์" in answer for answer in answers)
    assert any("ต้านทานมากกว่า" in answer for answer in answers)


def test_application_outlier_item_has_exactly_one_inconsistent_measurement():
    for seed in range(400):
        question = generate(PILOT_KEYS[2], random.Random(seed))
        stem = _text(question.stem)
        if "น่าจะคลาดเคลื่อน" not in stem:
            continue
        rows = [
            line.replace(",", " ").split()
            for line in stem.splitlines() if line.startswith("ครั้งที่")
        ]
        assert len(rows) == 4
        ratios = [int(row[2]) / int(row[4]) for row in rows]
        odd = [index for index, ratio in enumerate(ratios) if ratios.count(ratio) == 1]
        assert len(odd) == 1
        assert f"ครั้งที่ {odd[0] + 1}:" in _answer(question)


def test_two_hundred_seed_quality_gate_has_four_distinct_choices_each():
    for key in PILOT_KEYS:
        signatures = set()
        for seed in range(200):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4
            assert choices[question.answer]
            signatures.add((_text(question.stem), choices[question.answer]))
        minimum = 12 if key == PILOT_KEYS[0] else 40 if key == PILOT_KEYS[1] else 90
        assert len(signatures) >= minimum
