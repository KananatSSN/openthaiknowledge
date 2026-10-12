"""การตรึงคาร์บอนไดออกไซด์ในพืช C3 C4 และ CAM

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/11

Sets moved here from: science_wave_f57.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f57 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_C4 = "การตรึงคาร์บอนไดออกไซด์ในพืช C3 C4 และ CAM"


PLANT_TYPES = {
    "พืช C3": ("ข้าว", "ข้าวสาลี", "ถั่วเหลือง", "มะม่วง", "ทานตะวัน"),
    "พืช C4": ("ข้าวโพด", "อ้อย", "ข้าวฟ่าง", "หญ้าแพรก", "บานไม่รู้โรย"),
    "พืช CAM": ("สับปะรด", "กระบองเพชร", "ว่านหางจระเข้", "ศรนารายณ์", "กล้วยไม้บางชนิด"),
}


FEATURES = {
    "พืช C3": ("ตัวรับ CO₂ ตัวแรกคือ RuBP และได้ PGA ซึ่งมีคาร์บอน 3 อะตอมเป็นสารเสถียรตัวแรก",
               "เกิดโฟโตเรสไพเรชันได้มากเมื่ออากาศร้อนและปากใบปิด",
               "ตรึง CO₂ และสร้างน้ำตาลในเซลล์มีโซฟิลล์เพียงชนิดเดียว"),
    "พืช C4": ("ตรึง CO₂ ครั้งแรกด้วย PEP ในเซลล์มีโซฟิลล์ แล้วส่งต่อให้วัฏจักรคัลวินในเซลล์บันเดิลชีท",
               "มีเซลล์บันเดิลชีทที่มีคลอโรพลาสต์ล้อมรอบมัดท่อลำเลียงอย่างชัดเจน",
               "แยกขั้นตอนการตรึง CO₂ สองครั้งไว้คนละเซลล์ในเวลาเดียวกัน"),
    "พืช CAM": ("เปิดปากใบตอนกลางคืนเพื่อตรึง CO₂ เก็บไว้ในรูปกรดมาลิก",
               "น้ำในแวคิวโอลมีความเป็นกรดสูงในตอนเช้าและลดลงตอนเย็น",
               "แยกขั้นตอนการตรึง CO₂ สองครั้งไว้คนละเวลาในเซลล์เดียวกัน"),
}


C4_HINT = ("C3 ตรึง CO₂ ด้วยรูบิสโกได้ PGA C4 ตรึงด้วย PEP ในมีโซฟิลล์แล้วส่งไปบันเดิลชีท (แยกเซลล์) "
           "CAM ตรึงด้วย PEP ตอนกลางคืนเก็บเป็นกรดมาลิก แล้วเข้าวัฏจักรคัลวินตอนกลางวัน (แยกเวลา)")


C4_SCENARIOS = (
    ("ในวันที่อากาศร้อนและแห้ง พืชใดมักสังเคราะห์ด้วยแสงได้ดีกว่ากัน", "ข้าวโพด (C4) ดีกว่าข้าว (C3) เพราะเกิดโฟโตเรสไพเรชันน้อยกว่า",
     ("ข้าว (C3) ดีกว่าข้าวโพด (C4) เพราะใช้ ATP น้อยกว่า", "ทั้งสองดีเท่ากัน เพราะใช้วัฏจักรคัลวินเหมือนกันทุกประการ", "ข้าวโพดไม่สังเคราะห์ด้วยแสงในวันที่ร้อน")),
    ("เหตุใดพืช CAM จึงเหมาะกับที่แห้งแล้ง", "ปิดปากใบตอนกลางวันจึงสูญเสียน้ำน้อย แต่ยังตรึง CO₂ ได้ตอนกลางคืน",
     ("ไม่ต้องใช้ CO₂ ในการสังเคราะห์ด้วยแสง จึงปิดปากใบได้ตลอดวัน", "เปิดปากใบตลอดวันเพื่อรับน้ำจากอากาศ", "ไม่มีวัฏจักรคัลวิน จึงไม่ต้องเปิดปากใบรับ CO₂ เลยทั้งวัน")),
    ("โฟโตเรสไพเรชันเกิดขึ้นเมื่อใด", "รูบิสโกจับ O₂ แทน CO₂ เมื่อ O₂ ในใบสูงและ CO₂ ต่ำ เช่น เมื่อปากใบปิดในวันที่ร้อน",
     ("เมื่อพืชได้รับน้ำมากเกินไป", "รูบิสโกหยุดทำงานเมื่อพืชอยู่ในที่มืดสนิท และปากใบเปิดกว้างตลอดคืน", "รูบิสโกจับ CO₂ แทน O₂ เมื่อ CO₂ ในใบสูง เช่น เมื่อปากใบเปิดในวันที่เย็น")),
    ("วัดความเป็นกรดของน้ำคั้นจากใบสับปะรดตอนเช้าและตอนเย็น ผลควรเป็นอย่างไร", "ตอนเช้าเป็นกรดมากกว่า เพราะสะสมกรดมาลิกไว้ตลอดคืน",
     ("ตอนเย็นเป็นกรดมากกว่า เพราะสะสมกรดมาลิกตอนกลางวัน", "เท่ากันทั้งสองเวลา เพราะกรดมาลิกถูกใช้หมดทุกวัน", "ไม่เป็นกรดเลย เพราะพืชไม่สะสมกรดใดไว้ในเซลล์")),
)


@question_type(
    "biology.c4_cam_foundation",
    display_name={"th": "ตัวอย่างพืช C3 C4 และ CAM"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_C4,
)
class C4CamFoundation(QuestionType):
    """Which fixation pathway a plant uses."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(PLANT_TYPES))
        plant = rng.choice(PLANT_TYPES[kind])
        others = [k for k in PLANT_TYPES if k != kind]
        if rng.random() < 0.55:
            return _labelled(stem=f"{plant}จัดเป็นพืชกลุ่มใดตามกลไกการตรึง CO₂", correct=kind,
                             wrongs=(*others, "พืชที่ไม่ตรึง CO₂"), topic=TOPIC_C4, hint=C4_HINT)
        pool = [p for k in others for p in PLANT_TYPES[k]]
        return _labelled(stem=f"ข้อใดเป็น{kind}", correct=plant, wrongs=tuple(pool), topic=TOPIC_C4, hint=C4_HINT)


@question_type(
    "biology.c4_cam_fluency",
    display_name={"th": "เปรียบเทียบกลไกการตรึง CO₂ ของพืช C3 C4 และ CAM"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_C4,
)
class C4CamFluency(QuestionType):
    """Separate cells for C4, separate times for CAM."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(FEATURES))
        feature = rng.choice(FEATURES[kind])
        others = [k for k in FEATURES if k != kind]
        if rng.random() < 0.5:
            return _labelled(stem=f"พืชที่ \"{feature}\" คือพืชกลุ่มใด", correct=kind, wrongs=(*others, "พืชทุกกลุ่มเหมือนกัน"),
                             topic=TOPIC_C4, hint=C4_HINT)
        pool = [f for k in others for f in FEATURES[k]]
        return _labelled(stem=f"ข้อใดเป็นลักษณะของ{kind}", correct=feature, wrongs=tuple(pool), topic=TOPIC_C4,
                         hint=C4_HINT)


@question_type(
    "biology.c4_cam_application",
    display_name={"th": "วิเคราะห์ข้อได้เปรียบของพืช C4 และ CAM และพลังงานที่ใช้"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_C4,
)
class C4CamApplication(QuestionType):
    """Why the extra step pays in heat, and what it costs in ATP."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, right, wrongs = rng.choice(C4_SCENARIOS)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_C4, hint=C4_HINT)
        glucose = rng.randint(1, 25)
        c4 = rng.random() < 0.5
        per = 30 if c4 else 18
        kind = rng.choice(PLANT_TYPES["พืช C4" if c4 else "พืช C3"])
        return numeric(stem=f"{kind}เป็น{'พืช C4 ซึ่งใช้ ATP 5 โมเลกุล' if c4 else 'พืช C3 ซึ่งใช้ ATP 3 โมเลกุล'}ต่อการตรึง CO₂ 1 โมเลกุล "
                            f"การสร้างกลูโคส {glucose} โมเลกุลต้องใช้ ATP กี่โมเลกุล", answer=per * glucose,
                       wrongs=[(48 - per) * glucose, 5 * glucose if c4 else 3 * glucose, per * glucose // 6 * 2 + 1], unit="โมเลกุล",
                       topic=TOPIC_C4, hint="กลูโคส 1 โมเลกุลต้องตรึง CO₂ 6 โมเลกุล ATP ที่ใช้ = 6 × ATP ต่อ CO₂ × จำนวนกลูโคส")
