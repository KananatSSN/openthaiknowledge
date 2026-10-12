"""พันธะเดี่ยว พันธะคู่ พันธะสาม และจำนวนคู่อิเล็กตรอนร่วมพันธะ

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/8

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


TOPIC_BOND_ORDER = "พันธะเดี่ยว พันธะคู่ พันธะสาม และจำนวนคู่อิเล็กตรอนร่วมพันธะ"


SINGLE, DOUBLE, TRIPLE = "พันธะเดี่ยว", "พันธะคู่", "พันธะสาม"


PAIRS_OF = {SINGLE: 1, DOUBLE: 2, TRIPLE: 3}


class BondItem(NamedTuple):
    name: str
    bond_type: str


BOND_ITEMS: tuple[BondItem, ...] = (
    BondItem("H-H (แก๊สไฮโดรเจน)", SINGLE),
    BondItem("Cl-Cl (แก๊สคลอรีน)", SINGLE),
    BondItem("F-F (แก๊สฟลูออรีน)", SINGLE),
    BondItem("H-Cl (แก๊สไฮโดรเจนคลอไรด์)", SINGLE),
    BondItem("H-F (แก๊สไฮโดรเจนฟลูออไรด์)", SINGLE),
    BondItem("O=O (แก๊สออกซิเจน)", DOUBLE),
    BondItem("N≡N (แก๊สไนโตรเจน)", TRIPLE),
    BondItem("C≡O (แก๊สคาร์บอนมอนอกไซด์)", TRIPLE),
    BondItem("Br-Br (โบรมีน)", SINGLE),
    BondItem("C-H แต่ละพันธะของแก๊สมีเทน (CH4)", SINGLE),
    BondItem("O-H แต่ละพันธะของน้ำ (H-O-H)", SINGLE),
    BondItem("C=O แต่ละพันธะของแก๊สคาร์บอนไดออกไซด์ (O=C=O)", DOUBLE),
    BondItem("C=C ของแก๊สเอทีน (H2C=CH2)", DOUBLE),
    BondItem("C≡C ของแก๊สอีไทน์ (HC≡CH)", TRIPLE),
    BondItem("C≡N ของไฮโดรเจนไซยาไนด์ (H-C≡N)", TRIPLE),
)


NO_COVALENT_BOND_FILLER = "ไม่มีพันธะโคเวเลนต์ระหว่างอะตอมคู่นี้"


BOND_FILLERS = (NO_COVALENT_BOND_FILLER, "พันธะไอออนิก", "พันธะโลหะ")


def _bond_order_label(bond_type: str, pairs: int) -> str:
    return f"{bond_type} มีอิเล็กตรอนร่วมกัน {pairs} คู่"


MULTI_BOND_ITEMS: tuple[tuple[str, int, str], ...] = (
    ("แก๊สคาร์บอนไดออกไซด์ (O=C=O)", 2, DOUBLE),
    ("น้ำ (H-O-H)", 2, SINGLE),
    ("มีเทน (CH4)", 4, SINGLE),
    ("แอมโมเนีย (NH3)", 3, SINGLE),
    ("คาร์บอนเตตระคลอไรด์ (CCl4)", 4, SINGLE),
    ("ไฮโดรเจนเปอร์ออกไซด์ (H-O-O-H)", 3, SINGLE),
    ("อีเทน (H3C-CH3)", 7, SINGLE),
    ("คาร์บอนไดซัลไฟด์ (S=C=S)", 2, DOUBLE),
)


@question_type(
    "chem.covalent_bond_order_foundation",
    display_name={"th": "พันธะระหว่างอะตอมคู่นี้เป็นพันธะชนิดใด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_BOND_ORDER,
)
class CovalentBondOrderFoundation(QuestionType):
    """Bond type alone — not yet the shared electron-pair count."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(BOND_ITEMS)
        others = [t for t in (SINGLE, DOUBLE, TRIPLE) if t != item.bond_type]
        return _labelled(
            stem=f"พันธะระหว่างอะตอมคู่ร่วมพันธะใน {item.name} เป็นพันธะโคเวเลนต์ชนิดใด",
            correct=item.bond_type,
            wrongs=(*others, *BOND_FILLERS),
            topic=TOPIC_BOND_ORDER,
            hint="พันธะเดี่ยวมีเส้นขีดหนึ่งเส้น พันธะคู่มีสองเส้น และพันธะสามมีสามเส้นระหว่างอะตอมคู่นั้น",
        )


@question_type(
    "chem.covalent_bond_order_fluency",
    display_name={"th": "ชนิดของพันธะและจำนวนคู่อิเล็กตรอนร่วมพันธะ"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_BOND_ORDER,
)
class CovalentBondOrderFluency(QuestionType):
    """Both facts at once — the whole ม.5/8 indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(BOND_ITEMS)
        pairs = PAIRS_OF[item.bond_type]
        others = [t for t in (SINGLE, DOUBLE, TRIPLE) if t != item.bond_type]
        wrongs = tuple(_bond_order_label(t, PAIRS_OF[t]) for t in others)
        # The right bond type with a wrong count, and a wrong type with this bond's count.
        wrongs += tuple(_bond_order_label(item.bond_type, n) for n in (1, 2, 3, 4) if n != pairs)
        wrongs += (_bond_order_label(others[0], pairs),)
        return _labelled(
            stem=(f"พันธะระหว่างอะตอมคู่ร่วมพันธะใน {item.name} เป็นพันธะโคเวเลนต์ชนิดใด "
                  "และมีอิเล็กตรอนร่วมกันกี่คู่"),
            correct=_bond_order_label(item.bond_type, pairs),
            wrongs=wrongs,
            topic=TOPIC_BOND_ORDER,
            hint="พันธะเดี่ยวใช้อิเล็กตรอนร่วมกัน 1 คู่ พันธะคู่ใช้ 2 คู่ และพันธะสามใช้ 3 คู่",
        )


@question_type(
    "chem.covalent_bond_order_application",
    display_name={"th": "จำนวนและชนิดของพันธะโคเวเลนต์ทั้งหมดในโมเลกุล"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_BOND_ORDER,
)
class CovalentBondOrderApplication(QuestionType):
    """Count every bond in a molecule, not just one bonded pair."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, count, bond_type = rng.choice(MULTI_BOND_ITEMS)
        correct = f"มีพันธะโคเวเลนต์ทั้งหมด {count} พันธะ และเป็น{bond_type}ทุกพันธะ"
        options = [f"มีพันธะโคเวเลนต์ทั้งหมด {count} พันธะ และเป็น{t}ทุกพันธะ"
                   for t in (SINGLE, DOUBLE, TRIPLE) if t != bond_type]
        options += [f"มีพันธะโคเวเลนต์ทั้งหมด {n} พันธะ และเป็น{bond_type}ทุกพันธะ"
                    for n in (count + 1, count - 1, 2 * count) if n >= 1 and n != count]
        wrongs = tuple(dict.fromkeys(options))
        return _labelled(
            stem=f"{name} มีพันธะโคเวเลนต์ทั้งหมดกี่พันธะ และเป็นพันธะชนิดใด",
            correct=correct,
            wrongs=wrongs,
            topic=TOPIC_BOND_ORDER,
            hint="นับจำนวนเส้นพันธะทั้งหมดในสูตรโครงสร้าง แล้วดูว่าแต่ละพันธะมีกี่เส้นขีด",
        )
