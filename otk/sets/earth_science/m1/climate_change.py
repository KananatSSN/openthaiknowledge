"""การเปลี่ยนแปลงภูมิอากาศโลก

ธรณีวิทยา · ม.1 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.1/6

Sets moved here from: science_wave_c18.
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
from otk.sets._support.science_wave_c18 import CLIMATE_SCENARIOS

PROVENANCE = Provenance("original")


CLIMATE_TOPIC = "การเปลี่ยนแปลงภูมิอากาศโลก"


class Series(NamedTuple):
    """A climate record: what was measured, its unit, how it moves, and what follows."""
    measure: str
    unit: str
    scale: int
    rising: bool
    values: tuple[tuple[int, int], ...]
    situation: str
    effect: str
    false_effect: str


DECADES = ("พ.ศ. 2523", "พ.ศ. 2533", "พ.ศ. 2543", "พ.ศ. 2553", "พ.ศ. 2563")


# Rounded, per-decade ranges in units of 1/scale; the record draws one value from
# each, and the ranges do not overlap, so every draw keeps the real trend's
# direction. Every consequence of warming is linked, so a wrong effect is one the
# record contradicts, never another record's true effect.
SERIES = (
    Series("อุณหภูมิเฉลี่ยของโลกที่สูงกว่าค่าเฉลี่ยในอดีต", "องศาเซลเซียส", 100, True,
           ((10, 20), (30, 40), (50, 60), (70, 80), (95, 110)),
           "อุณหภูมิเฉลี่ยของโลกสูงขึ้นอย่างต่อเนื่อง",
           "ธารน้ำแข็งและน้ำแข็งขั้วโลกละลายมากขึ้น และเกิดคลื่นความร้อนบ่อยขึ้น",
           "น้ำแข็งขั้วโลกขยายตัวมากขึ้น และฤดูหนาวยาวนานขึ้นทั่วโลกทุกปี"),
    Series("ระดับน้ำทะเลเฉลี่ยของโลกเทียบกับปี พ.ศ. 2523", "มิลลิเมตร", 1, True,
           ((0, 5), (15, 25), (40, 50), (65, 75), (95, 105)),
           "ระดับน้ำทะเลเฉลี่ยสูงขึ้นอย่างต่อเนื่อง",
           "ชายฝั่งถูกกัดเซาะมากขึ้น และพื้นที่ชายฝั่งที่อยู่ต่ำเสี่ยงต่อน้ำท่วม",
           "ชายฝั่งงอกยื่นออกไปในทะเล และพื้นที่ชายฝั่งที่อยู่ต่ำปลอดภัยจากน้ำท่วมมากขึ้น"),
    Series("พื้นที่น้ำแข็งในมหาสมุทรอาร์กติกช่วงปลายฤดูร้อน", "ล้านตารางกิโลเมตร", 10, False,
           ((70, 75), (62, 67), (55, 60), (46, 51), (38, 43)),
           "พื้นที่น้ำแข็งในมหาสมุทรอาร์กติกลดลงอย่างต่อเนื่อง",
           "หมีขั้วโลกและสัตว์ที่อาศัยบนแผ่นน้ำแข็งสูญเสียที่อยู่และแหล่งหาอาหาร",
           "หมีขั้วโลกและสัตว์ที่อาศัยบนแผ่นน้ำแข็งมีพื้นที่หาอาหารกว้างขึ้น"),
)


def climate_record(rng: Random, series: Series) -> list[tuple[str, int]]:
    return [(decade, rng.randint(*band)) for decade, band in zip(DECADES, series.values)]


def show(series: Series, value: int) -> str:
    places = {1: 0, 10: 1, 100: 2}[series.scale]
    return f"{value / series.scale:.{places}f}"


def _reversed_situation(series: Series) -> str:
    return (series.situation.replace("สูงขึ้น", "ลดลง") if series.rising
            else series.situation.replace("ลดลง", "เพิ่มขึ้น"))


def _answer(situation: str, effect: str) -> str:
    return f"สถานการณ์: {situation} / ผลกระทบ: {effect}"


# Wrong effects and wrong causes for the foundation, two and three drawn per question.
EFFECT_DECOYS = (
    "ไม่มีผลกระทบต่อสิ่งมีชีวิตและสิ่งแวดล้อมใด ๆ",
    "โลกจะกลับเข้าสู่ยุคน้ำแข็งภายในไม่กี่ปี",
    "ฤดูกาลทั่วโลกจะหายไปเหลือเพียงฤดูเดียว คือฤดูร้อนที่ยาวตลอดทั้งปี",
    "โลกจะหยุดหมุนรอบตัวเองชั่วคราว",
)


CAUSE_DECOYS = (
    "ดวงอาทิตย์เคลื่อนเข้าใกล้โลกมากขึ้นทุกปี ทำให้โลกได้รับความร้อนมากขึ้นเรื่อย ๆ",
    "ชั้นโอโซนหนาขึ้นจนกักความร้อนไว้",
    "ดวงจันทร์โคจรเร็วขึ้น",
    "แกนโลกหยุดเอียงตั้งแต่ร้อยปีก่อน",
    "ภูเขาไฟทั่วโลกระเบิดพร้อมกันทุกปี ปล่อยความร้อนจากใต้ดินขึ้นมาในบรรยากาศ",
)


@question_type(
    "geo.climate_change_foundation",
    display_name={"th": "การเปลี่ยนแปลงภูมิอากาศโลกและสาเหตุ"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=CLIMATE_TOPIC,
)
class ClimateChangeFoundation(QuestionType):
    """Match each change to what follows from it, without a record."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        series = rng.choice(SERIES)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"เมื่อ{series.situation} จะเกิดผลกระทบใดตามมา",
                correct=series.effect,
                wrongs=(series.false_effect, *rng.sample(EFFECT_DECOYS, 2)),
                hint="นึกว่าสิ่งที่เปลี่ยนไปนั้นกระทบต่ออะไรโดยตรง",
                topic=CLIMATE_TOPIC,
            )
        return _labelled(
            stem="สาเหตุหลักที่ทำให้ภูมิอากาศโลกเปลี่ยนแปลงอย่างรวดเร็วในช่วงร้อยปีที่ผ่านมาคืออะไร",
            correct="แก๊สเรือนกระจกที่เพิ่มขึ้นจากกิจกรรมของมนุษย์ เช่น การเผาเชื้อเพลิงและการตัดไม้",
            wrongs=tuple(CAUSE_DECOYS),
            hint="นึกถึงสิ่งที่มนุษย์ปล่อยสู่บรรยากาศมากขึ้นตั้งแต่มีอุตสาหกรรม",
            topic=CLIMATE_TOPIC,
        )


@question_type(
    "geo.climate_change_fluency",
    display_name={"th": "อธิบายสถานการณ์และผลกระทบการเปลี่ยนแปลงภูมิอากาศจากข้อมูล"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=CLIMATE_TOPIC,
)
class ClimateChangeFluency(QuestionType):
    """State the trend a record shows and an effect that follows, in one answer."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        series = rng.choice(SERIES)
        record = " / ".join(f"{decade}: {show(series, value)}"
                            for decade, value in climate_record(rng, series))
        return _labelled(
            stem=f"ข้อมูลที่รวบรวมได้ของ{series.measure} (หน่วย {series.unit}) — {record} "
                 "จากข้อมูลนี้ ข้อใดอธิบายสถานการณ์และผลกระทบการเปลี่ยนแปลงภูมิอากาศโลกได้ถูกต้อง",
            correct=_answer(series.situation, series.effect),
            wrongs=(_answer(_reversed_situation(series), series.effect),
                    _answer(series.situation, series.false_effect),
                    _answer(series.situation, "ไม่มีผลกระทบต่อสิ่งมีชีวิตและสิ่งแวดล้อม")),
            hint="ดูตัวเลขจากปีแรกไปปีล่าสุดว่าเพิ่มหรือลด แล้วเลือกผลกระทบที่เกิดจากการเปลี่ยนแปลงนั้นโดยตรง",
            topic=CLIMATE_TOPIC,
        )


@question_type(
    "geo.climate_change_application",
    display_name={"th": "วิเคราะห์การเปลี่ยนแปลงภูมิอากาศในประเทศไทย"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=CLIMATE_TOPIC,
)
class ClimateChangeApplication(QuestionType):
    """Who floods first, weather versus climate, and choosing climate data."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CLIMATE_SCENARIOS,
            hint="แยกลมฟ้าอากาศระยะสั้นออกจากแนวโน้มภูมิอากาศระยะยาว",
        ), CLIMATE_TOPIC)
