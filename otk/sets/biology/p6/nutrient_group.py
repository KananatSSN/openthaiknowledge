"""สารอาหารและประโยชน์ของสารอาหาร

ชีวะ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.6/1

Sets moved here from: science_wave_b17.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import BODY_TOPIC, NUTRIENT_SCENARIOS, PRIMARY_SIX, _body

PROVENANCE = Provenance("original")


class Nutrient(NamedTuple):
    """One nutrient group: what it does, and a food it comes from."""
    name: str
    benefit: str
    sources: str


NUTRIENTS = (
    Nutrient("คาร์โบไฮเดรต",
             "ให้พลังงานแก่ร่างกายเป็นหลัก ใช้ในการทำกิจกรรมต่าง ๆ ในแต่ละวัน",
             "ข้าว ขนมปัง และเผือกมัน"),
    Nutrient("โปรตีน",
             "ใช้สร้างและซ่อมแซมส่วนที่สึกหรอของร่างกาย และทำให้ร่างกายเจริญเติบโต",
             "เนื้อสัตว์ ไข่ นม และถั่ว"),
    Nutrient("ไขมัน",
             "ให้พลังงานสูง เก็บสะสมไว้ใช้ยามจำเป็น และช่วยให้ร่างกายอบอุ่น",
             "น้ำมันพืช เนย และถั่วบางชนิด"),
    Nutrient("วิตามิน",
             "ช่วยให้อวัยวะต่าง ๆ ทำงานได้ตามปกติและช่วยให้ร่างกายต้านทานโรค",
             "ผักและผลไม้สด"),
    Nutrient("แร่ธาตุ",
             "ใช้เป็นส่วนประกอบของกระดูก ฟัน และเลือด",
             "นม ปลาเล็กปลาน้อย และผักใบเขียว"),
    Nutrient("น้ำ",
             "เป็นส่วนประกอบของร่างกาย ช่วยลำเลียงสารและช่วยขับของเสียออกไป",
             "น้ำดื่มสะอาด และน้ำที่อยู่ในผักผลไม้"),
)


class Meal(NamedTuple):
    """One plate, and the nutrient group it is short of."""
    description: str
    missing: str


# Each meal is short of exactly one group, which is what keeps the answer single.
MEALS = (
    Meal("ข้าวสวยกับน้ำมันพืชผัดกับไข่ดาว โดยไม่มีผักหรือผลไม้เลย", "วิตามิน"),
    Meal("ข้าวเปล่ากับผักลวกและผลไม้ โดยไม่มีเนื้อสัตว์ ไข่ นม หรือถั่วเลย", "โปรตีน"),
    Meal("ไก่ทอด ไข่ต้ม และผักสด โดยไม่มีข้าว ขนมปัง หรือแป้งใด ๆ เลย",
         "คาร์โบไฮเดรต"),
    Meal("ข้าว เนื้อสัตว์ ผัก และผลไม้ครบ แต่ไม่ได้ดื่มน้ำเลยตลอดวัน", "น้ำ"),
    Meal("ก๋วยเตี๋ยวน้ำใสที่มีแต่เส้นกับน้ำซุป ไม่ใส่เนื้อสัตว์ ลูกชิ้น หรือเต้าหู้เลย",
         "โปรตีน"),
    Meal("ข้าวต้มกับผักลวกและผลไม้ โดยไม่มีน้ำมัน เนย หรือของทอดใด ๆ ตลอดวัน",
         "ไขมัน"),
)


@question_type(
    "body.nutrient_group_foundation",
    display_name={"th": "สารอาหารแต่ละประเภทและประโยชน์"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class NutrientGroupFoundation(QuestionType):
    """Say what a nutrient is for, which nutrient does a job, or where it comes from."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(NUTRIENTS)
        others = [other for other in NUTRIENTS if other.name != item.name]
        rng.shuffle(others)
        draw = rng.random()
        if draw < 0.34:
            return _body(
                stem=f"“{item.name}” มีประโยชน์ต่อร่างกายอย่างไร",
                correct=item.benefit,
                wrongs=tuple(other.benefit for other in others[:3]),
                hint="แยกว่าสารอาหารนั้นให้พลังงาน ใช้สร้างร่างกาย "
                     "หรือช่วยให้ร่างกายทำงานได้ตามปกติ",
            )
        if draw < 0.67:
            return _body(
                stem=f"สารอาหารประเภทใดมีหน้าที่{item.benefit}",
                correct=item.name,
                wrongs=tuple(other.name for other in others[:3]),
                hint="อ่านประโยชน์ให้จบก่อน แล้วจึงเลือกสารอาหารที่ให้ประโยชน์นั้น",
            )
        return _body(
            stem=f"อาหารจำพวก{item.sources} ให้สารอาหารประเภทใดเป็นหลัก",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="นึกว่าอาหารกลุ่มนั้นกินแล้วได้อะไรเป็นหลัก",
        )


@question_type(
    "body.nutrient_group_fluency",
    display_name={"th": "อ่านสารอาหารจากอาหารที่รับประทาน"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class NutrientGroupFluency(QuestionType):
    """Read a real plate and say which nutrient group it is short of.

    ``ป.6/1`` says ``จากอาหารที่ตนเองรับประทาน``, so the item works from a meal
    rather than from the name of a nutrient.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(MEALS)
        others = [nutrient.name for nutrient in NUTRIENTS
                  if nutrient.name != item.missing]
        rng.shuffle(others)
        return _body(
            stem=f"มื้ออาหารที่ประกอบด้วย{item.description} "
                 f"ขาดสารอาหารประเภทใดมากที่สุด",
            correct=item.missing,
            wrongs=tuple(others[:3]),
            hint="ไล่ดูทีละอย่างว่าในจานนี้มีอะไรให้พลังงาน อะไรใช้สร้างร่างกาย "
                 "และอะไรช่วยให้ร่างกายทำงานได้ตามปกติ",
        )


@question_type(
    "body.nutrient_group_application",
    display_name={"th": "วิเคราะห์สารอาหารจากอาหารในชีวิตประจำวัน"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=BODY_TOPIC,
)
class NutrientGroupApplication(QuestionType):
    """Work back from a symptom or a habit to the nutrient behind it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, NUTRIENT_SCENARIOS,
            hint="ถามว่าอาการนี้เกี่ยวกับพลังงาน การสร้างร่างกาย "
                 "หรือการทำงานตามปกติของอวัยวะ",
        ), BODY_TOPIC)
