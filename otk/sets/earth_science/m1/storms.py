"""พายุฝนฟ้าคะนองและพายุหมุนเขตร้อน

ธรณีวิทยา · ม.1 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.1/3

Sets moved here from: science_wave_c17.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b2 import LEVEL as MIDDLE_ONE
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c17 import STORM_SCENARIOS

PROVENANCE = Provenance("original")


STORM_TOPIC = "พายุฝนฟ้าคะนองและพายุหมุนเขตร้อน"


class Storm(NamedTuple):
    """A storm, how it forms, and what it does to living things and the environment."""
    name: str
    forms: str
    effects: str


STORMS = (
    Storm("พายุฝนฟ้าคะนอง",
          "อากาศร้อนชื้นยกตัวสูงขึ้นอย่างรวดเร็วจนเกิดเมฆคิวมูโลนิมบัส ครอบคลุมพื้นที่ไม่กว้างและเกิดเพียงไม่กี่ชั่วโมง",
          "เกิดฟ้าผ่า ลมกระโชกแรง ลูกเห็บ และน้ำท่วมฉับพลันเฉพาะพื้นที่"),
    Storm("พายุหมุนเขตร้อน",
          "อากาศเหนือมหาสมุทรที่มีน้ำอุ่นหมุนเวียนเข้าหาศูนย์กลางความกดอากาศต่ำ ครอบคลุมพื้นที่กว้างหลายร้อยกิโลเมตรและนานหลายวัน",
          "ลมแรงและฝนตกหนักเป็นบริเวณกว้างหลายวัน ทำให้น้ำท่วมใหญ่ คลื่นซัดฝั่ง และบ้านเรือนพังเสียหาย"),
)


def _compare(forms: tuple[str, str], effects: tuple[str, str]) -> str:
    return " / ".join(f"{storm.name}: เกิดจาก{form} ผลคือ{effect}"
                      for storm, form, effect in zip(STORMS, forms, effects))


class Case(NamedTuple):
    """A storm situation, and the one practice that fits it."""
    situation: str
    practice: str


STORM_CASES = (
    Case("นักเรียนกำลังเล่นฟุตบอลกลางสนามโล่ง แล้วเริ่มมีฟ้าแลบฟ้าร้องและลมกระโชกแรง",
         "หยุดเล่นและหลบเข้าอาคารที่มิดชิด ไม่หลบใต้ต้นไม้สูงหรืออยู่กลางที่โล่ง"),
    Case("กรมอุตุนิยมวิทยาประกาศว่าพายุโซนร้อนจะเคลื่อนเข้าจังหวัดของนักเรียนในอีกสองวัน",
         "ติดตามประกาศอย่างต่อเนื่อง เตรียมน้ำดื่ม อาหาร ยา และไฟฉาย และอพยพเมื่อได้รับแจ้ง"),
    Case("ฝนตกหนักจากพายุหลายชั่วโมง จนน้ำไหลเชี่ยวท่วมถนนหน้าบ้าน",
         "ไม่เดินหรือขับรถลุยน้ำที่ไหลเชี่ยว และขึ้นไปอยู่ในที่สูง"),
    Case("มีประกาศเตือนคลื่นลมแรงในทะเลอ่าวไทยจากพายุที่กำลังเคลื่อนเข้าใกล้",
         "ชาวประมงงดออกเรือและนำเรือเข้าจอดในที่ปลอดภัย"),
    Case("ผู้ปกครองกำลังขับรถกลางพายุฝนฟ้าคะนอง ฝนตกหนักจนมองทางข้างหน้าแทบไม่เห็น",
         "ชะลอความเร็ว เปิดไฟหน้า และจอดในที่ปลอดภัยห่างจากต้นไม้ใหญ่และป้ายโฆษณาจนฝนซา"),
    Case("ลูกเห็บก้อนใหญ่เริ่มตกลงมาขณะนักเรียนเดินอยู่กลางลานโรงเรียน",
         "รีบเข้าไปอยู่ใต้หลังคาที่แข็งแรงและอยู่ห่างจากหน้าต่างกระจก"),
    Case("หลังพายุผ่านไป พบสายไฟฟ้าขาดตกอยู่บนพื้นที่มีน้ำขังหน้าบ้าน",
         "อยู่ห่างจากสายไฟและน้ำขังบริเวณนั้น แล้วแจ้งการไฟฟ้าให้มาแก้ไข"),
)


# True contrasts between the two storms. Swapping the two names makes each false.
STORM_CONTRASTS = (
    "{a}ครอบคลุมพื้นที่ไม่กว้าง ส่วน{b}ครอบคลุมพื้นที่กว้างหลายร้อยกิโลเมตร",
    "{a}เกิดเพียงไม่กี่ชั่วโมง ส่วน{b}อยู่นานหลายวัน",
    "{a}เกิดได้บนแผ่นดินเมื่ออากาศร้อนชื้นยกตัว ส่วน{b}ก่อตัวเหนือมหาสมุทรที่มีน้ำอุ่น",
    "{a}ทำให้น้ำท่วมฉับพลันเฉพาะพื้นที่ ส่วน{b}ทำให้น้ำท่วมใหญ่เป็นบริเวณกว้าง",
    "{a}เกิดจากเมฆคิวมูโลนิมบัสก้อนใหญ่ ส่วน{b}หมุนเวียนเข้าหาศูนย์กลางความกดอากาศต่ำ",
)


# More contrasts. Swapped, each puts at least one storm on the wrong side.
STORM_CONTRASTS = (*STORM_CONTRASTS,
    "{a}มักมีฟ้าแลบ ฟ้าร้อง และอาจมีลูกเห็บตกเป็นจุด ๆ ส่วน{b}มีตาพายุที่ค่อนข้างสงบอยู่ตรงกลาง",
    "{a}อ่อนกำลังลงเมื่อเมฆปล่อยฝนออกมาหมด ส่วน{b}อ่อนกำลังลงเมื่อขึ้นฝั่งและขาดไอน้ำจากทะเลอุ่น",
    "{a}เตือนภัยล่วงหน้าได้เพียงไม่กี่ชั่วโมง ส่วน{b}ติดตามเส้นทางได้ล่วงหน้าหลายวัน",
    "{a}ทำให้กิ่งไม้หักหรือป้ายล้มเป็นจุด ๆ ส่วน{b}ทำให้คลื่นซัดฝั่งสูงและบ้านเรือนเสียหายเป็นบริเวณกว้าง",
)


STORM_SAMENESS = (
    "ทั้งสองพายุก่อตัวเหนือมหาสมุทรและอยู่นานหลายวันเท่ากัน",
    "ทั้งสองพายุครอบคลุมพื้นที่เท่ากัน ต่างกันเพียงชื่อที่ใช้เรียก",
)


@question_type(
    "geo.storms_foundation",
    display_name={"th": "ปฏิบัติตนให้ปลอดภัยจากพายุ"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=STORM_TOPIC,
)
class StormsFoundation(QuestionType):
    """Put forward the practice that fits a storm case — the second free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        case = rng.choice(STORM_CASES)
        return _labelled(
            stem=f"{case.situation} ควรปฏิบัติตนอย่างไรจึงเหมาะสมและปลอดภัยที่สุด",
            correct=case.practice,
            wrongs=tuple([other.practice for other in STORM_CASES if other.practice != case.practice]),
            hint="หาอันตรายที่ใกล้ตัวที่สุดในเรื่อง แล้วเลือกวิธีที่หลีกเลี่ยงอันตรายนั้นโดยตรง",
            topic=STORM_TOPIC,
        )


@question_type(
    "geo.storms_fluency",
    display_name={"th": "เปรียบเทียบการเกิดและผลของพายุฝนฟ้าคะนองและพายุหมุนเขตร้อน"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=STORM_TOPIC,
)
class StormsFluency(QuestionType):
    """Compare both storms' formation and effects in one answer."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            thunder, cyclone = (storm.name for storm in STORMS)
            true = [c.format(a=thunder, b=cyclone) for c in STORM_CONTRASTS]
            false = [c.format(a=cyclone, b=thunder) for c in STORM_CONTRASTS]
            return _labelled(
                stem="ข้อใดเปรียบเทียบพายุฝนฟ้าคะนองกับพายุหมุนเขตร้อนได้ถูกต้อง",
                correct=rng.choice(true),
                wrongs=tuple(false + list(STORM_SAMENESS)),
                hint="เทียบขนาดพื้นที่ ระยะเวลา และที่ที่ก่อตัว แล้วตรวจว่าพายุแต่ละชนิดอยู่ถูกฝั่งหรือไม่",
                topic=STORM_TOPIC,
            )
        forms = tuple(storm.forms for storm in STORMS)
        effects = tuple(storm.effects for storm in STORMS)
        flipped_forms = (forms[1], forms[0])
        flipped_effects = (effects[1], effects[0])
        return _labelled(
            stem="ข้อใดเปรียบเทียบกระบวนการเกิดของพายุฝนฟ้าคะนองและพายุหมุนเขตร้อน "
                 "และผลที่มีต่อสิ่งมีชีวิตและสิ่งแวดล้อมได้ถูกต้องทั้งหมด",
            correct=_compare(forms, effects),
            wrongs=(_compare(flipped_forms, effects),
                    _compare(forms, flipped_effects),
                    _compare(flipped_forms, flipped_effects)),
            hint="เทียบขนาดพื้นที่และระยะเวลาก่อน แล้วตรวจว่าผลที่เกิดสอดคล้องกับขนาดของพายุหรือไม่",
            topic=STORM_TOPIC,
        )


@question_type(
    "geo.storms_application",
    display_name={"th": "วิเคราะห์การเกิดพายุและการลดความเสียหาย"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=STORM_TOPIC,
)
class StormsApplication(QuestionType):
    """Why a cyclone weakens over land, afternoon storms, and coastal preparation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, STORM_SCENARIOS,
            hint="นึกว่าพายุได้พลังงานมาจากที่ใด และขนาดของพายุบอกอะไรเกี่ยวกับความเสียหาย",
        ), STORM_TOPIC)
