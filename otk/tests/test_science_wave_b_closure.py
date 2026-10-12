"""Acceptance tests for the ``ว 1.1`` closure — the last nine open indicators.

One file for the nine because the filing turns on the same three questions for
all of them: which verbs stand free of ``สืบค้นข้อมูล``, which indicators name
more than one object, and which evidence clause is conduct.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

from otk.core import catalog, generate
from otk.core.curriculum_science import (
    SCIENCE_BASELINE_KEYS,
    SCIENCE_BIOLOGY_CLOSURE_KEYS,
    SCIENCE_WAVE_B_KEYS,
)
from otk.sets.biology.p5.adaptation import ADAPTATIONS
from otk.sets.biology.p1.animal_surroundings import AQUATIC, SURROUNDINGS
from otk.sets.biology.p1.habitat_dwellers import DWELLERS, NOT_FOUND, PLACES
from otk.sets.biology.m4.biome import BIOMES, GEOGRAPHY_FACTS
from otk.sets._support.science_wave_b32 import CONSEQUENCES, LIVING, NON_LIVING
from otk.sets.biology.p5.environment_care import ENVIRONMENT_CARE, ENVIRONMENT_NEEDS
from otk.sets.biology.p5.living_relations import RELATION_FACTS, RELATIONS
from otk.sets._support.science_wave_b33 import BIOLOGICAL, PHYSICAL, POPULATION_EFFECTS
from otk.sets.biology.m4.succession import (
    CAUSE_FACTS,
    NOT_SUCCESSION,
    PRIMARY,
    SECONDARY,
    SUCCESSION_ORDER,
    SUCCESSIONS,
)
from otk.sets.biology.m4.resource_conservation import ENVIRONMENT, PROBLEMS, RESOURCE
from otk.sets.biology.m4.population_change import FACTORS, POPULATION_FACTS


def _triple(prefix: str, outcome: str, statuses: tuple[str, str, str]) -> dict:
    return {f"{prefix}_{name}": (outcome, stage, status)
            for name, stage, status in zip(("foundation", "fluency", "application"),
                                           (1, 2, 3), statuses)}


FREE = ("exact", "exact", "standard_scope")
# key -> (indicator, stage, mapping status)
NEW_KEYS = {
    **_triple("ecology.habitat_dwellers", "ว 1.1 ป.1/1",
              ("standard_scope", "exact", "standard_scope")),
    **_triple("ecology.animal_surroundings", "ว 1.1 ป.1/2", FREE),
    **_triple("ecology.adaptation", "ว 1.1 ป.5/1", FREE),
    **_triple("ecology.living_relations", "ว 1.1 ป.5/2", FREE),
    **_triple("ecology.environment_care", "ว 1.1 ป.5/4", ("standard_scope",) * 3),
    **_triple("ecology.biome", "ว 1.1 ม.4/1", FREE),
    **_triple("ecology.succession", "ว 1.1 ม.4/2", FREE),
    **_triple("ecology.population_change", "ว 1.1 ม.4/3", FREE),
    **_triple("ecology.resource_conservation", "ว 1.1 ม.4/4", FREE),
}
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def _choices(question) -> list[str]:
    return [_text(choice.content) for choice in question.choices]


def _outcomes() -> dict:
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        return {row["outcome_code"]: row for row in csv.DictReader(handle)}


def _exact(outcome: str) -> set[str]:
    rows = {row["key"]: row for row in catalog()}
    return {key for key, (code, _, _) in NEW_KEYS.items()
            if code == outcome and rows[key]["mapping_status"] == "exact"}


def test_closure_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert len(NEW_KEYS) == 27
    assert set(NEW_KEYS) == set(SCIENCE_BIOLOGY_CLOSURE_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, status) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["mapping_status"] == status, key
        assert rows[key]["level"] == outcome.split()[-1].split("/")[0], key


def test_the_closure_stays_outside_the_approved_wave_b_cohort():
    """Wave B's gate approved 262 named sets; these did not go through it."""
    assert len(SCIENCE_WAVE_B_KEYS) == 262
    assert not SCIENCE_BIOLOGY_CLOSURE_KEYS & SCIENCE_WAVE_B_KEYS


def test_an_outcome_whose_evidence_is_conduct_has_no_exact_set():
    """``ป.5/4`` ends ``โดยมีส่วนร่วมในการดูแลรักษาสิ่งแวดล้อม``."""
    assert _exact("ว 1.1 ป.5/4") == set()


def test_an_outcome_that_names_its_evidence_files_only_the_set_that_reads_it():
    """``ป.1/1`` says ``จากข้อมูลที่รวบรวมได้``: only reading a record is exact."""
    assert _exact("ว 1.1 ป.1/1") == {"ecology.habitat_dwellers_fluency"}


def test_a_search_with_two_free_verbs_after_it_files_both_halves():
    """Every ม.4 indicator opens with ``สืบค้นข้อมูล`` and then names two verbs
    with objects of their own; the set doing each is exact, the search is not."""
    for prefix, outcome in (("ecology.biome", "ว 1.1 ม.4/1"),
                            ("ecology.succession", "ว 1.1 ม.4/2"),
                            ("ecology.population_change", "ว 1.1 ม.4/3"),
                            ("ecology.resource_conservation", "ว 1.1 ม.4/4")):
        assert _exact(outcome) == {f"{prefix}_foundation", f"{prefix}_fluency"}


def test_no_application_set_in_this_block_claims_an_exact_indicator():
    rows = {row["key"]: row for row in catalog()}
    for key, (_, stage, _) in NEW_KEYS.items():
        if stage == 3:
            assert rows[key]["mapping_status"] == "standard_scope", key


def test_the_multi_object_indicators_are_covered_across_all_their_objects():
    """``ป.5/2``, ``ม.4/3`` and ``ม.4/4`` each name two things; tables hold both."""
    assert {item.kind for item in RELATIONS} == {LIVING, NON_LIVING}
    assert {item.kind for item in CONSEQUENCES} == {LIVING, NON_LIVING}
    assert {item.kind for item in FACTORS} == {PHYSICAL, BIOLOGICAL}
    assert {item.kind for item in POPULATION_EFFECTS} == {PHYSICAL, BIOLOGICAL}
    targets = [item.target for item in PROBLEMS]
    assert targets.count(RESOURCE) == targets.count(ENVIRONMENT) == 4


def test_a_habitat_distractor_never_comes_from_the_answers_own_realm():
    """A pond fish is at home in a stream too; offering one would give two answers."""
    by_name = {item.name: item for item in DWELLERS}
    checked = {"name": 0, "place": 0}
    for seed in range(900):
        question = generate("ecology.habitat_dwellers_foundation", random.Random(seed))
        answer = _answer(question)
        wrongs = [text for text in _choices(question) if text != answer]
        if answer in by_name:
            checked["name"] += 1
            realm = PLACES[by_name[answer].place]
            assert all(PLACES[by_name[w].place] != realm for w in wrongs), wrongs
        else:
            checked["place"] += 1
            assert all(PLACES[w] != PLACES[answer] for w in wrongs), wrongs
    assert all(checked.values()), checked


def test_the_survey_answer_is_read_back_from_the_record_in_the_stem():
    checked = {"kind": 0, "place": 0}
    for seed in range(900):
        question = generate("ecology.habitat_dwellers_fluency", random.Random(seed))
        stem, answer = _text(question.stem), _answer(question)
        record = stem.split("ดังนี้ ")[1].split(" จากข้อมูลนี้")[0]
        found = {}
        for line in record.split(" / "):
            place, names = line.split(": ")
            for name in names.split(", "):
                found[name] = place
        if "พบที่บริเวณใด" in stem:
            checked["place"] += 1
            name = stem.split("“")[-1].split("”")[0]
            assert answer == found[name], stem
            assert NOT_FOUND in _choices(question)
            continue
        checked["kind"] += 1
        place = stem.split("“")[-1].split("”")[0]
        kind = "พืช" if "เป็นพืชที่" in stem else "สัตว์"
        kinds = {item.name: item.kind for item in DWELLERS}
        assert found[answer] == place and kinds[answer] == kind, stem
        for wrong in _choices(question):
            if wrong != answer:
                assert not (found[wrong] == place and kinds[wrong] == kind), stem
    assert all(checked.values()), checked


def test_a_stranded_animal_is_only_ever_moved_between_water_and_land():
    by_animal = {item.animal: item for item in SURROUNDINGS}
    places = {item.place: item for item in SURROUNDINGS}
    moved = 0
    for seed in range(600):
        question = generate("ecology.animal_surroundings_fluency", random.Random(seed))
        stem = _text(question.stem)
        if not stem.startswith("ถ้านำ"):
            continue
        moved += 1
        place = stem.split("“")[1].split("”")[0]
        animal = next(name for name in by_animal if stem.startswith(f"ถ้านำ{name}ไป"))
        assert (animal in AQUATIC) != (places[place].animal in AQUATIC), stem
        assert _answer(question) == f"เพราะที่นั่นไม่มี{by_animal[animal].essential}"
    assert moved


def test_an_adaptation_distractor_never_comes_from_the_same_habitat():
    """A lotus leaf floats too, so a same-habitat benefit could also be right."""
    benefits = {item.benefit: item.habitat for item in ADAPTATIONS}
    structures = {item.structure: item.habitat for item in ADAPTATIONS}
    for seed in range(600):
        question = generate("ecology.adaptation_foundation", random.Random(seed))
        answer = _answer(question)
        for wrong in _choices(question):
            if wrong != answer:
                assert benefits[wrong] != benefits[answer]
        question = generate("ecology.adaptation_fluency", random.Random(seed))
        answer = _answer(question)
        if " ซึ่งช่วยให้" in answer:
            habitat = structures[answer.split(" ซึ่งช่วยให้")[0]]
            for wrong in _choices(question):
                if wrong != answer:
                    assert structures[wrong.split(" ซึ่งช่วยให้")[0]] != habitat


def test_a_resource_remedy_is_never_offered_against_one_from_the_same_half():
    """Two resource problems can share a remedy; the other half cannot."""
    targets = {item.solution: item.target for item in PROBLEMS}
    for seed in range(600):
        question = generate("ecology.resource_conservation_fluency",
                            random.Random(seed))
        answer = _answer(question)
        wanted = next(item.solution for item in PROBLEMS
                      if item.situation in _text(question.stem))
        assert answer == wanted
        for wrong in _choices(question):
            if wrong != answer:
                assert targets[wrong] != targets[answer]


def test_the_succession_order_steps_one_group_at_a_time():
    assert SUCCESSION_ORDER[0] == "ไลเคน" and SUCCESSION_ORDER[-1] == "ไม้ยืนต้น"
    stepped = 0
    for seed in range(600):
        question = generate("ecology.succession_fluency", random.Random(seed))
        stem = _text(question.stem)
        if "ถัดจาก" not in stem:
            continue
        stepped += 1
        current = stem.split("“")[-1].split("”")[0]
        index = SUCCESSION_ORDER.index(current)
        assert _answer(question) == SUCCESSION_ORDER[index + 1], stem
    assert stepped


def test_both_kinds_of_succession_have_enough_cases_to_sort():
    kinds = [item.kind for item in SUCCESSIONS]
    assert kinds.count(PRIMARY) >= 4 and kinds.count(SECONDARY) >= 4
    assert len(NOT_SUCCESSION) >= 3


def test_no_two_rows_share_an_answer_across_the_closure_tables():
    """A repeated answer would put the same text in two choices."""
    for name, facts in (("relation", RELATION_FACTS), ("geography", GEOGRAPHY_FACTS),
                        ("cause", CAUSE_FACTS), ("population", POPULATION_FACTS)):
        answers = [fact.answer for fact in facts]
        assert len(answers) == len(set(answers)) >= 6, name
    for name, table, fields in (
        ("surroundings", SURROUNDINGS, ("animal", "place", "need", "essential")),
        ("adaptations", ADAPTATIONS, ("organism", "structure", "benefit")),
        ("biomes", BIOMES, ("name", "where", "vegetation", "reason")),
        ("care", ENVIRONMENT_CARE, ("practice", "reason")),
        ("problems", PROBLEMS, ("problem", "situation", "impact", "solution")),
    ):
        for field in fields:
            values = [getattr(item, field) for item in table]
            assert len(values) == len(set(values)) >= 6, (name, field)
    assert {need.practice for need in ENVIRONMENT_NEEDS} == {
        care.practice for care in ENVIRONMENT_CARE}


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


def test_wo_one_one_has_no_incomplete_indicator():
    """The closing condition: all sixteen ``ว 1.1`` indicators hold three stages."""
    rows = [row for row in _outcomes().values()
            if row["standard_or_group"] == "ว 1.1"]
    assert len(rows) == 16
    incomplete = [row["outcome_code"] for row in rows
                  if row["coverage_state"] != "complete"]
    assert not incomplete, incomplete
