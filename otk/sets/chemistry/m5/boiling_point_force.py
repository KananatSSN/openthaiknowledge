"""จุดเดือดของสารโคเวเลนต์กับแรงดึงดูดระหว่างโมเลกุล

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/11

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


TOPIC_BOILING = "จุดเดือดของสารโคเวเลนต์กับแรงดึงดูดระหว่างโมเลกุล"


NONPOLAR_FORCE = "แรงแผ่กระจาย (dispersion) เท่านั้น"


POLAR_FORCE = "แรงระหว่างขั้ว (dipole-dipole)"


HBOND_FORCE = "พันธะไฮโดรเจน"


RANK = {NONPOLAR_FORCE: 1, POLAR_FORCE: 2, HBOND_FORCE: 3}


FORCE_LABELS = {
    NONPOLAR_FORCE: ("มีแรงแผ่กระจาย (dispersion) เท่านั้น จึงมีจุดเดือดต่ำที่สุด"
                      "เมื่อเทียบกับโมเลกุลอื่นที่มีขนาดใกล้เคียงกัน"),
    POLAR_FORCE: ("มีแรงระหว่างขั้ว (dipole-dipole) จึงมีจุดเดือดสูงกว่าโมเลกุลไม่มีขั้ว "
                  "แต่ต่ำกว่าโมเลกุลที่มีพันธะไฮโดรเจน เมื่อขนาดใกล้เคียงกัน"),
    HBOND_FORCE: ("มีพันธะไฮโดรเจน จึงมีจุดเดือดสูงที่สุด"
                  "เมื่อเทียบกับโมเลกุลอื่นที่มีขนาดใกล้เคียงกัน"),
}


NO_ATTRACTION_FILLER = "ไม่มีแรงดึงดูดระหว่างโมเลกุลเลย จึงเป็นแก๊สที่อุณหภูมิห้องเสมอ"


FORCE_FILLERS = (NO_ATTRACTION_FILLER,
                 "มีพันธะไอออนิกระหว่างโมเลกุล จึงมีจุดเดือดสูงมากเหมือนเกลือแกง",
                 "มีพันธะโลหะระหว่างโมเลกุล จึงนำไฟฟ้าได้ดีและจุดเดือดสูงมาก")


class ForceItem(NamedTuple):
    name: str
    force: str


FORCE_ITEMS: tuple[ForceItem, ...] = (
    ForceItem("แก๊สไฮโดรเจน (H2)", NONPOLAR_FORCE),
    ForceItem("มีเทน (CH4)", NONPOLAR_FORCE),
    ForceItem("ไฮโดรเจนคลอไรด์ (HCl)", POLAR_FORCE),
    ForceItem("ไฮโดรเจนโบรไมด์ (HBr)", POLAR_FORCE),
    ForceItem("น้ำ (H2O)", HBOND_FORCE),
    ForceItem("แอมโมเนีย (NH3)", HBOND_FORCE),
    ForceItem("ไฮโดรเจนฟลูออไรด์ (HF)", HBOND_FORCE),
    # Every polar entry here boils above every nonpolar one, and below every hydrogen-bonded one.
    ForceItem("ออกซิเจน (O2)", NONPOLAR_FORCE),
    ForceItem("ไนโตรเจน (N2)", NONPOLAR_FORCE),
    ForceItem("ไฮโดรเจนซัลไฟด์ (H2S)", POLAR_FORCE),
    ForceItem("ไฮโดรเจนไอโอไดด์ (HI)", POLAR_FORCE),
    ForceItem("เมทานอล (CH3OH)", HBOND_FORCE),
)


FORCE_NAMES = {
    NONPOLAR_FORCE: "แรงแผ่กระจายเท่านั้น (ไม่มีขั้ว)",
    POLAR_FORCE: "แรงระหว่างขั้ว (มีขั้ว แต่ไม่มีพันธะไฮโดรเจน)",
    HBOND_FORCE: "พันธะไฮโดรเจน",
}


@question_type(
    "chem.boiling_point_force_foundation",
    display_name={"th": "สารคู่ใดมีจุดเดือดสูงกว่ากัน"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_BOILING,
)
class BoilingPointForceFoundation(QuestionType):
    """Pairwise comparison only — not yet the full explanation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        higher_force, lower_force = rng.sample((NONPOLAR_FORCE, POLAR_FORCE, HBOND_FORCE), 2)
        if RANK[higher_force] < RANK[lower_force]:
            higher_force, lower_force = lower_force, higher_force
        higher = rng.choice([item for item in FORCE_ITEMS if item.force == higher_force])
        lower = rng.choice([item for item in FORCE_ITEMS if item.force == lower_force])
        return _labelled(
            stem=(f"เมื่อเทียบขนาดโมเลกุลที่ใกล้เคียงกัน สารคู่ใดต่อไปนี้มีจุดเดือดสูงกว่า: "
                  f"{higher.name} กับ {lower.name}"),
            correct=higher.name,
            wrongs=(lower.name, "มีจุดเดือดเท่ากันทั้งสองสาร", "ไม่สามารถเปรียบเทียบได้",
                    "สารที่เป็นแก๊สที่อุณหภูมิห้องมีจุดเดือดสูงกว่า", "ขึ้นอยู่กับสีของสาร"),
            topic=TOPIC_BOILING,
            hint="แรงดึงดูดระหว่างโมเลกุลที่แข็งแรงกว่าทำให้ต้องใช้พลังงานมากกว่าในการแยกโมเลกุลออกจากกัน จุดเดือดจึงสูงกว่า",
        )


@question_type(
    "chem.boiling_point_force_fluency",
    display_name={"th": "แรงดึงดูดระหว่างโมเลกุลของสารที่กำหนดและผลต่อจุดเดือด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_BOILING,
)
class BoilingPointForceFluency(QuestionType):
    """State the force and its boiling-point effect together — the whole indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(FORCE_ITEMS)
        others = [f for f in (NONPOLAR_FORCE, POLAR_FORCE, HBOND_FORCE) if f != item.force]
        wrongs = tuple(FORCE_LABELS[f] for f in others) + FORCE_FILLERS
        return _labelled(
            stem=f"{item.name} มีแรงดึงดูดระหว่างโมเลกุลชนิดใด และมีผลต่อจุดเดือดอย่างไร",
            correct=FORCE_LABELS[item.force],
            wrongs=wrongs,
            topic=TOPIC_BOILING,
            hint="ดูก่อนว่าโมเลกุลมีขั้วหรือไม่ และมีไฮโดรเจนพันธะโดยตรงกับ N, O หรือ F หรือไม่",
        )


@question_type(
    "chem.boiling_point_force_application",
    display_name={"th": "สารในข้อใดมีแรงดึงดูดระหว่างโมเลกุลชนิดที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_BOILING,
)
class BoilingPointForceApplication(QuestionType):
    """Reverse direction: given the force, pick the matching substance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        force = rng.choice((NONPOLAR_FORCE, POLAR_FORCE, HBOND_FORCE))
        same = [item for item in FORCE_ITEMS if item.force == force]
        other = [item for item in FORCE_ITEMS if item.force != force]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        return _labelled(
            stem=f"สารในข้อใดต่อไปนี้มีแรงดึงดูดระหว่างโมเลกุลเป็น{FORCE_NAMES[force]}",
            correct=correct.name,
            wrongs=tuple(w.name for w in wrongs),
            topic=TOPIC_BOILING,
            hint="ดูก่อนว่าโมเลกุลมีขั้วหรือไม่ และมีไฮโดรเจนพันธะโดยตรงกับ N, O หรือ F หรือไม่",
        )
