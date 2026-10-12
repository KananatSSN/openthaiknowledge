"""แนวทางการเลือกรับประทานอาหาร

ชีวะ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.6/2

Sets moved here from: science_wave_b17.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import (
    BODY_TOPIC,
    FOOD_CHOICE_SCENARIOS,
    PRIMARY_SIX,
    _body,
)

PROVENANCE = Provenance("original")


class Guideline(NamedTuple):
    """One way of choosing food, and the reason behind it."""
    advice: str
    reason: str


# ป.6/2 names three things at once: ครบถ้วน, สัดส่วนที่เหมาะกับเพศและวัย, and
# ความปลอดภัย. Every guideline below belongs to one of the three.
GUIDELINES = (
    Guideline("กินอาหารให้ครบทุกประเภทในแต่ละวัน",
              "สารอาหารแต่ละประเภททำหน้าที่คนละอย่าง จึงแทนกันไม่ได้"),
    Guideline("กินข้าวหรือแป้งเป็นสัดส่วนมากที่สุด และกินอาหารรสหวานจัดหรือมันจัด"
              "แต่น้อย",
              "ร่างกายต้องการพลังงานจากคาร์โบไฮเดรตเป็นหลัก ส่วนน้ำตาลและไขมัน"
              "ที่มากเกินไปจะสะสมจนเกิดโรค"),
    Guideline("ปรับปริมาณอาหารให้เหมาะกับเพศ วัย และกิจกรรมของตนเอง",
              "คนที่กำลังเจริญเติบโตหรือใช้แรงมาก ต้องการพลังงานและโปรตีนมากกว่า"
              "คนที่ใช้แรงน้อย"),
    Guideline("เลือกอาหารที่ปรุงสุกใหม่และสะอาด",
              "อาหารที่ปรุงไม่สุกหรือทิ้งไว้นานมีเชื้อโรคเจริญอยู่ ทำให้ท้องเสียได้"),
    Guideline("อ่านฉลากและดูวันหมดอายุก่อนซื้ออาหารสำเร็จรูป",
              "ฉลากบอกทั้งวันหมดอายุและปริมาณน้ำตาล ไขมัน และโซเดียมที่ได้รับ"),
    Guideline("ดื่มน้ำสะอาดแทนน้ำหวานและน้ำอัดลม",
              "น้ำหวานให้น้ำตาลมากโดยไม่ให้สารอาหารอื่น ส่วนน้ำเปล่าให้สิ่งที่ร่างกาย"
              "ต้องการจริง ๆ"),
)


# (สถานการณ์, แนวทางที่ตรงกับสถานการณ์นั้น).
GUIDELINE_NEEDS = (
    ("นักเรียนกินแต่ข้าวกับหมูทอดทุกมื้อและไม่แตะผักเลย ควรปฏิบัติตามแนวทางใด",
     "กินอาหารให้ครบทุกประเภทในแต่ละวัน"),
    ("นักเรียนดื่มน้ำอัดลมวันละหลายกระป๋องและกินขนมหวานทุกวันจนน้ำหนักขึ้นเร็ว "
     "ควรปฏิบัติตามแนวทางใด",
     "กินข้าวหรือแป้งเป็นสัดส่วนมากที่สุด และกินอาหารรสหวานจัดหรือมันจัดแต่น้อย"),
    ("พี่ชายที่เป็นนักกีฬาและคุณยายที่นั่งอยู่บ้านทั้งวันกินอาหารปริมาณเท่ากันทุกมื้อ "
     "ควรปฏิบัติตามแนวทางใด",
     "ปรับปริมาณอาหารให้เหมาะกับเพศ วัย และกิจกรรมของตนเอง"),
    ("นักเรียนจะซื้ออาหารจากร้านที่วางอาหารทิ้งไว้กลางแดดตั้งแต่เช้า "
     "ควรปฏิบัติตามแนวทางใด",
     "เลือกอาหารที่ปรุงสุกใหม่และสะอาด"),
    ("นักเรียนกำลังเลือกซื้อนมกล่องในร้านสะดวกซื้อ ควรปฏิบัติตามแนวทางใด",
     "อ่านฉลากและดูวันหมดอายุก่อนซื้ออาหารสำเร็จรูป"),
    ("นักเรียนรู้สึกกระหายน้ำหลังเล่นกีฬา และมีทั้งน้ำเปล่ากับน้ำหวานให้เลือก "
     "ควรปฏิบัติตามแนวทางใด",
     "ดื่มน้ำสะอาดแทนน้ำหวานและน้ำอัดลม"),
)


@question_type(
    "body.food_choice_foundation",
    display_name={"th": "เหตุผลของแนวทางการเลือกรับประทานอาหาร"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class FoodChoiceFoundation(QuestionType):
    """Why each way of choosing food is worth following."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(GUIDELINES)
        others = [other for other in GUIDELINES if other.advice != item.advice]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _body(
                stem=f"เหตุใดจึงควร “{item.advice}”",
                correct=item.reason,
                wrongs=tuple(other.reason for other in others[:3]),
                hint="โยงกลับไปที่สารอาหารครบถ้วน สัดส่วนที่เหมาะสม "
                     "หรือความปลอดภัยของอาหาร",
            )
        return _body(
            stem=f"แนวทางใดอาศัยเหตุผลที่ว่า {item.reason}",
            correct=item.advice,
            wrongs=tuple(other.advice for other in others[:3]),
            hint="อ่านเหตุผลให้จบ แล้วจึงเลือกแนวทางที่ตรงกับเหตุผลนั้น",
        )


@question_type(
    "body.food_choice_fluency",
    display_name={"th": "เลือกแนวทางการรับประทานอาหารให้ตรงกับสถานการณ์"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class FoodChoiceFluency(QuestionType):
    """State the แนวทาง the situation calls for.

    ``ป.6/2``'s main verb is ``บอกแนวทาง``, so this is the set filed ``exact``.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        situation, advice = rng.choice(GUIDELINE_NEEDS)
        others = [item.advice for item in GUIDELINES if item.advice != advice]
        rng.shuffle(others)
        return _body(
            stem=situation, correct=advice, wrongs=tuple(others[:3]),
            hint="ระบุปัญหาในสถานการณ์ก่อนว่าเป็นเรื่องความครบถ้วน สัดส่วน "
                 "หรือความปลอดภัย",
        )


@question_type(
    "body.food_choice_application",
    display_name={"th": "วิเคราะห์การเลือกรับประทานอาหาร"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class FoodChoiceApplication(QuestionType):
    """Judge a claim or a habit against what the body actually needs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, FOOD_CHOICE_SCENARIOS,
            hint="ตรวจสามข้อ ได้สารอาหารครบหรือไม่ สัดส่วนเหมาะกับวัยหรือไม่ "
                 "และปลอดภัยหรือไม่",
        ), BODY_TOPIC)
