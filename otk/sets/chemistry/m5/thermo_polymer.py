"""โครงสร้างกับสมบัติเทอร์มอพลาสติกและเทอร์มอเซตของพอลิเมอร์

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/18

Sets moved here from: science_wave_e6.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e6 import SUBJECT, _labelled

PROVENANCE = Provenance("original")


TOPIC_THERMO_POLYMER = "โครงสร้างกับสมบัติเทอร์มอพลาสติกและเทอร์มอเซตของพอลิเมอร์"


THERMOPLASTIC, THERMOSET = "เทอร์มอพลาสติก", "เทอร์มอเซต"


class ThermoPolymerItem(NamedTuple):
    name: str
    kind: str


THERMO_POLYMER_ITEMS: tuple[ThermoPolymerItem, ...] = (
    ThermoPolymerItem("พอลิเอทิลีน (ถุงพลาสติก)", THERMOPLASTIC),
    ThermoPolymerItem("พอลิโพรพิลีน (กล่องพลาสติก)", THERMOPLASTIC),
    ThermoPolymerItem("พอลิไวนิลคลอไรด์ (ท่อ PVC)", THERMOPLASTIC),
    ThermoPolymerItem("เมลามีน (ภาชนะเมลามีน)", THERMOSET),
    ThermoPolymerItem("อีพอกซี (กาวสองส่วนผสม)", THERMOSET),
    ThermoPolymerItem("เบกาไลต์ (ด้ามจับหม้อ)", THERMOSET),
    ThermoPolymerItem("พอลิสไตรีน (กล่องโฟม)", THERMOPLASTIC),
    ThermoPolymerItem("พอลิเอทิลีนเทเรฟทาเลต (ขวดน้ำ PET)", THERMOPLASTIC),
    ThermoPolymerItem("ยูเรีย-ฟอร์มาลดีไฮด์ (เต้ารับและสวิตช์ไฟ)", THERMOSET),
    ThermoPolymerItem("พอลิเอสเตอร์เรซินเสริมใยแก้ว (ตัวเรือไฟเบอร์กลาส)", THERMOSET),
)


STRUCTURE_LABEL = {
    THERMOPLASTIC: "โครงสร้างเป็นสายโซ่ตรงหรือกิ่งก้านที่ไม่เชื่อมโยงกัน จึงอ่อนตัวเมื่อร้อนและขึ้นรูปใหม่ได้",
    THERMOSET: "โครงสร้างเป็นร่างแหที่เชื่อมโยงกันแน่นด้วยพันธะโคเวเลนต์ จึงแข็งตัวถาวรและขึ้นรูปใหม่ไม่ได้",
}


# What each kind does when heated again, the other way to describe it at Foundation.
BEHAVIOUR_LABEL = {
    THERMOPLASTIC: "อ่อนตัวเมื่อได้รับความร้อนและนำกลับมาหลอมขึ้นรูปใหม่ได้",
    THERMOSET: "ไม่อ่อนตัวเมื่อได้รับความร้อนอีก แต่จะแตกหรือไหม้เกรียม จึงหลอมขึ้นรูปใหม่ไม่ได้",
}


# More single facts about each kind, beside the two labels above. Each reads after
# ``พอลิเมอร์ที่`` and none is part of another, so a stem names one kind only.
MORE_CLUES = {
    THERMOPLASTIC: (
        "สายโซ่ยึดกันด้วยแรงยึดเหนี่ยวระหว่างโมเลกุลซึ่งอ่อน เมื่อได้รับความร้อนสายโซ่จึงเลื่อนผ่านกันได้",
        "นำไปหลอมแล้วรีไซเคิลเป็นผลิตภัณฑ์ใหม่ได้หลายครั้ง",
        "อ่อนนิ่มจนดัดหรือยืดเป็นรูปร่างใหม่ได้เมื่อได้รับความร้อน และกลับแข็งเมื่อเย็นลง",
    ),
    THERMOSET: (
        "สายโซ่ถูกยึดไขว้กันด้วยพันธะโคเวเลนต์จำนวนมากเป็นโครงข่ายสามมิติ",
        "ผ่านการบ่มหรือให้ความร้อนครั้งแรกแล้วเกิดการเชื่อมขวาง จึงคงรูปถาวร",
        "ทนความร้อนได้ดี เมื่อร้อนมากจะสลายตัวหรือไหม้เกรียมโดยไม่หลอมเหลว",
    ),
}


KIND_FILLERS = ("ทั้งสองประเภทพร้อมกัน", "ไม่จัดอยู่ในประเภทใด", "ยางธรรมชาติเท่านั้น", "โลหะผสม")


@question_type(
    "chem.thermo_polymer_foundation",
    display_name={"th": "โครงสร้างสายโซ่ที่ไม่เชื่อมโยงกันเป็นพอลิเมอร์ประเภทใด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_THERMO_POLYMER,
)
class ThermoPolymerFoundation(QuestionType):
    """One structural fact at a time — not yet the named polymer."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice((THERMOPLASTIC, THERMOSET))
        other = THERMOSET if kind == THERMOPLASTIC else THERMOPLASTIC
        clues = (f"มี{STRUCTURE_LABEL[kind]}", BEHAVIOUR_LABEL[kind], *MORE_CLUES[kind])
        stem = f"พอลิเมอร์ที่{rng.choice(clues)} จัดเป็นพอลิเมอร์ประเภทใด"
        return _labelled(
            stem=stem,
            correct=kind,
            wrongs=(other, *KIND_FILLERS),
            topic=TOPIC_THERMO_POLYMER,
            hint="เทอร์มอพลาสติกอ่อนตัวเมื่อร้อนและขึ้นรูปใหม่ได้ ส่วนเทอร์มอเซตแข็งตัวถาวรหลังขึ้นรูปครั้งแรก",
        )


@question_type(
    "chem.thermo_polymer_fluency",
    display_name={"th": "พอลิเมอร์ที่กำหนดเป็นเทอร์มอพลาสติกหรือเทอร์มอเซต และเพราะเหตุใด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_THERMO_POLYMER,
)
class ThermoPolymerFluency(QuestionType):
    """Name the type and its structural reason together — the whole indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(THERMO_POLYMER_ITEMS)
        other = THERMOSET if item.kind == THERMOPLASTIC else THERMOPLASTIC
        correct = f"{item.kind} เพราะ{STRUCTURE_LABEL[item.kind]}"
        wrong_swap = f"{other} เพราะ{STRUCTURE_LABEL[other]}"
        wrong_mismatch = f"{item.kind} เพราะ{STRUCTURE_LABEL[other]}"
        return _labelled(
            stem=f"{item.name} เป็นพอลิเมอร์ประเภทใด และเพราะเหตุใด",
            correct=correct,
            wrongs=(wrong_swap, wrong_mismatch, "ไม่สามารถจัดประเภทได้จากโครงสร้าง",
                    f"{other} เพราะ{STRUCTURE_LABEL[item.kind]}",
                    "เป็นได้ทั้งสองประเภท ขึ้นอยู่กับสีของผลิตภัณฑ์"),
            topic=TOPIC_THERMO_POLYMER,
            hint="ดูว่าโครงสร้างของพอลิเมอร์นี้เป็นสายโซ่อิสระ (ขึ้นรูปใหม่ได้) หรือร่างแหเชื่อมโยง (ขึ้นรูปใหม่ไม่ได้)",
        )


@question_type(
    "chem.thermo_polymer_application",
    display_name={"th": "พอลิเมอร์ในข้อใดจัดเป็นประเภทที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_THERMO_POLYMER,
)
class ThermoPolymerApplication(QuestionType):
    """Reverse direction: given the type, pick the matching polymer product."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice((THERMOPLASTIC, THERMOSET))
        same = [item for item in THERMO_POLYMER_ITEMS if item.kind == kind]
        other = [item for item in THERMO_POLYMER_ITEMS if item.kind != kind]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        return _labelled(
            stem=f"ผลิตภัณฑ์ในข้อใดต่อไปนี้ทำจากพอลิเมอร์ประเภท{kind}",
            correct=correct.name,
            wrongs=tuple(w.name for w in wrongs),
            topic=TOPIC_THERMO_POLYMER,
            hint="เทอร์มอพลาสติกขึ้นรูปใหม่ได้ (ถุง กล่อง ท่อพลาสติก) ส่วนเทอร์มอเซตขึ้นรูปใหม่ไม่ได้ (ภาชนะเมลามีน กาว ด้ามจับ)",
        )
