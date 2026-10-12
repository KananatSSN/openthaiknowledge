"""พลังงานจลน์ พลังงานศักย์ และความสัมพันธ์ระหว่างงานกับพลังงาน

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/11

Sets moved here from: science_wave_f4.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import G, numeric, show
from otk.sets._support.science_wave_f4 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_ENERGY = "พลังงานจลน์ พลังงานศักย์ และความสัมพันธ์ระหว่างงานกับพลังงาน"


@question_type(
    "phys.work_energy_foundation",
    display_name={"th": "คำนวณพลังงานจลน์ พลังงานศักย์โน้มถ่วง และแรงดึงสปริง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ENERGY,
)
class WorkEnergyFoundation(QuestionType):
    """One formula at a time: ½mv², mgh, and F = kx."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            m = rng.randint(1, 20)
            v = rng.randint(1, 12) * 2
            return numeric(stem=f"วัตถุมวล {m} kg เคลื่อนที่ด้วยความเร็ว {v} m/s มีพลังงานจลน์เท่าใด",
                           answer=Fraction(m * v * v, 2), wrongs=[m * v * v, Fraction(m * v, 2), m * v],
                           unit="J", topic=TOPIC_ENERGY, hint="Eₖ = ½mv² อย่าลืมยกกำลังสองความเร็ว")
        if shape == 1:
            m = rng.randint(1, 20)
            h = rng.randint(1, 20)
            return numeric(stem=f"วัตถุมวล {m} kg อยู่สูงจากพื้น {h} m มีพลังงานศักย์โน้มถ่วงเทียบกับพื้นเท่าใด (g = 10 m/s²)",
                           answer=m * G * h, wrongs=[m * h, Fraction(m * G * h, 2), m * G],
                           unit="J", topic=TOPIC_ENERGY, hint="Eₚ = mgh")
        k = rng.randint(1, 20) * 10
        x = Fraction(rng.randint(1, 10), 100)
        return numeric(stem=f"สปริงมีค่านิจ {k} N/m ต้องออกแรงเท่าใดจึงดึงให้ยืดออก {show(x * 100)} cm",
                       answer=k * x, wrongs=[k * x * 100, k * x * x / 2, Fraction(k) / 2], unit="N",
                       topic=TOPIC_ENERGY, hint="F = kx และต้องแปลงเซนติเมตรเป็นเมตรก่อน")


@question_type(
    "phys.work_energy_fluency",
    display_name={"th": "พลังงานศักย์ยืดหยุ่นและงานของแรงลัพธ์กับพลังงานจลน์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ENERGY,
)
class WorkEnergyFluency(QuestionType):
    """½kx², and W_net = ΔEₖ both ways."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            k = rng.randint(1, 20) * 100
            x = Fraction(rng.randint(1, 10), 10)
            return numeric(stem=f"สปริงมีค่านิจ {k:,} N/m ถูกอัดเข้าไป {show(x)} m สะสมพลังงานศักย์ยืดหยุ่นเท่าใด",
                           answer=k * x * x / 2, wrongs=[k * x * x, k * x / 2, k * x], unit="J",
                           topic=TOPIC_ENERGY, hint="พลังงานศักย์ยืดหยุ่น = ½kx²")
        m = rng.randint(1, 10) * 2
        u = rng.randint(0, 8)
        v = u + rng.randint(1, 8)
        work = Fraction(m * (v * v - u * u), 2)
        if shape == 1:
            return numeric(
                stem=f"แรงลัพธ์ทำให้วัตถุมวล {m} kg เปลี่ยนความเร็วจาก {u} m/s เป็น {v} m/s งานของแรงลัพธ์เท่าใด",
                answer=work, wrongs=[Fraction(m * (v - u) ** 2, 2), Fraction(m * v * v, 2), m * (v - u)],
                unit="J", topic=TOPIC_ENERGY,
                hint="งานของแรงลัพธ์ = พลังงานจลน์ที่เปลี่ยนไป = ½mv² − ½mu² (ไม่ใช่ ½m(v − u)²)")
        return numeric(
            stem=(f"แรงลัพธ์ทำงาน {show(work)} J กับวัตถุมวล {m} kg ที่มีความเร็วต้น {u} m/s "
                  "วัตถุจะมีความเร็วปลายเท่าใด"),
            answer=v, wrongs=[u + Fraction(2 * work, m), v * v, v + u], unit="m/s", topic=TOPIC_ENERGY,
            hint="½mv² = ½mu² + W แล้วถอดรากที่สอง")


@question_type(
    "phys.work_energy_application",
    display_name={"th": "ใช้ความสัมพันธ์ระหว่างงานกับพลังงานหาแรงเบรกและการยกวัตถุ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ENERGY,
)
class WorkEnergyApplication(QuestionType):
    """Stopping force from kinetic energy, and the work to lift against gravity."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            m = rng.randint(4, 20) * 100
            v = rng.choice((10, 20, 30))
            ke = Fraction(m * v * v, 2)
            s = rng.choice([x for x in (10, 20, 25, 40, 50, 100) if ke % x == 0])
            return numeric(
                stem=(f"รถยนต์มวล {m:,} kg วิ่งด้วยความเร็ว {v} m/s เบรกจนหยุดในระยะ {s} m "
                      "แรงเบรกเฉลี่ยมีขนาดเท่าใด"),
                answer=ke / s, wrongs=[ke, Fraction(m * v, s), ke / s * 2], unit="N", topic=TOPIC_ENERGY,
                hint="งานของแรงเบรก = พลังงานจลน์ที่หายไป: F × s = ½mv²")
        m = rng.randint(1, 20)
        h = rng.randint(2, 15)
        v = rng.randint(1, 5) * 2
        work = m * G * h + Fraction(m * v * v, 2)
        return numeric(
            stem=(f"ยกวัตถุมวล {m} kg จากพื้นขึ้นไปสูง {h} m แล้วปล่อยให้มีความเร็ว {v} m/s ที่ความสูงนั้น "
                  "งานที่ใช้ทั้งหมดเท่าใด (g = 10 m/s²)"),
            answer=work, wrongs=[m * G * h, Fraction(m * v * v, 2), m * h + m * v],
            unit="J", topic=TOPIC_ENERGY,
            hint="งานที่ใช้เท่ากับพลังงานศักย์โน้มถ่วงที่เพิ่มขึ้นรวมกับพลังงานจลน์ที่เพิ่มขึ้น")
