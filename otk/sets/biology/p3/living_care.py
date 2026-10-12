"""การดูแลตนเองและสัตว์ให้ได้รับอาหาร น้ำ และอากาศ

ชีวะ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.3/2

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
from otk.sets._support.science_wave_b16 import LIVING_CARE_SCENARIOS, PRIMARY_THREE

PROVENANCE = Provenance("original")


LIVING_CARE = (
    Care("รับประทานอาหารให้ครบห้าหมู่และตรงเวลา",
         "ร่างกายได้รับสารอาหารครบตามที่ต้องการ จึงเจริญเติบโตและมีแรงทำกิจกรรมได้"),
    Care("ดื่มน้ำสะอาดให้เพียงพอในแต่ละวัน",
         "น้ำเป็นส่วนประกอบของร่างกายและช่วยให้ร่างกายทำงานได้ตามปกติ"),
    Care("เปลี่ยนน้ำในภาชนะเลี้ยงสัตว์ให้สะอาดอยู่เสมอ",
         "น้ำที่สกปรกมีเชื้อโรคปนอยู่ สัตว์ที่ดื่มเข้าไปจึงป่วยได้ง่าย"),
    Care("ให้อาหารสัตว์เลี้ยงในปริมาณและเวลาที่เหมาะสม",
         "สัตว์สร้างอาหารเองไม่ได้ ต้องได้รับอาหารจากภายนอกอย่างสม่ำเสมอ "
         "แต่ถ้ามากเกินไปก็ทำให้อ้วนและป่วยได้"),
    Care("วางกรงหรือที่อยู่ของสัตว์ไว้ในที่ที่อากาศถ่ายเทได้",
         "สัตว์ต้องหายใจเอาอากาศเข้าไปตลอดเวลา ที่อับจึงทำให้สัตว์อ่อนแอและตายได้"),
    Care("ไม่ทิ้งสัตว์เลี้ยงไว้ในรถหรือในที่ปิดที่ร้อนจัด",
         "ในที่ปิดที่ร้อนจัด อากาศถ่ายเทไม่ได้และอุณหภูมิสูงขึ้นเร็วมาก "
         "สัตว์จึงเป็นอันตรายถึงชีวิตได้ในเวลาไม่นาน"),
)


LIVING_CARE_NEEDS = (
    Need("นักเรียนกินแต่ขนมกรุบกรอบแทนข้าวมื้อกลางวันทุกวัน ควรทำอย่างไร",
         "รับประทานอาหารให้ครบห้าหมู่และตรงเวลา"),
    Need("นักเรียนวิ่งเล่นกลางแดดจนเหนื่อยและรู้สึกคอแห้ง ควรทำอย่างไร",
         "ดื่มน้ำสะอาดให้เพียงพอในแต่ละวัน"),
    Need("น้ำในถ้วยของสุนัขที่บ้านขุ่นและมีเศษอาหารลอยอยู่มาหลายวันแล้ว ควรทำอย่างไร",
         "เปลี่ยนน้ำในภาชนะเลี้ยงสัตว์ให้สะอาดอยู่เสมอ"),
    Need("นักเรียนลืมให้อาหารกระต่ายที่เลี้ยงไว้บ่อยครั้งจนมันผอมลง ควรทำอย่างไร",
         "ให้อาหารสัตว์เลี้ยงในปริมาณและเวลาที่เหมาะสม"),
    Need("นักเรียนวางกรงนกไว้ในตู้เก็บของที่ปิดมิดชิดเพื่อไม่ให้เสียงดัง ควรทำอย่างไร",
         "วางกรงหรือที่อยู่ของสัตว์ไว้ในที่ที่อากาศถ่ายเทได้"),
    Need("พ่อจอดรถแวะซื้อของและจะทิ้งสุนัขไว้ในรถที่ปิดกระจกกลางแดด ควรบอกอย่างไร",
         "ไม่ทิ้งสัตว์เลี้ยงไว้ในรถหรือในที่ปิดที่ร้อนจัด"),
)


@question_type(
    "life.living_care_foundation",
    display_name={"th": "เหตุผลของการดูแลตนเองและสัตว์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class LivingCareFoundation(QuestionType):
    """Why each way of looking after a person or an animal matters."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_foundation(
            rng, system="ตนเองและสัตว์", cares=LIVING_CARE,
            hint="นึกว่าการทำแบบนั้นทำให้ได้รับอาหาร น้ำ หรืออากาศดีขึ้นอย่างไร",
        ), ANIMAL_TOPIC)


@question_type(
    "life.living_care_fluency",
    display_name={"th": "เลือกวิธีดูแลตนเองและสัตว์ให้ตรงกับสถานการณ์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class LivingCareFluency(QuestionType):
    """Pick what the situation calls for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_fluency(
            rng, needs=LIVING_CARE_NEEDS, cares=LIVING_CARE,
            hint="ดูก่อนว่าในสถานการณ์นี้กำลังขาดอาหาร ขาดน้ำสะอาด หรือขาดอากาศ",
        ), ANIMAL_TOPIC)


@question_type(
    "life.living_care_application",
    display_name={"th": "วิเคราะห์การดูแลตนเองและสัตว์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class LivingCareApplication(QuestionType):
    """Judge a piece of everyday advice about food, water and air."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, LIVING_CARE_SCENARIOS,
            hint="ตรวจว่าคำแนะนำนั้นทำให้ได้รับอาหาร น้ำ และอากาศพอเหมาะจริงหรือไม่",
        ), ANIMAL_TOPIC)
