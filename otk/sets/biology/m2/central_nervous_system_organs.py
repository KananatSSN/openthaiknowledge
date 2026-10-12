"""อวัยวะในระบบประสาทส่วนกลาง

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/10

Sets moved here from: science_wave_b11.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import LEVEL, SUBJECT, TOPIC, labelled, scenario_question
from otk.sets._support.science_wave_b11 import NERVOUS_SCENARIOS

PROVENANCE = Provenance("original")


class NervePart(NamedTuple):
    """One organ of the central nervous system and what it controls."""
    name: str
    function: str


# ระบบประสาทส่วนกลาง only. The peripheral nerves are outside this indicator.
NERVE_PARTS = (
    NervePart("สมองส่วนหน้า",
              "ควบคุมความคิด ความจำ การเรียนรู้ และการเคลื่อนไหวที่อยู่ใต้อำนาจจิตใจ"),
    NervePart("สมองน้อย",
              "ควบคุมการทรงตัว และทำให้การเคลื่อนไหวเป็นไปอย่างราบรื่นและประสานกัน"),
    NervePart("ก้านสมอง",
              "ควบคุมการทำงานที่จำเป็นต่อชีวิตซึ่งอยู่นอกอำนาจจิตใจ "
              "เช่น การหายใจและการเต้นของหัวใจ"),
    NervePart("ไขสันหลัง",
              "เป็นทางผ่านของกระแสประสาทระหว่างสมองกับร่างกาย "
              "และเป็นศูนย์กลางของปฏิกิริยารีเฟล็กซ์"),
)


# Exactly the four organs above, so "which one controls this" is never a
# three-choice item and never needs an invented fifth option.
CONTROLLED = (
    ("การทรงตัวขณะเดินบนคานแคบ", "สมองน้อย"),
    ("การขี่จักรยานได้อย่างคล่องแคล่วโดยไม่เสียหลัก", "สมองน้อย"),
    ("การท่องบทกลอนที่จำไว้ได้", "สมองส่วนหน้า"),
    ("การตัดสินใจเลือกคำตอบหลังจากชั่งใจแล้ว", "สมองส่วนหน้า"),
    ("การเต้นของหัวใจขณะที่กำลังหลับ", "ก้านสมอง"),
    ("การหายใจที่เกิดขึ้นเองโดยไม่ต้องนึกถึง", "ก้านสมอง"),
    ("การกระตุกของขาทันทีเมื่อถูกเคาะที่เอ็นใต้หัวเข่า", "ไขสันหลัง"),
    ("การชักมือกลับทันทีก่อนที่จะรู้สึกเจ็บเมื่อแตะของร้อน", "ไขสันหลัง"),
    ("การยืนขาเดียวได้นานโดยไม่ล้ม", "สมองน้อย"),
    ("การเล่นสเก็ตบอร์ดโดยไม่เสียหลัก", "สมองน้อย"),
    ("การเดินลงบันไดโดยไม่สะดุด", "สมองน้อย"),
    ("การรับลูกบอลที่โยนมาได้ตรงมือ", "สมองน้อย"),
    ("การแก้โจทย์คณิตศาสตร์", "สมองส่วนหน้า"),
    ("การวางแผนเส้นทางไปโรงเรียน", "สมองส่วนหน้า"),
    ("การจำชื่อเพื่อนใหม่ในห้อง", "สมองส่วนหน้า"),
    ("การแต่งประโยคภาษาไทยขึ้นเอง", "สมองส่วนหน้า"),
    ("การวาดภาพตามจินตนาการ", "สมองส่วนหน้า"),
    ("การกลืนอาหารที่เกิดขึ้นเองหลังอาหารถึงคอ", "ก้านสมอง"),
    ("การไอเมื่อมีสิ่งแปลกปลอมในลำคอ", "ก้านสมอง"),
    ("การจามเมื่อฝุ่นเข้าจมูก", "ก้านสมอง"),
    ("การกะพริบตาเองเมื่อมีสิ่งของพุ่งเข้าหาตา", "ก้านสมอง"),
    ("การรักษาความดันเลือดให้คงที่ขณะนอนหลับ", "ก้านสมอง"),
    ("การยกเท้าหนีทันทีเมื่อเหยียบของแหลม", "ไขสันหลัง"),
    ("การงอแขนหนีทันทีเมื่อถูกเข็มตำนิ้ว", "ไขสันหลัง"),
    ("การกระตุกของเท้าเมื่อถูกเคาะที่เอ็นร้อยหวาย", "ไขสันหลัง"),
    ("การชักเท้ากลับทันทีเมื่อเหยียบถ่านร้อน", "ไขสันหลัง"),
    ("การชักมือกลับทันทีเมื่อถูกหนามตำ", "ไขสันหลัง"),
)


# Real parts that are not in the central nervous system, offered only as wrong choices.
ORGAN_DECOYS = ("ต่อมใต้สมอง", "เส้นประสาทที่แขนและขา")


FUNCTION_DECOYS = ("สร้างฮอร์โมนควบคุมการเจริญเติบโตของร่างกาย",
                   "สร้างเซลล์เม็ดเลือดแดงให้ร่างกาย")


@question_type(
    "body.nervous_organs_foundation",
    display_name={"th": "อวัยวะในระบบประสาทส่วนกลางและหน้าที่"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class NervousOrgansFoundation(QuestionType):
    """Name an organ's job, or the organ that does a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(NERVE_PARTS)
        others = [other for other in NERVE_PARTS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return labelled(
                stem=f"“{item.name}” ทำหน้าที่ใดในระบบประสาทส่วนกลาง",
                correct=item.function,
                wrongs=tuple(other.function for other in others) + FUNCTION_DECOYS,
                hint="แยกก่อนว่าหน้าที่นั้นอยู่ใต้อำนาจจิตใจหรือไม่ "
                     "และเกี่ยวกับการทรงตัวหรือไม่",
            )
        return labelled(
            stem=f"อวัยวะใดในระบบประสาทส่วนกลางทำหน้าที่{item.function}",
            correct=item.name,
            wrongs=tuple(other.name for other in others) + ORGAN_DECOYS,
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกอวัยวะที่ทำหน้าที่นั้นโดยตรง",
        )


@question_type(
    "body.nervous_control_fluency",
    display_name={"th": "อวัยวะที่ควบคุมการทำงานแต่ละอย่างของร่างกาย"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class NervousControlFluency(QuestionType):
    """Say which organ controls a named action.

    ``ม.2/10`` asks for the organs' part *in controlling the body's working*, and
    that is what this item asks: every choice is one of the four organs, so a
    learner who can only recite the list still has to decide.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        action, part = rng.choice(CONTROLLED)
        wrongs = [item.name for item in NERVE_PARTS if item.name != part]
        rng.shuffle(wrongs)
        return labelled(
            stem=f"“{action}” ถูกควบคุมโดยอวัยวะใดเป็นหลัก",
            correct=part,
            wrongs=tuple(wrongs),
            hint="ถามว่าการทำงานนั้นต้องคิดก่อนหรือไม่ เกี่ยวกับการทรงตัวหรือไม่ "
                 "และเกิดขึ้นเร็วจนสมองยังไม่ทันสั่งหรือไม่",
        )


@question_type(
    "body.nervous_application",
    display_name={"th": "วิเคราะห์การควบคุมร่างกายและผลของการบาดเจ็บทางระบบประสาท"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class NervousApplication(QuestionType):
    """Work back from what a patient can and cannot do to the organ involved."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, NERVOUS_SCENARIOS,
            hint="ดูว่าสิ่งใดยังทำได้และสิ่งใดทำไม่ได้ แล้วจึงหาอวัยวะที่รับผิดชอบ"
                 "เฉพาะสิ่งที่เสียไป",
        )
