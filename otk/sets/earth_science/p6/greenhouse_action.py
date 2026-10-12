"""การลดแก๊สเรือนกระจก

ธรณีวิทยา · ป.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.6/9

Sets moved here from: science_wave_c16.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import Care, Need, care_fluency, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import PRIMARY_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c16 import ACTION_SCENARIOS

PROVENANCE = Provenance("original")


ACTION_TOPIC = "การลดแก๊สเรือนกระจก"


ACTION_CARE = (
    Care("ปิดไฟและถอดปลั๊กเครื่องใช้ไฟฟ้าเมื่อไม่ใช้",
         "ไฟฟ้าส่วนใหญ่ผลิตจากการเผาเชื้อเพลิง ใช้ไฟฟ้าน้อยลงจึงปล่อยแก๊สคาร์บอนไดออกไซด์น้อยลง"),
    Care("เดิน ปั่นจักรยาน หรือใช้รถโดยสารสาธารณะแทนรถยนต์ส่วนตัว",
         "รถยนต์ที่วิ่งน้อยลงเผาน้ำมันน้อยลง จึงปล่อยแก๊สคาร์บอนไดออกไซด์น้อยลง"),
    Care("ไถกลบฟางข้าวแทนการเผา",
         "การเผาปล่อยแก๊สคาร์บอนไดออกไซด์ออกมาทันที ส่วนการไถกลบคืนอินทรียวัตถุให้ดิน"),
    Care("ตักอาหารแต่พอกินและนำเศษอาหารไปทำปุ๋ยหมัก",
         "เศษอาหารที่ถูกฝังกลบรวมกับขยะอื่นจะเน่าและปล่อยแก๊สมีเทนออกมา"),
    Care("ช่วยกันปลูกและดูแลต้นไม้",
         "ต้นไม้ดูดซับแก๊สคาร์บอนไดออกไซด์ไปใช้ในการสร้างอาหาร"),
    Care("ลดการใช้ถุงพลาสติกและภาชนะที่ใช้ครั้งเดียวทิ้ง",
         "การผลิตพลาสติกใช้เชื้อเพลิงและพลังงานมาก ใช้น้อยลงจึงลดแก๊สคาร์บอนไดออกไซด์จากการผลิต"),
)


ACTION_NEEDS = (
    Need("ห้องเรียนหลายห้องเปิดไฟและพัดลมทิ้งไว้ตลอดช่วงพักกลางวันทั้งที่ไม่มีคนอยู่ "
         "ควรเสนอแนวทางใดที่ลดแก๊สเรือนกระจกได้ตรงกับปัญหาที่สุด",
         "ปิดไฟและถอดปลั๊กเครื่องใช้ไฟฟ้าเมื่อไม่ใช้"),
    Need("นักเรียนส่วนใหญ่บ้านอยู่ห่างโรงเรียนไม่ถึงหนึ่งกิโลเมตร แต่ผู้ปกครองขับรถยนต์มาส่งทุกคน "
         "ควรเสนอแนวทางใดที่ลดแก๊สเรือนกระจกได้ตรงกับปัญหาที่สุด",
         "เดิน ปั่นจักรยาน หรือใช้รถโดยสารสาธารณะแทนรถยนต์ส่วนตัว"),
    Need("หลังเก็บเกี่ยวข้าว ชาวนาในชุมชนจุดไฟเผาฟางทิ้งทั้งทุ่ง "
         "ควรเสนอแนวทางใดที่ลดแก๊สเรือนกระจกได้ตรงกับปัญหาที่สุด",
         "ไถกลบฟางข้าวแทนการเผา"),
    Need("โรงอาหารของโรงเรียนมีอาหารเหลือทิ้งรวมกับขยะอื่นหลายถังทุกวัน "
         "ควรเสนอแนวทางใดที่ลดแก๊สเรือนกระจกได้ตรงกับปัญหาที่สุด",
         "ตักอาหารแต่พอกินและนำเศษอาหารไปทำปุ๋ยหมัก"),
    Need("ที่ดินว่างของชุมชนถูกปล่อยโล่งหลังป่าเดิมถูกโค่น ไม่มีต้นไม้เหลืออยู่เลย "
         "ควรเสนอแนวทางใดที่ลดแก๊สเรือนกระจกได้ตรงกับปัญหาที่สุด",
         "ช่วยกันปลูกและดูแลต้นไม้"),
    Need("ร้านค้าในโรงเรียนใส่ขนมทุกชิ้นในถุงพลาสติกใบใหม่ และมีแก้วพลาสติกใช้ครั้งเดียวทิ้งเต็มถังขยะทุกวัน "
         "ควรเสนอแนวทางใดที่ลดแก๊สเรือนกระจกได้ตรงกับปัญหาที่สุด",
         "ลดการใช้ถุงพลาสติกและภาชนะที่ใช้ครั้งเดียวทิ้ง"),
)


@question_type(
    "geo.greenhouse_action_foundation",
    display_name={"th": "เหตุผลของแนวทางลดแก๊สเรือนกระจก"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=ACTION_TOPIC,
)
class GreenhouseActionFoundation(QuestionType):
    """Match a practice to why it cuts greenhouse gases, in either direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ACTION_CARE)
        others = [other for other in ACTION_CARE if other.practice != item.practice]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"การ“{item.practice}” ช่วยลดแก๊สเรือนกระจกได้อย่างไร",
                correct=item.reason,
                wrongs=tuple(other.reason for other in others[:3]),
                hint="นึกว่าการกระทำนั้นลดการเผาเชื้อเพลิง ลดการเน่าของขยะ หรือเพิ่มการดูดซับแก๊ส",
                topic=ACTION_TOPIC,
            )
        return _labelled(
            stem=f"แนวทางใดช่วยลดแก๊สเรือนกระจก โดยอาศัยเหตุผลที่ว่า{item.reason}",
            correct=item.practice,
            wrongs=tuple(other.practice for other in others[:3]),
            hint="นึกว่าการกระทำนั้นลดการเผาเชื้อเพลิง ลดการเน่าของขยะ หรือเพิ่มการดูดซับแก๊ส",
            topic=ACTION_TOPIC,
        )


@question_type(
    "geo.greenhouse_action_fluency",
    display_name={"th": "เสนอแนวทางลดแก๊สเรือนกระจกให้ตรงกับปัญหา"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=ACTION_TOPIC,
)
class GreenhouseActionFluency(QuestionType):
    """Put forward the practice that fits a case — the indicator's own clause."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_fluency(
            rng, needs=ACTION_NEEDS, cares=ACTION_CARE,
            hint="หาว่าแก๊สเรือนกระจกในเรื่องมาจากกิจกรรมใด แล้วเลือกแนวทางที่ลดกิจกรรมนั้นโดยตรง",
        ), ACTION_TOPIC)


@question_type(
    "geo.greenhouse_action_application",
    display_name={"th": "วางแผนและประเมินการลดแก๊สเรือนกระจก"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=ACTION_TOPIC,
)
class GreenhouseActionApplication(QuestionType):
    """Measure a campaign fairly, answer "one person can't", and choose what is doable."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ACTION_SCENARIOS,
            hint="ถามว่าแนวทางนั้นลดการเผาเชื้อเพลิงหรือการเกิดแก๊สได้จริงหรือไม่",
        ), ACTION_TOPIC)
