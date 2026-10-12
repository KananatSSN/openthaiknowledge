"""``ConceptBankType`` — a fixed bank of single-fact multiple-choice items.

Some สาระ is neither a calculation nor a category table: it is a set of concept
questions, each with one correct statement and its own hand-picked wrong ones
(conditions, definitions, applications). This base holds that bank and draws one
item per question; the item carries its own distractors, so the choices stay
diagnostic rather than random.

A subclass sets ``ITEMS`` to a list of :class:`Concept`; nothing else is needed.
Provide at least three distractors per item for a full four choices. An item
with more than three has three of them drawn each time, so a longer list of
plausible wrong statements widens the bank without a new stem.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import text
from otk.core.distractors import label_pool, length_matched_label_pool
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType


class Concept(NamedTuple):
    """One fixed MCQ item: a Thai question, its answer, and its own distractors."""
    stem: str
    correct: str
    distractors: tuple[str, ...]


class ConceptBankType(QuestionType):
    """Draw one item from a fixed ``ITEMS`` bank; each carries its distractors."""

    ITEMS: list[Concept] = []

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        it = rng.choice(self.ITEMS)
        # Every distractor goes to the pool: ``label_pool`` shuffles and takes
        # three, and the spares let the registry's length balancing swap in one
        # that is not visibly shorter than the answer.
        return GeneratedQuestion(
            stem=[text(it.stem)],
            correct=[text(it.correct)],
            distractors=label_pool(list(it.distractors)),
            topic=self.topic,
        )


def more_wrongs(bank: tuple, extras: tuple) -> tuple:
    """The same (สถานการณ์, ข้อสรุป, ตัวลวง) rows, each with further wrong readings appended.

    ``extras`` holds one tuple per row, in order. A row that carries more than three
    wrong readings has three drawn each time by ``label_pool``, so this widens a
    scenario bank without a new stem.
    """
    assert len(extras) == len(bank), "one tuple of extra wrong readings per row"
    rows = []
    for (stem, right, wrongs), more in zip(bank, extras):
        merged = (*wrongs, *more)
        assert right not in merged and len(set(merged)) == len(merged), stem
        rows.append((stem, right, merged))
    return tuple(rows)


def widen(items: list[Concept], extras: tuple) -> list[Concept]:
    """``ITEMS`` with further wrong statements appended to each item, in order."""
    assert len(extras) == len(items), "one tuple of extra wrong statements per item"
    out = []
    for item, more in zip(items, extras):
        merged = (*item.distractors, *more)
        assert item.correct not in merged and len(set(merged)) == len(merged), item.stem
        out.append(Concept(item.stem, item.correct, merged))
    return out


def contextual_scenario_question(rng: Random, bank: tuple, *, hint: str,
                                 topic: str) -> GeneratedQuestion:
    """Draw a scenario with substantial, context-specific alternatives.

    Each bank row is ``(stem, correct, wrongs)``.  Correct explanations from
    other rows are true in their own scenarios but do not explain the selected
    evidence, making them useful length-balanced distractors without inventing
    filler.  The stem explicitly asks for the best contextual match so only the
    selected row is defensible.
    """
    index = rng.randrange(len(bank))
    stem, correct, wrongs = bank[index]
    alternatives = [*wrongs, *(row[1] for i, row in enumerate(bank) if i != index)]
    return GeneratedQuestion(
        stem=[text(
            f"{stem} (เลือกคำอธิบายที่ตรงกับข้อมูลในสถานการณ์นี้มากที่สุด)"
        )],
        correct=[text(correct)],
        distractors=length_matched_label_pool([correct, *alternatives]),
        topic=topic,
        hint=[text(hint)],
    )
