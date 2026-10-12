"""การใช้ประโยชน์จากคำพยากรณ์อากาศ

ธรณีวิทยา · ม.1 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.1/5

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
from otk.sets._support.science_wave_c18 import FORECAST_USE_SCENARIOS, FORECAST_VALUE_FACTS

PROVENANCE = Provenance("original")


FORECAST_USE_TOPIC = "การใช้ประโยชน์จากคำพยากรณ์อากาศ"


class Plan(NamedTuple):
    """A reader of a forecast, the forecast, how to act on it, and how to use it."""
    situation: str
    conduct: str
    use: str


# Conduct and use are both specific to the forecast, so another plan's half is
# always wrong for a case.
PLANS = (
    Plan("ชาวประมงพื้นบ้านฟังคำพยากรณ์ว่า “พรุ่งนี้คลื่นลมแรง คลื่นสูง 2 ถึง 3 เมตร”",
         "งดออกเรือและผูกเรือไว้ในที่ปลอดภัย",
         "ใช้วันนั้นซ่อมอวนและเครื่องมือประมงแทน"),
    Plan("เกษตรกรฟังคำพยากรณ์ว่า “อีกสามวันจะมีฝนตกหนักต่อเนื่องหลายวัน”",
         "งดฉีดพ่นปุ๋ยและยาในช่วงที่ฝนจะตก เพราะจะถูกฝนชะล้างไป",
         "รีบเก็บเกี่ยวผลผลิตที่พร้อมและขุดทางระบายน้ำในแปลงไว้ก่อน"),
    Plan("นักเรียนเห็นคำพยากรณ์ว่า “พรุ่งนี้อุณหภูมิสูงสุด 40 องศาเซลเซียส และค่าดัชนีรังสียูวีสูงมาก”",
         "หลีกเลี่ยงกิจกรรมกลางแดดช่วงเที่ยงถึงบ่าย ดื่มน้ำให้เพียงพอ และทาครีมกันแดด",
         "ย้ายการซ้อมกีฬาไปเป็นช่วงเช้าหรือเย็น"),
    Plan("ครอบครัวหนึ่งเห็นคำพยากรณ์ว่า “อากาศหนาวเย็นลง อุณหภูมิต่ำสุด 8 องศาเซลเซียส บนยอดดอย”",
         "เตรียมเสื้อผ้ากันหนาวให้เพียงพอ โดยเฉพาะสำหรับเด็กและผู้สูงอายุ",
         "วางแผนเที่ยวชมทะเลหมอกบนยอดดอยในช่วงที่อากาศหนาว"),
)


CONDUCT = "ปฏิบัติตน"


USE = "ใช้ประโยชน์"


# More halves for each forecast, used only as the borrowed half of a wrong choice.
# Each still fits its own forecast only.
MORE_FORECAST_LINES = {
    PLANS[0].situation: (("นำเรือเข้าจอดในที่กำบังคลื่นลมตั้งแต่เย็นวันนี้",),
                         ("นัดคนในครอบครัวช่วยกันคัดแยกปลาที่ตากไว้แทนการออกทะเล",)),
    PLANS[1].situation: (("ไม่ตากผลผลิตไว้กลางแจ้งในช่วงที่ฝนจะตก",),
                         ("เก็บน้ำฝนที่ตกหนักไว้ในบ่อสำหรับใช้ในฤดูแล้ง",)),
    PLANS[2].situation: (("สวมหมวกและเสื้อแขนยาวเมื่อต้องออกกลางแจ้ง",),
                         ("ตากผ้าและพืชผลให้แห้งเร็วในวันที่แดดจัด",)),
    PLANS[3].situation: (("ห่มผ้าให้อบอุ่นและระวังไม่ให้ร่างกายเปียกชื้นในคืนที่หนาว",),
                         ("ปลูกผักเมืองหนาวที่ชอบอากาศเย็นในช่วงนั้น",)),
}


def _conduct(rng: Random, plan) -> str:
    return rng.choice((plan.conduct, *MORE_FORECAST_LINES[plan.situation][0]))


def _use(rng: Random, plan) -> str:
    return rng.choice((plan.use, *MORE_FORECAST_LINES[plan.situation][1]))


def _plan(conduct: str, use: str) -> str:
    return f"{CONDUCT}โดย{conduct} และ{USE}โดย{use}"


@question_type(
    "geo.forecast_use_foundation",
    display_name={"th": "คุณค่าของคำพยากรณ์อากาศ"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=FORECAST_USE_TOPIC,
)
class ForecastUseFoundation(QuestionType):
    """Why forecasts matter, where to get them, and one half of a plan."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return _retopic(scenario_question(
                rng, FORECAST_VALUE_FACTS,
                hint="คำพยากรณ์บอกล่วงหน้า จึงช่วยให้เตรียมตัวได้ทัน",
            ), FORECAST_USE_TOPIC)
        plan = rng.choice(PLANS)
        others = [other for other in PLANS if other.situation != plan.situation]
        return _labelled(
            stem=f"{plan.situation} ควรปฏิบัติตนอย่างไรจึงเหมาะสมที่สุด",
            correct=plan.conduct,
            wrongs=tuple(other.conduct for other in others),
            hint="ตรวจว่าวิธีปฏิบัติตนตรงกับสภาพอากาศที่พยากรณ์ไว้หรือไม่",
            topic=FORECAST_USE_TOPIC,
        )


@question_type(
    "geo.forecast_use_fluency",
    display_name={"th": "เสนอแนวทางปฏิบัติตนและใช้ประโยชน์จากคำพยากรณ์อากาศ"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=FORECAST_USE_TOPIC,
)
class ForecastUseFluency(QuestionType):
    """Propose conduct and use for the forecast in the case; a wrong choice gets one half wrong."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        plan = rng.choice(PLANS)
        others = [other for other in PLANS if other.situation != plan.situation]
        rng.shuffle(others)
        return _labelled(
            stem=f"{plan.situation} ควรเสนอแนวทางใดในการปฏิบัติตนและใช้ประโยชน์จากคำพยากรณ์นี้",
            correct=_plan(plan.conduct, plan.use),
            wrongs=(_plan(_conduct(rng, others[0]), plan.use),
                    _plan(plan.conduct, _use(rng, others[1])),
                    _plan(_conduct(rng, others[2]), _use(rng, others[2])),
                    # Both halves wrong, crossed between two other forecasts.
                    _plan(_conduct(rng, others[1]), _use(rng, others[0])),
                    _plan(_conduct(rng, others[0]), _use(rng, others[2]))),
            hint="อ่านคำพยากรณ์ให้ชัดก่อน แล้วตรวจทั้งส่วนปฏิบัติตนและส่วนใช้ประโยชน์ว่าตรงกับคำพยากรณ์นั้น",
            topic=FORECAST_USE_TOPIC,
        )


@question_type(
    "geo.forecast_use_application",
    display_name={"th": "วางแผนโดยใช้คำพยากรณ์อากาศ"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=FORECAST_USE_TOPIC,
)
class ForecastUseApplication(QuestionType):
    """Plan an outdoor event, keep watching a calm sea, and answer "forecasts are wrong"."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, FORECAST_USE_SCENARIOS,
            hint="คำพยากรณ์มีค่าเมื่อใช้เตรียมตัวล่วงหน้าและติดตามอย่างต่อเนื่อง",
        ), FORECAST_USE_TOPIC)
