"""วิทยาศาสตร์และวิธีการทางวิทยาศาสตร์

วิทยาศาสตร์ทั่วไป · ม.1 · เสริมทักษะ
Indicators: —

Sets moved here from: science_wave_g4.
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
from otk.sets._support.science_wave_g4 import (
    FIRST_SECONDARY,
    INVESTIGATIONS,
    METHOD_SCENARIOS,
    SUBJECT,
)

PROVENANCE = Provenance("original")


SCIENTIFIC_METHOD_TOPIC = "วิทยาศาสตร์และวิธีการทางวิทยาศาสตร์"


class Step(NamedTuple):
    """One step of the method: its name, what it is for, and what it produces."""
    order: int
    name: str
    purpose: str


STEPS = (
    Step(1, "ระบุปัญหา", "บอกให้ชัดว่ากำลังจะหาคำตอบของคำถามใด"),
    Step(2, "ตั้งสมมติฐาน", "คาดคะเนคำตอบล่วงหน้าในรูปที่ตรวจสอบได้ด้วยการทดลอง"),
    Step(3, "ออกแบบและทำการทดลอง", "วางแผนควบคุมตัวแปรแล้วลงมือเก็บข้อมูลจริง"),
    Step(4, "วิเคราะห์ข้อมูล", "จัดกระทำข้อมูลที่ได้ให้เห็นแบบรูปหรือแนวโน้ม"),
    Step(5, "สรุปผล", "ตอบว่าข้อมูลสนับสนุนหรือไม่สนับสนุนสมมติฐานที่ตั้งไว้"),
)


#: Things a learner might do that are not a step of the method at all.
STEP_DECOYS = ("ท่องจำคำตอบจากหนังสือเรียน", "เลือกคำตอบที่คนส่วนใหญ่เห็นด้วย")


PURPOSE_DECOYS = ("ทำให้ผลการทดลองออกมาตรงกับที่ครูต้องการ",
                  "ตกแต่งรายงานให้สวยงามน่าอ่านก่อนส่ง")


@question_type(
    "sci.scientific_method_foundation",
    display_name={"th": "เรียงลำดับขั้นตอนของวิธีการทางวิทยาศาสตร์"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=SCIENTIFIC_METHOD_TOPIC,
)
class ScientificMethodFoundation(QuestionType):
    """The order, and what each step is for.

    Half the draws ask for the step that follows a named one, half ask what a
    named step is *for*. Order alone can be memorised as a chant; the purpose is
    what makes the order make sense.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            index = rng.randrange(len(STEPS) - 1)
            step = STEPS[index]
            correct = STEPS[index + 1].name
            wrongs = tuple(s.name for s in STEPS if s.name not in (step.name, correct)) + STEP_DECOYS
            return _labelled(
                stem=f"ในวิธีการทางวิทยาศาสตร์ ขั้นตอนที่ทำต่อจาก “{step.name}” คือขั้นตอนใด",
                correct=correct, wrongs=tuple(wrongs),
                hint=("ลำดับคือ ระบุปัญหา ตั้งสมมติฐาน ออกแบบและทำการทดลอง "
                      "วิเคราะห์ข้อมูล แล้วจึงสรุปผล"),
                topic=SCIENTIFIC_METHOD_TOPIC,
            )
        step = rng.choice(STEPS)
        wrongs = tuple(s.purpose for s in STEPS if s.order != step.order) + PURPOSE_DECOYS
        return _labelled(
            stem=f"ขั้นตอน “{step.name}” ในวิธีการทางวิทยาศาสตร์ทำไปเพื่ออะไร",
            correct=step.purpose, wrongs=tuple(wrongs),
            hint="อ่านชื่อขั้นตอนแล้วถามว่าเมื่อทำขั้นนี้เสร็จ นักเรียนจะได้อะไรออกมา",
            topic=SCIENTIFIC_METHOD_TOPIC,
        )


@question_type(
    "sci.scientific_method_fluency",
    display_name={"th": "ตั้งสมมติฐานที่ตรวจสอบได้จากปัญหาที่กำหนดให้"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=SCIENTIFIC_METHOD_TOPIC,
)
class ScientificMethodFluency(QuestionType):
    """A hypothesis is a testable prediction, not a true statement.

    The leading distractor is a sentence about the same topic that is perfectly
    true and completely untestable — which is what a learner writes when they
    have been told a hypothesis is "an educated guess" and nothing more.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        case = rng.choice(INVESTIGATIONS)
        others = [i.hypothesis for i in INVESTIGATIONS if i.question != case.question]
        return _labelled(
            stem=(f"นักเรียนตั้งปัญหาว่า “{case.question}” "
                  f"ข้อใดเป็นสมมติฐานที่เหมาะสมกับปัญหานี้และตรวจสอบได้ด้วยการทดลอง"),
            correct=case.hypothesis,
            wrongs=(case.flaw, *rng.sample(others, 2)),
            hint=("สมมติฐานต้องตอบปัญหาข้อนั้นโดยตรง อยู่ในรูป ถ้า...แล้ว... "
                  "และต้องตรวจสอบได้ด้วยการทดลอง ไม่ใช่ข้อความที่จริงอยู่แล้ว"),
            topic=SCIENTIFIC_METHOD_TOPIC,
        )


@question_type(
    "sci.scientific_method_application",
    display_name={"th": "วิจารณ์การทดลองและการสรุปผลด้วยวิธีการทางวิทยาศาสตร์"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=SCIENTIFIC_METHOD_TOPIC,
)
class ScientificMethodApplication(QuestionType):
    """An uncontrolled variable, a hypothesis the data refused, and tentativeness."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, METHOD_SCENARIOS,
            hint=("ถามเสมอว่าข้อมูลที่เก็บมาสนับสนุนข้อสรุปนั้นได้จริงหรือไม่ "
                  "และมีตัวแปรอื่นที่ไม่ได้ควบคุมไว้หรือเปล่า"),
        ), SCIENTIFIC_METHOD_TOPIC)
