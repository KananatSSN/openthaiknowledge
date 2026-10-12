"""สมบัติกรด-เบสจากโครงสร้างของสารประกอบอินทรีย์

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/16

Sets moved here from: science_wave_e5.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e5 import SUBJECT, _labelled

PROVENANCE = Provenance("original")


TOPIC_ORGANIC_ACID_BASE = "สมบัติกรด-เบสจากโครงสร้างของสารประกอบอินทรีย์"


ACID, BASE, NEUTRAL = "กรด", "เบส", "กลาง (ไม่ใช่กรดหรือเบส)"


ACID_BASE_FILLER = "เป็นทั้งกรดและเบสพร้อมกัน"


ACID_BASE_FILLERS = (ACID_BASE_FILLER, "ขึ้นอยู่กับจำนวนอะตอมคาร์บอนในโมเลกุล",
                     "ขึ้นอยู่กับสถานะของสาร", "ขึ้นอยู่กับสีของสาร",
                     "เป็นกรดเฉพาะเมื่อร้อน และเป็นเบสเมื่อเย็น")


class OrganicItem(NamedTuple):
    name: str
    property: str


ORGANIC_ITEMS: tuple[OrganicItem, ...] = (
    OrganicItem("กรดอะซิติก (CH3-COOH)", ACID),
    OrganicItem("กรดฟอร์มิก (H-COOH)", ACID),
    OrganicItem("เมทิลเอมีน (CH3-NH2)", BASE),
    OrganicItem("เอทิลเอมีน (C2H5-NH2)", BASE),
    OrganicItem("เอทานอล (CH3-CH2-OH)", NEUTRAL),
    OrganicItem("มีเทน (CH4)", NEUTRAL),
    OrganicItem("กรดโพรพาโนอิก (CH3-CH2-COOH)", ACID),
    OrganicItem("กรดเบนโซอิก (C6H5-COOH)", ACID),
    OrganicItem("โพรพิลเอมีน (C3H7-NH2)", BASE),
    OrganicItem("แอนิลีน (C6H5-NH2)", BASE),
    OrganicItem("เมทานอล (CH3-OH)", NEUTRAL),
    OrganicItem("โพรเพน (CH3-CH2-CH3)", NEUTRAL),
)


# (a structural feature, the property it gives, and why)
ORGANIC_RULES = (
    ("สารประกอบอินทรีย์ที่มีหมู่คาร์บอกซิล (-COOH) มีสมบัติเป็นกรดหรือเบส", ACID,
     "หมู่คาร์บอกซิล (-COOH) แตกตัวให้ไฮโดรเจนไอออน (H+) จึงมีสมบัติเป็นกรด"),
    ("สารประกอบอินทรีย์ที่มีหมู่เอมีน (-NH2) มีสมบัติเป็นกรดหรือเบส", BASE,
     "หมู่เอมีน (-NH2) มีอะตอมไนโตรเจนที่รับโปรตอน (H+) ได้ จึงมีสมบัติเป็นเบส"),
    ("แอลกอฮอล์ซึ่งมีหมู่ไฮดรอกซิล (-OH) ต่อกับคาร์บอน มีสมบัติเป็นกรดหรือเบส", NEUTRAL,
     "หมู่ -OH ของแอลกอฮอล์ไม่แตกตัวให้ H+ หรือ OH- ในน้ำ จึงไม่แสดงสมบัติกรดหรือเบส"),
    ("ไฮโดรคาร์บอนซึ่งมีเพียงอะตอมคาร์บอนและไฮโดรเจน มีสมบัติเป็นกรดหรือเบส", NEUTRAL,
     "ไฮโดรคาร์บอนไม่มีหมู่ที่ให้หรือรับโปรตอน จึงไม่เป็นกรดหรือเบส"),
)


@question_type(
    "chem.organic_acid_base_foundation",
    display_name={"th": "หมู่คาร์บอกซิล (-COOH) ทำให้สารมีสมบัติเป็นกรดหรือเบส"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_ORGANIC_ACID_BASE,
)
class OrganicAcidBaseFoundation(QuestionType):
    """One structural rule at a time — not yet a named compound."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, property_, hint = rng.choice(ORGANIC_RULES)
        return _labelled(
            stem=stem,
            correct=property_,
            wrongs=(*(p for p in (ACID, BASE, NEUTRAL) if p != property_), *ACID_BASE_FILLERS),
            topic=TOPIC_ORGANIC_ACID_BASE,
            hint=hint,
        )


@question_type(
    "chem.organic_acid_base_fluency",
    display_name={"th": "สมบัติกรด-เบสของสารอินทรีย์ที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_ORGANIC_ACID_BASE,
)
class OrganicAcidBaseFluency(QuestionType):
    """Classify one named compound's structure directly — the whole indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ORGANIC_ITEMS)
        others = tuple(p for p in (ACID, BASE, NEUTRAL) if p != item.property)
        return _labelled(
            stem=f"{item.name} มีสมบัติความเป็นกรด-เบสอย่างไรจากโครงสร้าง",
            correct=item.property,
            wrongs=(*others, *ACID_BASE_FILLERS),
            topic=TOPIC_ORGANIC_ACID_BASE,
            hint="หมู่คาร์บอกซิล (-COOH) ทำให้เป็นกรด หมู่เอมีน (-NH2) ทำให้เป็นเบส และหมู่ไฮดรอกซิล (-OH) ของแอลกอฮอล์ไม่ใช่กรดหรือเบส",
        )


@question_type(
    "chem.organic_acid_base_application",
    display_name={"th": "สารในข้อใดมีสมบัติกรด-เบสที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_ORGANIC_ACID_BASE,
)
class OrganicAcidBaseApplication(QuestionType):
    """Reverse direction: given the property, pick the matching compound."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        property_ = rng.choice((ACID, BASE, NEUTRAL))
        same = [item for item in ORGANIC_ITEMS if item.property == property_]
        other = [item for item in ORGANIC_ITEMS if item.property != property_]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        return _labelled(
            stem=f"สารในข้อใดต่อไปนี้มีสมบัติเป็น{property_}",
            correct=correct.name,
            wrongs=tuple(w.name for w in wrongs),
            topic=TOPIC_ORGANIC_ACID_BASE,
            hint="หมู่คาร์บอกซิล (-COOH) ทำให้เป็นกรด หมู่เอมีน (-NH2) ทำให้เป็นเบส และหมู่ไฮดรอกซิล (-OH) ของแอลกอฮอล์ไม่ใช่กรดหรือเบส",
        )
