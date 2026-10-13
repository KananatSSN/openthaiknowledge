"""การดูแลรักษาระบบย่อยอาหาร

ชีวะ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.6/5

Sets moved here from: science_wave_b18.
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
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import BODY_TOPIC, PRIMARY_SIX
from otk.sets._support.science_wave_b18 import DIGESTIVE_CARE_SCENARIOS

PROVENANCE = Provenance("original")


DIGESTIVE_CARE = (
    Care("เคี้ยวอาหารให้ละเอียดก่อนกลืน",
         "อาหารชิ้นเล็กมีพื้นที่ให้น้ำย่อยทำงานมากกว่า กระเพาะอาหารจึงไม่ต้องทำงานหนัก"
         "และย่อยได้สมบูรณ์ขึ้น"),
    Care("กินอาหารให้ตรงเวลาทุกมื้อ",
         "ร่างกายหลั่งน้ำย่อยตามเวลาที่เคยชิน ถ้าไม่มีอาหารมาให้ย่อย "
         "น้ำย่อยจะกัดผนังกระเพาะอาหารจนเกิดแผลได้"),
    Care("เลี่ยงอาหารรสจัดและของหมักดองที่มากเกินไป",
         "อาหารรสจัดระคายเคืองผนังกระเพาะอาหารและลำไส้ ทำให้อักเสบได้ง่าย"),
    Care("กินผักผลไม้และดื่มน้ำให้พอ",
         "กากใยจากผักผลไม้และน้ำที่พอเพียงทำให้กากอาหารไม่แข็ง ลำไส้ใหญ่จึงขับออก"
         "ได้ตามปกติ"),
    Care("ไม่กลั้นอุจจาระเป็นประจำ",
         "กากอาหารที่ค้างอยู่ในลำไส้ใหญ่นานจะถูกดูดน้ำกลับไปมากจนแข็งและถ่ายลำบาก"),
    Care("ล้างมือก่อนรับประทานอาหารและกินอาหารที่ปรุงสุกสะอาด",
         "เชื้อโรคที่เข้าสู่ทางเดินอาหารทำให้ท้องเสียและลำไส้อักเสบ"),
)


DIGESTIVE_NEEDS = (
    Need("นักเรียนรีบกินข้าวให้ทันเข้าเรียนจนกลืนเป็นคำโต ๆ แล้วแน่นท้องทุกครั้ง "
         "ควรปฏิบัติตามแนวทางใด",
         "เคี้ยวอาหารให้ละเอียดก่อนกลืน"),
    Need("นักเรียนมักงดมื้อกลางวันแล้วไปกินรวดเดียวตอนเย็น จนเริ่มปวดแสบท้อง "
         "ควรปฏิบัติตามแนวทางใด",
         "กินอาหารให้ตรงเวลาทุกมื้อ"),
    Need("นักเรียนกินส้มตำเผ็ดจัดและของหมักดองแทบทุกวันจนแสบท้องบ่อย ๆ "
         "ควรปฏิบัติตามแนวทางใด",
         "เลี่ยงอาหารรสจัดและของหมักดองที่มากเกินไป"),
    Need("นักเรียนถ่ายอุจจาระแข็งและลำบากมาหลายวัน โดยกินแต่เนื้อสัตว์กับข้าว "
         "ควรปฏิบัติตามแนวทางใด",
         "กินผักผลไม้และดื่มน้ำให้พอ"),
    Need("นักเรียนไม่ชอบเข้าห้องน้ำที่โรงเรียนจึงอั้นไว้จนกลับถึงบ้านทุกวัน "
         "ควรปฏิบัติตามแนวทางใด",
         "ไม่กลั้นอุจจาระเป็นประจำ"),
    Need("นักเรียนหยิบขนมกินทันทีหลังเล่นกีฬาโดยไม่ได้ล้างมือ แล้วท้องเสียบ่อย "
         "ควรปฏิบัติตามแนวทางใด",
         "ล้างมือก่อนรับประทานอาหารและกินอาหารที่ปรุงสุกสะอาด"),
)


@question_type(
    "body.digestive_care_foundation",
    display_name={"th": "เหตุผลของแนวทางดูแลระบบย่อยอาหาร"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class DigestiveCareFoundation(QuestionType):
    """Why a habit keeps the gut working."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_foundation(
            rng, system="ระบบย่อยอาหาร", cares=DIGESTIVE_CARE,
            hint="โยงแนวทางกลับไปที่ผนังกระเพาะอาหาร การย่อย หรือการขับกากอาหาร",
        ), BODY_TOPIC)


@question_type(
    "body.digestive_care_fluency",
    display_name={"th": "เลือกแนวทางดูแลระบบย่อยอาหารให้ตรงกับสถานการณ์"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class DigestiveCareFluency(QuestionType):
    """State the แนวทาง the situation calls for — ``ป.6/5``'s own evidence."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_fluency(
            rng, needs=DIGESTIVE_NEEDS, cares=DIGESTIVE_CARE,
            hint="ระบุปัญหาก่อนว่าเป็นเรื่องการเคี้ยว เวลาอาหาร การระคายเคือง "
                 "การขับถ่าย หรือความสะอาด",
        ), BODY_TOPIC)


@question_type(
    "body.digestive_care_application",
    display_name={"th": "วิเคราะห์พฤติกรรมที่มีผลต่อระบบย่อยอาหาร"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class DigestiveCareApplication(QuestionType):
    """Explain why a habit changes how the gut works."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, DIGESTIVE_CARE_SCENARIOS,
            hint="อธิบายด้วยกลไกจริง เช่น น้ำย่อย พื้นที่ให้น้ำย่อยทำงาน "
                 "หรือการดูดน้ำกลับที่ลำไส้ใหญ่",
        ), BODY_TOPIC)


# More practices, each with its own reason and the one situation it answers,
# so every practice still answers exactly one situation.
DIGESTIVE_CARE += (
    Care('ไม่ออกกำลังกายหนักทันทีหลังกินอาหารอิ่ม',
         'หลังกินอาหาร ระบบย่อยอาหารกำลังทำงาน การออกแรงหนักทันทีทำให้ย่อยได้ไม่ดีและจุกเสียด'),
)
DIGESTIVE_NEEDS += (
    Need('นักเรียนกินข้าวกลางวันจนอิ่มแล้ววิ่งเล่นฟุตบอลทันที จึงจุกเสียดท้องบ่อย ควรปฏิบัติตามแนวทางใด',
         'ไม่ออกกำลังกายหนักทันทีหลังกินอาหารอิ่ม'),
)
