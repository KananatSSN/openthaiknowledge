"""ธาตุอาหารของพืช

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/14

Sets moved here from: science_wave_b6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import contextual_scenario_question
from otk.sets._support.science_wave_b6 import (
    LEVEL,
    NUTRIENT_SCENARIOS,
    NUTRIENTS,
    SUBJECT,
    TOPIC,
    _labelled,
)

PROVENANCE = Provenance("original")


@question_type(
    "plant.nutrient_foundation",
    display_name={"th": "ความสำคัญของธาตุอาหารแต่ละชนิดต่อพืช"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class NutrientFoundation(QuestionType):
    """Name a nutrient's job, or the nutrient that does a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(NUTRIENTS)
        others = [other for other in NUTRIENTS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” มีความสำคัญต่อพืชอย่างไร",
                correct=item.role,
                wrongs=tuple(other.role for other in others[:3]),
                hint="นึกถึงว่าธาตุนั้นเป็นส่วนประกอบของอะไรในพืช "
                     "หรือส่งเสริมการเจริญของส่วนใดเป็นพิเศษ",
            )
        return _labelled(
            stem=f"ธาตุอาหารใดของพืชทำหน้าที่{item.role}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกธาตุที่ทำหน้าที่นั้นโดยตรง",
        )


@question_type(
    "plant.nutrient_deficiency_fluency",
    display_name={"th": "อาการขาดธาตุอาหารของพืช"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class NutrientDeficiencyFluency(QuestionType):
    """Read a symptom for the nutrient that is short, or the other way round.

    The symptoms are deliberately close to one another — several kinds of yellow
    leaf — because telling them apart is what a grower actually has to do, and
    what turns "ไนโตรเจนทำให้ใบเขียว" into something usable.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(NUTRIENTS)
        others = [other for other in NUTRIENTS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"พืชแสดงอาการ “{item.deficiency}” พืชน่าจะขาดธาตุอาหารใด",
                correct=item.name,
                wrongs=tuple(other.name for other in others[:3]),
                hint="สังเกตว่าอาการเกิดที่ใบแก่หรือใบอ่อนก่อน "
                     "และเกิดทั้งใบหรือเฉพาะบางส่วนของใบ",
            )
        return _labelled(
            stem=f"พืชที่ขาด “{item.name}” จะแสดงอาการอย่างไร",
            correct=item.deficiency,
            wrongs=tuple(other.deficiency for other in others[:3]),
            hint="ธาตุที่พืชเคลื่อนย้ายจากใบแก่ไปเลี้ยงใบอ่อนได้ "
                 "จะทำให้ใบแก่แสดงอาการก่อน",
        )


@question_type(
    "plant.nutrient_application",
    display_name={"th": "วินิจฉัยปัญหาการเจริญเติบโตของพืชจากธาตุอาหาร"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class NutrientApplication(QuestionType):
    """Diagnose a real plant from what it looks like and where it is growing."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, NUTRIENT_SCENARIOS,
            hint="ระบุก่อนว่าอาการอยู่ที่ใบแก่ ใบอ่อน ราก หรือผล "
                 "แล้วจึงจับคู่กับธาตุที่ทำหน้าที่ตรงส่วนนั้น",
            topic=TOPIC,
        )
