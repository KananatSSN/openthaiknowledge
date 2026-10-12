"""Acceptance tests for Wave B — the ม.1 transport pair, ว 1.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m1.transport_direction import DIRECTION_CHOICES, DOWNWARD, JOURNEYS, UPWARD
from otk.sets._support.science_wave_b4 import DIRECTION_SCENARIOS, PHLOEM, TISSUE_SCENARIOS, XYLEM
from otk.sets.biology.m1.transport_tissue import VESSEL_ASPECTS


NEW_KEYS = {
    "plant.transport_tissue_foundation": ("ว 1.2 ม.1/9", 1, "exact_allowed"),
    "plant.transport_tissue_fluency": ("ว 1.2 ม.1/9", 2, "exact_allowed"),
    "plant.transport_tissue_application": ("ว 1.2 ม.1/9", 3, "exact_allowed"),
    "plant.transport_direction_foundation": ("ว 1.2 ม.1/10", 1, "diagram"),
    "plant.transport_direction_fluency": ("ว 1.2 ม.1/10", 2, "diagram"),
    "plant.transport_direction_application": ("ว 1.2 ม.1/10", 3, "diagram"),
}
COMPLETED = ("ว 1.2 ม.1/9", "ว 1.2 ม.1/10")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_transport_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, _) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["standard_code"] == "ว 1.2", key


def test_no_direction_set_claims_to_assess_the_drawn_diagram():
    """ม.1/10 says เขียนแผนภาพ, which multiple choice cannot require."""
    rows = {row["key"]: row for row in catalog()}
    for key, (_, _, kind) in NEW_KEYS.items():
        if kind == "diagram":
            assert rows[key]["mapping_status"] == "standard_scope", key


def test_each_completed_topic_holds_all_three_stages():
    rows = [row for row in catalog() if row["curriculum_node_id"]]
    for key, (outcome, _, _) in NEW_KEYS.items():
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
    for key, (outcome, _, _) in NEW_KEYS.items():
        assert key in rows[outcome]["current_set_keys"].split("; "), key


def test_every_aspect_states_a_different_value_for_each_vessel():
    """A shared value would make the swapped statement true, and the item broken."""
    assert len(VESSEL_ASPECTS) >= 4
    for aspect in VESSEL_ASPECTS:
        assert aspect.xylem != aspect.phloem, aspect.aspect
    values = [value for aspect in VESSEL_ASPECTS
              for value in (aspect.xylem, aspect.phloem)]
    assert len(values) == len(set(values))


def test_foundation_offers_one_true_statement_and_three_from_the_other_vessel():
    xylem = {aspect.xylem for aspect in VESSEL_ASPECTS}
    phloem = {aspect.phloem for aspect in VESSEL_ASPECTS}
    seen = set()
    for seed in range(600):
        question = generate("plant.transport_tissue_foundation", random.Random(seed))
        stem = _text(question.stem)
        tissue = XYLEM if f"“{XYLEM}”" in stem else PHLOEM
        seen.add(tissue)
        mine, theirs = (xylem, phloem) if tissue == XYLEM else (phloem, xylem)
        assert _answer(question) in mine, stem
        others = {_text(c.content) for c in question.choices} - {_answer(question)}
        assert others <= theirs, stem
    assert seen == {XYLEM, PHLOEM}


def test_exactly_one_pairing_is_the_right_way_round():
    truth = {(XYLEM, aspect.xylem) for aspect in VESSEL_ASPECTS}
    truth |= {(PHLOEM, aspect.phloem) for aspect in VESSEL_ASPECTS}
    for seed in range(600):
        question = generate("plant.transport_tissue_fluency", random.Random(seed))
        correct = 0
        for choice in question.choices:
            tissue, value = _text(choice.content).split(": ", 1)
            correct += (tissue, value) in truth
        assert correct == 1, [_text(c.content) for c in question.choices]
        tissue, value = _answer(question).split(": ", 1)
        assert (tissue, value) in truth


def test_every_journey_is_carried_by_the_vessel_that_carries_that_substance():
    assert len(DIRECTION_CHOICES) == 4
    for journey in JOURNEYS:
        assert journey.tissue in (XYLEM, PHLOEM)
        assert journey.direction in (UPWARD, DOWNWARD)
        # Water and dissolved minerals go up the xylem; nothing else does.
        if journey.tissue == XYLEM:
            assert journey.direction == UPWARD, journey
    # The rows must include sugar moving upward, or the set would teach the very
    # misconception it exists to correct.
    assert any(j.tissue == PHLOEM and j.direction == UPWARD for j in JOURNEYS)
    assert any(j.tissue == PHLOEM and j.direction == DOWNWARD for j in JOURNEYS)


def test_direction_answers_match_the_journey_named_in_the_stem():
    for seed in range(600):
        question = generate("plant.transport_direction_fluency", random.Random(seed))
        stem = _text(question.stem)
        if stem.startswith("การลำเลียงใดต่อไปนี้เกิดใน"):
            # The reverse form: the answer is the one journey with the named vessel and direction.
            answer = _answer(question)
            journey = next(j for j in JOURNEYS if answer == f"“{j.substance}” จาก{j.origin}ไปยัง{j.destination}")
            assert f"เกิดใน{journey.tissue} และ{journey.direction}" in stem, stem
            continue
        journey = next(j for j in JOURNEYS
                       if f"“{j.substance}”" in stem
                       and f"จาก{j.origin}ไปยัง{j.destination}" in stem)
        assert _answer(question) == f"{journey.tissue} {journey.direction}", stem
        assert {_text(c.content) for c in question.choices} == set(DIRECTION_CHOICES)


def test_authored_scenario_banks_are_well_formed():
    for bank in (TISSUE_SCENARIOS, DIRECTION_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "plant.transport_tissue_foundation": 8,
        "plant.transport_tissue_fluency": 8,
        "plant.transport_tissue_application": 6,
        "plant.transport_direction_foundation": 6,
        "plant.transport_direction_fluency": 7,
        "plant.transport_direction_application": 6,
    }
    concept_banks = {"plant.transport_direction_foundation"}
    for key, minimum in minimums.items():
        signatures = set()
        for seed in range(1000):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            if key not in concept_banks:
                assert question.hint, (key, seed)
            signatures.add((_text(question.stem), choices[question.answer]))
        assert len(signatures) >= minimum, (key, len(signatures))
