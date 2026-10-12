"""พืชและสัตว์ที่อาศัยอยู่บริเวณต่าง ๆ

ชีวะ · ป.1 · สสวท. พื้นฐาน
Indicators: ว 1.1 ป.1/1

Sets moved here from: science_wave_b31.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import PRIMARY_ONE, _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b31 import ECOLOGY_TOPIC, SURVEY_SCENARIOS

PROVENANCE = Provenance("original")


class Dweller(NamedTuple):
    """A plant or animal and the place a survey would find it."""
    name: str
    kind: str
    place: str


# place -> realm. Two places in the same realm can share inhabitants.
PLACES = {
    "สระน้ำ": "น้ำจืด",
    "ลำธารในป่า": "น้ำจืด",
    "ทะเล": "น้ำเค็ม",
    "สวนผลไม้": "บนบก",
    "ใต้ขอนไม้ผุที่ชื้น": "บนบก",
    "สนามหญ้า": "บนบก",
}


DWELLERS = (
    Dweller("บัว", "พืช", "สระน้ำ"),
    Dweller("ผักตบชวา", "พืช", "สระน้ำ"),
    Dweller("จอก", "พืช", "สระน้ำ"),
    Dweller("ปลานิล", "สัตว์", "สระน้ำ"),
    Dweller("ลูกอ๊อด", "สัตว์", "สระน้ำ"),
    Dweller("หอยขม", "สัตว์", "สระน้ำ"),
    Dweller("ปูน้ำตก", "สัตว์", "ลำธารในป่า"),
    Dweller("หญ้าทะเล", "พืช", "ทะเล"),
    Dweller("ปลาการ์ตูน", "สัตว์", "ทะเล"),
    Dweller("ดาวทะเล", "สัตว์", "ทะเล"),
    Dweller("ม้าน้ำ", "สัตว์", "ทะเล"),
    Dweller("ต้นมะม่วง", "พืช", "สวนผลไม้"),
    Dweller("ต้นมะละกอ", "พืช", "สวนผลไม้"),
    Dweller("กระรอก", "สัตว์", "สวนผลไม้"),
    Dweller("มอส", "พืช", "ใต้ขอนไม้ผุที่ชื้น"),
    Dweller("ไส้เดือนดิน", "สัตว์", "ใต้ขอนไม้ผุที่ชื้น"),
    Dweller("กิ้งกือ", "สัตว์", "ใต้ขอนไม้ผุที่ชื้น"),
    Dweller("ตั๊กแตน", "สัตว์", "สนามหญ้า"),
    Dweller("จิ้งหรีด", "สัตว์", "สนามหญ้า"),
)


def _elsewhere(item: Dweller) -> list[Dweller]:
    """Same kind, but from a realm where the item could not also be living."""
    realm = PLACES[item.place]
    return [other for other in DWELLERS
            if other.kind == item.kind and PLACES[other.place] != realm]


# Each of these places holds at least one plant and one animal, so a record of
# any three of them always gives a kind question something to ask.
SURVEYED = ("สระน้ำ", "ทะเล", "สวนผลไม้", "ใต้ขอนไม้ผุที่ชื้น")


NOT_FOUND = "ไม่พบในบริเวณใดที่สำรวจ"


def _record(places: list[str], rng: Random) -> str:
    lines = []
    for place in places:
        names = [item.name for item in DWELLERS if item.place == place]
        rng.shuffle(names)
        lines.append(f"{place}: {', '.join(names)}")
    return " / ".join(lines)


@question_type(
    "ecology.habitat_dwellers_foundation",
    display_name={"th": "พืชและสัตว์ในบริเวณต่าง ๆ"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class HabitatDwellersFoundation(QuestionType):
    """Know where a plant or animal is usually found, in either direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DWELLERS)
        realm = PLACES[item.place]
        if rng.random() < 0.5:
            others = [other.name for other in _elsewhere(item)]
            rng.shuffle(others)
            return _labelled(
                stem=f"{item.kind}ในข้อใดพบอาศัยอยู่บริเวณ “{item.place}”",
                correct=item.name, wrongs=tuple(others[:3]),
                hint="นึกถึงว่าสิ่งมีชีวิตแต่ละชนิดต้องอยู่ในน้ำหรืออยู่บนบก",
                topic=ECOLOGY_TOPIC,
            )
        places = [place for place, other in PLACES.items() if other != realm]
        rng.shuffle(places)
        return _labelled(
            stem=f"“{item.name}” พบอาศัยอยู่บริเวณใด",
            correct=item.place, wrongs=tuple(places[:3]),
            hint="นึกถึงว่าสิ่งมีชีวิตแต่ละชนิดต้องอยู่ในน้ำหรืออยู่บนบก",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.habitat_dwellers_fluency",
    display_name={"th": "ระบุพืชและสัตว์จากข้อมูลการสำรวจ"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class HabitatDwellersFluency(QuestionType):
    """Read a survey record and name what it found — the indicator's evidence.

    The answer comes from the record printed in the stem, not from what the
    learner remembers, so every wrong choice is wrong *according to the data*.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        places = rng.sample(SURVEYED, 3)
        stem = ("นักเรียนสำรวจและบันทึกชื่อสิ่งมีชีวิตที่พบ ดังนี้ "
                f"{_record(places, rng)} ")
        recorded = [item for item in DWELLERS if item.place in places]
        if rng.random() < 0.5:
            target = rng.choice(places)
            kind = rng.choice(("พืช", "สัตว์"))
            item = rng.choice([one for one in recorded
                               if one.place == target and one.kind == kind])
            # Wrong: the other kind from the same place, or the same kind from
            # another place. Never the same kind from the same place.
            others = [one.name for one in recorded
                      if not (one.place == target and one.kind == kind)]
            rng.shuffle(others)
            return _labelled(
                stem=stem + f"จากข้อมูลนี้ ข้อใดเป็น{kind}ที่พบบริเวณ“{target}”",
                correct=item.name, wrongs=tuple(others[:3]),
                hint="หาบรรทัดของบริเวณที่โจทย์ถาม แล้วดูว่าชื่อใดเป็น" + kind,
                topic=ECOLOGY_TOPIC,
            )
        item = rng.choice(recorded)
        wrongs = [place for place in places if place != item.place] + [NOT_FOUND]
        return _labelled(
            stem=stem + f"จากข้อมูลนี้ “{item.name}” พบที่บริเวณใด",
            correct=item.place, wrongs=tuple(wrongs),
            hint="หาชื่อสิ่งมีชีวิตในบันทึก แล้วดูว่าอยู่ในบรรทัดของบริเวณใด",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.habitat_dwellers_application",
    display_name={"th": "วิเคราะห์ข้อมูลการสำรวจสิ่งมีชีวิต"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class HabitatDwellersApplication(QuestionType):
    """Judge a survey: when it was done, where it looked, what it wrote down."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SURVEY_SCENARIOS,
            hint="ถามว่าข้อมูลได้มาอย่างไร และสำรวจครบทุกที่ทุกเวลาแล้วหรือยัง",
        ), ECOLOGY_TOPIC)
