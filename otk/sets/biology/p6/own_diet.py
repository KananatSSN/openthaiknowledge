"""การเลือกรับประทานอาหารของตนเอง

ชีวะ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.6/3

Sets moved here from: science_wave_b18.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, Care, care_foundation, scenario_question
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import BODY_TOPIC, PRIMARY_SIX, _body
from otk.sets._support.science_wave_b18 import OWN_DIET_SCENARIOS

PROVENANCE = Provenance("original")


class DayRecord(NamedTuple):
    """One day's eating as a learner would record it, and the fairest verdict."""
    record: str
    verdict: str


# Each verdict names one thing to fix, so the answer is single. The wrong choices
# are other days' verdicts — all reasonable-sounding, all wrong for this record.
DAY_RECORDS = (
    DayRecord("เช้า ปาท่องโก๋กับนมหวาน กลางวัน ข้าวไข่เจียว เย็น ข้าวผัดหมู "
              "ไม่มีผักหรือผลไม้เลยทั้งวัน",
              "ได้พลังงานและโปรตีนพอ แต่ขาดผักและผลไม้ จึงควรเพิ่มผักในมื้อกลางวัน"
              "และผลไม้เป็นของว่าง"),
    DayRecord("เช้า ไม่ได้กิน กลางวัน ก๋วยเตี๋ยวหนึ่งชาม เย็น ข้าวกับผัดผักรวม "
              "ดื่มน้ำเปล่าตลอดวัน",
              "อาหารที่กินมีคุณภาพดี แต่การอดมื้อเช้าทำให้ได้พลังงานไม่พอ"
              "ในช่วงเรียนตอนเช้า จึงควรกินมื้อเช้าด้วย"),
    DayRecord("เช้า ข้าวกับไข่ต้มและผลไม้ กลางวัน ข้าวกับแกงจืดและผัก "
              "เย็น ข้าวกับปลาทอดและผัก แต่ดื่มแต่น้ำอัดลมตลอดวัน",
              "มื้อหลักครบถ้วนดีแล้ว แต่ควรเปลี่ยนจากน้ำอัดลมเป็นน้ำเปล่า "
              "เพราะน้ำอัดลมให้น้ำตาลมากโดยไม่ให้สารอาหารอื่น"),
    DayRecord("เช้า ขนมกรุบกรอบหนึ่งถุง กลางวัน ข้าวกับไก่ทอดสองชิ้น "
              "เย็น พิซซ่าและน้ำหวาน ไม่มีผักเลย",
              "ได้ไขมันและน้ำตาลมากเกินไปและขาดผักผลไม้ จึงควรลดของทอดกับน้ำหวาน"
              "และเพิ่มผักผลไม้ในทุกมื้อ"),
    DayRecord("เช้า ข้าวต้มปลา กลางวัน สลัดผักหนึ่งจาน เย็น ผลไม้รวมหนึ่งจาน "
              "ไม่มีข้าวหรือแป้งในสองมื้อหลัง",
              "ได้ผักและผลไม้มากดีแล้ว แต่ได้พลังงานจากข้าวและแป้งน้อยเกินไป "
              "จึงควรเพิ่มข้าวหรือขนมปังในมื้อกลางวันและมื้อเย็น"),
    DayRecord("เช้า ข้าวกับหมูปิ้งสามไม้ กลางวัน ข้าวขาหมูจานใหญ่ "
              "เย็น ข้าวกับหมูกรอบ ไม่ได้กินผักและไม่ได้ออกกำลังกาย",
              "ได้เนื้อสัตว์ติดมันและพลังงานมากเกินความต้องการของวัย "
              "จึงควรลดปริมาณลง เพิ่มผัก และเคลื่อนไหวร่างกายให้มากขึ้น"),
)


DIET_CARE = (
    Care("กินอาหารเช้าทุกวัน",
         "ร่างกายไม่ได้รับอาหารมาตลอดคืน มื้อเช้าจึงเป็นพลังงานที่ใช้เรียน"
         "และทำกิจกรรมในช่วงเช้า"),
    Care("กินผักและผลไม้ให้ได้ทุกวัน",
         "ผักและผลไม้ให้วิตามินและแร่ธาตุที่ช่วยให้อวัยวะทำงานได้ตามปกติ "
         "ซึ่งอาหารกลุ่มอื่นให้แทนไม่ได้"),
    Care("กินเนื้อสัตว์ ไข่ นม หรือถั่วให้ได้ทุกวัน",
         "อาหารกลุ่มนี้ให้โปรตีนที่ใช้สร้างและซ่อมแซมร่างกาย "
         "ซึ่งจำเป็นมากในวัยที่กำลังเจริญเติบโต"),
    Care("ลดของทอดและขนมหวานลง",
         "ไขมันและน้ำตาลที่มากเกินความต้องการจะสะสมไว้ในร่างกายจนเกิดโรคอ้วน"
         "และฟันผุ"),
    Care("ดื่มน้ำเปล่าให้พอในแต่ละวัน",
         "น้ำเป็นส่วนประกอบของร่างกายและช่วยลำเลียงสารอาหารกับขับของเสียออกไป"),
    Care("กินอาหารให้เป็นเวลาและไม่กินจุบจิบทั้งวัน",
         "การกินเป็นเวลาทำให้ระบบย่อยอาหารทำงานเป็นจังหวะ "
         "และทำให้ควบคุมปริมาณอาหารที่ได้รับได้"),
)


@question_type(
    "body.own_diet_foundation",
    display_name={"th": "ความสำคัญของการได้รับสารอาหารครบถ้วน"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class OwnDietFoundation(QuestionType):
    """Why getting every nutrient group matters, in one's own case."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_foundation(
            rng, system="ร่างกายของตนเอง", cares=DIET_CARE,
            hint="โยงกลับไปที่หน้าที่ของสารอาหารกลุ่มนั้นในร่างกาย",
        ), BODY_TOPIC)


@question_type(
    "body.own_diet_fluency",
    display_name={"th": "ตรวจอาหารที่ตนเองรับประทานในหนึ่งวัน"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class OwnDietFluency(QuestionType):
    """Read a day's food record and say what it needs.

    ``ป.6/3``'s evidence clause is ``โดยการเลือกรับประทานอาหาร`` — conduct, so
    this set is ``standard_scope``. Judging a record is the closest an item gets.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DAY_RECORDS)
        others = [other.verdict for other in DAY_RECORDS
                  if other.verdict != item.verdict]
        rng.shuffle(others)
        return _body(
            stem=f"บันทึกอาหารหนึ่งวันของนักเรียนคนหนึ่งเป็นดังนี้ {item.record} "
                 f"ข้อใดสรุปและแนะนำได้เหมาะสมที่สุด",
            correct=item.verdict,
            wrongs=tuple(others[:3]),
            hint="ไล่ดูทีละกลุ่มว่าวันนี้ได้ข้าวหรือแป้ง เนื้อสัตว์ ผักผลไม้ "
                 "และน้ำครบหรือไม่ แล้วดูว่ามีอะไรมากเกินไปด้วยหรือเปล่า",
        )


@question_type(
    "body.own_diet_application",
    display_name={"th": "วิเคราะห์การเลือกรับประทานอาหารของตนเอง"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class OwnDietApplication(QuestionType):
    """Judge one's own eating, or advice about it, against what the body needs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, OWN_DIET_SCENARIOS,
            hint="ถามว่าได้สารอาหารครบทุกกลุ่มหรือไม่ และปริมาณเหมาะกับวัยและ"
                 "กิจกรรมของตนเองหรือไม่",
        ), BODY_TOPIC)
