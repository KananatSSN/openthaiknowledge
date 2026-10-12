"""แบบรูปเส้นทางการขึ้นและตกของดวงอาทิตย์

ดาราศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.3/1

Sets moved here from: science_wave_c1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import PRIMARY_THREE, _retopic
from otk.sets._support.science_wave_c1 import (
    EAST,
    SKY_TOPIC,
    SUBJECT,
    SUN_PATH_FACTS,
    SUN_PATH_SCENARIOS,
    WEST,
)

PROVENANCE = Provenance("original")


COMPASS = (EAST, WEST, "ทิศเหนือ", "ทิศใต้")


# The five observation times, and where the sun stood at each. Noon is the one
# row with no left-or-right direction, which is what makes it the turning point.
SUN_TIMES = ("07:00", "09:00", "12:00", "15:00", "17:00")


SUN_WHERE = ("ทาง" + EAST, "ทาง" + EAST,
             "เหนือศีรษะพอดี (สูงที่สุดในวัน)",
             "ทาง" + WEST, "ทาง" + WEST)


SHORTENS = "สั้นลงเรื่อย ๆ"


LENGTHENS = "ยาวขึ้นเรื่อย ๆ"


UNCHANGED = "ยาวเท่าเดิมตลอด"


BOTH_WAYS = "ยาวขึ้นก่อนแล้วจึงสั้นลง"


def _shadow_lengths(rng: Random) -> list[int]:
    """Five distinct lengths for one real day, shortest at noon.

    A shadow is longest near sunrise and sunset and shortest at midday, so the
    two outer readings are drawn from a band well above the two mid-morning and
    mid-afternoon ones, which in turn sit well above noon. Without the bands an
    independent draw can put 07:00 below 09:00, and the record would then
    describe a day that never happens. The values inside each band are drawn
    afresh per seed, so which outer reading is the longest is still a fact about
    this table rather than something a learner can memorise.
    """
    noon = rng.randrange(15, 31)
    outer = rng.sample(range(noon * 5, noon * 7), 2)
    middle = rng.sample(range(noon * 2, noon * 3), 2)
    return [outer[0], middle[0], noon, middle[1], outer[1]]


def _sun_table(lengths: list[int]) -> str:
    return " / ".join(
        f"{time} ดวงอาทิตย์อยู่{where} ความยาวเงาของเสา {length} เซนติเมตร"
        for time, where, length in zip(SUN_TIMES, SUN_WHERE, lengths))


@question_type(
    "astro.sun_path_pattern_foundation",
    display_name={"th": "ทิศและเส้นทางของดวงอาทิตย์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=SKY_TOPIC,
)
class SunPathPatternFoundation(QuestionType):
    """Know east, west, noon and the shadow's direction before reading a table."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SUN_PATH_FACTS,
            hint="นึกภาพดวงอาทิตย์ตอนเช้า ตอนเที่ยง และตอนเย็น ว่าอยู่ทางใดและสูงเท่าใด",
        ), SKY_TOPIC)


@question_type(
    "astro.sun_path_pattern_fluency",
    display_name={"th": "อ่านแบบรูปเส้นทางดวงอาทิตย์จากการสังเกต"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=SKY_TOPIC,
)
class SunPathPatternFluency(QuestionType):
    """State the daily pattern from a record of the sun and a pole's shadow.

    Every answer is read off the table in the stem. The lengths are drawn afresh
    for each seed, so which time holds the longest shadow is a fact about this
    record and not something the learner can have memorised.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        lengths = _shadow_lengths(rng)
        stem = ("นักเรียนสังเกตดวงอาทิตย์และวัดความยาวเงาของเสาในวันเดียวกัน "
                f"ได้ผลดังนี้ {_sun_table(lengths)} ")
        draw = rng.random()
        if draw < 0.2:
            longest = SUN_TIMES[lengths.index(max(lengths))]
            return _labelled(
                stem=stem + "จากข้อมูลนี้ เงาของเสายาวที่สุดในเวลาใด",
                correct=longest,
                wrongs=tuple(time for time in SUN_TIMES if time != longest)[:3],
                hint="เปรียบเทียบตัวเลขความยาวเงาในแต่ละแถว",
                topic=SKY_TOPIC,
            )
        if draw < 0.4:
            shortest = SUN_TIMES[lengths.index(min(lengths))]
            return _labelled(
                stem=stem + "จากข้อมูลนี้ เงาของเสาสั้นที่สุดในเวลาใด",
                correct=shortest,
                wrongs=tuple(time for time in SUN_TIMES if time != shortest)[:3],
                hint="เปรียบเทียบตัวเลขความยาวเงาในแต่ละแถว",
                topic=SKY_TOPIC,
            )
        if draw < 0.6:
            index = rng.choice([0, 1, 3, 4])
            where = SUN_WHERE[index].removeprefix("ทาง")
            return _labelled(
                stem=stem + f"จากข้อมูลนี้ ในเวลา {SUN_TIMES[index]} "
                            "ดวงอาทิตย์อยู่ทางทิศใด",
                correct=where,
                wrongs=tuple(other for other in COMPASS if other != where),
                hint="อ่านแถวของเวลาที่โจทย์ถามโดยตรง",
                topic=SKY_TOPIC,
            )
        if draw < 0.8:
            morning = rng.random() < 0.5
            span = "07:00 ถึง 12:00" if morning else "12:00 ถึง 17:00"
            correct = SHORTENS if morning else LENGTHENS
            wrongs = tuple(other for other in (SHORTENS, LENGTHENS, UNCHANGED,
                                               BOTH_WAYS) if other != correct)
            return _labelled(
                stem=stem + f"จากข้อมูลนี้ ในช่วงเวลา {span} "
                            "ความยาวเงาของเสาเปลี่ยนแปลงอย่างไร",
                correct=correct, wrongs=wrongs,
                hint="ดูตัวเลขความยาวเงาเรียงตามเวลาในช่วงที่โจทย์ถาม",
                topic=SKY_TOPIC,
            )
        return _labelled(
            stem=stem + "จากข้อมูลนี้ ข้อใดสรุปแบบรูปเส้นทางของดวงอาทิตย์ในวันนี้ได้ถูกต้อง",
            correct=f"ดวงอาทิตย์อยู่ทาง{EAST}ในตอนเช้า สูงที่สุดราวเที่ยงวัน "
                    f"แล้วอยู่ทาง{WEST}ในตอนเย็น",
            wrongs=(f"ดวงอาทิตย์อยู่ทาง{WEST}ในตอนเช้า แล้วอยู่ทาง{EAST}ในตอนเย็น",
                    "ดวงอาทิตย์อยู่เหนือศีรษะตลอดทั้งวันโดยไม่เปลี่ยนตำแหน่ง",
                    f"ดวงอาทิตย์อยู่ทาง{EAST}ตลอดทั้งวัน แล้วจึงตกลงที่เดิม"),
            hint="ดูคอลัมน์ทิศของดวงอาทิตย์เรียงจากแถวแรกไปแถวสุดท้าย",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.sun_path_pattern_application",
    display_name={"th": "ใช้แบบรูปของดวงอาทิตย์บอกทิศและเวลา"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=SKY_TOPIC,
)
class SunPathPatternApplication(QuestionType):
    """Use the daily pattern to place a window, a shadow, or a way of checking it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SUN_PATH_SCENARIOS,
            hint="นึกว่าดวงอาทิตย์อยู่ทางใดในเวลานั้น แล้วเงาจะทอดไปด้านตรงข้ามเสมอ",
        ), SKY_TOPIC)
