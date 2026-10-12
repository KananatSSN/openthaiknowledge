"""สิ่งมีชีวิตและสิ่งไม่มีชีวิต

ชีวะ · ป.2 · สสวท. พื้นฐาน
Indicators: ว 1.3 ป.2/1

Sets moved here from: science_wave_b23.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import PRIMARY_TWO, _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b23 import LIVING_SCENARIOS

PROVENANCE = Provenance("original")


LIVING_TOPIC = "สิ่งมีชีวิตและสิ่งไม่มีชีวิต"


class Trait(NamedTuple):
    """One thing living things do that non-living things do not."""
    name: str
    meaning: str


TRAITS = (
    Trait("ต้องการอาหารและน้ำ",
          "สิ่งมีชีวิตต้องกินอาหารและดื่มน้ำ หรือสร้างอาหารเองแล้วดูดน้ำขึ้นมาใช้ "
          "ส่วนสิ่งไม่มีชีวิตไม่ต้องการสิ่งเหล่านี้เลย"),
    Trait("เจริญเติบโตได้",
          "สิ่งมีชีวิตค่อย ๆ มีขนาดใหญ่ขึ้นและเปลี่ยนแปลงไปตามวัยด้วยตัวมันเอง "
          "ส่วนสิ่งไม่มีชีวิตจะโตขึ้นเองไม่ได้"),
    Trait("เคลื่อนไหวได้ด้วยตนเอง",
          "สิ่งมีชีวิตขยับส่วนต่าง ๆ ของตัวเองได้ เช่น สัตว์เดินได้ "
          "และพืชหันใบเข้าหาแสงได้ ส่วนสิ่งไม่มีชีวิตต้องมีแรงจากภายนอกมากระทำ"),
    Trait("สืบพันธุ์ได้",
          "สิ่งมีชีวิตทำให้เกิดสิ่งมีชีวิตรุ่นใหม่ชนิดเดียวกันได้ "
          "ส่วนสิ่งไม่มีชีวิตสร้างสิ่งใหม่ขึ้นเองไม่ได้"),
    Trait("ตอบสนองต่อสิ่งเร้าได้",
          "สิ่งมีชีวิตแสดงอาการเมื่อถูกแตะ ถูกแสง หรือได้ยินเสียง "
          "ส่วนสิ่งไม่มีชีวิตไม่แสดงอาการใดออกมาเอง"),
    Trait("ขับถ่ายของเสียได้",
          "สิ่งมีชีวิตกำจัดของเสียที่เกิดจากการทำงานของร่างกายออกไป "
          "ส่วนสิ่งไม่มีชีวิตไม่มีของเสียที่เกิดขึ้นเองให้ต้องกำจัด"),
)


class Thing(NamedTuple):
    """A thing to sort, the verdict, and the reason that settles it."""
    name: str
    verdict: str


THINGS = (
    Thing("ต้นมะม่วงในสวน",
          "เป็นสิ่งมีชีวิต เพราะเจริญเติบโตขึ้นได้เอง ต้องการน้ำและแสง "
          "และออกดอกออกผลเพื่อสืบพันธุ์ได้"),
    Thing("สุนัขที่เลี้ยงไว้ในบ้าน",
          "เป็นสิ่งมีชีวิต เพราะกินอาหาร เคลื่อนไหวได้เอง "
          "และมีลูกเป็นสุนัขรุ่นต่อไปได้"),
    Thing("เมล็ดถั่วเขียวที่กำลังงอกราก",
          "เป็นสิ่งมีชีวิต เพราะกำลังเจริญเติบโตขึ้นเป็นต้นใหม่ "
          "และต้องการน้ำกับอากาศในการงอก"),
    Thing("ตุ๊กตาหมีผ้า",
          "เป็นสิ่งไม่มีชีวิต เพราะไม่กินอาหาร ไม่โตขึ้นเอง "
          "และเคลื่อนไหวได้ต่อเมื่อมีคนมาจับ"),
    Thing("รถของเล่นที่ใส่ถ่านแล้ววิ่งได้",
          "เป็นสิ่งไม่มีชีวิต เพราะเคลื่อนที่ได้ด้วยพลังงานจากถ่าน "
          "ไม่ได้เคลื่อนไหวด้วยตัวเอง และไม่เจริญเติบโตหรือสืบพันธุ์"),
    Thing("ก้อนหินริมทาง",
          "เป็นสิ่งไม่มีชีวิต เพราะไม่ต้องการอาหารและน้ำ ไม่โตขึ้นเอง "
          "และไม่ตอบสนองเมื่อถูกแตะ"),
    Thing("หุ่นยนต์ของเล่นที่เดินได้และมีเสียง",
          "เป็นสิ่งไม่มีชีวิต เพราะแม้จะขยับและมีเสียงได้ แต่ทำตามคำสั่งที่ใส่ไว้ "
          "ไม่ได้เจริญเติบโตและไม่สืบพันธุ์"),
)


@question_type(
    "life.living_thing_foundation",
    display_name={"th": "ลักษณะของสิ่งมีชีวิต"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=LIVING_TOPIC,
)
class LivingThingFoundation(QuestionType):
    """Know the traits before sorting anything by them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(TRAITS)
        others = [other for other in TRAITS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"การที่สิ่งมีชีวิต “{item.name}” หมายความว่าอย่างไร",
                correct=item.meaning,
                wrongs=tuple(other.meaning for other in others[:3]),
                hint="เทียบกับสิ่งไม่มีชีวิตดูว่าสิ่งไม่มีชีวิตทำอย่างนั้นได้หรือไม่",
                topic=LIVING_TOPIC,
            )
        return _labelled(
            stem=f"ลักษณะใดของสิ่งมีชีวิตหมายถึงการที่{item.meaning}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านคำอธิบายให้จบก่อน แล้วจึงเลือกชื่อลักษณะที่ตรงกับคำอธิบายนั้น",
            topic=LIVING_TOPIC,
        )


@question_type(
    "life.living_thing_fluency",
    display_name={"th": "เปรียบเทียบสิ่งมีชีวิตกับสิ่งไม่มีชีวิต"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=LIVING_TOPIC,
)
class LivingThingFluency(QuestionType):
    """Sort a thing and say why — the ``เปรียบเทียบ`` the indicator asks for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(THINGS)
        others = [other.verdict for other in THINGS
                  if other.verdict != item.verdict]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.name}” เป็นสิ่งมีชีวิตหรือสิ่งไม่มีชีวิต และเพราะเหตุใด",
            correct=item.verdict, wrongs=tuple(others[:3]),
            hint="ถามสามข้อ คือกินอาหารหรือไม่ โตขึ้นเองหรือไม่ "
                 "และมีลูกหลานรุ่นต่อไปได้หรือไม่",
            topic=LIVING_TOPIC,
        )


@question_type(
    "life.living_thing_application",
    display_name={"th": "วิเคราะห์สิ่งมีชีวิตกับสิ่งไม่มีชีวิต"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=LIVING_TOPIC,
)
class LivingThingApplication(QuestionType):
    """Judge a borderline case, or a claim built on one trait alone."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, LIVING_SCENARIOS,
            hint="ลักษณะเดียวยังไม่พอตัดสิน ต้องดูหลายลักษณะประกอบกัน",
        ), LIVING_TOPIC)
