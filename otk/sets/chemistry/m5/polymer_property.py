"""สมบัติทางกายภาพของพอลิเมอร์เทียบกับมอนอเมอร์

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/15

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


TOPIC_POLYMER = "สมบัติทางกายภาพของพอลิเมอร์เทียบกับมอนอเมอร์"


HIGHER, LOWER = "สูงกว่า", "ต่ำกว่า"


COMPARISON_FILLERS = ("เท่ากันเสมอ", "ไม่สามารถเปรียบเทียบกันได้",
                      "สูงกว่าเฉพาะมวลโมเลกุล แต่จุดหลอมเหลวต่ำกว่า",
                      "ต่ำกว่าเฉพาะมวลโมเลกุล แต่จุดหลอมเหลวสูงกว่า")


class PolymerItem(NamedTuple):
    polymer_name: str
    monomer_name: str


POLYMER_ITEMS: tuple[PolymerItem, ...] = (
    PolymerItem("พอลิเอทิลีน (พลาสติกถุง)", "เอทิลีน (แก๊ส)"),
    PolymerItem("พอลิสไตรีน (โฟม)", "สไตรีน (ของเหลว)"),
    PolymerItem("พอลิไวนิลคลอไรด์ (PVC)", "ไวนิลคลอไรด์ (แก๊ส)"),
    PolymerItem("พอลิโพรพิลีน (กล่องพลาสติก)", "โพรพิลีน (แก๊ส)"),
    PolymerItem("พอลิเตตระฟลูออโรเอทิลีน (เทฟลอนเคลือบกระทะ)", "เตตระฟลูออโรเอทิลีน (แก๊ส)"),
    PolymerItem("พอลิเมทิลเมทาคริเลต (แผ่นอะคริลิก)", "เมทิลเมทาคริเลต (ของเหลว)"),
    PolymerItem("ยางธรรมชาติ (พอลิไอโซพรีน)", "ไอโซพรีน (ของเหลว)"),
    PolymerItem("พอลิอะคริโลไนไตรล์ (เส้นใยอะคริลิก)", "อะคริโลไนไตรล์ (ของเหลว)"),
)


POLYMER_FACTS = (
    ("พอลิเมอร์มีมวลโมเลกุลและจุดหลอมเหลวสูงกว่าหรือต่ำกว่ามอนอเมอร์ของมัน", HIGHER, (LOWER, *COMPARISON_FILLERS)),
    ("พอลิเมอร์เกิดขึ้นได้อย่างไร",
     "มอนอเมอร์จำนวนมากเชื่อมต่อกันด้วยพันธะโคเวเลนต์เป็นสายโซ่ยาว",
     ("พอลิเมอร์หลายสายหลอมรวมกันเป็นมอนอเมอร์ขนาดใหญ่เพียงโมเลกุลเดียว", "มอนอเมอร์สองโมเลกุลรวมกันเท่านั้น",
      "อะตอมโลหะเรียงตัวกันเป็นผลึกด้วยพันธะโลหะ", "ไอออนบวกและไอออนลบดึงดูดกันเป็นโครงผลึก", "มอนอเมอร์ละลายรวมกันในน้ำจนกลายเป็นสารละลายข้นหนืด", "มอนอเมอร์ละลายในน้ำจนเป็นเนื้อเดียว")),
    ("เหตุใดเอทิลีนจึงเป็นแก๊สที่อุณหภูมิห้อง แต่พอลิเอทิลีนเป็นของแข็ง",
     "พอลิเอทิลีนเป็นโมเลกุลสายยาวมวลมาก แรงระหว่างโมเลกุลจึงมากกว่าเอทิลีน",
     ("เอทิลีนมีมวลโมเลกุลมากกว่าพอลิเอทิลีน", "พอลิเอทิลีนมีโมเลกุลเล็กกว่าจึงอัดกันแน่นเป็นของแข็ง",
      "เอทิลีนมีพันธะคู่จึงเป็นแก๊ส ส่วนพอลิเอทิลีนไม่มีพันธะคู่เหลืออยู่เลย", "พอลิเอทิลีนมีขั้วมากกว่าเอทิลีน จึงเกิดพันธะไฮโดรเจนระหว่างสายได้", "พอลิเอทิลีนมีน้ำผสมอยู่จึงแข็งตัว", "ทั้งสองเป็นสารชนิดเดียวกันแต่ต่างสีกันเท่านั้น")),
    ("เมื่อมอนอเมอร์เชื่อมต่อกันเป็นพอลิเมอร์ มวลโมเลกุลเปลี่ยนไปอย่างไร",
     "เพิ่มขึ้นมาก เพราะพอลิเมอร์รวมมอนอเมอร์จำนวนมากไว้ในโมเลกุลเดียว",
     ("ลดลงเหลือครึ่งหนึ่ง เพราะเสียน้ำออกไป", "เท่าเดิม เพราะเป็นธาตุชนิดเดียวกันกับมอนอเมอร์", "ลดลง เพราะอะตอมบางส่วนหายไป",
      "เพิ่มขึ้นเพียงสองเท่าเสมอ เพราะมอนอเมอร์ต่อกันเป็นคู่เท่านั้น", "ลดลงมาก เพราะพันธะคู่ของมอนอเมอร์ถูกทำลายไปจนหมด", "เปลี่ยนเป็นศูนย์ เพราะพอลิเมอร์ไม่มีมวล")),
)


def _polymer_label(comparison: str) -> str:
    reason = ("เพราะเป็นสายโซ่ยาวจากมอนอเมอร์จำนวนมากเชื่อมต่อกัน"
              if comparison == HIGHER else "เพราะมีขนาดโมเลกุลเล็กกว่าพอลิเมอร์ของมัน")
    return f"มีมวลโมเลกุลและจุดหลอมเหลว{comparison}มอนอเมอร์ {reason}"


@question_type(
    "chem.polymer_property_foundation",
    display_name={"th": "พอลิเมอร์มีมวลโมเลกุลและจุดหลอมเหลวสูงหรือต่ำกว่ามอนอเมอร์"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_POLYMER,
)
class PolymerPropertyFoundation(QuestionType):
    """A general fact about polymers and monomers — not yet a named pair."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(POLYMER_FACTS)
        return _labelled(
            stem=stem,
            correct=correct,
            wrongs=wrongs,
            topic=TOPIC_POLYMER,
            hint="พอลิเมอร์เป็นสายโซ่ยาวที่เกิดจากมอนอเมอร์จำนวนมากเชื่อมต่อกัน จึงมีมวลโมเลกุลมากกว่ามอนอเมอร์เดี่ยว",
        )


@question_type(
    "chem.polymer_property_fluency",
    display_name={"th": "สมบัติทางกายภาพของพอลิเมอร์ที่กำหนดเทียบกับมอนอเมอร์"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_POLYMER,
)
class PolymerPropertyFluency(QuestionType):
    """Compare one named polymer with its own monomer — the whole indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(POLYMER_ITEMS)
        return _labelled(
            stem=f"{item.polymer_name} มีสมบัติทางกายภาพอย่างไรเมื่อเทียบกับมอนอเมอร์ของมันคือ {item.monomer_name}",
            correct=_polymer_label(HIGHER),
            wrongs=(_polymer_label(LOWER), *COMPARISON_FILLERS),
            topic=TOPIC_POLYMER,
            hint="พอลิเมอร์เป็นสายโซ่ยาวที่เกิดจากมอนอเมอร์จำนวนมากเชื่อมต่อกัน จึงมีมวลโมเลกุลมากกว่ามอนอเมอร์เดี่ยวเสมอ",
        )


@question_type(
    "chem.polymer_property_application",
    display_name={"th": "มอนอเมอร์ในข้อใดตรงกับพอลิเมอร์ที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_POLYMER,
)
class PolymerPropertyApplication(QuestionType):
    """Reverse direction: given the polymer, pick its own monomer."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        correct = rng.choice(POLYMER_ITEMS)
        wrongs = rng.sample([item for item in POLYMER_ITEMS if item != correct], 3)
        return _labelled(
            stem=f"มอนอเมอร์ของ {correct.polymer_name} คือข้อใด",
            correct=correct.monomer_name,
            wrongs=tuple(w.monomer_name for w in wrongs),
            topic=TOPIC_POLYMER,
            hint="มอนอเมอร์คือหน่วยเล็กที่เชื่อมต่อกันซ้ำ ๆ จนเกิดเป็นพอลิเมอร์",
        )
