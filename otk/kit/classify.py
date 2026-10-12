"""``ClassifyType`` — the shared "which one belongs to this group?" question type.

Many science หัวข้อ reduce to the same shape: a handful of **categories**, each
with a list of real **examples** (or properties). From one such table two ผู้เรียน
questions fall out, and this base builds both:

* ``classify`` — show one example, ask which category it belongs to. Distractors
  are the *other* category labels.
* ``pick`` — name a category, ask which example belongs to it. Distractors are
  examples drawn only from the *other* categories, so exactly one choice is right
  no matter how they shuffle.

A subclass supplies just the ``CATEGORIES`` table and two Thai stem templates
(``CLASSIFY_STEM`` with ``{member}``, ``PICK_STEM`` with ``{category}``). Wrong
choices are therefore always *real* siblings the student is studying — another
category, or an example from a different one — never an invented fact, the same
discipline as the เคมี element types.

``ask`` pins one style (``1`` = classify, ``2`` = pick); ``0`` draws one per item,
so a worksheet can drill exactly one direction.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType


class Category(NamedTuple):
    """One group in a classification and the concrete examples that belong to it."""
    label: str                     # the group name, shown as a choice
    members: tuple[str, ...]       # real examples/properties in this group


class ClassifyType(QuestionType):
    """Base for a classify/pick pair over a ``CATEGORIES`` table. See module docs."""

    CATEGORIES: list[Category] = []
    ASKS = ("classify", "pick")
    # Thai stem templates; subclasses override with their own phrasing.
    CLASSIFY_STEM = "“{member}” จัดอยู่ในกลุ่มใด"
    PICK_STEM = "ข้อใดจัดเป็น{category}"

    def build(self, rng: Random, ask: int = 0) -> GeneratedQuestion:
        cats = self.CATEGORIES
        asked = (self.ASKS[ask - 1] if 1 <= ask <= len(self.ASKS)
                 else rng.choice(self.ASKS))
        cat = rng.choice(cats)
        if asked == "classify":
            member = rng.choice(cat.members)
            return GeneratedQuestion(
                stem=[text(self.CLASSIFY_STEM.format(member=member))],
                correct=[text(cat.label)],
                distractors=label_pool([c.label for c in cats]),
                topic=self.topic,
            )
        member = rng.choice(cat.members)
        others = [m for c in cats if c.label != cat.label for m in c.members]
        return GeneratedQuestion(
            stem=[text(self.PICK_STEM.format(category=cat.label))],
            correct=[text(member)],
            distractors=label_pool(others),
            topic=self.topic,
        )
