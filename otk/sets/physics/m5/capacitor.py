"""ตัวเก็บประจุและความจุไฟฟ้า

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.5/5

Sets moved here from: science_wave_f11.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f11 import SUBJECT, UPPER_FIVE, _exact

PROVENANCE = Provenance("original")


TOPIC_CAPACITOR = "ตัวเก็บประจุและความจุไฟฟ้า"


CAPACITOR_FACTS = (
    ("ตัวเก็บประจุแบบแผ่นโลหะคู่ขนานประกอบด้วยอะไร", "แผ่นตัวนำสองแผ่นวางขนานกันโดยมีฉนวนคั่นกลาง",
     ("แผ่นฉนวนสองแผ่นมีตัวนำคั่นกลาง", "ขดลวดพันรอบแกนเหล็ก", "แผ่นตัวนำแผ่นเดียวต่อลงดิน")),
    ("เมื่อตัวเก็บประจุถูกอัดประจุเต็มที่ แผ่นทั้งสองมีประจุอย่างไร", "ขนาดเท่ากันแต่ชนิดตรงข้ามกัน",
     ("ขนาดเท่ากันและชนิดเดียวกัน", "มีประจุเฉพาะแผ่นที่ต่อขั้วบวก", "ไม่มีประจุทั้งสองแผ่น")),
    ("ความจุของตัวเก็บประจุแบบแผ่นขนานเพิ่มขึ้นเมื่อใด", "พื้นที่แผ่นมากขึ้นหรือระยะห่างระหว่างแผ่นน้อยลง",
     ("พื้นที่แผ่นน้อยลง", "ระยะห่างระหว่างแผ่นมากขึ้น", "ความต่างศักย์ที่ต่อมากขึ้น")),
    ("หน่วยของความจุไฟฟ้าคือข้อใด", "ฟารัด (F) ซึ่งเท่ากับคูลอมบ์ต่อโวลต์",
     ("โวลต์ต่อคูลอมบ์", "จูลต่อคูลอมบ์", "แอมแปร์ต่อวินาที")),
    ("ต่อตัวเก็บประจุแบบขนาน ปริมาณใดเท่ากันทุกตัว", "ความต่างศักย์คร่อมแต่ละตัว",
     ("ประจุบนแต่ละตัว", "พลังงานที่สะสมในแต่ละตัว", "ความจุของแต่ละตัว")),
    ("ต่อตัวเก็บประจุแบบอนุกรม ปริมาณใดเท่ากันทุกตัว", "ประจุบนแต่ละตัว",
     ("ความต่างศักย์คร่อมแต่ละตัว", "พลังงานที่สะสมในแต่ละตัว", "ความจุของแต่ละตัว")),
)


@question_type(
    "phys.capacitor_foundation",
    display_name={"th": "ส่วนประกอบของตัวเก็บประจุและความสัมพันธ์ Q = CV"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CAPACITOR,
)
class CapacitorFoundation(QuestionType):
    """What a capacitor is, and Q = CV each way round."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            stem, correct, wrongs = rng.choice(CAPACITOR_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_CAPACITOR,
                             hint="ตัวเก็บประจุคือตัวนำสองแผ่นคั่นด้วยฉนวน เก็บประจุได้ Q = CV")
        c = rng.choice((1, 2, 4, 5, 10, 20, 22, 47, 50, 100))
        v = rng.randint(2, 50)
        if shape == 1:
            return numeric(stem=f"ตัวเก็บประจุความจุ {c} μF ต่อกับความต่างศักย์ {v} V เก็บประจุได้กี่ไมโครคูลอมบ์",
                           answer=c * v, wrongs=[Fraction(c, v), Fraction(v, c), c + v], unit="μC",
                           topic=TOPIC_CAPACITOR, hint="Q = CV")
        return numeric(stem=f"ตัวเก็บประจุเก็บประจุ {c * v} μC เมื่อต่อกับความต่างศักย์ {v} V มีความจุกี่ไมโครฟารัด",
                       answer=c, wrongs=[c * v * v, Fraction(v, 1), c * 2], unit="μF",
                       topic=TOPIC_CAPACITOR, hint="C = Q/V")


@question_type(
    "phys.capacitor_fluency",
    display_name={"th": "คำนวณพลังงานสะสมในตัวเก็บประจุ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CAPACITOR,
)
class CapacitorFluency(QuestionType):
    """U = ½CV² = ½QV = Q²/2C, in millijoules."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        c, v = rng.choice([(c, v) for c in (1, 2, 4, 5, 10, 20, 50, 100, 200, 500, 1000) for v in range(2, 101)
                           if _exact(Fraction(c * v * v, 2000)) and Fraction(c * v * v, 2000) >= Fraction(1, 100)])
        energy = Fraction(c * v * v, 2000)
        hint = "U = ½CV² = ½QV (C เป็นฟารัด ได้พลังงานเป็นจูล 1 J = 1,000 mJ)"
        if rng.random() < 0.5:
            return numeric(stem=f"ตัวเก็บประจุความจุ {c:,} μF อัดประจุด้วยความต่างศักย์ {v} V สะสมพลังงานกี่มิลลิจูล",
                           answer=energy, wrongs=[energy * 2, Fraction(c * v, 2000), energy * 1000], unit="mJ",
                           topic=TOPIC_CAPACITOR, hint=hint)
        return numeric(stem=f"ตัวเก็บประจุมีประจุ {c * v:,} μC และความต่างศักย์ {v} V สะสมพลังงานกี่มิลลิจูล",
                       answer=energy, wrongs=[energy * 2, Fraction(c * v * v * v, 2000) if v < 20 else energy / 2,
                                              energy * 1000], unit="mJ", topic=TOPIC_CAPACITOR, hint=hint)


@question_type(
    "phys.capacitor_application",
    display_name={"th": "ความจุสมมูลของตัวเก็บประจุที่ต่อแบบอนุกรมและแบบขนาน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CAPACITOR,
)
class CapacitorApplication(QuestionType):
    """Parallel capacitances add; in series the reciprocals add and the charge is shared."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            caps = rng.sample((1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20), rng.choice((2, 3)))
            listed = " ".join(f"{c} μF" for c in caps)
            return numeric(stem=f"ต่อตัวเก็บประจุ {listed} แบบขนาน ความจุสมมูลเท่าใด",
                           answer=sum(caps), wrongs=[1 / sum(Fraction(1, c) for c in caps), max(caps), sum(caps) * 2],
                           unit="μF", topic=TOPIC_CAPACITOR, hint="ต่อขนาน ความจุสมมูล = ผลรวมของความจุ")
        pairs = [(a, b) for a in (2, 3, 4, 6, 8, 10, 12, 15, 20, 30, 60) for b in (2, 3, 4, 6, 8, 10, 12, 15, 20, 30, 60)
                 if a < b and _exact(Fraction(a * b, a + b))]
        a, b = rng.choice(pairs)
        series = Fraction(a * b, a + b)
        if shape == 1:
            return numeric(stem=f"ต่อตัวเก็บประจุ {a} μF และ {b} μF แบบอนุกรม ความจุสมมูลเท่าใด",
                           answer=series, wrongs=[a + b, Fraction(a + b, 2), b - a], unit="μF", topic=TOPIC_CAPACITOR,
                           hint="ต่ออนุกรม 1/C = 1/C₁ + 1/C₂ ความจุสมมูลน้อยกว่าตัวที่น้อยที่สุด")
        v = rng.choice([x for x in range(2, 61) if _exact(series * x) and _exact(series * x / a)])
        q = series * v
        return numeric(
            stem=(f"ต่อตัวเก็บประจุ {a} μF และ {b} μF แบบอนุกรมกับแบตเตอรี่ {v} V "
                  f"ความต่างศักย์คร่อมตัวเก็บประจุ {a} μF เท่าใด"),
            answer=q / a, wrongs=[q / b, Fraction(v, 2), v], unit="V", topic=TOPIC_CAPACITOR,
            hint="ต่ออนุกรมประจุเท่ากันทุกตัว: หา Q = C_รวม × V แล้ว V₁ = Q/C₁ (ตัวที่ความจุน้อยได้ความต่างศักย์มาก)")
