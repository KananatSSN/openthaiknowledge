"""องค์ประกอบของระบบสุริยะและคาบการโคจร

ดาราศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.4/3

Sets moved here from: science_wave_c4.
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
from otk.sets._support.science_wave_b17 import PRIMARY_FOUR
from otk.sets._support.science_wave_c1 import SKY_TOPIC, SUBJECT
from otk.sets._support.science_wave_c4 import ORBIT_SCENARIOS

PROVENANCE = Provenance("original")


class Planet(NamedTuple):
    """A planet, its place from the sun, and how long one orbit takes."""
    name: str
    order: int
    period: str
    days: float


# Periods as a model of the solar system would label them. ``days`` exists only
# so a test can check the table really does run longer with distance.
PLANETS = (
    Planet("ดาวพุธ", 1, "ประมาณ 88 วัน", 88),
    Planet("ดาวศุกร์", 2, "ประมาณ 225 วัน", 225),
    Planet("โลก", 3, "ประมาณ 365 วัน", 365),
    Planet("ดาวอังคาร", 4, "ประมาณ 687 วัน", 687),
    Planet("ดาวพฤหัสบดี", 5, "ประมาณ 12 ปี", 4333),
    Planet("ดาวเสาร์", 6, "ประมาณ 29 ปี", 10759),
    Planet("ดาวยูเรนัส", 7, "ประมาณ 84 ปี", 30687),
    Planet("ดาวเนปจูน", 8, "ประมาณ 165 ปี", 60190),
)


def _orbit_table() -> str:
    return " / ".join(f"{planet.name} (ลำดับที่ {planet.order} จากดวงอาทิตย์): "
                      f"คาบการโคจร{planet.period}" for planet in PLANETS)


FARTHER_LONGER = "ยิ่งอยู่ไกลจากดวงอาทิตย์ คาบการโคจรยิ่งยาวขึ้น"


FARTHER_SHORTER = "ยิ่งอยู่ไกลจากดวงอาทิตย์ คาบการโคจรยิ่งสั้นลง"


ALL_SAME = "ทุกดวงมีคาบการโคจรเท่ากัน"


NO_RULE = "คาบการโคจรไม่เกี่ยวกับระยะห่างจากดวงอาทิตย์"


@question_type(
    "astro.solar_system_periods_foundation",
    display_name={"th": "องค์ประกอบของระบบสุริยะ"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=SKY_TOPIC,
)
class SolarSystemPeriodsFoundation(QuestionType):
    """Know what the solar system holds and the order of its planets.

    The indicator's first half, ``สร้างแบบจำลองแสดงองค์ประกอบ``, is a model the
    learner builds, so nothing here claims it; this set supplies the knowledge
    the second half then compares.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        draw = rng.random()
        if draw < 0.4:
            planet = rng.choice(PLANETS)
            return _labelled(
                stem=f"“{planet.name}” เป็นดาวเคราะห์ลำดับที่เท่าใดจากดวงอาทิตย์",
                correct=f"ลำดับที่ {planet.order}",
                wrongs=tuple([f"ลำดับที่ {other.order}" for other in PLANETS
                                         if other.order != planet.order]),
                hint="ไล่ลำดับดาวเคราะห์จากดวงอาทิตย์ออกมา",
                topic=SKY_TOPIC,
            )
        if draw < 0.7:
            order = rng.randrange(1, len(PLANETS) + 1)
            planet = PLANETS[order - 1]
            return _labelled(
                stem=f"ดาวเคราะห์ลำดับที่ {order} จากดวงอาทิตย์คือดวงใด",
                correct=planet.name,
                wrongs=tuple([other.name for other in PLANETS
                                         if other.order != order]),
                hint="ไล่ลำดับดาวเคราะห์จากดวงอาทิตย์ออกมา",
                topic=SKY_TOPIC,
            )
        return _labelled(
            stem="ข้อใดกล่าวถึงองค์ประกอบของระบบสุริยะได้ถูกต้อง",
            correct="มีดวงอาทิตย์เป็นศูนย์กลาง และมีดาวเคราะห์ 8 ดวงโคจรอยู่รอบ ๆ "
                    "พร้อมทั้งดาวบริวาร ดาวเคราะห์แคระ และดาวเคราะห์น้อย",
            wrongs=("มีโลกเป็นศูนย์กลาง และมีดวงอาทิตย์กับดาวเคราะห์โคจรอยู่รอบ ๆ",
                    "มีดวงอาทิตย์เป็นศูนย์กลาง และมีดาวฤกษ์ดวงอื่นโคจรอยู่รอบ ๆ",
                    "มีดาวเคราะห์ 8 ดวงโคจรรอบกันเอง โดยไม่มีศูนย์กลาง"),
            hint="นึกว่าสิ่งใดอยู่ตรงกลาง และสิ่งใดโคจรอยู่รอบ ๆ",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.solar_system_periods_fluency",
    display_name={"th": "เปรียบเทียบคาบการโคจรของดาวเคราะห์"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=SKY_TOPIC,
)
class SolarSystemPeriodsFluency(QuestionType):
    """Compare orbital periods from the model's own table — the free verb.

    ``อธิบายเปรียบเทียบคาบการโคจร…จากแบบจำลอง`` carries an object of its own, and
    its verb is ``เปรียบเทียบ``, so this is the indicator's single ``exact`` set.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem = ("แบบจำลองระบบสุริยะแสดงคาบการโคจรของดาวเคราะห์ไว้ ดังนี้ "
                f"{_orbit_table()} ")
        draw = rng.random()
        if draw < 0.3:
            return _labelled(
                stem=stem + "จากแบบจำลองนี้ คาบการโคจรของดาวเคราะห์สัมพันธ์กับ"
                            "ระยะห่างจากดวงอาทิตย์อย่างไร",
                correct=FARTHER_LONGER,
                wrongs=(FARTHER_SHORTER, ALL_SAME, NO_RULE),
                hint="ไล่ดูคาบการโคจรจากดาวเคราะห์ลำดับที่ 1 ไปจนถึงลำดับสุดท้าย",
                topic=SKY_TOPIC,
            )
        pair = rng.sample(PLANETS, 2)
        longer = max(pair, key=lambda planet: planet.days)
        shorter = min(pair, key=lambda planet: planet.days)
        if draw < 0.65:
            return _labelled(
                stem=stem + f"จากแบบจำลองนี้ เมื่อเปรียบเทียบ “{pair[0].name}” "
                            f"กับ “{pair[1].name}” ข้อใดถูกต้อง",
                correct=f"{longer.name}มีคาบการโคจรยาวกว่า{shorter.name}",
                wrongs=(f"{shorter.name}มีคาบการโคจรยาวกว่า{longer.name}",
                        f"{pair[0].name}และ{pair[1].name}มีคาบการโคจรเท่ากัน",
                        f"{longer.name}โคจรรอบ{shorter.name}จึงเทียบคาบกันไม่ได้"),
                hint="อ่านคาบการโคจรของทั้งสองดวงจากตาราง แล้วเทียบกัน",
                topic=SKY_TOPIC,
            )
        planet = rng.choice(PLANETS)
        return _labelled(
            stem=stem + f"จากแบบจำลองนี้ “{planet.name}” มีคาบการโคจรเท่าใด",
            correct=planet.period,
            wrongs=tuple(other.period for other in PLANETS
                         if other.name != planet.name)[:3],
            hint="หาชื่อดาวเคราะห์ที่โจทย์ถาม แล้วอ่านคาบการโคจรที่เขียนไว้",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.solar_system_periods_application",
    display_name={"th": "วิเคราะห์คาบการโคจรและระบบสุริยะ"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=SKY_TOPIC,
)
class SolarSystemPeriodsApplication(QuestionType):
    """Reason from a period to a distance, and judge a model that flattens them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ORBIT_SCENARIOS,
            hint="นึกว่ายิ่งไกลจากดวงอาทิตย์ วงโคจรยิ่งยาวและใช้เวลายิ่งนาน",
        ), SKY_TOPIC)
