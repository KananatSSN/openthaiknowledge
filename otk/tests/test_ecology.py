"""Tests for the นิเวศวิทยา concept types (ป.6 — สิ่งมีชีวิตกับสิ่งแวดล้อม).

``test_core.py`` already asserts the shape invariants for every registered type
(valid question, 2–4 distinct choices, answer hidden). These pin the things
specific to ecology: the classification is *correct*, and — the property that
matters most for a "pick the member" question — every distractor comes from a
*different* category, so there is never a second right answer.
"""

from __future__ import annotations

import random

import pytest

from otk.core import catalog, generate
from otk.sets._support.biology import TOPIC_ECOLOGY
from otk.sets.biology.m3.ecosystem_components_and_levels import EcoLevels
from otk.sets.biology.p5.food_chains import FeedingGroups
from otk.sets.biology.m3.relationships_between_organisms import Symbiosis

KEYS = ["ecology.feeding", "ecology.symbiosis", "ecology.levels"]

# member → category label, for the two ClassifyType tables.
FEEDING = {m: c.label for c in FeedingGroups.CATEGORIES for m in c.members}
SYMBIOSIS = {m: c.label for c in Symbiosis.CATEGORIES for m in c.members}
LEVEL_BY_NAME = {f"{lv.th} ({lv.en})": lv for lv in EcoLevels.LEVELS}


def _texts(q) -> list[str]:
    return [c.content[0].text for c in q.choices]


# ── The tables are sound ─────────────────────────────────────────────────────

@pytest.mark.parametrize("cats", [FeedingGroups.CATEGORIES, Symbiosis.CATEGORIES])
def test_no_example_belongs_to_two_categories(cats):
    # A shared example would make a "pick the member" distractor a second answer.
    members = [m for c in cats for m in c.members]
    assert len(members) == len(set(members))


def test_category_labels_are_unique():
    for cats in (FeedingGroups.CATEGORIES, Symbiosis.CATEGORIES):
        labels = [c.label for c in cats]
        assert len(labels) == len(set(labels))


def test_levels_are_ascending_and_distinct():
    names = [f"{lv.th} ({lv.en})" for lv in EcoLevels.LEVELS]
    defs = [lv.definition for lv in EcoLevels.LEVELS]
    assert names[0].startswith("สิ่งมีชีวิต") and names[-1].startswith("ชีวมณฑล")
    assert len(set(names)) == len(names)
    assert len(set(defs)) == len(defs)


# ── Answers are the correct classification ───────────────────────────────────

@pytest.mark.parametrize("key,table,verb", [
    ("ecology.feeding", FEEDING, "จัดอยู่ในกลุ่ม"),
    ("ecology.symbiosis", SYMBIOSIS, "จัดเป็นรูปแบบ"),
])
def test_classify_answer_matches_the_table(key, table, verb):
    rng = random.Random(1)
    seen_classify = False
    for _ in range(400):
        q = generate(key, rng, ask=1)          # 1 = classify an example
        seen_classify = True
        stem = q.stem[0].text
        member = next(m for m in table if m in stem)
        assert q.choices[q.answer].content[0].text == table[member]
    assert seen_classify


@pytest.mark.parametrize("key,cats", [
    ("ecology.feeding", FeedingGroups.CATEGORIES),
    ("ecology.symbiosis", Symbiosis.CATEGORIES),
])
def test_pick_distractors_come_only_from_other_categories(key, cats):
    by_member = {m: c.label for c in cats for m in c.members}
    rng = random.Random(2)
    for _ in range(400):
        q = generate(key, rng, ask=2)          # 2 = pick a member of a category
        stem = q.stem[0].text
        asked = next(c.label for c in cats if c.label in stem)
        answer = q.choices[q.answer].content[0].text
        assert by_member[answer] == asked      # the correct choice fits the ask
        for other in _texts(q):
            if other != answer:
                # Every distractor is a real example from a *different* category.
                assert by_member[other] != asked
    # exactly one choice belongs to the asked category → no ambiguity
        in_cat = [t for t in _texts(q) if by_member[t] == asked]
        assert in_cat == [answer]


# ── Ecological levels ────────────────────────────────────────────────────────

def test_level_example_maps_to_its_level():
    rng = random.Random(3)
    example_to_name = {ex: f"{lv.th} ({lv.en})"
                       for lv in EcoLevels.LEVELS for ex in lv.examples}
    for _ in range(300):
        q = generate("ecology.levels", rng, ask=1)   # 1 = จากตัวอย่าง
        stem = q.stem[0].text
        ex = next(e for e in example_to_name if e in stem)
        assert q.choices[q.answer].content[0].text == example_to_name[ex]


def test_level_order_answer_is_the_next_larger_level():
    rng = random.Random(4)
    names = [f"{lv.th} ({lv.en})" for lv in EcoLevels.LEVELS]
    for _ in range(300):
        q = generate("ecology.levels", rng, ask=3)   # 3 = ระดับที่ใหญ่ถัดขึ้นไป
        stem = q.stem[0].text
        asked = next(n for n in names if n in stem)
        answer = q.choices[q.answer].content[0].text
        assert names.index(answer) == names.index(asked) + 1


def test_ask_param_pins_one_style():
    rng = random.Random(5)
    # ask=1 (classify) always shows a "which group" stem, never a "which example".
    assert all("จัดอยู่ในกลุ่ม" in generate("ecology.feeding", rng, ask=1).stem[0].text
               for _ in range(60))
    assert all("สัตว์ในข้อใด" in generate("ecology.feeding", rng, ask=2).stem[0].text
               for _ in range(60))


# ── Catalog wiring ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("key", KEYS)
def test_catalog_places_them_under_biology_p6(key):
    entry = {t["key"]: t for t in catalog()}[key]
    assert entry["subject"] == "ชีวะ"
    assert entry["legacy_level"] == "ป.6"
    assert entry["level"]
    assert entry["topic"] == TOPIC_ECOLOGY
    assert entry["params"] == {"ask": 0}
