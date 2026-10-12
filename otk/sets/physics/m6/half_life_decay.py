"""การสลายของนิวเคลียสกัมมันตรังสีและครึ่งชีวิต

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/14

Sets moved here from: science_wave_f17.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f17 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_HALF = "การสลายของนิวเคลียสกัมมันตรังสีและครึ่งชีวิต"


ISOTOPES = (("ไอโอดีน-131", 8, "วัน"), ("คาร์บอน-14", 5730, "ปี"), ("โคบอลต์-60", Fraction(53, 10), "ปี"),
            ("เรดอน-222", Fraction(38, 10), "วัน"), ("เทคนีเชียม-99m", 6, "ชั่วโมง"), ("ฟอสฟอรัส-32", 14, "วัน"))


@question_type(
    "phys.half_life_decay_foundation",
    display_name={"th": "ปริมาณนิวเคลียสกัมมันตรังสีที่เหลือหลังผ่านครึ่งชีวิต"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HALF,
)
class HalfLifeDecayFoundation(QuestionType):
    """N = N₀(½)ⁿ after n half-lives."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, half, unit = rng.choice(ISOTOPES)
        n = rng.randint(1, 5)
        start = rng.randint(1, 20) * 2 ** n * (5 if rng.random() < 0.5 else 1)
        left = Fraction(start, 2 ** n)
        return numeric(
            stem=f"{name}มีครึ่งชีวิต {show(half)} {unit} มีอยู่ {start:,} mg เมื่อเวลาผ่านไป {show(half * n)} {unit} จะเหลือกี่มิลลิกรัม",
            answer=left, wrongs=[Fraction(start, 2 * n), start - left, Fraction(start, 2 ** (n + 1))], unit="mg",
            topic=TOPIC_HALF, hint="ผ่านไป n ครึ่งชีวิต เหลือ N₀ ÷ 2ⁿ (ไม่ใช่ N₀ ÷ 2n)")


@question_type(
    "phys.half_life_decay_fluency",
    display_name={"th": "หาครึ่งชีวิตและเวลาที่ใช้ในการสลาย"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HALF,
)
class HalfLifeDecayFluency(QuestionType):
    """Half-life from how much is left after a time, and the time to fall to a fraction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        n = rng.randint(1, 5)
        half = rng.randint(1, 30)
        unit = rng.choice(("วัน", "ชั่วโมง", "ปี"))
        if rng.random() < 0.5:
            return numeric(
                stem=f"สารกัมมันตรังสีเหลือ 1/{2 ** n} ของปริมาณเดิมเมื่อเวลาผ่านไป {half * n} {unit} มีครึ่งชีวิตเท่าใด",
                answer=half, wrongs=[Fraction(half * n, 2 ** n), half * n, Fraction(half * n, 2)], unit=unit,
                topic=TOPIC_HALF, hint="เหลือ 1/2ⁿ คือผ่านไป n ครึ่งชีวิต ครึ่งชีวิต = เวลา ÷ n")
        return numeric(
            stem=f"สารกัมมันตรังสีมีครึ่งชีวิต {half} {unit} ต้องใช้เวลาเท่าใดกัมมันตภาพจึงลดลงเหลือ 1/{2 ** n} ของเดิม",
            answer=half * n, wrongs=[half * 2 ** n, half, Fraction(half * 2 ** n, 2)], unit=unit, topic=TOPIC_HALF,
            hint="กัมมันตภาพแปรผันตรงกับจำนวนนิวเคลียส ลดเหลือ 1/2ⁿ ต้องใช้ n ครึ่งชีวิต")


@question_type(
    "phys.half_life_decay_application",
    display_name={"th": "การหาอายุด้วยคาร์บอน-14 และกัมมันตภาพที่ลดลง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HALF,
)
class HalfLifeDecayApplication(QuestionType):
    """Carbon dating, and the activity after a hospital isotope has sat for days."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        n = rng.randint(1, 4)
        if rng.random() < 0.5:
            what = rng.choice(("ซากไม้ในถ้ำ", "กระดูกสัตว์โบราณ", "เมล็ดข้าวในแหล่งโบราณคดี", "ผ้าห่อศพโบราณ"))
            return numeric(
                stem=(f"{what}มีคาร์บอน-14 เหลือ {show(Fraction(100, 2 ** n))}% ของสิ่งมีชีวิตปัจจุบัน มีอายุประมาณกี่ปี "
                      "(ครึ่งชีวิตของคาร์บอน-14 = 5,730 ปี)"),
                answer=5730 * n, wrongs=[5730 * 2 ** n, 5730, 5730 * (n + 1)], unit="ปี", topic=TOPIC_HALF,
                hint="เหลือ 1/2ⁿ แปลว่าผ่านไป n ครึ่งชีวิต อายุ = n × 5,730 ปี")
        name, half, unit = rng.choice([x for x in ISOTOPES if x[2] != "ปี"])
        a0 = rng.randint(1, 20) * 2 ** n * 10
        return numeric(
            stem=(f"โรงพยาบาลได้รับ{name} (ครึ่งชีวิต {show(half)} {unit}) มีกัมมันตภาพ {a0:,} MBq เมื่อเก็บไว้ {show(half * n)} {unit} "
                  "กัมมันตภาพเหลือกี่เมกะเบกเคอเรล"),
            answer=Fraction(a0, 2 ** n), wrongs=[Fraction(a0, 2 * n), a0 - Fraction(a0, 2 ** n), Fraction(a0, 2 ** (n + 1))],
            unit="MBq", topic=TOPIC_HALF, hint="กัมมันตภาพลดลงครึ่งหนึ่งทุกครึ่งชีวิต")
