"""ปัจจัยภายนอกที่มีผลต่อการเจริญเติบโตของพืช

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/10

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
from otk.sets._support.science_wave_b19 import UPPER_FOUR, Fact, _fact_question
from otk.sets._support.science_wave_b22 import GROWTH_SCENARIOS, GROWTH_TOPIC

PROVENANCE = Provenance("original")


GROWTH_FACTS = (
    Fact("แสงมีผลต่อการเจริญเติบโตของพืชอย่างไร",
         "เป็นแหล่งพลังงานของการสังเคราะห์ด้วยแสง เมื่อได้รับแสงน้อยพืชจะสร้างอาหาร"
         "ได้น้อย ลำต้นยืดยาวผิดปกติและใบซีดเหลือง"),
    Fact("น้ำมีผลต่อการเจริญเติบโตของพืชอย่างไร",
         "เป็นวัตถุดิบของการสังเคราะห์ด้วยแสง เป็นตัวทำละลายที่ลำเลียงธาตุอาหาร "
         "และทำให้เซลล์เต่งจนค้ำจุนลำต้นและใบไว้ได้"),
    Fact("ธาตุอาหารในดินมีผลต่อการเจริญเติบโตของพืชอย่างไร",
         "พืชนำไปสร้างสารต่าง ๆ เช่น ใช้ไนโตรเจนสร้างโปรตีนและคลอโรฟิลล์ "
         "เมื่อขาดจะแสดงอาการใบเหลืองและเจริญเติบโตช้า"),
    Fact("อุณหภูมิมีผลต่อการเจริญเติบโตของพืชอย่างไร",
         "มีผลต่ออัตราการทำงานของเอนไซม์ที่เร่งปฏิกิริยาในเซลล์ "
         "ถ้าสูงหรือต่ำเกินช่วงที่เหมาะสม การเจริญเติบโตจะช้าลงหรือหยุดไป"),
    Fact("ความเป็นกรด-เบสของดินมีผลต่อการเจริญเติบโตของพืชอย่างไร",
         "มีผลต่อรูปของธาตุอาหารในดิน ถ้าดินเป็นกรดหรือเบสเกินไป รากจะดูดธาตุอาหาร"
         "บางชนิดไปใช้ไม่ได้แม้ในดินจะมีธาตุนั้นอยู่"),
    Fact("แก๊สออกซิเจนในดินมีผลต่อการเจริญเติบโตของพืชอย่างไร",
         "รากใช้ในการหายใจเพื่อให้ได้พลังงานสำหรับดูดน้ำและธาตุอาหาร "
         "ถ้าดินแฉะจนไม่มีอากาศแทรกอยู่ รากจะขาดออกซิเจนและเน่าได้"),
    Fact("ปริมาณแก๊สคาร์บอนไดออกไซด์ในอากาศมีผลต่อการเจริญเติบโตของพืชอย่างไร",
         "เป็นวัตถุดิบของการสังเคราะห์ด้วยแสง เมื่อมีน้อยอัตราการสังเคราะห์ด้วยแสง"
         "จะลดลง แม้แสงและน้ำจะเพียงพอก็ตาม"),
)


class Setting(NamedTuple):
    """A growing condition, and what it does to the plant and why."""
    condition: str
    outcome: str


SETTINGS = (
    Setting("ปลูกต้นถั่วไว้ในตู้มืดสนิท โดยรดน้ำและใส่ปุ๋ยตามปกติ",
            "ลำต้นยืดยาวผิดปกติ ใบเล็กและซีดเหลือง เพราะขาดแสงจึงสังเคราะห์ด้วยแสง"
            "ไม่ได้และสร้างคลอโรฟิลล์ไม่ได้"),
    Setting("รดน้ำต้นไม้ในกระถางจนมีน้ำขังอยู่ตลอดเวลาติดต่อกันหลายวัน",
            "รากเน่าและต้นเหี่ยวทั้งที่ดินมีน้ำมาก เพราะน้ำที่ขังไล่อากาศออกจากดิน "
            "รากจึงขาดแก๊สออกซิเจนสำหรับการหายใจ"),
    Setting("ปลูกพืชในดินทรายที่มีไนโตรเจนน้อยมาก",
            "ใบล่างเหลืองก่อนและต้นเตี้ยแคระ เพราะพืชต้องใช้ไนโตรเจนสร้างคลอโรฟิลล์"
            "และโปรตีน จึงย้ายไนโตรเจนจากใบแก่ไปเลี้ยงยอดอ่อน"),
    Setting("ปลูกพืชเมืองร้อนไว้ในห้องที่ควบคุมอุณหภูมิให้ต่ำมากตลอดเวลา",
            "การเจริญเติบโตช้าลงมากแม้ปัจจัยอื่นจะครบ เพราะเอนไซม์ที่เร่งปฏิกิริยา"
            "ในเซลล์ทำงานได้ช้าลงเมื่ออุณหภูมิต่ำกว่าช่วงที่เหมาะสม"),
    Setting("ปลูกพืชในดินที่เป็นกรดจัด ทั้งที่ใส่ปุ๋ยครบทุกธาตุแล้ว",
            "พืชยังแสดงอาการขาดธาตุอาหาร เพราะความเป็นกรดจัดทำให้ธาตุอาหารบางชนิด"
            "อยู่ในรูปที่รากดูดไปใช้ไม่ได้"),
    Setting("เพิ่มความเข้มข้นของแก๊สคาร์บอนไดออกไซด์ในโรงเรือนที่มีแสงและน้ำเพียงพอ",
            "อัตราการสังเคราะห์ด้วยแสงสูงขึ้นและพืชเจริญเติบโตเร็วขึ้น "
            "จนถึงระดับหนึ่งที่ปัจจัยอื่นกลายเป็นตัวจำกัดแทน"),
)


@question_type(
    "plant.growth_factor_foundation",
    display_name={"th": "ปัจจัยภายนอกที่มีผลต่อการเจริญเติบโตของพืช"},
    level=UPPER_FOUR, subject=SUBJECT, topic=GROWTH_TOPIC,
)
class GrowthFactorFoundation(QuestionType):
    """Explain how one external factor bears on growth — ``อธิบาย`` itself."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, GROWTH_FACTS, topic=GROWTH_TOPIC,
            hint="โยงปัจจัยนั้นกลับไปที่กระบวนการที่พืชใช้ "
                 "เช่น การสังเคราะห์ด้วยแสง การหายใจของราก หรือการดูดธาตุอาหาร",
        )


@question_type(
    "plant.growth_factor_fluency",
    display_name={"th": "ผลของปัจจัยภายนอกต่อการเจริญเติบโตของพืช"},
    level=UPPER_FOUR, subject=SUBJECT, topic=GROWTH_TOPIC,
)
class GrowthFactorFluency(QuestionType):
    """Say what a stated growing condition does to the plant, and why."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(SETTINGS)
        others = [other.outcome for other in SETTINGS
                  if other.outcome != item.outcome]
        rng.shuffle(others)
        return _labelled(
            stem=f"ถ้า{item.condition} พืชจะเจริญเติบโตอย่างไรและเพราะเหตุใด",
            correct=item.outcome, wrongs=tuple(others[:3]),
            hint="ระบุก่อนว่าปัจจัยใดถูกเปลี่ยนไป แล้วจึงตามไปว่ากระบวนการใด"
                 "ของพืชได้รับผลกระทบ",
            topic=GROWTH_TOPIC,
        )


@question_type(
    "plant.growth_factor_application",
    display_name={"th": "วิเคราะห์การทดลองเรื่องปัจจัยต่อการเจริญเติบโตของพืช"},
    level=UPPER_FOUR, subject=SUBJECT, topic=GROWTH_TOPIC,
)
class GrowthFactorApplication(QuestionType):
    """Judge a design or a conclusion about which factor limited growth."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, GROWTH_SCENARIOS,
            hint="ตรวจว่าการทดลองเปลี่ยนไปเพียงอย่างเดียวหรือไม่ "
                 "และข้อสรุปพูดเกินสิ่งที่การทดลองนั้นแยกแยะได้หรือเปล่า",
        ), GROWTH_TOPIC)
