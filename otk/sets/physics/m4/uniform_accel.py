"""การเคลื่อนที่แนวตรงด้วยความเร่งคงตัว

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/3

Sets moved here from: science_wave_f3.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import SUBJECT, UPPER_FOUR, G, _labelled, numeric, show

PROVENANCE = Provenance("original")


TOPIC_MOTION = "การเคลื่อนที่แนวตรงด้วยความเร่งคงตัว"


MOVERS = ("รถยนต์", "รถจักรยานยนต์", "รถไฟ", "นักปั่นจักรยาน", "รถบรรทุก")


GRAPH_FACTS = (
    ("ความชันของกราฟตำแหน่งกับเวลาบอกปริมาณใด", "ความเร็ว",
     ("ความเร่ง", "การกระจัด", "แรงลัพธ์")),
    ("ความชันของกราฟความเร็วกับเวลาบอกปริมาณใด", "ความเร่ง",
     ("ความเร็ว", "การกระจัด", "ระยะทางทั้งหมด")),
    ("พื้นที่ใต้กราฟความเร็วกับเวลาบอกปริมาณใด", "การกระจัด",
     ("ความเร่ง", "ความเร็วเฉลี่ย", "เวลาที่ใช้")),
    ("พื้นที่ใต้กราฟความเร่งกับเวลาบอกปริมาณใด", "ความเร็วที่เปลี่ยนไป",
     ("การกระจัด", "ตำแหน่ง", "แรงลัพธ์")),
    ("กราฟความเร็วกับเวลาของวัตถุที่มีความเร่งคงตัวมีลักษณะใด", "เส้นตรงที่มีความชันคงตัว",
     ("เส้นโค้งพาราโบลา", "เส้นขนานกับแกนเวลาเสมอ", "เส้นตั้งฉากกับแกนเวลา")),
)


@question_type(
    "phys.uniform_accel_foundation",
    display_name={"th": "ความหมายของกราฟและสมการการเคลื่อนที่ที่มีความเร่งคงตัว"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MOTION,
)
class UniformAccelFoundation(QuestionType):
    """What each graph's slope and area mean, and v = u + at in one step."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        if shape < 0.35:
            stem, correct, wrongs = rng.choice(GRAPH_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_MOTION,
                             hint="ความชันคืออัตราการเปลี่ยน พื้นที่ใต้กราฟคือผลคูณของสองแกน")
        u = rng.randint(0, 20)
        a = rng.randint(1, 6)
        t = rng.randint(2, 10)
        mover = rng.choice(MOVERS)
        if shape < 0.7:
            return numeric(
                stem=f"{mover}มีความเร็วต้น {u} m/s และเร่งด้วยความเร่ง {a} m/s² เป็นเวลา {t} s มีความเร็วปลายเท่าใด",
                answer=u + a * t, wrongs=[a * t, u + a, u * t + a], unit="m/s", topic=TOPIC_MOTION,
                hint="v = u + at")
        v = u + a * t
        return numeric(
            stem=f"{mover}เปลี่ยนความเร็วจาก {u} m/s เป็น {v} m/s อย่างสม่ำเสมอในเวลา {t} s มีความเร็วเฉลี่ยเท่าใด",
            answer=Fraction(u + v, 2), wrongs=[v - u, Fraction(v, t), v], unit="m/s", topic=TOPIC_MOTION,
            hint="เมื่อความเร่งคงตัว ความเร็วเฉลี่ย = (u + v) ÷ 2")


@question_type(
    "phys.uniform_accel_fluency",
    display_name={"th": "คำนวณการกระจัด ความเร็ว และความเร่งด้วยสมการการเคลื่อนที่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MOTION,
)
class UniformAccelFluency(QuestionType):
    """s = ut + ½at², v² = u² + 2as, and s from a velocity-time graph's area."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        mover = rng.choice(MOVERS)
        shape = rng.randrange(3)
        if shape == 0:
            u = rng.randint(0, 15)
            t = rng.randint(2, 10)
            a = rng.choice([x for x in range(1, 7) if (x * t * t) % 2 == 0])
            s = u * t + Fraction(a * t * t, 2)
            return numeric(
                stem=f"{mover}มีความเร็วต้น {u} m/s และเร่งด้วยความเร่ง {a} m/s² คงตัว ในเวลา {t} s ได้การกระจัดเท่าใด",
                answer=s, wrongs=[u * t + a * t * t, u * t, Fraction(a * t * t, 2)], unit="m", topic=TOPIC_MOTION,
                hint="s = ut + ½at²")
        if shape == 1:
            a = rng.choice((1, 2, 3, 4, 5))
            u = rng.randint(0, 10)
            s = rng.choice([x for x in range(5, 200) if ((u * u + 2 * a * x) ** 0.5).is_integer()] or [0])
            if s == 0:
                u, a, s = 0, 2, 25
            v = int((u * u + 2 * a * s) ** 0.5)
            return numeric(
                stem=(f"{mover}มีความเร็วต้น {u} m/s เร่งด้วยความเร่ง {a} m/s² คงตัว จนได้การกระจัด {s} m "
                      "มีความเร็วปลายเท่าใด"),
                answer=v, wrongs=[u + a * s, u * u + 2 * a * s, u + 2 * a * s], unit="m/s", topic=TOPIC_MOTION,
                hint="เมื่อไม่ทราบเวลา ใช้ v² = u² + 2as")
        u = rng.randint(2, 12) * 2
        t1 = rng.randint(2, 6)
        t2 = rng.randint(2, 6)
        # Speed up from u to v over t1, then hold v for t2: trapezium plus rectangle.
        v = u + rng.randint(1, 4) * 2
        s = Fraction(u + v, 2) * t1 + v * t2
        return numeric(
            stem=(f"กราฟความเร็วกับเวลาของ{mover}: ช่วง 0 ถึง {t1} s ความเร็วเพิ่มจาก {u} m/s เป็น {v} m/s "
                  f"อย่างสม่ำเสมอ แล้วคงที่ที่ {v} m/s อีก {t2} s การกระจัดทั้งหมดเท่าใด"),
            answer=s, wrongs=[v * (t1 + t2), u * t1 + v * t2, Fraction(u + v, 2) * (t1 + t2)],
            unit="m", topic=TOPIC_MOTION,
            hint="การกระจัดคือพื้นที่ใต้กราฟความเร็วกับเวลา: ช่วงแรกเป็นรูปสี่เหลี่ยมคางหมู ช่วงหลังเป็นสี่เหลี่ยมมุมฉาก")


@question_type(
    "phys.uniform_accel_application",
    display_name={"th": "การตกอิสระ การโยนขึ้นในแนวดิ่ง และระยะหยุดรถ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MOTION,
)
class UniformAccelApplication(QuestionType):
    """g at work, and a driver's reaction time added to the braking distance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(4)
        if shape == 0:
            t = rng.randint(1, 6)
            return numeric(
                stem=f"ปล่อยก้อนหินจากหน้าผาให้ตกอิสระ ใช้เวลา {t} s จึงถึงพื้น หน้าผาสูงเท่าใด (g = 10 m/s²)",
                answer=5 * t * t, wrongs=[G * t * t, G * t, 5 * t], unit="m", topic=TOPIC_MOTION,
                hint="ตกอิสระจากหยุดนิ่ง: s = ½gt²")
        if shape == 1:
            u = rng.choice((10, 20, 30, 40))
            return numeric(
                stem=f"โยนลูกบอลขึ้นในแนวดิ่งด้วยความเร็ว {u} m/s ลูกบอลขึ้นไปได้สูงสุดเท่าใด (g = 10 m/s²)",
                answer=Fraction(u * u, 2 * G), wrongs=[Fraction(u * u, G), Fraction(u, G), u * 2],
                unit="m", topic=TOPIC_MOTION,
                hint="ที่จุดสูงสุด v = 0 จาก v² = u² − 2gs จะได้ s = u²/2g")
        if shape == 2:
            u = rng.choice((10, 20, 30, 40, 50))
            return numeric(
                stem=f"โยนลูกบอลขึ้นในแนวดิ่งด้วยความเร็ว {u} m/s ลูกบอลใช้เวลาเท่าใดจึงกลับมาถึงมือ (g = 10 m/s²)",
                answer=Fraction(2 * u, G), wrongs=[Fraction(u, G), Fraction(u * u, 2 * G), Fraction(4 * u, G)],
                unit="s", topic=TOPIC_MOTION,
                hint="ขาขึ้นใช้เวลา u/g และขาลงใช้เวลาเท่ากัน")
        u = rng.choice((10, 15, 20, 25, 30))
        react = rng.choice((Fraction(1, 2), Fraction(1), Fraction(3, 2)))
        a = rng.choice([x for x in (2, 4, 5, 10) if (Fraction(u * u, 2 * x) * 100).denominator == 1])
        d = u * react + Fraction(u * u, 2 * a)
        return numeric(
            stem=(f"คนขับรถที่วิ่งด้วยความเร็ว {u} m/s เห็นสิ่งกีดขวาง ใช้เวลาตัดสินใจ {show(react)} s ก่อนเหยียบเบรก "
                  f"แล้วรถลดความเร็วด้วยความหน่วง {a} m/s² จนหยุด ระยะทางตั้งแต่เห็นจนหยุดเท่าใด"),
            answer=d, wrongs=[Fraction(u * u, 2 * a), u * react + Fraction(u * u, a), u * react],
            unit="m", topic=TOPIC_MOTION,
            hint="ระหว่างตัดสินใจ รถยังวิ่งด้วยความเร็วคงตัว (s = ut) แล้วจึงเบรก (s = u²/2a) นำสองช่วงมารวมกัน")
