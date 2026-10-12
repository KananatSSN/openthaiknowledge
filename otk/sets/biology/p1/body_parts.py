"""ส่วนต่าง ๆ ของสิ่งมีชีวิต

ชีวะ · ป.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.1/1

Sets moved here from: science_wave_b14.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import (
    BODY_PARTS_SCENARIOS,
    LIFE_TOPIC,
    PRIMARY_ONE,
    _labelled,
)

PROVENANCE = Provenance("original")


class Part(NamedTuple):
    """One body part: what it looks like and what it does."""
    group: str
    name: str
    look: str
    function: str


# All three groups the indicator names. Distractors are drawn within a group, so
# ใบ is never offered as an answer about a cat.
PARTS = (
    Part("มนุษย์", "ตา", "มีลักษณะกลม อยู่บนใบหน้าสองข้าง", "ใช้มองเห็นสิ่งต่าง ๆ รอบตัว"),
    Part("มนุษย์", "หู", "อยู่ด้านข้างของศีรษะทั้งสองข้าง", "ใช้ฟังเสียง"),
    Part("มนุษย์", "จมูก", "อยู่กลางใบหน้า มีรูสองรู", "ใช้หายใจและใช้ดมกลิ่น"),
    Part("มนุษย์", "มือ", "อยู่ปลายแขน มีนิ้วห้านิ้ว", "ใช้หยิบจับสิ่งของ"),
    Part("มนุษย์", "ปาก", "อยู่ใต้จมูก ภายในมีฟันและลิ้น", "ใช้กินอาหาร เคี้ยวอาหาร และใช้พูด"),
    Part("มนุษย์", "ขา", "เป็นส่วนที่ยาวอยู่ด้านล่างของลำตัว", "ใช้ยืนและใช้เดิน"),
    Part("สัตว์", "ปีกของนก", "แผ่ออกได้และมีขนปกคลุม", "ใช้บินไปในอากาศ"),
    Part("สัตว์", "ครีบของปลา", "เป็นแผ่นบาง ๆ อยู่ตามลำตัว", "ใช้ว่ายน้ำและช่วยทรงตัวในน้ำ"),
    Part("สัตว์", "หนวดของแมว", "เป็นเส้นแข็งยาวอยู่ข้างจมูก", "ใช้สัมผัสสิ่งของรอบตัว"),
    Part("สัตว์", "ขาของแมลง", "เป็นขาเล็ก ๆ หลายขาอยู่ที่ลำตัว", "ใช้เดินและใช้เกาะ"),
    Part("พืช", "ราก", "อยู่ใต้ดิน แตกแขนงเป็นเส้น ๆ", "ใช้ดูดน้ำและยึดต้นไว้กับดิน"),
    Part("พืช", "ลำต้น", "เป็นส่วนที่ตั้งขึ้นเหนือดิน", "ใช้ชูกิ่งและใบ และเป็นทางลำเลียงน้ำ"),
    Part("พืช", "ใบ", "เป็นแผ่นแบน ๆ สีเขียว", "ใช้สร้างอาหารให้แก่ต้นพืช"),
    Part("พืช", "ดอก", "มีกลีบสีสวยและมีกลิ่น", "เป็นส่วนที่ทำให้เกิดผลและเมล็ด"),
)


class Activity(NamedTuple):
    """One everyday activity and the parts that do it together."""
    name: str
    together: str


ACTIVITIES = (
    Activity("การรับประทานอาหาร", "มือหยิบอาหารเข้าปาก แล้วฟันในปากเคี้ยวให้ละเอียด"),
    Activity("การอ่านหนังสือออกเสียง", "ตามองตัวหนังสือ แล้วปากออกเสียงตามที่อ่าน"),
    Activity("การเดินข้ามถนน", "ตามองดูรถ หูฟังเสียงรถ แล้วขาก้าวเดินเมื่อปลอดภัย"),
    Activity("การเล่นฟุตบอล", "ตามองลูกบอล ขาวิ่งและเตะ และแขนช่วยทรงตัวไว้"),
    Activity("การล้างมือ", "มือทั้งสองข้างถูสบู่เข้าด้วยกัน และตามองว่าสะอาดแล้วหรือยัง"),
    Activity("การหยิบของที่อยู่สูง", "ตามองหาของ ขาเขย่งขึ้น และมือเอื้อมไปหยิบ"),
)


@question_type(
    "life.body_parts_foundation",
    display_name={"th": "ส่วนต่าง ๆ ของคน สัตว์ และพืช"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=LIFE_TOPIC,
)
class BodyPartsFoundation(QuestionType):
    """Name a part, say what it looks like, or say what it is for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(PARTS)
        others = [other for other in PARTS
                  if other.group == item.group and other.name != item.name]
        rng.shuffle(others)
        draw = rng.random()
        if draw < 0.34:
            return _labelled(
                stem=f"“{item.name}” ทำหน้าที่อะไร",
                correct=item.function,
                wrongs=tuple(other.function for other in others[:3]),
                hint="นึกถึงว่าเราใช้ส่วนนั้นทำอะไรในชีวิตประจำวัน",
                topic=LIFE_TOPIC,
            )
        if draw < 0.67:
            return _labelled(
                stem=f"“{item.name}” มีลักษณะอย่างไร",
                correct=item.look,
                wrongs=tuple(other.look for other in others[:3]),
                hint="นึกภาพส่วนนั้นว่าอยู่ตรงไหนและมีรูปร่างแบบใด",
                topic=LIFE_TOPIC,
            )
        return _labelled(
            stem=f"ส่วนใดของ{item.group}ทำหน้าที่{item.function}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกส่วนที่ทำหน้าที่นั้น",
            topic=LIFE_TOPIC,
        )


@question_type(
    "life.body_parts_fluency",
    display_name={"th": "ส่วนต่าง ๆ ของร่างกายทำงานร่วมกัน"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=LIFE_TOPIC,
)
class BodyPartsFluency(QuestionType):
    """Say which parts work together to do an activity.

    This is the second half of ``ป.1/1``, the one after ``รวมทั้ง``: not what one
    part does on its own, but what several parts do together.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ACTIVITIES)
        others = [other for other in ACTIVITIES if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ใน “{item.name}” ส่วนต่าง ๆ ของร่างกายทำงานร่วมกันอย่างไร",
                correct=item.together,
                wrongs=tuple(other.together for other in others[:3]),
                hint="นึกทีละขั้นว่าเราทำอะไรก่อนและใช้ส่วนใด แล้วทำอะไรต่อ",
                topic=LIFE_TOPIC,
            )
        return _labelled(
            stem=f"การที่{item.together} เป็นการทำกิจกรรมใด",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านให้จบว่าใช้ส่วนใดบ้าง แล้วนึกว่ากำลังทำอะไรอยู่",
            topic=LIFE_TOPIC,
        )


@question_type(
    "life.body_parts_application",
    display_name={"th": "ใช้ความรู้เรื่องส่วนต่าง ๆ ของสิ่งมีชีวิต"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=LIFE_TOPIC,
)
class BodyPartsApplication(QuestionType):
    """Explain an everyday observation by what the part is for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        question = scenario_question(
            rng, BODY_PARTS_SCENARIOS,
            hint="ถามตัวเองว่าส่วนนั้นมีหน้าที่อะไร แล้วถ้าไม่มีส่วนนั้นจะเป็นอย่างไร",
        )
        return GeneratedQuestion(
            stem=question.stem, correct=question.correct,
            distractors=question.distractors, topic=LIFE_TOPIC, hint=question.hint,
        )
