"""ลมฟ้าอากาศและปัจจัยที่มีผล

ธรณีวิทยา · ม.1 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.1/2

Sets moved here from: science_wave_c17.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b2 import LEVEL as MIDDLE_ONE
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c17 import WEATHER_SCENARIOS

PROVENANCE = Provenance("original")


WEATHER_TOPIC = "ลมฟ้าอากาศและปัจจัยที่มีผล"


class Factor(NamedTuple):
    """A weather component and the factor that changes it."""
    component: str
    factor: str


FACTORS = (
    Factor("อุณหภูมิอากาศ", "ความเข้มแสงหรือพลังงานจากดวงอาทิตย์ที่พื้นผิวได้รับ"),
    Factor("ความกดอากาศ", "อุณหภูมิของอากาศ เพราะอากาศร้อนขยายตัวและมีความหนาแน่นลดลง"),
    Factor("ลม", "ความกดอากาศสองบริเวณที่แตกต่างกัน"),
    Factor("ความชื้นในอากาศ", "ปริมาณไอน้ำจากการระเหยของแหล่งน้ำและอุณหภูมิของอากาศ"),
    Factor("เมฆและหยาดน้ำฟ้า", "ไอน้ำในอากาศที่ลอยสูงขึ้นแล้วเย็นลงจนควบแน่น"),
)


TIMES = ("06:00", "09:00", "12:00", "15:00", "18:00")


def day_record(rng: Random) -> list[tuple[str, int, int]]:
    """A day's (time, °C, relative humidity %). Temperature rises to one peak at
    12:00 or 15:00 and falls away from it; humidity is lowest exactly at the peak."""
    peak = rng.choice((2, 3))
    base = rng.randint(24, 27)
    by_distance = {0: 11, 1: rng.randint(7, 9), 2: rng.randint(3, 5), 3: rng.randint(0, 2)}
    temps = [base + by_distance[abs(index - peak)] for index in range(len(TIMES))]
    humidity = [95 - (temp - base) * 4 for temp in temps]
    return list(zip(TIMES, temps, humidity))


def _day_text(rows) -> str:
    return " / ".join(f"{time} อุณหภูมิ {temp} องศาเซลเซียส ความชื้นสัมพัทธ์ {rh} %"
                      for time, temp, rh in rows)


@question_type(
    "geo.weather_factors_foundation",
    display_name={"th": "องค์ประกอบของลมฟ้าอากาศและปัจจัยที่มีผล"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=WEATHER_TOPIC,
)
class WeatherFactorsFoundation(QuestionType):
    """Match each weather component to the factor that changes it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(FACTORS)
        others = [other for other in FACTORS if other.component != item.component]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ปัจจัยใดทำให้{item.component}เปลี่ยนแปลง",
                correct=item.factor,
                wrongs=tuple(other.factor for other in others[:3]),
                hint="องค์ประกอบของลมฟ้าอากาศส่งผลต่อกันเป็นทอด ๆ เริ่มจากพลังงานจากดวงอาทิตย์",
                topic=WEATHER_TOPIC,
            )
        return _labelled(
            stem=f"{item.factor} ทำให้องค์ประกอบใดของลมฟ้าอากาศเปลี่ยนแปลงโดยตรง",
            correct=item.component,
            wrongs=tuple(other.component for other in others[:3]),
            hint="องค์ประกอบของลมฟ้าอากาศส่งผลต่อกันเป็นทอด ๆ เริ่มจากพลังงานจากดวงอาทิตย์",
            topic=WEATHER_TOPIC,
        )


@question_type(
    "geo.weather_factors_fluency",
    display_name={"th": "อธิบายปัจจัยที่ทำให้ลมฟ้าอากาศเปลี่ยนแปลงจากข้อมูล"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=WEATHER_TOPIC,
)
class WeatherFactorsFluency(QuestionType):
    """Explain a change from a record: a day's readings, or pressure at two places."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            rows = day_record(rng)
            record = _day_text(rows)
            hottest = max(rows, key=lambda row: row[1])[0]
            return _labelled(
                stem=f"ข้อมูลที่บันทึกได้ในวันหนึ่ง — {record} "
                     "จากข้อมูลนี้ ช่วงเวลาใดความชื้นสัมพัทธ์ต่ำที่สุด และเพราะเหตุใด",
                correct=f"{hottest} เพราะอุณหภูมิสูงสุด อากาศร้อนจุไอน้ำได้มาก "
                        "ความชื้นสัมพัทธ์จึงต่ำ",
                wrongs=("06:00 เพราะอุณหภูมิต่ำที่สุด อากาศเย็นจุไอน้ำได้มากกว่าอากาศร้อนในทุกช่วงเวลา",
                        f"{hottest} เพราะแดดแรงทำให้ไอน้ำในอากาศระเหยหายไปหมดจนไม่เหลือเลย",
                        "18:00 เพราะดวงอาทิตย์ตก ไอน้ำจึงระเหยออกจากอากาศไปจนหมด"),
                hint="เทียบคอลัมน์อุณหภูมิกับความชื้นสัมพัทธ์ในเวลาเดียวกัน",
                topic=WEATHER_TOPIC,
            )
        high, low = rng.sample(("ก", "ข"), 2)
        high_hpa = rng.randint(1010, 1016)
        low_hpa = high_hpa - rng.randint(4, 9)
        values = {high: high_hpa, low: low_hpa}
        return _labelled(
            stem=f"สถานีตรวจอากาศสองแห่งที่อยู่ใกล้กันวัดความกดอากาศได้ — "
                 f"สถานี ก {values['ก']} เฮกโตพาสคัล / สถานี ข {values['ข']} เฮกโตพาสคัล "
                 "จากข้อมูลนี้ ลมน่าจะพัดไปทางใด และเพราะเหตุใด",
            correct=f"จากสถานี {high} ไปสถานี {low} เพราะอากาศเคลื่อนที่จากบริเวณความกดอากาศสูงไปยังบริเวณความกดอากาศต่ำ",
            wrongs=(f"จากสถานี {low} ไปสถานี {high} เพราะอากาศเคลื่อนที่จากบริเวณความกดอากาศต่ำไปยังบริเวณความกดอากาศสูง",
                    f"จากสถานี {high} ไปสถานี {low} เพราะอากาศที่มีความกดอากาศสูงร้อนกว่าจึงลอยตัวขึ้น",
                    "ไม่มีลม เพราะความกดอากาศไม่เกี่ยวกับการเกิดลม"),
            hint="หาสถานีที่ความกดอากาศสูงกว่า แล้วนึกว่าอากาศเคลื่อนไปทางใด",
            topic=WEATHER_TOPIC,
        )


@question_type(
    "geo.weather_factors_application",
    display_name={"th": "ใช้ปัจจัยของลมฟ้าอากาศอธิบายเหตุการณ์"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=WEATHER_TOPIC,
)
class WeatherFactorsApplication(QuestionType):
    """Mountains, cloudy nights, sea air, and designing a fair record."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, WEATHER_SCENARIOS,
            hint="หาว่าองค์ประกอบใดเปลี่ยน แล้วย้อนหาปัจจัยที่ทำให้เปลี่ยน",
        ), WEATHER_TOPIC)
