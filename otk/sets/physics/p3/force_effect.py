"""ผลของแรงต่อการเคลื่อนที่ของวัตถุ

ฟิสิกส์ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.3/1

Sets moved here from: science_wave_d14.
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
from otk.sets._support.science_wave_d14 import KIDS, SUBJECT, THIRD

PROVENANCE = Provenance("original")


FORCE_EFFECT_TOPIC = "ผลของแรงต่อการเคลื่อนที่ของวัตถุ"


START, STOP, FASTER, SLOWER, TURN = (
    "ทำให้วัตถุที่อยู่นิ่งเริ่มเคลื่อนที่",
    "ทำให้วัตถุที่กำลังเคลื่อนที่หยุดนิ่ง",
    "ทำให้วัตถุเคลื่อนที่เร็วขึ้น",
    "ทำให้วัตถุเคลื่อนที่ช้าลง",
    "ทำให้วัตถุเปลี่ยนทิศทางการเคลื่อนที่",
)


EFFECTS = (START, STOP, FASTER, SLOWER, TURN)


FORCE_HINT = "แรงทำให้วัตถุเริ่มเคลื่อนที่ หยุด เร็วขึ้น ช้าลง หรือเปลี่ยนทิศทางได้ เทียบการเคลื่อนที่ก่อนและหลังออกแรง"


class Push(NamedTuple):
    record: str
    effect: str


PUSHES = (
    Push("ลูกบอลวางนิ่งบนพื้น นักเรียนเตะลูกบอล ลูกบอลกลิ้งออกไป", START),
    Push("รถของเล่นวางนิ่งบนโต๊ะ นักเรียนผลักรถ รถแล่นออกไป", START),
    Push("ชิงช้าหยุดนิ่งอยู่ พ่อผลักชิงช้า ชิงช้าเริ่มแกว่ง", START),
    Push("ลูกแก้ววางนิ่งบนพื้น นักเรียนดีดลูกแก้ว ลูกแก้วกลิ้งออกไป", START),
    Push("ลูกบอลกลิ้งมาหาผู้รักษาประตู ผู้รักษาประตูใช้มือรับไว้ ลูกบอลหยุดนิ่ง", STOP),
    Push("รถเข็นกำลังเคลื่อนที่ นักเรียนดึงรถไว้จนรถหยุดนิ่ง", STOP),
    Push("ลูกปิงปองกลิ้งบนโต๊ะ นักเรียนเอามือวางขวางไว้ ลูกปิงปองหยุดนิ่ง", STOP),
    Push("นักเรียนผลักชิงช้าที่กำลังแกว่งมาทางเดียวกับที่ผลัก ชิงช้าแกว่งเร็วขึ้น", FASTER),
    Push("รถของเล่นกำลังแล่นช้า ๆ นักเรียนผลักตามทิศที่รถแล่น รถแล่นเร็วขึ้น", FASTER),
    Push("เพื่อนนั่งรถเข็นไปช้า ๆ นักเรียนช่วยเข็นไปทางเดียวกัน รถเข็นเร็วขึ้น", FASTER),
    Push("นักเรียนวิ่งอยู่แล้วเพื่อนดึงเสื้อไว้เบา ๆ นักเรียนวิ่งช้าลงแต่ยังไม่หยุด", SLOWER),
    Push("รถของเล่นแล่นเข้ามา นักเรียนดันสวนทางเบา ๆ รถแล่นช้าลงแต่ยังไม่หยุด", SLOWER),
    Push("จักรยานแล่นอยู่ ผู้ขี่บีบเบรกเบา ๆ จักรยานแล่นช้าลงแต่ยังไม่หยุด", SLOWER),
    Push("ลูกบอลกลิ้งตรงมา นักเรียนเตะด้านข้างลูกบอล ลูกบอลกลิ้งไปอีกทางหนึ่ง", TURN),
    Push("ลูกปิงปองลอยมาหานักเรียน นักเรียนตีด้วยไม้ ลูกปิงปองลอยกลับไปทางเดิม", TURN),
    Push("รถของเล่นแล่นตรงไป นักเรียนดันด้านข้างรถ รถเลี้ยวไปอีกทาง", TURN),
)


FORCE_OBJECTS = ("ลูกบอล", "รถของเล่น", "รถเข็น", "ลูกแก้ว", "กล่องบนพื้นลื่น", "เรือของเล่นในอ่างน้ำ")


HOW = {
    START: "ผลักหรือดึงวัตถุที่อยู่นิ่งไปในทิศที่ต้องการ",
    STOP: "ออกแรงสวนทางกับการเคลื่อนที่จนวัตถุหยุด",
    FASTER: "ออกแรงไปทางเดียวกับที่วัตถุกำลังเคลื่อนที่",
    SLOWER: "ออกแรงเบา ๆ สวนทางกับการเคลื่อนที่",
    TURN: "ออกแรงด้านข้างของวัตถุ ไปทางที่ต้องการให้เลี้ยว",
}


FORCE_EFFECT_SCENARIOS = (
    ("นักฟุตบอลต้องการให้ลูกบอลที่กลิ้งมาหาเปลี่ยนไปทางประตู ควรทำอย่างไร",
     "ออกแรงเตะลูกบอลในทิศไปทางประตู เพราะแรงทำให้วัตถุเปลี่ยนทิศทางการเคลื่อนที่ได้",
     ("ไม่ต้องออกแรง รอให้ลูกบอลเปลี่ยนทิศเอง",
      "ออกแรงเตะในทิศเดียวกับที่ลูกบอลกลิ้งมา ลูกบอลจะหยุดทันที",
      "ตะโกนบอกลูกบอลให้เปลี่ยนทิศ")),
    ("รถของเล่นสองคันเหมือนกันวางนิ่ง นักเรียนผลักคันแรกเบา ๆ และผลักคันที่สองแรง ๆ ข้อใดน่าจะเกิดขึ้น",
     "คันที่สองเคลื่อนที่ได้เร็วกว่า เพราะได้รับแรงมากกว่า",
     ("คันแรกเคลื่อนที่ได้เร็วกว่า",
      "ทั้งสองคันไม่เคลื่อนที่",
      "ทั้งสองคันเคลื่อนที่เร็วเท่ากันเสมอ")),
    ("จักรยานที่กำลังแล่นลงเนินค่อย ๆ ช้าลงจนหยุดเมื่อผู้ขี่บีบเบรก เพราะเหตุใด",
     "เบรกออกแรงต้านการหมุนของล้อ แรงนี้ทำให้จักรยานช้าลงจนหยุด",
     ("เบรกทำให้จักรยานเบาลง",
      "จักรยานหยุดเองโดยไม่มีแรงกระทำ",
      "เบรกออกแรงผลักจักรยานให้เร็วขึ้น")),
)


@question_type(
    "phys.force_effect_foundation",
    display_name={"th": "บอกผลของแรงที่มีต่อการเคลื่อนที่ของวัตถุ"},
    level=THIRD, subject=SUBJECT, topic=FORCE_EFFECT_TOPIC,
)
class ForceEffectFoundation(QuestionType):
    """Which statement is an effect of force, and an example for each effect."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return _labelled(
                stem="ข้อใดเป็นผลของแรงที่มีต่อการเคลื่อนที่ของวัตถุ",
                correct=rng.choice(EFFECTS),
                wrongs=tuple(("ทำให้วัตถุเปลี่ยนสีทันที", "ทำให้วัตถุมีมวลเพิ่มขึ้น",
                                         "ทำให้วัตถุเปลี่ยนเป็นวัสดุชนิดใหม่", "ทำให้วัตถุหายไป")),
                hint=FORCE_HINT, topic=FORCE_EFFECT_TOPIC,
            )
        effect = rng.choice(EFFECTS)
        right = rng.choice([p.record for p in PUSHES if p.effect == effect])
        pool = [p.record for p in PUSHES if p.effect != effect]
        return _labelled(stem=f"ข้อใดเป็นตัวอย่างของแรงที่{effect}", correct=right, wrongs=tuple(pool),
                         hint=FORCE_HINT, topic=FORCE_EFFECT_TOPIC)


@question_type(
    "phys.force_effect_fluency",
    display_name={"th": "ระบุผลของแรงต่อการเปลี่ยนแปลงการเคลื่อนที่จากหลักฐาน"},
    level=THIRD, subject=SUBJECT, topic=FORCE_EFFECT_TOPIC,
)
class ForceEffectFluency(QuestionType):
    """An observed push or pull; the change in motion it caused."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        push = rng.choice(PUSHES)
        others = [e for e in EFFECTS if e != push.effect]
        return _labelled(
            stem=f"นักเรียนสังเกตได้ว่า {push.record} จากหลักฐานนี้ แรงที่กระทำส่งผลอย่างไร",
            correct=push.effect,
            wrongs=tuple(others),
            hint="เทียบการเคลื่อนที่ก่อนและหลังออกแรง: เริ่ม หยุด เร็วขึ้น ช้าลง หรือเปลี่ยนทิศ",
            topic=FORCE_EFFECT_TOPIC,
        )


@question_type(
    "phys.force_effect_application",
    display_name={"th": "ใช้ผลของแรงอธิบายการเคลื่อนที่ในชีวิตประจำวัน"},
    level=THIRD, subject=SUBJECT, topic=FORCE_EFFECT_TOPIC,
)
class ForceEffectApplication(QuestionType):
    """Authored cases, and how to push an object to get the change you want."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return _retopic(scenario_question(rng, FORCE_EFFECT_SCENARIOS,
                                              hint="การเคลื่อนที่จะเปลี่ยนเมื่อมีแรงมากระทำ ทิศและขนาดของแรงกำหนดว่าเปลี่ยนอย่างไร"), FORCE_EFFECT_TOPIC)
        effect = rng.choice(EFFECTS)
        thing = rng.choice(FORCE_OBJECTS)
        kid = rng.choice(KIDS)
        goal = effect.removeprefix("ทำให้วัตถุ")
        others = [HOW[e] for e in EFFECTS if e != effect]
        return _labelled(stem=f"{kid}ต้องการให้{thing}{goal} ควรออกแรงอย่างไร", correct=HOW[effect], wrongs=tuple(others),
                         hint=FORCE_HINT, topic=FORCE_EFFECT_TOPIC)
