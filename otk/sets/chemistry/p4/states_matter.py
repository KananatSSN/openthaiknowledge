"""สมบัติของสสารทั้ง 3 สถานะ

เคมี · ป.4 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.4/3

Sets moved here from: science_wave_d5.
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
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d4 import FOURTH

PROVENANCE = Provenance("original")


STATES_TOPIC = "สมบัติของสสารทั้ง 3 สถานะ"


SOLID, LIQUID, GAS = "ของแข็ง", "ของเหลว", "แก๊ส"


class State(NamedTuple):
    name: str
    example: str
    fixed_shape: bool
    fixed_volume: bool
    observed: str


STATES = (
    State(SOLID, "ก้อนหิน", True, True,
          "ย้ายก้อนหินจากกล่องเหลี่ยมไปใส่ถ้วยกลม ก้อนหินมีรูปร่างเดิมและขนาดเดิม"),
    State(LIQUID, "น้ำ 100 มิลลิลิตร", False, True,
          "เทน้ำ 100 มิลลิลิตรจากแก้วทรงสูงลงชามกว้าง น้ำมีรูปร่างตามชาม และวัดได้ 100 มิลลิลิตรเท่าเดิม"),
    State(GAS, "อากาศ", False, False,
          "บีบอากาศจากลูกโป่งลูกเล็กเข้าไปในลูกโป่งลูกใหญ่ที่แฟบ อากาศกระจายเต็มลูกโป่งลูกใหญ่และมีรูปร่างตามลูกโป่ง"),
)


WEIGHED = "ชั่งภาชนะก่อนและหลังใส่สิ่งของทั้งสาม มวลรวมเพิ่มขึ้นทุกครั้ง และสิ่งของทั้งสามกินที่ในภาชนะจนสิ่งอื่นเข้าไปแทนที่ไม่ได้"


def state_parts(a: State, b: State) -> tuple[Part, ...]:
    """Two states compared on mass, space, shape and volume."""

    def shape(s: State) -> str:
        return "มีรูปร่างคงที่" if s.fixed_shape else "มีรูปร่างตามภาชนะ"

    def volume(s: State) -> str:
        return "มีปริมาตรคงที่" if s.fixed_volume else "มีปริมาตรเท่ากับภาชนะที่บรรจุ"

    def flip_shape(s: State) -> str:
        return "มีรูปร่างตามภาชนะ" if s.fixed_shape else "มีรูปร่างคงที่"

    def flip_volume(s: State) -> str:
        return "มีปริมาตรเท่ากับภาชนะที่บรรจุ" if s.fixed_volume else "มีปริมาตรคงที่"

    return (
        Part("มวล", f"{a.name}และ{b.name}มีมวลทั้งคู่", f"{b.name}ไม่มีมวล"),
        Part("การต้องการที่อยู่", f"{a.name}และ{b.name}ต้องการที่อยู่ทั้งคู่", f"{b.name}ไม่ต้องการที่อยู่"),
        Part("รูปร่าง", f"{a.name}{shape(a)} ส่วน{b.name}{shape(b)}",
             f"{a.name}{flip_shape(a)} ส่วน{b.name}{shape(b)}"),
        Part("ปริมาตร", f"{a.name}{volume(a)} ส่วน{b.name}{volume(b)}",
             f"{a.name}{volume(a)} ส่วน{b.name}{flip_volume(b)}"),
    )


STATES_SCENARIOS = (
    ("นักเรียนเป่าลูกโป่งแล้วนำไปชั่งเทียบกับลูกโป่งแฟบ พบว่าลูกโป่งที่เป่าลมมีมวลมากกว่าเล็กน้อย หลักฐานนี้บอกอะไร",
     "อากาศซึ่งเป็นแก๊สมีมวล",
     ("อากาศไม่มีมวล ลูกโป่งจึงหนักขึ้นเพราะยางยืดออก",
      "แก๊สไม่ต้องการที่อยู่",
      "ของแข็งเท่านั้นที่มีมวล",
      "ลูกโป่งหนักขึ้นเพราะมีน้ำอยู่ข้างใน",
      "แก๊สมีรูปร่างคงที่เหมือนของแข็ง")),
    ("คว่ำแก้วเปล่าลงในอ่างน้ำตรง ๆ แล้วพบว่าน้ำเข้าไปในแก้วได้เพียงเล็กน้อย เพราะเหตุใด",
     "ในแก้วมีอากาศอยู่ อากาศต้องการที่อยู่จึงกันน้ำไม่ให้เข้าไปเต็มแก้ว",
     ("แก้วเปล่าไม่มีอะไรอยู่ข้างใน น้ำจึงเข้าไม่ได้",
      "น้ำไม่ต้องการที่อยู่",
      "อากาศมีรูปร่างคงที่เหมือนของแข็ง",
      "น้ำมีมวลน้อยเกินไปจึงเข้าแก้วไม่ได้",
      "แก้วดูดน้ำไว้ที่ผนังจนหมด")),
    ("ถ้าเทน้ำผลไม้ 250 มิลลิลิตรจากกล่องลงในแก้วทรงสูง แล้วเทต่อลงในถ้วยกว้าง ปริมาตรของน้ำผลไม้เป็นอย่างไร",
     "ยังเป็น 250 มิลลิลิตร แม้รูปร่างจะเปลี่ยนไปตามภาชนะ",
     ("มากขึ้นในถ้วยกว้าง เพราะน้ำแผ่ออก",
      "น้อยลงในแก้วทรงสูง เพราะแก้วแคบ",
      "เปลี่ยนไปเท่ากับขนาดของภาชนะทุกครั้ง",
      "เหลือครึ่งหนึ่งเมื่อเทลงถ้วยกว้าง",
      "กลายเป็น 500 มิลลิลิตร เพราะเทสองครั้ง")),
    ("เมื่อบีบลูกโป่งที่เป่าลมไว้ ลูกโป่งเปลี่ยนรูปร่างไปตามแรงบีบ แต่เมื่อบีบก้อนหิน ก้อนหินไม่เปลี่ยนรูปร่าง ข้อใดอธิบายได้ถูกต้อง",
     "อากาศในลูกโป่งเป็นแก๊สซึ่งมีรูปร่างไม่คงที่ ส่วนก้อนหินเป็นของแข็งที่มีรูปร่างคงที่",
     ("อากาศในลูกโป่งเป็นของแข็ง ส่วนก้อนหินเป็นแก๊ส",
      "ก้อนหินไม่มีมวล จึงไม่เปลี่ยนรูปร่าง",
      "อากาศไม่ต้องการที่อยู่ จึงถูกบีบได้",
      "ทั้งอากาศและก้อนหินมีรูปร่างคงที่",
      "ลูกโป่งเปลี่ยนรูปร่างเพราะอากาศหายไปหมด")),
    ("เมื่อเปิดขวดน้ำหอมที่มุมห้อง สักพักคนที่อยู่อีกมุมห้องก็ได้กลิ่น ข้อใดอธิบายได้สอดคล้องกับสมบัติของแก๊ส",
     "ไอของน้ำหอมเป็นแก๊สที่แผ่กระจายเต็มที่ว่างของห้อง จึงไปถึงอีกมุมห้องได้",
     ("น้ำหอมเป็นของแข็งที่กลิ้งไปตามพื้น",
      "แก๊สมีรูปร่างคงที่จึงลอยเป็นก้อนไปหาคน",
      "แก๊สไม่มีมวลจึงหายไปทันที",
      "น้ำหอมเป็นของเหลวที่ไหลไปตามผนังห้อง",
      "กลิ่นไม่ใช่สสารจึงไม่ต้องการที่อยู่")),
)


@question_type(
    "chem.states_matter_foundation",
    display_name={"th": "ระบุสถานะของสสารจากรูปร่างและปริมาตร"},
    level=FOURTH, subject=SUBJECT, topic=STATES_TOPIC,
)
class StatesMatterFoundation(QuestionType):
    """A description of shape and volume, or an everyday example; which state it is."""

    EXAMPLES = {
        SOLID: ("ก้อนหิน", "ดินสอ", "ก้อนน้ำแข็ง", "ช้อนเหล็ก", "ไม้บรรทัด"),
        LIQUID: ("น้ำผลไม้ในแก้ว", "นมในกล่อง", "น้ำมันพืชในขวด", "น้ำเชื่อม"),
        GAS: ("อากาศในลูกโป่ง", "ไอน้ำที่ลอยจากกาต้มน้ำ", "อากาศในยางรถจักรยาน"),
    }

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        state = rng.choice(STATES)
        shape = "มีรูปร่างคงที่" if state.fixed_shape else "มีรูปร่างเปลี่ยนไปตามภาชนะ"
        volume = "มีปริมาตรคงที่" if state.fixed_volume else "มีปริมาตรเปลี่ยนไปตามภาชนะที่บรรจุ"
        stem = f"สสารชนิดหนึ่ง{shape} และ{volume} สสารนี้อยู่ในสถานะใด"
        if rng.random() < 0.6:
            stem = f"\"{rng.choice(self.EXAMPLES[state.name])}\" อยู่ในสถานะใด"
        return _labelled(
            stem=stem,
            correct=state.name,
            wrongs=(*(s.name for s in STATES if s != state), "ไม่ใช่สสาร เพราะไม่มีมวล",
                    "ไม่ใช่สสาร เพราะไม่ต้องการที่อยู่"),
            hint="ของแข็งคงทั้งรูปร่างและปริมาตร ของเหลวคงปริมาตรแต่รูปร่างตามภาชนะ แก๊สเปลี่ยนทั้งสองอย่าง",
            topic=STATES_TOPIC,
        )


@question_type(
    "chem.states_matter_fluency",
    display_name={"th": "เปรียบเทียบสมบัติของสสารทั้ง 3 สถานะจากข้อมูลการสังเกต"},
    level=FOURTH, subject=SUBJECT, topic=STATES_TOPIC,
)
class StatesMatterFluency(QuestionType):
    """Observations of two states; compare them on all four aspects."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = rng.sample(STATES, 2)
        mass, space, shape, volume = state_parts(a, b)
        # Either state may be the one wrongly said to lack mass or need no space.
        mass = mass._replace(false=rng.choice((mass.false, f"{a.name}ไม่มีมวล")))
        space = space._replace(false=rng.choice((space.false, f"{a.name}ไม่ต้องการที่อยู่")))
        return parts_item(
            rng, (mass, space, shape, volume),
            stem=(f"นักเรียนบันทึกการสังเกตไว้ว่า — {a.observed} / {b.observed} / {WEIGHED} "
                  f"จากข้อมูลนี้ ข้อใดเปรียบเทียบ{a.name} ({a.example}) กับ{b.name} ({b.example}) ได้ถูกต้องทั้งหมด"),
            hint="ตรวจทีละด้าน: มวล ที่อยู่ รูปร่าง และปริมาตร ข้อที่ผิดจะผิดอย่างน้อยหนึ่งด้าน",
            topic=STATES_TOPIC,
        )


@question_type(
    "chem.states_matter_application",
    display_name={"th": "ใช้สมบัติของสสารทั้ง 3 สถานะอธิบายสิ่งที่พบ"},
    level=FOURTH, subject=SUBJECT, topic=STATES_TOPIC,
)
class StatesMatterApplication(QuestionType):
    """A weighed balloon, a glass pushed into water, and poured juice."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, STATES_SCENARIOS,
            hint="นึกว่าสสารทุกสถานะมีมวลและต้องการที่อยู่ แล้วดูว่ารูปร่างหรือปริมาตรเปลี่ยนหรือไม่",
        ), STATES_TOPIC)
