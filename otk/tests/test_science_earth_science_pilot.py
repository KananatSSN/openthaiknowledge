"""Acceptance tests for the Phase 3 rock-cycle learning-path pilot."""

from __future__ import annotations

import csv
import random
from pathlib import Path

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_PILOT_KEYS
from otk.sets.earth_science.p6.rocks_and_the_rock_cycle import (
    ROCK_CLASSES,
    ROCK_CYCLE_ARROWS,
    ROCK_EXAMPLES,
    ROCK_FORMATION_PROCESSES,
    ROCK_TWO_STEP_ROUTES,
)
from otk.sets._support.science_pilots import ROCK_FIELD_EVIDENCE, ROCK_JOURNEYS, ROCK_MODEL_CLAIMS


PILOT_KEYS = (
    "geo.rock_cycle_foundation",
    "geo.rock_cycle_fluency",
    "geo.rock_cycle_application",
)
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_rock_cycle_pilot_is_additive_and_preserves_the_baseline():
    assert set(PILOT_KEYS) <= SCIENCE_PILOT_KEYS
    assert len(SCIENCE_BASELINE_KEYS) == 95
    assert "geo.rock_cycle" in SCIENCE_BASELINE_KEYS
    assert not set(PILOT_KEYS) & SCIENCE_BASELINE_KEYS


def test_rock_cycle_pilot_shares_one_curriculum_node_with_three_real_stages():
    rows = {row["key"]: row for row in catalog()}
    pilot = [rows[key] for key in PILOT_KEYS]
    assert [row["learning_stage"] for row in pilot] == [1, 2, 3]
    assert len({row["curriculum_node_id"] for row in pilot}) == 1
    assert rows["geo.rock_cycle"]["curriculum_node_id"] == pilot[0]["curriculum_node_id"]
    assert all(row["indicator_codes"] == ["ว 3.2 ป.6/1"] for row in pilot)
    assert pilot[1]["mapping_status"] == pilot[2]["mapping_status"] == "exact"


def test_rock_cycle_outcome_is_complete_with_all_contributing_keys():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        row = next(item for item in csv.DictReader(handle) if item["outcome_code"] == "ว 3.2 ป.6/1")
    assert row["coverage_state"] == "complete"
    assert row["current_set_count"] == "12"
    keys = set(row["current_set_keys"].split("; "))
    assert set(PILOT_KEYS) <= keys
    assert "geo.rock_cycle" in keys
    assert len(keys) == 12


def test_authored_rock_banks_name_only_the_three_classes_and_magma():
    allowed = set(ROCK_CLASSES) | {"แมกมา", "ตะกอน"}
    assert {rock_class for _, rock_class in ROCK_FORMATION_PROCESSES} == set(ROCK_CLASSES)
    assert {rock_class for _, rock_class in ROCK_EXAMPLES} == set(ROCK_CLASSES)
    for source, target, _ in ROCK_CYCLE_ARROWS:
        assert source in allowed and target in allowed
    for _, correct, _ in ROCK_JOURNEYS:
        assert all(step in allowed for step in correct.split(" → "))


def test_foundation_covers_processes_named_rocks_and_model_arrows():
    stems = []
    answers = []
    for seed in range(500):
        question = generate(PILOT_KEYS[0], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
        assert question.hint
    for process, _ in ROCK_FORMATION_PROCESSES:
        assert any(process in stem for stem in stems)
    for rock, _ in ROCK_EXAMPLES:
        assert any(rock in stem for stem in stems)
    for source, target, _ in ROCK_CYCLE_ARROWS:
        assert any(f"“{source}” ไปยัง “{target}”" in stem for stem in stems)
    assert set(ROCK_CLASSES) <= set(answers)


def test_fluency_compares_processes_and_predicts_model_steps():
    stems = []
    answers = []
    for seed in range(500):
        question = generate(PILOT_KEYS[1], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
        assert question.hint
    assert any("ข้อใดเปรียบเทียบการเกิด" in stem for stem in stems)
    assert any("จะได้หินใดและเกิดจากกระบวนการใด" in stem for stem in stems)
    assert any("ต้องผ่านกระบวนการใดตามลำดับ" in stem for stem in stems)
    assert any("เรียงลำดับการเกิดหินตะกอน" in stem for stem in stems)
    for _, _, correct, _ in ROCK_TWO_STEP_ROUTES:
        assert correct in answers
    assert any("หินอ่อน โดยกระบวนการการแปรสภาพ" == answer for answer in answers)


def test_application_uses_field_evidence_journeys_and_claim_evaluation():
    stems = []
    answers = []
    for seed in range(500):
        question = generate(PILOT_KEYS[2], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
        assert question.hint
    for evidence, correct, _ in ROCK_FIELD_EVIDENCE:
        assert any(evidence in stem for stem in stems)
        assert correct in answers
    for _, correct, _ in ROCK_JOURNEYS:
        assert correct in answers
    for claim, correct, _ in ROCK_MODEL_CLAIMS:
        assert any(claim in stem for stem in stems)
        assert correct in answers
    assert any("เย็นตัวช้ากว่าใต้เปลือกโลก" in answer for answer in answers)


def test_application_journeys_never_reverse_a_rock_cycle_step():
    impossible = {("ตะกอน", "หินอัคนี"), ("หินตะกอน", "แมกมา"), ("แมกมา", "หินตะกอน")}
    for _, correct, _ in ROCK_JOURNEYS:
        steps = correct.split(" → ")
        assert all(pair not in impossible for pair in zip(steps, steps[1:]))


def test_two_hundred_seed_quality_gate_has_four_distinct_choices_each():
    for key in PILOT_KEYS:
        signatures = set()
        for seed in range(200):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4
            assert choices[question.answer]
            signatures.add((_text(question.stem), choices[question.answer]))
        minimum = 20 if key == PILOT_KEYS[0] else 12 if key == PILOT_KEYS[1] else 16
        assert len(signatures) >= minimum
