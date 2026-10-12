"""ดาวบนท้องฟ้าเวลากลางวันและกลางคืน

ดาราศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.1/1

Sets moved here from: science_wave_c1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import PRIMARY_ONE, _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c1 import SKY_FACTS, SKY_SURVEY_SCENARIOS, SKY_TOPIC, SUBJECT

PROVENANCE = Provenance("original")


DAY = "กลางวัน"


NIGHT = "กลางคืน"


# Objects the record can show at night. ``ดวงจันทร์`` is kept out: it is the one
# object written on both lines, so it has to be the answer to the "both" branch
# rather than a choice in the other one.
NIGHT_ONLY = ("ดาวเหนือ", "ดาวศุกร์", "กลุ่มดาวนายพราน", "ดาวลูกไก่",
              "ดาวอังคาร", "ดาวพฤหัสบดี")


# Real sky objects that this record simply does not mention. They make wrong
# choices that are wrong *according to the data* without being untrue of the sky.
UNRECORDED = ("ดาวเสาร์", "ดาวหาง", "ดาวพุธ", "กลุ่มดาวจระเข้")


def _sky_record(night: list[str]) -> str:
    """The observation record, with ``ดวงจันทร์`` on both lines by construction."""
    return (f"{DAY}: ดวงอาทิตย์, ดวงจันทร์ (เห็นจาง ๆ)"
            f" / {NIGHT}: ดวงจันทร์, {', '.join(night)}")


@question_type(
    "astro.day_night_sky_foundation",
    display_name={"th": "ดาวบนท้องฟ้ากลางวันและกลางคืน"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=SKY_TOPIC,
)
class DayNightSkyFoundation(QuestionType):
    """Know what the day sky and the night sky hold, before reading any record."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SKY_FACTS,
            hint="นึกถึงสิ่งที่เห็นจริง ๆ เมื่อแหงนมองท้องฟ้าตอนกลางวันและตอนกลางคืน",
        ), SKY_TOPIC)


@question_type(
    "astro.day_night_sky_fluency",
    display_name={"th": "ระบุดาวจากบันทึกการสังเกตท้องฟ้า"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=SKY_TOPIC,
)
class DayNightSkyFluency(QuestionType):
    """Name the stars a record found, in the period it found them.

    This is the indicator's own evidence, ``จากข้อมูลที่รวบรวมได้``: the answer is
    read off the record printed in the stem.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        night = rng.sample(NIGHT_ONLY, 3)
        stem = ("นักเรียนสังเกตท้องฟ้าและบันทึกสิ่งที่มองเห็น ดังนี้ "
                f"{_sky_record(night)} ")
        draw = rng.random()
        if draw < 0.34:
            return _labelled(
                stem=stem + f"จากบันทึกนี้ ข้อใดคือดาวที่พบเฉพาะในเวลา{NIGHT}",
                correct=night[0],
                wrongs=("ดวงอาทิตย์",) + tuple(rng.sample(UNRECORDED, 2)),
                hint=f"ดูบรรทัด “{NIGHT}” ว่ามีชื่อใดบ้าง และชื่อนั้นอยู่ในบรรทัด"
                     f"“{DAY}” ด้วยหรือไม่",
                topic=SKY_TOPIC,
            )
        if draw < 0.67:
            wrongs = list(night)
            rng.shuffle(wrongs)
            return _labelled(
                stem=stem + f"จากบันทึกนี้ ข้อใดคือดาวที่พบเฉพาะในเวลา{DAY}",
                correct="ดวงอาทิตย์", wrongs=tuple(wrongs),
                hint=f"ดูบรรทัด “{DAY}” ว่ามีชื่อใดบ้าง และชื่อนั้นอยู่ในบรรทัด"
                     f"“{NIGHT}” ด้วยหรือไม่",
                topic=SKY_TOPIC,
            )
        wrongs = list(night)
        rng.shuffle(wrongs)
        return _labelled(
            stem=stem + f"จากบันทึกนี้ สิ่งใดพบทั้งในเวลา{DAY}และเวลา{NIGHT}",
            correct="ดวงจันทร์", wrongs=tuple(wrongs),
            hint="หาชื่อที่เขียนไว้ทั้งสองบรรทัด",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.day_night_sky_application",
    display_name={"th": "วิเคราะห์การสังเกตท้องฟ้า"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=SKY_TOPIC,
)
class DayNightSkyApplication(QuestionType):
    """Judge a sky observation: when it looked, where from, what it wrote down."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SKY_SURVEY_SCENARIOS,
            hint="ถามว่าข้อมูลได้มาอย่างไร และสังเกตครบทุกช่วงเวลาแล้วหรือยัง",
        ), SKY_TOPIC)
