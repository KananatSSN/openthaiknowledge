"""การเกิดลม

ธรณีวิทยา · ป.3 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.3/3

Sets moved here from: science_wave_c11.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import PRIMARY_THREE, _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c11 import WIND_FACTS, WIND_SCENARIOS

PROVENANCE = Provenance("original")


WIND_TOPIC = "การเกิดลม"


PLACES = (
    ("ลานคอนกรีต", "สระน้ำ"),
    ("ถนนลาดยาง", "สนามหญ้าใต้ร่มไม้"),
    ("หาดทรายตอนกลางวัน", "ผิวน้ำทะเลตอนกลางวัน"),
    ("หลังคาสังกะสี", "ลานใต้ต้นไม้ใหญ่"),
)


def thermometer_readings(rng: Random) -> tuple[int, int]:
    """Two air temperatures that always differ by at least three degrees."""
    cool = rng.randint(26, 31)
    return cool + rng.randint(3, 8), cool


@question_type(
    "geo.wind_origin_foundation",
    display_name={"th": "ลมและอากาศร้อนลอยตัว"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=WIND_TOPIC,
)
class WindOriginFoundation(QuestionType):
    """Know what wind is and that warmed air rises, before reading evidence."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, WIND_FACTS,
            hint="อากาศร้อนลอยขึ้น อากาศเย็นกว่าเคลื่อนเข้ามาแทนที่",
        ), WIND_TOPIC)


@question_type(
    "geo.wind_origin_fluency",
    display_name={"th": "อธิบายการเกิดลมจากผลการวัดอุณหภูมิ"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=WIND_TOPIC,
)
class WindOriginFluency(QuestionType):
    """Explain the wind from measured temperatures and a smoke trail — the evidence."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hot_place, cool_place = rng.choice(PLACES)
        hot, cool = thermometer_readings(rng)
        first, second = (hot_place, hot), (cool_place, cool)
        if rng.random() < 0.5:
            first, second = second, first
        record = (f"นักเรียนวัดอุณหภูมิอากาศเหนือสองบริเวณที่อยู่ติดกันในเวลาเดียวกัน — "
                  f"{first[0]} {first[1]} องศาเซลเซียส / {second[0]} {second[1]} องศาเซลเซียส")
        if rng.random() < 0.5:
            return _labelled(
                stem=f"{record} จากข้อมูลนี้ ลมที่พัดใกล้พื้นน่าจะพัดไปทางใด",
                correct=f"พัดจาก{cool_place}ไปยัง{hot_place}",
                wrongs=(f"พัดจาก{hot_place}ไปยัง{cool_place}",
                        "ไม่มีลมพัดเลย เพราะสองบริเวณอยู่ติดกัน",
                        f"พัดวนอยู่เหนือ{cool_place}เท่านั้น"),
                hint="อากาศเหนือบริเวณที่ร้อนกว่าลอยขึ้น อากาศจากบริเวณที่เย็นกว่าเข้ามาแทนที่",
                topic=WIND_TOPIC,
            )
        return _labelled(
            stem=f"{record} และเมื่อจุดธูปไว้ระหว่างสองบริเวณ ควันธูปลอยเอียงไปทาง{hot_place} "
                 "ข้อใดอธิบายการเกิดลมจากหลักฐานนี้ได้ถูกต้อง",
            correct=f"อากาศเหนือ{hot_place}ร้อนกว่าจึงลอยตัวสูงขึ้น "
                    f"อากาศที่เย็นกว่าจาก{cool_place}จึงเคลื่อนเข้ามาแทนที่ เกิดเป็นลม",
            wrongs=(f"อากาศเหนือ{cool_place}ร้อนกว่าจึงลอยตัวสูงขึ้น "
                    f"อากาศจาก{hot_place}จึงเคลื่อนเข้ามาแทนที่ เกิดเป็นลม",
                    f"อากาศเหนือ{hot_place}หนักกว่าจึงจมลงและดันควันออกไป",
                    "ควันธูปเอียงเพราะธูปถูกจุดไม่ตรง ไม่เกี่ยวกับอุณหภูมิ"),
            hint="เทียบอุณหภูมิสองบริเวณก่อน แล้วดูว่าอากาศที่ร้อนกว่าทำอย่างไร",
            topic=WIND_TOPIC,
        )


@question_type(
    "geo.wind_origin_application",
    display_name={"th": "ใช้หลักการเกิดลมอธิบายเหตุการณ์ใหม่"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=WIND_TOPIC,
)
class WindOriginApplication(QuestionType):
    """Explain a sea breeze and a curtain, and design a fair test of the idea."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, WIND_SCENARIOS,
            hint="หาว่าบริเวณใดร้อนกว่า แล้วนึกว่าอากาศเย็นกว่าจะเคลื่อนไปทางใด",
        ), WIND_TOPIC)
