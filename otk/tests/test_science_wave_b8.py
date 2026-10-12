"""Acceptance tests for Wave B — the ม.2 respiratory block, ว 1.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m2.respiratory import AIR_PATH, ORGANS
from otk.sets._support.science_wave_b8 import BREATHING_SCENARIOS, RESPIRATORY_SCENARIOS
from otk.sets.biology.m2.breathing_and_gas_exchange import (
    EXCHANGES,
    EXHALE,
    EXHALE_FACTS,
    INHALE,
    INHALE_FACTS,
)


NEW_KEYS = {
    "body.respiratory_organs_foundation": ("ว 1.2 ม.2/1", 1, "standard_scope"),
    "body.respiratory_path_fluency": ("ว 1.2 ม.2/1", 2, "exact"),
    "body.respiratory_application": ("ว 1.2 ม.2/1", 3, "exact"),
    "body.breathing_mechanism_foundation": ("ว 1.2 ม.2/2", 1, "standard_scope"),
    "body.gas_exchange_fluency": ("ว 1.2 ม.2/2", 2, "exact"),
    "body.breathing_application": ("ว 1.2 ม.2/2", 3, "standard_scope"),
}
COMPLETED = ("ว 1.2 ม.2/1", "ว 1.2 ม.2/2")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_respiratory_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, status) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["mapping_status"] == status, key
        assert rows[key]["level"] == "ม.2", key


def test_only_the_gas_exchange_half_of_the_model_indicator_claims_exact():
    """ม.2/2 says โดยใช้แบบจำลอง for breathing, but not for gas exchange."""
    rows = {row["key"]: row for row in catalog()}
    filed = {key: rows[key]["mapping_status"]
             for key, (outcome, _, _) in NEW_KEYS.items()
             if outcome == "ว 1.2 ม.2/2"}
    assert filed == {
        "body.breathing_mechanism_foundation": "standard_scope",
        "body.gas_exchange_fluency": "exact",
        "body.breathing_application": "standard_scope",
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


def test_the_air_path_runs_outside_in_and_ends_where_exchange_happens():
    assert AIR_PATH[0] == "จมูก" and AIR_PATH[-1] == "ถุงลม"
    assert len(AIR_PATH) == len(set(AIR_PATH)) >= 5
    # หลอดลม must come before its own branches, or the order question is wrong.
    assert AIR_PATH.index("หลอดลม") < AIR_PATH.index("หลอดลมฝอย")
    functions = [item.function for item in ORGANS]
    names = [item.name for item in ORGANS]
    assert len(functions) == len(set(functions))
    assert len(names) == len(set(names))


def test_path_answers_are_read_off_the_one_stored_order():
    checked = {"next": 0, "order": 0}
    for seed in range(600):
        question = generate("body.respiratory_path_fluency", random.Random(seed))
        stem = _text(question.stem)
        if "เรียงลำดับ" in stem:
            checked["order"] += 1
            assert _answer(question) == " → ".join(AIR_PATH), stem
            continue
        checked["next"] += 1
        current = next(name for name in AIR_PATH if f"“{name}”" in stem)
        assert _answer(question) == AIR_PATH[AIR_PATH.index(current) + 1], stem
    assert all(checked.values()), checked


def test_breathing_phase_statements_never_offer_two_true_ones():
    inhale, exhale = set(INHALE_FACTS), set(EXHALE_FACTS)
    assert len(inhale) == len(exhale) >= 4
    assert not inhale & exhale
    seen = set()
    for seed in range(600):
        question = generate("body.breathing_mechanism_foundation", random.Random(seed))
        stem = _text(question.stem)
        phase = INHALE if f"“{INHALE}”" in stem else EXHALE
        seen.add(phase)
        mine, theirs = (inhale, exhale) if phase == INHALE else (exhale, inhale)
        assert _answer(question) in mine, stem
        others = {_text(c.content) for c in question.choices} - {_answer(question)}
        assert others <= theirs, stem
    assert seen == {INHALE, EXHALE}


def test_every_gas_movement_is_stored_once_and_read_both_ways():
    directions = [item.direction for item in EXCHANGES]
    assert len(directions) == len(set(directions)) == 4
    places = {item.place for item in EXCHANGES}
    gases = {item.gas for item in EXCHANGES}
    # Two places times two gases is exactly the space the indicator names.
    assert len(places) == len(gases) == 2
    by_direction = {item.direction: item for item in EXCHANGES}
    checked = {"forward": 0, "backward": 0}
    for seed in range(600):
        question = generate("body.gas_exchange_fluency", random.Random(seed))
        stem = _text(question.stem)
        answer = _answer(question)
        if answer in by_direction:
            checked["forward"] += 1
            item = next(x for x in EXCHANGES
                        if x.place in stem and f"“{x.gas}”" in stem)
            assert answer == item.direction, stem
            continue
        checked["backward"] += 1
        item = by_direction[next(d for d in by_direction if f"“{d}”" in stem)]
        assert answer == f"{item.place} {item.gas}", stem
    assert all(checked.values()), checked


def test_authored_scenario_banks_are_well_formed():
    for bank in (RESPIRATORY_SCENARIOS, BREATHING_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


def test_the_breathing_bank_reads_the_model_and_names_its_limits():
    """โดยใช้แบบจำลอง is in the indicator; an item can read a model, not build one."""
    joined = " ".join(f"{stem} {correct}"
                      for stem, correct, _ in BREATHING_SCENARIOS)
    assert "แบบจำลอง" in joined
    assert "ข้อจำกัด" in joined


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "body.respiratory_organs_foundation": 12,
        "body.respiratory_path_fluency": 6,
        "body.respiratory_application": 6,
        "body.breathing_mechanism_foundation": 8,
        "body.gas_exchange_fluency": 8,
        "body.breathing_application": 6,
    }
    for key, minimum in minimums.items():
        signatures = set()
        for seed in range(1000):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            assert question.hint, (key, seed)
            signatures.add((_text(question.stem), choices[question.answer]))
        assert len(signatures) >= minimum, (key, len(signatures))
