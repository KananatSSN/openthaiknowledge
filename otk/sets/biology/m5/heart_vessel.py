"""โครงสร้างและการทำงานของหัวใจและหลอดเลือด

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/10

Sets moved here from: science_wave_f61.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f61 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_HEART = "โครงสร้างและการทำงานของหัวใจและหลอดเลือด"


HEART_PARTS = (
    ("หัวใจห้องล่างซ้าย", "มีผนังหนาที่สุด เพราะสูบฉีดเลือดไปทั่วร่างกาย"),
    ("ลิ้นไตรคัสพิด", "กั้นระหว่างหัวใจห้องบนขวาและห้องล่างขวา"),
    ("ลิ้นไบคัสพิด", "กั้นระหว่างหัวใจห้องบนซ้ายและห้องล่างซ้าย"),
    ("ลิ้นเซมิลูนาร์", "อยู่ที่โคนเอออร์ตาและพัลโมนารีอาร์เทอรี กันเลือดไหลย้อนเข้าหัวใจห้องล่าง"),
    ("เอสเอโนด (SA node)", "เป็นตัวกำหนดจังหวะการเต้นของหัวใจ อยู่ที่ผนังหัวใจห้องบนขวา"),
    ("เอวีโนด (AV node)", "รับกระแสไฟฟ้าจากห้องบนแล้วส่งต่อไปยังห้องล่าง"),
)


VESSELS = {
    "อาร์เทอรี": ("ผนังหนา มีกล้ามเนื้อเรียบและเส้นใยยืดหยุ่นมาก", "นำเลือดออกจากหัวใจด้วยความดันสูง"),
    "เวน": ("ผนังบางกว่า มีลิ้นกันเลือดไหลย้อนกลับ", "นำเลือดกลับเข้าหัวใจด้วยความดันต่ำ"),
    "หลอดเลือดฝอย": ("ผนังบางเพียงชั้นเดียว", "เป็นที่แลกเปลี่ยนสารระหว่างเลือดกับเซลล์"),
}


HEART_HINT = ("หัวใจห้องล่างซ้ายหนาที่สุด ลิ้นไตรคัสพิดอยู่ด้านขวา ไบคัสพิดอยู่ด้านซ้าย SA node กำหนดจังหวะ "
              "อาร์เทอรีผนังหนาความดันสูง เวนผนังบางมีลิ้น หลอดเลือดฝอยผนังชั้นเดียว")


@question_type(
    "biology.heart_vessel_foundation",
    display_name={"th": "ส่วนประกอบของหัวใจและหน้าที่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HEART,
)
class HeartVesselFoundation(QuestionType):
    """Chambers, valves and the pacemaker."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part, role = rng.choice(HEART_PARTS)
        others = rng.sample([p for p in HEART_PARTS if p[0] != part], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{part}มีลักษณะหรือหน้าที่อย่างไร", correct=role, wrongs=tuple(p[1] for p in others), topic=TOPIC_HEART,
                             hint=HEART_HINT)
        return _labelled(stem=f"ส่วนใดของหัวใจ{role}", correct=part, wrongs=tuple(p[0] for p in others), topic=TOPIC_HEART, hint=HEART_HINT)


@question_type(
    "biology.heart_vessel_fluency",
    display_name={"th": "เปรียบเทียบอาร์เทอรี เวน และหลอดเลือดฝอย"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HEART,
)
class HeartVesselFluency(QuestionType):
    """Wall, valves, pressure and job of each vessel."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        vessel = rng.choice(sorted(VESSELS))
        feature = rng.choice(VESSELS[vessel])
        others = [v for v in VESSELS if v != vessel]
        if rng.random() < 0.5:
            return _labelled(stem=f"หลอดเลือดที่ \"{feature}\" คือหลอดเลือดชนิดใด", correct=vessel, wrongs=(*others, "หลอดน้ำเหลือง"),
                             topic=TOPIC_HEART, hint=HEART_HINT)
        pool = [f for v in others for f in VESSELS[v]]
        return _labelled(stem=f"ข้อใดเป็นลักษณะของ{vessel}", correct=feature, wrongs=tuple(pool), topic=TOPIC_HEART,
                         hint=HEART_HINT)


@question_type(
    "biology.heart_vessel_application",
    display_name={"th": "คำนวณปริมาณเลือดที่หัวใจสูบฉีดและอ่านค่าความดันเลือด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HEART,
)
class HeartVesselApplication(QuestionType):
    """Cardiac output = heart rate × stroke volume; systolic over diastolic."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.6:
            rate = rng.randint(60, 100)
            stroke = rng.randrange(60, 91, 10)
            output = Fraction(rate * stroke, 1000)
            if rng.random() < 0.6:
                return numeric(stem=f"หัวใจเต้น {rate} ครั้งต่อนาที บีบเลือดออกครั้งละ {stroke} mL หัวใจสูบฉีดเลือดกี่ลิตรต่อนาที", answer=output,
                               wrongs=[rate * stroke, Fraction(rate + stroke, 1000) if (Fraction(rate + stroke, 1000) * 100).denominator == 1
                                       else output * 2, output * 60], unit="ลิตรต่อนาที", topic=TOPIC_HEART,
                               hint="ปริมาณเลือดที่สูบฉีดต่อนาที = อัตราการเต้น × ปริมาตรต่อครั้ง แล้วแปลง mL เป็นลิตร")
            return numeric(stem=f"หัวใจสูบฉีดเลือด {show(output)} ลิตรต่อนาที เต้น {rate} ครั้งต่อนาที บีบเลือดออกครั้งละกี่มิลลิลิตร",
                           answer=stroke, wrongs=[rate, output * 1000, stroke * 2], unit="mL", topic=TOPIC_HEART,
                           hint="ปริมาตรต่อครั้ง = ปริมาณเลือดต่อนาที (mL) ÷ อัตราการเต้น")
        systolic = rng.randrange(100, 161, 5)
        diastolic = rng.randrange(60, min(100, systolic - 30) + 1, 5)
        if rng.random() < 0.5:
            return _labelled(stem=f"วัดความดันเลือดได้ {systolic}/{diastolic} mmHg ตัวเลข {systolic} หมายถึงข้อใด",
                             correct="ความดันขณะหัวใจห้องล่างบีบตัว (ซิสโทลี)",
                             wrongs=("ความดันขณะหัวใจห้องล่างคลายตัว (ไดแอสโทลี)", "อัตราการเต้นของหัวใจต่อนาที", "ปริมาตรเลือดที่บีบออกต่อครั้ง"),
                             topic=TOPIC_HEART, hint="ค่าบนคือความดันขณะหัวใจบีบตัว ค่าล่างคือความดันขณะหัวใจคลายตัว")
        return numeric(stem=f"วัดความดันเลือดได้ {systolic}/{diastolic} mmHg ผลต่างระหว่างความดันขณะหัวใจบีบตัวและคลายตัว (ความดันชีพจร) เป็นกี่ mmHg",
                       answer=systolic - diastolic, wrongs=[systolic + diastolic, systolic, diastolic], unit="mmHg",
                       topic=TOPIC_HEART, hint="ความดันชีพจร = ค่าบน − ค่าล่าง")
