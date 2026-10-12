"""โครงสร้างแลกเปลี่ยนแก๊สของสัตว์

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/4

Sets moved here from: science_wave_f60.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f60 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_ANIMAL = "โครงสร้างแลกเปลี่ยนแก๊สของสัตว์"


ANIMALS = (
    ("ฟองน้ำ", "เซลล์ทุกเซลล์แลกเปลี่ยนแก๊สกับน้ำที่ไหลผ่านโดยตรงด้วยการแพร่"),
    ("ไฮดรา", "เซลล์ผิวลำตัวทั้งชั้นนอกและชั้นในแลกเปลี่ยนแก๊สกับน้ำโดยตรง"),
    ("พลานาเรีย", "ลำตัวแบนบางทำให้แก๊สแพร่ผ่านผิวลำตัวถึงทุกเซลล์ได้"),
    ("ไส้เดือนดิน", "ผิวหนังที่ชื้นและมีหลอดเลือดฝอยมาก"),
    ("แมลง", "ระบบท่อลมที่มีรูหายใจ (สไปเรเคิล) นำอากาศถึงเซลล์โดยตรง"),
    ("ปลา", "เหงือกที่เลือดไหลสวนทางกับน้ำ"),
    ("นก", "ปอดที่ทำงานร่วมกับถุงลม ทำให้อากาศไหลผ่านปอดทางเดียว"),
    ("กบตัวเต็มวัย", "ปอดร่วมกับผิวหนังที่ชุ่มชื้น"),
)


ANIMAL_HINT = ("สัตว์ขนาดเล็กหรือแบนใช้การแพร่ผ่านผิว ไส้เดือนใช้ผิวหนังชื้น แมลงใช้ท่อลม ปลาใช้เหงือกแบบสวนทาง "
               "นกใช้ปอดกับถุงลม กบใช้ปอดและผิวหนัง")


ANIMAL_FACTS = (
    ("เหตุใดไส้เดือนดินจึงต้องอาศัยในที่ชื้น", "แก๊สต้องละลายในความชื้นที่ผิวหนังก่อนจึงแพร่ผ่านได้",
     ("ผิวหนังต้องใช้น้ำในการสร้างอาหารให้ไส้เดือนดิน", "ไส้เดือนดินหายใจด้วยเหงือก", "ความชื้นที่ผิวหนังมีออกซิเจนมากกว่าในอากาศรอบตัว", "ไส้เดือนดินไม่มีหลอดเลือด")),
    ("ระบบท่อลมของแมลงแตกต่างจากระบบหายใจของสัตว์อื่นอย่างไร", "นำ O₂ ถึงเซลล์โดยตรง เลือดแทบไม่ได้ขนส่ง O₂",
     ("ใช้เลือดขนส่ง O₂ ไปยังเซลล์ทั้งหมดเช่นเดียวกับคน", "แลกเปลี่ยนแก๊สที่เหงือก", "ไม่ต้องมีรูหายใจ", "ใช้ผิวหนังชื้นเป็นอวัยวะแลกเปลี่ยนแก๊สหลัก")),
    ("การไหลแบบสวนทางของน้ำกับเลือดในเหงือกปลามีประโยชน์อย่างไร", "ทำให้ความเข้มข้นของ O₂ ในน้ำสูงกว่าในเลือดตลอดแนว จึงแพร่ได้มาก",
     ("ทำให้น้ำไหลช้าลงจนหยุด", "ทำให้เลือดและน้ำไม่ต้องสัมผัสกัน O₂ จึงผ่านเข้าเลือดได้โดยตรง", "ทำให้ปลาไม่ต้องใช้พลังงานในการเคลื่อนน้ำผ่านเหงือกเลย", "ทำให้ CO₂ เข้าสู่เลือด")),
    ("ถุงลมของนกมีบทบาทอย่างไร", "ทำให้อากาศไหลผ่านปอดทางเดียวตลอดทั้งหายใจเข้าและออก",
     ("เป็นที่แลกเปลี่ยนแก๊สหลักแทนปอดที่มีขนาดเล็ก", "ใช้เก็บอาหาร", "ใช้ผลิตเสียงร้องเท่านั้น ไม่เกี่ยวกับการหายใจเลย", "ใช้กรองน้ำ")),
    ("ลูกอ๊อดแลกเปลี่ยนแก๊สด้วยโครงสร้างใด", "เหงือก", ("ปอด", "ท่อลม", "ถุงลม", "ผิวหนังเพียงอย่างเดียวตลอดชีวิต")),
    ("เมื่อปลาถูกนำขึ้นจากน้ำ เหตุใดจึงหายใจไม่ได้แม้อากาศมี O₂ มาก", "แผ่นเหงือกติดกันจนพื้นที่แลกเปลี่ยนแก๊สลดลงมาก",
     ("อากาศไม่มี O₂", "เลือดปลาไม่มีฮีโมโกลบิน", "ปลาหายใจด้วยผิวหนังเท่านั้น ซึ่งต้องเปียกอยู่ตลอดเวลา", "เหงือกเปลี่ยนไปเป็นปอดเพื่อหายใจในอากาศไม่ทัน")),
    ("โครงสร้างแลกเปลี่ยนแก๊สของสัตว์ทุกชนิดมีลักษณะร่วมกันอย่างไร", "มีพื้นที่ผิวมาก บาง และชื้น",
     ("หนาและแห้งเพื่อป้องกันการสูญเสียน้ำ", "มีกระดูกหุ้มเสมอ", "อยู่ภายนอกร่างกายเสมอ", "ไม่มีหลอดเลือดมาเลี้ยง")),
    ("เหตุใดพลานาเรียจึงไม่ต้องมีอวัยวะหายใจเฉพาะ", "ลำตัวแบนบาง ทุกเซลล์อยู่ใกล้ผิว แก๊สแพร่ถึงได้",
     ("อาศัยอยู่บนบกที่มีออกซิเจนมากกว่าในน้ำ", "มีปอดขนาดเล็กซ่อนอยู่ใต้ผิวหนังตลอดแนวลำตัว", "ไม่ต้องใช้ออกซิเจนเลย", "มีเหงือกภายใน")),
)


@question_type(
    "biology.animal_gas_exchange_foundation",
    display_name={"th": "โครงสร้างที่ใช้แลกเปลี่ยนแก๊สของสัตว์ต่าง ๆ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ANIMAL,
)
class AnimalGasExchangeFoundation(QuestionType):
    """Which surface each animal breathes through, both ways."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        animal, organ = rng.choice(ANIMALS)
        others = rng.sample([a for a in ANIMALS if a[0] != animal], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{animal}แลกเปลี่ยนแก๊สด้วยโครงสร้างใด", correct=organ, wrongs=tuple(a[1] for a in others),
                             topic=TOPIC_ANIMAL, hint=ANIMAL_HINT)
        return _labelled(stem=f"สัตว์ใดแลกเปลี่ยนแก๊สด้วย{organ}", correct=animal, wrongs=tuple(a[0] for a in others), topic=TOPIC_ANIMAL,
                         hint=ANIMAL_HINT)


@question_type(
    "biology.animal_gas_exchange_fluency",
    display_name={"th": "การปรับตัวของโครงสร้างแลกเปลี่ยนแก๊ส"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ANIMAL,
)
class AnimalGasExchangeFluency(QuestionType):
    """Why each design works where the animal lives."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(ANIMAL_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_ANIMAL, hint=ANIMAL_HINT)


@question_type(
    "biology.animal_gas_exchange_application",
    display_name={"th": "เปรียบเทียบประสิทธิภาพการแลกเปลี่ยนแก๊ส"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ANIMAL,
)
class AnimalGasExchangeApplication(QuestionType):
    """Share of O₂ taken from water, and surface to volume."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            dissolved = rng.choice((6, 7, 8, 9, 10))
            share = rng.choice((50, 60, 75, 80, 85, 90))
            litres = rng.randrange(2, 41, 2)
            taken = Fraction(dissolved * share * litres, 100)
            return numeric(stem=f"น้ำมี O₂ ละลายอยู่ {dissolved} mg ต่อลิตร เหงือกปลาดึง O₂ ออกได้ร้อยละ {share} ถ้าน้ำไหลผ่านเหงือก {litres} ลิตร "
                                f"ปลาได้รับ O₂ กี่มิลลิกรัม", answer=taken,
                           wrongs=[dissolved * litres, Fraction(dissolved * (100 - share) * litres, 100), Fraction(dissolved * share, 100)],
                           unit="mg", topic=TOPIC_ANIMAL, hint="O₂ ที่ได้ = ความเข้มข้น × ปริมาตรน้ำ × ร้อยละที่ดึงได้ ÷ 100")
        side = rng.choice((1, 2, 3, 4, 5, 6, 10))
        ratio = Fraction(6, side)
        return numeric(stem=f"สัตว์สมมติรูปลูกบาศก์ยาวด้านละ {side} mm มีอัตราส่วนพื้นที่ผิวต่อปริมาตรเท่าใด (ต่อ mm)", answer=ratio,
                       wrongs=[6 * side, side * side, Fraction(side, 6)], unit="ต่อ mm", topic=TOPIC_ANIMAL,
                       hint="พื้นที่ผิว = 6 × ด้าน² ปริมาตร = ด้าน³ อัตราส่วน = 6 ÷ ด้าน ยิ่งตัวใหญ่ อัตราส่วนยิ่งน้อย จึงต้องมีอวัยวะหายใจเฉพาะ")
