"""การรับและคายพลังงานจากดวงอาทิตย์

ธรณีวิทยา · ม.5 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/1

Sets moved here from: science_wave_f78.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f78 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_SUN = "การรับและคายพลังงานจากดวงอาทิตย์"


# Every surface is named with its condition, so the one that needs a
# qualifier (sea at high sun) is not the one long name among short ones.
ALBEDO = (("หิมะที่เพิ่งตกใหม่ ๆ", 80), ("ทะเลทรายทรายสีอ่อน", 40), ("ทุ่งหญ้าเขียวขจีหน้าฝน", 25),
          ("ป่าไม้เขียวทึบทั้งผืน", 15), ("ผิวน้ำทะเลตอนแดดตั้งฉาก", 8), ("ถนนยางมะตอยสีดำ", 10))


SUN_FACTS = (
    ("เหตุใดบริเวณเส้นศูนย์สูตรจึงได้รับพลังงานจากดวงอาทิตย์ต่อพื้นที่มากกว่าบริเวณขั้วโลก", "แสงตกกระทบเกือบตั้งฉาก พลังงานจึงกระจายบนพื้นที่น้อยกว่า",
     ("อยู่ใกล้ดวงอาทิตย์มากกว่าหลายพันกิโลเมตร", "มีเมฆน้อยกว่า แสงอาทิตย์จึงส่องถึงพื้นได้มากกว่าทุกวัน", "มีกลางวันยาวกว่าบริเวณอื่นตลอดปี จึงได้รับแสงนานกว่ามาก", "โลกหมุนเร็วกว่าที่เส้นศูนย์สูตร")),
    ("เหตุใดพื้นดินร้อนเร็วและเย็นเร็วกว่าพื้นน้ำ", "พื้นดินมีความจุความร้อนจำเพาะต่ำกว่าน้ำ",
     ("พื้นดินสะท้อนแสงมากกว่าน้ำทุกกรณี", "น้ำสะท้อนแสงออกไปเกือบหมดทุกกรณี", "พื้นดินอยู่ใกล้ดวงอาทิตย์มากกว่า", "น้ำมีความจุความร้อนจำเพาะต่ำกว่าพื้นดิน")),
    ("ค่าอัตราส่วนสะท้อน (albedo) สูงหมายความว่าอย่างไร", "พื้นผิวสะท้อนแสงอาทิตย์ออกไปมากและดูดกลืนได้น้อย",
     ("พื้นผิวดูดกลืนแสงได้มาก", "พื้นผิวปล่อยรังสีอินฟราเรดออกมามากกว่าที่ได้รับ", "พื้นผิวปล่อยรังสีอินฟราเรดมาก", "พื้นผิวดูดกลืนแสงได้มาก และสะท้อนออกไปได้น้อย")),
    ("เหตุใดฤดูร้อนของซีกโลกเหนือจึงเกิดขึ้นเมื่อแกนโลกเอียงเข้าหาดวงอาทิตย์", "แสงตกกระทบชันขึ้นและช่วงกลางวันยาวขึ้น",
     ("โลกอยู่ใกล้ดวงอาทิตย์ที่สุดทุกครั้ง", "ดวงอาทิตย์ร้อนขึ้นในช่วงนั้น", "โลกอยู่ใกล้ดวงอาทิตย์ที่สุดในช่วงนั้น", "โลกหมุนรอบตัวเองช้าลงในช่วงนั้น")),
)


SUN_HINT = ("พลังงานต่อพื้นที่ขึ้นกับมุมที่แสงตกกระทบ ยิ่งตั้งฉากยิ่งได้มาก ช่วงกลางวันยาวได้รับมาก พื้นผิวสีอ่อนสะท้อนมาก "
            "น้ำมีความจุความร้อนสูงจึงร้อนและเย็นช้ากว่าพื้นดิน")


@question_type(
    "geo.solar_heating_foundation",
    display_name={"th": "ปัจจัยที่มีผลต่อการรับพลังงานจากดวงอาทิตย์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SUN,
)
class SolarHeatingFoundation(QuestionType):
    """Sun angle, day length, albedo, land and water."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(SUN_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_SUN, hint=SUN_HINT)


@question_type(
    "geo.solar_heating_fluency",
    display_name={"th": "เปรียบเทียบการสะท้อนแสงของพื้นผิวต่าง ๆ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SUN,
)
class SolarHeatingFluency(QuestionType):
    """Higher albedo reflects more and heats less."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        picked = rng.sample(ALBEDO, 4)
        most = rng.random() < 0.5
        right = max(picked, key=lambda x: x[1])[0] if most else min(picked, key=lambda x: x[1])[0]
        if rng.random() < 0.5:
            return _labelled(stem=f"พื้นผิวใด{'สะท้อนแสงอาทิตย์ได้มากที่สุด' if most else 'ดูดกลืนแสงอาทิตย์ได้มากที่สุด'}", correct=right,
                             wrongs=tuple(p[0] for p in picked if p[0] != right), topic=TOPIC_SUN, hint=SUN_HINT)
        table = " ".join(f"{n} ร้อยละ {a}" for n, a in picked)
        return _labelled(stem=f"อัตราส่วนสะท้อนของพื้นผิว: {table} พื้นผิวใดน่าจะมีอุณหภูมิ{'ต่ำที่สุด' if most else 'สูงที่สุด'}เมื่อได้รับแสงเท่ากัน",
                         correct=right, wrongs=tuple(p[0] for p in picked if p[0] != right), topic=TOPIC_SUN, hint=SUN_HINT)


@question_type(
    "geo.solar_heating_application",
    display_name={"th": "คำนวณพลังงานแสงอาทิตย์ต่อพื้นที่และพลังงานที่สะท้อน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SUN,
)
class SolarHeatingApplication(QuestionType):
    """Energy per area × sin(altitude); reflected = incoming × albedo."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        incoming = rng.randrange(600, 1201, 100)
        if rng.random() < 0.5:
            angle, sine = rng.choice(((30, Fraction(1, 2)), (90, Fraction(1))))
            return numeric(stem=f"แสงอาทิตย์ที่มีพลังงาน {incoming} W/m² เมื่อตกตั้งฉาก ถ้าตกกระทบพื้นด้วยมุมเงย {angle}° (sin {angle}° = {show(sine)}) "
                                f"พื้นได้รับพลังงานกี่ W/m²", answer=incoming * sine, wrongs=[incoming * (1 - sine) or incoming // 4, incoming, incoming * 2],
                           unit="W/m²", topic=TOPIC_SUN, hint="พลังงานต่อพื้นที่ = พลังงานเมื่อตกตั้งฉาก × sin (มุมเงยของดวงอาทิตย์)")
        surface, albedo = rng.choice(ALBEDO)
        reflected = Fraction(incoming * albedo, 100)
        if rng.random() < 0.5:
            return numeric(stem=f"แสงอาทิตย์ตกกระทบ{surface} {incoming} W/m² ซึ่งมีอัตราส่วนสะท้อนร้อยละ {albedo} พื้นผิวสะท้อนพลังงานกลับกี่ W/m²",
                           answer=reflected, wrongs=[incoming - reflected, albedo, reflected * 2], unit="W/m²", topic=TOPIC_SUN,
                           hint="พลังงานที่สะท้อน = พลังงานที่ตกกระทบ × อัตราส่วนสะท้อน ÷ 100")
        return numeric(stem=f"แสงอาทิตย์ตกกระทบ{surface} {incoming} W/m² ซึ่งมีอัตราส่วนสะท้อนร้อยละ {albedo} พื้นผิวดูดกลืนพลังงานไว้กี่ W/m²",
                       answer=incoming - reflected, wrongs=[reflected, incoming, 100 - albedo], unit="W/m²", topic=TOPIC_SUN,
                       hint="พลังงานที่ดูดกลืน = พลังงานที่ตกกระทบ − พลังงานที่สะท้อน")
