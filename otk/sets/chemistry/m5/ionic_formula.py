"""สูตรเคมีของไอออนและสารประกอบไอออนิก

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/12

Sets moved here from: science_wave_e4.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import math, text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e4 import SUBJECT

PROVENANCE = Provenance("original")


TOPIC_IONIC_FORMULA = "สูตรเคมีของไอออนและสารประกอบไอออนิก"


class IonItem(NamedTuple):
    name: str
    tex: str


ION_ITEMS: tuple[IonItem, ...] = (
    IonItem("โซเดียมไอออน", r"\mathrm{Na}^{+}"),
    IonItem("โพแทสเซียมไอออน", r"\mathrm{K}^{+}"),
    IonItem("แคลเซียมไอออน", r"\mathrm{Ca}^{2{+}}"),
    IonItem("อะลูมิเนียมไอออน", r"\mathrm{Al}^{3{+}}"),
    IonItem("แมกนีเซียมไอออน", r"\mathrm{Mg}^{2{+}}"),
    IonItem("คลอไรด์ไอออน", r"\mathrm{Cl}^{-}"),
    IonItem("ออกไซด์ไอออน", r"\mathrm{O}^{2{-}}"),
    IonItem("ซัลเฟตไอออน", r"\mathrm{SO}_4^{2{-}}"),
    IonItem("แอมโมเนียมไอออน", r"\mathrm{NH}_4^{+}"),
    IonItem("ไนเตรตไอออน", r"\mathrm{NO}_3^{-}"),
    IonItem("คาร์บอเนตไอออน", r"\mathrm{CO}_3^{2{-}}"),
    IonItem("ไฮดรอกไซด์ไอออน", r"\mathrm{OH}^{-}"),
)


class IonicCompound(NamedTuple):
    cation_name: str
    anion_name: str
    compound_name: str
    tex: str


IONIC_COMPOUNDS: tuple[IonicCompound, ...] = (
    IonicCompound("โซเดียมไอออน", "คลอไรด์ไอออน", "โซเดียมคลอไรด์", r"\mathrm{NaCl}"),
    IonicCompound("แคลเซียมไอออน", "คลอไรด์ไอออน", "แคลเซียมคลอไรด์", r"\mathrm{CaCl}_2"),
    IonicCompound("อะลูมิเนียมไอออน", "ออกไซด์ไอออน", "อะลูมิเนียมออกไซด์", r"\mathrm{Al}_2\mathrm{O}_3"),
    IonicCompound("แมกนีเซียมไอออน", "ซัลเฟตไอออน", "แมกนีเซียมซัลเฟต", r"\mathrm{MgSO}_4"),
    IonicCompound("แอมโมเนียมไอออน", "ไนเตรตไอออน", "แอมโมเนียมไนเตรต", r"\mathrm{NH}_4\mathrm{NO}_3"),
    IonicCompound("โพแทสเซียมไอออน", "คาร์บอเนตไอออน", "โพแทสเซียมคาร์บอเนต", r"\mathrm{K}_2\mathrm{CO}_3"),
    IonicCompound("แคลเซียมไอออน", "ไฮดรอกไซด์ไอออน", "แคลเซียมไฮดรอกไซด์", r"\mathrm{Ca}(\mathrm{OH})_2"),
)


@question_type(
    "chem.ionic_formula_foundation",
    display_name={"th": "เขียนสูตรเคมีของไอออน"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_IONIC_FORMULA,
)
class IonicFormulaFoundation(QuestionType):
    """The ion's own formula alone — not yet the compound it forms."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        correct = rng.choice(ION_ITEMS)
        wrongs = rng.sample([item for item in ION_ITEMS if item != correct], 3)
        return GeneratedQuestion(
            stem=[text(f"{correct.name}เขียนสูตรเคมีได้อย่างไร")],
            correct=[math(correct.tex)],
            distractors=fixed(*[[math(w.tex)] for w in wrongs]),
            topic=TOPIC_IONIC_FORMULA,
            hint=[text("สัญลักษณ์ธาตุตามด้วยประจุที่มุมบนขวา ไอออนหลายอะตอมมีสูตรและประจุรวมของกลุ่มอะตอมนั้น")],
        )


@question_type(
    "chem.ionic_formula_fluency",
    display_name={"th": "สูตรเคมีของสารประกอบไอออนิกจากไอออนที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_IONIC_FORMULA,
)
class IonicFormulaFluency(QuestionType):
    """Both formulas together — the whole ม.5/12 indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        correct = rng.choice(IONIC_COMPOUNDS)
        wrongs = rng.sample([item for item in IONIC_COMPOUNDS if item != correct], 3)
        return GeneratedQuestion(
            stem=[text(f"{correct.cation_name}กับ{correct.anion_name}รวมกันเป็นสารประกอบไอออนิก"
                       "ที่มีสูตรเคมีใด")],
            correct=[math(correct.tex)],
            distractors=fixed(*[[math(w.tex)] for w in wrongs]),
            topic=TOPIC_IONIC_FORMULA,
            hint=[text("ใช้ประจุของไอออนบวกเป็นตัวห้อยของไอออนลบ และประจุของไอออนลบเป็นตัวห้อยของไอออนบวก "
                       "แล้วลดตัวเลขให้เป็นอัตราส่วนอย่างต่ำ")],
        )


@question_type(
    "chem.ionic_formula_application",
    display_name={"th": "สูตรเคมีของสารประกอบไอออนิกจากชื่อสาร"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_IONIC_FORMULA,
)
class IonicFormulaApplication(QuestionType):
    """From the compound's common name, not from the ion pair handed over."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        correct = rng.choice(IONIC_COMPOUNDS)
        wrongs = rng.sample([item for item in IONIC_COMPOUNDS if item != correct], 3)
        return GeneratedQuestion(
            stem=[text(f"สารประกอบไอออนิกชื่อ \"{correct.compound_name}\" มีสูตรเคมีใด")],
            correct=[math(correct.tex)],
            distractors=fixed(*[[math(w.tex)] for w in wrongs]),
            topic=TOPIC_IONIC_FORMULA,
            hint=[text("ชื่อสารประกอบไอออนิกบอกทั้งไอออนบวกและไอออนลบที่ประกอบกันอยู่")],
        )
