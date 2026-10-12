"""สัตว์มีกระดูกสันหลังและสัตว์ไม่มีกระดูกสันหลัง

ชีวะ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 1.3 ป.4/3

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
from otk.sets._support.science_wave_b24 import VERTEBRATE_SCENARIOS

PROVENANCE = Provenance("original")


class Animal(NamedTuple):
    """An animal, which of the two groups it is in, and the reason."""
    name: str
    group: str
    because: str


BACKBONE = (
    Animal("ปลาทู", "สัตว์มีกระดูกสันหลัง",
           "มีกระดูกสันหลังเป็นแกนกลางลำตัวอยู่ภายใน ต่อจากกะโหลกไปถึงหาง"),
    Animal("กบ", "สัตว์มีกระดูกสันหลัง",
           "มีกระดูกสันหลังอยู่ภายในลำตัวที่ค้ำจุนร่างกายและต่อกับขาทั้งสี่"),
    Animal("งูเหลือม", "สัตว์มีกระดูกสันหลัง",
           "มีกระดูกสันหลังเรียงต่อกันเป็นข้อ ๆ ตลอดลำตัวจึงเลื้อยได้"),
    Animal("นกพิราบ", "สัตว์มีกระดูกสันหลัง",
           "มีกระดูกสันหลังอยู่ภายใน และมีกระดูกอกที่ยึดกล้ามเนื้อสำหรับบิน"),
    Animal("แมว", "สัตว์มีกระดูกสันหลัง",
           "มีกระดูกสันหลังเป็นแกนกลางที่ค้ำจุนร่างกายให้ยืนและวิ่งได้"),
    Animal("ไส้เดือนดิน", "สัตว์ไม่มีกระดูกสันหลัง",
           "ลำตัวอ่อนนิ่มเป็นปล้อง ๆ ไม่มีกระดูกใด ๆ อยู่ภายในเลย"),
    Animal("ปูม้า", "สัตว์ไม่มีกระดูกสันหลัง",
           "มีเปลือกแข็งหุ้มอยู่ภายนอกแทนโครงร่างภายใน จึงไม่มีกระดูกสันหลัง"),
    Animal("หอยทาก", "สัตว์ไม่มีกระดูกสันหลัง",
           "ลำตัวอ่อนนิ่มและมีเปลือกแข็งอยู่ภายนอก ไม่มีกระดูกอยู่ภายใน"),
    Animal("ผีเสื้อ", "สัตว์ไม่มีกระดูกสันหลัง",
           "มีเปลือกแข็งหุ้มลำตัวไว้ภายนอก และไม่มีกระดูกสันหลังอยู่ภายใน"),
    Animal("แมงกะพรุน", "สัตว์ไม่มีกระดูกสันหลัง",
           "ลำตัวอ่อนนุ่มคล้ายวุ้นทั้งตัว ไม่มีโครงกระดูกส่วนใดเลย"),
)


# Wrong criteria and wrong contrasts, sampled three at a time.
CRITERION_DECOYS = (
    "ใช้การมีส่วนแข็งเป็นเกณฑ์ ไม่ว่าจะอยู่ภายในหรือภายนอก",
    "ใช้ขนาดของลำตัวเป็นเกณฑ์ โดยสัตว์ที่ใหญ่กว่าจัดเป็นสัตว์มีกระดูกสันหลัง",
    "ใช้ที่อยู่อาศัยเป็นเกณฑ์ โดยสัตว์บกมีกระดูกสันหลัง ส่วนสัตว์น้ำไม่มี",
    "ใช้จำนวนขาเป็นเกณฑ์ โดยสัตว์ที่มีสี่ขาจัดเป็นสัตว์มีกระดูกสันหลัง",
    "ใช้วิธีเคลื่อนที่เป็นเกณฑ์ โดยสัตว์ที่เลื้อยได้จัดเป็นสัตว์ไม่มีกระดูกสันหลัง",
    "ใช้ความนิ่มของผิวเป็นเกณฑ์ สัตว์ผิวนิ่มไม่มีกระดูกสันหลัง",
    "ใช้สีของผิวหนังเป็นเกณฑ์ ไม่เกี่ยวกับโครงร่างภายในลำตัว",
    "ใช้การมีขนหรือเกล็ดเป็นเกณฑ์ ไม่ดูโครงร่างภายในลำตัว",
)


SHELL_DECOYS = (
    "ทั้งสองอย่างเป็นกระดูกสันหลังเหมือนกัน ต่างกันเพียงที่ความแข็งและสีของผิวนอก",
    "เปลือกแข็งของปูอยู่ภายในลำตัว ส่วนกระดูกสันหลังของปลาอยู่ภายนอกใต้เกล็ด",
    "ทั้งสองอย่างไม่ใช่โครงร่างของร่างกาย แต่เป็นเพียงส่วนที่ใช้ป้องกันตัวจากศัตรู",
    "ทั้งสองอย่างอยู่ภายนอกลำตัว ต่างกันเพียงที่ปูมีเปลือกหนากว่าเกล็ดปลา",
    "เปลือกแข็งของปูเป็นกระดูกสันหลังที่แตกเป็นแผ่น ส่วนของปลาต่อกันเป็นข้อ",
)


@question_type(
    "animal.vertebrate_group_foundation",
    display_name={"th": "เกณฑ์การจำแนกสัตว์โดยใช้กระดูกสันหลัง"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class VertebrateGroupFoundation(QuestionType):
    """The criterion, and the confusion between inner and outer skeletons."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            return _labelled(
                stem="การจำแนกสัตว์ออกเป็นสัตว์มีกระดูกสันหลังและสัตว์ไม่มีกระดูก"
                     "สันหลัง ใช้สิ่งใดเป็นเกณฑ์",
                correct="ใช้การมีกระดูกสันหลังเป็นแกนกลางอยู่ภายในลำตัวเป็นเกณฑ์",
                wrongs=tuple(CRITERION_DECOYS),
                hint="เกณฑ์อยู่ในชื่อของกลุ่มอยู่แล้ว "
                     "และสิ่งสำคัญคือกระดูกนั้นอยู่ภายในลำตัว",
                topic=GROUP_TOPIC,
            )
        return _labelled(
            stem="เปลือกแข็งของปูกับกระดูกสันหลังของปลา ต่างกันอย่างไร",
            correct="เปลือกปูเป็นโครงร่างที่หุ้มภายนอก ส่วนกระดูกสันหลังของปลาเป็นแกนอยู่ภายในลำตัว",
            wrongs=tuple(SHELL_DECOYS),
            hint="ถามว่าส่วนแข็งนั้นอยู่ด้านในหรือด้านนอกของลำตัว",
            topic=GROUP_TOPIC,
        )


@question_type(
    "animal.vertebrate_group_fluency",
    display_name={"th": "จำแนกสัตว์โดยใช้กระดูกสันหลังเป็นเกณฑ์"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class VertebrateGroupFluency(QuestionType):
    """Sort an animal by the backbone criterion, with the reason."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(BACKBONE)
        other_group = ("สัตว์ไม่มีกระดูกสันหลัง"
                       if item.group == "สัตว์มีกระดูกสันหลัง"
                       else "สัตว์มีกระดูกสันหลัง")
        others = [other.because for other in BACKBONE
                  if other.group != item.group]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.name}” จัดอยู่ในกลุ่มใด และเพราะเหตุใด",
            correct=f"{item.group} เพราะ{item.because}",
            wrongs=(f"{other_group} เพราะ{others[0]}",
                    f"{other_group} เพราะ{others[1]}",
                    f"{item.group} เพราะเคลื่อนที่ได้เร็วกว่าสัตว์ในอีกกลุ่มหนึ่ง"),
            hint="นึกภาพว่าถ้าผ่าลำตัวออกดู จะพบแกนกระดูกอยู่ตรงกลางหรือไม่",
            topic=GROUP_TOPIC,
        )


@question_type(
    "animal.vertebrate_group_application",
    display_name={"th": "วิเคราะห์การจำแนกสัตว์ด้วยกระดูกสันหลัง"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class VertebrateGroupApplication(QuestionType):
    """Judge a sorting that used hardness or habitat instead of the criterion."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, VERTEBRATE_SCENARIOS,
            hint="ถามอย่างเดียวว่ามีแกนกระดูกอยู่ภายในลำตัวหรือไม่ "
                 "ไม่ใช่ว่าตัวแข็งหรือตัวนิ่ม",
        ), GROUP_TOPIC)
