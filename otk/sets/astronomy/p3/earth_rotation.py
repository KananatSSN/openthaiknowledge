"""การหมุนรอบตัวเองของโลก กลางวันกลางคืน และการกำหนดทิศ

ดาราศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.3/2

Sets moved here from: science_wave_c2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import PRIMARY_THREE, _retopic
from otk.sets._support.science_wave_c1 import SKY_TOPIC, SUBJECT
from otk.sets._support.science_wave_c2 import ASPECTS, ROTATION_FACTS, ROTATION_SCENARIOS

PROVENANCE = Provenance("original")


MODEL = (
    "ครูวางลูกโลกไว้กลางห้องที่ปิดไฟ แล้วส่องไฟฉายดวงใหญ่ไปที่ลูกโลกจากด้านหนึ่ง "
    "โดยให้ไฟฉายแทนดวงอาทิตย์และวางนิ่งอยู่กับที่ ติดตุ๊กตาเล็ก ๆ ไว้บนลูกโลกแทน"
    "ผู้สังเกต จากนั้นค่อย ๆ หมุนลูกโลกรอบตัวเองไปทางเดียวกันอย่างช้า ๆ "
)


@question_type(
    "astro.earth_rotation_foundation",
    display_name={"th": "โลกหมุนรอบตัวเอง กลางวันกลางคืน และทิศ"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=SKY_TOPIC,
)
class EarthRotationFoundation(QuestionType):
    """Know the cause, the half-lit earth, and how east is fixed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ROTATION_FACTS,
            hint="นึกภาพลูกโลกที่หมุนอยู่หน้าไฟฉายซึ่งส่องนิ่งอยู่กับที่",
        ), SKY_TOPIC)


@question_type(
    "astro.earth_rotation_fluency",
    display_name={"th": "อธิบายสาเหตุจากแบบจำลองลูกโลกและไฟฉาย"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=SKY_TOPIC,
)
class EarthRotationFluency(QuestionType):
    """Read the globe-and-lamp model and give the cause it shows.

    The set reaches all three things the indicator names — the sun's rising and
    setting, day and night, and how direction is fixed — because only a set that
    spans them all is a defensible match for a three-object indicator.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ASPECTS)
        return _labelled(
            stem=f"{MODEL}ผลที่สังเกตได้คือ {item.seen} {item.question}",
            correct=item.correct, wrongs=tuple(item.wrongs),
            hint="สังเกตว่าในแบบจำลองนี้ สิ่งที่เคลื่อนที่คือลูกโลก ส่วนไฟฉายอยู่นิ่ง",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.earth_rotation_application",
    display_name={"th": "ใช้แบบจำลองอธิบายกลางวันกลางคืนและทิศ"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=SKY_TOPIC,
)
class EarthRotationApplication(QuestionType):
    """Take the model to a lost walker, the far side of the world, and a shadow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ROTATION_SCENARIOS,
            hint="ถามว่าอะไรกำลังหมุน และผู้สังเกตหันเข้าหาแสงหรือหันออกจากแสง",
        ), SKY_TOPIC)
