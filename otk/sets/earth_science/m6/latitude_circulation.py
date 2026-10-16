"""การหมุนเวียนของอากาศตามเขตละติจูด

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/10

Sets moved here from: science_wave_c25.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c25 import LATITUDE_SCENARIOS

PROVENANCE = Provenance("original")


LATITUDE_TOPIC = "การหมุนเวียนของอากาศตามเขตละติจูด"


class Belt(NamedTuple):
    """A latitude line: what the air does there, and the climate that follows."""
    latitude: str
    circulation: str
    climate: str


BELTS = (
    Belt("0 องศา (เส้นศูนย์สูตร)",
         "อากาศร้อนชื้นลอยตัวขึ้น ความกดอากาศที่ผิวพื้นต่ำ",
         "เมฆก่อตัวและฝนตกชุกเกือบตลอดปี จึงพบป่าดิบชื้น"),
    Belt("30 องศา",
         "อากาศที่เย็นลงจากระดับบนจมตัวลง ความกดอากาศที่ผิวพื้นสูง",
         "อากาศที่จมตัวลงอุ่นขึ้นและแห้ง ฝนตกน้อย จึงพบทะเลทรายขนาดใหญ่"),
    Belt("60 องศา",
         "อากาศอุ่นจากละติจูดกลางปะทะอากาศเย็นจากขั้วโลกแล้วถูกยกตัวขึ้น ความกดอากาศที่ผิวพื้นต่ำ",
         "มีเมฆ หยาดน้ำฟ้า และพายุบ่อย อากาศเย็นและชื้น"),
    Belt("90 องศา (ขั้วโลก)",
         "อากาศเย็นจัดและหนาแน่นจมตัวลง ความกดอากาศที่ผิวพื้นสูง",
         "หนาวจัดและมีหยาดน้ำฟ้าน้อยมาก"),
)


# Real places on or near each line, by the line's index in BELTS. Each reads
# before ``ละติจูด``, so the stem still names the line itself.
PLACES = (
    ("ลุ่มน้ำแอมะซอน ใกล้", "ลุ่มน้ำคองโก ใกล้", "หมู่เกาะอินโดนีเซีย ใกล้"),
    ("ทะเลทรายสะฮารา ใกล้", "ทะเลทรายเกรตวิกตอเรียในออสเตรเลีย ใกล้", "ทะเลทรายโซโนราในอเมริกาเหนือ ใกล้"),
    ("ประเทศนอร์เวย์ตอนใต้ ใกล้", "รัฐอะแลสกาตอนใต้ ใกล้", "มหาสมุทรใต้ทางใต้ของแหลมฮอร์น ใกล้"),
    ("ใจกลางมหาสมุทรอาร์กติก ที่", "ใจกลางทวีปแอนตาร์กติกา ที่"),
)

# Each rising belt is paired with a sinking one, so a swapped half is plainly wrong.
OPPOSITE = {0: 1, 1: 0, 2: 3, 3: 2}


def belt_line(circulation: str, climate: str) -> str:
    return f"การหมุนเวียนของอากาศ: {circulation} / ผลต่อภูมิอากาศ: {climate}"


class WindBelt(NamedTuple):
    band: str
    cell: str
    name: str
    north: str
    south: str


WIND_BELTS = (
    WindBelt("0–30 องศา", "เซลล์แฮดลีย์", "ลมค้า", "ทิศตะวันออกเฉียงเหนือ", "ทิศตะวันออกเฉียงใต้"),
    WindBelt("30–60 องศา", "เซลล์เฟอร์เรล", "ลมตะวันตก", "ทิศตะวันตกเฉียงใต้", "ทิศตะวันตกเฉียงเหนือ"),
    WindBelt("60–90 องศา", "เซลล์ขั้วโลก", "ลมตะวันออกขั้วโลก", "ทิศตะวันออกเฉียงเหนือ", "ทิศตะวันออกเฉียงใต้"),
)


def wind_text(belt: WindBelt, north: bool) -> str:
    return f"{belt.name}ใน{belt.cell} พัดมาจาก{belt.north if north else belt.south}"


@question_type(
    "geo.latitude_circulation_foundation",
    display_name={"th": "ระบุลมประจำและเซลล์การหมุนเวียนตามเขตละติจูด"},
    level=UPPER_SIX, subject=SUBJECT, topic=LATITUDE_TOPIC,
)
class LatitudeCirculationFoundation(QuestionType):
    """A band in one hemisphere; its surface wind and cell."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        draw = rng.random()
        if draw < 0.25:
            # One latitude line, and what the air near the ground does there.
            index = rng.randrange(len(BELTS))
            return _labelled(
                stem=f"ที่ละติจูด {BELTS[index].latitude} อากาศใกล้ผิวพื้นมีลักษณะอย่างไร",
                correct=BELTS[index].circulation,
                wrongs=tuple(other.circulation for i, other in enumerate(BELTS) if i != index),
                hint="เส้นศูนย์สูตรกับละติจูด 60 องศาอากาศลอยตัวขึ้น ละติจูด 30 องศากับขั้วโลกอากาศจมตัวลง",
                topic=LATITUDE_TOPIC,
            )
        index = rng.randrange(len(WIND_BELTS))
        belt = WIND_BELTS[index]
        north = rng.random() < 0.5
        hemisphere = "เหนือ" if north else "ใต้"
        if draw < 0.5:
            # The wind named in full; the learner gives back its band and hemisphere.
            return _labelled(
                stem=f"“{wind_text(belt, north)}” เป็นลมประจำที่พัดใกล้ผิวพื้นในช่วงละติจูดใด",
                correct=f"{belt.band}{hemisphere}",
                wrongs=tuple(f"{other.band}{side}" for other in WIND_BELTS for side in ("เหนือ", "ใต้")
                             if (other.band, side) != (belt.band, hemisphere)),
                hint="ชื่อเซลล์บอกช่วงละติจูด และทิศที่ลมพัดมาบอกว่าอยู่ซีกโลกใด",
                topic=LATITUDE_TOPIC,
            )
        return _labelled(
            stem=f"ลมประจำที่พัดใกล้ผิวพื้นระหว่างละติจูด {belt.band}{hemisphere} คือลมใด",
            correct=wind_text(belt, north),
            wrongs=tuple([wind_text(belt, not north)]
                + [wind_text(other, side) for i, other in enumerate(WIND_BELTS) if i != index
                   for side in (north, not north)]),
            hint="ระบุเซลล์จากช่วงละติจูดก่อน แล้วนึกว่าอากาศใกล้ผิวพื้นไหลไปทางใดและเบนไปทางใดในซีกโลกนั้น",
            topic=LATITUDE_TOPIC,
        )


@question_type(
    "geo.latitude_circulation_fluency",
    display_name={"th": "อธิบายการหมุนเวียนของอากาศตามเขตละติจูดและผลต่อภูมิอากาศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=LATITUDE_TOPIC,
)
class LatitudeCirculationFluency(QuestionType):
    """A latitude line; the circulation there and the climate it makes, together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(BELTS))
        belt = BELTS[index]
        _other = BELTS[rng.choice([i for i in range(len(BELTS)) if i not in (index, OPPOSITE[index])])]
        return _labelled(
            stem=(f"ข้อใดอธิบายการหมุนเวียนของอากาศบริเวณ{rng.choice(('', *PLACES[index]))}"
                  f"ละติจูด {belt.latitude} "
                  "และผลที่มีต่อภูมิอากาศบริเวณนั้นได้ถูกต้องทั้งหมด"),
            correct=belt_line(belt.circulation, belt.climate),
            # Any pairing that gets at least one half wrong for this belt.
            wrongs=tuple([belt_line(belt.circulation, one.climate) for one in BELTS if one is not belt]
                + [belt_line(one.circulation, belt.climate) for one in BELTS if one is not belt]
                + [belt_line(one.circulation, one.climate) for one in BELTS if one is not belt]),
            hint="อากาศลอยตัวขึ้นที่ใดจะเกิดเมฆและฝน อากาศจมตัวลงที่ใดจะแห้ง",
            topic=LATITUDE_TOPIC,
        )


@question_type(
    "geo.latitude_circulation_application",
    display_name={"th": "วิเคราะห์ทะเลทราย แถบฝน และลมตะวันตก"},
    level=UPPER_SIX, subject=SUBJECT, topic=LATITUDE_TOPIC,
)
class LatitudeCirculationApplication(QuestionType):
    """Deserts near 30 degrees, the migrating rain belt, and flights on the westerlies."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, LATITUDE_SCENARIOS,
            hint="ระบุเขตละติจูดก่อน แล้วนึกว่าอากาศที่นั่นลอยตัวขึ้นหรือจมตัวลง และลมใกล้ผิวพื้นพัดทางใด",
        ), LATITUDE_TOPIC)
