"""ไฮโดรคาร์บอนอิ่มตัวและไม่อิ่มตัวจากสูตรโครงสร้าง

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/14

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


TOPIC_SATURATION = "ไฮโดรคาร์บอนอิ่มตัวและไม่อิ่มตัวจากสูตรโครงสร้าง"


SATURATED, UNSATURATED = "ไฮโดรคาร์บอนอิ่มตัว", "ไฮโดรคาร์บอนไม่อิ่มตัว"


SATURATION_FILLERS = ("สารอินทรีย์ที่ไม่ใช่ไฮโดรคาร์บอน", "เป็นทั้งสองแบบพร้อมกัน", "ไม่จัดเป็นสารอินทรีย์",
                      "ขึ้นกับจำนวนไฮโดรเจน")


class HydrocarbonItem(NamedTuple):
    name: str
    saturated: bool


HYDROCARBON_ITEMS: tuple[HydrocarbonItem, ...] = (
    HydrocarbonItem("มีเทน (CH4)", True),
    HydrocarbonItem("อีเทน (H3C-CH3)", True),
    HydrocarbonItem("โพรเพน (CH3-CH2-CH3)", True),
    HydrocarbonItem("เอทีน (H2C=CH2)", False),
    HydrocarbonItem("โพรพีน (CH2=CH-CH3)", False),
    HydrocarbonItem("อีไทน์ (HC≡CH)", False),
    HydrocarbonItem("บิวเทน (CH3-CH2-CH2-CH3)", True),
    HydrocarbonItem("เพนเทน (CH3-CH2-CH2-CH2-CH3)", True),
    HydrocarbonItem("2-เมทิลโพรเพน (CH3-CH(CH3)-CH3)", True),
    HydrocarbonItem("ไซโคลเฮกเซน (C6H12 วงหกเหลี่ยม พันธะเดี่ยวทุกพันธะ)", True),
    HydrocarbonItem("1-บิวทีน (CH2=CH-CH2-CH3)", False),
    HydrocarbonItem("โพรไพน์ (HC≡C-CH3)", False),
    HydrocarbonItem("1,3-บิวทาไดอีน (CH2=CH-CH=CH2)", False),
    HydrocarbonItem("ไซโคลเฮกซีน (C6H10 วงหกเหลี่ยม มีพันธะคู่หนึ่งพันธะ)", False),
    HydrocarbonItem("เฮกเซน (CH3-CH2-CH2-CH2-CH2-CH3)", True),
    HydrocarbonItem("เฮปเทน (CH3-(CH2)5-CH3)", True),
    HydrocarbonItem("2-เมทิลบิวเทน (CH3-CH(CH3)-CH2-CH3)", True),
    HydrocarbonItem("2,2-ไดเมทิลโพรเพน (C(CH3)4)", True),
    HydrocarbonItem("ไซโคลโพรเพน (C3H6 วงสามเหลี่ยม พันธะเดี่ยวทุกพันธะ)", True),
    HydrocarbonItem("ไซโคลเพนเทน (C5H10 วงห้าเหลี่ยม พันธะเดี่ยวทุกพันธะ)", True),
    HydrocarbonItem("2-บิวทีน (CH3-CH=CH-CH3)", False),
    HydrocarbonItem("1-เพนทีน (CH2=CH-CH2-CH2-CH3)", False),
    HydrocarbonItem("2-เมทิลโพรพีน (CH2=C(CH3)-CH3)", False),
    HydrocarbonItem("1-บิวไทน์ (HC≡C-CH2-CH3)", False),
    HydrocarbonItem("2-บิวไทน์ (CH3-C≡C-CH3)", False),
    HydrocarbonItem("ไซโคลเพนทีน (C5H8 วงห้าเหลี่ยม มีพันธะคู่หนึ่งพันธะ)", False),
)


# (a general statement about carbon-carbon bonds, whether it describes a saturated hydrocarbon)
SATURATION_RULES = (
    ("สารประกอบไฮโดรคาร์บอนที่มีพันธะเดี่ยวระหว่างคาร์บอนทุกพันธะจัดเป็นไฮโดรคาร์บอนประเภทใด", True),
    ("สารประกอบไฮโดรคาร์บอนที่มีพันธะคู่ระหว่างคาร์บอนอย่างน้อยหนึ่งพันธะจัดเป็นไฮโดรคาร์บอนประเภทใด", False),
    ("สารประกอบไฮโดรคาร์บอนที่มีพันธะสามระหว่างคาร์บอนอย่างน้อยหนึ่งพันธะจัดเป็นไฮโดรคาร์บอนประเภทใด", False),
    ("แอลเคนซึ่งมีพันธะเดี่ยวระหว่างคาร์บอนทั้งหมดจัดเป็นไฮโดรคาร์บอนประเภทใด", True),
    ("แอลคีนซึ่งมีพันธะคู่ระหว่างคาร์บอนจัดเป็นไฮโดรคาร์บอนประเภทใด", False),
    ("แอลไคน์ซึ่งมีพันธะสามระหว่างคาร์บอนจัดเป็นไฮโดรคาร์บอนประเภทใด", False),
    ("ไฮโดรคาร์บอนแบบวงที่มีพันธะเดี่ยวระหว่างคาร์บอนทุกพันธะจัดเป็นไฮโดรคาร์บอนประเภทใด", True),
)


@question_type(
    "chem.hydrocarbon_saturation_foundation",
    display_name={"th": "พันธะเดี่ยวทุกพันธะระหว่างคาร์บอนจัดเป็นไฮโดรคาร์บอนประเภทใด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_SATURATION,
)
class HydrocarbonSaturationFoundation(QuestionType):
    """A general rule about the carbon-carbon bonds — not yet applied to a named hydrocarbon."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, saturated = rng.choice(SATURATION_RULES)
        return _labelled(
            stem=stem,
            correct=SATURATED if saturated else UNSATURATED,
            wrongs=(UNSATURATED if saturated else SATURATED, *SATURATION_FILLERS),
            topic=TOPIC_SATURATION,
            hint="ไฮโดรคาร์บอนไม่อิ่มตัวต้องมีพันธะคู่หรือพันธะสามระหว่างคาร์บอนอย่างน้อยหนึ่งพันธะ",
        )


@question_type(
    "chem.hydrocarbon_saturation_fluency",
    display_name={"th": "สารไฮโดรคาร์บอนที่กำหนดอิ่มตัวหรือไม่"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_SATURATION,
)
class HydrocarbonSaturationFluency(QuestionType):
    """Classify one named hydrocarbon directly — the whole ม.5/14 indicator."""
    max_choices = 2  # a bare yes/no label: fillers only padded it to four

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(HYDROCARBON_ITEMS)
        correct = SATURATED if item.saturated else UNSATURATED
        other = UNSATURATED if item.saturated else SATURATED
        return _labelled(
            stem=f"{item.name} เป็นไฮโดรคาร์บอนอิ่มตัวหรือไม่อิ่มตัว",
            correct=correct,
            wrongs=(other,),
            topic=TOPIC_SATURATION,
            hint="ดูสูตรโครงสร้างว่ามีพันธะคู่หรือพันธะสามระหว่างอะตอมคาร์บอนหรือไม่",
        )


@question_type(
    "chem.hydrocarbon_saturation_application",
    display_name={"th": "สารในข้อใดจัดอยู่ในประเภทไฮโดรคาร์บอนที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_SATURATION,
)
class HydrocarbonSaturationApplication(QuestionType):
    """Reverse direction: given the saturation type, pick the matching hydrocarbon."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        saturated = rng.choice((True, False))
        same = [item for item in HYDROCARBON_ITEMS if item.saturated == saturated]
        other = [item for item in HYDROCARBON_ITEMS if item.saturated != saturated]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        kind = SATURATED if saturated else UNSATURATED
        return _labelled(
            stem=f"สารในข้อใดต่อไปนี้จัดเป็น{kind}",
            correct=correct.name,
            wrongs=tuple(w.name for w in wrongs),
            topic=TOPIC_SATURATION,
            hint="ดูสูตรโครงสร้างว่ามีพันธะคู่หรือพันธะสามระหว่างอะตอมคาร์บอนหรือไม่",
        )
