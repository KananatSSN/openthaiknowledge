"""สิ่งที่จำเป็นต่อการดำรงชีวิตของมนุษย์และสัตว์

ชีวะ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.3/1

Sets moved here from: science_wave_b15.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import (
    ANIMAL_TOPIC,
    LIVING_NEEDS_SCENARIOS,
    PRIMARY_THREE,
    _retopic,
)

PROVENANCE = Provenance("original")


class Requirement(NamedTuple):
    """One thing living things need, and what it is needed for."""
    name: str
    reason: str
    missing: str


REQUIREMENTS = (
    Requirement("อาหาร",
                "ใช้เป็นแหล่งพลังงานและใช้สร้างร่างกายให้เจริญเติบโต",
                "ถ้าขาดไปนาน ๆ ร่างกายจะผอมลง อ่อนแรง และไม่เจริญเติบโต"),
    Requirement("น้ำ",
                "เป็นส่วนประกอบของร่างกาย และช่วยให้ร่างกายทำงานได้ตามปกติ",
                "ถ้าขาดไปจะรู้สึกกระหาย อ่อนเพลีย และอยู่ได้เพียงไม่กี่วัน"),
    Requirement("อากาศ",
                "ใช้ในการหายใจ เพื่อนำแก๊สออกซิเจนเข้าสู่ร่างกาย",
                "ถ้าขาดไปจะอยู่ได้เพียงไม่กี่นาทีเท่านั้น"),
    Requirement("ที่อยู่อาศัย",
                "เป็นที่หลบภัยจากศัตรู จากแดด และจากฝน",
                "ถ้าไม่มี จะถูกศัตรูทำร้ายได้ง่ายและทนสภาพอากาศไม่ไหว"),
)


# Humans and animals both need all four. What differs is where they get food,
# and that is the comparison the indicator's มนุษย์และสัตว์ invites.
GETTING_FOOD = (
    ("มนุษย์และสัตว์", "ต้องกินสิ่งมีชีวิตอื่นเป็นอาหาร เพราะสร้างอาหารเองไม่ได้"),
    ("พืช", "สร้างอาหารได้เองที่ใบเมื่อได้รับแสง จึงไม่ต้องกินสิ่งมีชีวิตอื่น"),
)


# Not needs and not their reasons or effects, offered only as wrong choices.
REQUIREMENT_DECOYS = ("ของเล่น", "โทรทัศน์")


REASON_DECOYS = ("ใช้สร้างอาหารขึ้นเองที่ผิวหนัง", "ใช้ทำให้ขนหรือผิวมีสีสวยขึ้น")


MISSING_DECOYS = ("ถ้าขาดไปจะตัวใหญ่ขึ้นและแข็งแรงกว่าเดิม",
                  "ถ้าขาดไปจะไม่มีผลใด ๆ เพราะร่างกายสร้างขึ้นเองได้")


@question_type(
    "life.living_needs_foundation",
    display_name={"th": "สิ่งที่จำเป็นต่อการดำรงชีวิตของมนุษย์และสัตว์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class LivingNeedsFoundation(QuestionType):
    """Name what living things need, and what they need it for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(REQUIREMENTS)
        others = [other for other in REQUIREMENTS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"มนุษย์และสัตว์ต้องการ “{item.name}” ไปเพื่ออะไร",
                correct=item.reason,
                wrongs=tuple(other.reason for other in others) + REASON_DECOYS,
                hint="นึกว่าร่างกายเอาสิ่งนั้นไปใช้ทำอะไร",
                topic=ANIMAL_TOPIC,
            )
        return _labelled(
            stem=f"สิ่งใดที่มนุษย์และสัตว์ต้องการ เพราะ{item.reason}",
            correct=item.name,
            wrongs=tuple(other.name for other in others) + REQUIREMENT_DECOYS,
            hint="อ่านเหตุผลให้จบ แล้วจึงเลือกสิ่งที่ใช้ทำแบบนั้น",
            topic=ANIMAL_TOPIC,
        )


@question_type(
    "life.living_needs_fluency",
    display_name={"th": "ผลของการขาดสิ่งที่จำเป็นต่อการดำรงชีวิต"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class LivingNeedsFluency(QuestionType):
    """Say what happens when one need is missing, and how plants differ.

    ``ป.3/1`` names มนุษย์ *and* สัตว์, and the thing that separates them from
    พืช is where the food comes from — so that comparison is asked here too.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            group, how = rng.choice(GETTING_FOOD)
            other_how = next(text for name, text in GETTING_FOOD if name != group)
            return _labelled(
                stem=f"“{group}” ได้อาหารมาอย่างไร",
                correct=how,
                wrongs=(other_how,
                        "ดูดอาหารสำเร็จรูปขึ้นมาจากดินโดยตรงทางราก",
                        "สร้างอาหารขึ้นเองในเวลากลางคืนโดยไม่ต้องใช้แสง",
                        "ดูดอาหารจากอากาศผ่านผิวหนัง"),
                hint="ถามว่าสิ่งมีชีวิตนั้นสร้างอาหารเองได้หรือไม่",
                topic=ANIMAL_TOPIC,
            )
        item = rng.choice(REQUIREMENTS)
        others = [other.missing for other in REQUIREMENTS
                  if other.missing != item.missing]
        rng.shuffle(others)
        return _labelled(
            stem=f"ถ้ามนุษย์หรือสัตว์ขาด “{item.name}” จะเกิดอะไรขึ้น",
            correct=item.missing,
            wrongs=tuple(others) + MISSING_DECOYS,
            hint="เรียงดูว่าขาดสิ่งใดแล้วอยู่ได้สั้นที่สุด และขาดสิ่งใดแล้วอยู่ได้นานกว่า",
            topic=ANIMAL_TOPIC,
        )


@question_type(
    "life.living_needs_application",
    display_name={"th": "ใช้ความรู้เรื่องสิ่งที่จำเป็นต่อการดำรงชีวิต"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class LivingNeedsApplication(QuestionType):
    """Work out what a living thing in a described situation is short of."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, LIVING_NEEDS_SCENARIOS,
            hint="ไล่ดูทีละอย่างว่าอาหาร น้ำ อากาศ และที่อยู่อาศัย "
                 "สิ่งมีชีวิตนั้นได้รับครบหรือไม่",
        ), ANIMAL_TOPIC)
