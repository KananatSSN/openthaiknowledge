"""Acceptance tests for Wave B — the ม.1 photosynthesis pair, ว 1.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m1.photosynthesis import EXPERIMENTS, FACTORS, NEITHER, PRODUCTS
from otk.sets.biology.m1.photosynthesis_importance import IMPORTANCE_CHANGES
from otk.sets._support.science_wave_b3 import IMPORTANCE_SCENARIOS, PHOTOSYNTHESIS_SCENARIOS


NEW_KEYS = {
    "plant.photosynthesis_foundation": ("ว 1.2 ม.1/6", 1),
    "plant.photosynthesis_fluency": ("ว 1.2 ม.1/6", 2),
    "plant.photosynthesis_application": ("ว 1.2 ม.1/6", 3),
    "plant.photosynthesis_importance_foundation": ("ว 1.2 ม.1/7", 1),
    "plant.photosynthesis_importance_fluency": ("ว 1.2 ม.1/7", 2),
    "plant.photosynthesis_importance_application": ("ว 1.2 ม.1/7", 3),
}
COMPLETED = ("ว 1.2 ม.1/6", "ว 1.2 ม.1/7")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_photosynthesis_sets_are_additive_and_correctly_staged():
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


def test_the_three_lists_are_disjoint_and_large_enough_to_ask_from():
    """A thing that is both a factor and a distractor would have two answers."""
    assert set(FACTORS) == {"แสง", "คลอโรฟิลล์", "น้ำ", "แก๊สคาร์บอนไดออกไซด์"}
    assert set(PRODUCTS) == {"น้ำตาลกลูโคส", "แก๊สออกซิเจน"}
    lists = (set(FACTORS), set(PRODUCTS), set(NEITHER))
    assert sum(len(item) for item in lists) == len(set().union(*lists))
    # Each of the three question directions needs three wrongs from the rest.
    assert len(PRODUCTS) + len(NEITHER) >= 3
    assert len(FACTORS) + len(NEITHER) >= 3
    assert len(FACTORS) + len(PRODUCTS) >= 3


def test_foundation_answers_always_come_from_the_list_the_stem_asks_for():
    wanted = {
        "ปัจจัยที่จำเป็น": set(FACTORS),
        "ผลผลิตที่ได้": set(PRODUCTS),
        "ไม่ใช่ทั้งปัจจัยและผลผลิต": set(NEITHER),
    }
    checked = dict.fromkeys(wanted, 0)
    for seed in range(900):
        question = generate("plant.photosynthesis_foundation", random.Random(seed))
        stem = _text(question.stem)
        phrase = next(key for key in wanted if key in stem)
        checked[phrase] += 1
        assert _answer(question) in wanted[phrase], stem
        # And no other choice may also belong to the asked list.
        others = {_text(c.content) for c in question.choices} - {_answer(question)}
        assert not others & wanted[phrase], stem
    assert all(checked.values()), checked


def test_every_experiment_changes_one_named_factor():
    factors = {item.factor for item in EXPERIMENTS}
    assert factors <= set(FACTORS), factors
    setups = [item.setup for item in EXPERIMENTS]
    results = [item.result for item in EXPERIMENTS]
    assert len(setups) == len(set(setups)) >= 4
    # Two setups sharing a result would make the result direction ambiguous.
    assert len(results) == len(set(results))


def test_experiment_answers_are_read_off_the_setup_in_the_stem():
    by_setup = {item.setup: item for item in EXPERIMENTS}
    checked = {"factor": 0, "result": 0}
    for seed in range(900):
        question = generate("plant.photosynthesis_fluency", random.Random(seed))
        stem = _text(question.stem)
        item = next(value for setup, value in by_setup.items() if setup in stem)
        if "ตรวจสอบปัจจัยใด" in stem:
            checked["factor"] += 1
            assert _answer(question) == item.factor, stem
            # Wrong factors may also be things that are not factors at all (``NEITHER``).
            assert {_text(c.content) for c in question.choices} <= set(FACTORS) | set(NEITHER), stem
        else:
            checked["result"] += 1
            assert _answer(question) == item.result, stem
    assert all(checked.values()), checked


def test_importance_wrong_choices_are_real_effects_of_a_different_change():
    changes = dict(IMPORTANCE_CHANGES)
    effects = {effect: change for change, effect in IMPORTANCE_CHANGES}
    assert len(changes) == len(effects) == len(IMPORTANCE_CHANGES) >= 4
    checked = {"forward": 0, "backward": 0}
    for seed in range(900):
        question = generate("plant.photosynthesis_importance_fluency",
                            random.Random(seed))
        stem = _text(question.stem)
        answer = _answer(question)
        offered = {_text(choice.content) for choice in question.choices}
        if "จะส่งผลอย่างไร" in stem:
            checked["forward"] += 1
            change = next(key for key in changes if f"“{key}”" in stem)
            assert answer == changes[change], stem
            # Every distractor is another row's real effect, not an invention.
            assert offered <= set(effects), stem
        else:
            checked["backward"] += 1
            effect = next(key for key in effects if f"“{key}”" in stem)
            assert answer == effects[effect], stem
            assert offered <= set(changes), stem
    assert all(checked.values()), checked


def test_authored_scenario_banks_are_well_formed():
    for bank in (PHOTOSYNTHESIS_SCENARIOS, IMPORTANCE_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "plant.photosynthesis_foundation": 10,
        "plant.photosynthesis_fluency": 8,
        "plant.photosynthesis_application": 6,
        "plant.photosynthesis_importance_foundation": 7,
        "plant.photosynthesis_importance_fluency": 10,
        "plant.photosynthesis_importance_application": 6,
    }
    concept_banks = {"plant.photosynthesis_importance_foundation"}
    for key, minimum in minimums.items():
        signatures = set()
        for seed in range(1000):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            # A ``Concept`` is a stem, an answer and its distractors; it carries
            # no hint by design, so only the generated sets are held to one.
            if key not in concept_banks:
                assert question.hint, (key, seed)
            signatures.add((_text(question.stem), choices[question.answer]))
        assert len(signatures) >= minimum, (key, len(signatures))
