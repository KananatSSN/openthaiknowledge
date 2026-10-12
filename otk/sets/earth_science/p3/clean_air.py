"""การลดมลพิษทางอากาศ

ธรณีวิทยา · ป.3 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.3/2

Sets moved here from: science_wave_c11.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import Care, Need, care_fluency, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import PRIMARY_THREE, _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c11 import CLEAN_AIR_SCENARIOS

PROVENANCE = Provenance("original")


CLEAN_AIR_TOPIC = "การลดมลพิษทางอากาศ"


CLEAN_AIR_CARE = (
    Care("ไม่เผาขยะ ใบไม้ หรือตอซังข้าว",
         "การเผาทำให้เกิดควันและฝุ่นละอองลอยขึ้นไปในอากาศโดยตรง"),
    Care("เดิน ปั่นจักรยาน หรือใช้รถโดยสารสาธารณะแทนการใช้รถยนต์ส่วนตัว",
         "รถยนต์ที่วิ่งบนถนนน้อยลงทำให้ควันจากท่อไอเสียลดลง"),
    Care("ปลูกต้นไม้และช่วยกันดูแลต้นไม้ในชุมชน",
         "ใบไม้ช่วยดักจับฝุ่นละออง และพืชช่วยเพิ่มแก๊สออกซิเจนให้อากาศ"),
    Care("ดับเครื่องยนต์ทุกครั้งเมื่อจอดรถรอเป็นเวลานาน",
         "เครื่องยนต์ที่ติดทิ้งไว้ยังปล่อยควันออกมาตลอดแม้รถไม่ได้วิ่ง"),
    Care("ทิ้งขยะให้ถูกที่และแยกขยะเพื่อนำกลับมาใช้ใหม่",
         "ขยะที่ถูกแยกและนำกลับไปใช้ใหม่ไม่ต้องถูกนำไปเผาทิ้ง"),
    Care("ปิดไฟและเครื่องใช้ไฟฟ้าทุกครั้งเมื่อไม่ใช้",
         "โรงไฟฟ้าหลายแห่งผลิตไฟฟ้าด้วยการเผาเชื้อเพลิง การใช้ไฟฟ้าน้อยลงจึงลดควันจากการผลิตไฟฟ้า"),
)


CLEAN_AIR_NEEDS = (
    Need("หลังเก็บเกี่ยวข้าว ชาวนาในหมู่บ้านมักจุดไฟเผาฟางและตอซัง ทำให้ท้องฟ้าเป็นหมอกควัน "
         "ควรเสนอแนวทางใดที่แก้ต้นเหตุได้ตรงที่สุด",
         "ไม่เผาขยะ ใบไม้ หรือตอซังข้าว"),
    Need("ถนนหน้าโรงเรียนมีรถยนต์ส่วนตัวมาส่งนักเรียนจำนวนมากจนควันรถลอยเข้ามาในห้องเรียน "
         "ทั้งที่บ้านของนักเรียนหลายคนอยู่ใกล้โรงเรียน ควรเสนอแนวทางใดที่แก้ต้นเหตุได้ตรงที่สุด",
         "เดิน ปั่นจักรยาน หรือใช้รถโดยสารสาธารณะแทนการใช้รถยนต์ส่วนตัว"),
    Need("ผู้ปกครองหลายคนจอดรถรอรับนักเรียนหน้าโรงเรียนนานครึ่งชั่วโมงโดยติดเครื่องยนต์ไว้ "
         "ควรเสนอแนวทางใดที่แก้ต้นเหตุได้ตรงที่สุด",
         "ดับเครื่องยนต์ทุกครั้งเมื่อจอดรถรอเป็นเวลานาน"),
    Need("ชุมชนริมถนนใหญ่มีฝุ่นละอองมาก และมีที่ว่างที่ยังไม่มีต้นไม้เลย ควรเสนอแนวทางใดที่ช่วยได้ตรงที่สุด",
         "ปลูกต้นไม้และช่วยกันดูแลต้นไม้ในชุมชน"),
    Need("ในชุมชนมีคนนำขวดพลาสติกและกล่องกระดาษไปกองรวมกันแล้วจุดไฟเผาทุกสัปดาห์ "
         "ควรเสนอแนวทางใดที่แก้ต้นเหตุได้ตรงที่สุด",
         "ทิ้งขยะให้ถูกที่และแยกขยะเพื่อนำกลับมาใช้ใหม่"),
    Need("หลังเลิกเรียนทุกวัน ห้องเรียนหลายห้องยังเปิดไฟและเครื่องปรับอากาศทิ้งไว้ทั้งที่ไม่มีใครอยู่ "
         "ควรเสนอแนวทางใดที่ช่วยลดมลพิษทางอากาศได้ตรงที่สุด",
         "ปิดไฟและเครื่องใช้ไฟฟ้าทุกครั้งเมื่อไม่ใช้"),
)


@question_type(
    "geo.clean_air_foundation",
    display_name={"th": "เหตุผลของแนวทางลดมลพิษทางอากาศ"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=CLEAN_AIR_TOPIC,
)
class CleanAirFoundation(QuestionType):
    """Match a practice to the reason it keeps air clean, in either direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CLEAN_AIR_CARE)
        others = [other for other in CLEAN_AIR_CARE if other.practice != item.practice]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"การ“{item.practice}” ช่วยลดมลพิษทางอากาศได้อย่างไร",
                correct=item.reason,
                wrongs=tuple(other.reason for other in others[:3]),
                hint="นึกว่าการกระทำนั้นทำให้ควันหรือฝุ่นลดลงอย่างไร",
                topic=CLEAN_AIR_TOPIC,
            )
        return _labelled(
            stem=f"แนวทางใดช่วยลดมลพิษทางอากาศ เพราะ{item.reason}",
            correct=item.practice,
            wrongs=tuple(other.practice for other in others[:3]),
            hint="นึกว่าการกระทำนั้นทำให้ควันหรือฝุ่นลดลงอย่างไร",
            topic=CLEAN_AIR_TOPIC,
        )


@question_type(
    "geo.clean_air_fluency",
    display_name={"th": "เสนอแนวทางลดมลพิษทางอากาศให้ตรงกับปัญหา"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=CLEAN_AIR_TOPIC,
)
class CleanAirFluency(QuestionType):
    """Put forward the practice that fits a case — the indicator's own clause."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_fluency(
            rng, needs=CLEAN_AIR_NEEDS, cares=CLEAN_AIR_CARE,
            hint="หาต้นเหตุของควันหรือฝุ่นในเรื่องก่อน แล้วเลือกแนวทางที่แก้ต้นเหตุนั้น",
        ), CLEAN_AIR_TOPIC)


@question_type(
    "geo.clean_air_application",
    display_name={"th": "วางแนวทางลดมลพิษทางอากาศในชุมชน"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=CLEAN_AIR_TOPIC,
)
class CleanAirApplication(QuestionType):
    """Make an agreement workable and trace pollution beyond the place it starts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CLEAN_AIR_SCENARIOS,
            hint="ถามว่าแนวทางนั้นลดควันหรือฝุ่นที่ต้นเหตุได้จริงหรือไม่",
        ), CLEAN_AIR_TOPIC)
