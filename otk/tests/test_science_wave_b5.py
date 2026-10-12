"""Acceptance tests for Wave B — the ม.1 plant reproduction pair, ว 1.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m1.flowers_fruits_and_seeds import (
    AFTER_FERTILISATION,
    FLOWER_PARTS,
    INSECT_FLOWER_FACTS,
    WIND_FLOWER_FACTS,
)
from otk.sets.biology.m1.reproduction import (
    ASEXUAL,
    ASEXUAL_FACTS,
    PROPAGULES,
    PROPAGULE_STRUCTURES,
    SEXUAL,
    SEXUAL_FACTS,
)
from otk.sets._support.science_wave_b5 import REPRODUCTION_SCENARIOS, SEED_SCENARIOS


NEW_KEYS = {
    "plant.reproduction_foundation": ("ว 1.2 ม.1/11", 1),
    "plant.reproduction_fluency": ("ว 1.2 ม.1/11", 2),
    "plant.reproduction_application": ("ว 1.2 ม.1/11", 3),
    "plant.flower_parts_foundation": ("ว 1.2 ม.1/12", 1),
    "plant.pollination_fluency": ("ว 1.2 ม.1/12", 2),
    "plant.seed_application": ("ว 1.2 ม.1/12", 3),
}
COMPLETED = ("ว 1.2 ม.1/11", "ว 1.2 ม.1/12")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_reproduction_sets_are_additive_and_correctly_staged():
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


def test_the_two_fact_lists_are_the_same_size_and_share_nothing():
    """A shared statement would be true of both modes, and the item unanswerable."""
    assert len(SEXUAL_FACTS) == len(ASEXUAL_FACTS) >= 4
    assert not set(SEXUAL_FACTS) & set(ASEXUAL_FACTS)
    assert len(INSECT_FLOWER_FACTS) == len(WIND_FLOWER_FACTS) >= 4
    assert not set(INSECT_FLOWER_FACTS) & set(WIND_FLOWER_FACTS)


def test_mode_statements_never_offer_two_true_ones():
    sexual, asexual = set(SEXUAL_FACTS), set(ASEXUAL_FACTS)
    seen = set()
    for seed in range(600):
        question = generate("plant.reproduction_foundation", random.Random(seed))
        stem = _text(question.stem)
        mode = SEXUAL if f"“{SEXUAL}”" in stem else ASEXUAL
        seen.add(mode)
        mine, theirs = (sexual, asexual) if mode == SEXUAL else (asexual, sexual)
        assert _answer(question) in mine, stem
        others = {_text(c.content) for c in question.choices} - {_answer(question)}
        assert others <= theirs, stem
    assert seen == {SEXUAL, ASEXUAL}


def test_propagule_answers_stay_single_when_two_plants_share_a_structure():
    """ขิง and ข่า both use a เหง้า, so neither may appear as the other's distractor."""
    by_plant = {item.plant: item.structure for item in PROPAGULES}
    shared = [s for s in PROPAGULE_STRUCTURES
              if len([p for p in PROPAGULES if p.structure == s]) > 1]
    assert shared, "the guard below is only meaningful if some structure is shared"
    checked = {"structure": 0, "plant": 0}
    for seed in range(900):
        question = generate("plant.reproduction_fluency", random.Random(seed))
        stem = _text(question.stem)
        plant = next((name for name in by_plant if f"“{name}”" in stem), None)
        if plant is not None:
            checked["structure"] += 1
            assert _answer(question) == by_plant[plant], stem
            continue
        checked["plant"] += 1
        structure = next(name for name in PROPAGULE_STRUCTURES if f"“{name}”" in stem)
        assert by_plant[_answer(question)] == structure, stem
        others = {_text(c.content) for c in question.choices} - {_answer(question)}
        # No distractor may be another plant that also uses this structure.
        assert all(by_plant[name] != structure for name in others), stem
    assert all(checked.values()), checked


def test_flower_part_answers_come_from_the_table_in_both_directions():
    by_name = {item.name: item.function for item in FLOWER_PARTS}
    by_function = {item.function: item.name for item in FLOWER_PARTS}
    assert len(by_name) == len(by_function) == len(FLOWER_PARTS) >= 8
    checked = {"name": 0, "function": 0}
    for seed in range(600):
        question = generate("plant.flower_parts_foundation", random.Random(seed))
        stem = _text(question.stem)
        name = next((key for key in by_name if f"“{key}”" in stem), None)
        if name is not None:
            checked["name"] += 1
            assert _answer(question) == by_name[name], stem
            continue
        checked["function"] += 1
        function = next(key for key in by_function if key in stem)
        assert _answer(question) == by_function[function], stem
    assert all(checked.values()), checked


def test_pollination_and_fertilisation_answers_are_read_off_their_tables():
    insect, wind = set(INSECT_FLOWER_FACTS), set(WIND_FLOWER_FACTS)
    becomes = dict(AFTER_FERTILISATION)
    assert len(becomes) == len(AFTER_FERTILISATION) >= 4
    assert len(set(becomes.values())) == len(becomes)
    checked = {"insect": 0, "wind": 0, "becomes": 0}
    for seed in range(900):
        question = generate("plant.pollination_fluency", random.Random(seed))
        stem = _text(question.stem)
        answer = _answer(question)
        if "ถ่ายเรณูโดยแมลง" in stem:
            checked["insect"] += 1
            assert answer in insect, stem
            assert {_text(c.content) for c in question.choices} - {answer} <= wind
        elif "ถ่ายเรณูโดยลม" in stem:
            checked["wind"] += 1
            assert answer in wind, stem
            assert {_text(c.content) for c in question.choices} - {answer} <= insect
        else:
            checked["becomes"] += 1
            before = next(key for key in becomes if f"“{key}”" in stem)
            assert answer == becomes[before], stem
    assert all(checked.values()), checked


def test_authored_scenario_banks_are_well_formed():
    for bank in (REPRODUCTION_SCENARIOS, SEED_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "plant.reproduction_foundation": 8,
        "plant.reproduction_fluency": 18,
        "plant.reproduction_application": 6,
        "plant.flower_parts_foundation": 16,
        "plant.pollination_fluency": 12,
        "plant.seed_application": 6,
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
