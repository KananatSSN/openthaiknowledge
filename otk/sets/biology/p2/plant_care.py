"""การดูแลพืชให้ได้รับน้ำและแสง

ชีวะ · ป.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.2/2

Sets moved here from: science_wave_b15.
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
from otk.sets._support.science_wave_b14 import PLANT_TOPIC
from otk.sets._support.science_wave_b15 import PLANT_CARE_SCENARIOS, PRIMARY_TWO, _retopic

PROVENANCE = Provenance("original")


PLANT_CARE = (
    Care("รดน้ำต้นไม้ให้ดินชุ่มแต่ไม่ให้น้ำท่วมขัง",
         "พืชต้องการน้ำ แต่ถ้าน้ำขังอยู่ตลอดเวลา รากจะเน่าจนดูดน้ำไม่ได้"),
    Care("วางกระถางไว้ในที่ที่มีแสงส่องถึง",
         "พืชใช้แสงสร้างอาหารที่ใบ ถ้าอยู่ในที่มืดก็สร้างอาหารไม่ได้และจะอ่อนแอลง"),
    Care("หมั่นสังเกตใบและดินว่าแห้งหรือไม่",
         "ใบที่เริ่มเหี่ยวและดินที่แห้งเป็นสัญญาณว่าพืชกำลังขาดน้ำ "
         "จะได้รดน้ำให้ทันก่อนต้นไม้เสียหาย"),
    Care("ย้ายกระถางออกจากที่ที่แดดแรงจัดตลอดทั้งวัน",
         "แดดที่แรงเกินไปทำให้น้ำในดินระเหยไปเร็วมากและทำให้ใบไหม้"),
    Care("ถอนวัชพืชที่ขึ้นแย่งอยู่ในกระถางออก",
         "วัชพืชแย่งทั้งน้ำในดินและแสงไปจากต้นไม้ที่เราปลูกไว้"),
    Care("ไม่วางสิ่งของบังแสงหรือทับต้นไม้เล็กไว้",
         "ต้นไม้ที่ถูกบังจะได้รับแสงไม่พอ จึงเจริญเติบโตช้ากว่าที่ควรจะเป็น"),
)


PLANT_CARE_NEEDS = (
    Need("นักเรียนรดน้ำต้นไม้จนน้ำขังเต็มจานรองทุกวัน แล้วใบเริ่มเหลืองและรากเน่า "
         "ควรทำอย่างไร",
         "รดน้ำต้นไม้ให้ดินชุ่มแต่ไม่ให้น้ำท่วมขัง"),
    Need("นักเรียนวางกระถางต้นไม้ไว้ใต้โต๊ะในมุมห้องที่แสงส่องไม่ถึง ควรทำอย่างไร",
         "วางกระถางไว้ในที่ที่มีแสงส่องถึง"),
    Need("นักเรียนไม่แน่ใจว่าวันนี้ต้องรดน้ำต้นไม้หรือยัง ควรทำอย่างไรก่อนตัดสินใจ",
         "หมั่นสังเกตใบและดินว่าแห้งหรือไม่"),
    Need("กระถางของนักเรียนวางอยู่กลางแดดจัดทั้งวันจนดินแห้งเร็วมากและปลายใบไหม้ "
         "ควรทำอย่างไร",
         "ย้ายกระถางออกจากที่ที่แดดแรงจัดตลอดทั้งวัน"),
    Need("ในกระถางของนักเรียนมีหญ้าขึ้นเต็มไปหมดจนต้นไม้ที่ปลูกไว้โตช้า ควรทำอย่างไร",
         "ถอนวัชพืชที่ขึ้นแย่งอยู่ในกระถางออก"),
    Need("นักเรียนวางกล่องใบใหญ่ไว้ข้างกระถางจนบังแสงต้นไม้ไว้ครึ่งวัน ควรทำอย่างไร",
         "ไม่วางสิ่งของบังแสงหรือทับต้นไม้เล็กไว้"),
)


@question_type(
    "plant.plant_care_foundation",
    display_name={"th": "เหตุผลของการดูแลพืชให้ได้รับน้ำและแสง"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantCareFoundation(QuestionType):
    """Why each way of looking after a plant helps it grow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_foundation(
            rng, system="ต้นไม้ที่เราปลูก", cares=PLANT_CARE,
            hint="นึกว่าการทำแบบนั้นทำให้ต้นไม้ได้รับน้ำหรือแสงมากขึ้นหรือน้อยลง",
        ), PLANT_TOPIC)


@question_type(
    "plant.plant_care_fluency",
    display_name={"th": "เลือกวิธีดูแลพืชให้ตรงกับปัญหา"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantCareFluency(QuestionType):
    """Pick the way of looking after a plant the situation calls for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_fluency(
            rng, needs=PLANT_CARE_NEEDS, cares=PLANT_CARE,
            hint="ดูก่อนว่าต้นไม้ในสถานการณ์นี้ขาดน้ำ ได้น้ำมากไป หรือขาดแสง",
        ), PLANT_TOPIC)


@question_type(
    "plant.plant_care_application",
    display_name={"th": "วิเคราะห์การดูแลพืชในชีวิตประจำวัน"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantCareApplication(QuestionType):
    """Explain what happened to a plant, or judge a plan for looking after one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, PLANT_CARE_SCENARIOS,
            hint="ถามว่าต้นไม้ต้นนั้นได้รับน้ำและแสงพอเหมาะหรือไม่ "
                 "และมีอะไรมาแย่งไปหรือเปล่า",
        ), PLANT_TOPIC)


# More practices, each with its own reason and the one situation it answers,
# so every practice still answers exactly one situation.
PLANT_CARE += (
    Care('เช็ดฝุ่นที่เกาะบนใบออกเป็นครั้งคราว',
         'ฝุ่นที่เกาะหนาบังแสงไม่ให้ถึงใบ ใบจึงสร้างอาหารได้น้อยลง'),
)
PLANT_CARE_NEEDS += (
    Need('ต้นไม้ที่วางไว้ในห้องมีฝุ่นเกาะหนาจนใบเป็นสีเทา ควรทำอย่างไร',
         'เช็ดฝุ่นที่เกาะบนใบออกเป็นครั้งคราว'),
)
