"""ประโยชน์และโทษของลม

ธรณีวิทยา · ป.3 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.3/4

Sets moved here from: science_wave_c11.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import PRIMARY_THREE, _retopic
from otk.sets._support.science_wave_c10 import LETTERS, SUBJECT
from otk.sets._support.science_wave_c11 import WIND_USE_SCENARIOS

PROVENANCE = Provenance("original")


WIND_USE_TOPIC = "ประโยชน์และโทษของลม"


BENEFIT = "ประโยชน์"


HARM = "โทษ"


class WindEvent(NamedTuple):
    """Something wind did, and whether it helped or harmed."""
    event: str
    kind: str


WIND_EVENTS = (
    WindEvent("ผ้าที่ตากไว้แห้งเร็วขึ้น", BENEFIT),
    WindEvent("กังหันลมหมุนผลิตไฟฟ้าให้หมู่บ้าน", BENEFIT),
    WindEvent("เรือใบแล่นออกไปหาปลาได้โดยไม่ใช้น้ำมัน", BENEFIT),
    WindEvent("ชาวนาใช้ลมพัดแยกเมล็ดข้าวลีบออกจากเมล็ดข้าวดี", BENEFIT),
    WindEvent("ต้นไม้ใหญ่หักโค่นขวางถนน", HARM),
    WindEvent("หลังคาบ้านหลายหลังถูกพัดปลิวหาย", HARM),
    WindEvent("ป้ายโฆษณาล้มทับรถที่จอดอยู่", HARM),
    WindEvent("ฝุ่นและควันไฟจากไร่ถูกพัดเข้ามาในหมู่บ้าน", HARM),
)


# Things that do not use wind at all, for the "which uses wind" question.
NOT_WIND = (
    "ใช้แผงโซลาร์เซลล์รับแสงแดดผลิตไฟฟ้า",
    "ใช้กังหันน้ำวิดน้ำเข้านา",
    "ใช้เตาถ่านหุงข้าว",
    "ใช้เขื่อนกักน้ำไว้ผลิตไฟฟ้า",
    "ใช้แสงแดดตากปลาให้แห้งในวันที่ลมสงบ",
)


def wind_record(rng: Random) -> list[WindEvent]:
    """Two events of each kind, shuffled, so each kind has a second example."""
    benefits = rng.sample([event for event in WIND_EVENTS if event.kind == BENEFIT], 2)
    harms = rng.sample([event for event in WIND_EVENTS if event.kind == HARM], 2)
    rows = benefits + harms
    rng.shuffle(rows)
    return rows


def _benefit_and_harm(benefit: str, harm: str) -> str:
    return f"{BENEFIT}ของลม เช่น {benefit} ส่วน{HARM}ของลม เช่น {harm}"


@question_type(
    "geo.wind_use_foundation",
    display_name={"th": "ประโยชน์หรือโทษของลม"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=WIND_USE_TOPIC,
)
class WindUseFoundation(QuestionType):
    """Tell a use of wind from something that does not use it, or a harm from a help."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            event = rng.choice([one for one in WIND_EVENTS if one.kind == BENEFIT])
            return _labelled(
                stem="ข้อใดเป็นการใช้ประโยชน์จากลม",
                correct=event.event,
                wrongs=tuple(NOT_WIND),
                hint="หาสิ่งที่ต้องอาศัยอากาศที่เคลื่อนที่จึงจะเกิดขึ้นได้",
                topic=WIND_USE_TOPIC,
            )
        event = rng.choice([one for one in WIND_EVENTS if one.kind == HARM])
        return _labelled(
            stem="ข้อใดเป็นโทษของลม",
            correct=event.event,
            wrongs=tuple(one.event for one in rng.sample(
                [one for one in WIND_EVENTS if one.kind == BENEFIT], 3)),
            hint="หาเหตุการณ์ที่ลมทำให้เกิดความเสียหาย",
            topic=WIND_USE_TOPIC,
        )


@question_type(
    "geo.wind_use_fluency",
    display_name={"th": "บรรยายประโยชน์และโทษของลมจากข้อมูล"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=WIND_USE_TOPIC,
)
class WindUseFluency(QuestionType):
    """Sort a village record into benefit and harm, both in one answer."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rows = wind_record(rng)
        benefits = [row.event for row in rows if row.kind == BENEFIT]
        harms = [row.event for row in rows if row.kind == HARM]
        record = " / ".join(f"เหตุการณ์ {letter}: {row.event}"
                            for letter, row in zip(LETTERS, rows))
        return _labelled(
            stem=f"นักเรียนรวบรวมเหตุการณ์ที่เกิดจากลมในหมู่บ้านในหนึ่งเดือน — {record} "
                 "จากข้อมูลนี้ ข้อใดบรรยายประโยชน์และโทษของลมได้ถูกต้อง",
            correct=_benefit_and_harm(benefits[0], harms[0]),
            wrongs=(_benefit_and_harm(harms[0], benefits[0]),
                    _benefit_and_harm(benefits[0], benefits[1]),
                    _benefit_and_harm(harms[1], harms[0]),
                    # Both halves wrong at once, so the answer is not the
                    # choice every wrong shares one half with.
                    _benefit_and_harm(harms[1], benefits[0]),
                    _benefit_and_harm(harms[0], benefits[1])),
            hint="แยกเหตุการณ์ที่ช่วยคนออกจากเหตุการณ์ที่ทำให้เสียหาย แล้วตรวจทั้งสองส่วนของคำตอบ",
            topic=WIND_USE_TOPIC,
        )


@question_type(
    "geo.wind_use_application",
    display_name={"th": "ใช้ประโยชน์และป้องกันโทษของลม"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=WIND_USE_TOPIC,
)
class WindUseApplication(QuestionType):
    """Prepare for a storm, place a turbine, and weigh benefit against harm."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, WIND_USE_SCENARIOS,
            hint="นึกว่าลมช่วยงานนั้นหรือทำให้เสียหาย แล้วเลือกวิธีที่ได้ประโยชน์และปลอดภัย",
        ), WIND_USE_TOPIC)
