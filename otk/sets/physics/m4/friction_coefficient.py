"""แรงเสียดทานและสัมประสิทธิ์ความเสียดทาน

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/7

Sets moved here from: science_wave_f1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_f1 import SUBJECT, UPPER_FOUR, G, _labelled, _num, _numeric

PROVENANCE = Provenance("adapted", sources=('sheet_database/Faii/ข้อสอบแรง.pdf',))


TOPIC_FRICTION_COEFFICIENT = "แรงเสียดทานและสัมประสิทธิ์ความเสียดทาน"


MU_VALUES = (0.1, 0.2, 0.25, 0.3, 0.375, 0.4, 0.5, 0.6, 0.75, 0.8, 1.0, 1.25)


MASSES = (0.2, 0.5, 1, 2, 4, 5, 10, 20, 40, 50)          # kg


# Mass/μ pairs whose friction force is a whole number of newtons, so the answer
# is writable either way round: μ = f/N and f = μN both come out clean.
FRICTION_POOL = tuple(
    (mass, mu, round(mu * mass * G))
    for mass in MASSES for mu in MU_VALUES
    if abs(mu * mass * G - round(mu * mass * G)) < 1e-9 and mu * mass * G >= 1
)


SURFACES = ("พื้นไม้", "พื้นปูน", "พื้นกระเบื้อง", "พื้นยางมะตอย")


MU_PAIRS = (("พื้นน้ำแข็ง", 0.05), ("พื้นกระเบื้องขัดมัน", 0.2), ("พื้นไม้", 0.35), ("พื้นปูน", 0.5),
            ("พื้นยางมะตอย", 0.7), ("พื้นยาง", 0.9))


@question_type(
    "phys.friction_coefficient_foundation",
    display_name={"th": "อธิบายความหมายของสัมประสิทธิ์ความเสียดทาน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FRICTION_COEFFICIENT,
)
class FrictionCoefficientFoundation(QuestionType):
    """What μ is, before any instance: a ratio, unitless, and larger when static."""

    FACTS = (
        ("สัมประสิทธิ์ความเสียดทานระหว่างผิวสัมผัสคู่หนึ่ง ๆ หมายถึงข้อใด",
         "อัตราส่วนระหว่างแรงเสียดทานกับแรงตั้งฉากที่ผิวสัมผัสกดกัน",
         ("ผลคูณระหว่างแรงเสียดทานกับแรงตั้งฉาก",
          "ผลต่างระหว่างแรงเสียดทานกับแรงตั้งฉาก",
          "อัตราส่วนระหว่างแรงเสียดทานกับพื้นที่ผิวสัมผัส"),
         "μ = f / N เป็นอัตราส่วนของแรงสองแรง"),
        ("สัมประสิทธิ์ความเสียดทานมีหน่วยเป็นอะไร",
         "ไม่มีหน่วย เพราะเป็นอัตราส่วนของแรงต่อแรง",
         ("นิวตัน", "นิวตันต่อตารางเมตร", "นิวตันต่อกิโลกรัม"),
         "หน่วยของแรงทั้งเศษและส่วนตัดกันหมด"),
        ("ข้อใดถูกต้องเกี่ยวกับสัมประสิทธิ์ความเสียดทานสถิตและจลน์ของผิวสัมผัสคู่เดียวกัน",
         "สัมประสิทธิ์ความเสียดทานสถิตมีค่ามากกว่าสัมประสิทธิ์ความเสียดทานจลน์",
         ("สัมประสิทธิ์ความเสียดทานสถิตมีค่าน้อยกว่าจลน์เสมอ",
          "ทั้งสองค่าเท่ากันเสมอ",
          "สัมประสิทธิ์ความเสียดทานจลน์มีค่าเป็นศูนย์"),
         "ต้องออกแรงมากกว่าเพื่อทำให้วัตถุเริ่มเคลื่อนที่ มากกว่าเพื่อให้เคลื่อนที่ต่อไป"),
        ("แรงเสียดทานที่ผิวสัมผัสคู่หนึ่ง ๆ ขึ้นกับสิ่งใด",
         "สัมประสิทธิ์ความเสียดทานและแรงตั้งฉากที่ผิวสัมผัสกดกัน",
         ("พื้นที่ผิวสัมผัสและความเร็วของวัตถุ",
          "ปริมาตรของวัตถุและชนิดของของเหลว",
          "มวลของวัตถุเพียงอย่างเดียว โดยไม่ขึ้นกับชนิดของผิว"),
         "f = μN — ชนิดของผิวอยู่ใน μ ส่วนน้ำหนักที่กดลงอยู่ใน N"),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            k = rng.choice((2, 3, 4))
            thing = rng.choice(("กล่อง", "ลังไม้", "ก้อนอิฐ", "ตู้"))
            return _labelled(
                stem=(f"วาง{thing}บนพื้นเดิม แล้วเพิ่มน้ำหนักที่กดลงบนพื้นเป็น {k} เท่า "
                      "สัมประสิทธิ์ความเสียดทานและแรงเสียดทานจะเป็นอย่างไร"),
                correct=f"สัมประสิทธิ์เท่าเดิม แต่แรงเสียดทานเพิ่มเป็น {k} เท่า",
                wrongs=(f"สัมประสิทธิ์เพิ่มเป็น {k} เท่า แต่แรงเสียดทานเท่าเดิม", f"ทั้งสองเพิ่มเป็น {k} เท่า",
                        "ทั้งสองเท่าเดิม"),
                topic=TOPIC_FRICTION_COEFFICIENT,
                hint="μ ขึ้นกับคู่ผิวสัมผัสเท่านั้น ส่วน f = μN จึงเพิ่มตาม N",
            )
        if roll < 0.7:
            (a, mu_a), (b, mu_b) = rng.sample(MU_PAIRS, 2)
            first, second = rng.sample(((a, mu_a), (b, mu_b)), 2)
            hard = a if mu_a > mu_b else b
            easy = b if mu_a > mu_b else a
            return _labelled(
                stem=(f"กล่องใบเดียวกันวางบน{first[0]} (μ = {first[1]:g}) และบน{second[0]} (μ = {second[1]:g}) "
                      "ลากบนผิวใดต้องใช้แรงมากกว่า"),
                correct=f"บน{hard} เพราะ μ มากกว่า แรงเสียดทาน μN จึงมากกว่า",
                wrongs=(f"บน{easy} เพราะ μ น้อยกว่า แรงเสียดทานจึงมากกว่า", "ใช้แรงเท่ากัน เพราะเป็นกล่องใบเดียวกัน",
                        f"บน{easy} เพราะ μ มากกว่า แรงเสียดทาน μN จึงมากกว่า"),
                topic=TOPIC_FRICTION_COEFFICIENT,
                hint="N เท่ากันเพราะกล่องใบเดียวกัน แรงเสียดทานจึงขึ้นกับ μ",
            )
        stem, correct, wrongs, hint = rng.choice(self.FACTS)
        return _labelled(stem=stem, correct=correct, wrongs=wrongs,
                         topic=TOPIC_FRICTION_COEFFICIENT, hint=hint)


@question_type(
    "phys.friction_coefficient_fluency",
    display_name={"th": "คำนวณสัมประสิทธิ์ความเสียดทานจากแรงลากและน้ำหนัก"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FRICTION_COEFFICIENT,
)
class FrictionCoefficientFluency(QuestionType):
    """The sheet's own shape: a measured pull and a mass, giving μ = f/N."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        mass, mu, force = rng.choice(FRICTION_POOL)
        normal = mass * G
        surface = rng.choice(SURFACES)
        return _numeric(
            stem=(f"ลากวัตถุมวล {_num(mass)} กิโลกรัม ไปตาม{surface}ในแนวราบด้วยความเร็วคงที่ "
                  f"ต้องออกแรง {_num(force)} นิวตัน จงหาสัมประสิทธิ์ความเสียดทานระหว่างวัตถุกับพื้น "
                  f"(กำหนดให้ g = {G} เมตรต่อวินาที²)"),
            answer=mu, unit="",
            # Inverting the ratio, and dividing by the mass instead of the weight,
            # are the two mistakes this item exists to catch.
            slips=(normal / force, force / mass, mu * 2, mu / 2),
            fillers=(mu + 0.5, mu + 1, mu + 1.5),
            topic=TOPIC_FRICTION_COEFFICIENT,
            hint="ลากด้วยความเร็วคงที่ แรงลากเท่ากับแรงเสียดทาน จาก f = μN และ N = mg จะได้ μ = f / mg",
        )


@question_type(
    "phys.friction_coefficient_application",
    display_name={"th": "ใช้ f = μN หาแรงที่ต้องออกและตัดสินว่าวัตถุจะเคลื่อนที่หรือไม่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FRICTION_COEFFICIENT,
)
class FrictionCoefficientApplication(QuestionType):
    """Run f = μN the other way: the force needed, or whether a push is enough."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        mass, mu, force = rng.choice(FRICTION_POOL)
        normal = mass * G
        surface = rng.choice(SURFACES)
        if rng.random() < 0.5:
            return _numeric(
                stem=(f"วัตถุมวล {_num(mass)} กิโลกรัม วางนิ่งบน{surface} "
                      f"สัมประสิทธิ์ความเสียดทานสถิตระหว่างผิวสัมผัสเท่ากับ {_num(mu)} "
                      f"ต้องออกแรงในแนวราบอย่างน้อยเท่าใดวัตถุจึงจะเริ่มเคลื่อนที่ "
                      f"(กำหนดให้ g = {G} เมตรต่อวินาที²)"),
                answer=force, unit="นิวตัน",
                # Multiplying μ by the mass rather than the weight, and dividing
                # where the formula multiplies.
                slips=(mu * mass, normal / mu if mu else None, normal, force * 2),
                fillers=(force + 1, force + 2, force + 5),
                topic=TOPIC_FRICTION_COEFFICIENT,
                hint=f"แรงเสียดทานสถิตสูงสุด f = μN โดย N = mg = {_num(normal)} นิวตัน",
            )
        # Given the friction force and μ, recover the normal force — the sheet's
        # ข้อ 17 and ข้อ 23 shape.
        return _numeric(
            stem=(f"ออกแรง {_num(force)} นิวตัน ลากวัตถุไปตาม{surface}ในแนวราบด้วยความเร็วคงที่ "
                  f"ถ้าสัมประสิทธิ์ความเสียดทานระหว่างผิวสัมผัสเท่ากับ {_num(mu)} "
                  f"จงหาน้ำหนักของวัตถุ"),
            answer=normal, unit="นิวตัน",
            slips=(force * mu, mass, force / (mu * mu) if mu else None, normal * 2),
            fillers=(normal + 5, normal + 10, normal + 20),
            topic=TOPIC_FRICTION_COEFFICIENT,
            hint="จาก f = μN จะได้ N = f / μ และ N เท่ากับน้ำหนักของวัตถุเมื่อวางบนพื้นราบ",
        )
