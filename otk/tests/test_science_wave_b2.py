"""Acceptance tests for Wave B — the ม.1 cell block, ว 1.2."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.m1.organisation import BODY_LEVELS
from otk.sets._support.science_wave_b2 import (
    BOTH,
    CELL_SCENARIOS,
    DIFFUSION_SCENARIOS,
    ORGANELLES,
    ORGANISATION_SCENARIOS,
    PLANT_ONLY,
    SHAPE_SCENARIOS,
    SPECIAL_CELLS,
)
from otk.sets.biology.m1.diffusion import EVERYDAY_CASES, TONICITY


NEW_KEYS = {
    "cell.organelle_function_foundation": ("ว 1.2 ม.1/1", 1),
    "cell.plant_animal_fluency": ("ว 1.2 ม.1/1", 2),
    "cell.structure_application": ("ว 1.2 ม.1/1", 3),
    "cell.shape_function_foundation": ("ว 1.2 ม.1/3", 1),
    "cell.shape_function_fluency": ("ว 1.2 ม.1/3", 2),
    "cell.shape_function_application": ("ว 1.2 ม.1/3", 3),
    "cell.organisation_foundation": ("ว 1.2 ม.1/4", 1),
    "cell.organisation_fluency": ("ว 1.2 ม.1/4", 2),
    "cell.organisation_application": ("ว 1.2 ม.1/4", 3),
    "cell.diffusion_foundation": ("ว 1.2 ม.1/5", 1),
    "cell.diffusion_fluency": ("ว 1.2 ม.1/5", 2),
    "cell.diffusion_application": ("ว 1.2 ม.1/5", 3),
}
COMPLETED = ("ว 1.2 ม.1/1", "ว 1.2 ม.1/3", "ว 1.2 ม.1/4", "ว 1.2 ม.1/5")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_cell_sets_are_additive_and_correctly_staged():
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


def test_the_organelle_table_is_exactly_the_seven_the_indicator_names():
    """ม.1/1 lists its structures; an eighth would drift past the outcome."""
    assert [item.name for item in ORGANELLES] == [
        "ผนังเซลล์", "เยื่อหุ้มเซลล์", "ไซโทพลาซึม", "นิวเคลียส",
        "แวคิวโอล", "ไมโทคอนเดรีย", "คลอโรพลาสต์",
    ]
    functions = [item.function for item in ORGANELLES]
    assert len(functions) == len(set(functions))
    plant_only = [item.name for item in ORGANELLES if item.where == PLANT_ONLY]
    assert plant_only == ["ผนังเซลล์", "คลอโรพลาสต์"]
    # Every other structure is shared, which is what makes the comparison work.
    assert all(item.where in (PLANT_ONLY, BOTH) for item in ORGANELLES)
    assert len([item for item in ORGANELLES if item.where == BOTH]) >= 4


def test_organelle_answers_come_from_the_table_in_both_directions():
    by_name = {item.name: item.function for item in ORGANELLES}
    by_function = {item.function: item.name for item in ORGANELLES}
    checked = {"name": 0, "function": 0}
    seen = set()
    for seed in range(600):
        question = generate("cell.organelle_function_foundation", random.Random(seed))
        stem = _text(question.stem)
        name = next((key for key in by_name if f"“{key}”" in stem), None)
        if name is not None:
            checked["name"] += 1
            seen.add(name)
            assert _answer(question) == by_name[name], stem
            continue
        checked["function"] += 1
        function = next(key for key in by_function if key in stem)
        assert _answer(question) == by_function[function], stem
    assert all(checked.values()), checked
    assert seen == set(by_name)


def test_plant_animal_answers_never_call_a_shared_structure_plant_only():
    plant_only = {item.name for item in ORGANELLES if item.where == PLANT_ONLY}
    shared = {item.name for item in ORGANELLES if item.where == BOTH}
    checked = {"pair": 0, "single": 0, "observation": 0}
    for seed in range(900):
        question = generate("cell.plant_animal_fluency", random.Random(seed))
        stem = _text(question.stem)
        answer = _answer(question)
        if "ทั้งคู่" in stem:
            checked["pair"] += 1
            named = {part for part in answer.split(" และ")}
            assert named == plant_only, stem
            for choice in question.choices:
                other = {part for part in _text(choice.content).split(" และ")}
                assert (other == plant_only) == (
                    _text(choice.content) == answer), stem
            continue
        if "โครงสร้างใดต่อไปนี้พบในเซลล์พืช" in stem:
            checked["single"] += 1
            assert answer in plant_only, stem
            others = {_text(c.content) for c in question.choices} - {answer}
            assert others <= shared, stem
            continue
        checked["observation"] += 1
        listed = {name for name in plant_only | shared if name in stem}
        expected = "เซลล์พืช" if listed & plant_only else "เซลล์สัตว์"
        assert answer.startswith(expected), stem
    assert all(checked.values()), checked


def test_every_specialised_cell_carries_a_job_a_shape_and_a_reason():
    names = [cell.name for cell in SPECIAL_CELLS]
    assert len(names) == len(set(names)) >= 6
    for field in ("job", "shape", "reason"):
        values = [getattr(cell, field) for cell in SPECIAL_CELLS]
        # Two cells sharing a job would make the reverse direction ambiguous.
        assert len(values) == len(set(values)), field


def test_shape_answers_come_from_the_table_in_every_direction():
    jobs = {cell.name: cell.job for cell in SPECIAL_CELLS}
    shapes = {cell.name: cell.shape for cell in SPECIAL_CELLS}
    reasons = {cell.name: cell.reason for cell in SPECIAL_CELLS}
    by_job = {cell.job: cell.name for cell in SPECIAL_CELLS}
    checked = {"job": 0, "which": 0, "shape": 0, "reason": 0}
    for seed in range(600):
        question = generate("cell.shape_function_foundation", random.Random(seed))
        stem = _text(question.stem)
        name = next((key for key in jobs if f"“{key}”" in stem), None)
        if name is not None:
            checked["job"] += 1
            assert _answer(question) == jobs[name], stem
        else:
            checked["which"] += 1
            job = next(key for key in by_job if key in stem)
            assert _answer(question) == by_job[job], stem
    for seed in range(600):
        question = generate("cell.shape_function_fluency", random.Random(seed))
        stem = _text(question.stem)
        name = next(key for key in shapes if f"“{key}”" in stem)
        if "ช่วยให้ทำหน้าที่ได้ดีอย่างไร" in stem:
            checked["reason"] += 1
            assert shapes[name] in stem, stem
            assert _answer(question) == reasons[name], stem
        else:
            checked["shape"] += 1
            assert _answer(question) == shapes[name], stem
    assert all(checked.values()), checked


def test_authored_scenario_banks_are_well_formed():
    for bank in (CELL_SCENARIOS, SHAPE_SCENARIOS, ORGANISATION_SCENARIOS,
                 DIFFUSION_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 5
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "cell.organelle_function_foundation": 14,
        "cell.plant_animal_fluency": 20,
        "cell.structure_application": 6,
        "cell.shape_function_foundation": 12,
        "cell.shape_function_fluency": 12,
        "cell.shape_function_application": 6,
        "cell.organisation_foundation": 10,
        "cell.organisation_fluency": 5,
        "cell.organisation_application": 6,
        "cell.diffusion_foundation": 7,
        "cell.diffusion_fluency": 12,
        "cell.diffusion_application": 6,
    }
    for key, minimum in minimums.items():
        signatures = set()
        for seed in range(1000):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            # Concept banks carry no hint by design — a ``Concept`` is a stem,
            # an answer and its distractors — so only the generated sets are
            # held to having one.
            if key != "cell.diffusion_foundation":
                assert question.hint, (key, seed)
            signatures.add((_text(question.stem), choices[question.answer]))
        assert len(signatures) >= minimum, (key, len(signatures))


def test_the_organisation_ladder_is_the_five_rungs_the_indicator_names():
    """ม.1/4 lists its levels; ประชากร belongs to the other ladder, not this one."""
    assert [level.name for level in BODY_LEVELS] == [
        "เซลล์", "เนื้อเยื่อ", "อวัยวะ", "ระบบอวัยวะ", "สิ่งมีชีวิต",
    ]
    for field in ("definition", "example"):
        values = [getattr(level, field) for level in BODY_LEVELS]
        assert len(values) == len(set(values)), field


def test_organisation_answers_and_ordering_come_from_that_one_list():
    names = [level.name for level in BODY_LEVELS]
    by_definition = {level.definition: level.name for level in BODY_LEVELS}
    by_example = {level.example: level.name for level in BODY_LEVELS}
    checked = {"definition": 0, "example": 0, "next": 0, "order": 0}
    for seed in range(600):
        question = generate("cell.organisation_foundation", random.Random(seed))
        stem = _text(question.stem)
        key = next((k for k in by_definition if f"“{k}”" in stem), None)
        if key is not None:
            checked["definition"] += 1
            assert _answer(question) == by_definition[key], stem
            continue
        checked["example"] += 1
        key = next(k for k in by_example if f"“{k}”" in stem)
        assert _answer(question) == by_example[key], stem
    for seed in range(600):
        question = generate("cell.organisation_fluency", random.Random(seed))
        stem = _text(question.stem)
        if "เรียงลำดับ" in stem:
            checked["order"] += 1
            assert _answer(question) == " → ".join(names), stem
            continue
        named = next(name for name in names if f"“{name}”" in stem)
        if "เล็กถัดลงมา" in stem:
            checked["below"] = checked.get("below", 0) + 1
            assert _answer(question) == names[names.index(named) - 1], stem
            continue
        checked["next"] += 1
        assert _answer(question) == names[names.index(named) + 1], stem
    assert all(checked.values()), checked


def test_every_everyday_case_is_one_process_without_argument():
    cases = dict(EVERYDAY_CASES)
    assert len(cases) == len(EVERYDAY_CASES)
    kinds = {kind for _, kind in EVERYDAY_CASES}
    assert kinds == {"การแพร่", "ออสโมซิส"}
    for kind in kinds:
        # Each direction of the question needs one answer and three wrongs.
        assert len([c for c, k in EVERYDAY_CASES if k == kind]) >= 4, kind


def test_diffusion_answers_never_put_an_osmosis_case_in_the_wrong_list():
    cases = dict(EVERYDAY_CASES)
    tonicity = {outside: (direction, effect)
                for outside, direction, effect in TONICITY}
    checked = {"pick": 0, "direction": 0, "effect": 0}
    for seed in range(900):
        question = generate("cell.diffusion_fluency", random.Random(seed))
        stem = _text(question.stem)
        answer = _answer(question)
        if "เหตุการณ์ใดต่อไปนี้" in stem:
            checked["pick"] += 1
            wanted = "ออสโมซิส" if "เป็นออสโมซิส" in stem else "การแพร่"
            assert cases[answer] == wanted, stem
            for choice in question.choices:
                text = _text(choice.content)
                assert (cases[text] == wanted) == (text == answer), stem
            continue
        outside = next(key for key in tonicity if key in stem)
        direction, effect = tonicity[outside]
        if "น้ำจะเคลื่อนที่อย่างไร" in stem:
            checked["direction"] += 1
            assert answer == direction, stem
        else:
            checked["effect"] += 1
            assert answer == effect, stem
    assert all(checked.values()), checked
