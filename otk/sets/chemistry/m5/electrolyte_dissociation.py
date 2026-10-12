"""การแตกตัวของสารและสารละลายอิเล็กโทรไลต์

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/13

Sets moved here from: science_wave_e4.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e4 import SUBJECT, _labelled

PROVENANCE = Provenance("original")


TOPIC_ELECTROLYTE = "การแตกตัวของสารและสารละลายอิเล็กโทรไลต์"


DISSOCIATES, DOES_NOT_DISSOCIATE = "แตกตัวเป็นไอออน", "ไม่แตกตัวเป็นไอออน"


ELECTROLYTE, NONELECTROLYTE = "สารละลายอิเล็กโทรไลต์", "สารละลายนอนอิเล็กโทรไลต์"


class DissociationItem(NamedTuple):
    name: str
    dissociates: bool


DISSOCIATION_ITEMS: tuple[DissociationItem, ...] = (
    DissociationItem("โซเดียมคลอไรด์ (เกลือแกง)", True),
    DissociationItem("กรดไฮโดรคลอริก (HCl)", True),
    DissociationItem("โพแทสเซียมไนเตรต (KNO3)", True),
    DissociationItem("โซเดียมไฮดรอกไซด์ (NaOH)", True),
    DissociationItem("กลูโคส (น้ำตาลกลูโคส)", False),
    DissociationItem("เอทานอล (แอลกอฮอล์)", False),
    DissociationItem("ยูเรีย", False),
    DissociationItem("ซูโครส (น้ำตาลทราย)", False),
    DissociationItem("แคลเซียมคลอไรด์ (CaCl2)", True),
    DissociationItem("กรดไนตริก (HNO3)", True),
    DissociationItem("แมกนีเซียมซัลเฟต (MgSO4)", True),
    DissociationItem("กลีเซอรอล", False),
    DissociationItem("อะซีโตน", False),
    DissociationItem("เมทานอล (CH3OH)", False),
)


_RULE = "เมื่อละลายน้ำจะแตกตัวเป็นไอออนหรือไม่"


_COVALENT = "สารโคเวเลนต์ทั่วไปที่ไม่ใช่กรดหรือเบส เช่น "


# As many "no" rules as "yes": with two choices, a set whose answer is
# usually the shorter label would be guessable by length.
ELECTROLYTE_RULES = (
    (f"สารประกอบไอออนิก{_RULE}", True),
    *((f"สารประกอบไอออนิก เช่น {name} {_RULE}", True)
      for name in ("โซเดียมคลอไรด์", "โพแทสเซียมคลอไรด์", "แคลเซียมคลอไรด์",
                   "แมกนีเซียมซัลเฟต", "โพแทสเซียมไนเตรต")),
    *((f"กรด เช่น {name} {_RULE}", True)
      for name in ("กรดไฮโดรคลอริก", "กรดไนตริก", "กรดซัลฟิวริก", "กรดแอซีติก")),
    *((f"เบส เช่น {name} {_RULE}", True)
      for name in ("โซเดียมไฮดรอกไซด์", "โพแทสเซียมไฮดรอกไซด์", "แคลเซียมไฮดรอกไซด์")),
    *((f"{_COVALENT}{name} {_RULE}", False)
      for name in ("น้ำตาล", "เอทานอล", "ยูเรีย", "กลูโคส", "ฟรักโทส", "แล็กโทส", "มอลโทส",
                   "กลีเซอรอล", "เมทานอล", "แอซีโตน", "เอทิลีนไกลคอล",
                   "ไอโซโพรพิลแอลกอฮอล์", "1-โพรพานอล")),
)


def _electrolyte_label(dissociates: bool) -> str:
    kind = DISSOCIATES if dissociates else DOES_NOT_DISSOCIATE
    result = ELECTROLYTE if dissociates else NONELECTROLYTE
    return f"{kind} ได้เป็น{result}"


@question_type(
    "chem.electrolyte_dissociation_foundation",
    display_name={"th": "สารประกอบไอออนิกละลายน้ำแตกตัวหรือไม่"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_ELECTROLYTE,
)
class ElectrolyteDissociationFoundation(QuestionType):
    """A general rule — not yet applied to one named substance."""
    max_choices = 2  # a bare yes/no label: fillers only padded it to four

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, dissociates = rng.choice(ELECTROLYTE_RULES)
        return _labelled(
            stem=stem,
            correct=DISSOCIATES if dissociates else DOES_NOT_DISSOCIATE,
            wrongs=(DOES_NOT_DISSOCIATE if dissociates else DISSOCIATES,),
            topic=TOPIC_ELECTROLYTE,
            hint="พันธะไอออนิกยึดไอออนบวกและลบไว้ด้วยแรงดึงดูดไฟฟ้าสถิต ซึ่งโมเลกุลน้ำที่มีขั้วแยกไอออนออกจากกันได้",
        )


@question_type(
    "chem.electrolyte_dissociation_fluency",
    display_name={"th": "สารที่กำหนดแตกตัวหรือไม่ และเป็นสารละลายชนิดใด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_ELECTROLYTE,
)
class ElectrolyteDissociationFluency(QuestionType):
    """Both facts at once — the whole ม.5/13 indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DISSOCIATION_ITEMS)
        other_label = _electrolyte_label(not item.dissociates)
        mismatched = (f"{DISSOCIATES if item.dissociates else DOES_NOT_DISSOCIATE} ได้เป็น"
                      f"{NONELECTROLYTE if item.dissociates else ELECTROLYTE}")
        return _labelled(
            stem=f"เมื่อละลายน้ำ {item.name} แตกตัวเป็นไอออนหรือไม่ และได้สารละลายชนิดใด",
            correct=_electrolyte_label(item.dissociates),
            wrongs=(other_label, mismatched, "ไม่ละลายน้ำ จึงไม่เกิดสารละลาย",
                    f"แตกตัวเป็นอะตอมที่เป็นกลาง ได้เป็น{NONELECTROLYTE}",
                    "ทำปฏิกิริยากับน้ำจนกลายเป็นแก๊สทั้งหมด"),
            topic=TOPIC_ELECTROLYTE,
            hint="สารประกอบไอออนิกและกรด-เบสแตกตัวเป็นไอออนได้สารละลายอิเล็กโทรไลต์ ส่วนสารโคเวเลนต์ทั่วไปไม่แตกตัว",
        )


@question_type(
    "chem.electrolyte_dissociation_application",
    display_name={"th": "สารในข้อใดได้สารละลายชนิดที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_ELECTROLYTE,
)
class ElectrolyteDissociationApplication(QuestionType):
    """Reverse direction: given the electrolyte class, pick the matching substance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        dissociates = rng.choice((True, False))
        same = [item for item in DISSOCIATION_ITEMS if item.dissociates == dissociates]
        other = [item for item in DISSOCIATION_ITEMS if item.dissociates != dissociates]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        result = ELECTROLYTE if dissociates else NONELECTROLYTE
        return _labelled(
            stem=f"สารในข้อใดต่อไปนี้เมื่อละลายน้ำแล้วได้{result}",
            correct=correct.name,
            wrongs=tuple(w.name for w in wrongs),
            topic=TOPIC_ELECTROLYTE,
            hint="สารประกอบไอออนิกและกรด-เบสแตกตัวเป็นไอออนได้สารละลายอิเล็กโทรไลต์ ส่วนสารโคเวเลนต์ทั่วไปไม่แตกตัว",
        )
