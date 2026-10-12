"""จีโนไทป์ ฟีโนไทป์ และอัตราส่วนของรุ่นลูก

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.3/3

Sets moved here from: science_wave_b26.
"""

from __future__ import annotations

from collections import Counter
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import Fact, _fact_question
from otk.sets._support.science_wave_b25 import (
    CROSS_TOPIC,
    MENDEL_TRAITS,
    MIDDLE_THREE,
    MendelTrait,
    _genotypes,
)
from otk.sets._support.science_wave_b26 import PUNNETT_SCENARIOS

PROVENANCE = Provenance("original")


RATIO_FACTS = (
    Fact("จีโนไทป์ของลูกเกิดขึ้นได้อย่างไร",
         "ลูกได้รับแอลลีลหนึ่งตัวจากพ่อและอีกหนึ่งตัวจากแม่ "
         "แอลลีลสองตัวนั้นมารวมกันเป็นจีโนไทป์ของลูก"),
    Fact("ฟีโนไทป์ของลูกถูกกำหนดโดยอะไร",
         "ถูกกำหนดโดยจีโนไทป์ที่ลูกได้รับ โดยถ้ามีแอลลีลเด่นอยู่อย่างน้อยหนึ่งตัว "
         "ฟีโนไทป์ที่ปรากฏจะเป็นลักษณะเด่น"),
    Fact("เหตุใดจีโนไทป์สองแบบจึงให้ฟีโนไทป์เดียวกันได้",
         "เพราะการข่มอย่างสมบูรณ์ทำให้ทั้ง TT และ Tt แสดงลักษณะเด่นเหมือนกัน "
         "จำนวนแบบของฟีโนไทป์จึงน้อยกว่าจำนวนแบบของจีโนไทป์"),
    Fact("ตารางพันเนตต์ใช้ทำอะไร",
         "ใช้จับคู่แอลลีลที่พ่อและแม่แต่ละฝ่ายให้ได้ทุกแบบ "
         "เพื่อหาจีโนไทป์ที่เป็นไปได้ของลูกและสัดส่วนของแต่ละแบบ"),
    Fact("อัตราส่วนที่คำนวณจากตารางพันเนตต์หมายความว่าอย่างไร",
         "เป็นสัดส่วนที่คาดหวังเมื่อมีลูกจำนวนมาก "
         "ไม่ใช่จำนวนที่ต้องเกิดขึ้นตรงตามนั้นในลูกทุกครอก"),
    Fact("การผสมระหว่างพ่อแม่ที่เป็นพันธุ์ทางทั้งคู่ให้ผลอย่างไร",
         "ให้จีโนไทป์สามแบบในอัตราส่วน 1 : 2 : 1 "
         "และให้ฟีโนไทป์สองแบบในอัตราส่วน 3 : 1"),
)


# Every ordered pair of the three genotypes, indexed as in ``_genotypes``.
PARENT_PAIRS = tuple((first, second) for first in range(3) for second in range(3))


def _cross(first: str, second: str) -> list[str]:
    """Every offspring genotype from the cross, written with the dominant first."""
    children = []
    for one in first:
        for two in second:
            children.append("".join(sorted((one, two))))
    return children


def _genotype_ratio(trait: MendelTrait, first: str, second: str) -> str:
    counts = Counter(_cross(first, second))
    codes = _genotypes(trait)
    parts = [counts.get(code, 0) for code in codes]
    divisor = min((part for part in parts if part), default=1)
    return " : ".join(str(part // divisor) for part in parts)


def _phenotype_ratio(trait: MendelTrait, first: str, second: str) -> str:
    upper = trait.letter
    children = _cross(first, second)
    dominant = sum(1 for child in children if upper in child)
    recessive = len(children) - dominant
    divisor = min((part for part in (dominant, recessive) if part), default=1)
    return f"{dominant // divisor} : {recessive // divisor}"


@question_type(
    "life.punnett_foundation",
    display_name={"th": "การเกิดจีโนไทป์และฟีโนไทป์ของลูก"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=CROSS_TOPIC,
)
class PunnettFoundation(QuestionType):
    """How the child's genotype and phenotype come about."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, RATIO_FACTS, topic=CROSS_TOPIC,
            hint="แยกให้ชัดว่าจีโนไทป์คือคู่ของแอลลีล "
                 "ส่วนฟีโนไทป์คือลักษณะที่ปรากฏออกมา",
        )


@question_type(
    "life.punnett_fluency",
    display_name={"th": "คำนวณอัตราส่วนจีโนไทป์และฟีโนไทป์ของรุ่นลูก"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=CROSS_TOPIC,
)
class PunnettFluency(QuestionType):
    """Compute the ratio the cross gives — ``คำนวณอัตราส่วน`` itself.

    Both the answer and the distractors are computed from real crosses, so every
    wrong choice is the right answer to a *different* cross rather than a number
    invented to look plausible.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        trait = rng.choice(MENDEL_TRAITS)
        codes = _genotypes(trait)
        first, second = rng.choice(PARENT_PAIRS)
        one, two = codes[first], codes[second]
        genotype = rng.random() < 0.5
        ratio = _genotype_ratio if genotype else _phenotype_ratio
        correct = ratio(trait, one, two)
        others = []
        for left, right in PARENT_PAIRS:
            value = ratio(trait, codes[left], codes[right])
            if value != correct and value not in others:
                others.append(value)
        rng.shuffle(others)
        if genotype:
            question = (f"อัตราส่วนของจีโนไทป์ {codes[0]} : {codes[1]} : "
                        f"{codes[2]} ในรุ่นลูกเป็นเท่าใด")
            hint = ("เขียนตารางพันเนตต์ให้ครบสี่ช่องก่อน "
                    "แล้วจึงนับว่าแต่ละจีโนไทป์ปรากฏกี่ช่อง")
        else:
            question = (f"อัตราส่วนของฟีโนไทป์ {trait.dominant} : "
                        f"{trait.recessive} ในรุ่นลูกเป็นเท่าใด")
            hint = ("นับช่องที่มีแอลลีลเด่นอย่างน้อยหนึ่งตัวเป็นลักษณะเด่น "
                    "เหลือเฉพาะช่องที่มีแอลลีลด้อยทั้งคู่จึงเป็นลักษณะด้อย")
        return _labelled(
            stem=f"ใน{trait.subject} แอลลีล {trait.letter} ซึ่งควบคุม"
                 f"{trait.dominant} ข่มแอลลีล {trait.letter.lower()} "
                 f"ซึ่งควบคุม{trait.recessive} อย่างสมบูรณ์ "
                 f"เมื่อผสม {one} กับ {two} {question}",
            correct=correct, wrongs=tuple(others[:3]), hint=hint,
            topic=CROSS_TOPIC,
        )


@question_type(
    "life.punnett_application",
    display_name={"th": "วิเคราะห์อัตราส่วนและจีโนไทป์ของพ่อแม่"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=CROSS_TOPIC,
)
class PunnettApplication(QuestionType):
    """Work back from the offspring seen to the parents' genotypes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, PUNNETT_SCENARIOS,
            hint="ลักษณะด้อยที่ปรากฏในลูกบอกได้ว่าพ่อแม่ทั้งสองฝ่ายมีแอลลีลด้อย "
                 "และอัตราส่วนเป็นค่าที่คาดหวัง ไม่ใช่จำนวนที่ต้องเกิดจริง",
        ), CROSS_TOPIC)
