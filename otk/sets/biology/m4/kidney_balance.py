"""ดุลยภาพของน้ำและสารในเลือด

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/2

Sets moved here from: science_wave_b19.
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
from otk.sets._support.science_wave_b19 import (
    BALANCE_TOPIC,
    KIDNEY_SCENARIOS,
    UPPER_FOUR,
    Fact,
    _fact_question,
)

PROVENANCE = Provenance("original")


KIDNEY_FACTS = (
    Fact("หน่วยไตทำหน้าที่ใดในการรักษาดุลยภาพของน้ำและสารในเลือด",
         "กรองน้ำและสารโมเลกุลเล็กออกจากเลือด แล้วดูดสารที่ยังมีประโยชน์กับน้ำ"
         "กลับคืน ก่อนขับส่วนที่เหลือออกเป็นปัสสาวะ"),
    Fact("การกรองที่โกลเมอรูลัสแยกสิ่งใดออกจากเลือด",
         "แยกน้ำและสารโมเลกุลเล็ก เช่น กลูโคส ยูเรีย และไอออนออกมา "
         "ส่วนเซลล์เม็ดเลือดและโปรตีนโมเลกุลใหญ่ยังคงอยู่ในหลอดเลือด"),
    Fact("ในคนปกติ กลูโคสที่ถูกกรองออกมาแล้วถูกจัดการอย่างไร",
         "ถูกดูดกลับเข้าสู่เลือดจนหมดที่ท่อหน่วยไตส่วนต้น "
         "จึงไม่พบกลูโคสในปัสสาวะของคนปกติ"),
    Fact("ฮอร์โมนแอนติไดยูเรติก (ADH) มีผลต่อไตอย่างไร",
         "เพิ่มการดูดน้ำกลับเข้าสู่เลือดที่ท่อหน่วยไตส่วนท้ายและท่อรวม "
         "ปัสสาวะจึงมีปริมาณน้อยลงและเข้มข้นขึ้น"),
    Fact("ต่อมใต้สมองส่วนหลังหลั่ง ADH เพิ่มขึ้นในภาวะใด",
         "เมื่อความเข้มข้นของสารในเลือดสูงขึ้น เช่น เสียเหงื่อมากหรือดื่มน้ำน้อย"),
    Fact("ฮอร์โมนแอลโดสเตอโรนจากต่อมหมวกไตชั้นนอกมีผลต่อไตอย่างไร",
         "เพิ่มการดูดโซเดียมไอออนกลับเข้าสู่เลือดที่ท่อหน่วยไต "
         "และน้ำจะถูกดูดกลับตามไปด้วย"),
    Fact("ยูเรียในเลือดเกิดขึ้นที่ใดและถูกกำจัดออกอย่างไร",
         "เกิดที่ตับจากการสลายกรดแอมิโนที่เกินความต้องการ "
         "แล้วลำเลียงไปกับเลือดเพื่อกำจัดออกทางไต"),
)


class Adjustment(NamedTuple):
    """A change in the body's water or solute state, and the kidney's response."""
    situation: str
    response: str


ADJUSTMENTS = (
    Adjustment("ออกกำลังกลางแดดจนเสียเหงื่อมากและยังไม่ได้ดื่มน้ำ",
               "เลือดเข้มข้นขึ้น ต่อมใต้สมองส่วนหลังจึงหลั่ง ADH มากขึ้น "
               "ไตดูดน้ำกลับมากขึ้น ปัสสาวะจึงน้อยลงและเข้มข้นขึ้น"),
    Adjustment("ดื่มน้ำเปล่าติดต่อกันหลายแก้วในเวลาสั้น ๆ",
               "เลือดเจือจางลง การหลั่ง ADH จึงลดลง ไตดูดน้ำกลับน้อยลง "
               "ปัสสาวะจึงมีปริมาณมากขึ้นและใสขึ้น"),
    Adjustment("รับประทานอาหารที่มีรสเค็มจัดเป็นมื้อใหญ่",
               "โซเดียมไอออนในเลือดสูงขึ้น ร่างกายจึงกระหายน้ำและหลั่ง ADH มากขึ้น "
               "ไตเก็บน้ำไว้เพื่อเจือจางเลือด แล้วจึงค่อย ๆ ขับโซเดียมส่วนเกินออก"),
    Adjustment("เสียน้ำและเกลือแร่จากการท้องเสียอย่างรุนแรง",
               "ปริมาตรเลือดลดลง ไตจึงถูกกระตุ้นให้ดูดโซเดียมไอออนและน้ำกลับมากขึ้น "
               "ผ่านการหลั่งแอลโดสเตอโรนที่เพิ่มขึ้น"),
    Adjustment("อยู่ในที่อากาศเย็นจัดเป็นเวลานานโดยไม่ได้เสียเหงื่อ",
               "ร่างกายเสียน้ำทางผิวหนังน้อย น้ำส่วนเกินจึงถูกขับออกทางไต "
               "ปัสสาวะจึงมีปริมาณมากกว่าปกติ"),
    Adjustment("รับประทานอาหารที่มีโปรตีนสูงมากติดต่อกันหลายวัน",
               "ตับสลายกรดแอมิโนส่วนเกินเป็นยูเรียมากขึ้น "
               "ไตจึงต้องขับยูเรียออกทางปัสสาวะมากขึ้นตามไปด้วย"),
)


@question_type(
    "body.kidney_balance_foundation",
    display_name={"th": "การทำงานของไตกับดุลยภาพของน้ำและสารในเลือด"},
    level=UPPER_FOUR, subject=SUBJECT, topic=BALANCE_TOPIC,
)
class KidneyBalanceFoundation(QuestionType):
    """How the nephron and its hormones hold blood water and solutes steady."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, KIDNEY_FACTS, topic=BALANCE_TOPIC,
            hint="แยกให้ชัดสามขั้น คือการกรอง การดูดกลับ และการขับออก "
                 "แล้วดูว่าฮอร์โมนเข้ามาเกี่ยวข้องที่ขั้นใด",
        )


@question_type(
    "body.kidney_balance_fluency",
    display_name={"th": "การปรับการทำงานของไตตามสภาวะของร่างกาย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=BALANCE_TOPIC,
)
class KidneyBalanceFluency(QuestionType):
    """Say how the kidney answers a change in the body's water or solute load."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ADJUSTMENTS)
        others = [other.response for other in ADJUSTMENTS
                  if other.response != item.response]
        rng.shuffle(others)
        return _labelled(
            stem=f"เมื่อ{item.situation} ไตจะทำงานอย่างไรเพื่อรักษาดุลยภาพ"
                 f"ของน้ำและสารในเลือด",
            correct=item.response, wrongs=tuple(others[:3]),
            hint="ถามก่อนว่าเลือดเข้มข้นขึ้นหรือเจือจางลง "
                 "แล้วจึงตามไปว่าไตควรเก็บน้ำไว้หรือขับออก",
            topic=BALANCE_TOPIC,
        )


@question_type(
    "body.kidney_balance_application",
    display_name={"th": "วิเคราะห์ความผิดปกติของดุลยภาพน้ำและสารในเลือด"},
    level=UPPER_FOUR, subject=SUBJECT, topic=BALANCE_TOPIC,
)
class KidneyBalanceApplication(QuestionType):
    """Read a clinical or experimental result back to the nephron step behind it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, KIDNEY_SCENARIOS,
            hint="ระบุให้ได้ว่าความผิดปกติอยู่ที่การกรอง การดูดกลับ "
                 "หรือที่ฮอร์โมนซึ่งควบคุมการดูดกลับ",
        ), BALANCE_TOPIC)
