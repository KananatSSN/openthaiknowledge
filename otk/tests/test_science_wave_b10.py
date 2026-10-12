"""Acceptance tests for Wave B — the ม.2 circulation block, ว 1.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m2.blood_circulation import BLOOD_LOOP, BLOOD_STATES
from otk.sets.biology.m2.heart_vessels_and_blood import BLOOD_PARTS, HEART_PARTS, VESSEL_FACTS
from otk.sets._support.science_wave_b10 import (
    CIRCULATION_MODEL_SCENARIOS,
    CIRCULATORY_SCENARIOS,
    HEART_RATE_SCENARIOS,
)
from otk.sets.biology.m2.heart_rate import HEART_RATE_FACTS, NON_VARIABLES, VARIABLES


NEW_KEYS = {
    "body.circulatory_parts_foundation": ("ว 1.2 ม.2/6", 1, "standard_scope"),
    "body.blood_vessels_fluency": ("ว 1.2 ม.2/6", 2, "standard_scope"),
    "body.circulatory_application": ("ว 1.2 ม.2/6", 3, "exact"),
    "body.blood_circuit_foundation": ("ว 1.2 ม.2/7", 1, "standard_scope"),
    "body.blood_circuit_fluency": ("ว 1.2 ม.2/7", 2, "standard_scope"),
    "body.circulation_model_application": ("ว 1.2 ม.2/7", 3, "standard_scope"),
    "body.heart_rate_foundation": ("ว 1.2 ม.2/8", 1, "standard_scope"),
    "body.heart_rate_experiment_fluency": ("ว 1.2 ม.2/8", 2, "standard_scope"),
    "body.heart_rate_application": ("ว 1.2 ม.2/8", 3, "standard_scope"),
}
COMPLETED = ("ว 1.2 ม.2/6", "ว 1.2 ม.2/7", "ว 1.2 ม.2/8")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_circulation_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, status) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["mapping_status"] == status, key
        assert rows[key]["level"] == "ม.2", key


def test_an_undivided_model_or_do_it_requirement_leaves_no_set_exact():
    """ม.2/7 and ม.2/8 have no half that stands free of what an item cannot do."""
    rows = {row["key"]: row for row in catalog()}
    for outcome in ("ว 1.2 ม.2/7", "ว 1.2 ม.2/8"):
        filed = {rows[key]["mapping_status"]
                 for key, (code, _, _) in NEW_KEYS.items() if code == outcome}
        assert filed == {"standard_scope"}, outcome


def test_only_the_set_spanning_all_three_structures_claims_the_sixth_indicator():
    """ม.2/6 names หัวใจ, หลอดเลือด and เลือด; a set covering one is not the whole."""
    rows = {row["key"]: row for row in catalog()}
    exact = {key for key, (code, _, _) in NEW_KEYS.items()
             if code == "ว 1.2 ม.2/6" and rows[key]["mapping_status"] == "exact"}
    assert exact == {"body.circulatory_application"}
    joined = " ".join(f"{stem} {correct}"
                      for stem, correct, _ in CIRCULATORY_SCENARIOS)
    for structure in ("หัวใจ", "หลอดเลือด", "เลือด"):
        assert structure in joined, structure


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


def test_heart_and_blood_parts_are_kept_in_separate_tables():
    """A heart chamber offered against เกล็ดเลือด tests nothing."""
    for parts in (HEART_PARTS, BLOOD_PARTS):
        assert len(parts) >= 4
        for field in ("name", "function"):
            values = [getattr(item, field) for item in parts]
            assert len(values) == len(set(values)), field
    assert not ({item.name for item in HEART_PARTS}
                & {item.name for item in BLOOD_PARTS})


def test_part_answers_never_mix_the_two_tables():
    heart = {item.name: item.function for item in HEART_PARTS}
    blood = {item.name: item.function for item in BLOOD_PARTS}
    checked = {"heart": 0, "blood": 0}
    for seed in range(600):
        question = generate("body.circulatory_parts_foundation", random.Random(seed))
        stem = _text(question.stem)
        offered = {_text(choice.content) for choice in question.choices}
        table = heart if any(name in stem for name in heart) or "ของหัวใจ" in stem \
            else blood
        checked["heart" if table is heart else "blood"] += 1
        assert offered <= set(table) | set(table.values()), stem
        name = next((key for key in table if f"“{key}”" in stem), None)
        if name is not None:
            assert _answer(question) == table[name], stem
        else:
            function = next(key for key, value in table.items() if value in stem)
            assert _answer(question) == function, stem
    assert all(checked.values()), checked


def test_no_vessel_statement_is_true_of_another_vessel():
    facts = [fact for group in VESSEL_FACTS.values() for fact in group]
    assert len(facts) == len(set(facts))
    assert len(VESSEL_FACTS) == 3
    # Three vessels means the item must offer statements, so every vessel needs
    # enough of its own to fill three wrong choices from the other two.
    assert all(len(group) >= 2 for group in VESSEL_FACTS.values())
    for seed in range(600):
        question = generate("body.blood_vessels_fluency", random.Random(seed))
        stem = _text(question.stem)
        vessel = next(name for name in VESSEL_FACTS if f"“{name}”" in stem)
        assert _answer(question) in VESSEL_FACTS[vessel], stem
        others = {_text(c.content) for c in question.choices} - {_answer(question)}
        assert not others & set(VESSEL_FACTS[vessel]), stem


def test_the_blood_loop_passes_the_lung_before_the_body():
    assert len(BLOOD_LOOP) == len(set(BLOOD_LOOP)) >= 6
    assert BLOOD_LOOP.index("ปอด") < BLOOD_LOOP.index("ส่วนต่าง ๆ ของร่างกาย")
    assert BLOOD_LOOP[0] == "หัวใจห้องล่างขวา"
    states = [item.state for item in BLOOD_STATES]
    places = [item.place for item in BLOOD_STATES]
    assert len(states) == len(set(states)) == len(places) == len(set(places)) == 4


def test_loop_answers_are_read_off_the_one_stored_order_and_wrap_around():
    checked = {"next": 0, "order": 0, "wrap": 0}
    for seed in range(600):
        question = generate("body.blood_circuit_fluency", random.Random(seed))
        stem = _text(question.stem)
        if "เรียงลำดับ" in stem:
            checked["order"] += 1
            assert _answer(question) == " → ".join(BLOOD_LOOP), stem
            continue
        checked["next"] += 1
        current = next(name for name in BLOOD_LOOP if f"“{name}”" in stem)
        index = BLOOD_LOOP.index(current)
        if index == len(BLOOD_LOOP) - 1:
            checked["wrap"] += 1
        assert _answer(question) == BLOOD_LOOP[(index + 1) % len(BLOOD_LOOP)], stem
    # The loop is closed, so the last place must lead back to the first.
    assert all(checked.values()), checked


def test_every_variable_question_offers_something_that_plays_no_role():
    roles = {item.role for item in VARIABLES}
    assert len(roles) == len(VARIABLES) == 3
    assert len({item.item for item in VARIABLES}) == 3
    assert len(NON_VARIABLES) >= 3 and len(set(NON_VARIABLES)) == len(NON_VARIABLES)
    by_role = {item.role: item.item for item in VARIABLES}
    checked = {"forward": 0, "backward": 0}
    for seed in range(600):
        question = generate("body.heart_rate_experiment_fluency",
                            random.Random(seed))
        stem = _text(question.stem)
        offered = {_text(choice.content) for choice in question.choices}
        role = next((name for name in by_role if f"“{name}”" in stem), None)
        if role is not None:
            checked["forward"] += 1
            assert _answer(question) == by_role[role], stem
            assert len(offered & set(NON_VARIABLES)) == 1, stem
            continue
        checked["backward"] += 1
        thing = next(name for name, value in by_role.items() if f"“{value}”" in stem)
        assert _answer(question) == thing, stem
        assert offered == roles | {"สิ่งที่ไม่เกี่ยวข้องกับการทดลองนี้"}, stem
    assert all(checked.values()), checked


def test_heart_rate_facts_have_one_answer_each():
    questions = [item.question for item in HEART_RATE_FACTS]
    answers = [item.answer for item in HEART_RATE_FACTS]
    assert len(questions) == len(set(questions)) >= 5
    assert len(answers) == len(set(answers)) == len(questions)


def test_authored_scenario_banks_are_well_formed():
    for bank in (CIRCULATORY_SCENARIOS, CIRCULATION_MODEL_SCENARIOS,
                 HEART_RATE_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


def test_the_circulation_bank_reads_the_model_and_names_its_limits():
    """โดยใช้แบบจำลอง is in the indicator; an item can read a model, not build one."""
    joined = " ".join(f"{stem} {correct}"
                      for stem, correct, _ in CIRCULATION_MODEL_SCENARIOS)
    assert "แบบจำลอง" in joined
    assert "ข้อจำกัด" in joined


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "body.circulatory_parts_foundation": 18,
        "body.blood_vessels_fluency": 12,
        "body.circulatory_application": 6,
        "body.blood_circuit_foundation": 8,
        "body.blood_circuit_fluency": 7,
        "body.circulation_model_application": 6,
        "body.heart_rate_foundation": 6,
        "body.heart_rate_experiment_fluency": 6,
        "body.heart_rate_application": 6,
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
