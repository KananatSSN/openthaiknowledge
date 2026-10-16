"""น้ำหนักของวัตถุในสนามโน้มถ่วง

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/6

Sets moved here from: science_wave_f2.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type

PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/outputs/teaching_plan/ข้อสอบแรง.md',))


SUBJECT = "ฟิสิกส์"


UPPER_FOUR = {"th": "ม.4"}


TOPIC = "น้ำหนักของวัตถุในสนามโน้มถ่วง"


EARTH_G = 10                             # m/s², the value this sheet works in


class Place(NamedTuple):
    name: str
    g: float                             # m/s² — rounded to the usual teaching values


# Hand-checked surface gravities, rounded as school texts round them.
PLACES = (
    Place("ดวงจันทร์", 1.6),
    Place("ดาวอังคาร", 3.7),
    Place("ดาวศุกร์", 8.9),
    Place("ดาวพฤหัสบดี", 24.8),
)


# Masses whose weight is clean at every g above as well as on Earth.
MASSES = (5, 10, 20, 25, 50, 100)


def _num(x) -> str:
    x = round(float(x), 2)
    return str(int(x)) if x == int(x) else f"{x:g}"


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...],
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=TOPIC,
        hint=[text(hint)],
    )


def _valued(*, stem: str, answer, unit: str, slips: tuple, fillers: tuple,
            hint: str) -> GeneratedQuestion:
    correct = f"{_num(answer)} {unit}".strip()
    wrongs: list[str] = []
    for value in (*slips, *fillers):
        if value is None or value <= 0:
            continue
        label = f"{_num(value)} {unit}".strip()
        if label != correct and label not in wrongs:
            wrongs.append(label)
        if len(wrongs) == 3:
            break
    return _labelled(stem=stem, correct=correct, wrongs=tuple(wrongs), hint=hint)


@question_type(
    "phys.weight_gravity_foundation",
    display_name={"th": "แยกมวลกับน้ำหนัก และระบุความหมายของสนามโน้มถ่วง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC,
)
class WeightGravityFoundation(QuestionType):
    """Mass against weight, before any product is worked out."""

    FACTS = (
        ("น้ำหนักของวัตถุคืออะไร",
         "แรงที่สนามโน้มถ่วงกระทำต่อมวลของวัตถุ",
         ("ปริมาณเนื้อสารที่วัตถุมี",
          "ปริมาตรของวัตถุ",
          "แรงที่วัตถุกดลงบนพื้นเสมอไม่ว่าอยู่ที่ใด"),
         "น้ำหนักเป็นแรง จึงมีหน่วยเป็นนิวตันและมีทิศเข้าหาศูนย์กลางของดาว"),
        ("มวลกับน้ำหนักต่างกันอย่างไร",
         "มวลเป็นปริมาณเนื้อสารซึ่งคงที่ ส่วนน้ำหนักเป็นแรงซึ่งเปลี่ยนตามสนามโน้มถ่วง",
         ("มวลเป็นแรง ส่วนน้ำหนักเป็นปริมาณเนื้อสาร",
          "ทั้งมวลและน้ำหนักเปลี่ยนตามสถานที่",
          "ทั้งมวลและน้ำหนักคงที่เสมอไม่ว่าอยู่ที่ใด"),
         "ย้ายไปดวงจันทร์ มวลเท่าเดิม แต่น้ำหนักลดลง"),
        ("หน่วยของมวลและหน่วยของน้ำหนักคือข้อใดตามลำดับ",
         "กิโลกรัม และ นิวตัน",
         ("นิวตัน และ กิโลกรัม",
          "กิโลกรัม และ กิโลกรัม",
          "นิวตัน และ นิวตัน"),
         "น้ำหนักเป็นแรง หน่วยจึงเป็นนิวตัน"),
        ("ถ้านำวัตถุชิ้นเดิมขึ้นไปบนดาวที่มีสนามโน้มถ่วงน้อยกว่าโลก ผลเป็นอย่างไร",
         "มวลเท่าเดิม แต่น้ำหนักน้อยลง",
         ("มวลน้อยลง แต่น้ำหนักเท่าเดิม",
          "ทั้งมวลและน้ำหนักน้อยลง",
          "ทั้งมวลและน้ำหนักเท่าเดิม"),
         "W = mg — m ไม่เปลี่ยน แต่ g เล็กลง W จึงเล็กลง"),
        ("ค่าสนามโน้มถ่วง g ที่ผิวโลกมีหน่วยตรงกับข้อใด",
         "นิวตันต่อกิโลกรัม",
         ("นิวตัน", "กิโลกรัม", "กิโลกรัมต่อนิวตัน"),
         "g บอกว่ามวล 1 กิโลกรัม ถูกดึงด้วยแรงกี่นิวตัน"),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            place = rng.choice(PLACES)
            mass = rng.choice(MASSES)
            thing = rng.choice(("นักบินอวกาศ", "หุ่นยนต์สำรวจ", "กล่องเครื่องมือ", "ยานสำรวจ"))
            lighter = place.g < EARTH_G
            return _labelled(
                stem=f"{thing}มวล {mass} กิโลกรัมบนโลก ถูกนำไปที่{place.name} มวลและน้ำหนักจะเป็นอย่างไร",
                correct=f"มวลยังเป็น {mass} กิโลกรัม แต่น้ำหนัก{'น้อยลง' if lighter else 'มากขึ้น'}",
                wrongs=(f"มวลยังเป็น {mass} กิโลกรัม และน้ำหนัก{'มากขึ้น' if lighter else 'น้อยลง'}",
                        f"มวลและน้ำหนัก{'น้อยลง' if lighter else 'มากขึ้น'}ทั้งคู่",
                        "มวลและน้ำหนักเท่าเดิมทั้งคู่"),
                hint=f"มวลไม่ขึ้นกับสถานที่ ส่วนน้ำหนัก W = mg ขึ้นกับ g ซึ่งที่{place.name}เท่ากับ {_num(place.g)} m/s²",
            )
        if roll < 0.7:
            a, b = rng.sample(PLACES + (Place("โลก", EARTH_G),), 2)
            stronger = a if a.g > b.g else b
            weaker = b if a.g > b.g else a
            return _labelled(
                stem=(f"g ที่ผิว{a.name}เท่ากับ {_num(a.g)} m/s² และที่ผิว{b.name}เท่ากับ {_num(b.g)} m/s² "
                      "วัตถุชิ้นเดียวกันจะมีน้ำหนักมากกว่าที่ใด"),
                correct=f"ที่{stronger.name} เพราะ g มากกว่า น้ำหนัก mg จึงมากกว่า",
                wrongs=(f"ที่{weaker.name} เพราะ g น้อยกว่า น้ำหนักจึงมากกว่า", "เท่ากัน เพราะเป็นวัตถุชิ้นเดียวกัน",
                        f"ที่{weaker.name} เพราะมวลมากกว่า"),
                hint="วัตถุชิ้นเดียวกันมีมวลเท่ากัน น้ำหนัก W = mg จึงแปรตาม g",
            )
        stem, correct, wrongs, hint = rng.choice(self.FACTS)
        return _labelled(stem=stem, correct=correct, wrongs=wrongs, hint=hint)


@question_type(
    "phys.weight_gravity_fluency",
    display_name={"th": "คำนวณน้ำหนักหรือมวลด้วย W = mg"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC,
)
class WeightGravityFluency(QuestionType):
    """Run ``W = mg`` on Earth, in both directions."""

    OBJECTS = ("กล่องพัสดุ", "ถุงทราย", "แท่งเหล็ก", "กระเป๋าเดินทาง", "ถังน้ำ")

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        mass = rng.choice(MASSES)
        item = rng.choice(self.OBJECTS)
        weight = mass * EARTH_G
        if rng.random() < 0.5:
            return _valued(
                stem=(f"{item}มีมวล {mass} กิโลกรัม วางอยู่บนผิวโลก "
                      f"จงหาน้ำหนักของ{item}นี้ (กำหนดให้ g = {EARTH_G} เมตรต่อวินาที²)"),
                answer=weight, unit="นิวตัน",
                # Reporting the mass as if it were the weight is the whole point
                # of the item; dividing by g is the same slip reversed.
                slips=(mass, mass / EARTH_G, weight * 2),
                fillers=(weight + 10, weight + 50, weight + 5),
                hint="W = mg — คูณมวลด้วยค่าสนามโน้มถ่วง แล้วตอบเป็นนิวตัน",
            )
        return _valued(
            stem=(f"{item}ใบหนึ่งมีน้ำหนัก {weight} นิวตัน เมื่อชั่งบนผิวโลก "
                  f"จงหามวลของ{item}นี้ (กำหนดให้ g = {EARTH_G} เมตรต่อวินาที²)"),
            answer=mass, unit="กิโลกรัม",
            slips=(weight, weight * EARTH_G, mass * 2),
            fillers=(mass + 5, mass + 10, mass + 1),
            hint="จาก W = mg จะได้ m = W / g",
        )


@question_type(
    "phys.weight_gravity_application",
    display_name={"th": "เปรียบเทียบน้ำหนักของวัตถุเดียวกันในสนามโน้มถ่วงต่างกัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC,
)
class WeightGravityApplication(QuestionType):
    """The same object somewhere else — the sheet's ตอน 5 ข้อ 2 shape."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        mass = rng.choice(MASSES)
        place = rng.choice(PLACES)
        there = mass * place.g
        here = mass * EARTH_G
        if rng.random() < 0.5:
            return _valued(
                stem=(f"วัตถุชิ้นหนึ่งมีมวล {mass} กิโลกรัม ถ้านำไปไว้บน{place.name} "
                      f"ซึ่งมีค่าสนามโน้มถ่วง {_num(place.g)} เมตรต่อวินาที² "
                      f"วัตถุนี้จะมีน้ำหนักเท่าใด"),
                answer=there, unit="นิวตัน",
                # Weighing it on Earth instead, and reporting the mass unchanged.
                slips=(here, mass, mass / place.g),
                fillers=(there + 10, there + 5, there + 20),
                hint=f"มวลไม่เปลี่ยนตามสถานที่ ใช้ W = mg โดย g ของ{place.name}",
            )
        return _labelled(
            stem=(f"นักบินอวกาศนำวัตถุมวล {mass} กิโลกรัม จากโลก "
                  f"(g = {EARTH_G} เมตรต่อวินาที²) ไปยัง{place.name} "
                  f"(g = {_num(place.g)} เมตรต่อวินาที²) ข้อใดถูกต้อง"),
            correct=f"มวลยังคงเป็น {mass} กิโลกรัมเท่าเดิม น้ำหนักเปลี่ยนเป็น {_num(there)} นิวตัน",
            wrongs=(f"ทั้งมวลและน้ำหนักเปลี่ยนเป็น {_num(there)} เท่ากันตามค่า g ใหม่",
                    f"มวลเปลี่ยนเป็น {_num(there)} กิโลกรัม ส่วนน้ำหนักคงเดิมที่ {_num(here)} นิวตัน",
                    f"ทั้งมวลและน้ำหนักคงเดิมที่ {mass} กิโลกรัม และ {_num(here)} นิวตัน"),
            hint="มวลคงที่เสมอ มีเพียงน้ำหนักที่เปลี่ยนตามค่า g ของแต่ละดาว",
        )
