"""ไซเล็มและโฟลเอ็ม

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/9

Sets moved here from: science_wave_b4.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b4 import (
    LEVEL,
    PHLOEM,
    SUBJECT,
    TISSUE_SCENARIOS,
    TOPIC,
    XYLEM,
    _labelled,
)

PROVENANCE = Provenance("original")


class VesselAspect(NamedTuple):
    """One property, stated for each vessel.

    Both values are true — of different vessels. That is what makes a swapped
    value a distractor worth offering rather than an obvious throwaway.
    """
    aspect: str
    xylem: str
    phloem: str


VESSEL_ASPECTS = (
    VesselAspect("สิ่งที่ลำเลียง",
                 "ลำเลียงน้ำและธาตุอาหารที่รากดูดขึ้นมาจากดิน",
                 "ลำเลียงอาหารประเภทน้ำตาลที่ใบสร้างขึ้น"),
    VesselAspect("ลักษณะของเซลล์",
                 "ประกอบด้วยเซลล์ที่ตายแล้ว ผนังหนา กลวงต่อกันเป็นท่อยาว",
                 "ประกอบด้วยเซลล์ที่ยังมีชีวิต มีแผ่นตะแกรงเจาะรูกั้นระหว่างเซลล์"),
    VesselAspect("ตำแหน่งในมัดท่อลำเลียง",
                 "อยู่ด้านในของมัดท่อลำเลียง ใกล้ใจกลางลำต้น",
                 "อยู่ด้านนอกของมัดท่อลำเลียง ใกล้เปลือกของลำต้น"),
    VesselAspect("ทิศทางการลำเลียง",
                 "ลำเลียงไปในทิศทางเดียว คือจากรากขึ้นสู่ลำต้นและใบ",
                 "ลำเลียงได้ทั้งขึ้นและลง จากแหล่งสร้างอาหารไปยังแหล่งที่ใช้หรือสะสม"),
    VesselAspect("แรงที่ใช้ลำเลียง",
                 "อาศัยแรงดึงจากการคายน้ำที่ใบเป็นหลัก",
                 "อาศัยเซลล์ที่ยังมีชีวิตช่วยลำเลียงจากแหล่งสร้างไปยังแหล่งที่ใช้"),
    VesselAspect("ผลเมื่อควั่นเปลือกรอบลำต้น",
                 "ยังลำเลียงได้ตามปกติ เพราะอยู่ในเนื้อไม้ใต้เปลือก",
                 "ถูกตัดขาดไปพร้อมเปลือก อาหารจึงลงไปไม่ถึงราก"),
)


def _values(tissue: str) -> tuple[str, ...]:
    return tuple(aspect.xylem if tissue == XYLEM else aspect.phloem
                 for aspect in VESSEL_ASPECTS)


@question_type(
    "plant.transport_tissue_foundation",
    display_name={"th": "ลักษณะและหน้าที่ของไซเล็มและโฟลเอ็ม"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class TransportTissueFoundation(QuestionType):
    """Pick the true statement about one vessel out of four.

    Not "which vessel is this" — there are two vessels, and two choices is not a
    question. The three wrong statements are all true of the *other* vessel, so
    the item cannot be answered by ruling out something that sounds invented.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        tissue = rng.choice((XYLEM, PHLOEM))
        other = PHLOEM if tissue == XYLEM else XYLEM
        mine, theirs = list(_values(tissue)), list(_values(other))
        rng.shuffle(theirs)
        return _labelled(
            stem=f"ข้อใดกล่าวถึง “{tissue}” ได้ถูกต้อง",
            correct=rng.choice(mine),
            wrongs=tuple(theirs[:3]),
            hint="ไซเล็มเกี่ยวข้องกับน้ำที่ขึ้นจากราก ส่วนโฟลเอ็มเกี่ยวข้องกับอาหารที่ใบสร้าง",
        )


@question_type(
    "plant.transport_tissue_fluency",
    display_name={"th": "จับคู่ลักษณะกับท่อลำเลียงของพืช"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class TransportTissueFluency(QuestionType):
    """Which of four pairings is the right way round.

    Each choice names a vessel and a property. Three of them attach a real
    property to the wrong vessel, which is the mistake worth catching: the facts
    are usually remembered and it is the attachment that slips.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        aspects = list(VESSEL_ASPECTS)
        rng.shuffle(aspects)
        first, second = aspects[0], aspects[1]
        tissue = rng.choice((XYLEM, PHLOEM))
        other = PHLOEM if tissue == XYLEM else XYLEM

        def value_for(aspect: VesselAspect, which: str) -> str:
            return aspect.xylem if which == XYLEM else aspect.phloem

        correct_value = value_for(first, tissue)
        return _labelled(
            stem="ข้อใดจับคู่ท่อลำเลียงกับลักษณะของมันได้ถูกต้อง",
            correct=f"{tissue}: {correct_value}",
            wrongs=(
                # the other vessel's value on this one
                f"{tissue}: {value_for(first, other)}",
                # this vessel's value on the other one
                f"{other}: {correct_value}",
                # and a second aspect, also on the wrong vessel
                f"{other}: {value_for(second, tissue)}",
            ),
            hint="ตรวจทีละข้อว่าลักษณะนั้นเป็นของท่อที่ระบุไว้จริงหรือไม่ "
                 "ทุกตัวเลือกเป็นเรื่องจริงของพืชทั้งสิ้น ต่างกันที่จับคู่ถูกหรือผิด",
        )


@question_type(
    "plant.transport_tissue_application",
    display_name={"th": "วิเคราะห์หน้าที่ของท่อลำเลียงจากผลการทดลองและสถานการณ์จริง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class TransportTissueApplication(QuestionType):
    """Explain a dye test, a girdled branch or a sap-feeding insect.

    Each item states something observable and asks which vessel accounts for it,
    so the position and the contents both have to be known — not just the names.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(TISSUE_SCENARIOS)
        return _labelled(
            stem=stem, correct=correct, wrongs=wrongs,
            hint="ถามสองข้อเสมอ: สิ่งที่เคลื่อนที่คือน้ำหรืออาหาร "
                 "และตำแหน่งที่พบอยู่ด้านในหรือด้านนอกของมัดท่อลำเลียง",
        )
