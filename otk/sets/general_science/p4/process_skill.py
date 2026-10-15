"""ทักษะกระบวนการทางวิทยาศาสตร์ ป.4

วิทยาศาสตร์ทั่วไป · ป.4 · เสริมทักษะ
Indicators: —

IPST opens every primary science book with the process skills a learner uses
in it, and files them as บทนำ with no ตัวชี้วัด, as at ม.1. ป.4 is where the
basic skills are named and practised on things a child can see and handle:
observing, measuring, sorting, counting, recording, inferring and predicting.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_g4 import SUBJECT

PROVENANCE = Provenance("original")


PRIMARY_FOUR = {"th": "ป.4"}


PROCESS_SKILL_TOPIC = "ทักษะกระบวนการทางวิทยาศาสตร์"


OBSERVE = "การสังเกต"
MEASURE = "การวัด"
CLASSIFY = "การจำแนกประเภท"
NUMBERS = "การใช้จำนวน"
COMMUNICATE = "การจัดกระทำและสื่อความหมายข้อมูล"
INFER = "การลงความเห็นจากข้อมูล"
PREDICT = "การพยากรณ์"
SPACE_TIME = "การใช้ความสัมพันธ์ระหว่างสเปซกับเวลา"

SKILL_NAMES = (OBSERVE, MEASURE, CLASSIFY, NUMBERS, COMMUNICATE, INFER, PREDICT, SPACE_TIME)


#: (what a child does, the one skill it is). Two per skill, each an action a
#: ป.4 class really does, worded so the action itself decides the skill.
ACTIONS = (
    ("ใช้แว่นขยายส่องดูใบไม้ แล้วบันทึกว่าใบมีขนเล็ก ๆ และขอบใบหยัก", OBSERVE),
    ("ดมกลิ่นและจับผิวของผลส้ม แล้วบันทึกว่ามีกลิ่นหอมและผิวขรุขระ", OBSERVE),
    ("ใช้ไม้บรรทัดหาความยาวของใบไม้ได้ 12 เซนติเมตร", MEASURE),
    ("ใช้เทอร์มอมิเตอร์หาอุณหภูมิของน้ำในแก้วได้ 30 องศาเซลเซียส", MEASURE),
    ("แบ่งเมล็ดพืชที่เก็บมาออกเป็นกลุ่มเมล็ดใหญ่และกลุ่มเมล็ดเล็ก", CLASSIFY),
    ("แยกสัตว์ในภาพเป็นกลุ่มที่มีกระดูกสันหลังและกลุ่มที่ไม่มีกระดูกสันหลัง", CLASSIFY),
    ("นับจำนวนเมล็ดถั่วที่งอกในแต่ละวัน แล้วนำมาบวกกันเป็นจำนวนทั้งหมด", NUMBERS),
    ("นำความสูงของต้นไม้สามต้นมาบวกกันแล้วหารด้วยสามเพื่อหาค่าเฉลี่ย", NUMBERS),
    ("นำจำนวนต้นกล้าที่งอกในแต่ละวันมาเขียนเป็นตารางและแผนภูมิแท่ง", COMMUNICATE),
    ("เรียงอุณหภูมิที่วัดได้ในแต่ละวันแล้วเขียนเป็นกราฟเส้นให้เพื่อนอ่าน", COMMUNICATE),
    ("เห็นพื้นดินเปียกในตอนเช้า แล้วอธิบายว่าเมื่อคืนน่าจะมีฝนตก", INFER),
    ("เห็นผลมะม่วงมีรอยกัดเล็ก ๆ แล้วอธิบายว่าน่าจะมีกระรอกมากินผล", INFER),
    ("จากข้อมูลว่าต้นถั่วสูงขึ้นวันละ 2 เซนติเมตร คาดว่าอีก 3 วันต้นถั่วจะสูงเท่าใด", PREDICT),
    ("จากตารางที่ลูกบอลกระดอนต่ำลงทุกครั้ง คาดว่าครั้งต่อไปจะกระดอนสูงเท่าใด", PREDICT),
    ("บันทึกตำแหน่งดวงจันทร์ทุกชั่วโมง แล้วบอกว่าดวงจันทร์เคลื่อนจากทิศตะวันออกไปทิศตะวันตกตามเวลา", SPACE_TIME),
    ("บันทึกความยาวและทิศของเงาเสาธงทุกชั่วโมง แล้วบอกว่าเงาเปลี่ยนไปตามเวลาอย่างไร", SPACE_TIME),
)


@question_type(
    "sci.process_skill_p4_foundation",
    display_name={"th": "บอกทักษะกระบวนการทางวิทยาศาสตร์จากสิ่งที่ลงมือทำ"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillP4Foundation(QuestionType):
    """Name the basic skill a child is using, from one thing they do."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        action, skill = rng.choice(ACTIONS)
        return _labelled(
            stem=f"นักเรียน{action} นักเรียนใช้ทักษะกระบวนการทางวิทยาศาสตร์ข้อใดมากที่สุด",
            correct=skill,
            wrongs=tuple(name for name in SKILL_NAMES if name != skill),
            hint=("ถามว่านักเรียนกำลังเก็บข้อมูล (สังเกต วัด) จัดการข้อมูล (จำแนก ใช้จำนวน จัดกระทำ) "
                  "หรือคิดต่อจากข้อมูล (ลงความเห็น พยากรณ์)"),
            topic=PROCESS_SKILL_TOPIC,
        )


#: (what the senses took in, a reasonable inference from it), about one scene.
OBSERVATION_PAIRS = (
    ("มีผึ้งหลายตัวบินมาเกาะที่ดอกไม้สีเหลือง", "ดอกไม้สีเหลืองนี้มีน้ำหวานที่ผึ้งชอบ"),
    ("ใบของต้นไม้ในห้องมืดมีสีซีดกว่าต้นที่อยู่ริมหน้าต่าง", "ต้นไม้ในห้องมืดได้รับแสงไม่เพียงพอ"),
    ("แก้วน้ำแข็งที่วางบนโต๊ะมีหยดน้ำเกาะอยู่รอบนอกแก้ว", "ไอน้ำในอากาศกลายเป็นหยดน้ำเมื่อโดนแก้วเย็น"),
    ("สุนัขเห่าและกระดิกหางเมื่อเจ้าของเดินเข้ามาในบ้าน", "สุนัขดีใจที่เห็นเจ้าของกลับมาถึงบ้าน"),
    ("ขนมปังที่วางทิ้งไว้หลายวันมีจุดสีเขียวขึ้นบนผิว", "มีราขึ้นบนขนมปังเพราะวางไว้ในที่ชื้น"),
    ("ลูกบอลที่เตะออกไปกลิ้งช้าลงจนหยุดนิ่งบนสนามหญ้า", "หญ้าบนสนามทำให้ลูกบอลเคลื่อนที่ช้าลงจนหยุด"),
    ("ดินในกระถางมีสีเข้มและเปียกชื้นเมื่อใช้มือจับ", "เมื่อเช้ามีคนรดน้ำต้นไม้ในกระถางนี้"),
    ("หลอดไฟในห้องไม่สว่างเมื่อกดสวิตช์หลายครั้ง", "หลอดไฟในห้องนี้น่าจะขาดแล้ว"),
)


@question_type(
    "sci.process_skill_p4_fluency",
    display_name={"th": "แยกการสังเกตออกจากการลงความเห็นจากข้อมูล"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillP4Fluency(QuestionType):
    """Which sentence the senses recorded, and which already explains it.

    Wrong choices come from the other side of the distinction only, so a
    learner cannot answer by topic; both directions are asked.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(OBSERVATION_PAIRS))
        observed, inferred = OBSERVATION_PAIRS[index]
        others = rng.sample([pair for i, pair in enumerate(OBSERVATION_PAIRS) if i != index], 2)
        if rng.random() < 0.5:
            return _labelled(
                stem="ข้อใดเป็นการสังเกต ไม่ใช่การลงความเห็นจากข้อมูล",
                correct=observed,
                wrongs=(inferred, others[0][1], others[1][1]),
                hint="การสังเกตคือสิ่งที่ตา หู จมูก ลิ้น หรือผิวกายรับรู้ได้ตรง ๆ ไม่มีการบอกสาเหตุ",
                topic=PROCESS_SKILL_TOPIC,
            )
        return _labelled(
            stem="ข้อใดเป็นการลงความเห็นจากข้อมูล ไม่ใช่การสังเกต",
            correct=inferred,
            wrongs=(observed, others[0][0], others[1][0]),
            hint="การลงความเห็นคือการบอกสาเหตุหรือเหตุผลเพิ่มจากสิ่งที่สังเกตได้ โดยใช้ความรู้เดิม",
            topic=PROCESS_SKILL_TOPIC,
        )


class Animal(NamedTuple):
    name: str
    backbone: bool
    in_water: bool
    lays_eggs: bool
    feathers: bool


#: Animals whose answer to every criterion below is not in doubt at ป.4.
ANIMALS = (
    Animal("ปลาทู", True, True, True, False),
    Animal("ไก่", True, False, True, True),
    Animal("แมว", True, False, False, False),
    Animal("ผีเสื้อ", False, False, True, False),
    Animal("กุ้ง", False, True, True, False),
    Animal("ปลาโลมา", True, True, False, False),
    Animal("นกพิราบ", True, False, True, True),
    Animal("ปลาหมึก", False, True, True, False),
    Animal("สุนัข", True, False, False, False),
)


#: (the criterion as a learner would state it, the field it reads).
CRITERIA = (
    ("การมีกระดูกสันหลัง", "backbone"),
    ("ที่อยู่อาศัย คืออาศัยอยู่ในน้ำหรือบนบก", "in_water"),
    ("การออกลูก คือออกลูกเป็นไข่หรือออกลูกเป็นตัว", "lays_eggs"),
    ("การมีขนนกปกคลุมร่างกาย", "feathers"),
)


def _split(animals, field: str) -> frozenset[frozenset[str]]:
    return frozenset(frozenset(a.name for a in animals if getattr(a, field) == side)
                     for side in (True, False))


@question_type(
    "sci.process_skill_p4_application",
    display_name={"th": "หาเกณฑ์ที่ใช้จำแนกประเภทสัตว์"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillP4Application(QuestionType):
    """Two groups of animals are shown; say which criterion made them.

    The animals are drawn so that only the chosen criterion splits them this
    way: every other criterion would put at least one animal in another group.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        while True:
            animals = rng.sample(ANIMALS, 5)
            label, field = rng.choice(CRITERIA)
            split = _split(animals, field)
            if frozenset() in split:
                continue
            if all(_split(animals, other) != split for _, other in CRITERIA if other != field):
                break
        first = [a.name for a in animals if getattr(a, field)]
        second = [a.name for a in animals if not getattr(a, field)]
        if rng.random() < 0.5:
            first, second = second, first
        return _labelled(
            stem=(f"นักเรียนจำแนกสัตว์ออกเป็น 2 กลุ่ม กลุ่มที่ 1: {' '.join(first)} "
                  f"กลุ่มที่ 2: {' '.join(second)} นักเรียนใช้เกณฑ์ใดในการจำแนก"),
            correct=label,
            wrongs=tuple(other for other, _ in CRITERIA if other != label),
            hint="ลองใช้เกณฑ์แต่ละข้อแบ่งสัตว์ทีละตัว แล้วดูว่าเกณฑ์ใดแบ่งได้ตรงกับทั้งสองกลุ่ม",
            topic=PROCESS_SKILL_TOPIC,
        )
