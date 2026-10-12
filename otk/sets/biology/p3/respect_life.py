"""การไม่รบกวนวัฏจักรชีวิตของสัตว์

ชีวะ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.3/4

Sets moved here from: science_wave_b16.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import (
    SUBJECT,
    Care,
    Need,
    care_fluency,
    care_foundation,
    scenario_question,
)
from otk.sets._support.science_wave_b15 import ANIMAL_TOPIC, _retopic
from otk.sets._support.science_wave_b16 import PRIMARY_THREE, RESPECT_SCENARIOS

PROVENANCE = Provenance("original")


RESPECT_CARE = (
    Care("ไม่จับลูกอ๊อดหรือลูกสัตว์ออกจากแหล่งน้ำมาเลี้ยงเล่น",
         "ลูกสัตว์ที่ถูกนำออกจากที่อยู่เดิมมักโตไม่ได้จนเต็มวัย "
         "วัฏจักรชีวิตของมันจึงขาดตอนลง"),
    Care("ไม่ทำลายรังนกหรือเก็บไข่นกออกจากรัง",
         "ไข่ที่ถูกนำออกจากรังจะไม่ฟักเป็นตัว วัฏจักรชีวิตของนกจึงหยุดลงตั้งแต่ระยะไข่"),
    Care("ไม่ทิ้งขยะลงในแหล่งน้ำที่สัตว์อาศัยอยู่",
         "ขยะทำให้น้ำสกปรกจนไข่และตัวอ่อนของสัตว์น้ำเจริญเติบโตต่อไปไม่ได้"),
    Care("ไม่จับผีเสื้อหรือแมลงมาเสียบไว้เล่น",
         "แมลงที่ถูกจับจะตายก่อนที่จะวางไข่ในรุ่นถัดไป วัฏจักรชีวิตจึงไม่ดำเนินต่อ"),
    Care("ไม่ปล่อยสัตว์เลี้ยงไปอยู่ในธรรมชาติตามใจชอบ",
         "สัตว์เลี้ยงที่ถูกปล่อยอาจอยู่ไม่รอด หรือไปรบกวนวัฏจักรชีวิตของสัตว์อื่น"
         "ในที่นั้น"),
    Care("ช่วยกันดูแลแหล่งน้ำและต้นไม้ที่เป็นที่อยู่ของสัตว์",
         "สัตว์ต้องใช้ที่อยู่เดิมในการวางไข่และเลี้ยงลูก ถ้าที่อยู่หายไป "
         "วัฏจักรชีวิตก็ดำเนินต่อไม่ได้"),
)


RESPECT_NEEDS = (
    Need("เพื่อนชวนนักเรียนช้อนลูกอ๊อดจากบ่อมาใส่ขวดไว้ดูเล่นที่บ้าน ควรทำอย่างไร",
         "ไม่จับลูกอ๊อดหรือลูกสัตว์ออกจากแหล่งน้ำมาเลี้ยงเล่น"),
    Need("นักเรียนเห็นรังนกที่มีไข่อยู่บนต้นไม้หน้าบ้าน และอยากเอาไข่มาดูใกล้ ๆ "
         "ควรทำอย่างไร",
         "ไม่ทำลายรังนกหรือเก็บไข่นกออกจากรัง"),
    Need("นักเรียนกินขนมเสร็จตอนไปเที่ยวริมคลองและไม่เห็นถังขยะอยู่ใกล้ ๆ "
         "ควรทำอย่างไร",
         "ไม่ทิ้งขยะลงในแหล่งน้ำที่สัตว์อาศัยอยู่"),
    Need("เพื่อนชวนนักเรียนจับผีเสื้อมาปักไว้บนกระดาษเพื่อทำผลงานส่งครู ควรทำอย่างไร",
         "ไม่จับผีเสื้อหรือแมลงมาเสียบไว้เล่น"),
    Need("นักเรียนเลี้ยงเต่าญี่ปุ่นไว้แล้วเบื่อ จึงคิดจะนำไปปล่อยที่บึงใกล้บ้าน "
         "ควรทำอย่างไร",
         "ไม่ปล่อยสัตว์เลี้ยงไปอยู่ในธรรมชาติตามใจชอบ"),
    Need("สระน้ำในโรงเรียนที่มีกบและปลาอาศัยอยู่เริ่มตื้นเขินและมีเศษใบไม้ทับถม "
         "ควรทำอย่างไร",
         "ช่วยกันดูแลแหล่งน้ำและต้นไม้ที่เป็นที่อยู่ของสัตว์"),
)


@question_type(
    "animal.respect_life_foundation",
    display_name={"th": "เหตุผลของการไม่รบกวนวัฏจักรชีวิตของสัตว์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class RespectLifeFoundation(QuestionType):
    """Why leaving an animal alone keeps its cycle going."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_foundation(
            rng, system="วัฏจักรชีวิตของสัตว์", cares=RESPECT_CARE,
            hint="นึกว่าถ้าทำแบบนั้น สัตว์จะข้ามระยะใดในวัฏจักรชีวิตไปไม่ได้",
        ), ANIMAL_TOPIC)


@question_type(
    "animal.respect_life_fluency",
    display_name={"th": "เลือกการปฏิบัติที่ไม่รบกวนวัฏจักรชีวิตของสัตว์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class RespectLifeFluency(QuestionType):
    """Pick what the situation calls for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_fluency(
            rng, needs=RESPECT_NEEDS, cares=RESPECT_CARE,
            hint="ดูว่าการกระทำในสถานการณ์นี้จะไปหยุดวัฏจักรชีวิตของสัตว์ที่ระยะใด",
        ), ANIMAL_TOPIC)


@question_type(
    "animal.respect_life_application",
    display_name={"th": "วิเคราะห์ผลของการรบกวนวัฏจักรชีวิตของสัตว์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class RespectLifeApplication(QuestionType):
    """Follow one act of interference through to the next generation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, RESPECT_SCENARIOS,
            hint="ตามต่อไปอีกขั้นว่าสัตว์ตัวนั้นจะได้โตไปวางไข่หรือมีลูกในรุ่นถัดไป"
                 "หรือไม่",
        ), ANIMAL_TOPIC)
