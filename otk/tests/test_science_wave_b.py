"""Acceptance tests for Wave B — the ม.3 ecology block, ว 1.1."""

from __future__ import annotations

import csv
import random
import re
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import (
    SCIENCE_BASELINE_KEYS,
    SCIENCE_WAVE_B_KEYS,
    SCIENCE_WAVE_KEYS,
)
from otk.sets._support.science_wave_b import (
    BALANCE_SCENARIOS,
    DECOMPOSER_SCENARIOS,
    INTERACTION_SURVEYS,
    RELATIONSHIPS,
    RELATIONSHIP_SURVEYS,
    TOXIN_SCENARIOS,
)
from otk.sets.biology.m3.ecosystem_balance_and_conservation import (
    DAMAGING_ACTIONS,
    PROTECTIVE_ACTIONS,
)
from otk.sets.biology.m3.food_webs_and_energy_transfer import (
    ENERGY_MEASUREMENTS,
    FOOD_WEBS,
    PRODUCER_ENERGY,
    chains_to,
    predators_of,
    trophic_level,
)
from otk.sets.biology.m3.relationships_between_organisms import SIGN_PAIRS
from otk.sets.biology.m3.biomagnification import TOXIN_CASES, magnification_factor
from otk.sets.biology.m3.producers_consumers_decomposers import (
    DecomposerRoleFoundation,
    MatterCycleFluency,
)
from otk.sets.biology.m3.ecosystem_components_and_levels import EcosystemComponentsFluency


NEW_KEYS = {
    "ecology.ecosystem_components_fluency": ("ว 1.1 ม.3/1", 2),
    "ecology.ecosystem_interaction_application": ("ว 1.1 ม.3/1", 3),
    "ecology.relationship_signs_fluency": ("ว 1.1 ม.3/2", 2),
    "ecology.relationship_survey_application": ("ว 1.1 ม.3/2", 3),
    "ecology.food_web_foundation": ("ว 1.1 ม.3/3", 1),
    "ecology.energy_transfer_fluency": ("ว 1.1 ม.3/3", 2),
    "ecology.food_web_application": ("ว 1.1 ม.3/3", 3),
    "ecology.decomposer_role_foundation": ("ว 1.1 ม.3/4", 1),
    "ecology.matter_cycle_fluency": ("ว 1.1 ม.3/4", 2),
    "ecology.decomposer_application": ("ว 1.1 ม.3/4", 3),
    "ecology.biomagnification_foundation": ("ว 1.1 ม.3/5", 1),
    "ecology.biomagnification_fluency": ("ว 1.1 ม.3/5", 2),
    "ecology.biomagnification_application": ("ว 1.1 ม.3/5", 3),
    "ecology.balance_foundation": ("ว 1.1 ม.3/6", 1),
    "ecology.balance_actions_fluency": ("ว 1.1 ม.3/6", 2),
    "ecology.balance_application": ("ว 1.1 ม.3/6", 3),
}
COMPLETED = ("ว 1.1 ม.3/1", "ว 1.1 ม.3/2", "ว 1.1 ม.3/3", "ว 1.1 ม.3/4",
             "ว 1.1 ม.3/5", "ว 1.1 ม.3/6")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _math(blocks) -> str:
    return " ".join(b.tex for b in blocks if b.kind == "math")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_wave_b_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    # A subset, not the whole cohort: Wave B also covers the ม.1 cell block,
    # which has its own acceptance tests.
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not SCIENCE_WAVE_B_KEYS & SCIENCE_BASELINE_KEYS
    # Wave B is its own cohort; a gate approving Wave A must not silently cover it.
    assert not SCIENCE_WAVE_B_KEYS & SCIENCE_WAVE_KEYS
    for key, (outcome, stage) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key


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


def test_the_ecosystem_component_table_covers_all_four_roles_without_overlap():
    categories = EcosystemComponentsFluency.CATEGORIES
    assert [category.label for category in categories] == [
        "องค์ประกอบทางกายภาพ (ไม่มีชีวิต)", "ผู้ผลิต", "ผู้บริโภค",
        "ผู้ย่อยสลายสารอินทรีย์",
    ]
    members = [member for category in categories for member in category.members]
    # An example in two categories would make the classify direction ambiguous.
    assert len(members) == len(set(members))
    for category in categories:
        assert len(category.members) >= 4, category.label


def test_component_answers_come_from_the_authored_table():
    owner = {member: category.label
             for category in EcosystemComponentsFluency.CATEGORIES
             for member in category.members}
    labels = {category.label for category in EcosystemComponentsFluency.CATEGORIES}
    seen = set()
    for seed in range(600):
        question = generate("ecology.ecosystem_components_fluency", random.Random(seed))
        stem = _text(question.stem)
        member = next((name for name in owner if f"“{name}”" in stem), None)
        if member is None:
            # The other direction: name a category, pick an example of it.
            label = next(name for name in labels if stem.endswith(name))
            assert owner[_answer(question)] == label, stem
            continue
        seen.add(member)
        assert _answer(question) == owner[member], stem
    assert len(seen) > 15


def test_every_relationship_carries_one_sign_pair_used_by_both_directions():
    for name, signs, examples in RELATIONSHIPS:
        assert signs in SIGN_PAIRS, name
        assert len(examples) >= 3, name
    by_name = {name: signs for name, signs, _ in RELATIONSHIPS}
    # The two (+, −) patterns are the pair the set exists to separate.
    assert by_name["ภาวะล่าเหยื่อ"] == by_name["ภาวะปรสิต"]
    assert by_name["ภาวะแข่งขัน"] != by_name["ภาวะพึ่งพากัน"]

    examples = {example: signs for _, signs, group in RELATIONSHIPS
                for example in group}
    checked = {"name": 0, "example": 0, "contrast": 0}
    for seed in range(600):
        question = generate("ecology.relationship_signs_fluency", random.Random(seed))
        stem = _text(question.stem)
        name = next((key for key in by_name if f"“{key}”" in stem), None)
        if name is not None:
            checked["name"] += 1
            assert _answer(question) == by_name[name], stem
            continue
        example = next((key for key in examples if f"“{key}”" in stem), None)
        if example is not None:
            checked["example"] += 1
            assert _answer(question) == examples[example], stem
            continue
        checked["contrast"] += 1
        assert "ภาวะล่าเหยื่อกับภาวะปรสิต" in stem, stem
    assert all(checked.values()), checked


def test_sign_pair_questions_offer_all_four_pairs_and_nothing_else():
    for seed in range(600):
        question = generate("ecology.relationship_signs_fluency", random.Random(seed))
        choices = {_text(choice.content) for choice in question.choices}
        if not choices & set(SIGN_PAIRS):
            continue        # the predation-versus-parasitism item
        assert choices == set(SIGN_PAIRS), choices


def test_authored_scenario_banks_are_well_formed():
    for bank in (INTERACTION_SURVEYS, RELATIONSHIP_SURVEYS, DECOMPOSER_SCENARIOS,
                 TOXIN_SCENARIOS, BALANCE_SCENARIOS):
        stems = [stem for stem, _, _ in bank]
        assert len(stems) == len(set(stems)) >= 6
        for stem, correct, wrongs in bank:
            assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
            assert correct not in wrongs, stem
            assert stem.rstrip().endswith(
                ("ถูกต้อง", "รูปแบบใด", "ได้ดีที่สุด", "เหมาะสมที่สุด",
                 "ที่สุด", "เพราะเหตุใด")), stem


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "ecology.ecosystem_components_fluency": 20,
        "ecology.ecosystem_interaction_application": 6,
        "ecology.relationship_signs_fluency": 20,
        "ecology.relationship_survey_application": 6,
        "ecology.food_web_foundation": 25,
        "ecology.energy_transfer_fluency": 25,
        "ecology.food_web_application": 25,
        "ecology.decomposer_role_foundation": 7,
        "ecology.matter_cycle_fluency": 25,
        "ecology.decomposer_application": 6,
        "ecology.biomagnification_foundation": 7,
        "ecology.biomagnification_fluency": 10,
        "ecology.biomagnification_application": 6,
        "ecology.balance_foundation": 7,
        "ecology.balance_actions_fluency": 12,
        "ecology.balance_application": 6,
    }
    for key, minimum in minimums.items():
        signatures = set()
        for seed in range(1000):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) or _math(choice.content)
                       for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            signatures.add((_text(question.stem), choices[question.answer]))
        assert len(signatures) >= minimum, (key, len(signatures))


def test_every_food_web_is_readable_and_its_levels_unambiguous_where_asked():
    """A web whose organism sits at two levels at once has no single answer."""
    for web in FOOD_WEBS:
        assert web.producer not in web.eats, web.habitat
        for name, prey in web.eats.items():
            assert prey, name
            assert name not in prey, name
            for item in prey:
                assert item == web.producer or item in web.eats, (name, item)
        for name in web.eats:
            # Every consumer is reachable from the producer, or it is not a web.
            assert chains_to(web, name), (web.habitat, name)
        ambiguous = [name for name in web.eats if trophic_level(web, name) is None]
        # Ambiguous ones are allowed and simply never asked about, but a web made
        # only of them would leave the level branch with nothing to draw.
        assert len(ambiguous) < len(web.eats), web.habitat


def test_food_web_answers_are_rederived_from_the_web_printed_in_the_stem():
    by_habitat = {web.habitat: web for web in FOOD_WEBS}
    names = {1: "ผู้ผลิต", 2: "ผู้บริโภคลำดับที่ 1", 3: "ผู้บริโภคลำดับที่ 2",
             4: "ผู้บริโภคลำดับที่ 3", 5: "ผู้บริโภคลำดับที่ 4"}
    checked = {"eats": 0, "level": 0}
    for seed in range(900):
        question = generate("ecology.food_web_foundation", random.Random(seed))
        stem = _text(question.stem)
        web = next(web for habitat, web in by_habitat.items() if habitat in stem)
        organisms = (web.producer, *web.eats)
        if "สิ่งมีชีวิตใดกิน" in stem:
            checked["eats"] += 1
            target = next(name for name in organisms
                          if stem.rstrip().endswith("สิ่งมีชีวิตใดกิน" + name))
            assert predators_of(web, target) == (_answer(question),), stem
            continue
        checked["level"] += 1
        target = next(name for name in organisms
                      if name + "ทำหน้าที่เป็นอะไร" in stem)
        level = trophic_level(web, target)
        assert level is not None, stem
        assert _answer(question) == names[level], stem
    assert all(checked.values()), checked


def test_path_counts_and_sole_food_answers_follow_from_the_web():
    by_habitat = {web.habitat: web for web in FOOD_WEBS}
    checked = {"paths": 0, "sole": 0, "alternative": 0}
    for seed in range(900):
        question = generate("ecology.food_web_application", random.Random(seed))
        stem = _text(question.stem)
        web = next(web for habitat, web in by_habitat.items() if habitat in stem)
        if "ได้กี่เส้นทาง" in stem:
            checked["paths"] += 1
            target = next(name for name in web.eats
                          if "ถ่ายทอดไปถึง" + name + "ได้กี่เส้นทาง" in stem)
            expected = str(len(chains_to(web, target))) + " เส้นทาง"
            assert _answer(question) == expected, stem
            continue
        if "ได้รับผลกระทบรุนแรงที่สุด" in stem:
            checked["sole"] += 1
            lost = next(name for name in (web.producer, *web.eats)
                        if "ถ้า" + name + "หายไปจากพื้นที่นี้" in stem)
            answer = _answer(question).split(" ")[0]
            # The one hit hardest must be the one with nothing else to eat.
            assert web.eats[answer] == (lost,), stem
            continue
        checked["alternative"] += 1
        eater = next(name for name, prey in web.eats.items()
                     if len(prey) >= 2 and name + "น่าจะเป็นอย่างไร" in stem)
        assert len(web.eats[eater]) >= 2, stem
        assert _answer(question).startswith("ยังอยู่ได้"), stem
    assert all(checked.values()), checked


def test_energy_transfer_rows_divide_cleanly_and_are_not_all_ten_per_cent():
    for energy in PRODUCER_ENERGY:
        assert energy % 1000 == 0, energy
    for lower, upper in ENERGY_MEASUREMENTS:
        assert upper < lower, (lower, upper)
        assert upper * 100 % lower == 0, (lower, upper)
    # A table of tens would let the answer be recited instead of computed.
    percents = {upper * 100 // lower for lower, upper in ENERGY_MEASUREMENTS}
    assert len(percents) > 1 and percents != {10}


def test_energy_answers_are_rebuilt_from_the_numbers_in_the_stem():
    checked = {"down": 0, "up": 0, "percent": 0}
    for seed in range(900):
        question = generate("ecology.energy_transfer_fluency", random.Random(seed))
        stem = _text(question.stem)
        numbers = [int(value.replace(",", ""))
                   for value in re.findall(r"[\d,]{3,}", stem)]
        answer = int(_math(question.choices[question.answer].content))
        if "จะได้รับพลังงานประมาณเท่าใด" in stem:
            checked["down"] += 1
            steps = int(re.search(r"ผู้บริโภคลำดับที่ (\d+)", stem).group(1))
            assert answer == numbers[0] // 10 ** steps, stem
        elif "ผู้ผลิตในระบบนิเวศนี้ตรึงพลังงานไว้" in stem:
            checked["up"] += 1
            assert answer == numbers[0] * 100, stem
        else:
            checked["percent"] += 1
            lower, upper = numbers[0], numbers[1]
            assert answer == upper * 100 // lower, stem
    assert all(checked.values()), checked


def test_function_and_concept_tables_offer_four_choices_and_no_overlap():
    categories = MatterCycleFluency.CATEGORIES
    # Three categories would make ClassifyType emit three-choice questions.
    assert len(categories) == 4
    members = [member for category in categories for member in category.members]
    assert len(members) == len(set(members))
    stems = [item.stem for item in DecomposerRoleFoundation.ITEMS]
    assert len(stems) == len(set(stems)) >= 6
    for item in DecomposerRoleFoundation.ITEMS:
        assert len(item.distractors) >= 3, item.stem
        assert item.correct not in item.distractors, item.stem


def test_every_toxin_case_rises_by_one_constant_factor():
    """The prediction branch reads a rate off the table, so the rate must exist."""
    for case in TOXIN_CASES:
        assert len(case.levels) == len(case.readings) >= 4, case.habitat
        assert case.source_reading > 0
        assert case.readings[0] > case.source_reading, case.habitat
        factor = magnification_factor(case)
        assert factor >= 2, case.habitat
        for lower, upper in zip(case.readings, case.readings[1:]):
            assert upper == lower * factor, (case.habitat, lower, upper)
        assert case.readings[-1] % case.source_reading == 0, case.habitat


def test_biomagnification_answers_are_rebuilt_from_the_printed_table():
    by_toxin = {case.toxin: case for case in TOXIN_CASES}
    checked = {"highest": 0, "times": 0, "predict": 0}
    for seed in range(900):
        question = generate("ecology.biomagnification_fluency", random.Random(seed))
        stem = _text(question.stem)
        case = next(case for toxin, case in by_toxin.items() if toxin in stem)
        answer = _answer(question)
        if "เข้มข้นที่สุด" in stem:
            checked["highest"] += 1
            assert answer == case.levels[-1], stem
        elif "เข้มข้นเป็นกี่เท่า" in stem:
            checked["times"] += 1
            times = case.readings[-1] // case.source_reading
            assert answer == f"{times:,} เท่า", stem
        else:
            checked["predict"] += 1
            expected = case.readings[-1] * magnification_factor(case)
            assert answer == f"{expected:,}", stem
    assert all(checked.values()), checked


def test_balance_action_questions_never_mix_the_two_lists():
    protective, damaging = set(PROTECTIVE_ACTIONS), set(DAMAGING_ACTIONS)
    # An action on both lists would make one of the two directions ambiguous.
    assert not protective & damaging
    assert len(protective) >= 6 and len(damaging) >= 6
    checked = {"damaging": 0, "protective": 0}
    for seed in range(900):
        question = generate("ecology.balance_actions_fluency", random.Random(seed))
        stem = _text(question.stem)
        choices = {_text(choice.content) for choice in question.choices}
        answer = _answer(question)
        if "ทำลายสมดุล" in stem:
            checked["damaging"] += 1
            assert answer in damaging, stem
            assert choices - {answer} <= protective, stem
        else:
            checked["protective"] += 1
            assert answer in protective, stem
            assert choices - {answer} <= damaging, stem
    assert all(checked.values()), checked
