"""Acceptance tests for Wave A slice 2 — the missing stages after consolidation."""

from __future__ import annotations

import csv
import random
from pathlib import Path

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_KEYS
from otk.sets.chemistry.m1.atoms_elements_compounds import ELEMENT_OR_COMPOUND, FORMULA_FACTS
from otk.sets.chemistry.m2.separating_solutions import SOLUTION_TASKS


NEW_KEYS = {
    "chem.solution_separation_application": ("ว 2.1 ม.2/1", 3),
    "chem.atom_element_compound_fluency": ("ว 2.1 ม.1/7", 2),
    "chem.atom_element_compound_application": ("ว 2.1 ม.1/7", 3),
    "phys.wave_model_application": ("ว 2.3 ม.3/10", 3),
    "phys.reflection_application": ("ว 2.3 ม.3/13", 3),
    "phys.refraction_dispersion_application": ("ว 2.3 ม.3/15", 3),
}
COMPLETED = ("ว 2.1 ม.2/1", "ว 2.3 ม.3/10", "ว 2.1 ม.1/7", "ว 2.3 ม.3/13", "ว 2.3 ม.3/15")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_slice_two_is_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (indicator, stage) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert indicator in rows[key]["indicator_codes"], key
        assert rows[key]["mapping_status"] == "exact", key


def test_every_completed_topic_now_holds_all_three_stages():
    rows = [row for row in catalog() if row["curriculum_node_id"]]
    for indicator in COMPLETED:
        node = next(r["curriculum_node_id"] for r in rows if indicator in r["indicator_codes"])
        stages = {r["learning_stage"] for r in rows if r["curriculum_node_id"] == node}
        assert stages == {1, 2, 3}, (indicator, sorted(stages))


def test_completed_outcomes_are_recorded_in_the_matrix():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        rows = {row["outcome_code"]: row for row in csv.DictReader(handle)}
    for indicator in COMPLETED:
        assert rows[indicator]["coverage_state"] == "complete", indicator


def test_solution_separation_reaches_every_authored_goal():
    stems = [
        _text(generate("chem.solution_separation_application", random.Random(seed)).stem)
        for seed in range(400)
    ]
    for task, _, _ in SOLUTION_TASKS:
        assert any(task in stem for stem in stems), task


def test_formula_reading_never_asks_a_symmetric_formula_to_be_ordered():
    """NaCl has one atom of each element, so 'swap the counts' is the answer."""
    for seed in range(500):
        question = generate("chem.atom_element_compound_fluency", random.Random(seed))
        stem = _text(question.stem)
        if "บอกอะไรเกี่ยวกับหนึ่งโมเลกุล" not in stem:
            continue
        formula = next(f for f, *_ in FORMULA_FACTS if f in stem)
        first, second = next((a, b) for f, _, a, b, _ in FORMULA_FACTS if f == formula)
        assert first != second, formula


def test_element_and_compound_answers_match_the_authored_table():
    for seed in range(500):
        question = generate("chem.atom_element_compound_fluency", random.Random(seed))
        stem = _text(question.stem)
        if "จัดเป็นธาตุหรือสารประกอบ" not in stem:
            continue
        formula = next(f for f, _, _ in ELEMENT_OR_COMPOUND if f"สาร {f} " in stem)
        kind = next(k for f, k, _ in ELEMENT_OR_COMPOUND if f == formula)
        assert _answer(question).startswith(kind), (formula, _answer(question))


def test_atom_counting_answers_are_independently_correct():
    checked = 0
    for seed in range(600):
        question = generate("chem.atom_element_compound_application", random.Random(seed))
        stem = _text(question.stem)
        if "กี่อะตอม" not in stem:
            continue
        checked += 1
        formula = next(f for f, *_ in FORMULA_FACTS if f in stem)
        _, _, _, second, (_, element_b) = next(
            item for item in FORMULA_FACTS if item[0] == formula
        )
        molecules = int(stem.split(" โมเลกุล")[0].split()[-1])
        assert element_b in stem
        assert _answer(question) == f"{second * molecules} อะตอม", stem
    assert checked


def test_reflection_measurements_obey_the_law_of_reflection():
    checked = 0
    for seed in range(600):
        question = generate("phys.reflection_application", random.Random(seed))
        stem = _text(question.stem)
        if "ครั้งที่ 1" in stem:
            checked += 1
            for line in stem.splitlines():
                if not line.startswith("ครั้งที่"):
                    continue
                incident = int(line.split("มุมตกกระทบ ")[1].split("°")[0])
                reflected = int(line.split("มุมสะท้อน ")[1].split("°")[0])
                assert incident == reflected, line
        elif "กับ<u>ผิวกระจก</u>" in stem:
            checked += 1
            angle = int(stem.split("ทำมุม ")[1].split("°")[0])
            assert _answer(question) == f"{90 - angle}°", stem
    assert checked


def test_eight_hundred_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "chem.solution_separation_application": 40,
        "chem.atom_element_compound_fluency": 8,
        "chem.atom_element_compound_application": 14,
        "phys.wave_model_application": 30,
        "phys.reflection_application": 12,
        "phys.refraction_dispersion_application": 5,
    }
    for key, minimum in minimums.items():
        signatures = set()
        for seed in range(800):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            assert question.hint
            signatures.add((_text(question.stem), choices[question.answer]))
        assert len(signatures) >= minimum, (key, len(signatures))
