"""อวัยวะในระบบหายใจ

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/1

Sets moved here from: science_wave_b8.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import contextual_scenario_question
from otk.sets._support.science_wave_b8 import (
    LEVEL,
    RESPIRATORY_SCENARIOS,
    SUBJECT,
    TOPIC,
    _labelled,
)

PROVENANCE = Provenance("original")


class Organ(NamedTuple):
    """One organ of the respiratory system and what it does."""
    name: str
    function: str


ORGANS = (
    Organ("จมูก", "กรองฝุ่นด้วยขนจมูก และปรับอุณหภูมิกับความชื้นของอากาศที่หายใจเข้า"),
    Organ("หลอดลม",
          "เป็นทางผ่านของอากาศลงสู่ปอด มีกระดูกอ่อนเป็นวงค้ำไว้ไม่ให้แฟบ"),
    Organ("หลอดลมฝอย", "แตกแขนงเล็กลงเรื่อย ๆ เพื่อนำอากาศไปยังถุงลมทั่วปอด"),
    Organ("ถุงลม", "เป็นบริเวณที่เกิดการแลกเปลี่ยนแก๊สระหว่างอากาศกับเลือด"),
    Organ("ปอด", "เป็นอวัยวะที่บรรจุถุงลมจำนวนมหาศาลไว้ภายใน"),
    Organ("กะบังลม",
          "เป็นกล้ามเนื้อที่หดและคลายตัวเพื่อเปลี่ยนปริมาตรของช่องอก"),
    Organ("กล้ามเนื้อยึดกระดูกซี่โครง",
          "ยกและลดกระดูกซี่โครงเพื่อช่วยเปลี่ยนปริมาตรของช่องอก"),
)


# The route air actually takes, in order. Stored once; the "what comes next"
# question reads it and nothing else does.
AIR_PATH = ("จมูก", "คอหอย", "กล่องเสียง", "หลอดลม", "หลอดลมฝอย", "ถุงลม")


@question_type(
    "body.respiratory_organs_foundation",
    display_name={"th": "อวัยวะในระบบหายใจและหน้าที่"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class RespiratoryOrgansFoundation(QuestionType):
    """Name an organ's job, or the organ that does a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ORGANS)
        others = [other for other in ORGANS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” ทำหน้าที่ใดในระบบหายใจ",
                correct=item.function,
                wrongs=tuple(other.function for other in others[:3]),
                hint="แยกก่อนว่าอวัยวะนั้นเป็นทางผ่านของอากาศ เป็นที่แลกเปลี่ยนแก๊ส "
                     "หรือเป็นกล้ามเนื้อที่ทำให้ช่องอกเปลี่ยนปริมาตร",
            )
        return _labelled(
            stem=f"อวัยวะใดในระบบหายใจทำหน้าที่{item.function}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกอวัยวะที่ทำหน้าที่นั้นโดยตรง",
        )


@question_type(
    "body.respiratory_path_fluency",
    display_name={"th": "เส้นทางของอากาศในระบบหายใจ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class RespiratoryPathFluency(QuestionType):
    """Follow the air from the nose to the alveoli.

    Naming organs is Foundation work. ``ม.2/1`` also asks how they are *related*,
    and the order of the route is the relation that matters: a learner who can
    name หลอดลมฝอย but puts it before หลอดลม has not got the system.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            index = rng.randrange(len(AIR_PATH) - 1)
            current, following = AIR_PATH[index], AIR_PATH[index + 1]
            others = [name for name in AIR_PATH if name != following]
            rng.shuffle(others)
            return _labelled(
                stem=f"อากาศที่หายใจเข้าไปผ่าน “{current}” แล้วจะผ่านอวัยวะใดต่อไป",
                correct=following,
                wrongs=tuple(others[:3]),
                hint="ไล่จากภายนอกเข้าสู่ภายใน จมูกอยู่นอกสุดและถุงลมอยู่ในสุด",
            )
        correct = " → ".join(AIR_PATH)
        reversed_path = " → ".join(reversed(AIR_PATH))
        swapped = list(AIR_PATH)
        swapped[3], swapped[4] = swapped[4], swapped[3]
        dropped = [name for name in AIR_PATH if name != "หลอดลม"]
        return _labelled(
            stem="ข้อใดเรียงลำดับเส้นทางของอากาศที่หายใจเข้าได้ถูกต้อง",
            correct=correct,
            wrongs=(reversed_path, " → ".join(swapped),
                    " → ".join(dropped + ["ปอด"])),
            hint="เริ่มจากอวัยวะที่อากาศสัมผัสก่อน แล้วไล่ลึกลงไปจนถึงที่แลกเปลี่ยนแก๊ส",
        )


@question_type(
    "body.respiratory_application",
    display_name={"th": "วิเคราะห์ความผิดปกติและการทำงานของระบบหายใจ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class RespiratoryApplication(QuestionType):
    """Explain a symptom or a habit by what the organ concerned actually does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, RESPIRATORY_SCENARIOS,
            hint="ระบุก่อนว่าเรื่องนี้เกี่ยวกับทางผ่านของอากาศ พื้นที่แลกเปลี่ยนแก๊ส "
                 "หรือกล้ามเนื้อที่ใช้หายใจ",
            topic=TOPIC,
        )
