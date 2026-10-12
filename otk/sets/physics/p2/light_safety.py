"""การป้องกันอันตรายจากแสงสว่างไม่เหมาะสม

ฟิสิกส์ · ป.2 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.2/2

Sets moved here from: science_wave_d22.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d22 import KIDS, SECOND

PROVENANCE = Provenance("original")


LIGHT_SAFETY_TOPIC = "การป้องกันอันตรายจากแสงสว่างไม่เหมาะสม"


class LightProblem(NamedTuple):
    case: str
    method: str


LIGHT_PROBLEMS = (
    LightProblem("อ่านหนังสือในที่แสงสลัวเป็นเวลานาน", "เปิดไฟหรือย้ายไปอ่านในที่ที่มีแสงสว่างเพียงพอ"),
    LightProblem("มองจอโทรศัพท์ที่สว่างจ้าในห้องมืดติดต่อกันนาน ๆ", "ลดความสว่างของจอหรือเปิดไฟห้องให้สว่างขึ้น"),
    LightProblem("มองดวงอาทิตย์โดยตรงด้วยตาเปล่า", "หลีกเลี่ยงการมองดวงอาทิตย์โดยตรง ใช้แว่นกรองแสงเฉพาะหากจำเป็น"),
    LightProblem("นั่งทำงานใต้แสงไฟที่จ้าจนแสบตา", "ใช้ฉากกั้นแสงหรือลดความสว่างของหลอดไฟ"),
    LightProblem("เดินกลางแดดจ้าที่ชายหาดตอนเที่ยง", "สวมแว่นกันแดดและหมวกปีกกว้างเพื่อลดแสงที่เข้าตา"),
    LightProblem("ใช้เลเซอร์พอยเตอร์เล่นกับเพื่อน", "ห้ามส่องแสงเลเซอร์เข้าตาตนเองหรือผู้อื่นเด็ดขาด"),
    LightProblem("ขับรถสวนกับรถที่เปิดไฟสูงตอนกลางคืน", "หลบสายตาไปทางขอบถนนด้านซ้ายชั่วครู่และลดความเร็ว"),
    LightProblem("เล่นเกมบนแท็บเล็ตติดต่อกันหลายชั่วโมง", "พักสายตาเป็นระยะโดยมองไปไกล ๆ และจำกัดเวลาใช้งาน"),
)


TOO_BRIGHT = ("แสงแดดจ้าสะท้อนจากผิวน้ำ", "แสงจากการเชื่อมโลหะ", "แสงแฟลชกล้องที่ยิงเข้าตาใกล้ ๆ", "แสงเลเซอร์ที่ส่องเข้าตา", "ไฟสูงของรถที่สวนมา")


TOO_DIM = ("แสงเทียนเล่มเดียวในห้องกว้าง", "แสงจากหน้าต่างเล็ก ๆ ตอนพลบค่ำ", "ห้องเรียนที่หลอดไฟเสียเกือบหมด", "ไฟหัวเตียงสีส้มดวงเล็ก", "ใต้ผ้าห่มที่ใช้ไฟจากโทรศัพท์")


SAFETY_HINT = "ทั้งแสงจ้าเกินไปและแสงสลัวเกินไปทำให้ดวงตาต้องทำงานหนักและอาจเป็นอันตราย ควรปรับแสงให้พอเหมาะ"


LIGHT_SAFETY_SCENARIOS = (
    ("นักเรียนคนหนึ่งนอนอ่านหนังสือโดยใช้แสงจากโทรศัพท์เพียงอย่างเดียวในห้องมืดทุกคืน ข้อใดแนะนำได้เหมาะสมที่สุด",
     "ควรเปิดไฟในห้องให้สว่างเพียงพอทุกครั้งที่อ่านหนังสือ ไม่ใช้แสงจอเพียงอย่างเดียวในที่มืด",
     ("ควรอ่านต่อไปได้ตามปกติเพราะแสงจากโทรศัพท์ไม่มีผลต่อดวงตา", "ควรปิดจอแล้วอ่านหนังสือในที่มืดสนิท เพราะไม่มีแสงเลยจะปลอดภัยต่อดวงตามากกว่า", "ควรเพิ่มความสว่างของจอโทรศัพท์ให้มากที่สุด แล้วอ่านต่อในที่มืดได้ตามต้องการ")),
    ("ช่างเชื่อมโลหะต้องสวมหน้ากากกันแสงพิเศษขณะทำงาน เหตุใดจึงจำเป็น",
     "แสงจากการเชื่อมโลหะจ้ามาก การมองโดยตรงเป็นเวลานานอาจทำอันตรายต่อดวงตาได้",
     ("เพื่อป้องกันฝุ่นและควันเพียงอย่างเดียว แสงจากการเชื่อมไม่มีผลต่อดวงตา", "แสงจากการเชื่อมโลหะไม่มีอันตรายต่อดวงตาเลย หน้ากากใช้กันสะเก็ดไฟเท่านั้น", "หน้ากากช่วยให้มองเห็นในที่มืดได้ชัดขึ้นเท่านั้น")),
    ("ห้องเรียนแห่งหนึ่งมีหลอดไฟเสียหลายดวงจนแสงสลัวมาก นักเรียนต้องเพ่งมองกระดานเป็นเวลานานทุกวัน ข้อใดเสนอแนะได้เหมาะสมที่สุด",
     "ควรแจ้งซ่อมหลอดไฟหรือเพิ่มแสงสว่างในห้องเรียนให้เพียงพอโดยเร็ว",
     ("ควรปล่อยไว้เช่นนั้น เพราะแสงสลัวไม่มีผลต่อดวงตาของนักเรียนเลย", "ควรปิดไฟที่เหลือให้มืดสนิท เพราะแสงสลัวอันตรายต่อดวงตามากกว่าความมืดสนิท", "ควรให้นักเรียนนั่งให้ไกลกระดานที่สุดโดยไม่แก้ไขแสง")),
)


@question_type(
    "phys.light_safety_foundation",
    display_name={"th": "บอกลักษณะแสงสว่างที่อาจเป็นอันตรายต่อดวงตา"},
    level=SECOND, subject=SUBJECT, topic=LIGHT_SAFETY_TOPIC,
)
class LightSafetyFoundation(QuestionType):
    """Too bright or too dim, for a long time, harms the eyes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            return _labelled(
                stem="แสงสว่างลักษณะใดอาจเป็นอันตรายต่อดวงตาเมื่อมองเป็นเวลานาน",
                correct="แสงที่จ้าเกินไปหรือสลัวเกินไป",
                wrongs=("แสงที่มีความสว่างพอเหมาะเท่านั้น", "แสงสีขาวทุกชนิดไม่ว่าจะสว่างเท่าใด", "แสงจากธรรมชาติเท่านั้น ไม่รวมแสงจากหลอดไฟ"),
                hint=SAFETY_HINT, topic=LIGHT_SAFETY_TOPIC,
            )
        bright = roll < 0.65
        return _labelled(stem=f"ข้อใดเป็นแสงที่{'จ้าเกินไป' if bright else 'สลัวเกินไป'}สำหรับดวงตา", correct=rng.choice(TOO_BRIGHT if bright else TOO_DIM),
                         wrongs=tuple(TOO_DIM if bright else TOO_BRIGHT), hint=SAFETY_HINT, topic=LIGHT_SAFETY_TOPIC)


@question_type(
    "phys.light_safety_fluency",
    display_name={"th": "เสนอแนะแนวทางป้องกันอันตรายจากแสงสว่างไม่เหมาะสม"},
    level=SECOND, subject=SUBJECT, topic=LIGHT_SAFETY_TOPIC,
)
class LightSafetyFluency(QuestionType):
    """A lighting problem; the method from the same table that fixes it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(LIGHT_PROBLEMS))
        problem = LIGHT_PROBLEMS[index]
        others = [p.method for i, p in enumerate(LIGHT_PROBLEMS) if i != index]
        return _labelled(
            stem=f"{problem.case} ควรป้องกันอันตรายต่อดวงตาด้วยวิธีใด",
            correct=problem.method,
            wrongs=tuple(others),
            hint="พิจารณาว่าแสงในสถานการณ์นั้นจ้าเกินไปหรือสลัวเกินไป แล้วเลือกวิธีที่ปรับแสงให้เหมาะสม",
            topic=LIGHT_SAFETY_TOPIC,
        )


@question_type(
    "phys.light_safety_application",
    display_name={"th": "วิเคราะห์สถานการณ์แสงสว่างไม่เหมาะสมและเสนอแนวทางป้องกัน"},
    level=SECOND, subject=SUBJECT, topic=LIGHT_SAFETY_TOPIC,
)
class LightSafetyApplication(QuestionType):
    """Authored cases, and a named child's situation judged and fixed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return _retopic(scenario_question(rng, LIGHT_SAFETY_SCENARIOS, hint=SAFETY_HINT), LIGHT_SAFETY_TOPIC)
        kid = rng.choice(KIDS)
        bright = rng.random() < 0.5
        case = rng.choice(TOO_BRIGHT if bright else TOO_DIM)
        right = ("แสงจ้าเกินไป ควรหลีกเลี่ยงการมองโดยตรงหรือใช้อุปกรณ์กรองแสง" if bright
                 else "แสงสลัวเกินไป ควรเพิ่มแสงสว่างให้เพียงพอก่อนใช้สายตา")
        return _labelled(stem=f"{kid}ต้องใช้สายตาท่ามกลาง{case} เป็นเวลานาน แสงนี้เป็นอย่างไร และควรทำอย่างไร", correct=right,
                         wrongs=(("แสงสลัวเกินไป ควรเพิ่มแสงสว่างให้เพียงพอก่อนใช้สายตา" if bright
                                  else "แสงจ้าเกินไป ควรหลีกเลี่ยงการมองโดยตรงหรือใช้อุปกรณ์กรองแสง"),
                                 "แสงพอเหมาะ ใช้สายตาต่อได้นานเท่าที่ต้องการ", "แสงไม่มีผลต่อดวงตา จึงไม่ต้องทำอะไร"),
                         hint=SAFETY_HINT, topic=LIGHT_SAFETY_TOPIC)
