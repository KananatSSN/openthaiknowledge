"""โรคทางพันธุกรรมจากยีนและโครโมโซม

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.3/5

Sets moved here from: science_wave_b26.
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
from otk.sets._support.science_wave_b25 import MIDDLE_THREE
from otk.sets._support.science_wave_b26 import DISEASE_SCENARIOS, DISEASE_TOPIC

PROVENANCE = Provenance("original")


class Disease(NamedTuple):
    """One genetic disease, the kind of change behind it, and its cause."""
    name: str
    kind: str
    cause: str


DISEASES = (
    Disease("โรคธาลัสซีเมีย", "การเปลี่ยนแปลงของยีน",
            "ยีนที่ควบคุมการสร้างสายโปรตีนของฮีโมโกลบินผิดปกติ "
            "เม็ดเลือดแดงจึงแตกง่ายและเกิดภาวะโลหิตจางเรื้อรัง"),
    Disease("โรคตาบอดสี", "การเปลี่ยนแปลงของยีน",
            "ยีนบนโครโมโซม X ที่ควบคุมการสร้างสารรับสีในจอตาผิดปกติ "
            "จึงแยกสีบางคู่ออกจากกันไม่ได้"),
    Disease("โรคฮีโมฟีเลีย", "การเปลี่ยนแปลงของยีน",
            "ยีนบนโครโมโซม X ที่ควบคุมการสร้างปัจจัยการแข็งตัวของเลือดผิดปกติ "
            "เลือดจึงหยุดไหลช้ากว่าปกติมาก"),
    Disease("ภาวะผิวเผือก", "การเปลี่ยนแปลงของยีน",
            "ยีนที่ควบคุมการสร้างเม็ดสีเมลานินผิดปกติ "
            "ผิวหนัง เส้นผม และตาจึงมีสีจางกว่าปกติ"),
    Disease("กลุ่มอาการดาวน์", "การเปลี่ยนแปลงของโครโมโซม",
            "มีโครโมโซมคู่ที่ 21 เกินมาหนึ่งแท่ง รวมเป็น 47 แท่ง"),
    Disease("กลุ่มอาการเทอร์เนอร์", "การเปลี่ยนแปลงของโครโมโซม",
            "มีโครโมโซมเพศเพียงแท่งเดียวคือ X รวมเป็น 45 แท่ง"),
    Disease("กลุ่มอาการไคลน์เฟลเตอร์", "การเปลี่ยนแปลงของโครโมโซม",
            "มีโครโมโซมเพศเป็น XXY รวมเป็น 47 แท่ง"),
    Disease("กลุ่มอาการเอ็ดเวิร์ด", "การเปลี่ยนแปลงของโครโมโซม",
            "มีโครโมโซมคู่ที่ 18 เกินมาหนึ่งแท่ง รวมเป็น 47 แท่ง"),
)


@question_type(
    "life.genetic_disease_foundation",
    display_name={"th": "การเปลี่ยนแปลงของยีนหรือโครโมโซมกับโรค"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=DISEASE_TOPIC,
)
class GeneticDiseaseFoundation(QuestionType):
    """Say what kind of change causes a named disease, and how."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DISEASES)
        others = [other.cause for other in DISEASES if other.name != item.name]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.name}” เกิดจากอะไร",
            correct=item.cause, wrongs=tuple(others[:3]),
            hint="แยกให้ออกว่าเป็นความผิดปกติที่ยีนหนึ่งยีน "
                 "หรือเป็นจำนวนโครโมโซมทั้งแท่งที่ผิดไป",
            topic=DISEASE_TOPIC,
        )


@question_type(
    "life.genetic_disease_fluency",
    display_name={"th": "ยกตัวอย่างโรคทางพันธุกรรมแต่ละแบบ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=DISEASE_TOPIC,
)
class GeneticDiseaseFluency(QuestionType):
    """Name a disease of the stated kind — ``ยกตัวอย่าง`` itself."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DISEASES)
        others = [other.name for other in DISEASES if other.kind != item.kind]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"โรคหรือกลุ่มอาการใดเกิดจาก{item.kind}",
                correct=item.name, wrongs=tuple(others[:3]),
                hint="โรคที่เกิดจากโครโมโซมมักทำให้จำนวนโครโมโซมทั้งแท่ง"
                     "ผิดไปจาก 46",
                topic=DISEASE_TOPIC,
            )
        wrong_kind = ("การเปลี่ยนแปลงของโครโมโซม"
                      if item.kind == "การเปลี่ยนแปลงของยีน"
                      else "การเปลี่ยนแปลงของยีน")
        return _labelled(
            stem=f"“{item.name}” จัดเป็นโรคทางพันธุกรรมที่เกิดจากสิ่งใด",
            correct=f"{item.kind} ซึ่งถ่ายทอดไปสู่รุ่นลูกได้",
            wrongs=(f"{wrong_kind} ซึ่งถ่ายทอดไปสู่รุ่นลูกได้",
                    "การติดเชื้อโรคจากผู้อื่นในระหว่างตั้งครรภ์",
                    "พฤติกรรมการใช้ชีวิตของผู้ป่วยเองหลังจากเกิดมาแล้ว"),
            hint="โรคทางพันธุกรรมเกิดจากสารพันธุกรรม ไม่ใช่จากการติดเชื้อ"
                 "หรือพฤติกรรม",
            topic=DISEASE_TOPIC,
        )


@question_type(
    "life.genetic_disease_application",
    display_name={"th": "วิเคราะห์โรคทางพันธุกรรม"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=DISEASE_TOPIC,
)
class GeneticDiseaseApplication(QuestionType):
    """Read a test result or a claim about inheritance of disease."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, DISEASE_SCENARIOS,
            hint="ถามก่อนว่าความผิดปกติอยู่ที่ยีนหนึ่งยีนหรือที่โครโมโซมทั้งแท่ง "
                 "และจำไว้ว่าโรคทางพันธุกรรมไม่ติดต่อ",
        ), DISEASE_TOPIC)
