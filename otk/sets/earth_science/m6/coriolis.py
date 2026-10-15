"""ทิศทางลมกับการหมุนรอบตัวเองของโลก

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/9

Sets moved here from: science_wave_c24.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c24 import CORIOLIS_SCENARIOS

PROVENANCE = Provenance("original")


CORIOLIS_TOPIC = "ทิศทางลมกับการหมุนรอบตัวเองของโลก"


NORTH, SOUTH = "ซีกโลกเหนือ", "ซีกโลกใต้"


SIDE = {NORTH: "ขวา", SOUTH: "ซ้าย"}


HEADINGS = ("ทิศเหนือ", "ทิศใต้", "ทิศตะวันออก", "ทิศตะวันตก")


# Where air moving along each heading ends up after turning right or left.
TURN = {
    ("ทิศเหนือ", "ขวา"): "ทิศตะวันออกเฉียงเหนือ", ("ทิศเหนือ", "ซ้าย"): "ทิศตะวันตกเฉียงเหนือ",
    ("ทิศใต้", "ขวา"): "ทิศตะวันตกเฉียงใต้", ("ทิศใต้", "ซ้าย"): "ทิศตะวันออกเฉียงใต้",
    ("ทิศตะวันออก", "ขวา"): "ทิศตะวันออกเฉียงใต้", ("ทิศตะวันออก", "ซ้าย"): "ทิศตะวันออกเฉียงเหนือ",
    ("ทิศตะวันตก", "ขวา"): "ทิศตะวันตกเฉียงเหนือ", ("ทิศตะวันตก", "ซ้าย"): "ทิศตะวันตกเฉียงใต้",
}


ROTATION = "เพราะโลกหมุนรอบตัวเองจากทิศตะวันตกไปทิศตะวันออก"


# Air spiralling into a low turns this way, seen from above.
CYCLONE = {NORTH: "ทวนเข็มนาฬิกา", SOUTH: "ตามเข็มนาฬิกา"}


# Things that travel far enough through the air for the turn to show.
MOVERS = (
    "อากาศที่เคลื่อนที่เป็นระยะทางไกล",
    "ลมที่พัดเป็นระยะทางไกล",
    "ลมค้าที่พัดจากละติจูดประมาณ 30 องศาเข้าหาเส้นศูนย์สูตร",
    "อากาศที่ไหลออกจากเขตความกดอากาศสูงไปเป็นระยะทางหลายร้อยกิโลเมตร",
    "ลมที่พัดจากขั้วโลกลงมายังละติจูดกลาง",
    "ลูกโป่งตรวจอากาศที่ลอยไปตามลมเป็นระยะทางไกล",
)

def turned(hemisphere: str, heading: str) -> str:
    return TURN[(heading, SIDE[hemisphere])]


@question_type(
    "geo.coriolis_foundation",
    display_name={"th": "ระบุทิศการเบนของอากาศในแต่ละซีกโลก"},
    level=UPPER_SIX, subject=SUBJECT, topic=CORIOLIS_TOPIC,
)
class CoriolisFoundation(QuestionType):
    """Which way air turns, or which way a low spins, in one hemisphere."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hemisphere = rng.choice((NORTH, SOUTH))
        other = SOUTH if hemisphere == NORTH else NORTH
        if rng.random() < 0.5:
            mover = rng.choice(MOVERS)
            return _labelled(
                stem=f"{mover}ใน{hemisphere}เบนไปทางใด",
                correct=f"เบนไปทาง{SIDE[hemisphere]}ของทิศที่เคลื่อนที่ {ROTATION}",
                wrongs=(f"เบนไปทาง{SIDE[other]}ของทิศที่เคลื่อนที่ {ROTATION}",
                        *rng.sample((
                            "เคลื่อนที่ตรงไม่เบน เพราะการหมุนรอบตัวเองของโลกไม่มีผลต่ออากาศ",
                            f"เบนไปทาง{SIDE[hemisphere]}ของทิศที่เคลื่อนที่ เพราะดวงอาทิตย์ดึงอากาศไปตามการโคจร",
                            f"เบนไปทาง{SIDE[hemisphere]}ของทิศที่เคลื่อนที่ เพราะแรงดึงดูดของดวงจันทร์",
                            "เบนขึ้นด้านบนเสมอ เพราะอากาศที่เคลื่อนที่ร้อนขึ้นและลอยตัว",
                        ), 2)),
                hint="ซีกโลกเหนือเบนขวา ซีกโลกใต้เบนซ้าย และเหตุคือการหมุนรอบตัวเองของโลก",
                topic=CORIOLIS_TOPIC,
            )
        if rng.random() < 0.5:
            # Air leaving a high turns the same side, so it spins the other way.
            return _labelled(
                stem=f"เมื่อมองจากด้านบน อากาศที่พัดออกจากศูนย์กลางความกดอากาศสูงใน{hemisphere}หมุนทางใด",
                correct=f"หมุน{CYCLONE[other]} เพราะอากาศที่พัดออกจากศูนย์กลางเบนไปทาง{SIDE[hemisphere]}",
                wrongs=(f"หมุน{CYCLONE[hemisphere]} เพราะอากาศที่พัดออกจากศูนย์กลางเบนไปทาง{SIDE[other]}",
                        f"หมุน{CYCLONE[hemisphere]} เพราะอากาศที่พัดออกจากศูนย์กลางเบนไปทาง{SIDE[hemisphere]}",
                        rng.choice(("ไม่หมุน เพราะอากาศพัดตรงออกจากศูนย์กลางไปทุกทิศ",
                                    "หมุนสลับทิศทุกวัน เพราะกลางวันและกลางคืนอากาศเบนต่างกัน",
                                    "ไม่หมุน เพราะอากาศพัดเข้าหาศูนย์กลางความกดอากาศสูงเสมอ"))),
                hint="อากาศที่พุ่งออกจากศูนย์กลางแล้วเบนไปทางเดียวกันทุกทิศ จะวนเป็นวงสวนกับวงของหย่อมความกดอากาศต่ำ",
                topic=CORIOLIS_TOPIC,
            )
        return _labelled(
            stem=f"เมื่อมองจากด้านบน อากาศที่พัดเข้าหาศูนย์กลางความกดอากาศต่ำใน{hemisphere}หมุนทางใด",
            correct=f"หมุน{CYCLONE[hemisphere]} เพราะอากาศที่พัดเข้าหาศูนย์กลางเบนไปทาง{SIDE[hemisphere]}",
            wrongs=(f"หมุน{CYCLONE[other]} เพราะอากาศที่พัดเข้าหาศูนย์กลางเบนไปทาง{SIDE[other]}",
                    f"หมุน{CYCLONE[other]} เพราะอากาศที่พัดเข้าหาศูนย์กลางเบนไปทาง{SIDE[hemisphere]}",
                    rng.choice(("ไม่หมุน เพราะอากาศพัดตรงเข้าหาศูนย์กลางจากทุกทิศ",
                                "หมุนสลับทิศทุกวัน เพราะกลางวันและกลางคืนอากาศเบนต่างกัน",
                                "ไม่หมุน เพราะอากาศพัดออกจากศูนย์กลางความกดอากาศต่ำเสมอ"))),
            hint="อากาศที่พุ่งเข้าหาศูนย์กลางแล้วเบนไปทางเดียวกันทุกทิศ จะวนเป็นวง",
            topic=CORIOLIS_TOPIC,
        )


@question_type(
    "geo.coriolis_fluency",
    display_name={"th": "อธิบายทิศทางการเคลื่อนที่ของอากาศจากการหมุนรอบตัวเองของโลก"},
    level=UPPER_SIX, subject=SUBJECT, topic=CORIOLIS_TOPIC,
)
class CoriolisFluency(QuestionType):
    """A hemisphere and a heading; where the air turns, and why."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hemisphere = rng.choice((NORTH, SOUTH))
        other = SOUTH if hemisphere == NORTH else NORTH
        heading = rng.choice(HEADINGS)
        right = turned(hemisphere, heading)
        wrong_side = turned(other, heading)
        # A diagonal that neither side reaches from this heading.
        _stray = rng.choice(sorted({diagonal for diagonal in TURN.values()} - {right, wrong_side}))
        return _labelled(
            stem=(f"มวลอากาศใน{hemisphere}เริ่มเคลื่อนที่ไปทาง{heading}เป็นระยะทางไกล "
                  "ข้อใดอธิบายทิศทางการเคลื่อนที่ของมวลอากาศนี้ได้ถูกต้อง"),
            correct=f"เบนไปทาง{SIDE[hemisphere]} จึงเคลื่อนที่เฉียงไปทาง{right} {ROTATION}",
            # Three of four: the wrong side, no turn, and the right side toward either
            # diagonal this heading cannot reach.
            wrongs=tuple([f"เบนไปทาง{SIDE[other]} จึงเคลื่อนที่เฉียงไปทาง{wrong_side} {ROTATION}",
                 f"เคลื่อนที่ตรงไปทาง{heading} เพราะการหมุนรอบตัวเองของโลกไม่ทำให้อากาศเบน"]
                + [f"เบนไปทาง{SIDE[hemisphere]} จึงเคลื่อนที่เฉียงไปทาง{one} {ROTATION}"
                   for one in sorted({diagonal for diagonal in TURN.values()} - {right, wrong_side})]),
            hint="ซีกโลกเหนือเบนขวา ซีกโลกใต้เบนซ้าย แล้วหมุนทิศที่เคลื่อนที่ไปทางนั้นเล็กน้อย",
            topic=CORIOLIS_TOPIC,
        )


@question_type(
    "geo.coriolis_application",
    display_name={"th": "วิเคราะห์ลมค้าและการหมุนของพายุในแต่ละซีกโลก"},
    level=UPPER_SIX, subject=SUBJECT, topic=CORIOLIS_TOPIC,
)
class CoriolisApplication(QuestionType):
    """Trade winds, no cyclones on the equator, and storms spinning both ways."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CORIOLIS_SCENARIOS,
            hint="ระบุซีกโลกก่อน แล้วนึกว่าอากาศเบนไปทางใดเมื่อเคลื่อนที่",
        ), CORIOLIS_TOPIC)
