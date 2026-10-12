"""แหล่งน้ำผิวดินและแหล่งน้ำใต้ดิน

ธรณีวิทยา · ม.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.2/8

Sets moved here from: science_wave_c21.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b8 import LEVEL as MIDDLE_TWO
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c21 import SOURCE_FACTS, SOURCE_SCENARIOS

PROVENANCE = Provenance("original")


WATER_SOURCE_TOPIC = "แหล่งน้ำผิวดินและแหล่งน้ำใต้ดิน"


WATER_MODEL = ("แบบจำลอง: ตู้กระจกใส่ชั้นกรวดและทรายทับบนชั้นดินเหนียว ปั้นพื้นผิวด้านบนให้มีแอ่ง "
               "แล้วรดน้ำลงไปเหมือนฝนตก")


SURFACE = "แหล่งน้ำผิวดิน"


GROUND = "แหล่งน้ำใต้ดิน"


SURFACE_TRUE = ("น้ำฝนส่วนที่ซึมลงดินไม่ทันไหลไปตามผิวดินลงสู่ที่ต่ำ "
                "แล้วขังอยู่ในแอ่งเป็นแหล่งน้ำผิวดิน ซึ่งเกิดได้มากเมื่อฝนตกหนักและพื้นที่เป็นแอ่ง")


GROUND_TRUE = ("น้ำฝนอีกส่วนซึมผ่านชั้นกรวดและทรายที่มีช่องว่างมาก "
               "แล้วถูกกักไว้เหนือชั้นดินเหนียวที่น้ำซึมผ่านยาก เป็นแหล่งน้ำใต้ดิน")


SURFACE_FALSE = ("น้ำฝนทั้งหมดซึมลงไปใต้ดินก่อน แล้วจึงดันขึ้นมาเป็นแหล่งน้ำผิวดิน "
                 "ซึ่งเกิดได้มากในพื้นที่สูงชันที่ไม่มีแอ่ง")


GROUND_FALSE = ("น้ำฝนซึมผ่านชั้นดินเหนียวได้ง่ายที่สุด "
                "แล้วถูกกักไว้ในชั้นกรวดและทรายด้านล่าง เป็นแหล่งน้ำใต้ดิน")


SURFACE_FALSES = (
    SURFACE_FALSE,
    "น้ำในแอ่งด้านบนเกิดจากไอน้ำในอากาศควบแน่นลงในแอ่งโดยตรง ไม่เกี่ยวกับน้ำฝนที่ไหลมา",
    "น้ำฝนไหลออกจากแอ่งไปยังที่สูงทั้งหมด แอ่งจึงมีน้ำขังได้เฉพาะเมื่อฝนหยุดตกนานหลายวัน",
)


GROUND_FALSES = (
    GROUND_FALSE,
    "น้ำใต้ดินเกิดจากน้ำทะเลที่ซึมเข้ามาใต้แผ่นดิน ไม่เกี่ยวกับน้ำฝนที่ซึมลงไป",
    "น้ำฝนซึมผ่านทุกชั้นลงไปจนถึงแก่นโลก จึงไม่มีชั้นใดกักน้ำไว้ได้",
)


def _sources(surface: str, ground: str) -> str:
    return f"{SURFACE}: {surface} / {GROUND}: {ground}"


@question_type(
    "geo.water_source_foundation",
    display_name={"th": "แหล่งน้ำผิวดินและแหล่งน้ำใต้ดิน"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=WATER_SOURCE_TOPIC,
)
class WaterSourceFoundation(QuestionType):
    """Know the sources and the factors one at a time, without the model."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SOURCE_FACTS,
            hint="น้ำที่ไหลบนผิวดินรวมเป็นแหล่งน้ำผิวดิน น้ำที่ซึมลงไปถูกกักไว้เป็นแหล่งน้ำใต้ดิน",
        ), WATER_SOURCE_TOPIC)


@question_type(
    "geo.water_source_fluency",
    display_name={"th": "อธิบายการเกิดแหล่งน้ำผิวดินและแหล่งน้ำใต้ดินจากแบบจำลอง"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=WATER_SOURCE_TOPIC,
)
class WaterSourceFluency(QuestionType):
    """Explain both sources from the model together; each wrong choice gets one wrong."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _labelled(
            stem=f"{WATER_MODEL} พบว่ามีน้ำขังในแอ่งด้านบน และมีน้ำสะสมอยู่เหนือชั้นดินเหนียว "
                 "ข้อใดอธิบายปัจจัยและกระบวนการเกิดแหล่งน้ำผิวดินและแหล่งน้ำใต้ดินจากแบบจำลองนี้ได้ถูกต้อง",
            correct=_sources(SURFACE_TRUE, GROUND_TRUE),
            # Each wrong gets at least one half wrong, drawn from several misreadings.
            wrongs=tuple([_sources(surface, GROUND_TRUE) for surface in SURFACE_FALSES]
                + [_sources(SURFACE_TRUE, ground) for ground in GROUND_FALSES]
                + [_sources(surface, ground) for surface in SURFACE_FALSES for ground in GROUND_FALSES]),
            hint="ตรวจทั้งสองส่วน: น้ำขังในแอ่งมาจากทางใด และน้ำใต้ดินถูกกักไว้เหนือชั้นใด",
            topic=WATER_SOURCE_TOPIC,
        )


@question_type(
    "geo.water_source_application",
    display_name={"th": "วิเคราะห์แหล่งน้ำผิวดินและน้ำใต้ดินในชีวิตจริง"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=WATER_SOURCE_TOPIC,
)
class WaterSourceApplication(QuestionType):
    """Land subsidence, sealed cities, and recharging groundwater."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SOURCE_SCENARIOS,
            hint="นึกว่าน้ำฝนไหลบนผิวดินหรือซึมลงดินได้มากน้อยเพียงใด",
        ), WATER_SOURCE_TOPIC)
