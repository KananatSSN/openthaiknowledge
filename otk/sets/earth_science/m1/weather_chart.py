"""การอ่านแผนที่อากาศอย่างง่าย

ธรณีวิทยา · ม.1 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.1/4

Sets moved here from: science_wave_g2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.ms1_diagrams import (
    SIDE_WORDS,
    WEATHER_CHARTS,
    diagram_question,
    weather_chart_alt,
)
from otk.sets._support.science_wave_b2 import LEVEL as MIDDLE_ONE
from otk.sets._support.science_wave_c10 import SUBJECT as GEO_SUBJECT

PROVENANCE = Provenance("original")


WEATHER_CHART_TOPIC = "การอ่านแผนที่อากาศอย่างง่าย"


@question_type(
    "geo.weather_chart_foundation",
    display_name={"th": "อ่านศูนย์กลางความกดอากาศสูงและต่ำจากแผนที่อากาศ"},
    level=MIDDLE_ONE, subject=GEO_SUBJECT, topic=WEATHER_CHART_TOPIC,
)
class WeatherChartFoundation(QuestionType):
    """Which side the H is on — reading the chart before interpreting it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(WEATHER_CHARTS)
        high, low = SIDE_WORDS[spec.high_side], SIDE_WORDS[spec.low_side]
        return diagram_question(
            spec.asset_id, weather_chart_alt(spec),
            stem="จากแผนที่อากาศ ศูนย์กลางความกดอากาศสูงและความกดอากาศต่ำอยู่ด้านใด",
            correct=f"ความกดอากาศสูงอยู่ด้าน{high} ความกดอากาศต่ำอยู่ด้าน{low}",
            wrongs=tuple(rng.sample((
                f"ความกดอากาศสูงอยู่ด้าน{low} ความกดอากาศต่ำอยู่ด้าน{high}",
                f"เป็นความกดอากาศสูงทั้งสองด้าน โดยด้าน{high}สูงกว่า",
                f"เป็นความกดอากาศต่ำทั้งสองด้าน โดยด้าน{low}ต่ำกว่า",
                f"ศูนย์กลางทั้งสองอยู่ด้าน{high} โดยความกดอากาศสูงอยู่ด้านบนของความกดอากาศต่ำ",
                "แผนที่นี้ไม่มีศูนย์กลางความกดอากาศ เพราะมีเพียงเส้นไอโซบาร์",
            ), 3)),
            hint="อักษร H คือศูนย์กลางความกดอากาศสูง อักษร L คือศูนย์กลางความกดอากาศต่ำ",
            topic=WEATHER_CHART_TOPIC,
        )


@question_type(
    "geo.weather_chart_fluency",
    display_name={"th": "บอกทิศทางการเคลื่อนที่ของอากาศจากแผนที่อากาศ"},
    level=MIDDLE_ONE, subject=GEO_SUBJECT, topic=WEATHER_CHART_TOPIC,
)
class WeatherChartFluency(QuestionType):
    """Air moves from high pressure to low; the chart says which way that is."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(WEATHER_CHARTS)
        high, low = SIDE_WORDS[spec.high_side], SIDE_WORDS[spec.low_side]
        return diagram_question(
            spec.asset_id, weather_chart_alt(spec),
            stem="จากแผนที่อากาศ อากาศจะเคลื่อนที่ในทิศใด และเพราะเหตุใด",
            correct=(f"เคลื่อนจากด้าน{high}ไปยังด้าน{low} "
                     f"เพราะอากาศเคลื่อนจากบริเวณความกดอากาศสูงไปยังบริเวณความกดอากาศต่ำ"),
            wrongs=tuple(rng.sample((
                f"เคลื่อนจากด้าน{low}ไปยังด้าน{high} "
                f"เพราะอากาศเคลื่อนจากบริเวณความกดอากาศต่ำไปยังบริเวณความกดอากาศสูง",
                "ไม่เคลื่อนที่ เพราะความกดอากาศทั้งสองบริเวณหักล้างกันพอดี",
                "เคลื่อนขึ้นในแนวดิ่งทั้งสองบริเวณเท่ากัน เพราะความกดอากาศไม่เกี่ยวกับทิศทางลม",
                f"เคลื่อนจากด้าน{high}ไปยังด้าน{low} เพราะอากาศที่ร้อนกว่าอยู่ด้าน{high}เสมอ",
                f"เคลื่อนจากด้าน{low}ไปยังด้าน{high} เพราะความกดอากาศต่ำดันอากาศออกไป",
            ), 3)),
            hint="ลมเกิดจากอากาศเคลื่อนที่จากที่ที่ความกดอากาศสูงกว่าไปยังที่ที่ความกดอากาศต่ำกว่า",
            topic=WEATHER_CHART_TOPIC,
        )


@question_type(
    "geo.weather_chart_application",
    display_name={"th": "พยากรณ์ลักษณะอากาศอย่างง่ายจากแผนที่อากาศ"},
    level=MIDDLE_ONE, subject=GEO_SUBJECT, topic=WEATHER_CHART_TOPIC,
)
class WeatherChartApplication(QuestionType):
    """What the weather is likely to be near each centre, and why."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(WEATHER_CHARTS)
        high, low = SIDE_WORDS[spec.high_side], SIDE_WORDS[spec.low_side]
        return diagram_question(
            spec.asset_id, weather_chart_alt(spec),
            stem="จากแผนที่อากาศ บริเวณใดมีโอกาสเกิดเมฆและฝนมากกว่ากัน และเพราะเหตุใด",
            correct=f"บริเวณด้าน{low} เพราะความกดอากาศต่ำทำให้อากาศลอยตัวขึ้น เย็นลงและควบแน่นเป็นเมฆ",
            wrongs=tuple(rng.sample((
                f"บริเวณด้าน{high} เพราะที่ความกดอากาศสูงอากาศลอยตัวขึ้นและควบแน่นเป็นเมฆได้ง่าย",
                f"บริเวณด้าน{high} เพราะความกดอากาศที่สูงกว่าบีบให้ไอน้ำกลายเป็นฝนทันที",
                "ทั้งสองบริเวณมีโอกาสเท่ากัน เพราะความกดอากาศไม่เกี่ยวกับการเกิดเมฆ",
                f"บริเวณด้าน{low} เพราะที่ความกดอากาศต่ำอากาศจมตัวลงและอุ่นขึ้น",
                f"บริเวณด้าน{high} เพราะลมพัดเมฆทั้งหมดไปรวมที่ความกดอากาศสูง",
            ), 3)),
            hint="ที่ความกดอากาศต่ำ อากาศลอยขึ้น ที่ความกดอากาศสูง อากาศจมลง แล้วคิดต่อว่าไอน้ำควบแน่นเมื่อใด",
            topic=WEATHER_CHART_TOPIC,
        )
