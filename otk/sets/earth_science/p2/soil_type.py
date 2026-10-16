"""ส่วนประกอบและชนิดของดิน

ธรณีวิทยา · ป.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.2/1

Sets moved here from: science_wave_c10.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import PRIMARY_TWO, _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SOIL_SCENARIOS, SUBJECT

PROVENANCE = Provenance("original")


SOIL_TOPIC = "ส่วนประกอบและชนิดของดิน"


class Component(NamedTuple):
    """One component of soil, and a simple test that shows it is there."""
    name: str
    evidence: str


# Each test shows exactly one component, so a test names one answer.
COMPONENTS = (
    Component("เศษหินและแร่", "ใส่ดินในแก้วน้ำ คนแล้วตั้งทิ้งไว้ มีเม็ดแข็ง ๆ ตกอยู่ที่ก้นแก้ว"),
    Component("ซากพืชซากสัตว์", "ใส่ดินในแก้วน้ำ คนแล้วตั้งทิ้งไว้ มีเศษใบไม้และกิ่งไม้เล็ก ๆ ลอยอยู่ที่ผิวน้ำ"),
    Component("น้ำ", "นำดินไปตากแดดหลายวัน ดินแห้งและมีน้ำหนักลดลง"),
    Component("อากาศ", "ค่อย ๆ เทน้ำลงบนดินแห้งในแก้ว มีฟองเล็ก ๆ ผุดขึ้นมา"),
)


ALL_COMPONENTS = "เศษหินและแร่ ซากพืชซากสัตว์ที่ย่อยสลาย น้ำ และอากาศ"


# More tests for each component; like COMPONENTS, each shows exactly one of them.
MORE_EVIDENCE = {
    "เศษหินและแร่": (
        "ร่อนดินแห้งผ่านตะแกรงละเอียด มีเม็ดเล็ก ๆ ที่แข็งและสากมือค้างอยู่บนตะแกรง",
        "ส่องดินด้วยแว่นขยาย เห็นเม็ดแข็งเล็ก ๆ บางเม็ดสะท้อนแสงเป็นประกาย",
    ),
    "ซากพืชซากสัตว์": (
        "ส่องดินด้วยแว่นขยาย เห็นเศษรากไม้เล็ก ๆ และเปลือกแมลงปนอยู่",
        "เขี่ยดินจากใต้ต้นไม้ พบเศษใบไม้ผุสีดำที่ยุ่ยจนแทบจำรูปใบไม่ได้",
    ),
    "น้ำ": (
        "ใส่ดินในถุงพลาสติกใสแล้วมัดปากถุงไว้กลางแดด มีหยดน้ำเกาะด้านในถุงจำนวนมาก",
        "ใส่ดินในจานที่มีฝาปิดแล้วนำไปอุ่น มีหยดน้ำเกาะอยู่ใต้ฝา",
    ),
    "อากาศ": (
        "กดก้อนดินแห้งให้จมลงในน้ำ มีฟองเล็ก ๆ ลอยขึ้นมาจากก้อนดิน",
        "เทน้ำลงในกระป๋องที่ใส่ดินแห้งไว้เต็ม มีฟองผุดขึ้นมาที่ผิวน้ำอยู่ครู่หนึ่ง",
    ),
}


def _evidence(rng: Random, name: str) -> str:
    base = next(item.evidence for item in COMPONENTS if item.name == name)
    return rng.choice((base, *MORE_EVIDENCE[name]))


class Soil(NamedTuple):
    """One soil type, by the two criteria the indicator names."""
    name: str
    texture: str
    cohesion: str


SOILS = (
    Soil("ดินร่วน", "เนื้อดินนุ่มมือ", "จับตัวกันปั้นเป็นก้อนได้ แต่แตกออกง่ายเมื่อกด"),
    Soil("ดินเหนียว", "เนื้อดินละเอียดและลื่นมือเมื่อเปียก", "จับตัวกันแน่น ปั้นเป็นเส้นยาวได้โดยไม่แตก"),
    Soil("ดินทราย", "เนื้อดินหยาบและสากมือ", "ไม่จับตัวกัน ปั้นเป็นก้อนไม่ได้"),
)


def _both_criteria(soil: Soil) -> str:
    return f"{soil.texture} และ{soil.cohesion}"


# Other ways a child might report the same two findings, keyed by soil name.
# Each still names both criteria and fits that soil only.
MORE_FEELS = {
    "ดินร่วน": ("ถูแล้วรู้สึกนุ่ม ไม่สากและไม่ลื่นมาก และกำแล้วเป็นก้อนหลวม ๆ ใช้นิ้วบี้ก็ร่วนออก",
               "ถูแล้วนุ่มมือ และปั้นเป็นก้อนได้ แต่พอปั้นเป็นเส้นก็ขาดง่าย"),
    "ดินเหนียว": ("ถูแล้วเนียนลื่นและติดนิ้ว และปั้นเป็นเส้นยาวแล้วขดเป็นวงได้โดยไม่แตก",
                 "ถูแล้วละเอียดมาก ลื่นเหมือนสบู่ และจับตัวเหนียวแน่น กดแล้วเป็นรอยนิ้วชัดเจน"),
    "ดินทราย": ("ถูแล้วสากมือ เห็นเม็ดเล็ก ๆ ชัดเจน และกำแล้วแบมือออกดินก็ร่วงกระจาย",
               "ถูแล้วหยาบและได้ยินเสียงเม็ดเสียดสีกัน และปั้นอย่างไรก็ไม่เป็นก้อน"),
}


@question_type(
    "geo.soil_type_foundation",
    display_name={"th": "ส่วนประกอบของดิน"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=SOIL_TOPIC,
)
class SoilTypeFoundation(QuestionType):
    """Identify the components of soil — the indicator's first free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.35:
            return _labelled(
                stem="ดินประกอบด้วยสิ่งใดบ้าง",
                correct=ALL_COMPONENTS,
                wrongs=("เศษหินและแร่เท่านั้น",
                        "น้ำและอากาศเท่านั้น",
                        "เศษหินและแร่ พลาสติก เศษแก้ว และโลหะที่ถูกทิ้ง",
                        "ซากพืชซากสัตว์ที่ย่อยสลายและน้ำเท่านั้น ไม่มีอากาศ"),
                hint="ดินมีทั้งส่วนที่เป็นของแข็ง ของเหลว และแก๊สอยู่ด้วยกัน",
                topic=SOIL_TOPIC,
            )
        item = rng.choice(COMPONENTS)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ข้อใดเป็นการทดลองที่แสดงว่าดินมี{item.name}",
                correct=_evidence(rng, item.name),
                wrongs=tuple(_evidence(rng, other.name)
                             for other in COMPONENTS if other.name != item.name),
                hint="นึกว่าสิ่งที่เห็นในการทดลองมาจากส่วนประกอบใดของดิน",
                topic=SOIL_TOPIC,
            )
        return _labelled(
            stem=f"นักเรียนทดลองว่า {_evidence(rng, item.name)} แสดงว่าดินมีส่วนประกอบใด",
            correct=item.name,
            wrongs=tuple(other.name for other in COMPONENTS if other.name != item.name),
            hint="นึกว่าสิ่งที่เห็นในการทดลองมาจากส่วนประกอบใดของดิน",
            topic=SOIL_TOPIC,
        )


@question_type(
    "geo.soil_type_fluency",
    display_name={"th": "จำแนกชนิดของดินจากเนื้อดินและการจับตัว"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=SOIL_TOPIC,
)
class SoilTypeFluency(QuestionType):
    """Classify soil by texture and cohesion together — the second free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        soil = rng.choice(SOILS)
        others = [other for other in SOILS if other.name != soil.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"นักเรียนนำดินตัวอย่างมาพรมน้ำเล็กน้อยแล้วใช้นิ้วถูและปั้น "
                     f"พบว่า{rng.choice((_both_criteria(soil), *MORE_FEELS[soil.name]))} "
                     "ดินตัวอย่างนี้เป็นดินชนิดใด",
                correct=soil.name,
                wrongs=tuple(other.name for other in others) + ("บอกไม่ได้ เพราะดินทุกชนิดมีลักษณะเหมือนกัน",),
                hint="ใช้ทั้งเนื้อดินและการจับตัวเป็นเกณฑ์ ไม่ใช้เพียงอย่างเดียว",
                topic=SOIL_TOPIC,
            )
        # A wrong answer keeps one criterion right and gets the other wrong, so a
        # learner who checks only one criterion cannot tell them apart.
        return _labelled(
            stem=f"{soil.name}มีลักษณะเนื้อดินและการจับตัวอย่างไร",
            correct=_both_criteria(soil),
            wrongs=tuple([f"{soil.texture} และ{other.cohesion}" for other in others]
                + [f"{other.texture} และ{soil.cohesion}" for other in others]
                + [_both_criteria(other) for other in others]),
            hint="ตรวจทั้งสองส่วน คือ เนื้อดินเมื่อถู และการจับตัวเมื่อปั้น",
            topic=SOIL_TOPIC,
        )


@question_type(
    "geo.soil_type_application",
    display_name={"th": "ใช้เกณฑ์จำแนกดินในสถานการณ์ใหม่"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=SOIL_TOPIC,
)
class SoilTypeApplication(QuestionType):
    """Classify fairly, predict drainage, and refuse to classify by colour."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SOIL_SCENARIOS,
            hint="นึกถึงเนื้อดินและการจับตัว แล้วคิดว่าส่งผลต่อสิ่งที่ถามอย่างไร",
        ), SOIL_TOPIC)
