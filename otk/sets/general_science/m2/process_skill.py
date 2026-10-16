"""ทักษะกระบวนการทางวิทยาศาสตร์ ม.2

วิทยาศาสตร์ทั่วไป · ม.2 · เสริมทักษะ
Indicators: —

Filed like the ม.1 unit (บทนำ, no ตัวชี้วัด). ม.2 adds the integrated skills a
class needs to run its own investigation: defining a term so it can be measured,
keeping every variable but one the same, and reading a relationship from data.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_g4 import SUBJECT

PROVENANCE = Provenance("original")


SECONDARY_TWO = {"th": "ม.2"}


PROCESS_SKILL_TOPIC = "ทักษะกระบวนการทางวิทยาศาสตร์"


class Definition(NamedTuple):
    """A term in an investigation and the operational definition that measures it.

    The wrongs are the three ways a definition fails to be operational: the
    dictionary meaning, a vague impression, and a measurement of something else.
    """
    context: str
    term: str
    operational: str
    wrongs: tuple[str, str, str]


DEFINITIONS = (
    Definition("ผลของปุ๋ยต่อการเจริญเติบโตของต้นถั่ว", "การเจริญเติบโตของต้นถั่ว",
               "ความสูงของต้นถั่วที่วัดจากผิวดินถึงยอดด้วยไม้บรรทัดทุก 2 วัน",
               ("การที่ต้นถั่วมีขนาดใหญ่ขึ้นและแข็งแรงขึ้นตามธรรมชาติของพืช",
                "ต้นถั่วที่ดูสวยงาม มีใบสีเขียวสดใส และไม่มีโรคแมลงรบกวน",
                "จำนวนครั้งที่รดน้ำต้นถั่วในหนึ่งสัปดาห์ตลอดการทดลอง")),
    Definition("ผลของอุณหภูมิน้ำต่อการละลายของน้ำตาล", "ความเร็วในการละลายของน้ำตาล",
               "เวลาที่น้ำตาล 5 กรัมละลายหมดในน้ำ 100 มิลลิลิตร จับเวลาด้วยนาฬิกาจับเวลา",
               ("การที่น้ำตาลหายไปในน้ำอย่างรวดเร็วจนมองไม่เห็นเม็ดน้ำตาลเลย",
                "ความหวานของน้ำเชื่อมที่ได้เมื่อชิมด้วยลิ้นหลังคนให้เข้ากัน",
                "อุณหภูมิของน้ำที่ใช้ละลายน้ำตาลในแต่ละชุดการทดลอง")),
    Definition("ผลของจำนวนรอบขดลวดต่อแม่เหล็กไฟฟ้า", "ความแรงของแม่เหล็กไฟฟ้า",
               "จำนวนคลิปหนีบกระดาษที่แม่เหล็กไฟฟ้าดูดติดขึ้นมาได้ในครั้งเดียว",
               ("ความสามารถของแม่เหล็กในการดึงดูดวัตถุที่ทำจากเหล็กเข้าหาตัว",
                "แม่เหล็กไฟฟ้าที่มีขนาดใหญ่ น้ำหนักมาก และดูน่าเกรงขาม",
                "จำนวนรอบของขดลวดที่พันรอบตะปูในแต่ละชุดการทดลอง")),
    Definition("ความเป็นกรดของน้ำจากแหล่งน้ำต่าง ๆ", "น้ำที่เป็นกรด",
               "น้ำที่ทำให้กระดาษลิตมัสสีน้ำเงินเปลี่ยนเป็นสีแดงเมื่อหยดลงไป",
               ("สารที่มีรสเปรี้ยว กัดกร่อนโลหะได้ และมีไฮโดรเจนเป็นองค์ประกอบ",
                "น้ำที่ดูขุ่น มีกลิ่นเหม็น และไม่น่าใช้ในชีวิตประจำวัน",
                "ปริมาตรของน้ำตัวอย่างที่เก็บมาจากแหล่งน้ำแต่ละแห่ง")),
    Definition("ผลของจำนวนถ่านไฟฉายต่อความสว่างของหลอดไฟ", "ความสว่างของหลอดไฟ",
               "ค่าที่อ่านได้จากเครื่องวัดความสว่างซึ่งวางห่างจากหลอดไฟ 1 เมตร",
               ("แสงที่ออกมาจากหลอดไฟซึ่งทำให้มองเห็นสิ่งต่าง ๆ รอบตัวได้",
                "หลอดไฟที่ดูสว่างจ้าจนรู้สึกแสบตาเมื่อมองตรง ๆ",
                "จำนวนถ่านไฟฉายที่ต่อเรียงกันในวงจรแต่ละชุด")),
    Definition("ผลของการออกกำลังกายต่อการหายใจ", "อัตราการหายใจ",
               "จำนวนครั้งที่หน้าอกยกขึ้นใน 1 นาที นับพร้อมจับเวลาด้วยนาฬิกาจับเวลา",
               ("กระบวนการที่ร่างกายนำแก๊สออกซิเจนเข้าไปใช้และขับคาร์บอนไดออกไซด์",
                "การหายใจแรงและถี่จนรู้สึกเหนื่อยหอบหลังออกกำลังกาย",
                "ระยะทางที่นักเรียนวิ่งได้ก่อนเริ่มนับการหายใจ")),
)


@question_type(
    "sci.process_skill_m2_foundation",
    display_name={"th": "กำหนดนิยามเชิงปฏิบัติการ"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillM2Foundation(QuestionType):
    """The definition that says how the term is measured in this investigation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DEFINITIONS)
        return _labelled(
            stem=(f"ในการทดลองเรื่อง{item.context} ข้อใดเป็นนิยามเชิงปฏิบัติการ"
                  f"ของ “{item.term}”"),
            correct=item.operational,
            wrongs=item.wrongs,
            hint=("นิยามเชิงปฏิบัติการบอกว่าจะวัดหรือสังเกตสิ่งนั้นอย่างไรในการทดลองนี้ "
                  "ไม่ใช่ความหมายทั่วไป และไม่ใช่การวัดสิ่งอื่น"),
            topic=PROCESS_SKILL_TOPIC,
        )


class Control(NamedTuple):
    """A variable that should be kept the same, with a proper and a stray value."""
    name: str
    kept: str
    stray: str


class Setup(NamedTuple):
    """A two-set investigation: what it changes, what it measures, what it keeps."""
    aim: str
    changed: str
    values: tuple[str, str]
    measured: str
    controls: tuple[Control, ...]


SETUPS = (
    Setup("ผลของชนิดปุ๋ยต่อความสูงของต้นผักบุ้ง", "ชนิดของปุ๋ย", ("ปุ๋ยหมัก", "ปุ๋ยเคมี"),
          "ความสูงของต้นผักบุ้ง",
          (Control("ปริมาณน้ำที่รดต่อวัน", "รดน้ำวันละ 50 มิลลิลิตร", "รดน้ำวันละ 100 มิลลิลิตร"),
           Control("ชนิดของดิน", "ปลูกในดินร่วน", "ปลูกในดินทราย"),
           Control("ปริมาณแสงที่ได้รับ", "วางกลางแดด", "วางในร่ม"))),
    Setup("ผลของอุณหภูมิน้ำต่อเวลาที่เม็ดฟู่ละลายหมด", "อุณหภูมิของน้ำ", ("น้ำ 30 องศาเซลเซียส", "น้ำ 60 องศาเซลเซียส"),
          "เวลาที่เม็ดฟู่ละลายหมด",
          (Control("ปริมาตรของน้ำ", "ใช้น้ำ 100 มิลลิลิตร", "ใช้น้ำ 200 มิลลิลิตร"),
           Control("จำนวนเม็ดฟู่", "ใส่เม็ดฟู่ 1 เม็ด", "ใส่เม็ดฟู่ 2 เม็ด"),
           Control("การคน", "ไม่คน", "คนตลอดเวลา"))),
    Setup("ผลของความสูงที่ปล่อยต่อความสูงที่ลูกบอลกระดอน", "ความสูงที่ปล่อยลูกบอล", ("ปล่อยจากที่สูง 50 เซนติเมตร", "ปล่อยจากที่สูง 100 เซนติเมตร"),
          "ความสูงที่ลูกบอลกระดอนขึ้น",
          (Control("ชนิดของลูกบอล", "ใช้ลูกเทนนิส", "ใช้ลูกปิงปอง"),
           Control("ชนิดของพื้น", "ปล่อยลงบนพื้นไม้", "ปล่อยลงบนพื้นปูน"),
           Control("วิธีปล่อยลูกบอล", "ปล่อยเฉย ๆ โดยไม่ออกแรงผลัก", "ออกแรงผลักลงเล็กน้อย"))),
    Setup("ผลของจำนวนรอบขดลวดต่อจำนวนคลิปที่แม่เหล็กไฟฟ้าดูดได้", "จำนวนรอบของขดลวด", ("พัน 20 รอบ", "พัน 40 รอบ"),
          "จำนวนคลิปที่ดูดได้",
          (Control("จำนวนถ่านไฟฉาย", "ต่อถ่าน 2 ก้อน", "ต่อถ่าน 4 ก้อน"),
           Control("ชนิดของแกน", "ใช้ตะปูเหล็กเป็นแกน", "ใช้แท่งไม้เป็นแกน"),
           Control("ขนาดของคลิป", "ใช้คลิปขนาดเล็ก", "ใช้คลิปขนาดใหญ่"))),
    Setup("ผลของสีกระป๋องต่ออุณหภูมิของน้ำที่ตากแดด", "สีของกระป๋อง", ("กระป๋องสีดำ", "กระป๋องสีขาว"),
          "อุณหภูมิของน้ำหลังตากแดด",
          (Control("ปริมาตรของน้ำ", "ใส่น้ำ 200 มิลลิลิตร", "ใส่น้ำ 400 มิลลิลิตร"),
           Control("เวลาที่ตากแดด", "ตากแดด 30 นาที", "ตากแดด 60 นาที"),
           Control("ขนาดของกระป๋อง", "ใช้กระป๋องขนาดเล็ก", "ใช้กระป๋องขนาดใหญ่"))),
)


@question_type(
    "sci.process_skill_m2_fluency",
    display_name={"th": "หาตัวแปรที่ไม่ได้ควบคุมในการทดลอง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillM2Fluency(QuestionType):
    """Two sets differ in the variable under test and, by mistake, in one more.

    The stray difference is drawn, so the same investigation can go wrong in
    any of its controls; the wrong choices are the variable under test, the
    one measured, and a control that was kept the same.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        setup = rng.choice(SETUPS)
        stray = rng.choice(setup.controls)
        kept = [c for c in setup.controls if c is not stray]

        def describe(value: str, second: bool) -> str:
            parts = [value] + [c.stray if (second and c is stray) else c.kept for c in setup.controls]
            return " ".join(parts)

        return _labelled(
            stem=(f"นักเรียนทดลองเรื่อง{setup.aim} โดยจัดชุดที่ 1: {describe(setup.values[0], False)} "
                  f"และชุดที่ 2: {describe(setup.values[1], True)} "
                  f"แล้ววัด{setup.measured} ข้อใดเป็นตัวแปรที่ควรควบคุมให้เหมือนกันแต่การทดลองนี้ไม่ได้ควบคุม"),
            correct=stray.name,
            wrongs=(setup.changed, setup.measured, rng.choice(kept).name),
            hint="เทียบชุดที่ 1 กับชุดที่ 2 ทีละอย่าง ควรต่างกันเพียงสิ่งที่ต้องการทดสอบเท่านั้น",
            topic=PROCESS_SKILL_TOPIC,
        )


class Relation(NamedTuple):
    """Two quantities in a straight-line relation, as a class would record them."""
    setup: str
    x_name: str
    x_unit: str
    y_name: str
    y_unit: str
    xs: tuple[int, int, int, int]
    start: tuple[int, int]
    slope: tuple[int, int]


RELATIONS = (
    Relation("นักเรียนแขวนถุงทรายมวลต่าง ๆ กับสปริงตัวเดิม", "มวลที่แขวน", "กรัม",
             "ความยาวที่สปริงยืดออก", "เซนติเมตร", (100, 200, 300, 400), (0, 0), (1, 3)),
    Relation("นักเรียนให้ความร้อนแก่น้ำในบีกเกอร์ด้วยเตาที่ให้ความร้อนคงที่", "เวลาที่ให้ความร้อน", "นาที",
             "อุณหภูมิของน้ำ", "องศาเซลเซียส", (2, 4, 6, 8), (24, 30), (3, 6)),
    Relation("นักเรียนจับเวลารถของเล่นที่เคลื่อนที่ด้วยอัตราเร็วคงที่", "เวลา", "วินาที",
             "ระยะทางที่รถเคลื่อนที่ได้", "เซนติเมตร", (2, 4, 6, 8), (0, 0), (10, 25)),
)


@question_type(
    "sci.process_skill_m2_application",
    display_name={"th": "อ่านความสัมพันธ์จากข้อมูลแล้วประมาณค่า"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillM2Application(QuestionType):
    """A straight-line record; estimate y halfway between two readings or past the last."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rel = rng.choice(RELATIONS)
        start = rng.randint(*rel.start)
        gap = rel.xs[1] - rel.xs[0]
        between = rng.random() < 0.5
        steps = range(rel.slope[0], rel.slope[1] + 1)
        # Change in y per x step. Between two readings it must be even, so the
        # estimate halfway is still a whole number.
        per_step = rng.choice([v for v in steps if v % 2 == 0] if between else list(steps))
        ys = [start + per_step * (x // gap) for x in rel.xs]
        table = " / ".join(f"{x} {rel.x_unit}: {y} {rel.y_unit}" for x, y in zip(rel.xs, ys))
        if between:
            i = rng.randrange(3)
            x = rel.xs[i] + gap // 2
            answer = ys[i] + per_step // 2
        else:
            ahead = rng.choice((1, 2))
            x = rel.xs[-1] + gap * ahead
            answer = ys[-1] + per_step * ahead
        return numeric(
            stem=(f"{rel.setup} บันทึก{rel.x_name}กับ{rel.y_name}ได้ดังนี้ {table} "
                  f"ถ้าความสัมพันธ์ยังเป็นแบบเดิม เมื่อ{rel.x_name} {x} {rel.x_unit} "
                  f"{rel.y_name}น่าจะเป็นเท่าใด"),
            answer=answer,
            # The nearest recorded value instead of an estimate, and one step off either way.
            wrongs=(min(ys, key=lambda y: abs(y - answer)), answer + per_step, answer - per_step),
            unit=rel.y_unit,
            hint=f"หาก่อนว่า{rel.y_name}เปลี่ยนไปเท่าใดเมื่อ{rel.x_name}เพิ่มขึ้นหนึ่งช่วง แล้วใช้อัตรานั้นประมาณค่าที่ถาม",
            topic=PROCESS_SKILL_TOPIC,
        )
