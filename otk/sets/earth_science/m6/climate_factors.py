"""ปัจจัยที่มีผลต่อการเปลี่ยนแปลงภูมิอากาศโลก

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/13

Sets moved here from: science_wave_c26.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_c26 import CLIMATE_FACTORS, CLIMATE_SCENARIOS

PROVENANCE = Provenance("original")


CLIMATE_FACTOR_TOPIC = "ปัจจัยที่มีผลต่อการเปลี่ยนแปลงภูมิอากาศโลก"


class Activity(NamedTuple):
    """A human activity that drives climate change, cases of it, and a practice that cuts it."""
    name: str
    cases: tuple[str, ...]
    practice: str


ACTIVITIES = (
    Activity("การเผาไหม้น้ำมันในการเดินทาง",
             ("ครอบครัวของนักเรียนขับรถยนต์ส่วนตัวคนละคันไปทำงานและไปโรงเรียนในเส้นทางเดียวกันทุกวัน",
              "พนักงานบริษัทหนึ่งขับรถยนต์คนเดียวต่อคันเข้าเมืองทุกเช้า ทั้งที่มีรถไฟฟ้าผ่านหน้าบ้าน"),
             "ใช้ระบบขนส่งสาธารณะ เดินทางร่วมกันในรถคันเดียว หรือเดินและปั่นจักรยานในระยะใกล้"),
    Activity("การใช้ไฟฟ้าที่ผลิตจากเชื้อเพลิงซากดึกดำบรรพ์",
             ("โรงเรียนเปิดเครื่องปรับอากาศและไฟในห้องเรียนทิ้งไว้ตลอดช่วงพักกลางวันที่ไม่มีคนอยู่",
              "หอพักแห่งหนึ่งใช้หลอดไส้รุ่นเก่าและเปิดโทรทัศน์ทิ้งไว้แม้ไม่มีคนดู"),
             "ปิดเครื่องใช้ไฟฟ้าเมื่อไม่ใช้ เลือกเครื่องใช้ไฟฟ้าประหยัดไฟ และติดตั้งแผงรับแสงอาทิตย์"),
    Activity("การตัดและเผาป่า",
             ("ชุมชนบนพื้นที่สูงถางและเผาป่าต้นน้ำทุกปีเพื่อเปิดพื้นที่ปลูกข้าวโพด",
              "บริษัทหนึ่งวางแผนตัดป่าชายเลนผืนใหญ่เพื่อทำบ่อเลี้ยงกุ้ง"),
             "อนุรักษ์ป่าเดิมไว้ ทำเกษตรแบบวนเกษตรบนพื้นที่เดิม และปลูกป่าทดแทนในพื้นที่เสื่อมโทรม"),
    Activity("การทิ้งขยะอินทรีย์ลงหลุมฝังกลบ",
             ("ร้านอาหารในตลาดทิ้งเศษอาหารรวมกับขยะอื่นทุกวัน และขยะทั้งหมดถูกนำไปฝังกลบ",
              "โรงอาหารของโรงเรียนมีเศษอาหารเหลือวันละหลายถังที่ถูกส่งไปหลุมฝังกลบ ซึ่งเศษอาหารเน่าเปื่อยแล้วปล่อยแก๊สมีเทน"),
             "คัดแยกเศษอาหารออกจากขยะอื่น แล้วนำไปทำปุ๋ยหมักหรือผลิตแก๊สชีวภาพแทนการฝังกลบ"),
    Activity("การเผาเศษวัสดุทางการเกษตรในที่โล่ง",
             ("หลังเก็บเกี่ยวข้าว ชาวนาในหมู่บ้านจุดไฟเผาฟางและตอซังทิ้งในนาทุกปี",
              "เกษตรกรไร่อ้อยเผาใบอ้อยก่อนตัดทุกฤดูเก็บเกี่ยว"),
             "ไถกลบตอซังและฟางลงดิน หรือตัดอ้อยสดแล้วนำใบไปคลุมดินแทนการเผา"),
)


@question_type(
    "geo.climate_factors_foundation",
    display_name={"th": "นำเสนอแนวปฏิบัติเพื่อลดกิจกรรมที่ส่งผลต่อการเปลี่ยนแปลงภูมิอากาศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=CLIMATE_FACTOR_TOPIC,
)
class ClimateFactorsFoundation(QuestionType):
    """A case of one activity; the practice that cuts that activity."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(ACTIVITIES))
        activity = ACTIVITIES[index]
        others = [other.practice for i, other in enumerate(ACTIVITIES) if i != index]
        return _labelled(
            stem=(f"{rng.choice(activity.cases)} ข้อใดเป็นแนวปฏิบัติที่ลดกิจกรรมในเรื่องนี้ "
                  "ซึ่งส่งผลต่อการเปลี่ยนแปลงภูมิอากาศโลกได้โดยตรง"),
            correct=activity.practice,
            wrongs=tuple(others),
            hint="ระบุก่อนว่ากิจกรรมในเรื่องปล่อยแก๊สเรือนกระจกจากอะไร แล้วเลือกแนวปฏิบัติที่ลดสิ่งนั้นโดยตรง",
            topic=CLIMATE_FACTOR_TOPIC,
        )


@question_type(
    "geo.climate_factors_fluency",
    display_name={"th": "อธิบายปัจจัยที่มีผลต่อการเปลี่ยนแปลงภูมิอากาศโลก"},
    level=UPPER_SIX, subject=SUBJECT, topic=CLIMATE_FACTOR_TOPIC,
)
class ClimateFactorsFluency(QuestionType):
    """Four of the factors explained together; each wrong choice falsifies one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = sorted(rng.sample(range(len(CLIMATE_FACTORS)), 4))
        return parts_item(
            rng, tuple(CLIMATE_FACTORS[i] for i in chosen),
            stem="ข้อใดอธิบายปัจจัยที่มีผลต่อการเปลี่ยนแปลงภูมิอากาศของโลกได้ถูกต้องทั้งหมด",
            hint="ตรวจทีละปัจจัย ข้อที่ผิดจะผิดอย่างน้อยหนึ่งปัจจัย",
            topic=CLIMATE_FACTOR_TOPIC,
        )


@question_type(
    "geo.climate_factors_application",
    display_name={"th": "วิเคราะห์ข้อมูลและผลย้อนกลับของการเปลี่ยนแปลงภูมิอากาศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=CLIMATE_FACTOR_TOPIC,
)
class ClimateFactorsApplication(QuestionType):
    """Pinatubo's cooling, thawing permafrost, and the carbon dioxide record."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CLIMATE_SCENARIOS,
            hint="แยกว่าปัจจัยใดทำให้โลกร้อนขึ้นหรือเย็นลง และผลนั้นอยู่ชั่วคราวหรือต่อเนื่อง",
        ), CLIMATE_FACTOR_TOPIC)
