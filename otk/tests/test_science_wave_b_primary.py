"""Acceptance tests for Wave B — the whole of ว 1.2 at primary level.

The fifteen primary indicators of ``ว 1.2`` were built as five slices but they
form one block: ป.1 body parts, ป.2 plants, ป.3 animals, ป.4 plant organs, and
the ป.6 nutrient and digestion pair. Testing them together is what makes the
filing rules visible in one place — especially the ``ตระหนัก`` split, which at
this level cuts three different ways.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.p1.body_parts import ACTIVITIES, PARTS
from otk.sets.biology.p1.body_care import BODY_CARE, BODY_CARE_NEEDS
from otk.sets.biology.p2.what_plants_need import TRIALS
from otk.sets.biology.p2.life_cycle import FLOWER_CYCLE, FLOWER_STAGES
from otk.sets.biology.p2.plant_care import PLANT_CARE, PLANT_CARE_NEEDS
from otk.sets.biology.p3.life_cycle import CYCLES, PATTERNS
from otk.sets.biology.p3.living_care import LIVING_CARE, LIVING_CARE_NEEDS
from otk.sets.biology.p3.respect_life import RESPECT_CARE, RESPECT_NEEDS
from otk.sets.biology.p6.food_choice import GUIDELINES, GUIDELINE_NEEDS
from otk.sets.biology.p6.nutrient_group import MEALS, NUTRIENTS
from otk.sets.biology.p4.organ_function import ORGANS
from otk.sets.biology.p6.own_diet import DAY_RECORDS, DIET_CARE
from otk.sets._support.science_wave_b18 import DIET_NEEDS
from otk.sets.biology.p6.digestive_care import DIGESTIVE_CARE, DIGESTIVE_NEEDS
from otk.sets.biology.p6.digestive_system import DIGESTIVE_ORGANS, FOOD_PATH


# key -> (indicator, stage, mapping status)
NEW_KEYS = {
    "life.body_parts_foundation": ("ว 1.2 ป.1/1", 1, "exact"),
    "life.body_parts_fluency": ("ว 1.2 ป.1/1", 2, "exact"),
    "life.body_parts_application": ("ว 1.2 ป.1/1", 3, "standard_scope"),
    "life.body_care_foundation": ("ว 1.2 ป.1/2", 1, "standard_scope"),
    "life.body_care_fluency": ("ว 1.2 ป.1/2", 2, "standard_scope"),
    "life.body_care_application": ("ว 1.2 ป.1/2", 3, "standard_scope"),
    "plant.growth_needs_foundation": ("ว 1.2 ป.2/1", 1, "standard_scope"),
    "plant.growth_evidence_fluency": ("ว 1.2 ป.2/1", 2, "exact"),
    "plant.growth_application": ("ว 1.2 ป.2/1", 3, "exact"),
    "plant.plant_care_foundation": ("ว 1.2 ป.2/2", 1, "standard_scope"),
    "plant.plant_care_fluency": ("ว 1.2 ป.2/2", 2, "standard_scope"),
    "plant.plant_care_application": ("ว 1.2 ป.2/2", 3, "standard_scope"),
    "plant.life_cycle_foundation": ("ว 1.2 ป.2/3", 1, "standard_scope"),
    "plant.life_cycle_fluency": ("ว 1.2 ป.2/3", 2, "standard_scope"),
    "plant.life_cycle_application": ("ว 1.2 ป.2/3", 3, "standard_scope"),
    "life.living_needs_foundation": ("ว 1.2 ป.3/1", 1, "standard_scope"),
    "life.living_needs_fluency": ("ว 1.2 ป.3/1", 2, "exact"),
    "life.living_needs_application": ("ว 1.2 ป.3/1", 3, "exact"),
    "life.living_care_foundation": ("ว 1.2 ป.3/2", 1, "standard_scope"),
    "life.living_care_fluency": ("ว 1.2 ป.3/2", 2, "standard_scope"),
    "life.living_care_application": ("ว 1.2 ป.3/2", 3, "standard_scope"),
    "animal.life_cycle_foundation": ("ว 1.2 ป.3/3", 1, "standard_scope"),
    "animal.life_cycle_fluency": ("ว 1.2 ป.3/3", 2, "exact"),
    "animal.life_cycle_application": ("ว 1.2 ป.3/3", 3, "standard_scope"),
    "animal.respect_life_foundation": ("ว 1.2 ป.3/4", 1, "standard_scope"),
    "animal.respect_life_fluency": ("ว 1.2 ป.3/4", 2, "standard_scope"),
    "animal.respect_life_application": ("ว 1.2 ป.3/4", 3, "standard_scope"),
    "plant.organ_function_foundation": ("ว 1.2 ป.4/1", 1, "exact"),
    "plant.organ_function_fluency": ("ว 1.2 ป.4/1", 2, "standard_scope"),
    "plant.organ_function_application": ("ว 1.2 ป.4/1", 3, "standard_scope"),
    "body.nutrient_group_foundation": ("ว 1.2 ป.6/1", 1, "standard_scope"),
    "body.nutrient_group_fluency": ("ว 1.2 ป.6/1", 2, "exact"),
    "body.nutrient_group_application": ("ว 1.2 ป.6/1", 3, "exact"),
    "body.food_choice_foundation": ("ว 1.2 ป.6/2", 1, "standard_scope"),
    "body.food_choice_fluency": ("ว 1.2 ป.6/2", 2, "exact"),
    "body.food_choice_application": ("ว 1.2 ป.6/2", 3, "standard_scope"),
    "body.own_diet_foundation": ("ว 1.2 ป.6/3", 1, "standard_scope"),
    "body.own_diet_fluency": ("ว 1.2 ป.6/3", 2, "standard_scope"),
    "body.own_diet_application": ("ว 1.2 ป.6/3", 3, "standard_scope"),
    "body.digestive_organs_foundation": ("ว 1.2 ป.6/4", 1, "exact"),
    "body.digestion_fluency": ("ว 1.2 ป.6/4", 2, "exact"),
    "body.digestion_application": ("ว 1.2 ป.6/4", 3, "standard_scope"),
    "body.digestive_care_foundation": ("ว 1.2 ป.6/5", 1, "standard_scope"),
    "body.digestive_care_fluency": ("ว 1.2 ป.6/5", 2, "exact"),
    "body.digestive_care_application": ("ว 1.2 ป.6/5", 3, "standard_scope"),
}
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_primary_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, status) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["mapping_status"] == status, key
        assert rows[key]["level"] == outcome.split()[-1].split("/")[0], key


def test_each_completed_topic_holds_all_three_stages():
    rows = [row for row in catalog() if row["curriculum_node_id"]]
    for key, (outcome, _, _) in NEW_KEYS.items():
        node = next(row["curriculum_node_id"] for row in rows if row["key"] == key)
        stages = {r["learning_stage"] for r in rows if r["curriculum_node_id"] == node}
        assert stages == {1, 2, 3}, (outcome, sorted(stages))


def test_wave_b_leaves_no_incomplete_primary_indicator_in_wo_one_two():
    """The closing condition of this block: every ป-level ว 1.2 indicator covered."""
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        rows = [row for row in csv.DictReader(handle)
                if row["outcome_code"].startswith("ว 1.2 ป.")]
    assert len(rows) == 15
    incomplete = [row["outcome_code"] for row in rows
                  if row["coverage_state"] != "complete"]
    assert not incomplete, incomplete


def test_the_tranak_rule_cuts_three_ways_at_primary_level():
    """Same word, three filings, decided by the evidence clause each time."""
    rows = {row["key"]: row for row in catalog()}
    exact_of = {}
    for key, (outcome, _, _) in NEW_KEYS.items():
        if rows[key]["mapping_status"] == "exact":
            exact_of.setdefault(outcome, set()).add(key)
    # ป.1/2, ป.3/2, ป.3/4, ป.6/3 — evidence is conduct, so no set is exact.
    for outcome in ("ว 1.2 ป.1/2", "ว 1.2 ป.3/2", "ว 1.2 ป.3/4", "ว 1.2 ป.6/3"):
        assert outcome not in exact_of, outcome
    # ป.6/5 — evidence is บอกแนวทาง, so exactly the Fluency set is exact.
    assert exact_of["ว 1.2 ป.6/5"] == {"body.digestive_care_fluency"}
    # ป.6/2 — บอกแนวทาง is the main verb, not evidence for an attitude.
    assert exact_of["ว 1.2 ป.6/2"] == {"body.food_choice_fluency"}


def test_no_tranak_outcome_whose_evidence_is_conduct_claims_exact():
    """The catalog-wide guard from ม.2, restated over the primary wording too."""
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        outcomes = {row["outcome_code"]: row["official_text"]
                    for row in csv.DictReader(handle)}
    conduct = ("โดยการดูแลส่วนต่าง ๆ", "โดยดูแลพืช", "โดยการดูแลตนเองและสัตว์",
               "โดยไม่ทำให้วัฏจักรชีวิตของสัตว์", "โดยการเลือกรับประทานอาหาร",
               "โดยการดูแลรักษาร่างกาย", "โดยการประพฤติตน", "โดยมีส่วนร่วม",
               "โดยการนำความรู้ไปใช้")
    for row in catalog():
        if row["mapping_status"] != "exact":
            continue
        for code in row["indicator_codes"] or ():
            text = outcomes.get(code, "")
            assert not any(phrase in text for phrase in conduct), (row["key"], code)


def test_a_model_verb_with_a_free_standing_second_half_is_split():
    """ป.3/3 and ป.6/4 both say สร้างแบบจำลอง, and both have a half that stands free."""
    rows = {row["key"]: row for row in catalog()}
    assert rows["animal.life_cycle_fluency"]["mapping_status"] == "exact"
    assert rows["animal.life_cycle_foundation"]["mapping_status"] == "standard_scope"
    assert rows["animal.life_cycle_application"]["mapping_status"] == "standard_scope"
    assert rows["body.digestive_organs_foundation"]["mapping_status"] == "exact"
    assert rows["body.digestion_fluency"]["mapping_status"] == "exact"
    assert rows["body.digestion_application"]["mapping_status"] == "standard_scope"
    # ป.2/3 has no second half at all, so nothing in it is exact.
    for key in ("plant.life_cycle_foundation", "plant.life_cycle_fluency",
                "plant.life_cycle_application"):
        assert rows[key]["mapping_status"] == "standard_scope", key


def test_every_care_table_is_one_to_one_and_answers_its_own_situations():
    for cares, needs in ((BODY_CARE, BODY_CARE_NEEDS),
                         (PLANT_CARE, PLANT_CARE_NEEDS),
                         (LIVING_CARE, LIVING_CARE_NEEDS),
                         (RESPECT_CARE, RESPECT_NEEDS),
                         (DIET_CARE, DIET_NEEDS),
                         (DIGESTIVE_CARE, DIGESTIVE_NEEDS)):
        assert len(cares) >= 4
        for field in ("practice", "reason"):
            values = [getattr(item, field) for item in cares]
            assert len(values) == len(set(values)), field
        practices = {item.practice for item in cares}
        answered = [need.practice for need in needs]
        assert set(answered) <= practices
        assert len(answered) == len(set(answered)) >= 5
        assert len({need.situation for need in needs}) == len(needs)


def test_body_parts_are_only_ever_offered_against_their_own_group():
    """ใบ must never be a distractor for a question about a cat."""
    groups = {}
    for part in PARTS:
        groups.setdefault(part.group, []).append(part)
    assert set(groups) == {"มนุษย์", "สัตว์", "พืช"}, "the indicator names all three"
    assert all(len(members) >= 4 for members in groups.values())
    by_name = {part.name: part for part in PARTS}
    for seed in range(600):
        question = generate("life.body_parts_foundation", random.Random(seed))
        stem = _text(question.stem)
        offered = {_text(choice.content) for choice in question.choices}
        named = next((name for name in by_name if f"“{name}”" in stem), None)
        if named is not None:
            group = by_name[named].group
            assert _answer(question) in {by_name[named].function, by_name[named].look}
        else:
            group = next(name for name in groups if f"ของ{name}" in stem)
            assert _answer(question) in {part.name for part in groups[group]}
        allowed = {part.name for part in groups[group]}
        allowed |= {part.function for part in groups[group]}
        allowed |= {part.look for part in groups[group]}
        assert offered <= allowed, stem


def test_every_activity_names_more_than_one_part_working_together():
    """ป.1/1's second half is about parts working together, not one part alone."""
    assert len({item.name for item in ACTIVITIES}) == len(ACTIVITIES) >= 5
    assert len({item.together for item in ACTIVITIES}) == len(ACTIVITIES)
    for item in ACTIVITIES:
        named = [part.name for part in PARTS
                 if part.group == "มนุษย์" and part.name in item.together]
        assert len(named) >= 2, item.name


def test_one_trial_changes_two_things_and_therefore_shows_nothing():
    """The point of ป.2/1: evidence only supports a conclusion if it is fair."""
    conclusions = [trial.conclusion for trial in TRIALS]
    assert len(conclusions) == len(set(conclusions)) >= 5
    unfair = [trial for trial in TRIALS if "บอกไม่ได้" in trial.conclusion]
    assert len(unfair) == 1, "exactly one trial is deliberately unfair"


def test_the_flowering_cycle_reads_off_one_stored_order():
    assert FLOWER_CYCLE[0] == "เมล็ด"
    assert len(FLOWER_CYCLE) == len(set(FLOWER_CYCLE)) >= 4
    assert [stage.name for stage in FLOWER_STAGES] == list(FLOWER_CYCLE)
    checked = {"next": 0, "order": 0, "wrap": 0}
    for seed in range(600):
        question = generate("plant.life_cycle_fluency", random.Random(seed))
        stem = _text(question.stem)
        if "เรียงลำดับ" in stem:
            checked["order"] += 1
            assert _answer(question) == " → ".join(FLOWER_CYCLE), stem
            continue
        current = next(name for name in FLOWER_CYCLE if f"“{name}”" in stem)
        index = FLOWER_CYCLE.index(current)
        if stem.startswith("ก่อนจะถึงระยะ"):
            # The reverse form: one step back, wrapping from the seed to the last stage.
            checked["before"] = checked.get("before", 0) + 1
            assert _answer(question) == FLOWER_CYCLE[index - 1], stem
            continue
        checked["next"] += 1
        if index == len(FLOWER_CYCLE) - 1:
            checked["wrap"] += 1
        assert _answer(question) == FLOWER_CYCLE[(index + 1) % len(FLOWER_CYCLE)]
    # A life cycle is a cycle: the last stage has to lead back to the first.
    assert all(checked.values()), checked


def test_two_animals_sharing_a_cycle_are_never_both_offered():
    """ตั๊กแตน and แมลงสาบ have identical stages; only one may appear per item."""
    assert len({cycle.animal for cycle in CYCLES}) == len(CYCLES) >= 6
    assert len(PATTERNS) >= 4
    shared = [cycle.stages for cycle in CYCLES]
    assert len(shared) != len(set(shared)), "the collision this test guards is real"
    for seed in range(600):
        question = generate("animal.life_cycle_foundation", random.Random(seed))
        choices = [_text(choice.content) for choice in question.choices]
        assert len(choices) == len(set(choices)) == 4, seed


def test_each_pattern_question_offers_only_real_patterns():
    by_animal = {cycle.animal: cycle for cycle in CYCLES}
    checked = {"pattern": 0, "partner": 0}
    for seed in range(600):
        question = generate("animal.life_cycle_fluency", random.Random(seed))
        stem = _text(question.stem)
        animal = next(name for name in by_animal if f"“{name}”" in stem)
        offered = {_text(choice.content) for choice in question.choices}
        if "แบบเดียวกับ" in stem:
            checked["partner"] += 1
            assert offered <= set(by_animal), stem
            assert by_animal[_answer(question)].pattern == by_animal[animal].pattern
            continue
        checked["pattern"] += 1
        assert offered <= set(PATTERNS), stem
        assert _answer(question) == by_animal[animal].pattern, stem
    assert all(checked.values()), checked


def test_the_four_plant_organs_are_exactly_the_ones_the_indicator_names():
    names = [organ.name for organ in ORGANS]
    assert names == ["ราก", "ลำต้น", "ใบ", "ดอก"]
    for field in ("function", "without"):
        values = [getattr(organ, field) for organ in ORGANS]
        assert len(values) == len(set(values)), field


def test_every_meal_is_short_of_exactly_the_group_named():
    groups = {nutrient.name for nutrient in NUTRIENTS}
    assert len(groups) == len(NUTRIENTS) >= 5
    assert {meal.missing for meal in MEALS} <= groups
    assert len({meal.description for meal in MEALS}) == len(MEALS) >= 5
    for seed in range(600):
        question = generate("body.nutrient_group_fluency", random.Random(seed))
        stem = _text(question.stem)
        offered = {_text(choice.content) for choice in question.choices}
        assert offered <= groups, stem
        meal = next(item for item in MEALS if item.description in stem)
        assert _answer(question) == meal.missing, stem


def test_each_guideline_and_each_day_record_has_its_own_answer():
    advice = [item.advice for item in GUIDELINES]
    reasons = [item.reason for item in GUIDELINES]
    assert len(advice) == len(set(advice)) >= 5
    assert len(reasons) == len(set(reasons)) == len(advice)
    answered = [chosen for _, chosen in GUIDELINE_NEEDS]
    assert set(answered) <= set(advice)
    assert len(answered) == len(set(answered)) >= 5
    verdicts = [record.verdict for record in DAY_RECORDS]
    assert len(verdicts) == len(set(verdicts)) >= 5
    assert len({record.record for record in DAY_RECORDS}) == len(DAY_RECORDS)


def test_the_food_path_runs_in_one_direction_and_liver_is_off_it():
    assert FOOD_PATH[0] == "ปาก" and FOOD_PATH[-1] == "ทวารหนัก"
    assert len(FOOD_PATH) == len(set(FOOD_PATH)) >= 5
    assert FOOD_PATH.index("ลำไส้เล็ก") < FOOD_PATH.index("ลำไส้ใหญ่")
    # ตับ helps from the side; putting it on the path would be wrong.
    assert "ตับ" not in FOOD_PATH
    assert "ตับ" in {organ.name for organ in DIGESTIVE_ORGANS}
    for field in ("name", "function"):
        values = [getattr(organ, field) for organ in DIGESTIVE_ORGANS]
        assert len(values) == len(set(values)), field


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "life.body_parts_foundation": 30,
        "life.body_parts_fluency": 12,
        "life.body_parts_application": 6,
        "life.body_care_foundation": 12,
        "life.body_care_fluency": 6,
        "life.body_care_application": 6,
        "plant.growth_needs_foundation": 8,
        "plant.growth_evidence_fluency": 6,
        "plant.growth_application": 6,
        "plant.plant_care_foundation": 12,
        "plant.plant_care_fluency": 6,
        "plant.plant_care_application": 6,
        "plant.life_cycle_foundation": 10,
        "plant.life_cycle_fluency": 6,
        "plant.life_cycle_application": 6,
        "life.living_needs_foundation": 8,
        "life.living_needs_fluency": 6,
        "life.living_needs_application": 6,
        "life.living_care_foundation": 12,
        "life.living_care_fluency": 6,
        "life.living_care_application": 6,
        "animal.life_cycle_foundation": 20,
        "animal.life_cycle_fluency": 10,
        "animal.life_cycle_application": 6,
        "animal.respect_life_foundation": 12,
        "animal.respect_life_fluency": 6,
        "animal.respect_life_application": 6,
        "plant.organ_function_foundation": 8,
        "plant.organ_function_fluency": 8,
        "plant.organ_function_application": 6,
        "body.nutrient_group_foundation": 18,
        "body.nutrient_group_fluency": 6,
        "body.nutrient_group_application": 6,
        "body.food_choice_foundation": 12,
        "body.food_choice_fluency": 6,
        "body.food_choice_application": 6,
        "body.own_diet_foundation": 12,
        "body.own_diet_fluency": 6,
        "body.own_diet_application": 6,
        "body.digestive_organs_foundation": 12,
        "body.digestion_fluency": 11,
        "body.digestion_application": 6,
        "body.digestive_care_foundation": 12,
        "body.digestive_care_fluency": 6,
        "body.digestive_care_application": 6,
    }
    assert set(minimums) == set(NEW_KEYS)
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
