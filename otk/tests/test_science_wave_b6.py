"""Acceptance tests for Wave B — the ม.1 plant nutrition pair, ว 1.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m1.fertiliser import EMPHASIS_PURPOSE, FERTILISERS
from otk.sets._support.science_wave_b6 import FERTILISER_SCENARIOS, NUTRIENTS, NUTRIENT_SCENARIOS


NEW_KEYS = {
    "plant.nutrient_foundation": ("ว 1.2 ม.1/14", 1),
    "plant.nutrient_deficiency_fluency": ("ว 1.2 ม.1/14", 2),
    "plant.nutrient_application": ("ว 1.2 ม.1/14", 3),
    "plant.fertiliser_foundation": ("ว 1.2 ม.1/15", 1),
    "plant.fertiliser_fluency": ("ว 1.2 ม.1/15", 2),
    "plant.fertiliser_application": ("ว 1.2 ม.1/15", 3),
}
COMPLETED = ("ว 1.2 ม.1/14", "ว 1.2 ม.1/15")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_nutrition_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["standard_code"] == "ว 1.2", key


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


def test_the_nutrient_table_holds_more_than_the_three_on_a_fertiliser_bag():
    """Three nutrients would leave "which nutrient" with three choices."""
    assert len(NUTRIENTS) >= 4
    names = [item.name for item in NUTRIENTS]
    assert {"ไนโตรเจน", "ฟอสฟอรัส", "โพแทสเซียม"} <= set(names)
    for field in ("name", "role", "deficiency"):
        values = [getattr(item, field) for item in NUTRIENTS]
        # A shared role or symptom would make the reverse direction ambiguous.
        assert len(values) == len(set(values)), field


def test_nutrient_answers_come_from_the_table_in_every_direction():
    roles = {item.name: item.role for item in NUTRIENTS}
    by_role = {item.role: item.name for item in NUTRIENTS}
    symptoms = {item.name: item.deficiency for item in NUTRIENTS}
    by_symptom = {item.deficiency: item.name for item in NUTRIENTS}
    checked = {"role": 0, "which": 0, "symptom": 0, "named": 0}
    for seed in range(600):
        question = generate("plant.nutrient_foundation", random.Random(seed))
        stem = _text(question.stem)
        name = next((key for key in roles if f"“{key}”" in stem), None)
        if name is not None:
            checked["role"] += 1
            assert _answer(question) == roles[name], stem
        else:
            checked["which"] += 1
            role = next(key for key in by_role if key in stem)
            assert _answer(question) == by_role[role], stem
    for seed in range(600):
        question = generate("plant.nutrient_deficiency_fluency", random.Random(seed))
        stem = _text(question.stem)
        symptom = next((key for key in by_symptom if f"“{key}”" in stem), None)
        if symptom is not None:
            checked["symptom"] += 1
            assert _answer(question) == by_symptom[symptom], stem
        else:
            checked["named"] += 1
            name = next(key for key in symptoms if f"“{key}”" in stem)
            assert _answer(question) == symptoms[name], stem
    assert all(checked.values()), checked


def test_every_emphasis_has_a_purpose_and_at_least_one_bag():
    emphases = {item.emphasis for item in FERTILISERS}
    assert emphases == set(EMPHASIS_PURPOSE)
    assert len(emphases) == 4, "four emphases is what keeps the item at four choices"
    formulas = [item.formula for item in FERTILISERS]
    assert len(formulas) == len(set(formulas))
    # More than one bag per emphasis is the point of the distractor filter below.
    assert len(FERTILISERS) > len(emphases)


def test_no_fertiliser_distractor_shares_the_answers_emphasis():
    """46-0-0 and 21-0-0 both lead with nitrogen; offering both gives two answers."""
    emphasis_of = {item.formula: item.emphasis for item in FERTILISERS}
    purpose_of = {value: key for key, value in EMPHASIS_PURPOSE.items()}
    checked = {"formula": 0, "purpose": 0}
    for seed in range(900):
        question = generate("plant.fertiliser_fluency", random.Random(seed))
        stem = _text(question.stem)
        answer = _answer(question)
        offered = {_text(choice.content) for choice in question.choices}
        if answer in emphasis_of:
            checked["formula"] += 1
            wanted = purpose_of[next(p for p in purpose_of if p in stem)]
            assert emphasis_of[answer] == wanted, stem
            assert all(emphasis_of[other] != wanted
                       for other in offered - {answer}), stem
            continue
        checked["purpose"] += 1
        formula = next(key for key in emphasis_of if f"“{key}”" in stem)
        assert answer == EMPHASIS_PURPOSE[emphasis_of[formula]], stem
        assert offered <= set(EMPHASIS_PURPOSE.values()), stem
    assert all(checked.values()), checked


def test_authored_scenario_banks_are_well_formed():
    for bank in (NUTRIENT_SCENARIOS, FERTILISER_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "plant.nutrient_foundation": 12,
        "plant.nutrient_deficiency_fluency": 12,
        "plant.nutrient_application": 6,
        "plant.fertiliser_foundation": 6,
        "plant.fertiliser_fluency": 14,
        "plant.fertiliser_application": 6,
    }
    concept_banks = {"plant.fertiliser_foundation"}
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
