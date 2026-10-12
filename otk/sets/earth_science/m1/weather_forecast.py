"""การพยากรณ์อากาศ

ธรณีวิทยา · ม.1 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.1/4

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
from otk.sets._support.science_wave_c17 import FORECAST_SCENARIOS

PROVENANCE = Provenance("original")


FORECAST_TOPIC = "การพยากรณ์อากาศ"


class Instrument(NamedTuple):
    """A weather instrument and what it measures."""
    name: str
    measures: str


INSTRUMENTS = (
    Instrument("เทอร์โมมิเตอร์", "อุณหภูมิอากาศ"),
    Instrument("บารอมิเตอร์", "ความกดอากาศ"),
    Instrument("ไฮกรอมิเตอร์", "ความชื้นในอากาศ"),
    Instrument("อะนีมอมิเตอร์", "อัตราเร็วลม"),
    Instrument("ศรลม", "ทิศทางลม"),
    Instrument("เครื่องวัดปริมาณน้ำฝน", "ปริมาณน้ำฝน"),
)


FORECAST_STEPS = (
    "ตรวจวัดองค์ประกอบของลมฟ้าอากาศจากสถานีตรวจอากาศ ดาวเทียม และเรดาร์",
    "รวบรวมและส่งข้อมูลไปยังศูนย์พยากรณ์อากาศ",
    "วิเคราะห์ข้อมูลด้วยแผนที่อากาศและแบบจำลองทางคอมพิวเตอร์",
    "จัดทำคำพยากรณ์และเผยแพร่ให้ประชาชน",
)


RAIN = "มีโอกาสเกิดฝนตกในวันถัดไป"


CLEAR = "ท้องฟ้าน่าจะแจ่มใสและมีโอกาสเกิดฝนน้อยในวันถัดไป"


def forecast_record(rng: Random) -> tuple[str, list[tuple[str, int, int, str]]]:
    """Three days whose trends decide the forecast: pressure falling with humidity
    and cloud rising means rain; the reverse means clear weather."""
    outcome = rng.choice((RAIN, CLEAR))
    pressures = sorted(rng.sample(range(1004, 1016), 3), reverse=(outcome == RAIN))
    humidities = sorted(rng.sample(range(55, 95, 5), 3), reverse=(outcome == CLEAR))
    clouds = ["มีเมฆเล็กน้อย", "มีเมฆบางส่วน", "มีเมฆมาก"]
    if outcome == CLEAR:
        clouds.reverse()
    days = [(f"วันที่ {n}", p, h, c) for n, p, h, c in zip((1, 2, 3), pressures, humidities, clouds)]
    return outcome, days


@question_type(
    "geo.weather_forecast_foundation",
    display_name={"th": "อธิบายการพยากรณ์อากาศ"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=FORECAST_TOPIC,
)
class WeatherForecastFoundation(QuestionType):
    """Explain how a forecast is made: its instruments and its steps."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            order = list(FORECAST_STEPS)
            wrong_orders: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
            while len(wrong_orders) < 3:
                shuffled = order[:]
                rng.shuffle(shuffled)
                if shuffled != order:
                    wrong_orders[" → ".join(shuffled)] = None
            return _labelled(
                stem="ข้อใดเรียงลำดับขั้นตอนการพยากรณ์อากาศได้ถูกต้อง",
                correct=" → ".join(order),
                wrongs=tuple(wrong_orders),
                hint="ต้องมีข้อมูลก่อนจึงวิเคราะห์ได้ และต้องวิเคราะห์ก่อนจึงพยากรณ์ได้",
                topic=FORECAST_TOPIC,
            )
        item = rng.choice(INSTRUMENTS)
        others = [other for other in INSTRUMENTS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ในการพยากรณ์อากาศ {item.name}ใช้ตรวจวัดสิ่งใด",
                correct=item.measures,
                wrongs=tuple(other.measures for other in others[:3]),
                hint="นึกถึงชื่อเครื่องมือ ซึ่งมักบอกสิ่งที่วัด",
                topic=FORECAST_TOPIC,
            )
        return _labelled(
            stem=f"ในการพยากรณ์อากาศ ต้องใช้เครื่องมือใดตรวจวัด{item.measures}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="นึกถึงชื่อเครื่องมือ ซึ่งมักบอกสิ่งที่วัด",
            topic=FORECAST_TOPIC,
        )


@question_type(
    "geo.weather_forecast_fluency",
    display_name={"th": "พยากรณ์อากาศอย่างง่ายจากข้อมูล"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=FORECAST_TOPIC,
)
class WeatherForecastFluency(QuestionType):
    """Make a simple forecast from three days of readings — the second free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        outcome, days = forecast_record(rng)
        record = " / ".join(f"{day}: ความกดอากาศ {p} เฮกโตพาสคัล ความชื้นสัมพัทธ์ {h} % {c}"
                            for day, p, h, c in days)
        other = CLEAR if outcome == RAIN else RAIN
        falling = outcome == RAIN
        reason = ("ความกดอากาศลดลง ความชื้นและเมฆเพิ่มขึ้น" if falling
                  else "ความกดอากาศสูงขึ้น ความชื้นและเมฆลดลง")
        wrong_reason = ("ความกดอากาศสูงขึ้น ความชื้นและเมฆลดลง" if falling
                        else "ความกดอากาศลดลง ความชื้นและเมฆเพิ่มขึ้น")
        return _labelled(
            stem=f"นักเรียนบันทึกข้อมูลลมฟ้าอากาศติดต่อกัน 3 วัน — {record} "
                 "จากข้อมูลนี้ พยากรณ์อากาศในวันที่ 4 ได้อย่างไร",
            correct=f"{outcome} เพราะ{reason}",
            wrongs=(f"{other} เพราะ{reason}",
                    f"{outcome} เพราะ{wrong_reason}",
                    f"{other} เพราะ{wrong_reason}"),
            hint="ดูแนวโน้มของความกดอากาศ ความชื้น และเมฆจากวันที่ 1 ถึงวันที่ 3",
            topic=FORECAST_TOPIC,
        )


@question_type(
    "geo.weather_forecast_application",
    display_name={"th": "ใช้คำพยากรณ์อากาศในชีวิตจริง"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=FORECAST_TOPIC,
)
class WeatherForecastApplication(QuestionType):
    """Read a percentage forecast, plan a farm day, and see why range costs accuracy."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, FORECAST_SCENARIOS,
            hint="นึกว่าคำพยากรณ์บอกอะไร และข้อมูลใดทำให้พยากรณ์ได้",
        ), FORECAST_TOPIC)
