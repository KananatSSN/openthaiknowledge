"""การระบุปัญหา สมมติฐาน และการออกแบบการทดลอง

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/2

Sets moved here from: science_wave_f44.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f44 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_METHOD = "การระบุปัญหา สมมติฐาน และการออกแบบการทดลอง"


# (question studied, independent, dependent, controlled, hypothesis)
EXPERIMENTS = (
    ("อุณหภูมิมีผลต่อการงอกของเมล็ดถั่วเขียวหรือไม่", "อุณหภูมิ", "จำนวนเมล็ดที่งอก",
     "ชนิดและจำนวนเมล็ด ปริมาณน้ำ", "ถ้าอุณหภูมิสูงขึ้นถึงระดับหนึ่ง เมล็ดจะงอกได้มากขึ้น"),
    ("ความเข้มแสงมีผลต่ออัตราการสังเคราะห์ด้วยแสงของสาหร่ายหรือไม่", "ความเข้มแสง", "จำนวนฟองแก๊สที่เกิดต่อนาที",
     "ชนิดสาหร่าย อุณหภูมิของน้ำ", "ถ้าความเข้มแสงมากขึ้น สาหร่ายจะเกิดฟองแก๊สมากขึ้น"),
    ("ความเข้มข้นของสารละลายน้ำตาลมีผลต่อมวลของชิ้นมันฝรั่งหรือไม่", "ความเข้มข้นของสารละลายน้ำตาล", "มวลที่เปลี่ยนไปของชิ้นมันฝรั่ง",
     "ขนาดชิ้นมันฝรั่ง เวลาที่แช่", "ถ้าสารละลายเข้มข้นมากขึ้น ชิ้นมันฝรั่งจะมีมวลลดลงมากขึ้น"),
    ("pH มีผลต่อการทำงานของเอนไซม์อะไมเลสหรือไม่", "pH ของสารละลาย", "เวลาที่แป้งถูกย่อยหมด",
     "ปริมาณแป้งและเอนไซม์ อุณหภูมิ", "ถ้า pH ใกล้ค่าที่เหมาะสม เอนไซม์จะย่อยแป้งได้เร็วที่สุด"),
    ("ชนิดของปุ๋ยมีผลต่อความสูงของต้นข้าวโพดหรือไม่", "ชนิดของปุ๋ย", "ความสูงของต้นข้าวโพด",
     "ปริมาณน้ำ แสง ชนิดดิน", "ถ้าใช้ปุ๋ยที่มีไนโตรเจนมาก ต้นข้าวโพดจะสูงกว่า"),
    ("การออกกำลังกายมีผลต่ออัตราการเต้นของหัวใจหรือไม่", "ระยะเวลาการออกกำลังกาย", "อัตราการเต้นของหัวใจ",
     "ชนิดการออกกำลังกาย อายุของผู้ทดลอง", "ถ้าออกกำลังกายนานขึ้น อัตราการเต้นของหัวใจจะเพิ่มขึ้น"),
    ("ปริมาณน้ำที่รดมีผลต่อการเจริญของต้นผักบุ้งหรือไม่", "ปริมาณน้ำที่รดต่อวัน", "ความยาวของต้นผักบุ้ง",
     "ชนิดดิน แสง อุณหภูมิ", "ถ้ารดน้ำมากขึ้นถึงระดับหนึ่ง ต้นผักบุ้งจะยาวขึ้น"),
    ("อุณหภูมิมีผลต่อการหมักของยีสต์หรือไม่", "อุณหภูมิ", "ปริมาตรแก๊ส CO₂ ที่เกิดขึ้น",
     "ปริมาณยีสต์และน้ำตาล เวลา", "ถ้าอุณหภูมิเหมาะสม ยีสต์จะผลิตแก๊ส CO₂ ได้มากที่สุด"),
)


ROLES = {"ตัวแปรต้น": 1, "ตัวแปรตาม": 2, "ตัวแปรควบคุม": 3}


@question_type(
    "biology.scientific_method_foundation",
    display_name={"th": "ระบุตัวแปรในการทดลอง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_METHOD,
)
class ScientificMethodFoundation(QuestionType):
    """What is changed, what is measured, and what is kept the same."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        exp = rng.choice(EXPERIMENTS)
        role, index = rng.choice(list(ROLES.items()))
        right = exp[index]
        others = [exp[i] for i in (1, 2, 3) if i != index]
        pool = [e[i] for e in EXPERIMENTS if e is not exp for i in (1, 2, 3) if e[i] not in (right, *others)]
        return _labelled(stem=f"การทดลองเพื่อตอบปัญหา \"{exp[0]}\" ข้อใดเป็น{role}", correct=right,
                         wrongs=(*others, rng.choice(pool)), topic=TOPIC_METHOD,
                         hint="ตัวแปรต้นคือสิ่งที่เปลี่ยน ตัวแปรตามคือผลที่วัด ตัวแปรควบคุมคือสิ่งที่ต้องคงที่")


@question_type(
    "biology.scientific_method_fluency",
    display_name={"th": "สมมติฐานที่สอดคล้องกับปัญหา"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_METHOD,
)
class ScientificMethodFluency(QuestionType):
    """A hypothesis links the variable changed to the result expected, and can be tested."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        exp = rng.choice(EXPERIMENTS)
        others = [e[4] for e in EXPERIMENTS if e is not exp]
        if rng.random() < 0.6:
            return _labelled(stem=f"ปัญหา \"{exp[0]}\" สมมติฐานใดเหมาะสมที่สุด", correct=exp[4],
                             wrongs=tuple(others), topic=TOPIC_METHOD,
                             hint="สมมติฐานที่ดีเชื่อมตัวแปรต้นกับตัวแปรตามของปัญหานั้น และตรวจสอบได้ด้วยการทดลอง")
        return _labelled(stem=f"สมมติฐาน \"{exp[4]}\" ตรงกับปัญหาใด", correct=exp[0],
                         wrongs=tuple([e[0] for e in EXPERIMENTS if e is not exp]), topic=TOPIC_METHOD,
                         hint="ดูว่าสมมติฐานพูดถึงตัวแปรใดเป็นเหตุและผล")


@question_type(
    "biology.scientific_method_application",
    display_name={"th": "ออกแบบการทดลองที่ยุติธรรมและมีชุดควบคุม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_METHOD,
)
class ScientificMethodApplication(QuestionType):
    """Change only one thing; keep a control; repeat to trust the result."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        exp = rng.choice(EXPERIMENTS)
        facts = (
            (f"ในการทดลองเรื่อง \"{exp[0]}\" เพราะเหตุใดจึงต้องควบคุม{exp[3]}ให้เหมือนกัน",
             f"เพื่อให้ผลที่เปลี่ยนไปเกิดจาก{exp[1]}เพียงอย่างเดียว",
             ("เพื่อให้ได้ผลการทดลองเร็วขึ้นและใช้เวลาน้อยลง", "เพื่อให้ใช้อุปกรณ์น้อยลงและประหยัดสารเคมี",
              f"เพื่อให้{exp[2]}มีค่าเท่ากันทุกชุดไม่ว่าตัวแปรต้นเป็นเท่าใด")),
            (f"ในการทดลองเรื่อง \"{exp[0]}\" เพราะเหตุใดจึงต้องทำการทดลองซ้ำหลายครั้ง",
             "เพื่อให้ผลน่าเชื่อถือมากขึ้นและลดความคลาดเคลื่อนโดยบังเอิญ",
             ("เพื่อพิสูจน์ว่าสมมติฐานถูกเสมอ แม้ผลบางครั้งจะไม่ตรง", "เพื่อเปลี่ยนตัวแปรต้นหลายตัวพร้อมกันในแต่ละครั้ง", "เพื่อไม่ต้องบันทึกผลทุกครั้งที่ทดลอง")),
            (f"ในการทดลองเรื่อง \"{exp[0]}\" ชุดควบคุมมีไว้เพื่ออะไร",
             "เป็นชุดเปรียบเทียบที่ไม่เปลี่ยนตัวแปรต้น เพื่อดูว่าผลเกิดจากตัวแปรต้นจริง",
             ("เพื่อเพิ่มจำนวนตัวแปรต้นให้เปรียบเทียบได้หลายค่าพร้อมกันในครั้งเดียว", "เพื่อให้ได้ผลตามสมมติฐานเสมอ แม้ตัวแปรต้นจะไม่มีผล", "เพื่อแทนการบันทึกข้อมูลของชุดทดลอง")),
            (f"ผลการทดลองเรื่อง \"{exp[0]}\" ไม่เป็นไปตามสมมติฐาน ควรทำอย่างไร",
             "ตรวจสอบวิธีทดลองและข้อมูล แล้วยอมรับผลหรือตั้งสมมติฐานใหม่เพื่อทดสอบต่อ",
             ("แก้ตัวเลขให้ตรงกับสมมติฐาน แล้วสรุปว่าสมมติฐานถูกต้อง", "ทิ้งผลการทดลองทั้งหมดโดยไม่บันทึก แล้วทดลองใหม่จนได้ผลตามที่คาดไว้", "สรุปว่าสมมติฐานถูกต้องอยู่ดี แล้วตัดข้อมูลที่ไม่ตรงออก")),
        )
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_METHOD,
                         hint="การทดลองที่ดีเปลี่ยนตัวแปรต้นเพียงตัวเดียว มีชุดควบคุม และทำซ้ำ")
