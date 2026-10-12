"""Acceptance tests for Wave B — the ม.2 nervous system block, ว 1.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m2.circulatory_care import CIRCULATORY_CARE, CIRCULATORY_NEEDS
from otk.sets._support.science_wave_b11 import (
    CIRCULATORY_CARE_SCENARIOS,
    NERVOUS_CARE_SCENARIOS,
    NERVOUS_SCENARIOS,
)
from otk.sets.biology.m2.central_nervous_system_organs import CONTROLLED, NERVE_PARTS
from otk.sets.biology.m2.nervous_care import NERVOUS_CARE, NERVOUS_NEEDS


NEW_KEYS = {
    "body.circulatory_care_foundation": ("ว 1.2 ม.2/9", 1, "standard_scope"),
    "body.circulatory_care_fluency": ("ว 1.2 ม.2/9", 2, "exact"),
    "body.circulatory_care_application": ("ว 1.2 ม.2/9", 3, "standard_scope"),
    "body.nervous_organs_foundation": ("ว 1.2 ม.2/10", 1, "standard_scope"),
    "body.nervous_control_fluency": ("ว 1.2 ม.2/10", 2, "exact"),
    "body.nervous_application": ("ว 1.2 ม.2/10", 3, "exact"),
    "body.nervous_care_foundation": ("ว 1.2 ม.2/11", 1, "standard_scope"),
    "body.nervous_care_fluency": ("ว 1.2 ม.2/11", 2, "exact"),
    "body.nervous_care_application": ("ว 1.2 ม.2/11", 3, "standard_scope"),
}
COMPLETED = ("ว 1.2 ม.2/9", "ว 1.2 ม.2/10", "ว 1.2 ม.2/11")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_nervous_and_care_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, status) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["mapping_status"] == status, key
        assert rows[key]["level"] == "ม.2", key


def test_each_bok_naewthang_indicator_has_exactly_one_exact_set():
    rows = {row["key"]: row for row in catalog()}
    for outcome in ("ว 1.2 ม.2/9", "ว 1.2 ม.2/11"):
        exact = {key for key, (code, _, _) in NEW_KEYS.items()
                 if code == outcome and rows[key]["mapping_status"] == "exact"}
        assert len(exact) == 1, outcome
        assert rows[exact.pop()]["learning_stage"] == 2, outcome


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


def test_every_care_table_is_a_one_to_one_practice_and_reason_table():
    for cares in (CIRCULATORY_CARE, NERVOUS_CARE):
        assert len(cares) >= 4
        for field in ("practice", "reason"):
            values = [getattr(item, field) for item in cares]
            assert len(values) == len(set(values)), field


def test_every_situation_is_answered_by_a_practice_from_its_own_table():
    for needs, cares in ((CIRCULATORY_NEEDS, CIRCULATORY_CARE),
                         (NERVOUS_NEEDS, NERVOUS_CARE)):
        practices = {item.practice for item in cares}
        answered = [need.practice for need in needs]
        assert set(answered) <= practices
        assert len(answered) == len(set(answered))
        assert len({need.situation for need in needs}) == len(needs) >= 5


def test_care_fluency_answers_the_situation_and_offers_only_real_practices():
    for key, needs, cares in (
        ("body.circulatory_care_fluency", CIRCULATORY_NEEDS, CIRCULATORY_CARE),
        ("body.nervous_care_fluency", NERVOUS_NEEDS, NERVOUS_CARE),
    ):
        wanted = {need.situation: need.practice for need in needs}
        practices = {item.practice for item in cares}
        seen = set()
        for seed in range(600):
            question = generate(key, random.Random(seed))
            stem = _text(question.stem)
            seen.add(stem)
            offered = {_text(choice.content) for choice in question.choices}
            assert offered <= practices, stem
            assert _answer(question) == wanted[stem], stem
        assert seen == set(wanted)


def test_the_central_nervous_system_table_holds_exactly_its_four_organs():
    """Four organs is what lets "which one controls this" offer all of them."""
    names = [item.name for item in NERVE_PARTS]
    functions = [item.function for item in NERVE_PARTS]
    assert len(names) == len(set(names)) == 4
    assert len(functions) == len(set(functions))
    # Peripheral nerves and sense organs are outside ม.2/10 and must not appear.
    joined = " ".join(f"{item.name} {item.function}" for item in NERVE_PARTS)
    for outside in ("ประสาทส่วนปลาย", "อวัยวะรับความรู้สึก"):
        assert outside not in joined, outside


def test_every_controlled_action_names_an_organ_from_the_table():
    organs = {item.name for item in NERVE_PARTS}
    actions = [action for action, _ in CONTROLLED]
    assert len(actions) == len(set(actions)) >= 6
    assert {part for _, part in CONTROLLED} == organs, "each organ is asked about"
    by_action = dict(CONTROLLED)
    seen = set()
    for seed in range(600):
        question = generate("body.nervous_control_fluency", random.Random(seed))
        stem = _text(question.stem)
        action = next(name for name in by_action if f"“{name}”" in stem)
        seen.add(action)
        offered = {_text(choice.content) for choice in question.choices}
        assert offered == organs, stem
        assert _answer(question) == by_action[action], stem
    assert seen == set(by_action)


def test_authored_scenario_banks_are_well_formed():
    for bank in (CIRCULATORY_CARE_SCENARIOS, NERVOUS_SCENARIOS,
                 NERVOUS_CARE_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


def test_the_nervous_care_bank_says_why_the_damage_is_permanent():
    """A precaution with no consequence attached is a slogan, not an understanding."""
    joined = " ".join(correct for _, correct, _ in NERVOUS_CARE_SCENARIOS)
    assert "สร้างทดแทนได้ยาก" in joined


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "body.circulatory_care_foundation": 12,
        "body.circulatory_care_fluency": 6,
        "body.circulatory_care_application": 6,
        "body.nervous_organs_foundation": 8,
        "body.nervous_control_fluency": 8,
        "body.nervous_application": 6,
        "body.nervous_care_foundation": 12,
        "body.nervous_care_fluency": 6,
        "body.nervous_care_application": 6,
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
