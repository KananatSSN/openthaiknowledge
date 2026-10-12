"""ส่วนประกอบและความสำคัญของอากาศ

ธรณีวิทยา · ป.3 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.3/1

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
from otk.sets._support.science_wave_c11 import AIR_SCENARIOS

PROVENANCE = Provenance("original")


AIR_TOPIC = "ส่วนประกอบและความสำคัญของอากาศ"


class Observation(NamedTuple):
    """What a simple activity showed, and the component of air it shows."""
    seen: str
    component: str


# Each activity shows exactly one component, so a record row names one answer.
OBSERVATIONS = (
    Observation("ครอบแก้วลงบนเทียนที่จุดอยู่ ไม่นานเปลวไฟก็ดับ", "แก๊สออกซิเจน"),
    Observation("นำแก้วใส่น้ำแข็งวางไว้ ไม่นานมีหยดน้ำเกาะอยู่รอบนอกแก้ว", "ไอน้ำ"),
    Observation("แสงแดดส่องผ่านช่องหน้าต่างเข้ามาในห้องมืด เห็นผงเล็ก ๆ ลอยอยู่ในลำแสง", "ฝุ่นละออง"),
    Observation("ตั้งน้ำปูนใสทิ้งไว้ในที่เปิดโล่งหลายวัน ผิวหน้าน้ำปูนใสมีฝ้าขุ่นเกิดขึ้น", "แก๊สคาร์บอนไดออกไซด์"),
)


# Parts in every hundred parts of dry air.
COMPOSITION = (("แก๊สไนโตรเจน", 78), ("แก๊สออกซิเจน", 21), ("แก๊สอื่น ๆ", 1))


def observation_record(rows: list[Observation]) -> str:
    return " / ".join(f"กิจกรรม {letter}: {row.seen}"
                      for letter, row in zip(LETTERS, rows))


class Pollution(NamedTuple):
    """A pollution source, the living things it reaches, and what the record counts."""
    source: str
    living: str
    effect: str
    unit: str
    importance: str


POLLUTIONS = (
    Pollution("ฝุ่นละอองจากการเผาไร่", "นักเรียนในโรงเรียน", "ไอและแสบตา", "คน",
              "คนต้องหายใจเอาอากาศเข้าสู่ร่างกายตลอดเวลา"),
    Pollution("ควันจากท่อไอเสียรถยนต์", "ใบของต้นไม้ริมถนน", "มีคราบดำเกาะจนเหลือง", "ใบ",
              "พืชต้องใช้อากาศในการสร้างอาหารและหายใจ"),
    Pollution("ควันจากปล่องโรงงาน", "ผู้สูงอายุในชุมชน", "หายใจลำบากจนต้องไปพบแพทย์", "คน",
              "คนต้องหายใจเอาอากาศเข้าสู่ร่างกายตลอดเวลา"),
)


LEVELS = ("น้อย", "ปานกลาง", "มาก", "มากที่สุด")


def pollution_record(rng: Random, item: Pollution) -> tuple[str, list[tuple[str, int]]]:
    """Four days, shuffled, whose counts rise strictly with the pollution level."""
    counts = sorted(rng.sample(range(2, 30), 4))
    days = list(zip(LEVELS, counts))
    rng.shuffle(days)
    text = " / ".join(
        f"วันที่ {number}: {item.source}{level} พบ{item.living}ที่{item.effect} {count} {item.unit}"
        for number, (level, count) in enumerate(days, start=1))
    return text, days


def _spanning(item: Pollution, rising: bool) -> str:
    direction = "มากขึ้น" if rising else "น้อยลง"
    return (f"อากาศมีความสำคัญเพราะ{item.importance} "
            f"เมื่อ{item.source}ในอากาศเพิ่มขึ้น {item.living}ก็{item.effect}{direction}")


@question_type(
    "geo.air_composition_foundation",
    display_name={"th": "ระบุส่วนประกอบของอากาศจากข้อมูล"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=AIR_TOPIC,
)
class AirCompositionFoundation(QuestionType):
    """Identify the components of air from a chart or an activity record."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            chart = " / ".join(f"{name} {parts} ส่วน" for name, parts in COMPOSITION)
            ranked = sorted(COMPOSITION, key=lambda row: row[1], reverse=True)
            which = rng.randrange(2)
            word = "มากที่สุด" if which == 0 else "มากเป็นอันดับสอง"
            return _labelled(
                stem=f"ข้อมูลส่วนประกอบของอากาศแห้งในทุก 100 ส่วน — {chart} "
                     f"จากข้อมูลนี้ แก๊สใดมีอยู่ในอากาศ{word}",
                correct=ranked[which][0],
                wrongs=tuple(name for name, _ in ranked if name != ranked[which][0])
                       + ("แก๊สคาร์บอนไดออกไซด์",),
                hint="เปรียบเทียบจำนวนส่วนของแต่ละแก๊สในข้อมูล",
                topic=AIR_TOPIC,
            )
        rows = list(OBSERVATIONS)
        rng.shuffle(rows)
        index = rng.randrange(4)
        return _labelled(
            stem=f"นักเรียนทำกิจกรรมและบันทึกผลดังนี้ — {observation_record(rows)} "
                 f"จากบันทึกนี้ กิจกรรมใดแสดงว่าอากาศมี{rows[index].component}",
            correct=f"กิจกรรม {LETTERS[index]}",
            wrongs=tuple(f"กิจกรรม {letter}" for letter in LETTERS if letter != LETTERS[index]),
            hint="นึกว่าสิ่งที่เห็นในแต่ละกิจกรรมเกิดจากส่วนประกอบใดของอากาศ",
            topic=AIR_TOPIC,
        )


@question_type(
    "geo.air_composition_fluency",
    display_name={"th": "บรรยายความสำคัญของอากาศและผลกระทบของมลพิษจากข้อมูล"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=AIR_TOPIC,
)
class AirCompositionFluency(QuestionType):
    """Describe the importance of air and the harm of pollution from one record.

    The indicator's second verb governs both objects, so every answer states both.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(POLLUTIONS)
        record, _ = pollution_record(rng, item)
        return _labelled(
            stem=f"นักเรียนบันทึกข้อมูลเป็นเวลา 4 วัน — {record} "
                 "จากข้อมูลนี้ ข้อใดบรรยายความสำคัญของอากาศและผลกระทบของมลพิษทางอากาศได้ถูกต้อง",
            correct=_spanning(item, rising=True),
            wrongs=(_spanning(item, rising=False),
                    f"อากาศไม่มีความสำคัญต่อ{item.living} "
                    f"เมื่อ{item.source}ในอากาศเพิ่มขึ้น {item.living}จึงไม่ได้รับผลใด ๆ",
                    f"อากาศมีความสำคัญเพราะ{item.importance} "
                    f"แต่{item.source}ในอากาศไม่เกี่ยวกับจำนวน{item.living}ที่{item.effect}"),
            hint="เรียงวันจากมลพิษน้อยไปมาก แล้วดูว่าจำนวนที่นับได้เพิ่มหรือลด",
            topic=AIR_TOPIC,
        )


@question_type(
    "geo.air_composition_application",
    display_name={"th": "ใช้ความรู้เรื่องอากาศและมลพิษในชีวิตประจำวัน"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=AIR_TOPIC,
)
class AirCompositionApplication(QuestionType):
    """Reason about air in a closed room, on a dusty day, and in a fair survey."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, AIR_SCENARIOS,
            hint="นึกว่าสิ่งมีชีวิตใช้อากาศอย่างไร และมลพิษเข้าสู่ร่างกายได้อย่างไร",
        ), AIR_TOPIC)
