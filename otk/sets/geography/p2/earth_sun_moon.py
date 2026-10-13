"""โลก ดวงอาทิตย์ และดวงจันทร์

ภูมิศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ส 5.1 ป.2/3
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.sets._support.geography import P2, SUBJECT, choices, stage, turned

PROVENANCE = Provenance("original")


TOPIC = "โลก ดวงอาทิตย์ และดวงจันทร์"

FOUR = ("ทิศตะวันออก", "ทิศตะวันตก", "ทิศเหนือ", "ทิศใต้")


def _others(right: str) -> tuple[str, ...]:
    return tuple(d for d in FOUR if d != right)


@question_type(
    "geog.earth_sun_moon_p2",
    display_name={"th": "อธิบายปรากฏการณ์ที่เกิดจากโลก ดวงอาทิตย์ และดวงจันทร์"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class EarthSunMoon(ConceptBankType):
    ITEMS = [
        Concept("ดวงอาทิตย์ขึ้นทางทิศใด", "ทิศตะวันออก", _others("ทิศตะวันออก")),
        Concept("ดวงอาทิตย์ตกทางทิศใด", "ทิศตะวันตก", _others("ทิศตะวันตก")),
        Concept("ดวงจันทร์ขึ้นทางทิศใด", "ทิศตะวันออก", _others("ทิศตะวันออก")),
        Concept("ตอนเช้า เงาของต้นไม้ทอดไปทางทิศใด", "ทิศตะวันตก", _others("ทิศตะวันตก")),
        Concept("ตอนเย็น เงาของต้นไม้ทอดไปทางทิศใด", "ทิศตะวันออก", _others("ทิศตะวันออก")),
        Concept("เหตุใดโลกจึงมีกลางวันและกลางคืน", "เพราะโลกหมุนรอบตัวเอง",
                ("เพราะดวงอาทิตย์ดับลงทุกคืน", "เพราะดวงจันทร์บังดวงอาทิตย์ทุกคืน",
                 "เพราะเมฆบังดวงอาทิตย์ทุกเย็น")),
        Concept("ดวงจันทร์สว่างได้เพราะเหตุใด", "สะท้อนแสงจากดวงอาทิตย์",
                ("มีไฟลุกไหม้อยู่บนดวงจันทร์", "ปล่อยแสงออกมาเองทั้งดวง", "สะท้อนแสงไฟจากเมืองบนโลก")),
        Concept("ดวงจันทร์ที่เห็นเปลี่ยนรูปร่างไปในแต่ละคืน เรียกว่าอะไร", "ข้างขึ้นข้างแรม",
                ("สุริยุปราคา", "ฤดูกาล", "กลางวันกลางคืน")),
    ]


SUN = {"ตอนเช้า": "ทิศตะวันออก", "ตอนเย็น": "ทิศตะวันตก"}


@question_type(
    "geog.sun_direction_p2",
    display_name={"th": "ใช้ตำแหน่งของดวงอาทิตย์บอกทิศ"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class SunDirection(QuestionType):
    def build(self, rng: Random, **params):
        when = rng.choice(tuple(SUN))
        toward = rng.random() < 0.5
        facing = SUN[when] if toward else turned(SUN[when], 4)
        side, turn = rng.choice((("ข้างหน้า", 0), ("ข้างหลัง", 4), ("ขวามือ", 2), ("ซ้ายมือ", -2)))
        pose = "หันหน้าเข้าหาดวงอาทิตย์" if toward else "หันหลังให้ดวงอาทิตย์"
        correct = turned(facing, turn)
        slips = [("direction.left_right_swapped", turned(facing, -turn))] if turn in (2, -2) else []
        return choices(
            stem=f"{when} ยืน{pose} {side}ของเราคือทิศใด",
            correct=correct,
            wrongs=[*slips, ("direction.opposite", turned(correct, 4)), turned(correct, 2), turned(correct, -2)],
            hint="ดวงอาทิตย์ขึ้นทางทิศตะวันออกตอนเช้า และตกทางทิศตะวันตกตอนเย็น หาทิศที่หันหน้าไปก่อน แล้วค่อยหาทิศอื่น",
            topic=TOPIC)


@question_type(
    "geog.earth_sun_moon_reasoning_p2",
    display_name={"th": "ใช้ความรู้เรื่องโลก ดวงอาทิตย์ และดวงจันทร์อธิบายเหตุการณ์"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class EarthSunMoonReasoning(ConceptBankType):
    ITEMS = [
        Concept("ใช้ไฟฉายส่องลูกโลกในห้องมืด แล้วหมุนลูกโลกช้า ๆ กิจกรรมนี้จำลองปรากฏการณ์ใด",
                "การเกิดกลางวันและกลางคืน", ("การเกิดฤดูกาล", "การเกิดข้างขึ้นข้างแรม", "การเกิดฝนตก")),
        Concept("ขณะที่ประเทศไทยเป็นเวลากลางวัน ประเทศที่อยู่อีกด้านหนึ่งของโลกเป็นเวลาใด",
                "เวลากลางคืน", ("เวลากลางวันเหมือนกัน", "เวลาเที่ยงวันพอดี", "เวลาเช้าตรู่เสมอ")),
        Concept("ทำไมเราจึงมองไม่เห็นดาวส่วนใหญ่ในเวลากลางวัน", "แสงอาทิตย์สว่างกลบแสงดาว",
                ("ดาวทุกดวงดับในเวลากลางวัน", "ดาวย้ายไปอยู่ใต้พื้นโลก", "เมฆบังดาวไว้ทุกดวง")),
        Concept("ห้องเรียนที่มีหน้าต่างหันไปทางทิศตะวันออก จะได้รับแสงแดดส่องเข้ามามากในช่วงใด",
                "ช่วงเช้า", ("ช่วงบ่ายแก่", "ช่วงเย็น", "ช่วงกลางคืน")),
        Concept("ถ้าต้องการปลูกต้นไม้ไว้บังแดดตอนบ่ายให้บ้าน ควรปลูกไว้ทางทิศใดของบ้าน",
                "ทิศตะวันตก", ("ทิศตะวันออก", "ทิศเหนือ", "ทิศใต้")),
    ]
