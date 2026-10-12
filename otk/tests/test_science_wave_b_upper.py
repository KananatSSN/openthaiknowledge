"""Acceptance tests for Wave B — ``ว 1.2 ม.4``, which closes ``ว 1.2``.

One file for all twelve indicators: the filing rules at ม.4 turn on how each
indicator's verbs are joined, and that is only legible with the whole block in
view at once.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m4.acid_base import ACID_BASE_FACTS, DISTURBANCES
from otk.sets.biology.m4.kidney_balance import ADJUSTMENTS, KIDNEY_FACTS
from otk.sets.biology.m4.membrane import CONTRAST_PAIRS, MEMBRANE_FACTS, MODES
from otk.sets.biology.m4.immune_response import DEFENCE_ORDER, DEFENCES
from otk.sets.biology.m4.immune_disorder import DISORDERS
from otk.sets.biology.m4.temperature_balance import EXPOSURES, TEMPERATURE_FACTS
from otk.sets.biology.m4.hiv_immunity import CONTACTS, HIV_FACTS
from otk.sets.biology.m4.food_test import OBSERVATIONS, TESTS
from otk.sets.biology.m4.useful_substance import USES
from otk.sets.biology.m4.growth_factor import GROWTH_FACTS, SETTINGS
from otk.sets.biology.m4.growth_regulator import REGULATORS
from otk.sets.biology.m4.stimulus_response import RESPONSES


# key -> (indicator, stage, mapping status)
NEW_KEYS = {
    "cell.membrane_structure_foundation": ("ว 1.2 ม.4/1", 1, "exact"),
    "cell.membrane_transport_fluency": ("ว 1.2 ม.4/1", 2, "exact"),
    "cell.membrane_transport_application": ("ว 1.2 ม.4/1", 3, "standard_scope"),
    "body.kidney_balance_foundation": ("ว 1.2 ม.4/2", 1, "exact"),
    "body.kidney_balance_fluency": ("ว 1.2 ม.4/2", 2, "exact"),
    "body.kidney_balance_application": ("ว 1.2 ม.4/2", 3, "standard_scope"),
    "body.acid_base_foundation": ("ว 1.2 ม.4/3", 1, "exact"),
    "body.acid_base_fluency": ("ว 1.2 ม.4/3", 2, "exact"),
    "body.acid_base_application": ("ว 1.2 ม.4/3", 3, "standard_scope"),
    "body.temperature_balance_foundation": ("ว 1.2 ม.4/4", 1, "exact"),
    "body.temperature_balance_fluency": ("ว 1.2 ม.4/4", 2, "exact"),
    "body.temperature_balance_application": ("ว 1.2 ม.4/4", 3, "standard_scope"),
    "body.immune_response_foundation": ("ว 1.2 ม.4/5", 1, "exact"),
    "body.immune_response_fluency": ("ว 1.2 ม.4/5", 2, "exact"),
    "body.immune_response_application": ("ว 1.2 ม.4/5", 3, "standard_scope"),
    "body.immune_disorder_foundation": ("ว 1.2 ม.4/6", 1, "exact"),
    "body.immune_disorder_fluency": ("ว 1.2 ม.4/6", 2, "exact"),
    "body.immune_disorder_application": ("ว 1.2 ม.4/6", 3, "standard_scope"),
    "body.hiv_immunity_foundation": ("ว 1.2 ม.4/7", 1, "exact"),
    "body.hiv_immunity_fluency": ("ว 1.2 ม.4/7", 2, "exact"),
    "body.hiv_immunity_application": ("ว 1.2 ม.4/7", 3, "standard_scope"),
    "plant.food_test_foundation": ("ว 1.2 ม.4/8", 1, "standard_scope"),
    "plant.food_test_fluency": ("ว 1.2 ม.4/8", 2, "exact"),
    "plant.food_test_application": ("ว 1.2 ม.4/8", 3, "standard_scope"),
    "plant.useful_substance_foundation": ("ว 1.2 ม.4/9", 1, "exact"),
    "plant.useful_substance_fluency": ("ว 1.2 ม.4/9", 2, "exact"),
    "plant.useful_substance_application": ("ว 1.2 ม.4/9", 3, "standard_scope"),
    "plant.growth_factor_foundation": ("ว 1.2 ม.4/10", 1, "exact"),
    "plant.growth_factor_fluency": ("ว 1.2 ม.4/10", 2, "exact"),
    "plant.growth_factor_application": ("ว 1.2 ม.4/10", 3, "standard_scope"),
    "plant.growth_regulator_foundation": ("ว 1.2 ม.4/11", 1, "standard_scope"),
    "plant.growth_regulator_fluency": ("ว 1.2 ม.4/11", 2, "exact"),
    "plant.growth_regulator_application": ("ว 1.2 ม.4/11", 3, "standard_scope"),
    "plant.stimulus_response_foundation": ("ว 1.2 ม.4/12", 1, "exact"),
    "plant.stimulus_response_fluency": ("ว 1.2 ม.4/12", 2, "exact"),
    "plant.stimulus_response_application": ("ว 1.2 ม.4/12", 3, "standard_scope"),
}
ROOT = Path(__file__).resolve().parents[2]

# The three ``ว 1.2`` indicators no multiple-choice item can reach: ``ตระหนัก``
# outcomes whose evidence clause is conduct — planting trees, sparing
# pollinators, using the knowledge at home. They are left uncovered on purpose.
# ม.1/2 (using a microscope) was here until Wave I (2026-10-12) wrote sets for
# the parts of it an answer can show; the three attitude indicators remain.
UNREACHABLE = ("ว 1.2 ม.1/8", "ว 1.2 ม.1/13", "ว 1.2 ม.1/18")


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def _outcomes() -> dict:
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        return {row["outcome_code"]: row for row in csv.DictReader(handle)}


def test_upper_secondary_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, status) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["mapping_status"] == status, key
        assert rows[key]["level"] == "ม.4", key


def test_an_indicator_whose_first_verb_is_a_lab_act_files_only_the_free_half():
    """``ม.4/8`` and ``ม.4/11`` each pair an unassessable verb with a free one.

    ``ทดสอบ`` and ``สืบค้นข้อมูล`` cannot be asked for on paper, so the set that
    covers them stays ``standard_scope``; the half that stands free — naming the
    substance, giving the agricultural use — is what is filed ``exact``.
    """
    rows = {row["key"]: row for row in catalog()}
    for outcome, expected in (("ว 1.2 ม.4/8", {"plant.food_test_fluency"}),
                              ("ว 1.2 ม.4/11",
                               {"plant.growth_regulator_fluency"})):
        exact = {key for key, (code, _, _) in NEW_KEYS.items()
                 if code == outcome and rows[key]["mapping_status"] == "exact"}
        assert exact == expected, outcome


def test_no_application_set_in_this_block_claims_an_exact_indicator():
    """Analysing a case is within the standard, but it is not the stated verb."""
    rows = {row["key"]: row for row in catalog()}
    for key, (_, stage, _) in NEW_KEYS.items():
        if stage == 3:
            assert rows[key]["mapping_status"] == "standard_scope", key


def test_the_multi_object_indicators_are_covered_across_all_their_objects():
    """``ม.4/3`` names two organs and ``ม.4/4`` names three; each set spans them."""
    kidney_and_lung = " ".join(fact.answer for fact in ACID_BASE_FACTS)
    assert "ไต" in kidney_and_lung and "ปอด" in kidney_and_lung
    for organ in ("ไต", "ปอด"):
        assert any(organ in item.response for item in DISTURBANCES), organ
    effectors = " ".join(fact.answer for fact in TEMPERATURE_FACTS)
    for effector in ("หลอดเลือด", "เหงื่อ", "กล้ามเนื้อ"):
        assert effector in effectors, effector
        assert any(effector in item.response for item in EXPOSURES), effector


def test_every_transport_contrast_asks_about_a_field_the_two_modes_differ_on():
    """Three modes agree on both fields; a pair drawn from them says nothing."""
    assert CONTRAST_PAIRS
    for first, second, fields in CONTRAST_PAIRS:
        assert fields
        for field in fields:
            assert getattr(first, field) != getattr(second, field)
    same = [mode.name for mode in MODES
            if mode.energy == "ไม่ใช้พลังงานจากเซลล์" and mode.gradient]
    assert len(same) == 3, same
    for name in same:
        assert not any(first.name == name and second.name == name
                       for first, second, _ in CONTRAST_PAIRS)


def test_the_transport_fluency_answer_always_comes_from_the_mode_table():
    descriptions = {mode.name: mode.description for mode in MODES}
    examples = {mode.example: mode.name for mode in MODES}
    checked = {"describe": 0, "example": 0, "contrast": 0}
    for seed in range(900):
        question = generate("cell.membrane_transport_fluency", random.Random(seed))
        stem, answer = _text(question.stem), _answer(question)
        if "เปรียบเทียบ" in stem:
            checked["contrast"] += 1
            continue
        name = next((key for key in descriptions if f"“{key}”" in stem), None)
        if name is not None:
            checked["describe"] += 1
            assert answer == descriptions[name], stem
            continue
        checked["example"] += 1
        example = next(key for key in examples if f"“{key}”" in stem)
        assert answer == examples[example], stem
    assert all(checked.values()), checked


def test_both_kinds_of_immune_response_are_present_and_answered_with_a_reason():
    kinds = {item.kind for item in DEFENCES}
    assert kinds == {"จำเพาะ", "ไม่จำเพาะ"}
    reasons = [item.reason for item in DEFENCES]
    assert len(reasons) == len(set(reasons)) >= 6
    wanted = {item.example: f"แบบ{item.kind} เพราะ{item.reason}"
              for item in DEFENCES}
    checked = {"kind": 0, "order": 0}
    for seed in range(900):
        question = generate("body.immune_response_fluency", random.Random(seed))
        stem, answer = _text(question.stem), _answer(question)
        example = next((key for key in wanted if f"“{key}”" in stem), None)
        if example is None:
            checked["order"] += 1
            current = next(step for step in DEFENCE_ORDER if f"“{step}”" in stem)
            index = DEFENCE_ORDER.index(current)
            assert answer == DEFENCE_ORDER[index + 1], stem
            continue
        checked["kind"] += 1
        assert answer == wanted[example], stem
    assert all(checked.values()), checked


def test_the_non_specific_steps_come_before_the_specific_ones_in_the_order():
    joined = " ".join(DEFENCE_ORDER)
    assert joined.index("ผิวหนัง") < joined.index("ฟาโกไซโทซิส")
    assert joined.index("ฟาโกไซโทซิส") < joined.index("แอนติบอดี")
    assert DEFENCE_ORDER[-1].startswith("เซลล์ความจำ")


def test_no_two_immune_disorders_share_a_cause_or_a_case():
    assert len(DISORDERS) >= 6
    for field in ("name", "cause", "case"):
        values = [getattr(item, field) for item in DISORDERS]
        assert len(values) == len(set(values)), field


def test_the_hiv_contact_table_holds_both_verdicts_and_answers_from_itself():
    verdicts = {item.verdict.split(" เพราะ")[0] for item in CONTACTS}
    assert verdicts == {"มีโอกาสรับเชื้อ", "ไม่มีโอกาสรับเชื้อ"}
    wanted = {item.situation: item.verdict for item in CONTACTS}
    seen = set()
    for seed in range(600):
        question = generate("body.hiv_immunity_fluency", random.Random(seed))
        stem = _text(question.stem)
        situation = next(key for key in wanted if f"“{key}”" in stem)
        seen.add(situation)
        assert _answer(question) == wanted[situation], stem
    assert seen == set(wanted)


def test_every_food_test_observation_names_a_substance_the_test_table_knows():
    known = {test.substance for test in TESTS}
    assert {item.substance for item in OBSERVATIONS} <= known
    # ไอโอดีน is used in two different tests, so a learner who matches on the
    # reagent alone gets it wrong; the table must keep both.
    iodine = [test.substance for test in TESTS if "ไอโอดีน" in test.reagent]
    assert sorted(iodine) == sorted(["แป้ง", "วิตามินซี"])
    wanted = {item.record: item.substance for item in OBSERVATIONS}
    seen = set()
    for seed in range(600):
        question = generate("plant.food_test_fluency", random.Random(seed))
        stem = _text(question.stem)
        record = next(key for key in wanted if key in stem)
        seen.add(record)
        assert _answer(question) == wanted[record], stem
    assert seen == set(wanted)


def test_no_two_plant_substances_or_regulators_answer_the_same_need():
    """Two rows sharing a need would give one situation two right answers."""
    for table, fields in ((USES, ("substance", "use", "need")),
                          (REGULATORS, ("name", "effect", "use", "need"))):
        assert len(table) >= 6
        for field in fields:
            values = [getattr(item, field) for item in table]
            assert len(values) == len(set(values)), field


def test_every_plant_response_names_what_it_does_for_the_plant():
    """``ม.4/12`` closes with ``ที่มีผลต่อการดำรงชีวิต``, so a name is not enough."""
    assert len(RESPONSES) >= 6
    for field in ("name", "description", "example", "benefit"):
        values = [getattr(item, field) for item in RESPONSES]
        assert len(values) == len(set(values)), field
    wanted = {item.example: f"{item.name} ซึ่งทำให้{item.benefit}"
              for item in RESPONSES}
    seen = set()
    for seed in range(600):
        question = generate("plant.stimulus_response_fluency", random.Random(seed))
        stem = _text(question.stem)
        example = next(key for key in wanted if f"“{key}”" in stem)
        seen.add(example)
        assert _answer(question) == wanted[example], stem
    assert seen == set(wanted)


def test_the_fact_tables_have_no_repeated_answer():
    """A repeated answer would put the same text in two choices."""
    for name, facts in (("membrane", MEMBRANE_FACTS), ("kidney", KIDNEY_FACTS),
                        ("acid-base", ACID_BASE_FACTS),
                        ("temperature", TEMPERATURE_FACTS), ("hiv", HIV_FACTS),
                        ("growth", GROWTH_FACTS)):
        answers = [fact.answer for fact in facts]
        assert len(answers) == len(set(answers)) >= 6, name
    for name, table, field in (("adjustment", ADJUSTMENTS, "response"),
                               ("disturbance", DISTURBANCES, "response"),
                               ("exposure", EXPOSURES, "response"),
                               ("setting", SETTINGS, "outcome")):
        values = [getattr(item, field) for item in table]
        assert len(values) == len(set(values)) >= 6, name


def test_each_completed_topic_holds_all_three_stages():
    rows = [row for row in catalog() if row["curriculum_node_id"]]
    for key, (outcome, _, _) in NEW_KEYS.items():
        node = next(row["curriculum_node_id"] for row in rows if row["key"] == key)
        stages = {r["learning_stage"] for r in rows if r["curriculum_node_id"] == node}
        assert stages == {1, 2, 3}, (outcome, sorted(stages))


def test_completed_outcomes_are_recorded_in_the_matrix():
    rows = _outcomes()
    for key, (outcome, _, _) in NEW_KEYS.items():
        assert rows[outcome]["coverage_state"] == "complete", outcome
        assert key in rows[outcome]["current_set_keys"].split("; "), key


def test_wave_b_leaves_no_incomplete_indicator_in_wo_one_two_mo_four():
    """The closing condition of this block: all twelve ม.4 indicators covered."""
    rows = [row for code, row in _outcomes().items()
            if code.startswith("ว 1.2 ม.4/")]
    assert len(rows) == 12
    incomplete = [row["outcome_code"] for row in rows
                  if row["coverage_state"] != "complete"]
    assert not incomplete, incomplete


def test_only_the_unreachable_outcomes_remain_open_across_all_of_wo_one_two():
    """``ว 1.2`` is closed apart from the three no item can honestly assess."""
    rows = [row for code, row in _outcomes().items()
            if row["standard_or_group"] == "ว 1.2"]
    assert len(rows) == 62
    open_codes = tuple(sorted(row["outcome_code"] for row in rows
                              if row["coverage_state"] != "complete"))
    assert open_codes == tuple(sorted(UNREACHABLE)), open_codes
