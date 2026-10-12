"""ธรณีพิบัติภัยบนผิวโลก

ธรณีวิทยา · ม.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.2/10

Sets moved here from: science_wave_c22.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b8 import LEVEL as MIDDLE_TWO
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c22 import SURFACE_HAZARD_SCENARIOS, _matching_item

PROVENANCE = Provenance("original")


SURFACE_HAZARD_TOPIC = "ธรณีพิบัติภัยบนผิวโลก"


class SurfaceHazard(NamedTuple):
    """A hazard, and a description carrying its model, its process and its effect."""
    name: str
    description: str
    process: str


SURFACE_HAZARDS = (
    SurfaceHazard("น้ำท่วม",
                  "แบบจำลองรดน้ำปริมาณมากลงบนพื้นที่ลาดสู่ร่องน้ำจนน้ำล้นตลิ่ง แสดงว่าน้ำฝนที่ไหลลงมาเกินกว่าทางน้ำจะรับได้จึงเอ่อล้นท่วมพื้นที่ ผลกระทบคือบ้านเรือนและพื้นที่เกษตรเสียหาย",
                  "น้ำฝนที่ไหลลงมาเกินกว่าทางน้ำจะรับได้จึงเอ่อล้นท่วมพื้นที่"),
    SurfaceHazard("การกัดเซาะชายฝั่ง",
                  "แบบจำลองโยกถาดน้ำให้เกิดคลื่นซัดกองทรายริมถาดซ้ำ ๆ แสดงว่าคลื่นและกระแสน้ำพัดพาตะกอนชายฝั่งออกไป ผลกระทบคือแนวชายฝั่งร่นถอยและสิ่งปลูกสร้างริมทะเลพัง",
                  "คลื่นและกระแสน้ำพัดพาตะกอนชายฝั่งออกไป"),
    SurfaceHazard("ดินถล่ม",
                  "แบบจำลองรดน้ำบนกองดินลาดชันที่ไม่มีพืชคลุมจนดินอิ่มน้ำแล้วไถลลงมา แสดงว่าดินที่อุ้มน้ำจนหนักเคลื่อนที่ลงตามแรงโน้มถ่วง ผลกระทบคือบ้านเรือนถูกทับและเส้นทางถูกตัดขาด",
                  "ดินที่อุ้มน้ำจนหนักเคลื่อนที่ลงตามแรงโน้มถ่วง"),
    SurfaceHazard("หลุมยุบ",
                  "แบบจำลองวางน้ำตาลก้อนไว้ใต้ทรายแล้วรดน้ำจนน้ำตาลละลาย ทรายด้านบนยุบลงเป็นหลุม แสดงว่าน้ำใต้ดินละลายหินปูนจนเกิดโพรงแล้วเพดานโพรงถล่ม ผลกระทบคือพื้นดินยุบเป็นหลุมอย่างฉับพลัน",
                  "น้ำใต้ดินละลายหินปูนจนเกิดโพรงแล้วเพดานโพรงถล่ม"),
    SurfaceHazard("แผ่นดินทรุด",
                  "แบบจำลองบีบฟองน้ำที่อิ่มน้ำใต้ชั้นทรายให้น้ำไหลออก ผิวทรายค่อย ๆ ต่ำลงทั่วบริเวณ แสดงว่าการสูบน้ำใต้ดินมากเกินไปทำให้ชั้นดินอัดตัว ผลกระทบคือพื้นที่ต่ำลงช้า ๆ น้ำท่วมขังง่าย และอาคารร้าว",
                  "การสูบน้ำใต้ดินมากเกินไปทำให้ชั้นดินอัดตัว"),
)


@question_type(
    "geo.surface_hazard_foundation",
    display_name={"th": "กระบวนการเกิดธรณีพิบัติภัยบนผิวโลก"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=SURFACE_HAZARD_TOPIC,
)
class SurfaceHazardFoundation(QuestionType):
    """One hazard's process at a time, in either direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hazard = rng.choice(SURFACE_HAZARDS)
        others = [other for other in SURFACE_HAZARDS if other.name != hazard.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"{hazard.name}เกิดจากกระบวนการใด",
                correct=hazard.process,
                wrongs=tuple(other.process for other in others[:3]),
                hint="นึกว่าภัยนั้นเกี่ยวกับน้ำผิวดิน คลื่น ความลาดชัน โพรงหินปูน หรือน้ำใต้ดิน",
                topic=SURFACE_HAZARD_TOPIC,
            )
        return _labelled(
            stem=f"ภัยที่เกิดจาก{hazard.process} คือภัยใด",
            correct=hazard.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="นึกว่าภัยนั้นเกี่ยวกับน้ำผิวดิน คลื่น ความลาดชัน โพรงหินปูน หรือน้ำใต้ดิน",
            topic=SURFACE_HAZARD_TOPIC,
        )


@question_type(
    "geo.surface_hazard_fluency",
    display_name={"th": "อธิบายการเกิดและผลกระทบของธรณีพิบัติภัยจากแบบจำลอง"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=SURFACE_HAZARD_TOPIC,
)
class SurfaceHazardFluency(QuestionType):
    """Place all five hazards against their models; each wrong choice swaps two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _matching_item(
            rng, [h.name for h in SURFACE_HAZARDS], [h.description for h in SURFACE_HAZARDS],
            intro="แบบจำลองและคำอธิบายธรณีพิบัติภัย 5 ชนิด",
            question="ข้อใดจับคู่น้ำท่วม การกัดเซาะชายฝั่ง ดินถล่ม หลุมยุบ และแผ่นดินทรุด กับคำอธิบายได้ถูกต้องทั้งหมด",
            hint="จับคู่จากสิ่งที่แบบจำลองทำ: รดน้ำ โยกคลื่น ดินลาดชัน ละลายโพรง หรือบีบน้ำออก",
            topic=SURFACE_HAZARD_TOPIC,
        )


@question_type(
    "geo.surface_hazard_application",
    display_name={"th": "วิเคราะห์ความเสี่ยงและการจัดการธรณีพิบัติภัย"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=SURFACE_HAZARD_TOPIC,
)
class SurfaceHazardApplication(QuestionType):
    """Where sinkholes form, why Bangkok limits groundwater, and a sea wall's side effect."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SURFACE_HAZARD_SCENARIOS,
            hint="ย้อนหาว่าภัยนั้นเกิดจากกระบวนการใด แล้วนึกว่าอะไรทำให้กระบวนการนั้นรุนแรงขึ้น",
        ), SURFACE_HAZARD_TOPIC)
