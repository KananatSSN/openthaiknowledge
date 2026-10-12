"""วิวัฒนาการของดาวฤกษ์

ดาราศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.6/7

Sets moved here from: science_wave_c8.
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
from otk.sets._support.science_wave_c1 import SUBJECT
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c8 import EVOLUTION_SCENARIOS

PROVENANCE = Provenance("original")


EVOLUTION_TOPIC = "วิวัฒนาการของดาวฤกษ์"


class Track(NamedTuple):
    """One initial-mass band, the road it takes, and what it leaves behind."""
    mass: str
    path: str
    remnant: str
    lifetime: str


# The bands do not overlap, so an initial mass picks exactly one row.
TRACKS = (
    Track("น้อยกว่าประมาณ 0.5 เท่าของมวลดวงอาทิตย์",
          "อยู่ในแถบลำดับหลักนานมากโดยไม่พองตัวเป็นดาวยักษ์แดง",
          "ดาวแคระขาวที่มีฮีเลียมเป็นองค์ประกอบ",
          "นานกว่าอายุของเอกภพในปัจจุบัน"),
    Track("ประมาณ 0.5 ถึง 8 เท่าของมวลดวงอาทิตย์",
          "ออกจากแถบลำดับหลักไปเป็นดาวยักษ์แดง แล้วสลัดชั้นนอกออกเป็นเนบิวลาดาวเคราะห์",
          "ดาวแคระขาวที่มีคาร์บอนและออกซิเจนเป็นองค์ประกอบ",
          "ประมาณหนึ่งหมื่นล้านปี"),
    Track("ประมาณ 8 ถึง 20 เท่าของมวลดวงอาทิตย์",
          "พองตัวเป็นดาวยักษ์ใหญ่แดง แล้วระเบิดเป็นซูเปอร์โนวา",
          "ดาวนิวตรอน",
          "ประมาณสิบถึงร้อยล้านปี"),
    Track("มากกว่าประมาณ 20 เท่าของมวลดวงอาทิตย์",
          "พองตัวเป็นดาวยักษ์ใหญ่แดง แล้วระเบิดเป็นซูเปอร์โนวาและยุบตัวต่อไปไม่หยุด",
          "หลุมดำ",
          "ประมาณไม่กี่ล้านปี"),
)


class Change(NamedTuple):
    """A property of a star, and which way it moves at a step of its life."""
    step: str
    radius: str
    surface: str
    luminosity: str


CHANGES = (
    Change("เมื่อดาวฤกษ์คล้ายดวงอาทิตย์ออกจากแถบลำดับหลักไปเป็นดาวยักษ์แดง",
           "ใหญ่ขึ้นมาก", "ต่ำลง", "สูงขึ้นมาก"),
    Change("เมื่อดาวยักษ์แดงสลัดชั้นนอกออกแล้วเหลือแก่นเป็นดาวแคระขาว",
           "เล็กลงมาก", "สูงขึ้น", "ลดลงมาก"),
    Change("ขณะที่ดาวฤกษ์อยู่ในแถบลำดับหลักเป็นเวลานาน",
           "เกือบคงที่", "เกือบคงที่", "เกือบคงที่"),
)


RADIUS = "รัศมี"


SURFACE = "อุณหภูมิผิว"


LUMINOSITY = "ความส่องสว่าง"


def _properties(item: Change) -> str:
    return (f"{RADIUS}{item.radius} {SURFACE}{item.surface} "
            f"และ{LUMINOSITY}{item.luminosity}")


# Paths, remnants and masses no initial-mass band leads to.
PATH_DECOYS = ("ค่อย ๆ หดตัวลงจนกลายเป็นดาวเคราะห์แก๊ส",
               "กลายเป็นดาวหางแล้วโคจรออกจากกาแล็กซีไป")


REMNANT_DECOYS = ("ดาวเคราะห์แก๊สขนาดใหญ่", "เนบิวลาที่พร้อมยุบตัวเป็นดาวฤกษ์ดวงใหม่ทันที")


MASS_DECOYS = ("เท่ากับมวลของโลกพอดี", "น้อยกว่ามวลของดาวพฤหัสบดี")


def _property_wrongs(item, others) -> list[str]:
    """Whole wrong steps, or one property borrowed from another step."""
    wrongs = [_properties(other) for other in others]
    wrongs += [f"{RADIUS}{other.radius} {SURFACE}{item.surface} และ{LUMINOSITY}{item.luminosity}"
               for other in others if other.radius != item.radius]
    wrongs += [f"{RADIUS}{item.radius} {SURFACE}{other.surface} และ{LUMINOSITY}{item.luminosity}"
               for other in others if other.surface != item.surface]
    if item.luminosity != "เกือบคงที่":
        wrongs.append(f"{RADIUS}{item.radius} {SURFACE}{item.surface} แต่{LUMINOSITY}คงที่")
    return [text for text in dict.fromkeys(wrongs) if text != _properties(item)]


@question_type(
    "astro.stellar_evolution_foundation",
    display_name={"th": "ลำดับวิวัฒนาการตามมวลตั้งต้น"},
    level=UPPER_SIX, subject=SUBJECT, topic=EVOLUTION_TOPIC,
)
class StellarEvolutionFoundation(QuestionType):
    """Give the road a star takes from its initial mass — the first free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(TRACKS)
        others = [other for other in TRACKS if other.mass != item.mass]
        rng.shuffle(others)
        draw = rng.random()
        if draw < 0.35:
            return _labelled(
                stem=f"ดาวฤกษ์ที่มีมวลตั้งต้น{item.mass} จะมีลำดับวิวัฒนาการอย่างไร",
                correct=item.path,
                wrongs=tuple([other.path for other in others[:3]] + list(PATH_DECOYS)),
                hint="ยิ่งมวลตั้งต้นมาก ยิ่งพองตัวใหญ่และจบชีวิตอย่างรุนแรงกว่า",
                topic=EVOLUTION_TOPIC,
            )
        if draw < 0.7:
            return _labelled(
                stem=f"ดาวฤกษ์ที่มีมวลตั้งต้น{item.mass} จะเหลืออะไรไว้เมื่อสิ้นอายุขัย",
                correct=item.remnant,
                wrongs=tuple([other.remnant for other in others[:3]] + list(REMNANT_DECOYS)),
                hint="มวลตั้งต้นเป็นตัวกำหนดว่าแก่นที่เหลือจะยุบลงไปได้ไกลเพียงใด",
                topic=EVOLUTION_TOPIC,
            )
        return _labelled(
            stem=f"ดาวฤกษ์ที่เหลือ “{item.remnant}” ไว้เมื่อสิ้นอายุขัย "
                 "มีมวลตั้งต้นประมาณเท่าใด",
            correct=item.mass,
            wrongs=tuple([other.mass for other in others[:3]] + list(MASS_DECOYS)),
            hint="ย้อนจากซากที่เหลือกลับไปหาช่วงมวลที่ทำให้เกิดซากแบบนั้น",
            topic=EVOLUTION_TOPIC,
        )


@question_type(
    "astro.stellar_evolution_fluency",
    display_name={"th": "วิเคราะห์การเปลี่ยนแปลงสมบัติของดาวฤกษ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=EVOLUTION_TOPIC,
)
class StellarEvolutionFluency(QuestionType):
    """Say which way each property moves — the indicator's second free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CHANGES)
        others = [other for other in CHANGES if other.step != item.step]
        if rng.random() < 0.6:
            return _labelled(
                stem=f"{item.step} สมบัติของดาวฤกษ์เปลี่ยนแปลงอย่างไร",
                correct=_properties(item),
                wrongs=tuple(_property_wrongs(item, others)),
                hint="ตอบให้ครบทั้งสามสมบัติ แล้วตรวจทิศทางของแต่ละอย่าง",
                topic=EVOLUTION_TOPIC,
            )
        return _labelled(
            stem="ดาวยักษ์แดงมีอุณหภูมิผิวต่ำกว่าดวงอาทิตย์ "
                 "แต่กลับส่องสว่างกว่ามาก ข้อใดอธิบายได้ถูกต้อง",
            correct="รัศมีที่ใหญ่ขึ้นมากทำให้พื้นที่ผิวเพิ่มขึ้นจนชดเชยอุณหภูมิที่ต่ำลงได้เกินพอ",
            wrongs=tuple((
                "อุณหภูมิผิวที่ต่ำลงเป็นสาเหตุโดยตรงที่ทำให้ส่องสว่างมากขึ้น",
                "ดาวยักษ์แดงอยู่ใกล้โลกกว่าดวงอาทิตย์จึงดูสว่างกว่า",
                "ความส่องสว่างไม่เกี่ยวกับรัศมีและอุณหภูมิผิวของดาวฤกษ์",
                "รัศมีที่เล็กลงทำให้พลังงานรวมอยู่ในพื้นที่แคบจึงสว่างกว่า",
                "ดาวยักษ์แดงมีอุณหภูมิผิวสูงกว่าดวงอาทิตย์จริง ๆ แต่ดูเป็นสีแดงเพราะฝุ่น",
            )),
            hint="ความส่องสว่างขึ้นกับทั้งพื้นที่ผิวและอุณหภูมิผิว",
            topic=EVOLUTION_TOPIC,
        )


@question_type(
    "astro.stellar_evolution_application",
    display_name={"th": "วิเคราะห์ชะตากรรมของดาวฤกษ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=EVOLUTION_TOPIC,
)
class StellarEvolutionApplication(QuestionType):
    """Trace a remnant back to a mass, and place a star on its road."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, EVOLUTION_SCENARIOS,
            hint="มวลตั้งต้นเป็นตัวกำหนดทั้งอายุขัยและซากที่เหลือไว้",
        ), EVOLUTION_TOPIC)
