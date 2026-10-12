"""หัวใจ หลอดเลือด และเลือด

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/6

Sets moved here from: science_wave_b10.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import LEVEL, SUBJECT, TOPIC, labelled, scenario_question
from otk.sets._support.science_wave_b10 import CIRCULATORY_SCENARIOS

PROVENANCE = Provenance("original")


class Part(NamedTuple):
    """One structure and the single job it does."""
    name: str
    function: str


HEART_PARTS = (
    Part("หัวใจห้องบนขวา",
         "รับเลือดที่มีออกซิเจนต่ำซึ่งไหลกลับมาจากส่วนต่าง ๆ ของร่างกาย"),
    Part("หัวใจห้องล่างขวา", "สูบฉีดเลือดที่มีออกซิเจนต่ำออกไปยังปอด"),
    Part("หัวใจห้องบนซ้าย", "รับเลือดที่มีออกซิเจนสูงซึ่งไหลกลับมาจากปอด"),
    Part("หัวใจห้องล่างซ้าย",
         "สูบฉีดเลือดที่มีออกซิเจนสูงออกไปเลี้ยงส่วนต่าง ๆ ของร่างกาย"),
    Part("ลิ้นหัวใจ", "กั้นไม่ให้เลือดไหลย้อนกลับขณะหัวใจบีบตัว"),
)


BLOOD_PARTS = (
    Part("เซลล์เม็ดเลือดแดง",
         "ลำเลียงแก๊สออกซิเจนไปยังเซลล์ทั่วร่างกาย โดยมีฮีโมโกลบินเป็นตัวจับออกซิเจน"),
    Part("เซลล์เม็ดเลือดขาว", "ทำลายเชื้อโรคและสิ่งแปลกปลอมที่เข้าสู่ร่างกาย"),
    Part("เกล็ดเลือด", "ช่วยให้เลือดแข็งตัวเมื่อหลอดเลือดฉีกขาด"),
    Part("น้ำเลือด",
         "เป็นของเหลวที่ลำเลียงสารอาหาร ของเสีย และเซลล์เม็ดเลือดไปตามหลอดเลือด"),
)


# Four statements true of each vessel and of no other. Three vessel names would
# give a three-choice item, so the item offers statements instead of names.
VESSEL_FACTS = {
    "หลอดเลือดแดง": (
        "นำเลือดออกจากหัวใจไปยังส่วนต่าง ๆ ของร่างกาย",
        "มีผนังหนาและยืดหยุ่นเพื่อรองรับความดันเลือดที่สูง",
        "เลือดภายในไหลเป็นจังหวะตามการบีบตัวของหัวใจ จึงจับชีพจรได้",
        "ผนังมีกล้ามเนื้อเรียบหนา จึงหดและขยายเพื่อควบคุมปริมาณเลือดที่ไหลผ่านได้",
    ),
    "หลอดเลือดดำ": (
        "นำเลือดจากส่วนต่าง ๆ ของร่างกายกลับเข้าสู่หัวใจ",
        "มีผนังบางกว่าและยืดหยุ่นน้อยกว่า เพราะความดันเลือดภายในต่ำ",
        "มีลิ้นกั้นเป็นระยะเพื่อกันไม่ให้เลือดไหลย้อนกลับ",
        "อยู่ตื้นใกล้ผิวหนังในหลายบริเวณจนมองเห็นเป็นเส้นได้",
    ),
    "หลอดเลือดฝอย": (
        "มีผนังบางเพียงชั้นเดียวของเซลล์",
        "เป็นบริเวณที่เกิดการแลกเปลี่ยนแก๊สและสารระหว่างเลือดกับเซลล์",
        "แทรกอยู่ทั่วเนื้อเยื่อจนเซลล์เกือบทุกเซลล์อยู่ใกล้หลอดเลือดชนิดนี้",
        "เลือดไหลผ่านช้าที่สุดในบรรดาหลอดเลือดทั้งสามชนิด",
    ),
}


@question_type(
    "body.circulatory_parts_foundation",
    display_name={"th": "โครงสร้างของหัวใจและส่วนประกอบของเลือด"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class CirculatoryPartsFoundation(QuestionType):
    """Name a structure's job, or the structure that does a job.

    Heart parts and blood parts are drawn as separate tables. Mixing them would
    offer หัวใจห้องล่างซ้าย as a distractor for a question about เกล็ดเลือด, which
    tests nothing.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        heart = rng.random() < 0.5
        parts = HEART_PARTS if heart else BLOOD_PARTS
        group = "หัวใจ" if heart else "เลือด"
        item = rng.choice(parts)
        others = [other for other in parts if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return labelled(
                stem=f"“{item.name}” ทำหน้าที่ใด",
                correct=item.function,
                wrongs=tuple(other.function for other in others[:3]),
                hint="สำหรับหัวใจให้แยกว่ารับเลือดเข้าหรือสูบเลือดออก และเลือดนั้นมี"
                     "ออกซิเจนสูงหรือต่ำ สำหรับเลือดให้แยกว่าเป็นเซลล์หรือของเหลว",
            )
        return labelled(
            stem=f"ส่วนใดของ{group}ทำหน้าที่{item.function}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกส่วนที่ทำหน้าที่นั้นโดยตรง",
        )


@question_type(
    "body.blood_vessels_fluency",
    display_name={"th": "เปรียบเทียบหลอดเลือดแดง หลอดเลือดดำ และหลอดเลือดฝอย"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class BloodVesselsFluency(QuestionType):
    """Which statement is true of the vessel named in the stem.

    Three vessels would give three choices if asked by name, so the item offers
    four statements and every wrong one is true of a different vessel.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        vessel = rng.choice(sorted(VESSEL_FACTS))
        theirs = [fact for name, facts in VESSEL_FACTS.items()
                  if name != vessel for fact in facts]
        rng.shuffle(theirs)
        return labelled(
            stem=f"ข้อใดเป็นจริงเกี่ยวกับ “{vessel}”",
            correct=rng.choice(VESSEL_FACTS[vessel]),
            wrongs=tuple(theirs[:3]),
            hint="เริ่มที่ทิศทางของเลือดเทียบกับหัวใจ แล้วจึงดูความหนาของผนัง "
                 "และดูว่าเป็นที่แลกเปลี่ยนสารหรือไม่",
        )


@question_type(
    "body.circulatory_application",
    display_name={"th": "วิเคราะห์โครงสร้างของหัวใจ หลอดเลือด และเลือด"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class CirculatoryApplication(QuestionType):
    """Explain an observation by the structure that produces it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, CIRCULATORY_SCENARIOS,
            hint="ถามว่าโครงสร้างนั้นต้องรับความดันเท่าใด ต้องลำเลียงอะไร "
                 "และต้องให้สารผ่านเข้าออกได้หรือไม่",
        )
