"""การชนและการดีดตัวแยกจากกันในหนึ่งมิติ

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/15

Sets moved here from: science_wave_f5.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f5 import SUBJECT, UPPER_FOUR, _exact

PROVENANCE = Provenance("original")


TOPIC_COLLISION = "การชนและการดีดตัวแยกจากกันในหนึ่งมิติ"


COLLISION_FACTS = (
    ("ในการชนแบบยืดหยุ่น ปริมาณใดคงตัว", "ทั้งโมเมนตัมรวมและพลังงานจลน์รวม",
     ("โมเมนตัมรวมเท่านั้น", "พลังงานจลน์รวมเท่านั้น", "ความเร็วของวัตถุแต่ละก้อน")),
    ("ในการชนแบบไม่ยืดหยุ่น ปริมาณใดคงตัว", "โมเมนตัมรวม แต่พลังงานจลน์รวมลดลง",
     ("พลังงานจลน์รวม แต่โมเมนตัมรวมลดลง", "ทั้งโมเมนตัมรวมและพลังงานจลน์รวม", "ไม่มีปริมาณใดคงตัว")),
    ("วัตถุสองก้อนชนกันแล้วติดกันไป เป็นการชนแบบใด", "การชนแบบไม่ยืดหยุ่น ที่พลังงานจลน์สูญเสียมากที่สุด",
     ("การชนแบบยืดหยุ่น", "การดีดตัวแยกจากกัน", "การชนที่โมเมนตัมไม่คงตัว")),
    ("กฎการอนุรักษ์โมเมนตัมใช้ได้เมื่อใด", "เมื่อแรงลัพธ์ภายนอกที่กระทำต่อระบบเป็นศูนย์",
     ("เมื่อการชนเป็นแบบยืดหยุ่นเท่านั้น", "เมื่อวัตถุมีมวลเท่ากันเท่านั้น", "เมื่อวัตถุหยุดนิ่งหลังชน")),
    ("ระบบที่หยุดนิ่งแล้วดีดตัวแยกจากกัน โมเมนตัมรวมหลังแยกเท่าใด", "ศูนย์ โดยวัตถุทั้งสองมีโมเมนตัมขนาดเท่ากันแต่ทิศตรงข้าม",
     ("เท่ากับโมเมนตัมของก้อนที่เร็วกว่า", "มากกว่าศูนย์เพราะมีพลังงานจากสปริง", "เท่ากับผลรวมขนาดโมเมนตัมของสองก้อน")),
)


@question_type(
    "phys.collision_1d_foundation",
    display_name={"th": "ประเภทของการชนและการชนแล้วติดกันไป"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_COLLISION,
)
class Collision1dFoundation(QuestionType):
    """What each kind of collision keeps, and one body hitting another at rest and sticking."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.35:
            stem, correct, wrongs = rng.choice(COLLISION_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_COLLISION,
                             hint="ทุกการชนโมเมนตัมรวมคงตัว แต่พลังงานจลน์รวมคงตัวเฉพาะการชนแบบยืดหยุ่น")
        m1, m2, u = rng.choice([(a, b, c) for a in range(1, 11) for b in range(1, 11)
                                for c in range(2, 21) if _exact(Fraction(a * c, a + b))])
        what = rng.choice(("รถทดลอง", "รถไฟของเล่น", "ก้อนดินน้ำมัน", "รถบัมเปอร์คาร์"))
        return numeric(
            stem=(f"{what}มวล {m1} kg เคลื่อนที่ด้วยความเร็ว {u} m/s ชน{what}มวล {m2} kg ที่หยุดนิ่ง "
                  "แล้วติดกันไป ความเร็วหลังชนเท่าใด"),
            answer=Fraction(m1 * u, m1 + m2), wrongs=[Fraction(u, 2), Fraction(m1 * u, m2), Fraction(m2 * u, m1 + m2)],
            unit="m/s", topic=TOPIC_COLLISION, hint="m₁u = (m₁ + m₂)v เพราะโมเมนตัมรวมก่อนชนเท่ากับหลังชน")


@question_type(
    "phys.collision_1d_fluency",
    display_name={"th": "ใช้กฎการอนุรักษ์โมเมนตัมกับการชนและการดีดตัวแยกจากกัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_COLLISION,
)
class Collision1dFluency(QuestionType):
    """Head-on sticking, an unknown speed after the hit, and a recoil."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            m1, u1, m2, u2 = rng.choice([(a, b, c, d) for a in range(1, 9) for b in range(2, 13)
                                         for c in range(1, 9) for d in range(1, 13)
                                         if a * b > c * d and _exact(Fraction(a * b - c * d, a + c))])
            return numeric(
                stem=(f"รถทดลอง ก มวล {m1} kg วิ่งไปทางขวาด้วยอัตราเร็ว {u1} m/s ชนประสานงากับรถทดลอง ข มวล {m2} kg "
                      f"ที่วิ่งไปทางซ้ายด้วยอัตราเร็ว {u2} m/s แล้วติดกันไป อัตราเร็วหลังชนเท่าใด"),
                answer=Fraction(m1 * u1 - m2 * u2, m1 + m2),
                wrongs=[Fraction(m1 * u1 + m2 * u2, m1 + m2), Fraction(abs(u1 - u2)), Fraction(m1 * u1 - m2 * u2, m1)],
                unit="m/s", topic=TOPIC_COLLISION,
                hint="กำหนดทิศขวาเป็นบวก ความเร็วทางซ้ายเป็นลบ: m₁u₁ − m₂u₂ = (m₁ + m₂)v")
        if shape == 1:
            m1, m2, u, v1 = rng.choice([(a, b, c, d) for a in range(1, 9) for b in range(1, 9)
                                        for c in range(4, 13) for d in range(1, c)
                                        if _exact(Fraction(a * (c - d), b))])
            return numeric(
                stem=(f"ลูกบอล ก มวล {m1} kg เคลื่อนที่ด้วยความเร็ว {u} m/s ชนลูกบอล ข มวล {m2} kg ที่หยุดนิ่ง "
                      f"หลังชน ก เคลื่อนที่ต่อไปในทิศเดิมด้วยความเร็ว {v1} m/s ลูกบอล ข มีความเร็วเท่าใด"),
                answer=Fraction(m1 * (u - v1), m2),
                wrongs=[Fraction(m1 * u, m2), Fraction(m1 * (u + v1), m2), u - v1],
                unit="m/s", topic=TOPIC_COLLISION, hint="m₁u = m₁v₁ + m₂v₂ แล้วแก้หา v₂")
        # Pushed apart from rest: m₁v₁ = m₂v₂, drawn only where v₂ is exact.
        who = rng.randrange(3)
        if who == 0:
            bullet_g, v, m2 = rng.choice([(b, s, g) for b in (10, 20, 25, 50) for s in range(200, 900, 100)
                                          for g in (2, 3, 4, 5) if _exact(Fraction(b * s, 1000 * g))])
            m1 = Fraction(bullet_g, 1000)
            sub = (f"ปืนมวล {m2} kg ยิงกระสุนมวล {bullet_g} g ออกไปด้วยอัตราเร็ว {v} m/s "
                   "ปืนสะท้อนถอยหลังด้วยอัตราเร็วเท่าใด")
        elif who == 1:
            m1, m2, v = rng.choice([(a, b, s) for a in range(30, 81, 5) for b in range(30, 81, 5) if a != b
                                    for s in range(1, 7) if _exact(Fraction(a * s, b))])
            sub = (f"นักสเกตมวล {m1} kg และ {m2} kg ยืนนิ่งแล้วผลักกันออก คนมวล {m1} kg เคลื่อนที่ออกด้วย"
                   f"อัตราเร็ว {v} m/s คนมวล {m2} kg เคลื่อนที่ออกด้วยอัตราเร็วเท่าใด")
        else:
            m1, m2, v = rng.choice([(a, b, s) for a in range(1, 9) for b in range(1, 9) if a != b
                                    for s in range(1, 11) if _exact(Fraction(a * s, b))])
            sub = (f"รถทดลองมวล {m1} kg และ {m2} kg อัดสปริงไว้ระหว่างกันและหยุดนิ่ง เมื่อปล่อย รถมวล {m1} kg "
                   f"เคลื่อนที่ออกด้วยอัตราเร็ว {v} m/s รถมวล {m2} kg เคลื่อนที่ออกด้วยอัตราเร็วเท่าใด")
        answer = Fraction(m1) * v / m2
        return numeric(stem=sub, answer=answer, wrongs=[v, Fraction(m1) * v, Fraction(v, 2)],
                       unit="m/s", topic=TOPIC_COLLISION,
                       hint="ก่อนแยกโมเมนตัมรวมเป็นศูนย์ หลังแยกจึงมีขนาดเท่ากันแต่ทิศตรงข้าม: m₁v₁ = m₂v₂")


@question_type(
    "phys.collision_1d_application",
    display_name={"th": "พลังงานจลน์ในการชน: การชนแบบยืดหยุ่นและไม่ยืดหยุ่น"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_COLLISION,
)
class Collision1dApplication(QuestionType):
    """Kinetic energy lost when bodies stick, telling elastic from inelastic, and the elastic hit."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            m1, m2, u = rng.choice([(a, b, c) for a in range(1, 9) for b in range(1, 9)
                                    for c in range(2, 13) if (a * c) % (a + b) == 0])
            v = Fraction(m1 * u, m1 + m2)
            lost = Fraction(m1 * u * u, 2) - (m1 + m2) * v * v / 2
            return numeric(
                stem=(f"วัตถุมวล {m1} kg เคลื่อนที่ด้วยความเร็ว {u} m/s ชนวัตถุมวล {m2} kg ที่หยุดนิ่งแล้วติดกันไป "
                      "พลังงานจลน์ที่สูญเสียไปในการชนเท่าใด"),
                answer=lost, wrongs=[Fraction(m1 * u * u, 2), (m1 + m2) * v * v / 2, Fraction(m1 * u * u, 4)],
                unit="J", topic=TOPIC_COLLISION,
                hint="หาความเร็วหลังชนจากกฎการอนุรักษ์โมเมนตัมก่อน แล้วนำพลังงานจลน์ก่อนชนลบพลังงานจลน์หลังชน")
        if shape == 1:
            while True:
                m2 = rng.randint(1, 4)
                m1 = rng.randint(m2 + 1, 6)
                u = rng.randint(1, 24 // (m1 + m2)) * (m1 + m2)
                p, ke = m1 * u, m1 * u * u
                v1e, v2e = Fraction((m1 - m2) * u, m1 + m2), Fraction(2 * m1 * u, m1 + m2)
                if rng.random() < 0.5:
                    v1, v2, elastic = v1e, v2e, True
                    break
                vc = Fraction(p, m1 + m2)
                # A true inelastic hit: momentum kept, the two still separate, kinetic energy lost.
                options = [(Fraction(p - m2 * x, m1), Fraction(x)) for x in range(int(vc) + 1, int(v2e))
                           if Fraction(p - m2 * x, m1) >= 0 and _exact(Fraction(p - m2 * x, m1))]
                options = [(a, b) for a, b in options if b > a and m1 * a * a + m2 * b * b < ke]
                if options:
                    v1, v2 = rng.choice(options)
                    elastic = False
                    break
            assert m1 * v1 + m2 * v2 == p
            right = "การชนแบบยืดหยุ่น เพราะพลังงานจลน์รวมก่อนและหลังชนเท่ากัน"
            wrong = "การชนแบบไม่ยืดหยุ่น เพราะพลังงานจลน์รวมหลังชนลดลง"
            if not elastic:
                right, wrong = wrong, right
            return _labelled(
                stem=(f"รถทดลอง ก มวล {m1} kg เคลื่อนที่ด้วยความเร็ว {u} m/s ชนรถทดลอง ข มวล {m2} kg ที่หยุดนิ่ง "
                      f"หลังชน ก และ ข เคลื่อนที่ไปทางเดิมด้วยความเร็ว {show(v1)} m/s และ {show(v2)} m/s ตามลำดับ "
                      "การชนนี้เป็นแบบใด"),
                correct=right,
                wrongs=(wrong, "การดีดตัวแยกจากกัน เพราะโมเมนตัมรวมเป็นศูนย์",
                        "เกิดขึ้นไม่ได้ เพราะโมเมนตัมรวมก่อนและหลังชนไม่เท่ากัน"),
                topic=TOPIC_COLLISION,
                hint="โมเมนตัมรวมคงตัวทั้งสองแบบ ให้เทียบพลังงานจลน์รวม ½mv² ก่อนและหลังชน")
        if rng.random() < 0.4:
            m = rng.randint(1, 10)
            u = rng.randint(2, 20)
            return _labelled(
                stem=(f"ลูกบิลเลียด ก มวล {m * 100} g เคลื่อนที่ด้วยความเร็ว {u} m/s ชนตรงกับลูก ข มวลเท่ากันที่หยุดนิ่ง "
                      "แบบยืดหยุ่น หลังชนความเร็วของทั้งสองเป็นอย่างไร"),
                correct=f"ก หยุดนิ่ง และ ข เคลื่อนที่ด้วยความเร็ว {u} m/s",
                wrongs=(f"ทั้งสองเคลื่อนที่ไปด้วยกันด้วยความเร็ว {show(Fraction(u, 2))} m/s",
                        f"ก กระดอนกลับด้วยความเร็ว {u} m/s และ ข หยุดนิ่ง",
                        f"ก และ ข เคลื่อนที่ด้วยความเร็ว {u} m/s เท่ากัน"),
                topic=TOPIC_COLLISION,
                hint="การชนแบบยืดหยุ่นของมวลเท่ากันที่ก้อนหนึ่งหยุดนิ่ง ความเร็วจะแลกกัน")
        m1, m2, u = rng.choice([(a, b, c) for a in range(1, 9) for b in range(1, 9) if a != b
                                for c in range(2, 16) if _exact(Fraction(2 * a * c, a + b))])
        return numeric(
            stem=(f"วัตถุมวล {m1} kg เคลื่อนที่ด้วยความเร็ว {u} m/s ชนตรงกับวัตถุมวล {m2} kg ที่หยุดนิ่ง แบบยืดหยุ่น "
                  f"วัตถุมวล {m2} kg มีความเร็วหลังชนเท่าใด"),
            answer=Fraction(2 * m1 * u, m1 + m2),
            wrongs=[Fraction(m1 * u, m1 + m2), Fraction(m1 * u, m2), Fraction(abs(m1 - m2) * u, m1 + m2)],
            unit="m/s", topic=TOPIC_COLLISION,
            hint="การชนแบบยืดหยุ่นกับเป้าที่หยุดนิ่ง: v₂ = 2m₁u ÷ (m₁ + m₂) จากการอนุรักษ์ทั้งโมเมนตัมและพลังงานจลน์")
