"""การมีส่วนร่วมดูแลรักษาความหลากหลายทางชีวภาพ

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.3/11

Sets moved here from: science_wave_b28.
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
from otk.sets._support.science_wave_b25 import MIDDLE_THREE
from otk.sets._support.science_wave_b28 import BIODIVERSITY_TOPIC, CARE_SCENARIOS

PROVENANCE = Provenance("original")


BIODIVERSITY_CARE = (
    Care("ไม่ปล่อยสัตว์เลี้ยงหรือสัตว์ต่างถิ่นลงสู่แหล่งน้ำธรรมชาติ",
         "สัตว์ต่างถิ่นอาจแย่งอาหารและที่อยู่จนชนิดพื้นเมืองลดลง "
         "และบางชนิดไม่มีผู้ล่าตามธรรมชาติในถิ่นใหม่"),
    Care("ไม่ซื้อผลิตภัณฑ์ที่ทำจากสัตว์ป่าหรือพืชหายาก",
         "ความต้องการซื้อเป็นแรงจูงใจให้มีการล่าและเก็บจากธรรมชาติต่อไป "
         "การไม่ซื้อจึงตัดที่ต้นทางของปัญหา"),
    Care("ช่วยกันปลูกและดูแลพรรณไม้ท้องถิ่นในโรงเรียนและชุมชน",
         "พรรณไม้ท้องถิ่นเป็นอาหารและที่อาศัยของแมลงและนกประจำถิ่น "
         "จึงช่วยรักษาสิ่งมีชีวิตหลายชนิดไว้พร้อมกัน"),
    Care("ลดการใช้สารเคมีกำจัดแมลงในบริเวณบ้านและแปลงเกษตร",
         "สารเคมีทำลายทั้งแมลงศัตรูพืชและแมลงที่มีประโยชน์ "
         "เช่น แมลงผสมเรณูและตัวห้ำที่ควบคุมศัตรูพืชตามธรรมชาติ"),
    Care("แยกและจัดการขยะไม่ให้ลงสู่แหล่งน้ำและทะเล",
         "ขยะโดยเฉพาะพลาสติกทำให้สัตว์น้ำติดหรือกินเข้าไปจนตาย "
         "และสะสมอยู่ในระบบนิเวศเป็นเวลานาน"),
    Care("ร่วมสำรวจและบันทึกชนิดของสิ่งมีชีวิตในท้องถิ่น",
         "ข้อมูลที่เก็บอย่างต่อเนื่องทำให้รู้ว่าชนิดใดกำลังลดลง "
         "และเป็นหลักฐานให้วางแผนอนุรักษ์ได้ตรงจุด"),
)


BIODIVERSITY_NEEDS = (
    Need("นักเรียนเลี้ยงปลาต่างถิ่นไว้ในตู้ แล้วเบื่อจึงคิดจะนำไปปล่อยในคลอง "
         "ควรปฏิบัติตามแนวทางใด",
         "ไม่ปล่อยสัตว์เลี้ยงหรือสัตว์ต่างถิ่นลงสู่แหล่งน้ำธรรมชาติ"),
    Need("ร้านของที่ระลึกแห่งหนึ่งขายเครื่องประดับที่ทำจากเปลือกหอยหายาก "
         "และงาช้าง ควรปฏิบัติตามแนวทางใด",
         "ไม่ซื้อผลิตภัณฑ์ที่ทำจากสัตว์ป่าหรือพืชหายาก"),
    Need("โรงเรียนมีพื้นที่ว่างและอยากเพิ่มนกกับผีเสื้อในบริเวณโรงเรียน "
         "ควรปฏิบัติตามแนวทางใด",
         "ช่วยกันปลูกและดูแลพรรณไม้ท้องถิ่นในโรงเรียนและชุมชน"),
    Need("สวนหลังบ้านของนักเรียนเคยมีผึ้งมาตอมดอกไม้ แต่หลังจากพ่นยาฆ่าแมลง"
         "ทุกสัปดาห์แล้วไม่มีผึ้งมาอีกเลย ควรปฏิบัติตามแนวทางใด",
         "ลดการใช้สารเคมีกำจัดแมลงในบริเวณบ้านและแปลงเกษตร"),
    Need("ชายหาดใกล้บ้านมีถุงพลาสติกลอยอยู่จำนวนมาก และพบเต่าทะเลเกยตื้น "
         "ควรปฏิบัติตามแนวทางใด",
         "แยกและจัดการขยะไม่ให้ลงสู่แหล่งน้ำและทะเล"),
    Need("ชุมชนสงสัยว่านกบางชนิดในท้องถิ่นหายไป แต่ไม่มีข้อมูลย้อนหลังเลย "
         "ควรปฏิบัติตามแนวทางใด",
         "ร่วมสำรวจและบันทึกชนิดของสิ่งมีชีวิตในท้องถิ่น"),
)


@question_type(
    "ecology.biodiversity_care_foundation",
    display_name={"th": "เหตุผลของแนวทางดูแลความหลากหลายทางชีวภาพ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=BIODIVERSITY_TOPIC,
)
class BiodiversityCareFoundation(QuestionType):
    """Match a conservation practice to the reason it works."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_foundation(
            rng, system="ความหลากหลายทางชีวภาพในท้องถิ่น",
            cares=BIODIVERSITY_CARE,
            hint="โยงกลับไปว่าการกระทำนั้นตัดปัญหาที่ต้นทางใด",
        ), BIODIVERSITY_TOPIC)


@question_type(
    "ecology.biodiversity_care_fluency",
    display_name={"th": "เลือกแนวทางดูแลความหลากหลายทางชีวภาพ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=BIODIVERSITY_TOPIC,
)
class BiodiversityCareFluency(QuestionType):
    """Choose the practice that fits the situation.

    ``ม.3/11``'s evidence clause is ``โดยมีส่วนร่วมในการดูแลรักษา`` — conduct, so
    this set is ``standard_scope`` even though it states a แนวทาง.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_fluency(
            rng, needs=BIODIVERSITY_NEEDS, cares=BIODIVERSITY_CARE,
            hint="เลือกแนวทางที่ตรงกับปัญหาที่โจทย์บรรยายไว้ "
                 "ไม่ใช่แนวทางที่ดีโดยทั่วไป",
        ), BIODIVERSITY_TOPIC)


@question_type(
    "ecology.biodiversity_care_application",
    display_name={"th": "วิเคราะห์การมีส่วนร่วมดูแลความหลากหลายทางชีวภาพ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=BIODIVERSITY_TOPIC,
)
class BiodiversityCareApplication(QuestionType):
    """Judge whether an action helps diversity or only looks like it does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CARE_SCENARIOS,
            hint="ถามว่าการกระทำนั้นแก้ที่ต้นเหตุของการสูญเสียหรือไม่ "
                 "และผลอยู่ได้นานเพียงใด",
        ), BIODIVERSITY_TOPIC)


# More practices, each with its own reason and the one situation it answers,
# so every practice still answers exactly one situation.
BIODIVERSITY_CARE += (
    Care('ไม่เก็บพืชหรือจับสัตว์ออกจากป่าและเขตอนุรักษ์',
         'การนำสิ่งมีชีวิตออกจากถิ่นที่อยู่ลดจำนวนประชากรในธรรมชาติ ซึ่งชนิดที่เหลือน้อยอาจฟื้นตัวไม่ทัน'),
    Care('ลดแสงไฟที่ส่องสว่างจ้าตลอดคืนบริเวณริมน้ำ',
         'แสงไฟรบกวนสัตว์ที่หากินและสื่อสารในเวลากลางคืน เช่น หิ่งห้อยที่ใช้แสงของตนหาคู่'),
)
BIODIVERSITY_NEEDS += (
    Need('นักท่องเที่ยวเห็นกล้วยไม้ป่าสวยงามในอุทยานแห่งชาติ และอยากขุดกลับไปปลูกที่บ้าน ควรปฏิบัติตามแนวทางใด',
         'ไม่เก็บพืชหรือจับสัตว์ออกจากป่าและเขตอนุรักษ์'),
    Need('ชุมชนริมคลองติดไฟส่องสว่างจ้าตลอดคืน และหิ่งห้อยที่เคยมีมากลดลงเรื่อย ๆ ควรปฏิบัติตามแนวทางใด',
         'ลดแสงไฟที่ส่องสว่างจ้าตลอดคืนบริเวณริมน้ำ'),
)
