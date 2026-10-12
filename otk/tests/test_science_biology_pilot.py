"""Acceptance tests for the Phase 3 food-chain learning-path pilot."""

from __future__ import annotations

import random
import csv
from pathlib import Path

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_PILOT_KEYS
from otk.sets.biology.p5.food_chains import FOOD_CHAINS, ROLES


PILOT_KEYS = (
    "ecology.food_chain_foundation",
    "ecology.food_chain_fluency",
    "ecology.food_chain_application",
)
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_food_chain_pilot_is_additive_and_keeps_the_95_key_baseline_stable():
    assert set(PILOT_KEYS) <= SCIENCE_PILOT_KEYS
    assert len(SCIENCE_BASELINE_KEYS) == 95
    assert "ecology.feeding" in SCIENCE_BASELINE_KEYS
    assert not set(PILOT_KEYS) & SCIENCE_BASELINE_KEYS


def test_food_chain_pilot_shares_one_curriculum_node_with_three_real_stages():
    rows = {row["key"]: row for row in catalog()}
    pilot = [rows[key] for key in PILOT_KEYS]
    assert [row["learning_stage"] for row in pilot] == [1, 2, 3]
    assert len({row["curriculum_node_id"] for row in pilot}) == 1
    assert all(row["indicator_codes"] == ["ว 1.1 ป.5/3"] for row in pilot)
    assert pilot[1]["mapping_status"] == "exact"


def test_food_chain_outcome_is_marked_complete_with_all_contributing_keys():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        row = next(
            item for item in csv.DictReader(handle)
            if item["outcome_code"] == "ว 1.1 ป.5/3"
        )
    assert row["coverage_state"] == "complete"
    assert row["current_set_count"] == "4"
    assert set(row["current_set_keys"].split("; ")) == {"ecology.feeding", *PILOT_KEYS}


def test_foundation_identifies_every_role_in_every_authored_chain():
    seen = set()
    for seed in range(500):
        question = generate(PILOT_KEYS[0], random.Random(seed))
        stem = _text(question.stem)
        answer = _answer(question)
        for chain in FOOD_CHAINS:
            if chain.diagram not in stem:
                continue
            for index, role in enumerate(ROLES):
                if role in stem:
                    assert answer == chain.members[index]
                    seen.add((chain.habitat, role))
                    break
            break
    assert seen == {(chain.habitat, role) for chain in FOOD_CHAINS for role in ROLES}


def test_fluency_builds_chains_and_reasons_about_direct_changes():
    stems = []
    answers = []
    for seed in range(300):
        question = generate(PILOT_KEYS[1], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
        assert question.hint
    assert any("เขียนโซ่อาหารได้ถูกต้อง" in stem for stem in stems)
    assert any("แนวโน้มระยะสั้น" in stem for stem in stems)
    assert any("พลังงาน" in stem for stem in stems)
    assert any("ผู้บริโภคลำดับที่ 1" in answer for answer in answers)


def test_application_uses_before_after_evidence_and_two_step_explanations():
    stems = set()
    answers = []
    for seed in range(300):
        question = generate(PILOT_KEYS[2], random.Random(seed))
        stem = _text(question.stem)
        stems.add(stem)
        answers.append(_answer(question))
        assert "ก่อน→หลัง" in stem
        assert "→" in stem
        assert question.hint
    assert len(stems) >= 200
    assert any("อาหารน้อยลง" in answer and "ถูกกินน้อยลง" in answer for answer in answers)
    assert any("ถูกล่าน้อยลง" in answer and "กิน" in answer for answer in answers)
    assert any("ส่งผลต่อเนื่อง" in answer for answer in answers)


def test_two_hundred_seed_quality_gate_has_four_distinct_choices_each():
    for key in PILOT_KEYS:
        signatures = set()
        for seed in range(200):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4
            assert choices[question.answer]
            signatures.add((_text(question.stem), choices[question.answer]))
        minimum = 20 if key != PILOT_KEYS[2] else 150
        assert len(signatures) >= minimum
