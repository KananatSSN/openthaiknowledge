"""ตำแหน่งและเส้นทางของกลุ่มดาวฤกษ์ในรอบปี

ดาราศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.5/2

Sets moved here from: science_wave_c3.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b24 import PRIMARY_FIVE
from otk.sets._support.science_wave_c1 import EAST, SKY_TOPIC, SUBJECT, WEST
from otk.sets._support.science_wave_c3 import STAR_MAP_SCENARIOS

PROVENANCE = Provenance("original")


# A star map reading for one evening: where the map puts each group, and the
# path it gives. All four rise in the east and set in the west, because every
# star group does; what the map adds is where each one stands right now.
CHART_TIME = "20:00 น."


CHART = (
    ("กลุ่มดาวนายพราน", "ทางทิศตะวันออก สูงจากขอบฟ้าประมาณ 20 องศา"),
    ("กลุ่มดาวคนคู่", "ทางทิศตะวันออกเฉียงเหนือ ใกล้ขอบฟ้า"),
    ("กลุ่มดาวลูกไก่", "เกือบกลางท้องฟ้า"),
    ("กลุ่มดาวนกอินทรี", "ทางทิศตะวันตก ใกล้จะลับขอบฟ้า"),
)


def _chart() -> str:
    return " / ".join(f"{group}: {where}" for group, where in CHART)


# The same group, seen at the same clock time in different months. At a fixed
# hour a star group stands about a month's worth further west each time, until
# it is lost in the evening twilight and returns a year later.
YEAR_GROUP = "กลุ่มดาวนายพราน"


YEAR_CHART = (
    ("ธันวาคม", "ทางทิศตะวันออก ใกล้ขอบฟ้า"),
    ("มกราคม", "ทางทิศตะวันออก สูงขึ้นจากขอบฟ้า"),
    ("กุมภาพันธ์", "เกือบกลางท้องฟ้า"),
    ("มีนาคม", "ทางทิศตะวันตก เยื้องจากกลางท้องฟ้า"),
    ("เมษายน", "ทางทิศตะวันตก ใกล้ขอบฟ้า"),
)


WESTWARD = "ค่อย ๆ เลื่อนจากทางทิศตะวันออกไปทางทิศตะวันตกเมื่อเดือนผ่านไป"


EASTWARD = "ค่อย ๆ เลื่อนจากทางทิศตะวันตกไปทางทิศตะวันออกเมื่อเดือนผ่านไป"


FIXED = "อยู่ที่ตำแหน่งเดิมทุกเดือน"


RANDOM_MOVE = "เลื่อนไปมาโดยไม่มีแบบรูปที่แน่นอน"


def _year_chart() -> str:
    return " / ".join(f"{month}: {where}" for month, where in YEAR_CHART)


# Positions no group on the printed chart occupies.
CHART_DECOYS = ("ทางทิศใต้ ใกล้ขอบฟ้า", "ทางทิศเหนือ สูงจากขอบฟ้าประมาณ 60 องศา")


YEAR_DECOYS = ("เลื่อนขึ้นลงในแนวดิ่งโดยไม่เลื่อนไปทางทิศใด",
               "เลื่อนไปทางทิศเหนือทีละน้อยเมื่อเดือนผ่านไป")


@question_type(
    "astro.star_map_foundation",
    display_name={"th": "ใช้แผนที่ดาวระบุตำแหน่งกลุ่มดาวฤกษ์"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=SKY_TOPIC,
)
class StarMapFoundation(QuestionType):
    """Read a star map for position and path — the indicator's first free verb.

    ``ใช้แผนที่ดาวระบุตำแหน่งและเส้นทาง`` and ``อธิบายแบบรูป…ในรอบปี`` are joined by
    ``และ`` and carry objects of their own, so each earns an ``exact`` set. This
    one answers from the chart printed in the stem.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem = (f"แผนที่ดาวสำหรับคืนหนึ่ง เวลา {CHART_TIME} แสดงตำแหน่งของกลุ่มดาว "
                f"ดังนี้ {_chart()} ")
        draw = rng.random()
        if draw < 0.4:
            group, where = rng.choice(CHART)
            return _labelled(
                stem=stem + f"จากแผนที่ดาวนี้ “{group}” อยู่ที่ตำแหน่งใด",
                correct=where,
                wrongs=tuple([other for name, other in CHART if name != group]
                                        + list(CHART_DECOYS)),
                hint="หาชื่อกลุ่มดาวที่โจทย์ถาม แล้วอ่านตำแหน่งที่เขียนไว้ข้างชื่อนั้น",
                topic=SKY_TOPIC,
            )
        if draw < 0.7:
            group = CHART[3][0]
            return _labelled(
                stem=stem + "จากแผนที่ดาวนี้ กลุ่มดาวใดกำลังจะตกลับขอบฟ้าเป็นกลุ่มแรก",
                correct=group,
                wrongs=tuple(name for name, _ in CHART if name != group),
                hint=f"กลุ่มดาวตกทาง{WEST} จึงหากลุ่มที่แผนที่วางไว้ใกล้ขอบฟ้าด้านนั้น",
                topic=SKY_TOPIC,
            )
        group = CHART[0][0]
        return _labelled(
            stem=stem + f"จากแผนที่ดาวนี้ เส้นทางการขึ้นและตกของ “{group}” "
                        "ในคืนนี้เป็นอย่างไร",
            correct=f"ขึ้นทาง{EAST} เคลื่อนข้ามท้องฟ้า แล้วตกทาง{WEST}",
            wrongs=(f"ขึ้นทาง{WEST} เคลื่อนข้ามท้องฟ้า แล้วตกทาง{EAST}",
                    "อยู่ที่ตำแหน่งเดิมตลอดคืนโดยไม่เคลื่อนที่",
                    f"ขึ้นทาง{EAST} แล้วย้อนกลับไปตกทาง{EAST}เช่นเดิม"),
            hint="กลุ่มดาวเคลื่อนข้ามท้องฟ้าไปทางเดียวกับดวงอาทิตย์และดวงจันทร์",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.star_map_fluency",
    display_name={"th": "แบบรูปเส้นทางกลุ่มดาวฤกษ์ในรอบปี"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=SKY_TOPIC,
)
class StarMapFluency(QuestionType):
    """Give the yearly pattern from a record of the same hour in five months.

    This is the indicator's second free verb, ``อธิบายแบบรูป…ในรอบปี``, so it is
    the second ``exact`` set. The answer is read off the record in the stem.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem = (f"นักเรียนใช้แผนที่ดาวดูตำแหน่งของ “{YEAR_GROUP}” ที่เวลา {CHART_TIME} "
                f"ของทุกเดือน ได้ผลดังนี้ {_year_chart()} ")
        draw = rng.random()
        if draw < 0.35:
            return _labelled(
                stem=stem + "จากข้อมูลนี้ ตำแหน่งของกลุ่มดาวนี้ในเวลาเดิมของแต่ละเดือน"
                            "เปลี่ยนแปลงอย่างไร",
                correct=WESTWARD,
                wrongs=tuple((EASTWARD, FIXED, RANDOM_MOVE, *YEAR_DECOYS)),
                hint="อ่านตำแหน่งของเดือนแรกแล้วไล่ไปจนถึงเดือนสุดท้าย",
                topic=SKY_TOPIC,
            )
        if draw < 0.7:
            month, where = rng.choice(YEAR_CHART)
            return _labelled(
                stem=stem + f"จากข้อมูลนี้ ในเดือน{month} เวลา {CHART_TIME} "
                            "กลุ่มดาวนี้อยู่ที่ตำแหน่งใด",
                correct=where,
                wrongs=tuple([other for name, other in YEAR_CHART if name != month]),
                hint="หาแถวของเดือนที่โจทย์ถามโดยตรง",
                topic=SKY_TOPIC,
            )
        return _labelled(
            stem=stem + "จากข้อมูลนี้ ถ้าสังเกตต่อไปเรื่อย ๆ ข้อใดน่าจะเกิดขึ้น",
            correct="กลุ่มดาวนี้จะลับขอบฟ้าทางทิศตะวันตกไปในที่สุด "
                    "แล้วกลับมาปรากฏที่ตำแหน่งเดิมอีกครั้งเมื่อครบหนึ่งปี",
            wrongs=tuple((
                "กลุ่มดาวนี้จะหยุดอยู่ทางทิศตะวันตกและไม่เปลี่ยนตำแหน่งอีก",
                "กลุ่มดาวนี้จะย้อนกลับไปทางทิศตะวันออกในเดือนถัดไป",
                "กลุ่มดาวนี้จะหายไปอย่างถาวรและไม่กลับมาอีก",
                "กลุ่มดาวนี้จะเลื่อนขึ้นไปอยู่เหนือศีรษะและค้างอยู่ตรงนั้นตลอดปี",
                "กลุ่มดาวนี้จะกลายเป็นกลุ่มดาวอื่นเมื่อครบหกเดือน",
            )),
            hint="ทิศทางการเลื่อนในตารางบอกว่ากลุ่มดาวกำลังมุ่งไปทางใด",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.star_map_application",
    display_name={"th": "ใช้แผนที่ดาวและแบบรูปในรอบปี"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=SKY_TOPIC,
)
class StarMapApplication(QuestionType):
    """Predict where a group will be, and judge how a map should be used."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, STAR_MAP_SCENARIOS,
            hint="ถามว่าแผนที่ตรงกับเดือนและเวลาหรือไม่ และกลุ่มดาวเลื่อนไปทางใด",
        ), SKY_TOPIC)
