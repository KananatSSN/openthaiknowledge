"""สมบัติของไอโซโทปกัมมันตรังสีและครึ่งชีวิต

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/7

Sets moved here from: science_wave_f20.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f20 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_HALF = "สมบัติของไอโซโทปกัมมันตรังสีและครึ่งชีวิต"


ISOTOPES = (("โซเดียม-24", 15, "ชั่วโมง"), ("ไอโอดีน-131", 8, "วัน"), ("ฟอสฟอรัส-32", 14, "วัน"),
            ("เรดอน-222", Fraction(38, 10), "วัน"), ("โคบอลต์-60", Fraction(53, 10), "ปี"), ("สตรอนเชียม-90", 28, "ปี"),
            ("ทริเทียม", Fraction(123, 10), "ปี"), ("เทคนีเชียม-99m", 6, "ชั่วโมง"))


HALF_FACTS = (
    ("ครึ่งชีวิตของไอโซโทปกัมมันตรังสีคืออะไร", "เวลาที่นิวเคลียสกัมมันตรังสีสลายไปจนเหลือครึ่งหนึ่งของปริมาณเดิม",
     ("เวลาที่สารสลายหมด", "ครึ่งหนึ่งของเวลาที่สารสลายหมด", "เวลาที่รังสีเดินทางได้ครึ่งทาง")),
    ("ครึ่งชีวิตของไอโซโทปกัมมันตรังสีเปลี่ยนไปเมื่อใด", "ไม่เปลี่ยน ไม่ว่าอุณหภูมิ ความดัน หรือสารประกอบที่ไอโซโทปนั้นอยู่",
     ("เปลี่ยนเมื่ออุณหภูมิสูงขึ้น", "เปลี่ยนเมื่อความดันเพิ่มขึ้น", "เปลี่ยนเมื่อไอโซโทปรวมเป็นสารประกอบ")),
    ("ไอโซโทปกัมมันตรังสีต่างจากไอโซโทปเสถียรอย่างไร", "นิวเคลียสไม่เสถียร จึงสลายตัวและแผ่รังสีออกมาได้เอง",
     ("มีจำนวนโปรตอนต่างจากไอโซโทปเสถียร", "มีสมบัติทางเคมีต่างกันมาก", "ไม่มีนิวตรอนในนิวเคลียส")),
    ("นิวเคลียสที่มีจำนวนนิวตรอนมากเกินไปมักสลายให้รังสีชนิดใด", "รังสีบีตา เพราะนิวตรอนเปลี่ยนเป็นโปรตอน",
     ("รังสีแอลฟา เพราะเสียโปรตอนสองตัว", "รังสีแกมมาเท่านั้น", "โพซิตรอนเสมอ")),
)


@question_type(
    "chem.half_life_calc_foundation",
    display_name={"th": "สมบัติของไอโซโทปกัมมันตรังสีและมวลที่เหลือหลังผ่านครึ่งชีวิต"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HALF,
)
class HalfLifeCalcFoundation(QuestionType):
    """What half-life is, and m = m₀/2ⁿ."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.35:
            stem, correct, wrongs = rng.choice(HALF_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_HALF,
                             hint="ครึ่งชีวิตเป็นค่าเฉพาะของแต่ละไอโซโทป ไม่ขึ้นกับอุณหภูมิ ความดัน หรือสารประกอบ")
        name, half, unit = rng.choice(ISOTOPES)
        n = rng.randint(1, 5)
        start = rng.randint(1, 25) * 2 ** n
        return numeric(
            stem=f"{name} (ครึ่งชีวิต {show(half)} {unit}) มวล {start} g เมื่อเวลาผ่านไป {show(half * n)} {unit} จะเหลือกี่กรัม",
            answer=Fraction(start, 2 ** n), wrongs=[Fraction(start, 2 * n), start - Fraction(start, 2 ** n), Fraction(start, 2 ** (n - 1))],
            unit="g", topic=TOPIC_HALF, hint="หาจำนวนครึ่งชีวิต n = เวลา ÷ ครึ่งชีวิต แล้วมวลที่เหลือ = มวลเดิม ÷ 2ⁿ")


@question_type(
    "chem.half_life_calc_fluency",
    display_name={"th": "คำนวณครึ่งชีวิตและเวลาในการสลาย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HALF,
)
class HalfLifeCalcFluency(QuestionType):
    """Half-life from masses and time, and the time to fall to a mass."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        n = rng.randint(1, 5)
        half = rng.randint(2, 40)
        unit = rng.choice(("วัน", "ชั่วโมง", "นาที", "ปี"))
        start = rng.randint(1, 20) * 2 ** n
        left = Fraction(start, 2 ** n)
        if rng.random() < 0.5:
            return numeric(
                stem=f"ไอโซโทปกัมมันตรังสีมวล {start} g สลายจนเหลือ {show(left)} g ในเวลา {half * n} {unit} มีครึ่งชีวิตเท่าใด",
                answer=half, wrongs=[Fraction(half * n, 2), half * n, Fraction(half * n, 2 ** n)], unit=unit,
                topic=TOPIC_HALF, hint="หาว่าลดลงครึ่งหนึ่งกี่ครั้ง (n) แล้วครึ่งชีวิต = เวลา ÷ n")
        return numeric(
            stem=f"ไอโซโทปกัมมันตรังสีมีครึ่งชีวิต {half} {unit} มวล {start} g ต้องใช้เวลาเท่าใดจึงเหลือ {show(left)} g",
            answer=half * n, wrongs=[half * 2 ** n, half, half * (n + 1)], unit=unit, topic=TOPIC_HALF,
            hint="มวลลดลงครึ่งหนึ่ง n ครั้ง ใช้เวลา n × ครึ่งชีวิต")


@question_type(
    "chem.half_life_calc_application",
    display_name={"th": "มวลที่สลายไปและเศษส่วนที่เหลือของไอโซโทปกัมมันตรังสี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HALF,
)
class HalfLifeCalcApplication(QuestionType):
    """How much has decayed, not how much is left, and the fraction left as a percentage."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, half, unit = rng.choice(ISOTOPES)
        n = rng.randint(1, 4)
        if rng.random() < 0.5:
            start = rng.randint(1, 25) * 2 ** n
            decayed = start - Fraction(start, 2 ** n)
            return numeric(
                stem=f"{name} (ครึ่งชีวิต {show(half)} {unit}) มวล {start} g เมื่อผ่านไป {show(half * n)} {unit} สลายไปแล้วกี่กรัม",
                answer=decayed, wrongs=[Fraction(start, 2 ** n), Fraction(start, 2), start - Fraction(start, 2 * n)],
                unit="g", topic=TOPIC_HALF, hint="มวลที่สลายไป = มวลเดิม − มวลที่เหลือ (มวลที่เหลือ = มวลเดิม ÷ 2ⁿ)")
        return numeric(
            stem=f"เมื่อผ่านไป {show(half * n)} {unit} {name} (ครึ่งชีวิต {show(half)} {unit}) เหลือกี่เปอร์เซ็นต์ของปริมาณเดิม",
            answer=Fraction(100, 2 ** n), wrongs=[100 - Fraction(100, 2 ** n), Fraction(100, 2 * n), Fraction(100, 2 ** (n + 1))],
            unit="%", topic=TOPIC_HALF, hint="เหลือ (1/2)ⁿ ของเดิม แล้วคูณ 100")
