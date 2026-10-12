"""การลำเลียงอาหารในพืช

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/8

Sets moved here from: science_wave_f56.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f56 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_PHLOEM = "การลำเลียงอาหารในพืช"


PHLOEM_FACTS = (
    ("สมมติฐานการไหลของมวลสาร (pressure flow) อธิบายการลำเลียงอาหารอย่างไร",
     "น้ำตาลถูกลำเลียงเข้าซีฟทิวบ์ที่แหล่งสร้าง น้ำออสโมซิสตามเข้าไปเกิดแรงดัน ดันสารไปยังแหล่งใช้",
     ("อาหารเคลื่อนที่ลงด้วยแรงโน้มถ่วงเพียงอย่างเดียว", "น้ำตาลแพร่ผ่านไซเลมขึ้นสู่ยอด แล้วแรงดึงจากการคายน้ำดึงน้ำตาลไปยังทุกส่วนของพืช", "แรงดึงจากการคายน้ำที่ใบดึงน้ำตาลลงสู่ราก โดยน้ำไหลออกจากซีฟทิวบ์ไปยังไซเลม",
      "เซลล์ซีฟทิวบ์หดตัวบีบอาหารไปข้างหน้า")),
    ("สารอาหารส่วนใหญ่ที่ลำเลียงในโฟลเอ็มอยู่ในรูปใด", "ซูโครส (น้ำตาลโมเลกุลคู่)", ("กลูโคส (น้ำตาลโมเลกุลเดี่ยว)", "แป้ง", "เซลลูโลส", "กรดไขมัน")),
    ("การลำเลียงน้ำตาลเข้าสู่ซีฟทิวบ์ที่ใบต้องใช้อะไร", "พลังงานจาก ATP เพราะเป็นการลำเลียงแบบแอกทีฟทรานสปอร์ต",
     ("ไม่ต้องใช้พลังงานเลย เพราะเป็นการแพร่ธรรมดา", "พลังงานแสงที่ส่องถึงซีฟทิวบ์โดยตรง", "แรงดึงจากการคายน้ำ", "แรงดันรากเท่านั้น", "การแพร่แบบธรรมดาเท่านั้น")),
    ("การใช้เพลี้ยอ่อนศึกษาการลำเลียงอาหารทำได้อย่างไร", "ตัดปากเพลี้ยที่แทงอยู่ในโฟลเอ็มแล้วเก็บของเหลวที่ไหลออกมาวิเคราะห์",
     ("ให้เพลี้ยกินใบแล้วนับจำนวนใบที่หายไป", "วัดความเร็วของเพลี้ยที่เดินบนลำต้น", "ใช้เพลี้ยดูดน้ำจากไซเลม แล้ววัดปริมาณน้ำที่เพลี้ยดูดได้แต่ละวัน",
      "นับจำนวนเพลี้ยบนต้นแต่ละวัน แล้วเปรียบเทียบกับจำนวนใบที่เหี่ยว")),
    ("เซลล์ใดในโฟลเอ็มเป็นทางให้อาหารเคลื่อนที่ผ่าน", "ซีฟทิวบ์เมมเบอร์",
     ("เวสเซลเมมเบอร์", "เทรคีดเมมเบอร์", "เซลล์ไฟเบอร์", "เซลล์คุม")),
    ("ที่แหล่งใช้ เมื่อน้ำตาลถูกนำออกจากซีฟทิวบ์ จะเกิดอะไรขึ้น", "น้ำออสโมซิสออกจากซีฟทิวบ์ ความดันลดลง",
     ("น้ำออสโมซิสเข้าซีฟทิวบ์ ความดันเพิ่มขึ้น", "ซีฟทิวบ์สร้างน้ำตาลเพิ่ม ความดันจึงเพิ่มขึ้น", "น้ำตาลถูกดันเข้าไซเลม ความดันจึงลดลง", "ความดันในซีฟทิวบ์ไม่เปลี่ยน")),
    ("อาหารในโฟลเอ็มเคลื่อนที่ในทิศทางใด", "ได้ทั้งขึ้นและลง จากแหล่งสร้างไปยังแหล่งใช้",
     ("ขึ้นจากรากสู่ใบ ตามทิศทางการไหลของน้ำในไซเลม", "ลงจากใบสู่ราก ตามแรงโน้มถ่วงที่ดึงน้ำตาลลงมา", "ไม่มีทิศทางแน่นอนและไม่เคลื่อนที่", "ไปตามทิศของแรงลมเท่านั้น")),
)


SOURCES = ("ใบที่เจริญเต็มที่และสังเคราะห์ด้วยแสง", "หัวมันเทศที่กำลังงอกต้นใหม่", "ใบเลี้ยงของเมล็ดถั่วที่กำลังงอก",
           "รากแครอตที่สะสมอาหารแล้วเริ่มแทงช่อดอก")


SINKS = ("ผลมะม่วงอ่อนที่กำลังขยายขนาด", "ใบอ่อนที่ยังสังเคราะห์ด้วยแสงได้ไม่พอใช้", "ปลายรากที่กำลังยืดยาวลงในดิน", "หัวมันฝรั่งที่กำลังสะสมแป้งไว้",
         "ดอกไม้ที่กำลังบานและสร้างน้ำหวาน")


PHLOEM_HINT = "แหล่งสร้าง (source) ส่งน้ำตาลออก เช่น ใบที่โตเต็มที่ แหล่งใช้ (sink) รับน้ำตาล เช่น ผล ราก ยอดอ่อน อวัยวะสะสมอาหาร"


@question_type(
    "biology.food_transport_foundation",
    display_name={"th": "กลไกการลำเลียงอาหารทางโฟลเอ็ม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PHLOEM,
)
class FoodTransportFoundation(QuestionType):
    """Pressure flow, sucrose, and the aphid method."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(PHLOEM_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_PHLOEM, hint=PHLOEM_HINT)


@question_type(
    "biology.food_transport_fluency",
    display_name={"th": "แหล่งสร้างและแหล่งใช้อาหารในพืช"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PHLOEM,
)
class FoodTransportFluency(QuestionType):
    """Source or sink, by whether the organ exports or imports sugar now."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        source = rng.random() < 0.5
        if rng.random() < 0.5:
            organ = rng.choice(SOURCES if source else SINKS)
            return _labelled(stem=f"{organ}ทำหน้าที่อะไรในการลำเลียงอาหาร", correct="แหล่งสร้าง (source)" if source else "แหล่งใช้ (sink)",
                             wrongs=("แหล่งใช้ (sink)" if source else "แหล่งสร้าง (source)", "ไม่เกี่ยวข้องกับการลำเลียงอาหาร",
                                     "ทางลำเลียงน้ำในไซเลม"), topic=TOPIC_PHLOEM, hint=PHLOEM_HINT)
        right, wrong = (SOURCES, SINKS) if source else (SINKS, SOURCES)
        return _labelled(stem=f"ข้อใดทำหน้าที่เป็น{'แหล่งสร้าง (source)' if source else 'แหล่งใช้ (sink)'}ของน้ำตาล",
                         correct=rng.choice(right), wrongs=tuple(wrong), topic=TOPIC_PHLOEM, hint=PHLOEM_HINT)


@question_type(
    "biology.food_transport_application",
    display_name={"th": "ผลการทดลองควั่นเปลือกและอัตราการลำเลียงอาหาร"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PHLOEM,
)
class FoodTransportApplication(QuestionType):
    """Ringing removes the phloem; tracer arrival gives the speed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            cases = (
                ("ควั่นเปลือกลำต้นไม้ยืนต้นออกเป็นวงรอบ ทิ้งไว้ระยะหนึ่ง เปลือกเหนือรอยควั่นจะเป็นอย่างไร",
                 "บวมพองขึ้น เพราะอาหารที่ลำเลียงลงมาทางโฟลเอ็มสะสมอยู่เหนือรอยควั่น",
                 ("เหี่ยวทันที เพราะน้ำขึ้นไปไม่ได้", "ไม่เปลี่ยนแปลง เพราะโฟลเอ็มอยู่ในเนื้อไม้", "บวมพองใต้รอยควั่น เพราะน้ำสะสม")),
                ("หลังควั่นเปลือกรอบลำต้น ใบเหนือรอยควั่นยังสดอยู่ได้ระยะหนึ่งเพราะเหตุใด", "ไซเลมอยู่ในเนื้อไม้ยังไม่ถูกตัด น้ำจึงขึ้นไปได้",
                 ("โฟลเอ็มยังลำเลียงน้ำขึ้นไปได้", "ใบสร้างน้ำขึ้นเองได้", "รากหยุดดูดน้ำ")),
                ("ถ้าควั่นเปลือกรอบลำต้นทิ้งไว้นานหลายเดือน ต้นไม้มักตายเพราะเหตุใด", "รากไม่ได้รับอาหารจากใบจนตาย แล้วไม่สามารถดูดน้ำได้",
                 ("ใบได้รับน้ำมากเกินไป", "ไซเลมถูกตัดขาดทันที", "ลำต้นสังเคราะห์ด้วยแสงมากเกินไป")),
            )
            stem, right, wrongs = rng.choice(cases)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_PHLOEM,
                             hint="การควั่นเปลือกตัดโฟลเอ็มซึ่งอยู่ในเปลือก แต่ไซเลมอยู่ในเนื้อไม้ยังลำเลียงน้ำได้")
        while True:
            speed = rng.choice((20, 25, 30, 40, 50, 60, 75, 80, 100))
            minutes = rng.choice((6, 12, 15, 20, 30, 45))
            distance = Fraction(speed * minutes, 60)
            if (distance * 100).denominator == 1:
                break
        plant = rng.choice(("ต้นถั่ว", "ต้นทานตะวัน", "ต้นอ้อย", "ต้นมะเขือเทศ"))
        if rng.random() < 0.5:
            return numeric(stem=f"ให้ใบ{plant}ได้รับ ¹⁴CO₂ แล้วพบน้ำตาลที่มี ¹⁴C ในโฟลเอ็มห่างจากใบ {show(distance)} cm หลังผ่านไป {minutes} นาที "
                                f"อัตราการลำเลียงอาหารเป็นกี่เซนติเมตรต่อชั่วโมง", answer=speed,
                           wrongs=[distance / minutes if (distance / minutes * 100).denominator == 1 else speed * 2, distance, speed / 2],
                           unit="cm ต่อชั่วโมง", topic=TOPIC_PHLOEM, hint="แปลงนาทีเป็นชั่วโมงแล้วหาร: อัตรา = ระยะทาง ÷ เวลา (ชั่วโมง)")
        return numeric(stem=f"อาหารในโฟลเอ็มของ{plant}เคลื่อนที่ด้วยอัตรา {speed} cm ต่อชั่วโมง ใน {minutes} นาทีจะเคลื่อนที่ได้กี่เซนติเมตร",
                       answer=distance, wrongs=[speed * minutes, speed, distance * 2], unit="cm", topic=TOPIC_PHLOEM,
                       hint="ระยะทาง = อัตรา × เวลา (ชั่วโมง) เวลา = นาที ÷ 60")
