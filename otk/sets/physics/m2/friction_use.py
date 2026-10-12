"""การลดและเพิ่มแรงเสียดทาน

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/9

Sets moved here from: science_wave_d20.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d18 import SECONDARY_TWO

PROVENANCE = Provenance("original")


FRICTION_USE_TOPIC = "การลดและเพิ่มแรงเสียดทาน"


class Problem(NamedTuple):
    case: str
    change: str
    method: str


PROBLEMS = (
    Problem("บานพับประตูมีเสียงดังและเปิดปิดฝืด", "ลดแรงเสียดทาน", "หยอดน้ำมันหล่อลื่นที่บานพับ"),
    Problem("ผู้สูงอายุลื่นล้มในห้องน้ำที่พื้นเปียก", "เพิ่มแรงเสียดทาน", "ปูแผ่นยางกันลื่นที่มีผิวขรุขระบนพื้น"),
    Problem("ลิ้นชักไม้เลื่อนเข้าออกยาก", "ลดแรงเสียดทาน", "ถูเทียนไขที่รางลิ้นชักให้ผิวลื่นขึ้น"),
    Problem("รถจักรยานยนต์ลื่นไถลบนถนนที่มีทรายละเอียดขณะเบรก", "เพิ่มแรงเสียดทาน", "เปลี่ยนยางที่ดอกยางสึกเป็นยางที่มีดอกยางลึก"),
    Problem("ต้องเข็นตู้หนักข้ามห้องบ่อย ๆ", "ลดแรงเสียดทาน", "ติดล้อเลื่อนที่ขาตู้"),
    Problem("นักวิ่งลื่นบนลู่วิ่งในวันที่ฝนตก", "เพิ่มแรงเสียดทาน", "สวมรองเท้าวิ่งที่พื้นมีปุ่มยึดเกาะ"),
    Problem("โซ่จักรยานฝืดและมีเสียงดังขณะปั่น", "ลดแรงเสียดทาน", "หยอดน้ำมันหล่อลื่นที่โซ่"),
    Problem("ขวดโหลฝาเกลียวเปิดยากเพราะมือลื่น", "เพิ่มแรงเสียดทาน", "ใช้ผ้ายางกันลื่นจับฝาขณะบิด"),
    Problem("พรมเช็ดเท้าเลื่อนไถลบนพื้นกระเบื้องเมื่อเหยียบ", "เพิ่มแรงเสียดทาน", "รองใต้พรมด้วยแผ่นยางกันลื่น"),
    Problem("เพลาของล้อรถเข็นสึกหรอเร็วเพราะหมุนเสียดสีกัน", "ลดแรงเสียดทาน", "ใส่ตลับลูกปืนที่เพลาล้อ"),
    Problem("บันไดคอนกรีตหน้าบ้านลื่นเมื่อฝนตก", "เพิ่มแรงเสียดทาน", "ติดแถบกันลื่นผิวขรุขระที่ขอบขั้นบันได"),
    Problem("ประตูบานเลื่อนกระจกเลื่อนยากเพราะรางมีฝุ่นสะสม", "ลดแรงเสียดทาน", "ทำความสะอาดรางแล้วหยอดสารหล่อลื่น"),
    Problem("ไม้เทนนิสหลุดมือบ่อยเพราะเหงื่อ", "เพิ่มแรงเสียดทาน", "พันด้ามจับด้วยกริปที่ซับเหงื่อ"),
    Problem("ต้องลากเรือเล็กขึ้นฝั่งทรายบ่อย ๆ", "ลดแรงเสียดทาน", "วางท่อนไม้กลมใต้เรือให้กลิ้งแทนการลาก"),
    Problem("รถยนต์ติดหล่มโคลนลื่นเพราะล้อหมุนฟรี", "เพิ่มแรงเสียดทาน", "รองใต้ล้อด้วยแผ่นไม้หรือกิ่งไม้"),
    Problem("นักสกีไถลบนหิมะได้ช้าเพราะแผ่นสกีฝืด", "ลดแรงเสียดทาน", "ลงแว็กซ์ที่ใต้แผ่นสกี"),
)


USEFUL_FRICTION = ("แรงเสียดทานระหว่างพื้นรองเท้ากับพื้นขณะเดิน", "แรงเสียดทานระหว่างยางรถกับถนนขณะเบรก",
                   "แรงเสียดทานระหว่างมือกับไม้ขณะปีนต้นไม้", "แรงเสียดทานระหว่างไม้ขีดไฟกับข้างกลักจนติดไฟ",
                   "แรงเสียดทานระหว่างปากกากับกระดาษขณะเขียน", "แรงเสียดทานที่ทำให้ตะปูยึดอยู่ในเนื้อไม้",
                   "แรงเสียดทานระหว่างผ้าเบรกกับจานเบรกจักรยาน", "แรงเสียดทานระหว่างเชือกกับมือขณะชักเย่อ")


HARMFUL_FRICTION = ("แรงเสียดทานในข้อต่อเครื่องจักรที่ทำให้สึกหรอ", "แรงเสียดทานระหว่างลิ้นชักกับรางที่ทำให้ฝืด",
                    "แรงเสียดทานที่บานพับประตูทำให้มีเสียงดัง", "แรงเสียดทานในเครื่องยนต์ที่ทำให้เกิดความร้อนสูญเปล่า",
                    "แรงเสียดทานของอากาศที่ทำให้รถสิ้นเปลืองน้ำมัน", "แรงเสียดทานที่ทำให้พื้นรองเท้าสึกเร็ว",
                    "แรงเสียดทานที่โซ่จักรยานแห้งทำให้ปั่นหนัก", "แรงเสียดทานที่ทำให้ยางรถสึกหรอ")


def _proposal(change: str, method: str) -> str:
    return f"ควร{change} โดย{method}"


FRICTION_USE_SCENARIOS = (
    ("ข้อใดเป็นแรงเสียดทานที่เป็นประโยชน์ และไม่ควรลดลง",
     "แรงเสียดทานระหว่างพื้นรองเท้ากับพื้นขณะเดิน",
     ("แรงเสียดทานในข้อต่อเครื่องจักรที่ทำให้สึกหรอ", "แรงเสียดทานระหว่างลิ้นชักกับรางที่ทำให้ฝืด", "แรงเสียดทานที่บานพับประตูทำให้มีเสียงดัง")),
    ("เหตุใดนักโบว์ลิ่งจึงทาน้ำมันบนลานโบว์ลิ่งบางส่วน แต่รองเท้าโบว์ลิ่งมีพื้นยางที่ส้นข้างหนึ่ง",
     "ลานที่ลื่นช่วยให้ลูกไถลได้ไกล ส่วนพื้นยางช่วยเพิ่มแรงเสียดทานให้ผู้เล่นหยุดตัวได้",
     ("ทั้งสองอย่างช่วยลดแรงเสียดทาน", "ทั้งสองอย่างช่วยเพิ่มแรงเสียดทาน", "น้ำมันทำให้ลูกหนักขึ้น")),
    ("ถ้ารางเลื่อนประตูบานเลื่อนมีแรงเสียดทาน 40 นิวตัน หลังหยอดน้ำมันลดลงร้อยละ 75 จะเหลือแรงเสียดทานเท่าใด",
     "10 นิวตัน", ("30 นิวตัน", "75 นิวตัน", "35 นิวตัน")),
)


@question_type(
    "phys.friction_use_foundation",
    display_name={"th": "จำแนกวิธีลดและเพิ่มแรงเสียดทาน"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_USE_TOPIC,
)
class FrictionUseFoundation(QuestionType):
    """A method; whether it reduces or increases friction, or which method does one of them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            change = rng.choice(("ลดแรงเสียดทาน", "เพิ่มแรงเสียดทาน"))
            right = rng.choice([p.method for p in PROBLEMS if p.change == change])
            return _labelled(
                stem=f"ข้อใดเป็นวิธี{change}",
                correct=right,
                wrongs=tuple([p.method for p in PROBLEMS if p.change != change]),
                hint="ผิวลื่น ล้อ ลูกปืน และสารหล่อลื่นลดแรงเสียดทาน ผิวขรุขระ ยาง และดอกยางเพิ่มแรงเสียดทาน",
                topic=FRICTION_USE_TOPIC,
            )
        problem = rng.choice(PROBLEMS)
        other = "เพิ่มแรงเสียดทาน" if problem.change == "ลดแรงเสียดทาน" else "ลดแรงเสียดทาน"
        return _labelled(
            stem=f"\"{problem.method}\" เป็นวิธีใด",
            correct=problem.change,
            wrongs=(other, "ไม่เกี่ยวกับแรงเสียดทาน", "เพิ่มน้ำหนักของวัตถุ"),
            hint="ผิวลื่น ล้อ และสารหล่อลื่นลดแรงเสียดทาน ผิวขรุขระและดอกยางเพิ่มแรงเสียดทาน",
            topic=FRICTION_USE_TOPIC,
        )


@question_type(
    "phys.friction_use_fluency",
    display_name={"th": "วิเคราะห์สถานการณ์และเสนอแนะวิธีลดหรือเพิ่มแรงเสียดทาน"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_USE_TOPIC,
)
class FrictionUseFluency(QuestionType):
    """A problem; whether friction should go down or up, and how."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(PROBLEMS))
        problem = PROBLEMS[index]
        other = "เพิ่มแรงเสียดทาน" if problem.change == "ลดแรงเสียดทาน" else "ลดแรงเสียดทาน"
        opposite = rng.choice([p for p in PROBLEMS if p.change == other])
        return _labelled(
            stem=f"{problem.case} ข้อใดวิเคราะห์และเสนอแนะแนวทางแก้ปัญหาได้เหมาะสมที่สุด",
            correct=_proposal(problem.change, problem.method),
            wrongs=(_proposal(other, problem.method),
                    _proposal(other, opposite.method),
                    _proposal(problem.change, "ทาสีใหม่ให้สวยงาม")),
            hint="ถามก่อนว่าปัญหาเกิดจากแรงเสียดทานมากเกินไปหรือน้อยเกินไป แล้วเลือกวิธีที่เปลี่ยนไปทางนั้น",
            topic=FRICTION_USE_TOPIC,
        )


@question_type(
    "phys.friction_use_application",
    display_name={"th": "ชั่งประโยชน์และโทษของแรงเสียดทานในสถานการณ์จริง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_USE_TOPIC,
)
class FrictionUseApplication(QuestionType):
    """Authored cases, useful or harmful friction, and what oiling leaves."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            useful = rng.random() < 0.5
            right_pool, wrong_pool = (USEFUL_FRICTION, HARMFUL_FRICTION) if useful else (HARMFUL_FRICTION, USEFUL_FRICTION)
            return _labelled(
                stem=("ข้อใดเป็นแรงเสียดทานที่เป็นประโยชน์ และไม่ควรลดลง" if useful
                      else "ข้อใดเป็นแรงเสียดทานที่เป็นโทษ และควรหาทางลดลง"),
                correct=rng.choice(right_pool), wrongs=tuple(wrong_pool),
                hint="แรงเสียดทานมีทั้งประโยชน์และโทษ เลือกลดหรือเพิ่มตามสิ่งที่งานนั้นต้องการ",
                topic=FRICTION_USE_TOPIC,
            )
        if roll < 0.7:
            before = rng.randrange(20, 201, 20)
            percent = rng.choice((25, 50, 75))
            left = before * (100 - percent) // 100
            return numeric(
                stem=(f"รางเลื่อนมีแรงเสียดทาน {before} นิวตัน หลังหยอดน้ำมันหล่อลื่น แรงเสียดทานลดลงร้อยละ {percent} "
                      "จะเหลือแรงเสียดทานเท่าใด"),
                answer=left, wrongs=(before - left, before - percent, before * percent // 100 + before),
                unit="นิวตัน", topic=FRICTION_USE_TOPIC,
                hint="แรงที่เหลือ = แรงเดิม × (100 − ร้อยละที่ลดลง) ÷ 100",
            )
        return _retopic(scenario_question(
            rng, FRICTION_USE_SCENARIOS,
            hint="แรงเสียดทานมีทั้งประโยชน์และโทษ เลือกลดหรือเพิ่มตามสิ่งที่งานนั้นต้องการ",
        ), FRICTION_USE_TOPIC)
