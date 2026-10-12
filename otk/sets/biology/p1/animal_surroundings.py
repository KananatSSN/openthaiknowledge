"""สภาพแวดล้อมที่เหมาะสมกับการดำรงชีวิตของสัตว์

ชีวะ · ป.1 · สสวท. พื้นฐาน
Indicators: ว 1.1 ป.1/2

Sets moved here from: science_wave_b31.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import PRIMARY_ONE, _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b31 import ECOLOGY_TOPIC, SURROUNDINGS_SCENARIOS

PROVENANCE = Provenance("original")


class Surroundings(NamedTuple):
    """An animal, the surroundings it needs, and what those surroundings supply."""
    animal: str
    place: str
    need: str
    essential: str


# Each ``place`` names the feature the animal depends on, so no place in the
# table suits a second animal as well as it suits its own.
SURROUNDINGS = (
    Surroundings("ปลา", "แหล่งน้ำสะอาดที่มีน้ำตลอดปี",
                 "หายใจด้วยเหงือกโดยใช้อากาศที่ละลายอยู่ในน้ำ จึงต้องอยู่ในน้ำตลอดเวลา",
                 "น้ำให้หายใจด้วยเหงือก"),
    Surroundings("ไส้เดือนดิน", "ดินร่วนที่ชื้น มีเศษใบไม้ผุปนอยู่",
                 "หายใจทางผิวหนังที่ต้องชื้นอยู่เสมอ และกินเศษใบไม้ผุในดินเป็นอาหาร",
                 "ดินชื้นที่ช่วยให้ผิวหนังไม่แห้ง"),
    Surroundings("นกหัวขวาน", "ต้นไม้ใหญ่ที่มีลำต้นให้เจาะทำโพรงรัง",
                 "เจาะเปลือกไม้หาหนอนและแมลงกิน และเจาะโพรงในลำต้นเป็นรัง",
                 "ต้นไม้ให้เจาะหาอาหารและทำรัง"),
    Surroundings("ผีเสื้อ", "สวนที่มีต้นไม้ดอกบานให้ดูดน้ำหวาน",
                 "ดูดน้ำหวานจากดอกไม้เป็นอาหาร",
                 "ดอกไม้ให้ดูดน้ำหวาน"),
    Surroundings("ค้างคาว", "ถ้ำที่มืดและมีเพดานให้ห้อยตัว",
                 "ห้อยตัวพักผ่อนในที่มืดตอนกลางวัน แล้วออกหากินตอนกลางคืน",
                 "ที่มืดให้ห้อยตัวพักตอนกลางวัน"),
    Surroundings("ปูลม", "หาดทรายชื้นริมทะเล",
                 "ขุดรูในทรายชื้นเป็นที่หลบภัย และหาเศษอาหารที่คลื่นซัดขึ้นมา",
                 "ทรายชื้นให้ขุดรูหลบภัย"),
)


AQUATIC = frozenset({"ปลา"})


@question_type(
    "ecology.animal_surroundings_foundation",
    display_name={"th": "สภาพแวดล้อมที่เหมาะกับสัตว์"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class AnimalSurroundingsFoundation(QuestionType):
    """Say which surroundings suit an animal, or which animal suits them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(SURROUNDINGS)
        others = [other for other in SURROUNDINGS if other.animal != item.animal]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"สภาพแวดล้อมใดเหมาะสมกับการดำรงชีวิตของ“{item.animal}”มากที่สุด",
                correct=item.place,
                wrongs=tuple(other.place for other in others[:3]),
                hint="นึกถึงว่าสัตว์ชนิดนั้นกินอะไร หายใจอย่างไร และพักอยู่ที่ใด",
                topic=ECOLOGY_TOPIC,
            )
        return _labelled(
            stem=f"“{item.place}” เป็นสภาพแวดล้อมที่เหมาะสมกับการดำรงชีวิต"
                 f"ของสัตว์ใดมากที่สุด",
            correct=item.animal,
            wrongs=tuple(other.animal for other in others[:3]),
            hint="ดูว่าสภาพแวดล้อมนั้นมีอาหารหรือที่อยู่แบบใด แล้วนึกถึงสัตว์ที่ต้องการสิ่งนั้น",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.animal_surroundings_fluency",
    display_name={"th": "บอกเหตุผลที่สภาพแวดล้อมเหมาะกับสัตว์"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class AnimalSurroundingsFluency(QuestionType):
    """Say *why* the surroundings suit the animal, or what it loses elsewhere."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(SURROUNDINGS)
        others = [other for other in SURROUNDINGS if other.animal != item.animal]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"เหตุใด“{item.place}”จึงเหมาะสมกับการดำรงชีวิตของ{item.animal}",
                correct=f"เพราะ{item.animal}{item.need}",
                wrongs=tuple(f"เพราะ{item.animal}{other.need}"
                             for other in others[:3]),
                hint="เลือกเหตุผลที่เป็นความจริงของสัตว์ชนิดนั้น "
                     "ไม่ใช่ของสัตว์ชนิดอื่น",
                topic=ECOLOGY_TOPIC,
            )
        # Only a move between water and land is certain to strand the animal.
        # A flower garden still has damp soil for an earthworm, so a move
        # between two land places could make the stem itself untrue.
        elsewhere = rng.choice([other for other in others
                                if (other.animal in AQUATIC)
                                != (item.animal in AQUATIC)])
        return _labelled(
            stem=f"ถ้านำ{item.animal}ไปไว้ที่“{elsewhere.place}” "
                 f"{item.animal}จะดำรงชีวิตได้ยาก เพราะเหตุใด",
            correct=f"เพราะที่นั่นไม่มี{item.essential}",
            wrongs=tuple(f"เพราะที่นั่นไม่มี{other.essential}"
                         for other in others if other is not elsewhere)[:2]
            + ("เพราะสัตว์ทุกชนิดอยู่ได้เฉพาะในที่ที่มันเกิดเท่านั้น",),
            hint="นึกถึงสิ่งที่สัตว์ชนิดนั้นขาดไม่ได้ แล้วดูว่าที่ใหม่มีสิ่งนั้นหรือไม่",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.animal_surroundings_application",
    display_name={"th": "วิเคราะห์สภาพแวดล้อมที่เหมาะกับสัตว์"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class AnimalSurroundingsApplication(QuestionType):
    """Use what an animal needs to plan for it, or to explain a problem."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SURROUNDINGS_SCENARIOS,
            hint="นึกถึงสิ่งที่สัตว์ชนิดนั้นขาดไม่ได้ก่อน แล้วค่อยดูว่าสถานการณ์ขาดสิ่งใด",
        ), ECOLOGY_TOPIC)
