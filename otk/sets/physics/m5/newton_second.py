"""ความสัมพันธ์ระหว่างความเร่ง แรงลัพธ์ และมวล

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.5/3

Sets moved here from: science_wave_e11.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e11 import SUBJECT, UPPER_FIVE, _labelled, _numeric, show

PROVENANCE = Provenance("original")


TOPIC_NEWTON2 = "ความสัมพันธ์ระหว่างความเร่ง แรงลัพธ์ และมวล"


BODIES = ("กล่องไม้", "รถเข็น", "รถของเล่น", "ลังสินค้า", "เลื่อนหิมะ", "ก้อนหินบนพื้นน้ำแข็ง")


@question_type(
    "phys.newton_second_foundation",
    display_name={"th": "ความเร่งเปลี่ยนอย่างไรเมื่อแรงลัพธ์หรือมวลเปลี่ยน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEWTON2,
)
class NewtonSecondFoundation(QuestionType):
    """One variable at a time: the direction and size of the change in a."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        k = rng.choice((2, 3, 4))
        hint = "ความเร่งแปรผันตรงกับแรงลัพธ์ และแปรผกผันกับมวล (a = F/m)"
        shape = rng.random()
        if shape < 0.4:
            return _labelled(
                stem=(f"ออกแรงลัพธ์ดึง{rng.choice(BODIES)}ให้เคลื่อนที่ ถ้าเพิ่มแรงลัพธ์เป็น {k} เท่า "
                      "โดยมวลเท่าเดิม ความเร่งจะเป็นอย่างไร"),
                correct=f"เพิ่มขึ้นเป็น {k} เท่า",
                wrongs=(f"ลดลงเหลือ 1/{k} เท่า", "เท่าเดิม", f"เพิ่มขึ้นเป็น {k * k} เท่า",
                        f"ลดลงเหลือ 1/{k * k} เท่า"),  # wrong way and squared
                topic=TOPIC_NEWTON2, hint=hint,
            )
        if shape < 0.8:
            return _labelled(
                stem=(f"ออกแรงลัพธ์เท่าเดิมดึง{rng.choice(BODIES)} ถ้าวัตถุมีมวลเพิ่มขึ้นเป็น {k} เท่า "
                      "ความเร่งจะเป็นอย่างไร"),
                correct=f"ลดลงเหลือ 1/{k} เท่า",
                wrongs=(f"เพิ่มขึ้นเป็น {k} เท่า", "เท่าเดิม", f"ลดลงเหลือ 1/{k * k} เท่า",
                        f"เพิ่มขึ้นเป็น {k * k} เท่า"),  # wrong way and squared
                topic=TOPIC_NEWTON2, hint=hint,
            )
        return _labelled(
            stem="แรงลัพธ์ 1 นิวตันหมายถึงข้อใด",
            correct="แรงลัพธ์ที่ทำให้วัตถุมวล 1 กิโลกรัมมีความเร่ง 1 เมตรต่อวินาทีกำลังสอง",
            wrongs=("แรงที่ทำให้วัตถุมวล 1 กิโลกรัมเคลื่อนที่ด้วยความเร็ว 1 เมตรต่อวินาที",
                    "น้ำหนักของวัตถุมวล 1 กิโลกรัม",
                    "แรงที่ทำให้วัตถุเคลื่อนที่ได้ระยะทาง 1 เมตร"),
            topic=TOPIC_NEWTON2, hint=hint,
        )


@question_type(
    "phys.newton_second_fluency",
    display_name={"th": "คำนวณความเร่ง แรงลัพธ์ หรือมวลจาก F = ma"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEWTON2,
)
class NewtonSecondFluency(QuestionType):
    """The relationship itself, solved for any one of its three quantities."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        m = rng.randint(2, 25)
        a = rng.randint(1, 10)
        f = m * a
        body = rng.choice(BODIES)
        hint = "แรงลัพธ์ = มวล × ความเร่ง (F = ma)"
        shape = rng.randrange(3)
        if shape == 0:
            return _numeric(
                stem=f"แรงลัพธ์ {f} นิวตันกระทำต่อ{body}มวล {m} กิโลกรัม วัตถุมีความเร่งเท่าใด",
                answer=a, wrongs=[f * m, Fraction(m, f), f - m], unit="m/s²",
                topic=TOPIC_NEWTON2, hint=hint)
        if shape == 1:
            return _numeric(
                stem=f"ต้องใช้แรงลัพธ์เท่าใดจึงจะทำให้{body}มวล {m} กิโลกรัมมีความเร่ง {a} m/s²",
                answer=f, wrongs=[m + a, Fraction(m, a), Fraction(a, m)], unit="นิวตัน",
                topic=TOPIC_NEWTON2, hint=hint)
        return _numeric(
            stem=f"แรงลัพธ์ {f} นิวตันทำให้{body}มีความเร่ง {a} m/s² {body}มีมวลเท่าใด",
            answer=m, wrongs=[f * a, Fraction(a, f), f - a], unit="กิโลกรัม",
            topic=TOPIC_NEWTON2, hint=hint)


@question_type(
    "phys.newton_second_application",
    display_name={"th": "ใช้ F = ma กับแรงหลายแรงและการเปลี่ยนความเร็ว"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEWTON2,
)
class NewtonSecondApplication(QuestionType):
    """Two forces to a net force first; a speed change to a force; two bodies compared."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        body = rng.choice(BODIES)
        if shape == 0:
            m = rng.randint(2, 20)
            a = rng.randint(1, 6)
            friction = rng.randint(2, 30)
            push = m * a + friction
            return _numeric(
                stem=(f"ออกแรง {push} นิวตันลาก{body}มวล {m} กิโลกรัมไปตามพื้นราบ "
                      f"มีแรงเสียดทาน {friction} นิวตันต้านการเคลื่อนที่ ความเร่งของ{body}เท่าใด"),
                answer=a, wrongs=[Fraction(push, m), Fraction(push + friction, m), push - friction],
                unit="m/s²", topic=TOPIC_NEWTON2,
                hint="หาแรงลัพธ์ก่อน (แรงที่ออก − แรงเสียดทาน) แล้วจึงหารด้วยมวล")
        if shape == 1:
            m = rng.randint(2, 20) * 50
            dv = rng.randint(2, 10) * 2
            t = rng.choice([d for d in (2, 4, 5, 8, 10) if (m * dv) % d == 0])
            f = Fraction(m * dv, t)
            return _numeric(
                stem=(f"รถยนต์มวล {m:,} กิโลกรัมเพิ่มความเร็วจาก 0 เป็น {dv} m/s ในเวลา {t} วินาที "
                      "อย่างสม่ำเสมอ แรงลัพธ์ที่กระทำต่อรถยนต์เท่าใด"),
                answer=f, wrongs=[m * dv, Fraction(m, t), f * 2], unit="นิวตัน",
                topic=TOPIC_NEWTON2,
                hint="หาความเร่งจาก (ความเร็วที่เปลี่ยน ÷ เวลา) แล้วคูณด้วยมวล")
        f = rng.randint(2, 12) * 6
        m1, m2 = rng.sample((1, 2, 3, 6), 2)
        a1, a2 = Fraction(f, m1), Fraction(f, m2)
        ratio = a1 / a2
        return _labelled(
            stem=(f"ออกแรงลัพธ์ {f} นิวตันเท่ากันกระทำต่อวัตถุ ก มวล {m1} กิโลกรัม และวัตถุ ข "
                  f"มวล {m2} กิโลกรัม ข้อใดถูกต้อง"),
            correct=f"วัตถุ ก มีความเร่ง {show(a1)} m/s² ซึ่งเป็น {show(ratio)} เท่าของวัตถุ ข",
            wrongs=(f"วัตถุ ก มีความเร่ง {show(a2)} m/s² ซึ่งเป็น {show(1 / ratio)} เท่าของวัตถุ ข",
                    f"วัตถุทั้งสองมีความเร่งเท่ากัน คือ {show(Fraction(f, m1 + m2))} m/s²",
                    f"วัตถุ ก มีความเร่ง {show(f * m1)} m/s² ซึ่งเป็น {show(Fraction(m1, m2))} เท่าของวัตถุ ข"),
            topic=TOPIC_NEWTON2,
            hint="แรงลัพธ์เท่ากัน วัตถุมวลน้อยจะมีความเร่งมากกว่า ตามอัตราส่วนผกผันของมวล",
        )
