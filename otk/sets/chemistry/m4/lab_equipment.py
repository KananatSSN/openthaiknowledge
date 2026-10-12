"""การเลือกและใช้อุปกรณ์ในการทำปฏิบัติการเคมี

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 3 ม.4/2

Sets moved here from: science_wave_f41.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f41 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_EQUIPMENT = "การเลือกและใช้อุปกรณ์ในการทำปฏิบัติการเคมี"


# (equipment, what it is for, how finely it reads)
EQUIPMENT = (
    ("ขวดกำหนดปริมาตร", "เตรียมสารละลายให้มีปริมาตรแน่นอนตามขีดบอกปริมาตรเพียงขีดเดียว", "ละเอียดสูง"),
    ("ปิเปตต์แบบปริมาตร", "ถ่ายเทสารละลายปริมาตรที่แน่นอนค่าเดียว เช่น 25.00 cm³", "ละเอียดสูง"),
    ("บิวเรตต์", "หยดสารละลายและอ่านปริมาตรที่ใช้ในการไทเทรต", "ละเอียดสูง อ่านได้ทศนิยม 2 ตำแหน่ง"),
    ("กระบอกตวง", "ตวงปริมาตรของเหลวโดยประมาณได้หลายค่า", "ละเอียดปานกลาง"),
    ("บีกเกอร์", "ใส่ ผสม หรือให้ความร้อนแก่สาร ไม่ใช้วัดปริมาตรที่ต้องการความแม่นยำ", "หยาบ"),
    ("เครื่องชั่งไฟฟ้า", "ชั่งมวลของสาร", "ขึ้นกับรุ่น เช่น 0.01 g หรือ 0.0001 g"),
    ("ขวดรูปกรวย", "ใส่สารละลายที่ถูกไทเทรต หมุนเขย่าได้โดยไม่หก", "หยาบ"),
)


JOBS = (
    ("เตรียมสารละลาย NaCl 0.100 mol/dm³ ปริมาตร 250.00 cm³ ให้ได้ความเข้มข้นแม่นยำ", "ขวดกำหนดปริมาตร"),
    ("ดูดสารละลายกรด 25.00 cm³ ใส่ขวดรูปกรวยเพื่อไทเทรต", "ปิเปตต์แบบปริมาตร"),
    ("วัดปริมาตรเบสที่ใช้ไปในการไทเทรต", "บิวเรตต์"),
    ("ตวงน้ำประมาณ 50 cm³ เพื่อล้างตะกอน", "กระบอกตวง"),
    ("ต้มน้ำเพื่อละลายของแข็ง", "บีกเกอร์"),
    ("หามวลของ CuSO₄·5H₂O ที่ใช้เตรียมสารละลาย", "เครื่องชั่งไฟฟ้า"),
)


# (instrument, scale step, digits recorded)
READINGS = (("บิวเรตต์", Fraction(1, 10), 2), ("กระบอกตวงขนาด 100 cm³", Fraction(1), 1),
            ("กระบอกตวงขนาด 10 cm³", Fraction(1, 10), 2), ("เทอร์มอมิเตอร์ที่มีขีดทุก 1 °C", Fraction(1), 1))


@question_type(
    "chem.lab_equipment_foundation",
    display_name={"th": "หน้าที่ของอุปกรณ์ในห้องปฏิบัติการเคมี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EQUIPMENT,
)
class LabEquipmentFoundation(QuestionType):
    """What each piece is for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, use, _ = rng.choice(EQUIPMENT)
        others = [e for e in EQUIPMENT if e[0] != name]
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}ใช้ทำอะไร", correct=use, wrongs=tuple(e[1] for e in rng.sample(others, 3)),
                             topic=TOPIC_EQUIPMENT, hint="เครื่องแก้ววัดปริมาตรแต่ละชนิดมีความละเอียดและหน้าที่ต่างกัน")
        return _labelled(stem=f"อุปกรณ์ใดใช้{use}", correct=name, wrongs=tuple(e[0] for e in rng.sample(others, 3)),
                         topic=TOPIC_EQUIPMENT, hint="เครื่องแก้ววัดปริมาตรแต่ละชนิดมีความละเอียดและหน้าที่ต่างกัน")


@question_type(
    "chem.lab_equipment_fluency",
    display_name={"th": "เลือกอุปกรณ์ให้เหมาะกับงาน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EQUIPMENT,
)
class LabEquipmentFluency(QuestionType):
    """Precise work needs volumetric glassware; rough work does not."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        job, right = rng.choice(JOBS)
        others = [e[0] for e in EQUIPMENT if e[0] != right]
        return _labelled(stem=f"ต้องการ{job} ควรใช้อุปกรณ์ใด", correct=right, wrongs=tuple(others),
                         topic=TOPIC_EQUIPMENT, hint="งานที่ต้องการปริมาตรแน่นอนใช้ขวดกำหนดปริมาตร ปิเปตต์ หรือบิวเรตต์")


@question_type(
    "chem.lab_equipment_application",
    display_name={"th": "อ่านค่าและบันทึกผลการวัดให้ถูกต้อง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EQUIPMENT,
)
class LabEquipmentApplication(QuestionType):
    """Read to one digit past the smallest scale mark; a titre is final − initial."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            start = Fraction(rng.randrange(0, 1001, 5), 100)
            used = Fraction(rng.randrange(500, 3001, 5), 100)
            end = start + used
            return numeric(stem=f"การไทเทรตครั้งหนึ่ง อ่านบิวเรตต์ก่อนไทเทรตได้ {float(start):.2f} cm³ และหลังไทเทรตได้ {float(end):.2f} cm³ "
                                "ใช้สารละลายไปกี่ cm³",
                           answer=used, wrongs=[end, end + start, used + 1], unit="cm³", topic=TOPIC_EQUIPMENT,
                           hint="ปริมาตรที่ใช้ = ค่าที่อ่านได้หลังไทเทรต − ค่าก่อนไทเทรต")
        instrument, step, digits = rng.choice(READINGS)
        places = {Fraction(1, 10): 2, Fraction(1): 1}[step]
        value = Fraction(rng.randrange(100, 4000), 10 ** places)
        right = f"{float(value):.{places}f}"
        # Too few digits, too many digits, and the decimal point in the wrong place.
        wrongs = tuple(dict.fromkeys(w for w in (f"{float(value):.{places - 1}f}", f"{float(value):.{places + 1}f}",
                                                 f"{float(value) * 10:.{places}f}", f"{float(value) + 1:.{places}f}")
                                     if w != right))
        return _labelled(stem=f"อ่านค่าจาก{instrument} (ขีดสเกลเล็กที่สุด {show(step)}) ได้ค่าใกล้ {show(value)} ควรบันทึกผลอย่างไร",
                         correct=right, wrongs=wrongs[:3], topic=TOPIC_EQUIPMENT,
                         hint="บันทึกให้ละเอียดกว่าขีดสเกลเล็กที่สุดหนึ่งตำแหน่ง (ประมาณค่าหลักสุดท้าย)")
