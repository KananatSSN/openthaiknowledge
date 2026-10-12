"""การนำวิธีการแยกสารไปแก้ปัญหา

เคมี · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.2/3

Sets moved here from: science_wave_d9.
"""

from __future__ import annotations

from decimal import Decimal
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d9 import SECONDARY_TWO

PROVENANCE = Provenance("original")


SEPARATION_TOPIC = "การนำวิธีการแยกสารไปแก้ปัญหา"


EVAPORATE = "การระเหยแห้ง"


CRYSTALLISE = "การตกผลึก"


DISTIL = "การกลั่นอย่างง่าย"


CHROMATOGRAPHY = "โครมาโทกราฟีแบบกระดาษ"


EXTRACT = "การสกัดด้วยตัวทำละลาย"


PRINCIPLE = {
    EVAPORATE: "ทำให้ตัวทำละลายระเหยไปจนหมด เหลือตัวละลายที่เป็นของแข็ง",
    CRYSTALLISE: "ทำให้สารละลายอิ่มตัวแล้วเย็นลง ตัวละลายแยกออกมาเป็นผลึกที่บริสุทธิ์",
    DISTIL: "ต้มให้ของเหลวกลายเป็นไอแล้วควบแน่นกลับ ได้ของเหลวที่แยกจากสารที่ระเหยยาก",
    CHROMATOGRAPHY: "ให้ตัวทำละลายพาสารเคลื่อนที่บนกระดาษ สารต่างชนิดเคลื่อนที่ได้ระยะต่างกัน",
    EXTRACT: "ใช้ตัวทำละลายที่ละลายสารที่ต้องการได้ดี ดึงสารนั้นออกมาจากของผสม",
}


class Problem(NamedTuple):
    problem: str
    method: str
    defensible: frozenset[str] = frozenset()


PROBLEMS = (
    Problem("ชาวบ้านต้องการผลิตเกลือจากน้ำทะเลให้ได้ปริมาณมากโดยใช้แดดและลม", EVAPORATE,
            frozenset({CRYSTALLISE})),
    Problem("ลูกเรือกลางทะเลต้องการทำน้ำดื่มจากน้ำทะเล", DISTIL),
    Problem("นักวิทยาศาสตร์อาหารต้องการตรวจว่าลูกอมสีแดงมีสีผสมอาหารกี่ชนิดปนกันอยู่", CHROMATOGRAPHY),
    Problem("แม่ค้าต้องการสีเขียวจากใบเตยมาใช้แต่งสีขนม", EXTRACT),
    Problem("โรงงานต้องการทำจุนสีให้บริสุทธิ์เป็นเม็ดผลึกสีฟ้าสวยจากสารละลายที่มีสิ่งเจือปนเล็กน้อย", CRYSTALLISE),
    Problem("ต้องการเก็บสารหอมจากดอกมะลิโดยแช่ดอกในตัวทำละลายที่เหมาะสม", EXTRACT),
    Problem("นักเรียนต้องการน้ำบริสุทธิ์จากน้ำประปาเพื่อใช้ในการทดลอง", DISTIL),
    Problem("ตำรวจต้องการเปรียบเทียบหมึกบนเอกสารปลอมกับหมึกของปากกาที่ยึดได้", CHROMATOGRAPHY),
    Problem("ต้องการน้ำตาลทรายเม็ดใสที่บริสุทธิ์จากน้ำอ้อยที่กรองแล้ว", CRYSTALLISE, frozenset({EVAPORATE})),
    Problem("ต้องการสกัดน้ำมันออกจากเมล็ดถั่วเหลืองด้วยเฮกเซน", EXTRACT),
)


def _solution(method: str) -> str:
    return f"ใช้{method} เพราะ{PRINCIPLE[method]}"


SEPARATION_SCENARIOS = (
    ("น้ำทะเลมีเกลือละลายอยู่ประมาณร้อยละ 3 โดยมวล ถ้าระเหยน้ำทะเล 500 กิโลกรัมจนแห้ง จะได้เกลือประมาณกี่กิโลกรัม",
     "15 กิโลกรัม",
     ("3 กิโลกรัม", "150 กิโลกรัม", "1.5 กิโลกรัม", "30 กิโลกรัม", "485 กิโลกรัม")),
    ("นักเรียนออกแบบเครื่องกลั่นน้ำพลังงานแสงอาทิตย์จากกล่องพลาสติกใส ส่วนใดของการออกแบบสำคัญที่สุดต่อการได้น้ำจืด",
     "มีผิวเอียงที่เย็นกว่าให้ไอน้ำควบแน่น และมีรางรองรับหยดน้ำที่ไหลลงมาแยกจากน้ำเค็ม",
     ("ทาสีกล่องทั้งหมดให้ทึบเพื่อไม่ให้แสงเข้า",
      "ใส่เกลือเพิ่มลงในน้ำเค็มเพื่อให้ระเหยเร็วขึ้น",
      "ให้หยดน้ำที่ควบแน่นไหลกลับลงไปในน้ำเค็ม",
      "ปิดกล่องทุกด้านด้วยวัสดุทึบไม่ให้แสงเข้า",
      "วางกล่องไว้ในที่ร่มตลอดวันเพื่อให้น้ำเย็น")),
    ("ผลโครมาโทกราฟีของหมึกปากกา ก แยกได้ 3 แถบสี ส่วนหมึกที่พบบนเอกสารปลอมแยกได้ 3 แถบสีที่ระยะเดียวกันทุกแถบ ข้อสรุปใดเหมาะสมที่สุด",
     "หมึกบนเอกสารน่าจะมาจากปากกาชนิดเดียวกับปากกา ก",
     ("หมึกบนเอกสารไม่ใช่หมึกจากปากกา ก แน่นอน",
      "หมึกทั้งสองมีสีเดียวในส่วนผสม",
      "โครมาโทกราฟีใช้เปรียบเทียบหมึกไม่ได้",
      "หมึกบนเอกสารมีสารสีมากกว่าหมึกปากกา ก",
      "ต้องใช้การกลั่นแทนจึงจะเปรียบเทียบหมึกได้")),
)


def salt_from_seawater(rng: Random) -> GeneratedQuestion:
    """Salt left when seawater of a given percentage is evaporated to dryness."""
    percent = Decimal(rng.choice(("3", "3.5", "4")))
    mass = rng.choice((200, 400, 500, 1000, 2000))
    answer = percent * mass / 100
    pool = (percent * mass / 10, percent, percent * mass / 1000, answer * 2, mass - answer)
    fmt_kg = lambda value: f"{value.normalize():f} กิโลกรัม"
    return _labelled(
        stem=(f"น้ำทะเลมีเกลือละลายอยู่ประมาณร้อยละ {percent} โดยมวล ถ้าระเหยน้ำทะเล {mass:,} กิโลกรัมจนแห้ง "
              "จะได้เกลือประมาณกี่กิโลกรัม"),
        correct=fmt_kg(answer),
        wrongs=tuple(dict.fromkeys(fmt_kg(w) for w in pool if w != answer)),
        hint="มวลเกลือ = ร้อยละโดยมวล × มวลน้ำทะเล ÷ 100",
        topic=SEPARATION_TOPIC,
    )


@question_type(
    "chem.separation_problem_foundation",
    display_name={"th": "บอกหลักการของวิธีแยกสารแต่ละวิธี"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=SEPARATION_TOPIC,
)
class SeparationProblemFoundation(QuestionType):
    """One separation method; the principle it works by."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        method = rng.choice(tuple(PRINCIPLE))
        others = [m for m in PRINCIPLE if m != method]
        if rng.random() < 0.5:
            return _labelled(
                stem=f"วิธีแยกสารใดใช้หลักการ \"{PRINCIPLE[method]}\"",
                correct=method,
                wrongs=tuple(others),
                hint="นึกว่าวิธีนี้ใช้สมบัติใดของสารในการแยก: การระเหย จุดเดือด การละลาย หรือการเคลื่อนที่บนกระดาษ",
                topic=SEPARATION_TOPIC,
            )
        return _labelled(
            stem=f"ข้อใดเป็นหลักการของ{method}",
            correct=PRINCIPLE[method],
            wrongs=tuple(PRINCIPLE[m] for m in rng.sample(others, 3)),
            hint="นึกว่าวิธีนี้ใช้สมบัติใดของสารในการแยก: การระเหย จุดเดือด การละลาย หรือการเคลื่อนที่บนกระดาษ",
            topic=SEPARATION_TOPIC,
        )


@question_type(
    "chem.separation_problem_fluency",
    display_name={"th": "นำวิธีการแยกสารไปใช้แก้ปัญหาในชีวิตประจำวัน"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=SEPARATION_TOPIC,
)
class SeparationProblemFluency(QuestionType):
    """A problem; the separation method that solves it, with its principle."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        problem = rng.choice(PROBLEMS)
        others = [m for m in PRINCIPLE if m != problem.method and m not in problem.defensible]
        return _labelled(
            stem=f"{problem.problem} ควรใช้วิธีแยกสารใดแก้ปัญหานี้ เพราะเหตุใด",
            correct=_solution(problem.method),
            wrongs=tuple(_solution(m) for m in rng.sample(others, 3)),
            hint="ระบุก่อนว่าสารที่ต้องการอยู่ในรูปใดและต่างจากสารอื่นอย่างไร แล้วเลือกวิธีที่ใช้ความต่างนั้น",
            topic=SEPARATION_TOPIC,
        )


@question_type(
    "chem.separation_problem_application",
    display_name={"th": "ออกแบบและคำนวณในการแก้ปัญหาด้วยการแยกสาร"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=SEPARATION_TOPIC,
)
class SeparationProblemApplication(QuestionType):
    """Salt from seawater by percentage, a solar still, and matching ink."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return salt_from_seawater(rng)
        return _retopic(scenario_question(
            rng, SEPARATION_SCENARIOS,
            hint="ใช้หลักการแยกสารร่วมกับการคำนวณหรือการออกแบบให้ใช้ได้จริง",
        ), SEPARATION_TOPIC)
