"""สาเหตุที่มองไม่เห็นดาวส่วนใหญ่ในเวลากลางวัน

ดาราศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.1/2

Sets moved here from: science_wave_c1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import PRIMARY_ONE, _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c1 import (
    DAYTIME_FACTS,
    DAYTIME_SCENARIOS,
    DEMOS,
    SKY_TOPIC,
    SUBJECT,
)

PROVENANCE = Provenance("original")


@question_type(
    "astro.daytime_stars_foundation",
    display_name={"th": "ดาวในเวลากลางวัน"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=SKY_TOPIC,
)
class DaytimeStarsFoundation(QuestionType):
    """Know that the stars stay put and that sunlight is what hides them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, DAYTIME_FACTS,
            hint="นึกว่าแสงที่สว่างกว่ากลบแสงที่สลัวกว่าได้อย่างไร",
        ), SKY_TOPIC)


@question_type(
    "astro.daytime_stars_fluency",
    display_name={"th": "อธิบายสาเหตุจากหลักฐานเชิงประจักษ์"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=SKY_TOPIC,
)
class DaytimeStarsFluency(QuestionType):
    """Read a demonstration and give the cause it shows — the indicator's evidence."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DEMOS)
        return _labelled(
            stem=f"{item.setup} ผลที่สังเกตได้คือ {item.seen} "
                 "จากหลักฐานนี้ ข้อใดอธิบายได้เหมาะสมที่สุด "
                 "และช่วยให้เข้าใจว่าเหตุใดกลางวันจึงมองไม่เห็นดาวส่วนใหญ่",
            correct=item.conclusion, wrongs=tuple(item.wrongs),
            hint="อ่านว่าสิ่งที่เปลี่ยนไปในการทดลองคือความสว่างรอบข้าง ไม่ใช่ตัวแหล่งกำเนิดแสง",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.daytime_stars_application",
    display_name={"th": "ใช้เหตุผลเรื่องความสว่างของท้องฟ้า"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=SKY_TOPIC,
)
class DaytimeStarsApplication(QuestionType):
    """Carry the cause into eclipses, moonlight, and a proposed way of looking."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, DAYTIME_SCENARIOS,
            hint="ถามว่าความสว่างของท้องฟ้าเปลี่ยนไปหรือไม่ และดาวยังอยู่ที่เดิมหรือเปล่า",
        ), SKY_TOPIC)
