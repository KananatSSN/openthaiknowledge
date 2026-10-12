"""ความสัมพันธ์ระหว่างสิ่งมีชีวิตกับสิ่งมีชีวิตและสิ่งไม่มีชีวิต

ชีวะ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 1.1 ป.5/2

Sets moved here from: science_wave_b32.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import Fact, _fact_question
from otk.sets._support.science_wave_b24 import PRIMARY_FIVE
from otk.sets._support.science_wave_b31 import ECOLOGY_TOPIC
from otk.sets._support.science_wave_b32 import CONSEQUENCES, LIVING, NON_LIVING, RELATION_SCENARIOS

PROVENANCE = Provenance("original")


class Relation(NamedTuple):
    """One relationship, stated, and which of the two kinds it is."""
    statement: str
    kind: str


RELATIONS = (
    Relation("ผึ้งกินน้ำหวานจากดอกไม้ และช่วยถ่ายเรณูให้ดอกไม้", LIVING),
    Relation("นกเอี้ยงกินแมลงที่เกาะอยู่บนหลังควาย ควายจึงไม่ถูกแมลงรบกวน", LIVING),
    Relation("กาฝากแทงรากเข้าไปดูดน้ำและอาหารจากต้นมะม่วง", LIVING),
    Relation("งูกินหนูนาเป็นอาหาร", LIVING),
    Relation("กล้วยไม้เกาะอยู่บนกิ่งของต้นไม้ใหญ่เพื่อรับแสง", LIVING),
    Relation("ต้นไม้ใช้แสงแดดในการสร้างอาหาร", NON_LIVING),
    Relation("ปลาใช้อากาศที่ละลายอยู่ในน้ำในการหายใจ", NON_LIVING),
    Relation("ไส้เดือนดินใช้ดินที่ชื้นเป็นที่อยู่อาศัย", NON_LIVING),
    Relation("ปูเสฉวนใช้เปลือกหอยเปล่าเป็นที่อยู่และที่หลบภัย", NON_LIVING),
    Relation("นกใช้กิ่งไม้แห้งและใบหญ้าแห้งสร้างรัง", NON_LIVING),
)


RELATION_FACTS = (
    Fact("สิ่งไม่มีชีวิตที่พืชต้องใช้ในการสร้างอาหารมีอะไรบ้าง",
         "แสง น้ำ และแก๊สคาร์บอนไดออกไซด์"),
    Fact("สัตว์ได้ประโยชน์จากพืชในด้านใดบ้าง",
         "ได้พืชเป็นอาหาร และได้ใช้พืชเป็นที่อยู่อาศัยหรือที่หลบภัย"),
    Fact("พืชบางชนิดได้ประโยชน์จากสัตว์ในด้านใด",
         "ได้รับการถ่ายเรณู และได้รับการช่วยพาเมล็ดไปงอกในที่ใหม่"),
    Fact("ดินมีความสำคัญต่อพืชอย่างไร",
         "เป็นที่ยึดเกาะของราก และมีน้ำกับธาตุอาหารให้รากดูดขึ้นไปใช้"),
    Fact("เหตุใดสัตว์ส่วนใหญ่จึงขาดอากาศไม่ได้",
         "เพราะต้องใช้แก๊สออกซิเจนในอากาศในการหายใจ"),
    Fact("ผู้ล่ามีความสำคัญต่อจำนวนของเหยื่ออย่างไร",
         "ช่วยควบคุมจำนวนเหยื่อไม่ให้เพิ่มขึ้นมากเกินไป"),
)


@question_type(
    "ecology.living_relations_foundation",
    display_name={"th": "ความสัมพันธ์ของสิ่งมีชีวิตกับสิ่งรอบตัว"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class LivingRelationsFoundation(QuestionType):
    """Say what one relationship gives, or tell the two kinds apart."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            return _fact_question(
                rng, RELATION_FACTS, topic=ECOLOGY_TOPIC,
                hint="แยกให้ออกว่าสิ่งมีชีวิตได้อะไรจากสิ่งมีชีวิตอื่น "
                     "และได้อะไรจากสิ่งไม่มีชีวิต",
            )
        kind = rng.choice((LIVING, NON_LIVING))
        item = rng.choice([one for one in RELATIONS if one.kind == kind])
        others = [one.statement for one in RELATIONS if one.kind != kind]
        rng.shuffle(others)
        return _labelled(
            stem=f"ข้อใดเป็นความสัมพันธ์ระหว่าง{kind}",
            correct=item.statement, wrongs=tuple(others[:3]),
            hint="ดูสิ่งที่สิ่งมีชีวิตในข้อนั้นเกี่ยวข้องด้วย ว่ามีชีวิตหรือไม่มีชีวิต",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.living_relations_fluency",
    display_name={"th": "อธิบายผลของความสัมพันธ์ต่อการดำรงชีวิต"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class LivingRelationsFluency(QuestionType):
    """Predict what happens to one side when the other side changes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CONSEQUENCES)
        return _labelled(
            stem=item.stem, correct=item.correct, wrongs=tuple(item.wrongs),
            hint="นึกก่อนว่าสิ่งมีชีวิตนั้นได้อะไรจากอีกฝ่าย "
                 "แล้วถามว่าเมื่อสิ่งนั้นหายไปจะเกิดอะไรขึ้น",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.living_relations_application",
    display_name={"th": "วิเคราะห์ความสัมพันธ์ในสิ่งแวดล้อม"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class LivingRelationsApplication(QuestionType):
    """Follow a change through more than one relationship."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, RELATION_SCENARIOS,
            hint="ตามผลไปทีละขั้น ว่าสิ่งที่เปลี่ยนไปเคยให้อะไรแก่ใคร",
        ), ECOLOGY_TOPIC)
