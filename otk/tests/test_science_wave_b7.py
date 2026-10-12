"""Acceptance tests for Wave B — the ม.1 propagation pair, ว 1.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets._support.science_wave_b7 import (
    METHODS,
    PROPAGATION_SCENARIOS,
    TISSUE_CULTURE_SCENARIOS,
)
from otk.sets.biology.m1.tissue_culture import TISSUE_CULTURE_USES


NEW_KEYS = {
    "plant.propagation_foundation": ("ว 1.2 ม.1/16", 1, "standard_scope"),
    "plant.propagation_fluency": ("ว 1.2 ม.1/16", 2, "standard_scope"),
    "plant.propagation_application": ("ว 1.2 ม.1/16", 3, "exact"),
    "plant.tissue_culture_foundation": ("ว 1.2 ม.1/17", 1, "standard_scope"),
    "plant.tissue_culture_fluency": ("ว 1.2 ม.1/17", 2, "exact"),
    "plant.tissue_culture_application": ("ว 1.2 ม.1/17", 3, "exact"),
}
COMPLETED = ("ว 1.2 ม.1/16", "ว 1.2 ม.1/17")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_propagation_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, status) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["mapping_status"] == status, key


def test_only_the_application_set_claims_the_choosing_indicator():
    """ม.1/16's verb is เลือก…ให้เหมาะสม, so only the Application set is exact."""
    rows = {row["key"]: row for row in catalog()}
    filed = {key: rows[key]["mapping_status"]
             for key in NEW_KEYS if key.startswith("plant.propagation_")}
    assert filed == {
        "plant.propagation_foundation": "standard_scope",
        "plant.propagation_fluency": "standard_scope",
        "plant.propagation_application": "exact",
    }


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


def test_no_two_methods_answer_the_same_need():
    """ปักชำ and ตอนกิ่ง both clone a plant; only the wording separates them."""
    assert len(METHODS) >= 5
    for field in ("name", "procedure", "best_for"):
        values = [getattr(item, field) for item in METHODS]
        assert len(values) == len(set(values)), field


def test_method_answers_come_from_the_table_in_every_direction():
    procedures = {item.name: item.procedure for item in METHODS}
    by_procedure = {item.procedure: item.name for item in METHODS}
    needs = {item.name: item.best_for for item in METHODS}
    by_need = {item.best_for: item.name for item in METHODS}
    checked = {"procedure": 0, "which": 0, "need": 0, "choose": 0}
    for seed in range(600):
        question = generate("plant.propagation_foundation", random.Random(seed))
        stem = _text(question.stem)
        name = next((key for key in procedures if f"“{key}”" in stem), None)
        if name is not None:
            checked["procedure"] += 1
            assert _answer(question) == procedures[name], stem
        else:
            checked["which"] += 1
            procedure = next(key for key in by_procedure if key in stem)
            assert _answer(question) == by_procedure[procedure], stem
    for seed in range(600):
        question = generate("plant.propagation_fluency", random.Random(seed))
        stem = _text(question.stem)
        name = next((key for key in needs if f"“{key}”" in stem), None)
        if name is not None:
            checked["need"] += 1
            assert _answer(question) == needs[name], stem
        else:
            checked["choose"] += 1
            need = next(key for key in by_need if key in stem)
            assert _answer(question) == by_need[need], stem
    assert all(checked.values()), checked


def test_each_tissue_culture_use_has_its_own_reason():
    uses = dict(TISSUE_CULTURE_USES)
    reasons = {reason: use for use, reason in TISSUE_CULTURE_USES}
    assert len(uses) == len(reasons) == len(TISSUE_CULTURE_USES) >= 4
    checked = {"why": 0, "which": 0}
    for seed in range(600):
        question = generate("plant.tissue_culture_fluency", random.Random(seed))
        stem = _text(question.stem)
        offered = {_text(choice.content) for choice in question.choices}
        use = next((key for key in uses if f"“{key}”" in stem), None)
        if use is not None:
            checked["why"] += 1
            assert _answer(question) == uses[use], stem
            # Every distractor is another use's reason, not a generic virtue.
            assert offered <= set(reasons), stem
            continue
        checked["which"] += 1
        reason = next(key for key in reasons if f"“{key}”" in stem)
        assert _answer(question) == reasons[reason], stem
        assert offered <= set(uses), stem
    assert all(checked.values()), checked


def test_authored_scenario_banks_are_well_formed():
    for bank in (PROPAGATION_SCENARIOS, TISSUE_CULTURE_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


def test_the_tissue_culture_bank_names_the_technique_limits_too():
    """ความสำคัญ with no cost attached is a slogan, not an understanding."""
    joined = " ".join(correct for _, correct, _ in TISSUE_CULTURE_SCENARIOS)
    assert "ต้นทุน" in joined
    assert "ปรับสภาพ" in joined


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "plant.propagation_foundation": 10,
        "plant.propagation_fluency": 10,
        "plant.propagation_application": 6,
        "plant.tissue_culture_foundation": 6,
        "plant.tissue_culture_fluency": 8,
        "plant.tissue_culture_application": 6,
    }
    concept_banks = {"plant.tissue_culture_foundation"}
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
