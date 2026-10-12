"""ระบบย่อยอาหาร

ชีวะ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.6/4

Sets moved here from: science_wave_b18.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import BODY_TOPIC, PRIMARY_SIX, _body
from otk.sets._support.science_wave_b18 import DIGESTION_SCENARIOS

PROVENANCE = Provenance("original")


class Organ(NamedTuple):
    """One organ of the digestive system and what it does."""
    name: str
    function: str


DIGESTIVE_ORGANS = (
    Organ("ปาก", "บดเคี้ยวอาหารให้เล็กลงด้วยฟัน และมีน้ำลายช่วยย่อยแป้ง"),
    Organ("หลอดอาหาร", "บีบตัวเป็นจังหวะเพื่อส่งอาหารลงสู่กระเพาะอาหาร"),
    Organ("กระเพาะอาหาร", "คลุกเคล้าอาหารกับน้ำย่อยที่ย่อยโปรตีน"),
    Organ("ลำไส้เล็ก",
          "ย่อยอาหารจนมีขนาดเล็กที่สุด และดูดซึมสารอาหารเข้าสู่กระแสเลือด"),
    Organ("ลำไส้ใหญ่", "ดูดน้ำกลับคืนสู่ร่างกาย และเก็บกากอาหารไว้ก่อนขับออก"),
    Organ("ตับ", "สร้างน้ำดีที่ช่วยให้ไขมันแตกตัวเป็นหยดเล็ก ๆ ก่อนถูกย่อย"),
)


# The route food takes. ตับ is not on it — it helps from the side, which is why
# it is in the organ table but not in the path.
FOOD_PATH = ("ปาก", "หลอดอาหาร", "กระเพาะอาหาร", "ลำไส้เล็ก", "ลำไส้ใหญ่",
             "ทวารหนัก")


class Fact(NamedTuple):
    """One question about digestion or absorption, and its single answer."""
    question: str
    answer: str


DIGESTION_FACTS = (
    Fact("การย่อยอาหารหมายถึงอะไร",
         "การทำให้อาหารมีขนาดเล็กลงจนร่างกายดูดซึมเข้าสู่เลือดได้"),
    Fact("การดูดซึมสารอาหารเกิดขึ้นที่ใดเป็นหลัก",
         "ที่ลำไส้เล็ก ซึ่งมีผนังด้านในเป็นขนเล็ก ๆ จำนวนมากเพื่อเพิ่มพื้นที่ดูดซึม"),
    Fact("เหตุใดจึงต้องเคี้ยวอาหารให้ละเอียดก่อนกลืน",
         "อาหารชิ้นเล็กมีพื้นที่ให้น้ำย่อยทำงานได้มากกว่า การย่อยจึงเร็วและสมบูรณ์ขึ้น"),
    Fact("สารอาหารที่ถูกดูดซึมแล้วไปที่ใดต่อ",
         "เข้าสู่กระแสเลือด แล้วถูกลำเลียงไปเลี้ยงเซลล์ทั่วร่างกาย"),
    Fact("กากอาหารที่เหลือจากการดูดซึมจะเป็นอย่างไรต่อไป",
         "ถูกส่งต่อไปยังลำไส้ใหญ่ ซึ่งดูดน้ำกลับคืน แล้วจึงขับออกทางทวารหนัก"),
    Fact("น้ำย่อยมีบทบาทอย่างไรในการย่อยอาหาร",
         "ช่วยย่อยอาหารแต่ละประเภทให้เล็กลง โดยน้ำย่อยแต่ละชนิดย่อยอาหารคนละอย่าง"),
)


@question_type(
    "body.digestive_organs_foundation",
    display_name={"th": "อวัยวะในระบบย่อยอาหารและหน้าที่"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class DigestiveOrgansFoundation(QuestionType):
    """Name an organ's job, or the organ that does a job.

    This is the ``บรรยายหน้าที่ของอวัยวะในระบบย่อยอาหาร`` part of ``ป.6/4``, which
    stands free of the model requirement.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DIGESTIVE_ORGANS)
        others = [other for other in DIGESTIVE_ORGANS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _body(
                stem=f"“{item.name}” ทำหน้าที่ใดในระบบย่อยอาหาร",
                correct=item.function,
                wrongs=tuple(other.function for other in others[:3]),
                hint="แยกว่าอวัยวะนั้นบดเคี้ยว เป็นทางผ่าน ย่อย ดูดซึม หรือดูดน้ำกลับ",
            )
        return _body(
            stem=f"อวัยวะใดในระบบย่อยอาหารทำหน้าที่{item.function}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกอวัยวะที่ทำหน้าที่นั้นโดยตรง",
        )


@question_type(
    "body.digestion_fluency",
    display_name={"th": "การย่อยอาหารและการดูดซึมสารอาหาร"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class DigestionFluency(QuestionType):
    """Follow the food along, and say how digestion and absorption work.

    This is the ``รวมทั้งอธิบายการย่อยอาหารและการดูดซึมสารอาหาร`` part of
    ``ป.6/4``, which also stands free of the model requirement.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            index = rng.randrange(len(FOOD_PATH) - 1)
            current, following = FOOD_PATH[index], FOOD_PATH[index + 1]
            others = [name for name in FOOD_PATH if name != following]
            rng.shuffle(others)
            return _body(
                stem=f"อาหารที่ผ่าน “{current}” แล้วจะผ่านอวัยวะใดต่อไป",
                correct=following,
                wrongs=tuple(others[:3]),
                hint="ไล่จากที่ที่อาหารเข้าสู่ร่างกาย ไปจนถึงที่ที่กากอาหารออกไป",
            )
        item = rng.choice(DIGESTION_FACTS)
        others = [other.answer for other in DIGESTION_FACTS
                  if other.answer != item.answer]
        rng.shuffle(others)
        return _body(
            stem=item.question, correct=item.answer, wrongs=tuple(others[:3]),
            hint="แยกให้ชัดระหว่างการย่อย ซึ่งทำให้อาหารเล็กลง "
                 "กับการดูดซึม ซึ่งพาสารอาหารเข้าสู่เลือด",
        )


@question_type(
    "body.digestion_application",
    display_name={"th": "ตีความแบบจำลองและการทำงานของระบบย่อยอาหาร"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class DigestionApplication(QuestionType):
    """Read a model of the gut, then follow food through real cases."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, DIGESTION_SCENARIOS,
            hint="ระบุก่อนว่าเรื่องนี้เกี่ยวกับการทำให้อาหารเล็กลง การดูดซึม "
                 "หรือการดูดน้ำกลับ",
        ), BODY_TOPIC)
