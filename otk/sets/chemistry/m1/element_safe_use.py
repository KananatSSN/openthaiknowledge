"""การใช้ธาตุอย่างปลอดภัยและคุ้มค่า

เคมี · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.1/3

Sets moved here from: science_wave_d7.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d7 import SECONDARY_ONE

PROVENANCE = Provenance("original")


GUIDELINE_TOPIC = "การใช้ธาตุอย่างปลอดภัยและคุ้มค่า"


class Guideline(NamedTuple):
    case: str
    safe: str
    worthwhile: str


GUIDELINES = (
    Guideline("ครอบครัวของนักเรียนมีถ่านไฟฉายและแบตเตอรี่โทรศัพท์ที่ใช้หมดแล้วหลายก้อน",
              "ไม่ทุบหรือเผา และแยกทิ้งในถังขยะอันตราย",
              "เปลี่ยนมาใช้แบตเตอรี่แบบชาร์จซ้ำได้ และส่งแบตเตอรี่เก่าไปรีไซเคิล"),
    Guideline("โรงอาหารของโรงเรียนมีกระป๋องเครื่องดื่มอะลูมิเนียมที่ใช้แล้วจำนวนมากทุกวัน",
              "ล้างกระป๋องและระวังขอบที่คมขณะบีบ",
              "แยกกระป๋องส่งรีไซเคิล เพราะนำอะลูมิเนียมไปหลอมใช้ใหม่ได้โดยใช้พลังงานน้อยกว่าผลิตใหม่"),
    Guideline("ห้องเรียนมีหลอดฟลูออเรสเซนต์ที่เสียแล้วและกำลังจะซื้อหลอดใหม่",
              "ห่อหลอดเก่าไม่ให้แตก แล้วทิ้งในถังขยะอันตราย เพราะหลอดมีปรอท",
              "เปลี่ยนเป็นหลอดแอลอีดีที่ประหยัดไฟ อายุการใช้งานยาว และไม่มีปรอท"),
    Guideline("บ้านของนักเรียนใช้น้ำยาฟอกขาวที่มีคลอรีนทำความสะอาดห้องน้ำ",
              "ใช้ในที่อากาศถ่ายเท และไม่ผสมกับน้ำยาล้างห้องน้ำชนิดอื่น เพราะอาจเกิดแก๊สพิษ",
              "ตวงใช้ตามปริมาณที่ฉลากกำหนด ไม่ใช้เกินความจำเป็น"),
    Guideline("บ้านของนักเรียนมีเทอร์โมมิเตอร์ปรอทแบบแก้วที่ตกแตก",
              "เปิดหน้าต่าง ไม่ใช้มือเปล่าหรือเครื่องดูดฝุ่น ใช้กระดาษแข็งกวาดปรอทใส่ภาชนะปิดแล้วทิ้งเป็นขยะอันตราย",
              "เปลี่ยนมาใช้เทอร์โมมิเตอร์แบบดิจิทัลที่ไม่มีปรอทและใช้ได้นาน"),
    Guideline("ร้านเชื่อมโลหะเกิดควันโลหะขณะทำงานทุกวัน",
              "สวมหน้ากากและแว่นป้องกัน และทำงานในที่อากาศถ่ายเท",
              "เก็บเศษโลหะที่เหลือจากงานเชื่อมขายให้ร้านรับซื้อเพื่อนำไปหลอมใช้ใหม่"),
    Guideline("สวนผักของโรงเรียนใช้ปุ๋ยเคมีที่มีไนโตรเจนและฟอสฟอรัส",
              "สวมถุงมือขณะใส่ปุ๋ยและเก็บปุ๋ยให้พ้นมือเด็ก",
              "ใส่ปุ๋ยตามปริมาณที่พืชต้องการ ไม่ใส่เกินจนไหลลงแหล่งน้ำ"),
)


def _guideline(safe: str, worthwhile: str) -> str:
    return f"ปลอดภัย: {safe} / คุ้มค่า: {worthwhile}"


GUIDELINE_SCENARIOS = (
    ("โรงเรียนหนึ่งคำนวณว่าการเปลี่ยนหลอดฟลูออเรสเซนต์ 100 หลอดเป็นหลอดแอลอีดีช่วยลดค่าไฟฟ้าได้ปีละ 20,000 บาท ถ้าหลอดแอลอีดีราคารวม 60,000 บาท จะคืนทุนภายในกี่ปี",
     "3 ปี",
     ("2 ปี", "6 ปี", "12 ปี", "4 ปี", "1 ปี")),
    ("นักเรียนเห็นว่าอะลูมิเนียมรีไซเคิลได้แทบไม่จำกัดครั้ง ข้อใดแสดงความตระหนักถึงคุณค่าของอะลูมิเนียมได้ดีที่สุด",
     "ชวนเพื่อนแยกกระป๋องอะลูมิเนียมออกจากขยะอื่นเพื่อส่งรีไซเคิล",
     ("ทิ้งกระป๋องรวมกับเศษอาหาร",
      "เผากระป๋องเพื่อลดปริมาณขยะ",
      "ฝังกระป๋องไว้ในดินหลังบ้าน",
      "ขายกระป๋องปนกับเศษอาหารโดยไม่แยก",
      "ใช้กระป๋องครั้งเดียวแล้วทิ้งลงคลอง")),
    ("ร้านซ่อมโทรศัพท์มีแผงวงจรเก่าที่มีทองแดงและทองคำปริมาณเล็กน้อย ข้อใดเป็นแนวทางที่ทั้งคุ้มค่าและปลอดภัย",
     "ส่งให้โรงงานรีไซเคิลที่ได้รับอนุญาตสกัดโลหะกลับมาใช้ใหม่",
     ("เผาแผงวงจรกลางแจ้งเพื่อเอาโลหะออก",
      "ทิ้งรวมกับขยะทั่วไปเพราะมีโลหะน้อย",
      "แช่แผงวงจรในกรดที่บ้านโดยไม่มีอุปกรณ์ป้องกัน",
      "ทุบแผงวงจรในห้องนอนเพื่อแยกทองคำ",
      "ขายแผงวงจรให้ผู้ที่นำไปเผาในที่โล่ง")),
)


def payback(rng: Random) -> GeneratedQuestion:
    """Lamp savings per year against their price; the years to pay back."""
    saving = rng.randrange(10_000, 40_001, 5_000)
    years = rng.randint(2, 6)
    cost = saving * years
    lamps = rng.choice((50, 80, 100, 120, 200))
    pool = (years + 1, years - 1, 2 * years, years + 2, lamps // 10)
    wrongs = tuple(dict.fromkeys(f"{w} ปี" for w in pool if w > 0 and w != years))
    return _labelled(
        stem=(f"โรงเรียนหนึ่งคำนวณว่าการเปลี่ยนหลอดฟลูออเรสเซนต์ {lamps} หลอดเป็นหลอดแอลอีดีช่วยลดค่าไฟฟ้าได้ปีละ {saving:,} บาท "
              f"ถ้าหลอดแอลอีดีราคารวม {cost:,} บาท จะคืนทุนภายในกี่ปี"),
        correct=f"{years} ปี",
        wrongs=wrongs,
        hint="จำนวนปีที่คืนทุน = ราคาหลอดทั้งหมด ÷ ค่าไฟฟ้าที่ลดลงต่อปี",
        topic=GUIDELINE_TOPIC,
    )


@question_type(
    "chem.element_safe_use_foundation",
    display_name={"th": "บอกวิธีใช้ผลิตภัณฑ์ที่มีธาตุอย่างปลอดภัย"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=GUIDELINE_TOPIC,
)
class ElementSafeUseFoundation(QuestionType):
    """A product containing an element; the safe way to handle it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(GUIDELINES))
        guide = GUIDELINES[index]
        others = [g for i, g in enumerate(GUIDELINES) if i != index]
        return _labelled(
            stem=f"{guide.case} ข้อใดเป็นการปฏิบัติที่ปลอดภัยที่สุด",
            correct=guide.safe,
            wrongs=tuple(g.safe for g in others),
            hint="หาอันตรายของธาตุในผลิตภัณฑ์นั้นก่อน แล้วเลือกวิธีที่ป้องกันอันตรายนั้นโดยตรง",
            topic=GUIDELINE_TOPIC,
        )


@question_type(
    "chem.element_safe_use_fluency",
    display_name={"th": "เสนอแนวทางการใช้ธาตุอย่างปลอดภัยและคุ้มค่า"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=GUIDELINE_TOPIC,
)
class ElementSafeUseFluency(QuestionType):
    """A case; the guideline that is safe and worthwhile at once."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(GUIDELINES))
        guide = GUIDELINES[index]
        first, second = rng.sample([g for i, g in enumerate(GUIDELINES) if i != index], 2)
        return _labelled(
            stem=f"{guide.case} ข้อใดเป็นแนวทางการใช้ธาตุที่ทั้งปลอดภัยและคุ้มค่าเหมาะสมที่สุด",
            correct=_guideline(guide.safe, guide.worthwhile),
            wrongs=(_guideline(first.safe, guide.worthwhile),
                    _guideline(guide.safe, first.worthwhile),
                    _guideline(second.safe, second.worthwhile)),
            hint="ตรวจทั้งสองส่วนว่าตรงกับสิ่งของในเรื่อง: ส่วนที่ป้องกันอันตราย และส่วนที่ใช้ธาตุให้คุ้มค่า",
            topic=GUIDELINE_TOPIC,
        )


@question_type(
    "chem.element_safe_use_application",
    display_name={"th": "ตัดสินใจใช้ธาตุอย่างคุ้มค่าและปลอดภัยในสถานการณ์จริง"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=GUIDELINE_TOPIC,
)
class ElementSafeUseApplication(QuestionType):
    """Payback on LED lamps, valuing aluminium, and old circuit boards."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return payback(rng)
        return _retopic(scenario_question(
            rng, GUIDELINE_SCENARIOS,
            hint="ชั่งทั้งความปลอดภัยต่อคนและสิ่งแวดล้อม กับความคุ้มค่าของทรัพยากรและเงิน",
        ), GUIDELINE_TOPIC)
