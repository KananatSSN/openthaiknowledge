"""Acceptance tests for Wave B — the ม.2 reproductive and puberty block, ว 1.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m2.reproductive import EGG_PATH, FEMALE_ORGANS, MALE_ORGANS, SPERM_PATH
from otk.sets.biology.m2.sex_hormones_and_puberty import (
    FEMALE_CHANGES,
    FEMALE_HORMONE,
    HORMONE_FACTS,
    MALE_CHANGES,
    MALE_HORMONE,
    SHARED_CHANGES,
)
from otk.sets.biology.m2.puberty_care import PUBERTY_CARE, PUBERTY_NEEDS
from otk.sets._support.science_wave_b12 import (
    PUBERTY_CARE_SCENARIOS,
    PUBERTY_SCENARIOS,
    REPRODUCTIVE_SCENARIOS,
)


NEW_KEYS = {
    "body.reproductive_organs_foundation": ("ว 1.2 ม.2/12", 1, "standard_scope"),
    "body.reproductive_organs_fluency": ("ว 1.2 ม.2/12", 2, "standard_scope"),
    "body.reproductive_model_application": ("ว 1.2 ม.2/12", 3, "standard_scope"),
    "body.sex_hormone_foundation": ("ว 1.2 ม.2/13", 1, "standard_scope"),
    "body.puberty_change_fluency": ("ว 1.2 ม.2/13", 2, "exact"),
    "body.puberty_application": ("ว 1.2 ม.2/13", 3, "exact"),
    "body.puberty_care_foundation": ("ว 1.2 ม.2/14", 1, "standard_scope"),
    "body.puberty_care_fluency": ("ว 1.2 ม.2/14", 2, "standard_scope"),
    "body.puberty_care_application": ("ว 1.2 ม.2/14", 3, "standard_scope"),
}
COMPLETED = ("ว 1.2 ม.2/12", "ว 1.2 ม.2/13", "ว 1.2 ม.2/14")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_reproductive_and_puberty_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, status) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["mapping_status"] == status, key
        assert rows[key]["level"] == "ม.2", key


def test_a_tranak_indicator_whose_evidence_is_conduct_has_no_exact_set():
    """ม.2/14 says โดยการดูแลรักษาร่างกายและจิตใจ — conduct, not บอกแนวทาง."""
    rows = {row["key"]: row for row in catalog()}
    filed = {rows[key]["mapping_status"] for key, (code, _, _) in NEW_KEYS.items()
             if code == "ว 1.2 ม.2/14"}
    assert filed == {"standard_scope"}


def test_the_model_indicator_leaves_no_set_exact():
    """ม.2/12 ends in โดยใช้แบบจำลอง with no second half, as ม.2/7 does."""
    rows = {row["key"]: row for row in catalog()}
    filed = {rows[key]["mapping_status"] for key, (code, _, _) in NEW_KEYS.items()
             if code == "ว 1.2 ม.2/12"}
    assert filed == {"standard_scope"}


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


def test_the_two_reproductive_systems_are_kept_in_separate_tables():
    for organs in (MALE_ORGANS, FEMALE_ORGANS):
        assert len(organs) >= 4
        for field in ("name", "function"):
            values = [getattr(item, field) for item in organs]
            assert len(values) == len(set(values)), field
    assert not ({item.name for item in MALE_ORGANS}
                & {item.name for item in FEMALE_ORGANS})


def test_organ_answers_never_mix_the_two_systems():
    male = {item.name: item.function for item in MALE_ORGANS}
    female = {item.name: item.function for item in FEMALE_ORGANS}
    checked = {"male": 0, "female": 0}
    for seed in range(600):
        question = generate("body.reproductive_organs_foundation",
                            random.Random(seed))
        stem = _text(question.stem)
        offered = {_text(choice.content) for choice in question.choices}
        table = male if offered <= set(male) | set(male.values()) else female
        assert offered <= set(table) | set(table.values()), stem
        checked["male" if table is male else "female"] += 1
        name = next((key for key in table if f"“{key}”" in stem), None)
        if name is not None:
            assert _answer(question) == table[name], stem
        else:
            answer_name = next(key for key, value in table.items() if value in stem)
            assert _answer(question) == answer_name, stem
    assert all(checked.values()), checked


def test_each_sex_cell_follows_its_own_stored_path():
    assert SPERM_PATH[0] == "อัณฑะ" and SPERM_PATH[-1] == "ท่อปัสสาวะ"
    assert EGG_PATH[0] == "รังไข่" and EGG_PATH[-1] == "มดลูก"
    assert len(SPERM_PATH) == len(set(SPERM_PATH))
    assert len(EGG_PATH) == len(set(EGG_PATH))
    assert not set(SPERM_PATH) & set(EGG_PATH)
    checked = {"next": 0, "order": 0}
    for seed in range(600):
        question = generate("body.reproductive_organs_fluency", random.Random(seed))
        stem = _text(question.stem)
        path = SPERM_PATH if "เซลล์อสุจิ" in stem else EGG_PATH
        if "เรียงลำดับ" in stem:
            checked["order"] += 1
            assert _answer(question) == " → ".join(path), stem
            continue
        checked["next"] += 1
        current = next(name for name in path if f"“{name}”" in stem)
        assert _answer(question) == path[path.index(current) + 1], stem
    assert all(checked.values()), checked


def test_no_change_is_claimed_for_one_sex_when_it_belongs_to_both():
    male, female, shared = set(MALE_CHANGES), set(FEMALE_CHANGES), set(SHARED_CHANGES)
    assert len(male) == len(female) >= 4
    assert not male & female
    assert not shared & (male | female)
    assert len(shared) >= 3
    checked = {"male": 0, "female": 0, "shared": 0}
    for seed in range(600):
        question = generate("body.puberty_change_fluency", random.Random(seed))
        stem = _text(question.stem)
        offered = {_text(choice.content) for choice in question.choices}
        if "ทั้งในเพศชาย" in stem:
            checked["shared"] += 1
            assert _answer(question) in shared, stem
            # Sex-specific changes fill the wrong choices, never another shared one.
            assert offered - {_answer(question)} <= male | female, stem
            continue
        if f"“{MALE_HORMONE}”" in stem:
            checked["male"] += 1
            mine, theirs = male, female
        else:
            assert f"“{FEMALE_HORMONE}”" in stem, stem
            checked["female"] += 1
            mine, theirs = female, male
        assert _answer(question) in mine, stem
        assert offered - {_answer(question)} <= theirs, stem
    assert all(checked.values()), checked


def test_hormone_facts_have_one_answer_each():
    questions = [item.question for item in HORMONE_FACTS]
    answers = [item.answer for item in HORMONE_FACTS]
    assert len(questions) == len(set(questions)) >= 5
    assert len(answers) == len(set(answers)) == len(questions)


def test_every_puberty_situation_is_answered_by_a_practice_from_the_table():
    practices = {item.practice for item in PUBERTY_CARE}
    answered = [need.practice for need in PUBERTY_NEEDS]
    assert set(answered) <= practices
    assert len(answered) == len(set(answered)) >= 5
    wanted = {need.situation: need.practice for need in PUBERTY_NEEDS}
    for seed in range(600):
        question = generate("body.puberty_care_fluency", random.Random(seed))
        stem = _text(question.stem)
        offered = {_text(choice.content) for choice in question.choices}
        assert offered <= practices, stem
        assert _answer(question) == wanted[stem], stem


def test_authored_scenario_banks_are_well_formed():
    for bank in (REPRODUCTIVE_SCENARIOS, PUBERTY_SCENARIOS, PUBERTY_CARE_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


def test_the_reproductive_bank_reads_the_model_and_names_its_limits():
    joined = " ".join(f"{stem} {correct}"
                      for stem, correct, _ in REPRODUCTIVE_SCENARIOS)
    assert "แบบจำลอง" in joined
    assert "ข้อจำกัด" in joined


def test_the_puberty_banks_say_that_timing_differs_between_people():
    """"Everyone changes at a different time" is the misconception worth fixing."""
    joined = " ".join(correct for _, correct, _ in PUBERTY_SCENARIOS)
    assert "ต่างกันไปในแต่ละคน" in joined or "ต่างกันไปในแต่ละบุคคล" in joined
    assert "ไม่ได้แสดงว่าคนใดผิดปกติ" in joined


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "body.reproductive_organs_foundation": 20,
        "body.reproductive_organs_fluency": 7,
        "body.reproductive_model_application": 6,
        "body.sex_hormone_foundation": 6,
        "body.puberty_change_fluency": 12,
        "body.puberty_application": 6,
        "body.puberty_care_foundation": 12,
        "body.puberty_care_fluency": 6,
        "body.puberty_care_application": 6,
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
