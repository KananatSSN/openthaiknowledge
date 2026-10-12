"""กฎการเคลื่อนที่ของนิวตันและการนำไปใช้

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/5

Sets moved here from: science_wave_f3.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import SUBJECT, UPPER_FOUR, G, _labelled, numeric

PROVENANCE = Provenance("original")


TOPIC_NEWTON = "กฎการเคลื่อนที่ของนิวตันและการนำไปใช้"


NEWTON_FACTS = (
    ("วัตถุจะรักษาสภาพหยุดนิ่งหรือเคลื่อนที่ด้วยความเร็วคงตัว เมื่อใด", "เมื่อแรงลัพธ์ที่กระทำต่อวัตถุเป็นศูนย์",
     ("เมื่อมีแรงกระทำต่อวัตถุเพียงแรงเดียว", "เมื่อวัตถุมีมวลมาก", "เมื่อไม่มีแรงโน้มถ่วง")),
    ("ผู้โดยสารในรถที่เบรกกะทันหันพุ่งไปข้างหน้า อธิบายได้ด้วยข้อใด", "ความเฉื่อย ตามกฎการเคลื่อนที่ข้อที่หนึ่ง",
     ("แรงปฏิกิริยาจากเบาะดันไปข้างหน้า", "รถออกแรงผลักผู้โดยสารไปข้างหน้า", "แรงโน้มถ่วงเปลี่ยนทิศ")),
    ("แผนภาพวัตถุอิสระของกล่องที่วางนิ่งบนพื้นราบต้องมีแรงใดบ้าง", "น้ำหนักของกล่องและแรงที่พื้นดันกล่อง",
     ("น้ำหนักของกล่องและแรงที่กล่องกดพื้น", "แรงที่พื้นดันกล่องเท่านั้น", "น้ำหนักของกล่อง แรงเสียดทาน และแรงดึง")),
    ("แผนภาพวัตถุอิสระแสดงแรงแบบใด", "เฉพาะแรงที่วัตถุอื่นกระทำต่อวัตถุที่สนใจ",
     ("ทุกแรงที่วัตถุที่สนใจกระทำต่อวัตถุอื่น", "เฉพาะแรงกิริยาและแรงปฏิกิริยาคู่กัน", "เฉพาะน้ำหนักของวัตถุ")),
)


@question_type(
    "phys.newton_applied_foundation",
    display_name={"th": "กฎการเคลื่อนที่ของนิวตันและแผนภาพวัตถุอิสระ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NEWTON,
)
class NewtonAppliedFoundation(QuestionType):
    """The laws and what a free-body diagram holds."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(NEWTON_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_NEWTON,
                             hint="แผนภาพวัตถุอิสระแสดงแรงที่กระทำต่อวัตถุที่สนใจเท่านั้น แล้วใช้ ΣF = ma")
        m = rng.randint(2, 20)
        a = rng.randint(1, 6)
        friction = rng.randint(1, 10) * 5
        push = m * a + friction
        return numeric(
            stem=(f"ออกแรง {push} N ผลักกล่องมวล {m} kg บนพื้นราบ มีแรงเสียดทาน {friction} N "
                  "ความเร่งของกล่องเท่าใด"),
            answer=a, wrongs=[Fraction(push, m), Fraction(push + friction, m), push - friction],
            unit="m/s²", topic=TOPIC_NEWTON, hint="ΣF = ma โดยแรงลัพธ์คือแรงผลักลบแรงเสียดทาน")


@question_type(
    "phys.newton_applied_fluency",
    display_name={"th": "ใช้กฎของนิวตันกับวัตถุที่ติดกันหรือผูกเชือกต่อกัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NEWTON,
)
class NewtonAppliedFluency(QuestionType):
    """Two bodies moving together: the shared acceleration, then the force between them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        m1 = rng.randint(1, 10)
        m2 = rng.randint(1, 10)
        a = rng.randint(1, 5)
        f = (m1 + m2) * a
        rope = rng.random() < 0.5
        if rng.random() < 0.4:
            return numeric(
                stem=(f"ออกแรง {f} N {'ดึงรถ ก ซึ่งผูกเชือกติดกับรถ ข' if rope else 'ผลักกล่อง ก ที่วางชิดกล่อง ข'} "
                      f"บนพื้นลื่น ก มีมวล {m1} kg และ ข มีมวล {m2} kg ความเร่งของระบบเท่าใด"),
                answer=a, wrongs=[Fraction(f, m1), Fraction(f, m2), f], unit="m/s²", topic=TOPIC_NEWTON,
                hint="วัตถุเคลื่อนที่ไปด้วยกัน ใช้มวลรวม: a = F ÷ (m₁ + m₂)")
        what = "แรงตึงในเชือกระหว่างรถทั้งสอง" if rope else "แรงที่กล่อง ก ดันกล่อง ข"
        return numeric(
            stem=(f"ออกแรง {f} N {'ดึงรถ ก ซึ่งผูกเชือกติดกับรถ ข' if rope else 'ผลักกล่อง ก ที่วางชิดกล่อง ข'} "
                  f"บนพื้นลื่น ก มีมวล {m1} kg และ ข มีมวล {m2} kg {what}มีขนาดเท่าใด"),
            answer=m2 * a, wrongs=[f, m1 * a, Fraction(f, 2)], unit="N", topic=TOPIC_NEWTON,
            hint="หาความเร่งของระบบก่อน แล้วเขียนแผนภาพวัตถุอิสระของ ข: แรงที่ ข ได้รับ = m₂a")


@question_type(
    "phys.newton_applied_application",
    display_name={"th": "ใช้กฎของนิวตันกับลิฟต์ รอก และพื้นเอียง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NEWTON,
)
class NewtonAppliedApplication(QuestionType):
    """A scale in a lift, two masses over a pulley, and a frictionless slope."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            m = rng.randint(4, 12) * 5
            a = rng.randint(1, 4)
            up = rng.random() < 0.5
            reading = m * (G + a if up else G - a)
            return numeric(
                stem=(f"คนมวล {m} kg ยืนบนตาชั่งสปริงในลิฟต์ที่กำลัง{'เร่งขึ้น' if up else 'เร่งลง'}"
                      f"ด้วยความเร่ง {a} m/s² ตาชั่งอ่านค่าแรงได้เท่าใด (g = 10 m/s²)"),
                answer=reading, wrongs=[m * G, m * (G - a if up else G + a), m * a], unit="N", topic=TOPIC_NEWTON,
                hint="เขียนแผนภาพวัตถุอิสระของคน: N − mg = ma เมื่อเร่งขึ้น และ mg − N = ma เมื่อเร่งลง")
        if shape == 1:
            # Only pairs whose acceleration comes out exact.
            m1, m2 = rng.choice([(a, b) for a in range(2, 13) for b in range(1, a)
                                 if ((a - b) * G * 100) % (a + b) == 0])
            total = m1 + m2
            a = Fraction((m1 - m2) * G, total)
            return numeric(
                stem=(f"แขวนมวล {m1} kg และ {m2} kg ที่ปลายเชือกเบาซึ่งคล้องผ่านรอกลื่น ปล่อยให้เคลื่อนที่ "
                      "ความเร่งของมวลทั้งสองเท่าใด (g = 10 m/s²)"),
                answer=a, wrongs=[Fraction((m1 - m2) * G, m1), Fraction(m1 * G, total), G], unit="m/s²",
                topic=TOPIC_NEWTON,
                hint="แรงลัพธ์ของระบบคือผลต่างของน้ำหนัก (m₁ − m₂)g และมวลที่ถูกเร่งคือมวลรวม")
        m = rng.randint(1, 10)
        return numeric(
            stem=(f"กล่องมวล {m} kg ไถลลงพื้นเอียงลื่นที่ทำมุม 37° กับแนวระดับ ความเร่งของกล่องเท่าใด "
                  "(g = 10 m/s², sin 37° = 0.6)"),
            answer=6, wrongs=[8, 10, Fraction(6 * m)], unit="m/s²", topic=TOPIC_NEWTON,
            hint="แรงลัพธ์ตามพื้นเอียงคือ mg sin θ ดังนั้น a = g sin θ ไม่ขึ้นกับมวล")
