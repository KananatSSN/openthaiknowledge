"""สารควบคุมการเจริญเติบโตของพืช

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/11

Sets moved here from: science_wave_b22.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import UPPER_FOUR
from otk.sets._support.science_wave_b22 import GROWTH_TOPIC, REGULATOR_SCENARIOS

PROVENANCE = Provenance("original")


class Regulator(NamedTuple):
    """A synthetic plant growth regulator, what it does, and how farming uses it."""
    name: str
    effect: str
    use: str
    need: str


REGULATORS = (
    Regulator("ออกซินสังเคราะห์",
              "กระตุ้นการยืดตัวของเซลล์และการเกิดรากของกิ่ง",
              "ใช้จุ่มโคนกิ่งปักชำเพื่อให้ออกรากได้เร็วขึ้นและมากขึ้น",
              "ต้องการให้กิ่งปักชำของไม้ประดับออกรากเร็วและรอดมากขึ้น"),
    Regulator("จิบเบอเรลลินสังเคราะห์",
              "กระตุ้นการยืดตัวของปล้องและกระตุ้นการงอกของเมล็ด",
              "ใช้ฉีดพ่นองุ่นไร้เมล็ดให้ช่อยืดยาวและผลมีขนาดใหญ่ขึ้น",
              "ต้องการให้ผลองุ่นมีขนาดใหญ่ขึ้นและช่อไม่แน่นจนผลเบียดกัน"),
    Regulator("เอทิฟอน",
              "สลายตัวให้แก๊สเอทิลีน ซึ่งเร่งการสุกของผลและการหลุดร่วง",
              "ใช้บ่มผลไม้ เช่น กล้วยและมะม่วง ให้สุกพร้อมกันตามเวลาที่ต้องการ",
              "ต้องการให้ผลไม้ที่เก็บมาสุกพร้อมกันก่อนส่งถึงตลาด"),
    Regulator("ไซโทไคนินสังเคราะห์",
              "กระตุ้นการแบ่งเซลล์และชะลอการแก่ของใบ",
              "ใช้ในอาหารเพาะเลี้ยงเนื้อเยื่อเพื่อชักนำให้เกิดยอดจำนวนมาก "
              "และใช้ยืดอายุไม้ตัดดอก",
              "ต้องการเพิ่มจำนวนยอดจากชิ้นส่วนพืชในการเพาะเลี้ยงเนื้อเยื่อ"),
    Regulator("พาโคลบิวทราโซล",
              "ยับยั้งการสร้างจิบเบอเรลลิน ทำให้ปล้องสั้นลงและทรงพุ่มกะทัดรัด",
              "ใช้ราดโคนต้นมะม่วงเพื่อชักนำให้ออกดอกนอกฤดู "
              "และใช้กับไม้กระถางให้ต้นเตี้ยได้รูปทรง",
              "ต้องการให้มะม่วงออกดอกนอกฤดูกาลเพื่อขายได้ราคาสูงขึ้น"),
    Regulator("สารกำจัดวัชพืชกลุ่มออกซินสังเคราะห์",
              "ในความเข้มข้นสูงทำให้พืชใบเลี้ยงคู่เจริญผิดปกติจนตาย "
              "แต่มีผลต่อพืชใบเลี้ยงเดี่ยวน้อยกว่ามาก",
              "ใช้กำจัดวัชพืชใบกว้างในนาข้าวโดยไม่ทำอันตรายต่อต้นข้าว",
              "ต้องการกำจัดวัชพืชใบกว้างในนาข้าวโดยไม่ให้กระทบต้นข้าว"),
)


@question_type(
    "plant.growth_regulator_foundation",
    display_name={"th": "สารควบคุมการเจริญเติบโตของพืชและผลที่เกิดขึ้น"},
    level=UPPER_FOUR, subject=SUBJECT, topic=GROWTH_TOPIC,
)
class GrowthRegulatorFoundation(QuestionType):
    """What each synthetic regulator does to the plant."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(REGULATORS)
        others = [other for other in REGULATORS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” มีผลต่อพืชอย่างไร",
                correct=item.effect,
                wrongs=tuple(other.effect for other in others[:3]),
                hint="แยกให้ออกว่าสารนั้นเร่งการเจริญเติบโต ชะลอไว้ "
                     "หรือเร่งการสุกและการหลุดร่วง",
                topic=GROWTH_TOPIC,
            )
        return _labelled(
            stem=f"สารควบคุมการเจริญเติบโตชนิดใด{item.effect}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านผลที่เกิดกับพืชให้จบก่อน แล้วจึงเลือกสารที่ให้ผลนั้นโดยตรง",
            topic=GROWTH_TOPIC,
        )


@question_type(
    "plant.growth_regulator_fluency",
    display_name={"th": "การประยุกต์ใช้สารควบคุมการเจริญเติบโตทางการเกษตร"},
    level=UPPER_FOUR, subject=SUBJECT, topic=GROWTH_TOPIC,
)
class GrowthRegulatorFluency(QuestionType):
    """Give the agricultural use that answers a need — ``ยกตัวอย่าง`` itself."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(REGULATORS)
        others = [f"{other.name}: {other.use}" for other in REGULATORS
                  if other.name != item.name]
        rng.shuffle(others)
        correct = f"{item.name}: {item.use}"
        return _labelled(
            stem=f"เกษตรกร{item.need} ควรประยุกต์ใช้สารควบคุมการเจริญเติบโต"
                 f"อย่างไร",
            correct=correct, wrongs=tuple(others[:3]),
            hint="จับคู่สิ่งที่เกษตรกรต้องการกับผลที่สารนั้นมีต่อพืชโดยตรง",
            topic=GROWTH_TOPIC,
        )


@question_type(
    "plant.growth_regulator_application",
    display_name={"th": "วิเคราะห์การใช้สารควบคุมการเจริญเติบโตของพืช"},
    level=UPPER_FOUR, subject=SUBJECT, topic=GROWTH_TOPIC,
)
class GrowthRegulatorApplication(QuestionType):
    """Weigh how a regulator is being used against what it actually does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, REGULATOR_SCENARIOS,
            hint="กลับไปที่ผลที่สารนั้นมีต่อพืช แล้วถามว่าการใช้ในกรณีนี้"
                 "ตรงกับผลนั้นและอยู่ในปริมาณที่แนะนำหรือไม่",
        ), GROWTH_TOPIC)
