"""สภาพขั้วของโมเลกุลที่ประกอบด้วยสองอะตอม

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/9

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


TOPIC_POLARITY = "สภาพขั้วของโมเลกุลที่ประกอบด้วยสองอะตอม"


POLAR, NONPOLAR = "มีขั้ว", "ไม่มีขั้ว"


POLARITY_FILLERS = ("มีขั้วเฉพาะในบางสถานะของสาร", "ไม่สามารถระบุสภาพขั้วได้จากสูตรโครงสร้าง",
                    "มีขั้วเฉพาะเมื่อละลายน้ำ", "ขึ้นอยู่กับมวลของโมเลกุลเท่านั้น")


# The rule stated with its reason, so the answer is not the one short choice.
POLARITY_WHY = {
    POLAR: "มีขั้ว เพราะอะตอมทั้งสองดึงดูดอิเล็กตรอนคู่ร่วมพันธะไม่เท่ากัน",
    NONPOLAR: "ไม่มีขั้ว เพราะอะตอมทั้งสองดึงดูดอิเล็กตรอนคู่ร่วมพันธะเท่ากัน",
}


POLARITY_WHY_FILLERS = ("มีขั้ว เพราะอะตอมทั้งสองมีมวลไม่เท่ากัน", "ไม่มีขั้ว เพราะเป็นโมเลกุลที่มีเพียงสองอะตอม",
                        "มีขั้ว เพราะเป็นโมเลกุลที่มีสองอะตอม", "ไม่สามารถระบุสภาพขั้วได้จากชนิดของอะตอมเพียงอย่างเดียว",
                        "มีขั้วเฉพาะเมื่อละลายน้ำ เพราะน้ำดึงอิเล็กตรอนออกจากโมเลกุล")


class PolarityItem(NamedTuple):
    name: str
    polarity: str


POLARITY_ITEMS: tuple[PolarityItem, ...] = (
    PolarityItem("แก๊สไฮโดรเจน (H-H)", NONPOLAR),
    PolarityItem("แก๊สออกซิเจน (O=O)", NONPOLAR),
    PolarityItem("แก๊สไนโตรเจน (N≡N)", NONPOLAR),
    PolarityItem("แก๊สคลอรีน (Cl-Cl)", NONPOLAR),
    PolarityItem("แก๊สไฮโดรเจนคลอไรด์ (H-Cl)", POLAR),
    PolarityItem("แก๊สไฮโดรเจนฟลูออไรด์ (H-F)", POLAR),
    PolarityItem("แก๊สไฮโดรเจนโบรไมด์ (H-Br)", POLAR),
    PolarityItem("แก๊สคาร์บอนมอนอกไซด์ (C≡O)", POLAR),
    PolarityItem("แก๊สฟลูออรีน (F-F)", NONPOLAR),
    PolarityItem("โบรมีน (Br-Br)", NONPOLAR),
    PolarityItem("ไอโอดีน (I-I)", NONPOLAR),
    PolarityItem("แก๊สไฮโดรเจนไอโอไดด์ (H-I)", POLAR),
    PolarityItem("แก๊สไนโตรเจนมอนอกไซด์ (N=O)", POLAR),
    PolarityItem("คลอรีนมอนอฟลูออไรด์ (Cl-F)", POLAR),
)


POLARITY_RULES = (
    ("โมเลกุลที่ประกอบด้วยอะตอมชนิดเดียวกัน 2 อะตอม เช่น H-H หรือ O=O มีสภาพขั้วเป็นอย่างไร", NONPOLAR),
    ("โมเลกุลที่ประกอบด้วยอะตอมต่างชนิดกัน 2 อะตอม เช่น H-Cl มีสภาพขั้วเป็นอย่างไร", POLAR),
    ("โมเลกุลสองอะตอมที่อะตอมทั้งสองมีค่าอิเล็กโทรเนกาติวิตีเท่ากัน มีสภาพขั้วเป็นอย่างไร", NONPOLAR),
    ("โมเลกุลสองอะตอมที่อะตอมทั้งสองมีค่าอิเล็กโทรเนกาติวิตีต่างกัน มีสภาพขั้วเป็นอย่างไร", POLAR),
)


def formula_of(name: str) -> str:
    """The structural formula in a bank name's brackets."""
    return name[name.rindex("(") + 1:-1]


@question_type(
    "chem.molecule_polarity_foundation",
    display_name={"th": "โมเลกุลที่ประกอบด้วยอะตอมชนิดเดียวกันมีสภาพขั้วอย่างไร"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_POLARITY,
)
class MoleculePolarityFoundation(QuestionType):
    """A general rule — not yet applied to one named molecule."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, polarity = rng.choice(POLARITY_RULES)
        return _labelled(
            stem=stem,
            correct=POLARITY_WHY[polarity],
            wrongs=(POLARITY_WHY[POLAR if polarity == NONPOLAR else NONPOLAR], *POLARITY_WHY_FILLERS),
            topic=TOPIC_POLARITY,
            hint="อะตอมชนิดเดียวกันดึงดูดอิเล็กตรอนคู่ร่วมพันธะเท่ากัน อิเล็กตรอนจึงอยู่กึ่งกลางพันธะ",
        )


@question_type(
    "chem.molecule_polarity_fluency",
    display_name={"th": "สภาพขั้วของโมเลกุลที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_POLARITY,
)
class MoleculePolarityFluency(QuestionType):
    """Classify one named molecule directly — the whole ม.5/9 indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(POLARITY_ITEMS)
        other = POLAR if item.polarity == NONPOLAR else NONPOLAR
        return _labelled(
            stem=f"โมเลกุล {item.name} มีสภาพขั้วอย่างไร",
            correct=item.polarity,
            wrongs=(other, *POLARITY_FILLERS),
            topic=TOPIC_POLARITY,
            hint="โมเลกุลจากอะตอมต่างชนิดกันมีขั้ว เพราะอะตอมทั้งสองดึงดูดอิเล็กตรอนคู่ร่วมพันธะไม่เท่ากัน",
        )


@question_type(
    "chem.molecule_polarity_application",
    display_name={"th": "โมเลกุลในข้อใดจัดอยู่ในหมวดขั้วที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_POLARITY,
)
class MoleculePolarityApplication(QuestionType):
    """Reverse direction: given a polarity, pick the matching molecule."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        polarity = rng.choice((POLAR, NONPOLAR))
        same = [item for item in POLARITY_ITEMS if item.polarity == polarity]
        other = [item for item in POLARITY_ITEMS if item.polarity != polarity]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        return _labelled(
            stem=f"โมเลกุลในข้อใดต่อไปนี้จัดเป็นโมเลกุลที่{polarity}",
            # Formulas alone: the names of the compounds run longer than the elements'.
            correct=formula_of(correct.name),
            wrongs=tuple(formula_of(w.name) for w in wrongs),
            topic=TOPIC_POLARITY,
            hint="ดูก่อนว่าโมเลกุลประกอบด้วยอะตอมชนิดเดียวกันหรือต่างชนิดกัน",
        )


# More rows: the set drew from four or five, so a learner met them all in a
# few tries. Every added row asks something the others do not.
POLARITY_RULES += (
    ('โมเลกุลไนโตรเจน (N≡N) มีสภาพขั้วเป็นอย่างไร', NONPOLAR),
    ('โมเลกุลไฮโดรเจนฟลูออไรด์ (H-F) มีสภาพขั้วเป็นอย่างไร', POLAR),
    ('โมเลกุลคลอรีน (Cl-Cl) มีสภาพขั้วเป็นอย่างไร', NONPOLAR),
    ('โมเลกุลคาร์บอนมอนอกไซด์ (C≡O) มีสภาพขั้วเป็นอย่างไร', POLAR),
)
