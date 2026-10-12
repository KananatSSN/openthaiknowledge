"""การใช้เชื้อเพลิงซากดึกดำบรรพ์อย่างรู้คุณค่า

ธรณีวิทยา · ม.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.2/2

Sets moved here from: science_wave_c19.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b8 import LEVEL as MIDDLE_TWO
from otk.sets._support.science_wave_b9 import Care, Need, care_fluency, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c19 import FUEL_USE_SCENARIOS

PROVENANCE = Provenance("original")


FUEL_USE_TOPIC = "การใช้เชื้อเพลิงซากดึกดำบรรพ์อย่างรู้คุณค่า"


FUEL_CARE = (
    Care("ใช้รถโดยสารสาธารณะหรือเดินทางร่วมกันแทนการขับรถยนต์คนละคัน",
         "รถที่วิ่งน้อยลงใช้น้ำมันน้อยลง จึงช่วยให้น้ำมันที่มีจำกัดใช้ได้นานขึ้นและลดมลพิษ"),
    Care("ตรวจเช็กเครื่องยนต์และเติมลมยางให้เหมาะสมอยู่เสมอ",
         "เครื่องยนต์ที่เผาไหม้สมบูรณ์และยางที่ลมพอดีทำให้สิ้นเปลืองน้ำมันน้อยลง"),
    Care("ปิดเครื่องใช้ไฟฟ้าเมื่อไม่ใช้และเลือกเครื่องใช้ไฟฟ้าประหยัดพลังงาน",
         "ไฟฟ้าส่วนใหญ่ผลิตจากแก๊สธรรมชาติและถ่านหิน ใช้ไฟฟ้าน้อยลงจึงเผาเชื้อเพลิงน้อยลง"),
    Care("ปิดวาล์วถังแก๊สหุงต้มหลังใช้และใช้ภาชนะที่เหมาะกับขนาดเตา",
         "แก๊สไม่รั่วไหลทิ้งและความร้อนไม่สูญเปล่ารอบภาชนะ"),
    Care("ดับเครื่องยนต์ทุกครั้งเมื่อจอดรอเป็นเวลานาน",
         "เครื่องยนต์ที่ติดทิ้งไว้เผาน้ำมันตลอดเวลาแม้รถไม่ได้เคลื่อนที่"),
    Care("วางแผนเส้นทางให้ทำธุระหลายอย่างในการเดินทางครั้งเดียว",
         "ระยะทางรวมที่ขับสั้นลงทำให้ใช้น้ำมันน้อยลง"),
)


FUEL_NEEDS = (
    Need("พนักงานในบริษัทเดียวกันห้าคนบ้านอยู่ซอยเดียวกัน แต่ต่างคนต่างขับรถยนต์มาทำงานทุกวัน "
         "ควรเสนอแนวทางใดที่ตรงกับปัญหาที่สุด",
         "ใช้รถโดยสารสาธารณะหรือเดินทางร่วมกันแทนการขับรถยนต์คนละคัน"),
    Need("รถของครอบครัวกินน้ำมันมากกว่าเดิม ยางดูแบนและไม่ได้เข้ารับการตรวจเช็กมานาน "
         "ควรเสนอแนวทางใดที่ตรงกับปัญหาที่สุด",
         "ตรวจเช็กเครื่องยนต์และเติมลมยางให้เหมาะสมอยู่เสมอ"),
    Need("ค่าไฟฟ้าของโรงเรียนสูงขึ้นมาก เพราะเปิดเครื่องปรับอากาศและคอมพิวเตอร์ทิ้งไว้หลังเลิกเรียน "
         "ควรเสนอแนวทางใดที่ตรงกับปัญหาที่สุด",
         "ปิดเครื่องใช้ไฟฟ้าเมื่อไม่ใช้และเลือกเครื่องใช้ไฟฟ้าประหยัดพลังงาน"),
    Need("แก๊สหุงต้มของร้านอาหารหมดเร็วผิดปกติ เพราะเปิดวาล์วถังค้างไว้และใช้หม้อใบเล็กบนเตาหัวใหญ่ "
         "ควรเสนอแนวทางใดที่ตรงกับปัญหาที่สุด",
         "ปิดวาล์วถังแก๊สหุงต้มหลังใช้และใช้ภาชนะที่เหมาะกับขนาดเตา"),
    Need("ผู้ปกครองหลายคนจอดรถรอรับลูกหน้าโรงเรียนนานครึ่งชั่วโมงโดยติดเครื่องยนต์ไว้ "
         "ควรเสนอแนวทางใดที่ตรงกับปัญหาที่สุด",
         "ดับเครื่องยนต์ทุกครั้งเมื่อจอดรอเป็นเวลานาน"),
    Need("ครอบครัวหนึ่งขับรถเข้าเมืองวันละหลายรอบ รอบละธุระเดียว เช่น ซื้อของ จ่ายค่าไฟ และรับพัสดุ "
         "ควรเสนอแนวทางใดที่ตรงกับปัญหาที่สุด",
         "วางแผนเส้นทางให้ทำธุระหลายอย่างในการเดินทางครั้งเดียว"),
)


@question_type(
    "geo.fuel_saving_foundation",
    display_name={"th": "เหตุผลของแนวทางใช้เชื้อเพลิงอย่างรู้คุณค่า"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=FUEL_USE_TOPIC,
)
class FuelSavingFoundation(QuestionType):
    """Match a practice to why it stretches fossil fuel, in either direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(FUEL_CARE)
        others = [other for other in FUEL_CARE if other.practice != item.practice]
        if rng.random() < 0.5:
            return _labelled(
                stem=f"การ“{item.practice}” ช่วยให้ใช้เชื้อเพลิงซากดึกดำบรรพ์อย่างรู้คุณค่าได้อย่างไร",
                correct=item.reason,
                wrongs=tuple(other.reason for other in others),
                hint="นึกว่าการกระทำนั้นลดการเผาเชื้อเพลิงชนิดใดลง",
                topic=FUEL_USE_TOPIC,
            )
        return _labelled(
            stem=f"แนวทางใดช่วยประหยัดเชื้อเพลิง โดยอาศัยเหตุผลที่ว่า{item.reason}",
            correct=item.practice,
            wrongs=tuple(other.practice for other in others),
            hint="นึกว่าการกระทำนั้นลดการเผาเชื้อเพลิงชนิดใดลง",
            topic=FUEL_USE_TOPIC,
        )


@question_type(
    "geo.fuel_saving_fluency",
    display_name={"th": "เสนอแนวทางใช้เชื้อเพลิงซากดึกดำบรรพ์ให้ตรงกับปัญหา"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=FUEL_USE_TOPIC,
)
class FuelSavingFluency(QuestionType):
    """Put forward the practice that fits a case — the indicator's own clause."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_fluency(
            rng, needs=FUEL_NEEDS, cares=FUEL_CARE,
            hint="หาว่าเชื้อเพลิงในเรื่องสิ้นเปลืองไปเพราะอะไร แล้วเลือกแนวทางที่แก้สาเหตุนั้น",
        ), FUEL_USE_TOPIC)


@question_type(
    "geo.fuel_saving_application",
    display_name={"th": "วางแผนลดการพึ่งพาเชื้อเพลิงซากดึกดำบรรพ์"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=FUEL_USE_TOPIC,
)
class FuelSavingApplication(QuestionType):
    """The national value of saving, measuring a campaign, and a long-term plan."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, FUEL_USE_SCENARIOS,
            hint="นึกว่าแนวทางนั้นลดการใช้เชื้อเพลิงได้จริงและยั่งยืนหรือไม่",
        ), FUEL_USE_TOPIC)
