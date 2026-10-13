"""การเกิดพันธะไฮโดรเจนจากสูตรโครงสร้าง

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/10

Sets moved here from: science_wave_e3.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e3 import SUBJECT, _labelled

PROVENANCE = Provenance("original")


TOPIC_HYDROGEN_BOND = "การเกิดพันธะไฮโดรเจนจากสูตรโครงสร้าง"


CAN_H_BOND, CANNOT_H_BOND = "เกิดพันธะไฮโดรเจนได้", "ไม่เกิดพันธะไฮโดรเจน"


class HBondItem(NamedTuple):
    name: str
    can_bond: str


H_BOND_ITEMS: tuple[HBondItem, ...] = (
    HBondItem("น้ำ (H-O-H)", CAN_H_BOND),
    HBondItem("แอมโมเนีย (H3N)", CAN_H_BOND),
    HBondItem("ไฮโดรเจนฟลูออไรด์ (H-F)", CAN_H_BOND),
    HBondItem("เมทานอล (CH3-O-H)", CAN_H_BOND),
    HBondItem("มีเทน (CH4)", CANNOT_H_BOND),
    HBondItem("ไฮโดรเจนซัลไฟด์ (H2S)", CANNOT_H_BOND),
    HBondItem("ไฮโดรเจนคลอไรด์ (H-Cl)", CANNOT_H_BOND),
    HBondItem("คาร์บอนไดออกไซด์ (CO2)", CANNOT_H_BOND),
    HBondItem("ไฮดราซีน (H2N-NH2)", CAN_H_BOND),
    HBondItem("เอทานอล (CH3-CH2-O-H)", CAN_H_BOND),
    HBondItem("กรดแอซีติก (CH3-COOH)", CAN_H_BOND),
    HBondItem("เมทิลเอมีน (CH3-NH2)", CAN_H_BOND),
    HBondItem("อีเทน (CH3-CH3)", CANNOT_H_BOND),
    HBondItem("ไฮโดรเจนโบรไมด์ (H-Br)", CANNOT_H_BOND),
    HBondItem("ฟอสฟีน (PH3)", CANNOT_H_BOND),
    HBondItem("คาร์บอนเตตระคลอไรด์ (CCl4)", CANNOT_H_BOND),
    HBondItem("ไฮโดรเจนเปอร์ออกไซด์ (H-O-O-H)", CAN_H_BOND),
    HBondItem("กรดฟอร์มิก (H-COOH)", CAN_H_BOND),
    HBondItem("เอทิลีนไกลคอล (HO-CH2-CH2-OH)", CAN_H_BOND),
    HBondItem("ไดเมทิลเอมีน (CH3-NH-CH3)", CAN_H_BOND),
    HBondItem("1-โพรพานอล (CH3-CH2-CH2-O-H)", CAN_H_BOND),
    # O or N present but no H on it: nothing to donate.
    HBondItem("ไดเมทิลอีเทอร์ (CH3-O-CH3)", CANNOT_H_BOND),
    HBondItem("แอซีโตน (CH3-CO-CH3)", CANNOT_H_BOND),
    HBondItem("ฟอร์มาลดีไฮด์ (H2C=O)", CANNOT_H_BOND),
    HBondItem("คลอโรมีเทน (CH3-Cl)", CANNOT_H_BOND),
    HBondItem("ไซเลน (SiH4)", CANNOT_H_BOND),
)


H_BOND_FACTS = (
    ("ไฮโดรเจนที่สร้างพันธะโดยตรงกับอะตอมของธาตุกลุ่มใดทำให้เกิดพันธะไฮโดรเจนได้",
     "N, O และ F",
     ("Cl, Br และ I", "C และ S", "ธาตุทุกชนิดที่สร้างพันธะกับไฮโดรเจน", "H และ He", "Na และ K")),
    ("พันธะไฮโดรเจนคือแรงดึงดูดระหว่างสิ่งใด",
     "อะตอม H ที่พันธะกับ N, O หรือ F ในโมเลกุลหนึ่ง กับอะตอม N, O หรือ F ของอีกโมเลกุลหนึ่ง",
     ("อะตอม H สองอะตอมที่อยู่ภายในโมเลกุลเดียวกัน เช่น H สองอะตอมในโมเลกุลน้ำ", "ไอออนบวกกับไอออนลบในผลึกไอออนิก เช่น Na⁺ กับ Cl⁻ ในผลึกเกลือแกง",
      "อะตอมโลหะกับอิเล็กตรอนอิสระ", "อะตอม H ที่พันธะกับ C ในโมเลกุลหนึ่ง กับอะตอม C ของอีกโมเลกุลหนึ่ง",
      "นิวเคลียสกับอิเล็กตรอนภายในอะตอม H")),
    ("พันธะไฮโดรเจนส่งผลต่อจุดเดือดของสารอย่างไร",
     "ทำให้จุดเดือดสูงกว่าสารที่มีมวลโมเลกุลใกล้เคียงแต่ไม่เกิดพันธะไฮโดรเจน",
     ("ทำให้จุดเดือดต่ำกว่าสารที่มีมวลโมเลกุลใกล้เคียงแต่ไม่เกิดพันธะไฮโดรเจน", "ไม่มีผลต่อจุดเดือดเลย",
      "ทำให้สารระเหิดได้ทันทีที่อุณหภูมิห้อง เพราะโมเลกุลแยกออกจากกันง่าย", "ทำให้จุดเดือดเท่ากับน้ำเสมอ",
      "ทำให้สารนำไฟฟ้าได้ดีเหมือนโลหะ")),
    ("เหตุใดน้ำ (H2O) จึงมีจุดเดือดสูงกว่าไฮโดรเจนซัลไฟด์ (H2S) มาก ทั้งที่มีขนาดโมเลกุลเล็กกว่า",
     "โมเลกุลของน้ำเกิดพันธะไฮโดรเจนต่อกัน แต่ H2S ไม่เกิดพันธะไฮโดรเจน",
     ("H2S เกิดพันธะไฮโดรเจนได้มากกว่าน้ำ เพราะอะตอม S ใหญ่กว่า O", "น้ำมีมวลโมเลกุลมากกว่า H2S จึงมีแรงลอนดอนมากกว่าและเดือดยากกว่า",
      "น้ำเป็นสารประกอบไอออนิก", "H2S ไม่มีแรงดึงดูดระหว่างโมเลกุลเลย",
      "น้ำมีพันธะโลหะระหว่างโมเลกุล")),
)


@question_type(
    "chem.hydrogen_bond_foundation",
    display_name={"th": "อะตอมธาตุใดสร้างพันธะไฮโดรเจนกับไฮโดรเจนได้"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_HYDROGEN_BOND,
)
class HydrogenBondFoundation(QuestionType):
    """A general fact — which atoms allow it, what it is, and what it does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(H_BOND_FACTS)
        return _labelled(
            stem=stem,
            correct=correct,
            wrongs=wrongs,
            topic=TOPIC_HYDROGEN_BOND,
            hint="N, O และ F มีขนาดเล็กและดึงดูดอิเล็กตรอนสูง ทำให้ไฮโดรเจนที่พันธะด้วยมีขั้วบวกสูงพอจะดึงดูดอะตอมข้างเคียง",
        )


@question_type(
    "chem.hydrogen_bond_fluency",
    display_name={"th": "สารที่กำหนดเกิดพันธะไฮโดรเจนได้หรือไม่"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_HYDROGEN_BOND,
)
class HydrogenBondFluency(QuestionType):
    """Classify one named substance directly — the whole ม.5/10 indicator."""
    max_choices = 2  # a bare yes/no label: fillers only padded it to four

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(H_BOND_ITEMS)
        other = CANNOT_H_BOND if item.can_bond == CAN_H_BOND else CAN_H_BOND
        return _labelled(
            stem=f"สาร {item.name} เกิดพันธะไฮโดรเจนได้หรือไม่",
            correct=item.can_bond,
            wrongs=(other,),
            topic=TOPIC_HYDROGEN_BOND,
            hint="ดูว่าไฮโดรเจนในโครงสร้างพันธะโดยตรงกับ N, O หรือ F หรือไม่",
        )


@question_type(
    "chem.hydrogen_bond_application",
    display_name={"th": "สารในข้อใดจัดอยู่ในหมวดที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_HYDROGEN_BOND,
)
class HydrogenBondApplication(QuestionType):
    """Reverse direction: given the capability, pick the matching substance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        capability = rng.choice((CAN_H_BOND, CANNOT_H_BOND))
        same = [item for item in H_BOND_ITEMS if item.can_bond == capability]
        other = [item for item in H_BOND_ITEMS if item.can_bond != capability]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        return _labelled(
            stem=f"สารในข้อใดต่อไปนี้{capability}",
            correct=correct.name,
            wrongs=tuple(w.name for w in wrongs),
            topic=TOPIC_HYDROGEN_BOND,
            hint="ดูว่าไฮโดรเจนในโครงสร้างพันธะโดยตรงกับ N, O หรือ F หรือไม่",
        )


# More rows: the set drew from four or five, so a learner met them all in a
# few tries. Every added row asks something the others do not.
H_BOND_FACTS += (
    ('เหตุใดแอมโมเนีย (NH3) จึงมีจุดเดือดสูงกว่ามีเทน (CH4) ซึ่งมีมวลโมเลกุลใกล้เคียงกัน',
     'โมเลกุลแอมโมเนียเกิดพันธะไฮโดรเจนต่อกัน แต่มีเทนไม่เกิด',
     ('มีเทนเกิดพันธะไฮโดรเจนต่อกันได้แข็งแรงกว่าแอมโมเนีย', 'แอมโมเนียมีมวลโมเลกุลมากกว่ามีเทนหลายเท่าตัว',
      'มีเทนเป็นโมเลกุลมีขั้วมาก แต่แอมโมเนียไม่มีขั้ว', 'แอมโมเนียเป็นสารประกอบไอออนิกที่มีแรงไอออนิก',
      'ทั้งสองไม่มีแรงยึดเหนี่ยวระหว่างโมเลกุลใด ๆ เลย')),
    ('เหตุใดน้ำแข็งจึงลอยน้ำได้',
     'พันธะไฮโดรเจนจัดโมเลกุลในน้ำแข็งให้มีช่องว่าง น้ำแข็งจึงหนาแน่นน้อยกว่าน้ำ',
     ('น้ำแข็งทุกก้อนมีฟองอากาศอัดอยู่ภายในจำนวนมากจึงลอยได้', 'น้ำแข็งหนาแน่นกว่าน้ำเสมอ แต่แรงตึงผิวช่วยพยุงไว้',
      'น้ำแข็งไม่มีพันธะไฮโดรเจน โมเลกุลจึงอยู่ห่างกันมาก', 'น้ำแข็งเป็นสารคนละชนิดกับน้ำจึงมีสมบัติต่างกัน',
      'แรงลอยตัวไม่กระทำต่อน้ำแข็ง น้ำแข็งจึงไม่จม')),
    ('เอทานอล (C2H5OH) ละลายน้ำได้ดี เพราะเหตุใด',
     'หมู่ -OH ของเอทานอลเกิดพันธะไฮโดรเจนกับโมเลกุลน้ำได้',
     ('เอทานอลเป็นสารประกอบไอออนิกที่แตกตัวในน้ำได้ดี', 'เอทานอลไม่มีขั้วเหมือนน้ำมันจึงผสมกับน้ำได้',
      'เอทานอลทำปฏิกิริยากับน้ำเกิดเป็นสารใหม่ทันที', 'เอทานอลมีมวลโมเลกุลมากกว่าน้ำหลายสิบเท่า',
      'เอทานอลเป็นแก๊สที่อุณหภูมิห้องจึงกระจายในน้ำ')),
    ('สารใดต่อไปนี้เกิดพันธะไฮโดรเจนระหว่างโมเลกุลได้',
     'ไฮโดรเจนฟลูออไรด์ (HF)',
     ('มีเทน (CH4)', 'ไฮโดรเจน (H2)', 'คาร์บอนไดออกไซด์ (CO2)', 'ไฮโดรเจนคลอไรด์ (HCl)', 'อีเทน (C2H6)')),
)
