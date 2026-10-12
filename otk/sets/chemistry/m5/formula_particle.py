"""ธาตุ สารประกอบ และอนุภาคจากสูตรเคมี

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/1

Sets moved here from: science_wave_e1.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import math, text
from otk.core.distractors import fixed, label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e1 import SUBJECT

PROVENANCE = Provenance("original")


TOPIC_FORMULA = "ธาตุ สารประกอบ และอนุภาคจากสูตรเคมี"


class FormulaItem(NamedTuple):
    tex: str
    element_or_compound: str   # "ธาตุ" or "สารประกอบ"
    particle: str              # "อะตอม", "โมเลกุล" or "ไอออน"


ELEMENT, COMPOUND = "ธาตุ", "สารประกอบ"


ATOM, MOLECULE, ION = "อะตอม", "โมเลกุล", "ไอออน"


FORMULAS: tuple[FormulaItem, ...] = (
    FormulaItem(r"\mathrm{Na}", ELEMENT, ATOM),
    FormulaItem(r"\mathrm{Fe}", ELEMENT, ATOM),
    FormulaItem(r"\mathrm{He}", ELEMENT, ATOM),
    FormulaItem(r"\mathrm{O}_2", ELEMENT, MOLECULE),
    FormulaItem(r"\mathrm{N}_2", ELEMENT, MOLECULE),
    FormulaItem(r"\mathrm{Cl}^{-}", ELEMENT, ION),
    FormulaItem(r"\mathrm{Na}^{+}", ELEMENT, ION),
    FormulaItem(r"\mathrm{Mg}^{2{+}}", ELEMENT, ION),
    FormulaItem(r"\mathrm{H}_2\mathrm{O}", COMPOUND, MOLECULE),
    FormulaItem(r"\mathrm{CO}_2", COMPOUND, MOLECULE),
    FormulaItem(r"\mathrm{CH}_4", COMPOUND, MOLECULE),
    FormulaItem(r"\mathrm{NH}_4^{+}", COMPOUND, ION),
    FormulaItem(r"\mathrm{SO}_4^{2{-}}", COMPOUND, ION),
    FormulaItem(r"\mathrm{CO}_3^{2{-}}", COMPOUND, ION),
)


CATEGORIES: tuple[tuple[str, str], ...] = tuple(sorted({
    (item.element_or_compound, item.particle) for item in FORMULAS
}))


def _category_label(ec: str, particle: str) -> str:
    return f"{ec}ที่อยู่ในรูป{particle}"


def _formula_block(item: FormulaItem) -> list:
    return [math(item.tex)]


@question_type(
    "chem.formula_particle_foundation",
    display_name={"th": "สูตรเคมี → ธาตุหรือสารประกอบ"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class FormulaParticleFoundation(QuestionType):
    """Pick the formula that is only an element, or only a compound.

    The half of ม.5/1 that does not yet ask about the particle form.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        target = rng.choice((ELEMENT, COMPOUND))
        same = [f for f in FORMULAS if f.element_or_compound == target]
        other = [f for f in FORMULAS if f.element_or_compound != target]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        return GeneratedQuestion(
            stem=[text(f"สูตรเคมีในข้อใดต่อไปนี้แสดง{target}")],
            correct=_formula_block(correct),
            distractors=fixed(*[_formula_block(w) for w in wrongs]),
            topic=TOPIC_FORMULA,
            hint=[text("สารที่ประกอบด้วยธาตุชนิดเดียวเป็นธาตุ "
                       "ส่วนสารที่มีธาตุมากกว่าหนึ่งชนิดรวมกันด้วยพันธะเคมีเป็นสารประกอบ")],
        )


@question_type(
    "chem.formula_particle_fluency",
    display_name={"th": "สูตรเคมี → ธาตุ/สารประกอบ และอะตอม/โมเลกุล/ไอออน"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class FormulaParticleFluency(QuestionType):
    """Classify a formula on both axes at once — the full ม.5/1 indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(FORMULAS)
        label = _category_label(item.element_or_compound, item.particle)
        all_labels = [_category_label(ec, particle) for ec, particle in CATEGORIES]
        wrongs = rng.sample([candidate for candidate in all_labels if candidate != label], 3)
        return GeneratedQuestion(
            stem=[text("สารที่มีสูตรเคมี "), math(item.tex),
                  text(" จัดเป็นธาตุหรือสารประกอบ และอยู่ในรูปอะตอม โมเลกุล หรือไอออน")],
            correct=[text(label)],
            distractors=label_pool([label, *wrongs]),
            topic=TOPIC_FORMULA,
            hint=[text("ดูก่อนว่าสูตรมีธาตุชนิดเดียวหรือหลายชนิด แล้วดูว่ามีประจุกำกับไว้หรือไม่ "
                       "และมีอะตอมเดียวหรือหลายอะตอมเกาะกัน")],
        )


@question_type(
    "chem.formula_particle_application",
    display_name={"th": "จำแนกกลุ่มสูตรเคมีตามธาตุ/สารประกอบ และอนุภาค"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class FormulaParticleApplication(QuestionType):
    """Given a target category, pick the one formula that belongs to it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        ec, particle = rng.choice(CATEGORIES)
        same = [f for f in FORMULAS if (f.element_or_compound, f.particle) == (ec, particle)]
        other = [f for f in FORMULAS if (f.element_or_compound, f.particle) != (ec, particle)]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        label = _category_label(ec, particle)
        return GeneratedQuestion(
            stem=[text(f"สูตรเคมีในข้อใดต่อไปนี้จัดเป็น{label}")],
            correct=_formula_block(correct),
            distractors=fixed(*[_formula_block(w) for w in wrongs]),
            topic=TOPIC_FORMULA,
            hint=[text("ธาตุที่มีอะตอมเดียวเป็นอะตอม ธาตุหรือสารประกอบที่มีอะตอมมากกว่าหนึ่งเกาะกัน "
                       "โดยไม่มีประจุเป็นโมเลกุล และที่มีประจุกำกับเป็นไอออน")],
        )
