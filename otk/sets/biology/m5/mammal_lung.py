"""โครงสร้างของปอดสัตว์เลี้ยงลูกด้วยน้ำนม

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/5

Sets moved here from: science_wave_f60.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f60 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_LUNG = "โครงสร้างของปอดสัตว์เลี้ยงลูกด้วยน้ำนม"


AIRWAY = ("รูจมูก", "โพรงจมูก", "คอหอย", "กล่องเสียง", "ท่อลม", "หลอดลม", "หลอดลมฝอย", "ถุงลม")


LUNG_PARTS = (
    ("ท่อลม", "มีกระดูกอ่อนรูปตัว C เรียงเป็นระยะ ทำให้ท่อไม่แฟบ"),
    ("เยื่อบุท่อทางเดินหายใจ", "มีซิเลียและเมือกดักจับฝุ่นและจุลินทรีย์"),
    ("ถุงลม", "ผนังบางชั้นเดียว มีหลอดเลือดฝอยล้อมรอบจำนวนมาก เป็นที่แลกเปลี่ยนแก๊ส"),
    ("เยื่อหุ้มปอด", "เป็นเยื่อสองชั้นที่มีของเหลวอยู่ระหว่างกันช่วยลดแรงเสียดทาน"),
    ("กล่องเสียง", "มีเส้นเสียงและฝาปิดกล่องเสียงกันอาหารตกลงหลอดลม"),
    ("หลอดลมฝอย", "เป็นท่อเล็กที่แตกแขนงมากและไม่มีกระดูกอ่อนหุ้ม"),
)


LUNG_HINT = "อากาศผ่านรูจมูก โพรงจมูก คอหอย กล่องเสียง ท่อลม หลอดลม หลอดลมฝอย แล้วถึงถุงลมที่แลกเปลี่ยนแก๊ส"


@question_type(
    "biology.mammal_lung_foundation",
    display_name={"th": "ทางเดินของอากาศจากจมูกถึงถุงลม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LUNG,
)
class MammalLungFoundation(QuestionType):
    """The order of the airway."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            i = rng.randrange(len(AIRWAY) - 1)
            nxt = AIRWAY[i + 1]
            pool = [a for a in AIRWAY if a not in (AIRWAY[i], nxt)] + ["หลอดอาหาร"]
            return _labelled(stem=f"อากาศที่ผ่าน{AIRWAY[i]}แล้วจะผ่านส่วนใดต่อไป", correct=nxt, wrongs=tuple(pool),
                             topic=TOPIC_LUNG, hint=LUNG_HINT)
        start = rng.randrange(len(AIRWAY) - 3)
        chunk = list(AIRWAY[start:start + 4])
        wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
        while len(wrongs) < 3:
            c = chunk[:]
            rng.shuffle(c)
            if c != chunk:
                wrongs[" → ".join(c)] = None
        return _labelled(stem="ข้อใดเรียงลำดับทางเดินของอากาศขณะหายใจเข้าได้ถูกต้อง", correct=" → ".join(chunk), wrongs=tuple(wrongs),
                         topic=TOPIC_LUNG, hint=LUNG_HINT)


@question_type(
    "biology.mammal_lung_fluency",
    display_name={"th": "ลักษณะและหน้าที่ของโครงสร้างในระบบหายใจ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LUNG,
)
class MammalLungFluency(QuestionType):
    """What each part looks like in a dissected lung, and why."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part, looks = rng.choice(LUNG_PARTS)
        others = rng.sample([p for p in LUNG_PARTS if p[0] != part], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"จากการสังเกตปอดหมู {part}มีลักษณะหรือหน้าที่อย่างไร", correct=looks, wrongs=tuple(p[1] for p in others),
                             topic=TOPIC_LUNG, hint=LUNG_HINT)
        return _labelled(stem=f"โครงสร้างใดในระบบหายใจ{looks}", correct=part, wrongs=tuple(p[0] for p in others), topic=TOPIC_LUNG,
                         hint=LUNG_HINT)


@question_type(
    "biology.mammal_lung_application",
    display_name={"th": "คำนวณพื้นที่ผิวของถุงลม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LUNG,
)
class MammalLungApplication(QuestionType):
    """Millions of alveoli times the area of each: tens of square metres."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        millions = rng.randrange(200, 601, 20)
        each = rng.choice((Fraction(1, 5), Fraction(1, 4), Fraction(3, 10), Fraction(1, 10)))
        total = millions * each  # 10⁶ × mm² = m²
        if rng.random() < 0.6:
            return numeric(stem=f"ปอดของคนมีถุงลมประมาณ {millions} ล้านถุง แต่ละถุงมีพื้นที่ผิวเฉลี่ย {show(each)} mm² "
                                f"พื้นที่ผิวรวมของถุงลมเป็นกี่ตารางเมตร", answer=total,
                           wrongs=[total * 1000, total / 10, millions], unit="m²", topic=TOPIC_LUNG,
                           hint="1 m² = 1,000,000 mm² ดังนั้น (จำนวนล้านถุง × พื้นที่ต่อถุงเป็น mm²) ได้ผลเป็น m² โดยตรง")
        return numeric(stem=f"ถุงลมมีพื้นที่ผิวรวม {show(total)} m² ถ้าแต่ละถุงมีพื้นที่ผิว {show(each)} mm² มีถุงลมประมาณกี่ล้านถุง",
                       answer=millions, wrongs=[total, millions * 10, Fraction(millions, 10)], unit="ล้านถุง", topic=TOPIC_LUNG,
                       hint="จำนวนถุง (ล้าน) = พื้นที่รวม (m²) ÷ พื้นที่ต่อถุง (mm²)")
