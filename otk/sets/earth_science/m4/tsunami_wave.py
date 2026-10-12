"""สึนามิ

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/7

Sets moved here from: science_wave_f76.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f76 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_TSUNAMI = "สึนามิ"


TSUNAMI_FACTS = (
    ("สาเหตุที่พบบ่อยที่สุดของสึนามิคืออะไร", "แผ่นดินไหวใต้ทะเลที่ทำให้พื้นทะเลยกตัวหรือยุบตัวในแนวดิ่ง",
     ("พายุหมุนเขตร้อนที่พัดผ่านทะเลเป็นเวลานาน", "น้ำขึ้นน้ำลงตามปกติที่สูงกว่าทุกวัน", "ลมมรสุมพัดแรงจนน้ำทะเลยกตัวสูงเป็นคลื่นยักษ์ในแนวดิ่ง", "กระแสน้ำอุ่นในมหาสมุทร")),
    ("สึนามิในทะเลลึกต่างจากเมื่อเข้าใกล้ชายฝั่งอย่างไร", "ในทะเลลึกคลื่นเร็วแต่เตี้ย เมื่อถึงที่ตื้นคลื่นช้าลงและสูงขึ้นมาก",
     ("ในทะเลลึกคลื่นสูงมาก เมื่อถึงฝั่งคลื่นเตี้ยลง", "ความเร็วเท่ากันตลอด", "ในทะเลลึกไม่มีคลื่นเลย คลื่นเกิดขึ้นเฉพาะเมื่อถึงชายฝั่งที่ตื้น", "คลื่นหายไปก่อนถึงฝั่งเสมอเพราะพลังงานหมดกลางทะเล")),
    ("สัญญาณเตือนตามธรรมชาติก่อนสึนามิมาถึงคือข้อใด", "น้ำทะเลลดลงอย่างรวดเร็วผิดปกติจนเห็นพื้นทะเล",
     ("ฝนตกหนักฉับพลัน", "ท้องฟ้ามีเมฆมาก", "น้ำทะเลอุ่นขึ้นเล็กน้อย", "คลื่นลมสงบกว่าปกติทุกครั้ง")),
    ("เมื่อได้รับการเตือนภัยสึนามิ ควรปฏิบัติอย่างไร", "รีบอพยพขึ้นที่สูงหรืออาคารสูงที่แข็งแรงตามเส้นทางอพยพ",
     ("ลงไปดูน้ำทะเลที่ลดลง", "อยู่ที่ชายหาดรอดูคลื่นเพื่อดูว่าคลื่นสูงแค่ไหนก่อนหนี", "หลบในห้องใต้ดินริมทะเลที่มีประตูปิดมิดชิด", "ขับเรือเข้าหาฝั่งให้เร็วที่สุดเพื่อหนีคลื่น")),
    ("เหตุใดสึนามิมักเป็นคลื่นหลายลูกต่อเนื่องกัน", "พื้นทะเลที่เปลี่ยนไปทำให้เกิดคลื่นยาวหลายลูก และลูกหลังอาจใหญ่กว่า",
     ("เพราะลมพัดคลื่นตามกันมาเป็นระลอกจากกลางทะเล", "มีคลื่นเพียงลูกเดียวเสมอ แต่สะท้อนไปมาระหว่างเกาะจนดูเหมือนหลายลูก", "คลื่นสะท้อนจากดวงจันทร์กลับมาที่ชายฝั่งหลายครั้ง", "เพราะเรือแล่นผ่าน")),
)


TSUNAMI_HINT = ("สึนามิเกิดจากการยกหรือยุบตัวของพื้นทะเลอย่างฉับพลัน ในทะเลลึกเคลื่อนที่เร็วตามสูตร v = √(g d) "
                "เมื่อถึงที่ตื้นช้าลงและสูงขึ้น เห็นน้ำลดผิดปกติให้รีบขึ้นที่สูง")


@question_type(
    "geo.tsunami_wave_foundation",
    display_name={"th": "สาเหตุ ลักษณะ และการปฏิบัติตนเมื่อเกิดสึนามิ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TSUNAMI,
)
class TsunamiWaveFoundation(QuestionType):
    """Causes, behaviour near shore, warning signs and safety."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(TSUNAMI_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_TSUNAMI, hint=TSUNAMI_HINT)


@question_type(
    "geo.tsunami_wave_fluency",
    display_name={"th": "พื้นที่เสี่ยงและเหตุการณ์ที่ทำให้เกิดสึนามิ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TSUNAMI,
)
class TsunamiWaveFluency(QuestionType):
    """Which events can raise a tsunami, and which places are at risk."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        can = ("แผ่นดินไหวขนาดใหญ่ที่แนวมุดตัวใต้ทะเล", "ภูเขาไฟใต้ทะเลระเบิด", "ดินถล่มขนาดใหญ่ลงสู่ทะเล", "อุกกาบาตขนาดใหญ่ตกลงมหาสมุทร")
        cannot = ("ลมมรสุมตะวันตกเฉียงใต้", "น้ำขึ้นน้ำลงรายวัน", "แผ่นดินไหวขนาดเล็กกลางทวีป", "ฝนตกหนักหลายวัน")
        if rng.random() < 0.6:
            yes = rng.random() < 0.5
            right, wrong = (can, cannot) if yes else (cannot, can)
            return _labelled(stem=f"เหตุการณ์ใด{'อาจทำให้เกิด' if yes else 'ไม่ทำให้เกิด'}สึนามิ", correct=rng.choice(right),
                             wrongs=tuple(wrong), topic=TOPIC_TSUNAMI, hint=TSUNAMI_HINT)
        risky = ("ชายฝั่งทะเลอันดามันของไทย เช่น ภูเก็ตและพังงา", "ชายฝั่งประเทศญี่ปุ่น", "ชายฝั่งประเทศชิลี", "ชายฝั่งเกาะสุมาตรา")
        safe = ("ที่ราบภาคกลางห่างทะเลหลายร้อยกิโลเมตร", "ยอดดอยสูงในภาคเหนือ", "ทะเลสาบกลางทวีปเล็ก ๆ ที่ไม่มีรอยเลื่อน")
        return _labelled(stem="พื้นที่ใดเสี่ยงต่อสึนามิมากที่สุด", correct=rng.choice(risky), wrongs=tuple(safe), topic=TOPIC_TSUNAMI,
                         hint="พื้นที่เสี่ยงคือชายฝั่งที่หันเข้าหาแนวมุดตัวของแผ่นธรณี เช่น ชายฝั่งอันดามันซึ่งหันเข้าหาร่องลึกซุนดา")


@question_type(
    "geo.tsunami_wave_application",
    display_name={"th": "คำนวณความเร็วและเวลาเดินทางของสึนามิ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TSUNAMI,
)
class TsunamiWaveApplication(QuestionType):
    """v = √(g d) in deep water; time = distance ÷ speed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        speed = rng.choice((30, 40, 50, 60, 70, 80, 90, 100, 120, 150, 200, 250))  # m/s
        depth = speed * speed // 10
        if rng.random() < 0.5:
            return numeric(stem=f"สึนามิเคลื่อนที่ในทะเลลึก {depth:,} m ด้วยอัตราเร็ว v = √(g d) เมื่อ g = 10 m/s² อัตราเร็วเป็นกี่เมตรต่อวินาที",
                           answer=speed, wrongs=[depth // 10, speed * 10, speed // 2], unit="m/s", topic=TOPIC_TSUNAMI, hint=TSUNAMI_HINT)
        km_h = speed * Fraction(36, 10)
        distance = km_h * rng.choice((Fraction(1, 2), 1, 2, 3))
        hours = distance / km_h
        return numeric(stem=f"สึนามิเคลื่อนที่ด้วยอัตราเร็ว {speed} m/s (เท่ากับ {show(km_h)} km/h) จากจุดเกิดถึงชายฝั่งระยะ {show(distance)} km ใช้เวลากี่ชั่วโมง",
                       answer=hours, wrongs=[distance / speed if (distance / speed * 100).denominator == 1 else hours * 2, hours * 60, hours + 1],
                       unit="ชั่วโมง", topic=TOPIC_TSUNAMI, hint="เวลา = ระยะทาง ÷ อัตราเร็ว (ใช้หน่วย km และ km/h)")
