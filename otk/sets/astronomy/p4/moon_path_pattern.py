"""แบบรูปเส้นทางการขึ้นและตกของดวงจันทร์

ดาราศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.4/1

Sets moved here from: science_wave_c2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import PRIMARY_FOUR
from otk.sets._support.science_wave_c1 import EAST, SKY_TOPIC, SUBJECT, WEST
from otk.sets._support.science_wave_c2 import MOON_FACTS, MOON_SCENARIOS

PROVENANCE = Provenance("original")


# The four observing times of one night, and where the moon stood at each.
MOON_TIMES = ("19:00", "21:00", "23:00", "01:00")


MOON_WHERE = ("ทาง" + EAST + " เหนือขอบฟ้าเล็กน้อย",
              "ทาง" + EAST + " สูงขึ้นกว่าเดิม",
              "เกือบกลางท้องฟ้า",
              "ทาง" + WEST + " ต่ำลงใกล้ขอบฟ้า")


LATER = "ขึ้นช้ากว่าคืนก่อนหน้าประมาณครึ่งชั่วโมงถึงหนึ่งชั่วโมง"


EARLIER = "ขึ้นเร็วกว่าคืนก่อนหน้าประมาณครึ่งชั่วโมงถึงหนึ่งชั่วโมง"


SAME_TIME = "ขึ้นเวลาเดิมทุกคืน"


NO_PATTERN = "ขึ้นเร็วบ้างช้าบ้างโดยไม่มีแบบรูป"


def _moonrise_times(rng: Random) -> list[str]:
    """Four nights of moonrise times, each later than the night before.

    The moon rises later each night, so the times must increase; drawn per seed
    so the answer is a fact about this record rather than a remembered one.
    """
    minutes = rng.randrange(18 * 60, 19 * 60)
    times = []
    for _ in range(4):
        times.append(f"{minutes // 60:02d}:{minutes % 60:02d}")
        minutes += rng.randrange(35, 66)
    return times


def _moon_night_table() -> str:
    return " / ".join(f"{time} ดวงจันทร์อยู่{where}"
                      for time, where in zip(MOON_TIMES, MOON_WHERE))


def _moon_nights_table(times: list[str]) -> str:
    return " / ".join(f"คืนที่ {night} ดวงจันทร์ขึ้นทาง{EAST} เวลา {time} "
                      f"และตกทาง{WEST}"
                      for night, time in enumerate(times, start=1))


@question_type(
    "astro.moon_path_pattern_foundation",
    display_name={"th": "ทิศการขึ้นและตกของดวงจันทร์"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=SKY_TOPIC,
)
class MoonPathPatternFoundation(QuestionType):
    """Know that the moon, like the sun, comes up in the east and goes down west."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, MOON_FACTS,
            hint="นึกว่าโลกหมุนรอบตัวเอง สิ่งที่อยู่บนท้องฟ้าจึงปรากฏเคลื่อนไปทางเดียวกัน",
        ), SKY_TOPIC)


@question_type(
    "astro.moon_path_pattern_fluency",
    display_name={"th": "อ่านแบบรูปเส้นทางดวงจันทร์จากการสังเกต"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=SKY_TOPIC,
)
class MoonPathPatternFluency(QuestionType):
    """State the moon's path from a record of where and when it was seen.

    Two records are used: one night watched hour by hour, which gives the path
    across the sky, and four nights of moonrise, which gives the repeat. Both
    answers are read off the record printed in the stem.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem = ("นักเรียนสังเกตดวงจันทร์จากจุดเดิมในคืนเดียวกัน ได้ผลดังนี้ "
                    f"{_moon_night_table()} ")
            if rng.random() < 0.5:
                index = rng.choice([0, 1, 3])
                where = MOON_WHERE[index].removeprefix("ทาง")
                return _labelled(
                    stem=stem + f"จากข้อมูลนี้ ในเวลา {MOON_TIMES[index]} "
                                "ดวงจันทร์อยู่ที่ใด",
                    correct=where,
                    wrongs=tuple(other.removeprefix("ทาง")
                                 for other in MOON_WHERE if other != MOON_WHERE[index]),
                    hint="อ่านแถวของเวลาที่โจทย์ถามโดยตรง",
                    topic=SKY_TOPIC,
                )
            return _labelled(
                stem=stem + "จากข้อมูลนี้ ข้อใดสรุปเส้นทางของดวงจันทร์ในคืนนี้ได้ถูกต้อง",
                correct=f"ปรากฏขึ้นทาง{EAST} เคลื่อนข้ามท้องฟ้า แล้วต่ำลงทาง{WEST}",
                wrongs=(f"ปรากฏขึ้นทาง{WEST} เคลื่อนข้ามท้องฟ้า แล้วต่ำลงทาง{EAST}",
                        "อยู่ที่ตำแหน่งเดิมตลอดคืนโดยไม่เคลื่อนที่",
                        f"ปรากฏขึ้นทาง{EAST} แล้วย้อนกลับไปต่ำลงทาง{EAST}เช่นเดิม"),
                hint="ดูตำแหน่งของดวงจันทร์เรียงจากแถวแรกไปแถวสุดท้าย",
                topic=SKY_TOPIC,
            )
        times = _moonrise_times(rng)
        stem = ("นักเรียนบันทึกการขึ้นและตกของดวงจันทร์ติดต่อกันสี่คืน ได้ผลดังนี้ "
                f"{_moon_nights_table(times)} ")
        if rng.random() < 0.5:
            return _labelled(
                stem=stem + "จากข้อมูลนี้ เวลาที่ดวงจันทร์ขึ้นในแต่ละคืนเปลี่ยนแปลงอย่างไร",
                correct=LATER, wrongs=(EARLIER, SAME_TIME, NO_PATTERN),
                hint="เทียบเวลาขึ้นของคืนที่ 1 กับคืนถัด ๆ ไป",
                topic=SKY_TOPIC,
            )
        return _labelled(
            stem=stem + "จากข้อมูลนี้ ข้อใดคือแบบรูปที่ซ้ำเดิมทุกคืน",
            correct=f"ดวงจันทร์ขึ้นทาง{EAST}และตกทาง{WEST}ทุกคืน",
            wrongs=(f"ดวงจันทร์ขึ้นทาง{WEST}และตกทาง{EAST}ทุกคืน",
                    f"ดวงจันทร์ขึ้นทาง{EAST}และตกทาง{EAST}ด้วยทุกคืน",
                    "ดวงจันทร์ขึ้นเวลาเดิมทุกคืน"),
            hint="ดูว่าข้อความส่วนใดเหมือนกันในทั้งสี่คืน",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.moon_path_pattern_application",
    display_name={"th": "ใช้แบบรูปเส้นทางของดวงจันทร์"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=SKY_TOPIC,
)
class MoonPathPatternApplication(QuestionType):
    """Predict where the moon goes next, and judge a record that does not fit."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, MOON_SCENARIOS,
            hint="นึกว่าดวงจันทร์เคลื่อนจากทิศตะวันออกไปทิศตะวันตกเช่นเดียวกับดวงอาทิตย์",
        ), SKY_TOPIC)
