"""Acceptance tests for Wave B — the ม.2 pregnancy block, which closes ว 1.2 ม.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m2.teen_pregnancy import CONDUCTS, IMPACTS
from otk.sets.biology.m2.contraception import CONTRACEPTION
from otk.sets._support.science_wave_b13 import (
    CONTRACEPTION_SCENARIOS,
    PREGNANCY_SCENARIOS,
    TEEN_PREGNANCY_SCENARIOS,
)
from otk.sets.biology.m2.menstrual_cycle_and_pregnancy import EVENTS, PREGNANCY_ORDER


NEW_KEYS = {
    "body.reproductive_cycle_foundation": ("ว 1.2 ม.2/15", 1, "standard_scope"),
    "body.fertilisation_fluency": ("ว 1.2 ม.2/15", 2, "exact"),
    "body.pregnancy_application": ("ว 1.2 ม.2/15", 3, "exact"),
    "body.contraception_foundation": ("ว 1.2 ม.2/16", 1, "standard_scope"),
    "body.contraception_fluency": ("ว 1.2 ม.2/16", 2, "standard_scope"),
    "body.contraception_application": ("ว 1.2 ม.2/16", 3, "exact"),
    "body.teen_pregnancy_foundation": ("ว 1.2 ม.2/17", 1, "standard_scope"),
    "body.teen_pregnancy_fluency": ("ว 1.2 ม.2/17", 2, "standard_scope"),
    "body.teen_pregnancy_application": ("ว 1.2 ม.2/17", 3, "standard_scope"),
}
COMPLETED = ("ว 1.2 ม.2/15", "ว 1.2 ม.2/16", "ว 1.2 ม.2/17")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_pregnancy_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, status) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["mapping_status"] == status, key
        assert rows[key]["level"] == "ม.2", key


def test_the_choosing_indicator_is_filed_the_same_way_as_its_precedent():
    """ม.2/16 has the same verb as ว 1.2 ม.1/16, so only Application is exact."""
    rows = {row["key"]: row for row in catalog()}
    exact = {key for key, (code, _, _) in NEW_KEYS.items()
             if code == "ว 1.2 ม.2/16" and rows[key]["mapping_status"] == "exact"}
    assert exact == {"body.contraception_application"}
    precedent = rows["plant.propagation_application"]["mapping_status"]
    assert precedent == "exact", "the ม.1/16 precedent this follows"


def test_a_tranak_indicator_whose_evidence_is_conduct_has_no_exact_set():
    rows = {row["key"]: row for row in catalog()}
    filed = {rows[key]["mapping_status"] for key, (code, _, _) in NEW_KEYS.items()
             if code == "ว 1.2 ม.2/17"}
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


def test_wave_b_leaves_no_incomplete_indicator_in_wo_one_two_mo_two():
    """The closing condition of this block: all seventeen ม.2 indicators covered."""
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        rows = [row for row in csv.DictReader(handle)
                if row["outcome_code"].startswith("ว 1.2 ม.2/")]
    assert len(rows) == 17
    incomplete = [row["outcome_code"] for row in rows
                  if row["coverage_state"] != "complete"]
    assert not incomplete, incomplete


def test_the_event_table_and_the_order_agree():
    names = [item.name for item in EVENTS]
    descriptions = [item.description for item in EVENTS]
    assert len(names) == len(set(names)) >= 5
    assert len(descriptions) == len(set(descriptions))
    assert set(PREGNANCY_ORDER) <= set(names)
    # Menstruation is the other branch, so it is deliberately not on this path.
    assert "การมีประจำเดือน" not in PREGNANCY_ORDER
    assert PREGNANCY_ORDER[0] == "การตกไข่" and PREGNANCY_ORDER[-1] == "การคลอด"
    assert (PREGNANCY_ORDER.index("การปฏิสนธิ")
            < PREGNANCY_ORDER.index("การฝังตัว"))


def test_both_branches_after_ovulation_are_asked_and_answered_correctly():
    checked = {"next": 0, "order": 0, "fertilised": 0, "not_fertilised": 0}
    for seed in range(600):
        question = generate("body.fertilisation_fluency", random.Random(seed))
        stem = _text(question.stem)
        answer = _answer(question)
        if "เรียงลำดับ" in stem:
            checked["order"] += 1
            assert answer == " → ".join(PREGNANCY_ORDER), stem
            continue
        if "ถ้าเซลล์ไข่ได้รับการปฏิสนธิ" in stem:
            checked["fertilised"] += 1
            assert "ฝังตัว" in answer, stem
            continue
        if "ถ้าเซลล์ไข่ไม่ได้รับการปฏิสนธิ" in stem:
            checked["not_fertilised"] += 1
            assert "ประจำเดือน" in answer, stem
            continue
        checked["next"] += 1
        current = next(name for name in PREGNANCY_ORDER if f"“{name}”" in stem)
        index = PREGNANCY_ORDER.index(current)
        assert answer == PREGNANCY_ORDER[index + 1], stem
    assert all(checked.values()), checked


def test_no_two_contraceptive_methods_answer_the_same_need():
    """Two methods sharing a need would give the situation two right answers."""
    assert len(CONTRACEPTION) >= 5
    for field in ("name", "mechanism", "best_for"):
        values = [getattr(item, field) for item in CONTRACEPTION]
        assert len(values) == len(set(values)), field


def test_contraception_answers_come_from_the_table_in_every_direction():
    mechanisms = {item.name: item.mechanism for item in CONTRACEPTION}
    by_mechanism = {item.mechanism: item.name for item in CONTRACEPTION}
    needs = {item.name: item.best_for for item in CONTRACEPTION}
    by_need = {item.best_for: item.name for item in CONTRACEPTION}
    checked = {"mechanism": 0, "which": 0, "need": 0, "choose": 0}
    for seed in range(600):
        question = generate("body.contraception_foundation", random.Random(seed))
        stem = _text(question.stem)
        name = next((key for key in mechanisms if f"“{key}”" in stem), None)
        if name is not None:
            checked["mechanism"] += 1
            assert _answer(question) == mechanisms[name], stem
        else:
            checked["which"] += 1
            mechanism = next(key for key in by_mechanism if key in stem)
            assert _answer(question) == by_mechanism[mechanism], stem
    for seed in range(600):
        question = generate("body.contraception_fluency", random.Random(seed))
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


def test_every_impact_and_every_course_of_action_is_distinct():
    for field in ("aspect", "effect"):
        values = [getattr(item, field) for item in IMPACTS]
        assert len(values) == len(set(values)) >= 5, field
    situations = [item.situation for item in CONDUCTS]
    actions = [item.action for item in CONDUCTS]
    assert len(situations) == len(set(situations)) >= 5
    assert len(actions) == len(set(actions)) == len(situations)


def test_the_conduct_item_answers_the_situation_from_its_own_table():
    wanted = {item.situation: item.action for item in CONDUCTS}
    actions = set(wanted.values())
    seen = set()
    for seed in range(600):
        question = generate("body.teen_pregnancy_fluency", random.Random(seed))
        stem = _text(question.stem)
        seen.add(stem)
        offered = {_text(choice.content) for choice in question.choices}
        # Every wrong choice is another real course of action, not a bad one.
        assert offered <= actions, stem
        assert _answer(question) == wanted[stem], stem
    assert seen == set(wanted)


def test_authored_scenario_banks_are_well_formed():
    for bank in (PREGNANCY_SCENARIOS, CONTRACEPTION_SCENARIOS,
                 TEEN_PREGNANCY_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


def test_the_pregnancy_bank_spans_all_four_things_the_indicator_names():
    joined = " ".join(f"{stem} {correct}"
                      for stem, correct, _ in PREGNANCY_SCENARIOS)
    for topic in ("ตกไข่", "ประจำเดือน", "ปฏิสนธิ", "ตั้งครรภ์"):
        assert topic in joined, topic


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "body.reproductive_cycle_foundation": 12,
        "body.fertilisation_fluency": 7,
        "body.pregnancy_application": 6,
        "body.contraception_foundation": 12,
        "body.contraception_fluency": 12,
        "body.contraception_application": 6,
        "body.teen_pregnancy_foundation": 12,
        "body.teen_pregnancy_fluency": 6,
        "body.teen_pregnancy_application": 6,
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
