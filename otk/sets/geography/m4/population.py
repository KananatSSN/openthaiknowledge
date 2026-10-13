"""ประชากรและการตั้งถิ่นฐาน

ภูมิศาสตร์ · ม.4 · สสวท. พื้นฐาน
Indicators: ส 5.2 ม.4-6/1
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.geography import M4, SUBJECT, choices, number, stage

PROVENANCE = Provenance("original")


TOPIC = "ประชากรและการตั้งถิ่นฐาน"

PLACES = ("จังหวัด ก", "เมือง ข", "อำเภอ ค", "เกาะ ง")


@question_type(
    "geog.population_density_m4",
    display_name={"th": "คำนวณความหนาแน่นของประชากร"},
    level=M4, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class PopulationDensity(QuestionType):
    def build(self, rng: Random, **params):
        area = rng.choice((150, 240, 320, 450, 600, 800, 1_250, 2_000, 2_500, 4_000))
        density = rng.choice((25, 40, 60, 75, 80, 120, 150, 200, 250, 400))
        people = area * density
        place = rng.choice(PLACES)
        unit = "คนต่อตารางกิโลเมตร"
        return choices(
            stem=(f"{place} มีพื้นที่ {number(area)} ตารางกิโลเมตร มีประชากร {number(people)} คน "
                  "ความหนาแน่นของประชากรเป็นเท่าใด"),
            correct=f"{number(density)} {unit}",
            wrongs=[("units.wrong_conversion", f"{number(density * 10)} {unit}"),
                    ("units.wrong_conversion", f"{number(Fraction(density, 10))} {unit}"),
                    f"{number(density * 2)} {unit}", f"{number(density + 20)} {unit}"],
            hint="ความหนาแน่นของประชากร = จำนวนประชากร ÷ พื้นที่ (ตารางกิโลเมตร)",
            topic=TOPIC)


@question_type(
    "geog.natural_increase_m4",
    display_name={"th": "คำนวณอัตราการเพิ่มของประชากรตามธรรมชาติ"},
    level=M4, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class NaturalIncrease(QuestionType):
    def build(self, rng: Random, **params):
        while True:
            people = rng.choice((200_000, 400_000, 500_000, 800_000, 1_000_000, 2_000_000))
            births = rng.randrange(people // 100, people * 3 // 100, 100)
            deaths = rng.randrange(people // 200, people // 100, 100)
            rate = Fraction(births - deaths, people) * 100
            plain = Fraction(births, people) * 100
            summed = Fraction(births + deaths, people) * 100
            if all((x * 100).denominator == 1 for x in (rate, plain, summed)):
                break
        place = rng.choice(PLACES)
        return choices(
            stem=(f"ในปีหนึ่ง {place} มีประชากรกลางปี {number(people)} คน มีคนเกิด {number(births)} คน "
                  f"และมีคนตาย {number(deaths)} คน อัตราการเพิ่มของประชากรตามธรรมชาติเป็นร้อยละเท่าใด"),
            correct=f"ร้อยละ {number(rate)}",
            wrongs=[("steps.missed_a_step", f"ร้อยละ {number(plain)}"),
                    ("operation.reversed", f"ร้อยละ {number(summed)}"),
                    ("units.wrong_conversion", f"ร้อยละ {number(rate * 10)}"),
                    f"ร้อยละ {number(rate + 1)}"],
            hint="อัตราการเพิ่มตามธรรมชาติ = (จำนวนเกิด − จำนวนตาย) ÷ ประชากรกลางปี × 100",
            topic=TOPIC)


@question_type(
    "geog.doubling_time_m4",
    display_name={"th": "ประมาณเวลาที่ประชากรเพิ่มเป็นสองเท่า"},
    level=M4, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class DoublingTime(QuestionType):
    def build(self, rng: Random, **params):
        rate = rng.choice((Fraction(1, 2), Fraction(7, 10), 1, Fraction(7, 5), 2, Fraction(5, 2),
                           Fraction(7, 2), 5, 7))
        years = Fraction(70) / rate
        place = rng.choice(PLACES)
        return choices(
            stem=(f"{place} มีอัตราการเพิ่มของประชากรร้อยละ {number(rate)} ต่อปีคงที่ "
                  "ถ้าใช้กฎ 70 ประชากรจะเพิ่มเป็นสองเท่าภายในประมาณกี่ปี"),
            correct=f"{number(years)} ปี",
            # Only exact wrong values: a rounded one would stand out.
            wrongs=[("operation.reversed", f"{number(70 * rate)} ปี"),
                    *(f"{number(w)} ปี" for w in (Fraction(100) / rate, years * 2, years / 2,
                                                   years + 10)
                      if (w * 100).denominator == 1)],
            hint="กฎ 70: เวลาที่ประชากรเพิ่มเป็นสองเท่า (ปี) ≈ 70 ÷ อัตราการเพิ่มร้อยละต่อปี",
            topic=TOPIC)


@question_type(
    "geog.settlement_pattern_m4",
    display_name={"th": "จำแนกรูปแบบการตั้งถิ่นฐาน"},
    level=M4, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class SettlementPattern(ClassifyType):
    ASKS = ("pick",)           # three groups: a classify question would offer three choices
    PICK_STEM = "ข้อใดเป็นลักษณะของการตั้งถิ่นฐาน{category}"
    CATEGORIES = [
        Category("แบบกระจาย", ("บ้านแต่ละหลังอยู่ห่างกันกลางไร่นาของตน",
                               "บ้านเรือนตั้งอยู่โดดเดี่ยวกระจัดกระจายบนที่ราบกว้าง",
                               "ฟาร์มปศุสัตว์แต่ละแห่งอยู่ห่างกันหลายกิโลเมตร")),
        Category("แบบรวมกลุ่ม", ("บ้านเรือนรวมกันหนาแน่นรอบวัดและตลาด",
                                 "บ้านเรือนรวมกันอยู่รอบแหล่งน้ำเพียงแห่งเดียว",
                                 "บ้านเรือนรวมกันเป็นกลุ่มก้อนรอบโอเอซิสกลางทะเลทราย")),
        Category("แบบแนวยาว", ("บ้านเรือนเรียงเป็นแถวยาวตามริมแม่น้ำ",
                               "บ้านเรือนเรียงเป็นแนวยาวตามสองข้างถนน",
                               "บ้านเรือนเรียงเป็นแนวยาวขนานไปกับชายหาด")),
    ]
