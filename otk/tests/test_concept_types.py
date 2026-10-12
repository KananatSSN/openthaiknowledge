"""Tests for every ``ConceptBankType`` — the fixed single-fact MCQ banks.

Parametrized over *all* registered concept banks (ฟิสิกส์ การสะท้อนกลับหมด /
การกระจายของแสง, ดาราศาสตร์ แรงโน้มถ่วง / ฤดู / ข้างขึ้นข้างแรม / น้ำขึ้นน้ำลง / …),
so a new bank in any subject is covered the moment it is added. Each item must
answer with its own correct choice and offer only its own distractors, and every
item must be reachable.
"""

from __future__ import annotations

import random

import pytest

from otk.core import REGISTRY, generate
from otk.kit.concept_bank import ConceptBankType

CONCEPT_KEYS = sorted(k for k, t in REGISTRY.items()
                      if isinstance(t, ConceptBankType))


def _answer(q) -> str:
    return q.choices[q.answer].content[0].text


@pytest.mark.parametrize("key", CONCEPT_KEYS)
def test_answer_and_distractors_come_from_the_item(key):
    items = {it.stem: it for it in REGISTRY[key].ITEMS}
    rng = random.Random(6)
    seen = set()
    for _ in range(400):
        q = generate(key, rng)
        stem = q.stem[0].text
        it = items[stem]
        seen.add(stem)
        assert _answer(q) == it.correct
        texts = {c.content[0].text for c in q.choices}
        assert it.correct in texts
        assert texts <= {it.correct, *it.distractors}   # nothing invented
    assert seen == set(items)                            # every item is drawn


@pytest.mark.parametrize("key", CONCEPT_KEYS)
def test_items_have_four_distinct_choices(key):
    for it in REGISTRY[key].ITEMS:
        assert it.correct not in it.distractors, f"{key}: answer among distractors"
        assert len({it.correct, *it.distractors}) >= 4, \
            f"{key}: fewer than four distinct choices in {it.stem!r}"


@pytest.mark.parametrize("key", CONCEPT_KEYS)
def test_item_stems_are_unique(key):
    stems = [it.stem for it in REGISTRY[key].ITEMS]
    assert len(stems) == len(set(stems)), f"{key}: duplicate item stem"
