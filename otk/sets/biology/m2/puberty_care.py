"""การดูแลร่างกายและจิตใจในวัยหนุ่มสาว

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/14

Sets moved here from: science_wave_b12.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import (
    LEVEL,
    SUBJECT,
    TOPIC,
    Care,
    Need,
    care_fluency,
    care_foundation,
    scenario_question,
)
from otk.sets._support.science_wave_b12 import PUBERTY_CARE_SCENARIOS

PROVENANCE = Provenance("original")


PUBERTY_CARE = (
    Care("รักษาความสะอาดของร่างกายและอวัยวะเพศเป็นประจำ",
         "ต่อมเหงื่อและต่อมไขมันทำงานมากขึ้นในวัยนี้ การทำความสะอาดจึงลดกลิ่นกาย "
         "และลดโอกาสอักเสบติดเชื้อ"),
    Care("รับประทานอาหารให้ครบห้าหมู่และได้รับแคลเซียมอย่างเพียงพอ",
         "ร่างกายกำลังเจริญเติบโตอย่างรวดเร็ว จึงต้องการสารอาหารสำหรับสร้างกระดูก"
         "และกล้ามเนื้อมากกว่าช่วงวัยอื่น"),
    Care("ออกกำลังกายและนอนหลับพักผ่อนให้เพียงพอ",
         "ช่วยให้การเจริญเติบโตเป็นไปตามปกติ และช่วยให้อารมณ์มั่นคงขึ้นในช่วงที่"
         "ฮอร์โมนกำลังเปลี่ยนแปลง"),
    Care("ปรึกษาผู้ใหญ่ที่ไว้ใจได้เมื่อมีข้อสงสัยหรือความกังวล",
         "การเปลี่ยนแปลงในวัยนี้เป็นเรื่องปกติ การได้รับข้อมูลที่ถูกต้องช่วยลด"
         "ความกังวลและป้องกันความเข้าใจผิด"),
    Care("ไม่นำการเปลี่ยนแปลงของตนเองไปเปรียบเทียบกับเพื่อน",
         "แต่ละคนเข้าสู่วัยหนุ่มสาวในเวลาที่ต่างกันตามช่วงที่ฮอร์โมนเริ่มหลั่ง "
         "ความต่างนี้จึงไม่ใช่ความผิดปกติ"),
    Care("รู้เท่าทันอารมณ์ของตนเองและหากิจกรรมผ่อนคลายที่เหมาะสม",
         "ฮอร์โมนที่เปลี่ยนแปลงทำให้อารมณ์แปรปรวนง่ายขึ้น "
         "การรู้ที่มาของอารมณ์จึงช่วยให้จัดการกับอารมณ์นั้นได้"),
)


PUBERTY_NEEDS = (
    Need("นักเรียนเริ่มมีเหงื่อออกมากและมีกลิ่นกายชัดเจนกว่าเดิมหลังเลิกเรียน "
         "ควรปฏิบัติตามแนวทางใด",
         "รักษาความสะอาดของร่างกายและอวัยวะเพศเป็นประจำ"),
    Need("นักเรียนสูงขึ้นเร็วมากในปีนี้และรู้สึกหิวบ่อยกว่าเดิม "
         "ควรปฏิบัติตามแนวทางใดเพื่อให้ร่างกายเจริญเติบโตได้เต็มที่",
         "รับประทานอาหารให้ครบห้าหมู่และได้รับแคลเซียมอย่างเพียงพอ"),
    Need("นักเรียนนอนดึกเล่นโทรศัพท์ทุกคืนและรู้สึกเพลียกับหงุดหงิดง่ายในตอนกลางวัน "
         "ควรปฏิบัติตามแนวทางใด",
         "ออกกำลังกายและนอนหลับพักผ่อนให้เพียงพอ"),
    Need("นักเรียนมีข้อสงสัยเกี่ยวกับการเปลี่ยนแปลงของร่างกายตนเอง แต่ได้ข้อมูล"
         "ที่ขัดแย้งกันจากอินเทอร์เน็ต ควรปฏิบัติตามแนวทางใด",
         "ปรึกษาผู้ใหญ่ที่ไว้ใจได้เมื่อมีข้อสงสัยหรือความกังวล"),
    Need("นักเรียนกังวลว่าตนเองยังไม่มีการเปลี่ยนแปลงเหมือนเพื่อนร่วมชั้นที่อายุเท่ากัน "
         "ควรปฏิบัติตามแนวทางใด",
         "ไม่นำการเปลี่ยนแปลงของตนเองไปเปรียบเทียบกับเพื่อน"),
    Need("นักเรียนรู้สึกว่าตนเองโมโหง่ายกว่าเดิมมากจนมีปากเสียงกับคนในบ้านบ่อยครั้ง "
         "ควรปฏิบัติตามแนวทางใด",
         "รู้เท่าทันอารมณ์ของตนเองและหากิจกรรมผ่อนคลายที่เหมาะสม"),
)


@question_type(
    "body.puberty_care_foundation",
    display_name={"th": "เหตุผลของแนวทางดูแลตนเองในวัยหนุ่มสาว"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PubertyCareFoundation(QuestionType):
    """Why each way of looking after oneself matches a change of puberty."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return care_foundation(
            rng, system="ร่างกายและจิตใจในวัยหนุ่มสาว", cares=PUBERTY_CARE,
            hint="โยงแนวทางกลับไปที่การเปลี่ยนแปลงที่กำลังเกิดขึ้นจริง เช่น "
                 "ต่อมไขมันทำงานมากขึ้น ร่างกายเติบโตเร็ว หรืออารมณ์แปรปรวน",
        )


@question_type(
    "body.puberty_care_fluency",
    display_name={"th": "เลือกแนวทางดูแลตนเองให้ตรงกับการเปลี่ยนแปลง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PubertyCareFluency(QuestionType):
    """Pick the way of looking after oneself that the situation calls for.

    ``ม.2/14``'s evidence clause is ``โดยการดูแลรักษาร่างกายและจิตใจของตนเอง`` —
    conduct, which no item can observe. So this set is ``standard_scope``, unlike
    the ``บอกแนวทาง`` topics built on the same machinery.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return care_fluency(
            rng, needs=PUBERTY_NEEDS, cares=PUBERTY_CARE,
            hint="ระบุก่อนว่าสถานการณ์นี้เป็นเรื่องของร่างกายที่กำลังเปลี่ยนแปลง "
                 "หรือเป็นเรื่องของความรู้สึกและความกังวล",
        )


@question_type(
    "body.puberty_care_application",
    display_name={"th": "วิเคราะห์สถานการณ์การดูแลตนเองในวัยหนุ่มสาว"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PubertyCareApplication(QuestionType):
    """Judge advice about puberty against what is actually happening in the body."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, PUBERTY_CARE_SCENARIOS,
            hint="ตรวจว่าคำแนะนำนั้นสอดคล้องกับการเปลี่ยนแปลงที่เกิดขึ้นจริงหรือไม่ "
                 "และปลอดภัยต่อร่างกายที่กำลังเจริญเติบโตหรือไม่",
        )
