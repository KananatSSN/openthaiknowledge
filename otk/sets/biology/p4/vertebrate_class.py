"""กลุ่มของสัตว์มีกระดูกสันหลัง

ชีวะ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 1.3 ป.4/4

Sets moved here from: science_wave_b24.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import PRIMARY_FOUR
from otk.sets._support.science_wave_b23 import GROUP_TOPIC
from otk.sets._support.science_wave_b24 import CLASS_SCENARIOS

PROVENANCE = Provenance("original")


class Klass(NamedTuple):
    """One of the five vertebrate groups, its marks, and examples of it."""
    name: str
    marks: str
    examples: tuple[str, ...]


CLASSES = (
    Klass("กลุ่มปลา",
          "ผิวหนังมีเกล็ดปกคลุม หายใจด้วยเหงือก เคลื่อนที่ด้วยครีบ "
          "และวางไข่ในน้ำ",
          ("ปลาทู", "ปลานิล", "ปลาดุก", "ปลาฉลาม")),
    Klass("กลุ่มสัตว์สะเทินน้ำสะเทินบก",
          "ผิวหนังเปียกชื้นและไม่มีเกล็ด ตัวอ่อนอยู่ในน้ำและหายใจด้วยเหงือก "
          "เมื่อโตเต็มวัยขึ้นบกและหายใจด้วยปอดร่วมกับผิวหนัง",
          ("กบ", "เขียด", "คางคก", "อึ่งอ่าง")),
    Klass("กลุ่มสัตว์เลื้อยคลาน",
          "ผิวหนังแห้งและมีเกล็ดแข็งปกคลุม หายใจด้วยปอดตลอดชีวิต "
          "และวางไข่ที่มีเปลือกเหนียวบนบก",
          ("งู", "จิ้งจก", "เต่า", "จระเข้")),
    Klass("กลุ่มนก",
          "มีขนแบบขนนกปกคลุมลำตัว ปากเป็นจะงอยไม่มีฟัน ขาคู่หน้าเปลี่ยนไปเป็นปีก "
          "และวางไข่ที่มีเปลือกแข็ง",
          ("นกพิราบ", "ไก่", "เป็ด", "นกกระจอกเทศ")),
    Klass("กลุ่มสัตว์เลี้ยงลูกด้วยน้ำนม",
          "มีขนเป็นเส้นปกคลุมลำตัว มีต่อมน้ำนมสำหรับเลี้ยงลูก "
          "และส่วนใหญ่ออกลูกเป็นตัว",
          ("แมว", "ช้าง", "ค้างคาว", "โลมา")),
)


@question_type(
    "animal.vertebrate_class_foundation",
    display_name={"th": "ลักษณะเฉพาะของสัตว์มีกระดูกสันหลังแต่ละกลุ่ม"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class VertebrateClassFoundation(QuestionType):
    """Describe a group by what can be seen — the ``บรรยาย`` half of ``ป.4/4``."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CLASSES)
        others = [other for other in CLASSES if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"สัตว์ใน “{item.name}” มีลักษณะเฉพาะที่สังเกตได้อย่างไร",
                correct=item.marks,
                wrongs=tuple(other.marks for other in others[:3]),
                hint="ดูสิ่งที่สังเกตได้จากภายนอกก่อน คือผิวหนังหรือขน "
                     "แล้วจึงดูวิธีหายใจและการมีลูก",
                topic=GROUP_TOPIC,
            )
        return _labelled(
            stem=f"สัตว์มีกระดูกสันหลังกลุ่มใดมีลักษณะว่า {item.marks}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านลักษณะให้ครบทุกข้อ เพราะบางกลุ่มมีลักษณะข้อแรกเหมือนกัน",
            topic=GROUP_TOPIC,
        )


@question_type(
    "animal.vertebrate_class_fluency",
    display_name={"th": "ยกตัวอย่างสัตว์ในแต่ละกลุ่ม"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class VertebrateClassFluency(QuestionType):
    """Place an example in its group — the ``ยกตัวอย่าง`` half of ``ป.4/4``."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CLASSES)
        others = [other for other in CLASSES if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            example = rng.choice(item.examples)
            return _labelled(
                stem=f"“{example}” จัดอยู่ในสัตว์มีกระดูกสันหลังกลุ่มใด",
                correct=item.name,
                wrongs=tuple(other.name for other in others[:3]),
                hint="ดูที่ผิวหนังหรือขนที่ปกคลุมลำตัวเป็นอันดับแรก",
                topic=GROUP_TOPIC,
            )
        return _labelled(
            stem=f"สัตว์ในข้อใดอยู่ใน “{item.name}”",
            correct=rng.choice(item.examples),
            wrongs=tuple(rng.choice(other.examples) for other in others[:3]),
            hint="นึกถึงลักษณะเฉพาะของกลุ่มนั้น "
                 "แล้วตรวจว่าสัตว์ในตัวเลือกมีลักษณะนั้นครบหรือไม่",
            topic=GROUP_TOPIC,
        )


@question_type(
    "animal.vertebrate_class_application",
    display_name={"th": "วิเคราะห์กลุ่มของสัตว์มีกระดูกสันหลัง"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class VertebrateClassApplication(QuestionType):
    """Place an animal whose habitat or movement points the wrong way."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CLASS_SCENARIOS,
            hint="ที่อยู่อาศัยและวิธีเคลื่อนที่หลอกได้ "
                 "ให้ดูผิวหนัง วิธีหายใจ และการมีลูกเป็นหลัก",
        ), GROUP_TOPIC)
