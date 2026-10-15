"""วัฏจักรน้ำ

ธรณีวิทยา · ป.5 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.5/3

Sets moved here from: science_wave_c12.
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
from otk.sets._support.science_wave_b24 import PRIMARY_FIVE
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c12 import CYCLE_SCENARIOS
from otk.sets._support.life_earth_diagrams import WATER_CYCLE_ALT, WATER_CYCLES, WATER_STEPS
from otk.sets._support.ms1_diagrams import diagram_question

PROVENANCE = Provenance("original")


CYCLE_TOPIC = "วัฏจักรน้ำ"


class Step(NamedTuple):
    """A process of the water cycle, what happens, and what stands for it in the model."""
    name: str
    happens: str
    in_model: str


# In cycle order. The model is a covered bowl of water in the sun, with ice on the
# lid over one side and a small tray on the other side under the ice.
STEPS = (
    Step("การระเหย", "น้ำที่ได้รับความร้อนกลายเป็นไอน้ำลอยขึ้นสู่อากาศ",
         "น้ำในชามที่ถูกแดดส่องจนร้อน กลายเป็นไอลอยขึ้น"),
    Step("การควบแน่น", "ไอน้ำที่ลอยสูงขึ้นไปเย็นลงจนกลายเป็นละอองน้ำเล็ก ๆ รวมกันเป็นเมฆ",
         "ไอน้ำที่ลอยไปถูกฝาใต้ก้อนน้ำแข็งแล้วกลายเป็นหยดน้ำเกาะอยู่ใต้ฝา"),
    Step("หยาดน้ำฟ้า", "ละอองน้ำรวมกันจนหนักแล้วตกลงมาเป็นฝน",
         "หยดน้ำใต้ฝารวมกันจนหนักแล้วหยดลงมา"),
    Step("การไหลกลับสู่แหล่งน้ำ", "น้ำที่ตกลงมาไหลไปตามผิวดินและซึมลงดินกลับสู่แหล่งน้ำ",
         "หยดน้ำที่ตกลงในถาดเล็กแล้วไหลกลับลงไปในชาม"),
)


MODEL = ("แบบจำลอง: ชามใส่น้ำวางกลางแดด ปิดด้วยฝาใส และวางก้อนน้ำแข็งไว้บนฝา "
         "ใต้ก้อนน้ำแข็งมีถาดเล็กที่เอียงลงสู่น้ำในชาม")


# Everyday examples of each process, one process per example.
STEP_EXAMPLES = {
    "การระเหย": ("ผ้าที่ตากไว้กลางแดดแห้ง", "แอ่งน้ำบนถนนหายไปหลังแดดออก",
                 "น้ำในแก้วที่เปิดทิ้งไว้หลายวันลดลง", "น้ำทะเลในนาเกลือลดลงจนเหลือแต่เกลือ"),
    "การควบแน่น": ("หยดน้ำเกาะใต้ฝาหม้อที่กำลังต้มน้ำ", "เมฆก่อตัวขึ้นบนท้องฟ้าในตอนบ่าย",
                   "กระจกในห้องน้ำเป็นฝ้าหลังอาบน้ำอุ่น", "หยดน้ำเกาะรอบนอกแก้วน้ำเย็น"),
    "หยาดน้ำฟ้า": ("ฝนตกจากเมฆลงสู่พื้น", "ลูกเห็บตกลงมาระหว่างพายุ", "หิมะตกบนยอดเขาสูง",
                   "ฝนปรอยตกลงมาจากเมฆสีเทา"),
    "การไหลกลับสู่แหล่งน้ำ": ("น้ำฝนไหลลงคูแล้วไหลต่อไปยังแม่น้ำ",
                             "น้ำฝนซึมลงดินแล้วไปรวมกับน้ำใต้ดิน",
                             "น้ำจากภูเขาไหลลงลำธารแล้วลงสู่ทะเล",
                             "น้ำฝนบนหลังคาไหลลงรางน้ำแล้วลงบ่อ"),
}


def _next_step(step: Step) -> Step:
    return STEPS[(STEPS.index(step) + 1) % len(STEPS)]


@question_type(
    "geo.water_cycle_foundation",
    display_name={"th": "กระบวนการในวัฏจักรน้ำ"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=CYCLE_TOPIC,
)
class WaterCycleFoundation(QuestionType):
    """Name each process of the cycle and what happens in it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        step = rng.choice(STEPS)
        others = [other for other in STEPS if other.name != step.name]
        ask = rng.randrange(4)
        if ask == 2:
            return _labelled(
                stem=f"“{rng.choice(STEP_EXAMPLES[step.name])}” เป็นกระบวนการใดในวัฏจักรน้ำ",
                correct=step.name,
                wrongs=tuple(other.name for other in others),
                hint="ถามว่าน้ำกำลังกลายเป็นไอ ไอกำลังกลายเป็นน้ำ น้ำกำลังตกลงมา "
                     "หรือน้ำกำลังไหลกลับ",
                topic=CYCLE_TOPIC,
            )
        if ask == 3:
            return _labelled(
                stem=f"{MODEL} ส่วนที่{step.in_model} แทนกระบวนการใดในวัฏจักรน้ำ",
                correct=step.name,
                wrongs=tuple(other.name for other in others),
                hint="จับคู่สิ่งที่เกิดในแบบจำลองกับสิ่งที่เกิดในธรรมชาติ",
                topic=CYCLE_TOPIC,
            )
        if ask == 0:
            return _labelled(
                stem=f"ในวัฏจักรน้ำ “{step.name}” คืออะไร",
                correct=step.happens,
                wrongs=tuple(other.happens for other in others),
                hint="นึกลำดับ: น้ำกลายเป็นไอ ไอกลายเป็นเมฆ เมฆกลายเป็นฝน ฝนกลับสู่แหล่งน้ำ",
                topic=CYCLE_TOPIC,
            )
        return _labelled(
            stem=f"กระบวนการที่{step.happens} เรียกว่าอะไร",
            correct=step.name,
            wrongs=tuple(other.name for other in others),
            hint="นึกลำดับ: น้ำกลายเป็นไอ ไอกลายเป็นเมฆ เมฆกลายเป็นฝน ฝนกลับสู่แหล่งน้ำ",
            topic=CYCLE_TOPIC,
        )


@question_type(
    "geo.water_cycle_fluency",
    display_name={"th": "อธิบายวัฏจักรน้ำจากแบบจำลอง"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=CYCLE_TOPIC,
)
class WaterCycleFluency(QuestionType):
    """Read a described model and say what each part explains, or what comes next."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        step = rng.choice(STEPS)
        others = [other for other in STEPS if other.name != step.name]
        draw = rng.random()
        if draw < 0.15:
            return _labelled(
                stem=f"{MODEL} ในธรรมชาติ “{rng.choice(STEP_EXAMPLES[step.name])}” "
                     "ตรงกับสิ่งใดในแบบจำลองนี้",
                correct=step.in_model,
                wrongs=tuple(other.in_model for other in others),
                hint="หาว่าเหตุการณ์ในธรรมชาติเป็นกระบวนการใด แล้วหาส่วนของแบบจำลองที่แทนกระบวนการนั้น",
                topic=CYCLE_TOPIC,
            )
        if draw < 0.3:
            following = _next_step(step)
            return _labelled(
                stem=f"หลังจาก “{rng.choice(STEP_EXAMPLES[step.name])}” "
                     "กระบวนการถัดไปในวัฏจักรน้ำคือข้อใด",
                correct=following.name,
                wrongs=tuple(other.name for other in STEPS if other.name != following.name),
                hint="บอกก่อนว่าเหตุการณ์นั้นเป็นกระบวนการใด แล้วไล่ต่อไปหนึ่งขั้น",
                topic=CYCLE_TOPIC,
            )
        if draw < 0.55:
            return _labelled(
                stem=f"{MODEL} ในแบบจำลองนี้ “{step.in_model}” "
                     "อธิบายกระบวนการใดในวัฏจักรน้ำ",
                correct=step.name,
                wrongs=tuple(other.name for other in others),
                hint="เทียบสิ่งที่เกิดในชามกับสิ่งที่เกิดกับน้ำในธรรมชาติ",
                topic=CYCLE_TOPIC,
            )
        if draw < 0.78:
            return _labelled(
                stem=f"{MODEL} ในแบบจำลองนี้ สิ่งใดแทน “{step.name}”",
                correct=step.in_model,
                wrongs=tuple(other.in_model for other in others),
                hint="เทียบสิ่งที่เกิดในชามกับสิ่งที่เกิดกับน้ำในธรรมชาติ",
                topic=CYCLE_TOPIC,
            )
        following = _next_step(step)
        return _labelled(
            stem=f"{MODEL} ในแบบจำลองนี้ หลังจาก “{step.in_model}” "
                 "จะเกิดสิ่งใดต่อไป และแทนกระบวนการใด",
            correct=f"{following.in_model} ซึ่งแทน{following.name}",
            wrongs=tuple(f"{other.in_model} ซึ่งแทน{other.name}"
                         for other in STEPS if other.name != following.name),
            hint="ไล่ตามทางของน้ำในชามทีละขั้น น้ำจะวนกลับมาที่เดิม",
            topic=CYCLE_TOPIC,
        )


@question_type(
    "geo.water_cycle_application",
    display_name={"th": "ใช้วัฏจักรน้ำอธิบายเหตุการณ์ใหม่"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=CYCLE_TOPIC,
)
class WaterCycleApplication(QuestionType):
    """Change the model and predict, and trace water that seems to vanish."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CYCLE_SCENARIOS,
            hint="นึกว่าความร้อนและความเย็นทำให้น้ำเปลี่ยนสถานะอย่างไร",
        ), CYCLE_TOPIC)


@question_type(
    "geo.water_cycle_diagram",
    display_name={"th": "ระบุกระบวนการในวัฏจักรน้ำจากภาพ"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=CYCLE_TOPIC,
)
class WaterCycleDiagram(QuestionType):
    """Read the numbered arrows of a drawn water cycle.

    Name the process an arrow shows, find the arrow for a process, or match an
    everyday example to its arrow. The numbering differs between pictures.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(WATER_CYCLES)
        step = rng.choice(STEPS)
        number = spec.numbers[WATER_STEPS.index(step.name)]
        hint = "ดูว่าลูกศรพาน้ำจากที่ใดไปที่ใด: จากทะเลขึ้นฟ้า เข้าไปในเมฆ จากเมฆลงดิน หรือจากดินกลับลงทะเล"
        kind = rng.randrange(3)
        if kind == 0:
            return diagram_question(
                spec.asset_id, WATER_CYCLE_ALT,
                stem=f"จากภาพวัฏจักรน้ำ ลูกศรหมายเลข {number} แสดงกระบวนการใด",
                correct=step.name,
                wrongs=tuple(s.name for s in STEPS if s is not step),
                hint=hint, topic=CYCLE_TOPIC,
            )
        if kind == 1:
            return diagram_question(
                spec.asset_id, WATER_CYCLE_ALT,
                stem=f"จากภาพวัฏจักรน้ำ ลูกศรหมายเลขใดแสดง{step.name}",
                correct=f"หมายเลข {number}",
                wrongs=tuple(f"หมายเลข {n}" for n in spec.numbers if n != number),
                hint=hint, topic=CYCLE_TOPIC,
            )
        example = rng.choice(STEP_EXAMPLES[step.name])
        return diagram_question(
            spec.asset_id, WATER_CYCLE_ALT,
            stem=f"จากภาพวัฏจักรน้ำ เหตุการณ์ “{example}” เป็นกระบวนการเดียวกับลูกศรหมายเลขใด",
            correct=f"หมายเลข {number}",
            wrongs=tuple(f"หมายเลข {n}" for n in spec.numbers if n != number),
            hint="บอกให้ได้ก่อนว่าเหตุการณ์นั้นเป็นกระบวนการใด แล้วหาลูกศรของกระบวนการนั้นในภาพ",
            topic=CYCLE_TOPIC,
        )
