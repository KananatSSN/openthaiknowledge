"""Acceptance tests for Wave B — the ม.2 excretory and care block, ว 1.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m2.excretory_care import EXCRETORY_CARE, EXCRETORY_NEEDS
from otk.sets._support.science_wave_b9 import (
    EXCRETORY_CARE_SCENARIOS,
    EXCRETORY_SCENARIOS,
    RESPIRATORY_CARE_SCENARIOS,
)
from otk.sets.biology.m2.excretory_system import EXCRETORY_ORGANS, SUBSTANCES, URINE_PATH
from otk.sets.biology.m2.respiratory_care import RESPIRATORY_CARE, RESPIRATORY_NEEDS


NEW_KEYS = {
    "body.respiratory_care_foundation": ("ว 1.2 ม.2/3", 1, "standard_scope"),
    "body.respiratory_care_fluency": ("ว 1.2 ม.2/3", 2, "exact"),
    "body.respiratory_care_application": ("ว 1.2 ม.2/3", 3, "standard_scope"),
    "body.excretory_organs_foundation": ("ว 1.2 ม.2/4", 1, "standard_scope"),
    "body.urine_path_fluency": ("ว 1.2 ม.2/4", 2, "exact"),
    "body.excretory_application": ("ว 1.2 ม.2/4", 3, "exact"),
    "body.excretory_care_foundation": ("ว 1.2 ม.2/5", 1, "standard_scope"),
    "body.excretory_care_fluency": ("ว 1.2 ม.2/5", 2, "exact"),
    "body.excretory_care_application": ("ว 1.2 ม.2/5", 3, "standard_scope"),
}
COMPLETED = ("ว 1.2 ม.2/3", "ว 1.2 ม.2/4", "ว 1.2 ม.2/5")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_excretory_and_care_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, status) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["mapping_status"] == status, key
        assert rows[key]["level"] == "ม.2", key


def test_only_the_bok_naewthang_set_claims_exact_in_a_tranak_topic():
    """ม.2/3 and ม.2/5 say โดยการบอกแนวทาง — stating it is what an item can do."""
    rows = {row["key"]: row for row in catalog()}
    for outcome in ("ว 1.2 ม.2/3", "ว 1.2 ม.2/5"):
        filed = {key: rows[key]["mapping_status"]
                 for key, (code, _, _) in NEW_KEYS.items() if code == outcome}
        exact = {key for key, status in filed.items() if status == "exact"}
        assert len(exact) == 1, (outcome, filed)
        assert rows[exact.pop()]["learning_stage"] == 2, outcome


def test_no_tranak_outcome_whose_evidence_is_conduct_claims_exact():
    """ดูแลรักษาร่างกาย / ประพฤติตน / มีส่วนร่วม cannot be observed by an item."""
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        outcomes = {row["outcome_code"]: row["official_text"]
                    for row in csv.DictReader(handle)}
    conduct = ("โดยการดูแลรักษาร่างกาย", "โดยการประพฤติตน", "โดยมีส่วนร่วม",
               "โดยการนำความรู้ไปใช้")
    for row in catalog():
        if row["mapping_status"] != "exact":
            continue
        for code in row["indicator_codes"] or ():
            text = outcomes.get(code, "")
            assert not any(phrase in text for phrase in conduct), (row["key"], code)


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
    for cares in (RESPIRATORY_CARE, EXCRETORY_CARE):
        assert len(cares) >= 4
        for field in ("practice", "reason"):
            values = [getattr(item, field) for item in cares]
            # A shared reason would make the reverse direction ambiguous.
            assert len(values) == len(set(values)), field


def test_every_situation_is_answered_by_a_practice_from_its_own_table():
    """A แนวทาง that is not in the pool cannot be offered as a choice."""
    for needs, cares in ((RESPIRATORY_NEEDS, RESPIRATORY_CARE),
                         (EXCRETORY_NEEDS, EXCRETORY_CARE)):
        practices = {item.practice for item in cares}
        answered = [need.practice for need in needs]
        assert set(answered) <= practices
        # Two situations sharing an answer would make one of them un-diagnostic.
        assert len(answered) == len(set(answered))
        assert len({need.situation for need in needs}) == len(needs) >= 5


def test_care_answers_are_read_off_the_care_table_in_both_directions():
    for key, cares in (("body.respiratory_care_foundation", RESPIRATORY_CARE),
                       ("body.excretory_care_foundation", EXCRETORY_CARE)):
        reasons = {item.practice: item.reason for item in cares}
        by_reason = {item.reason: item.practice for item in cares}
        checked = {"reason": 0, "practice": 0}
        for seed in range(600):
            question = generate(key, random.Random(seed))
            stem = _text(question.stem)
            practice = next((name for name in reasons if f"“{name}”" in stem), None)
            if practice is not None:
                checked["reason"] += 1
                assert _answer(question) == reasons[practice], stem
                continue
            checked["practice"] += 1
            reason = next(name for name in by_reason if name in stem)
            assert _answer(question) == by_reason[reason], stem
        assert all(checked.values()), (key, checked)


def test_care_fluency_answers_the_situation_and_offers_only_real_practices():
    for key, needs, cares in (
        ("body.respiratory_care_fluency", RESPIRATORY_NEEDS, RESPIRATORY_CARE),
        ("body.excretory_care_fluency", EXCRETORY_NEEDS, EXCRETORY_CARE),
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


def test_the_urine_path_runs_from_the_kidney_out():
    assert URINE_PATH[0] == "ไต" and URINE_PATH[-1] == "ท่อปัสสาวะ"
    assert len(URINE_PATH) == len(set(URINE_PATH)) >= 4
    assert URINE_PATH.index("ท่อไต") < URINE_PATH.index("กระเพาะปัสสาวะ")
    for field in ("name", "function"):
        values = [getattr(item, field) for item in EXCRETORY_ORGANS]
        assert len(values) == len(set(values)), field
    assert {item.name for item in EXCRETORY_ORGANS} >= set(URINE_PATH)


def test_every_substance_has_one_fate_and_the_three_fates_are_all_represented():
    fates = [item.fate for item in SUBSTANCES]
    assert len(fates) == len(set(fates)) == len(SUBSTANCES) >= 4
    joined = " ".join(fates)
    # Filtered and excreted, filtered and reabsorbed, too large to be filtered.
    assert "ขับออกไปกับปัสสาวะ" in joined
    assert "ดูดกลับ" in joined
    assert "ใหญ่เกินกว่าจะผ่านการกรอง" in joined


def test_urine_path_answers_are_read_off_the_one_stored_order():
    fates = {item.name: item.fate for item in SUBSTANCES}
    checked = {"next": 0, "order": 0, "fate": 0}
    for seed in range(600):
        question = generate("body.urine_path_fluency", random.Random(seed))
        stem = _text(question.stem)
        if "เรียงลำดับ" in stem:
            checked["order"] += 1
            assert _answer(question) == " → ".join(URINE_PATH), stem
            continue
        if "หน่วยไต" in stem:
            checked["fate"] += 1
            name = next(key for key in fates if f"“{key}”" in stem)
            assert _answer(question) == fates[name], stem
            continue
        checked["next"] += 1
        current = next(name for name in URINE_PATH if f"“{name}”" in stem)
        assert _answer(question) == URINE_PATH[URINE_PATH.index(current) + 1], stem
    assert all(checked.values()), checked


def test_authored_scenario_banks_are_well_formed():
    for bank in (RESPIRATORY_CARE_SCENARIOS, EXCRETORY_SCENARIOS,
                 EXCRETORY_CARE_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "body.respiratory_care_foundation": 12,
        "body.respiratory_care_fluency": 6,
        "body.respiratory_care_application": 6,
        "body.excretory_organs_foundation": 12,
        "body.urine_path_fluency": 9,
        "body.excretory_application": 6,
        "body.excretory_care_foundation": 12,
        "body.excretory_care_fluency": 6,
        "body.excretory_care_application": 6,
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
