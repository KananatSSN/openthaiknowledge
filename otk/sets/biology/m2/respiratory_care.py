"""การดูแลรักษาระบบหายใจ

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/3

Sets moved here from: science_wave_b9.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import (
    LEVEL,
    RESPIRATORY_CARE_SCENARIOS,
    SUBJECT,
    TOPIC,
    Care,
    Need,
    care_fluency,
    care_foundation,
    scenario_question,
)

PROVENANCE = Provenance("original")


RESPIRATORY_CARE = (
    Care("ไม่สูบบุหรี่และหลีกเลี่ยงควันบุหรี่มือสอง",
         "ควันบุหรี่ทำลายขนกวัดและผนังถุงลม ทางเดินหายใจจึงกำจัดสิ่งแปลกปลอมได้น้อยลง "
         "และพื้นที่แลกเปลี่ยนแก๊สลดลงอย่างถาวร"),
    Care("สวมหน้ากากที่กรองอนุภาคขนาดเล็กเมื่ออยู่ในที่ที่มีฝุ่นละอองมาก",
         "ฝุ่นที่มีขนาดเล็กมากผ่านขนจมูกและเมือกเข้าไปถึงถุงลมได้ "
         "การกรองก่อนหายใจเข้าจึงลดปริมาณฝุ่นที่ไปถึงถุงลม"),
    Care("ออกกำลังกายอย่างสม่ำเสมอ",
         "กะบังลมและกล้ามเนื้อระหว่างซี่โครงแข็งแรงขึ้น ช่องอกจึงเปลี่ยนปริมาตรได้เต็มที่ "
         "และปอดรับอากาศได้มากขึ้นในการหายใจแต่ละครั้ง"),
    Care("ฉีดวัคซีนป้องกันโรคของระบบทางเดินหายใจตามกำหนด",
         "ลดโอกาสติดเชื้อที่ทำให้หลอดลมและถุงลมอักเสบ "
         "ซึ่งการอักเสบซ้ำ ๆ จะทำให้เนื้อปอดเสียหายสะสม"),
    Care("หายใจเข้าทางจมูกแทนการอ้าปากหายใจ",
         "จมูกกรองฝุ่นด้วยขนจมูกและเมือก อีกทั้งปรับอุณหภูมิและความชื้นของอากาศ "
         "ก่อนที่อากาศจะลงไปถึงปอด"),
    Care("พักผ่อนและดื่มน้ำให้เพียงพอเมื่อเป็นหวัด",
         "น้ำที่เพียงพอทำให้เมือกในทางเดินหายใจไม่เหนียวข้น "
         "ขนกวัดจึงพัดเมือกที่ดักเชื้อโรคไว้ออกมาได้ตามปกติ"),
)


RESPIRATORY_NEEDS = (
    Need("นักเรียนต้องเดินทางผ่านบริเวณที่มีค่าฝุ่นละอองขนาดเล็กสูงเป็นประจำทุกวัน "
         "ควรปฏิบัติตามแนวทางใดจึงจะดูแลระบบหายใจได้ตรงกับปัญหา",
         "สวมหน้ากากที่กรองอนุภาคขนาดเล็กเมื่ออยู่ในที่ที่มีฝุ่นละอองมาก"),
    Need("ในบ้านของนักเรียนมีผู้สูบบุหรี่เป็นประจำ และน้องเล็กไอเรื้อรังมาหลายเดือน "
         "แนวทางใดช่วยรักษาระบบหายใจของทุกคนในบ้านได้ตรงที่สุด",
         "ไม่สูบบุหรี่และหลีกเลี่ยงควันบุหรี่มือสอง"),
    Need("นักเรียนเหนื่อยหอบเมื่อขึ้นบันไดเพียงสองชั้น และต้องการให้กล้ามเนื้อที่ใช้ในการ"
         "หายใจแข็งแรงขึ้น ควรปฏิบัติตามแนวทางใด",
         "ออกกำลังกายอย่างสม่ำเสมอ"),
    Need("ก่อนถึงฤดูที่มีการระบาดของโรคติดเชื้อในระบบทางเดินหายใจ "
         "แนวทางใดช่วยลดโอกาสที่ปอดจะอักเสบซ้ำ ๆ ได้ล่วงหน้า",
         "ฉีดวัคซีนป้องกันโรคของระบบทางเดินหายใจตามกำหนด"),
    Need("นักเรียนเป็นหวัดและมีเสมหะเหนียวข้นจนไอออกได้ยาก ควรปฏิบัติตามแนวทางใด",
         "พักผ่อนและดื่มน้ำให้เพียงพอเมื่อเป็นหวัด"),
    Need("นักเรียนมักอ้าปากหายใจขณะวิ่งในสนามที่มีฝุ่นฟุ้ง และมักเจ็บคอหลังเลิกซ้อม "
         "ควรปรับพฤติกรรมตามแนวทางใด",
         "หายใจเข้าทางจมูกแทนการอ้าปากหายใจ"),
)


@question_type(
    "body.respiratory_care_foundation",
    display_name={"th": "เหตุผลของแนวทางดูแลระบบหายใจ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class RespiratoryCareFoundation(QuestionType):
    """Why a habit protects the respiratory organs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return care_foundation(
            rng, system="ระบบหายใจ", cares=RESPIRATORY_CARE,
            hint="โยงแนวทางกลับไปที่อวัยวะที่มันปกป้อง เช่น ขนกวัด ผนังถุงลม "
                 "หรือกล้ามเนื้อที่ใช้หายใจ",
        )


@question_type(
    "body.respiratory_care_fluency",
    display_name={"th": "เลือกแนวทางดูแลระบบหายใจให้ตรงกับสถานการณ์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class RespiratoryCareFluency(QuestionType):
    """State the แนวทาง the situation calls for.

    ``ม.2/3`` names its own evidence: ``โดยการบอกแนวทางในการดูแลรักษาอวัยวะใน
    ระบบหายใจให้ทำงานเป็นปกติ``. Stating that แนวทาง is what this item asks for,
    so this is the one set in the topic filed ``exact``.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return care_fluency(
            rng, needs=RESPIRATORY_NEEDS, cares=RESPIRATORY_CARE,
            hint="ถามตัวเองว่าอวัยวะใดกำลังถูกคุกคามในสถานการณ์นี้ "
                 "แล้วเลือกแนวทางที่ปกป้องอวัยวะนั้นโดยตรง",
        )


@question_type(
    "body.respiratory_care_application",
    display_name={"th": "วิเคราะห์สถานการณ์ที่มีผลต่อระบบหายใจ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class RespiratoryCareApplication(QuestionType):
    """Explain why a habit or an exposure changes how the system works."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, RESPIRATORY_CARE_SCENARIOS,
            hint="อธิบายด้วยกลไกจริง เช่น ขนกวัด พื้นที่แลกเปลี่ยนแก๊ส "
                 "หรือความแตกต่างของความเข้มข้นแก๊ส ไม่ใช่ด้วยความรู้สึกว่าดีหรือไม่ดี",
        )
