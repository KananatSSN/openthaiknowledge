"""ระบบหมุนเวียนเลือดแบบเปิดและแบบปิด

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/8

Sets moved here from: science_wave_f61.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f61 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_CIRC = "ระบบหมุนเวียนเลือดแบบเปิดและแบบปิด"


OPEN = ("แมลง", "กุ้ง", "หอยทาก", "แมงมุม", "หอยกาบ")


CLOSED = ("ไส้เดือนดิน", "หมึก", "ปลา", "กบ", "นก", "คน")


CIRC_FEATURES = {
    "แบบเปิด": ("เลือดไหลออกจากหลอดเลือดไปอยู่ในช่องว่างในลำตัว (ฮีโมซีล) แล้วจึงกลับเข้าหัวใจ",
                "เลือดสัมผัสกับเนื้อเยื่อโดยตรงและไหลช้า"),
    "แบบปิด": ("เลือดไหลอยู่ในหลอดเลือดตลอด แลกเปลี่ยนสารผ่านหลอดเลือดฝอย",
               "เลือดไหลได้เร็วและควบคุมการกระจายเลือดไปยังอวัยวะได้ดีกว่า"),
}


CIRC_HINT = ("แมลง กุ้ง และหอยส่วนใหญ่มีระบบเปิด ไส้เดือนดิน หมึก และสัตว์มีกระดูกสันหลังมีระบบปิด "
             "ปลามีหัวใจ 2 ห้อง สัตว์สะเทินน้ำสะเทินบก 3 ห้อง นกและสัตว์เลี้ยงลูกด้วยน้ำนม 4 ห้อง")


HEARTS = (("ปลา", 2, "1 ห้องบน 1 ห้องล่าง เลือดผ่านหัวใจครั้งเดียวต่อรอบ"),
          ("กบ", 3, "2 ห้องบน 1 ห้องล่าง เลือดที่มีออกซิเจนสูงและต่ำผสมกันบ้างในห้องล่าง"),
          ("นก", 4, "2 ห้องบน 2 ห้องล่าง แยกเลือดที่มีออกซิเจนสูงและต่ำได้สมบูรณ์"),
          ("คน", 4, "2 ห้องบน 2 ห้องล่าง แยกเลือดที่มีออกซิเจนสูงและต่ำได้สมบูรณ์"),
          ("จระเข้", 4, "2 ห้องบน 2 ห้องล่าง แยกเลือดที่มีออกซิเจนสูงและต่ำได้สมบูรณ์"))


@question_type(
    "biology.circulation_type_foundation",
    display_name={"th": "สัตว์ที่มีระบบหมุนเวียนเลือดแบบเปิดและแบบปิด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CIRC,
)
class CirculationTypeFoundation(QuestionType):
    """Open or closed, by animal."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        is_open = rng.random() < 0.5
        same, other = (OPEN, CLOSED) if is_open else (CLOSED, OPEN)
        kind = "แบบเปิด" if is_open else "แบบปิด"
        if rng.random() < 0.5:
            animal = rng.choice(same)
            return _labelled(stem=f"{animal}มีระบบหมุนเวียนเลือดแบบใด", correct=f"ระบบหมุนเวียนเลือด{kind}",
                             wrongs=(f"ระบบหมุนเวียนเลือด{'แบบปิด' if is_open else 'แบบเปิด'}", "ไม่มีระบบหมุนเวียนเลือด",
                                     "ใช้ระบบท่อลมแทนระบบหมุนเวียนเลือดทั้งหมด"), topic=TOPIC_CIRC, hint=CIRC_HINT)
        return _labelled(stem=f"สัตว์ใดมีระบบหมุนเวียนเลือด{kind}", correct=rng.choice(same), wrongs=tuple(other),
                         topic=TOPIC_CIRC, hint=CIRC_HINT)


@question_type(
    "biology.circulation_type_fluency",
    display_name={"th": "เปรียบเทียบระบบหมุนเวียนเลือดแบบเปิดและแบบปิด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CIRC,
)
class CirculationTypeFluency(QuestionType):
    """Where the blood goes in each."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(CIRC_FEATURES))
        other = next(k for k in CIRC_FEATURES if k != kind)
        feature = rng.choice(CIRC_FEATURES[kind])
        if rng.random() < 0.5:
            return _labelled(stem=f"ข้อใดเป็นลักษณะของระบบหมุนเวียนเลือด{kind}", correct=feature,
                             wrongs=(*CIRC_FEATURES[other], "ไม่มีหัวใจสูบฉีดเลือด"), topic=TOPIC_CIRC, hint=CIRC_HINT)
        return _labelled(stem=f"ระบบหมุนเวียนเลือดที่ \"{feature}\" เป็นแบบใด และพบในสัตว์ใด",
                         correct=f"{kind} เช่น {rng.choice(OPEN if kind == 'แบบเปิด' else CLOSED)}",
                         wrongs=(f"{other} เช่น {rng.choice(OPEN if other == 'แบบเปิด' else CLOSED)}",
                                 f"{kind} เช่น {rng.choice(CLOSED if kind == 'แบบเปิด' else OPEN)}",
                                 f"{other} เช่น {rng.choice(CLOSED if other == 'แบบเปิด' else OPEN)}"),
                         topic=TOPIC_CIRC, hint=CIRC_HINT)


@question_type(
    "biology.circulation_type_application",
    display_name={"th": "จำนวนห้องหัวใจและการไหลเวียนเลือดของสัตว์มีกระดูกสันหลัง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CIRC,
)
class CirculationTypeApplication(QuestionType):
    """Two, three or four chambers; one loop or two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        animal, chambers, detail = rng.choice(HEARTS)
        if rng.random() < 0.5:
            return numeric(stem=f"หัวใจของ{animal}มีกี่ห้อง", answer=chambers, wrongs=[c for c in (2, 3, 4, 1) if c != chambers],
                           unit="ห้อง", topic=TOPIC_CIRC, hint=CIRC_HINT)
        roll = rng.random()
        if roll < 0.3:
            loops = 1 if animal == "ปลา" else 2
            return numeric(stem=f"เลือดของ{animal}ไหลผ่านหัวใจกี่ครั้งในการไหลเวียนครบหนึ่งรอบทั่วร่างกาย", answer=loops,
                           wrongs=[3 - loops, 4, 3], unit="ครั้ง", topic=TOPIC_CIRC,
                           hint="ปลามีการไหลเวียนรอบเดียว (หัวใจ → เหงือก → ร่างกาย) สัตว์บกมีการไหลเวียนสองวงจร ผ่านหัวใจ 2 ครั้ง")
        details = sorted(({h[2] for h in HEARTS} | {"ไม่มีห้องหัวใจ ใช้หลอดเลือดบีบตัวแทน", "1 ห้องบน 2 ห้องล่าง เลือดไหลย้อนกลับได้ตลอด"})
                         - {detail})
        return _labelled(stem=f"หัวใจของ{animal}มีลักษณะอย่างไร", correct=detail, wrongs=tuple(details), topic=TOPIC_CIRC,
                         hint=CIRC_HINT)
