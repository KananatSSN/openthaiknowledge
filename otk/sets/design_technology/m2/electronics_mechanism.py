"""กลไก ไฟฟ้า และอิเล็กทรอนิกส์

การออกแบบและเทคโนโลยี · ม.2 · สสวท. พื้นฐาน
Indicators: ว 4.1 ม.2/5

Sets moved here from: technology_t2s2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1 import SUBJECT
from otk.sets._support.technology_t2s2 import M2

PROVENANCE = Provenance("original")


PARTS_TOPIC = "กลไก ไฟฟ้า และอิเล็กทรอนิกส์"


COMPONENTS = (
    ("ตัวต้านทาน", "จำกัดปริมาณกระแสไฟฟ้าที่ไหลในวงจร"),
    ("ไดโอดเปล่งแสง (LED)", "เปล่งแสงเมื่อมีกระแสไฟฟ้าไหลผ่านในทิศที่ถูกต้อง"),
    ("ไดโอด", "ยอมให้กระแสไฟฟ้าไหลผ่านได้ทางเดียว"),
    ("ตัวเก็บประจุ", "เก็บประจุไฟฟ้าไว้และคายประจุออกมาได้"),
    ("ตัวต้านทานไวแสง (LDR)", "มีความต้านทานลดลงเมื่อได้รับแสงมากขึ้น"),
    ("สวิตช์", "ตัดหรือต่อวงจรไฟฟ้า"),
    ("มอเตอร์ไฟฟ้า", "เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานกล"),
    ("ออดหรือบัซเซอร์", "เปลี่ยนพลังงานไฟฟ้าเป็นเสียง"),
)


COLOURS = ("ดำ", "น้ำตาล", "แดง", "ส้ม", "เหลือง", "เขียว", "น้ำเงิน", "ม่วง", "เทา", "ขาว")


def ohms(value: int) -> str:
    return f"{value:,} โอห์ม"


MECHANISMS = (
    ("ลูกเบี้ยว", "เปลี่ยนการหมุนเป็นการเคลื่อนที่ขึ้นลง"),
    ("เฟืองกับแร็ก (เฟืองสะพาน)", "เปลี่ยนการหมุนเป็นการเลื่อนเป็นแนวตรง"),
    ("ข้อเหวี่ยงกับก้านต่อ", "เปลี่ยนการเคลื่อนที่ไปกลับเป็นการหมุน"),
    ("พูลเลย์กับสายพาน", "ส่งการหมุนจากแกนหนึ่งไปยังอีกแกนหนึ่งที่อยู่ห่างกัน"),
    ("เฟืองขนาดต่างกันสองตัว", "เปลี่ยนความเร็วและทิศทางการหมุน"),
    ("คาน", "ช่วยผ่อนแรงในการยกหรืองัดวัตถุ"),
)


@question_type(
    "tech.electronics_mechanism_foundation",
    display_name={"th": "บอกหน้าที่ของอุปกรณ์อิเล็กทรอนิกส์"},
    level=M2, subject=SUBJECT, topic=PARTS_TOPIC,
)
class ElectronicsMechanismFoundation(QuestionType):
    def build(self, rng: Random, **params):
        index = rng.randrange(len(COMPONENTS))
        part, job = COMPONENTS[index]
        others = rng.sample([row for i, row in enumerate(COMPONENTS) if i != index], 3)
        hint = "นึกถึงสิ่งที่อุปกรณ์ทำกับกระแสไฟฟ้า ทั้งจำกัด ปล่อยทางเดียว เก็บประจุ ตัดต่อ หรือเปลี่ยนเป็นพลังงานอื่น"
        if rng.random() < 0.5:
            return _labelled(stem=f"{part}ทำหน้าที่ใดในวงจร",
                             correct=job, wrongs=tuple(j for _, j in others), hint=hint, topic=PARTS_TOPIC)
        return _labelled(stem=f"อุปกรณ์ใด{job}",
                         correct=part, wrongs=tuple(p for p, _ in others), hint=hint, topic=PARTS_TOPIC)


@question_type(
    "tech.electronics_mechanism_fluency",
    display_name={"th": "อ่านค่าตัวต้านทานจากแถบสี"},
    level=M2, subject=SUBJECT, topic=PARTS_TOPIC,
)
class ElectronicsMechanismFluency(QuestionType):
    """Four-band code: two digits, a multiplier, and a gold tolerance band."""

    def build(self, rng: Random, **params):
        first, second, power = rng.randint(1, 9), rng.randint(0, 9), rng.randint(0, 4)
        value = (10 * first + second) * 10 ** power
        wrongs = {(10 * first + second) * 10 ** (power + 1), (10 * second + first) * 10 ** power,
                  (10 * first + second) * 10 ** max(power - 1, 0), (first + second) * 10 ** power,
                  (10 * first + second) * power if power else (10 * first + second) * 10 ** 2} - {value}
        wrongs = {w for w in wrongs if w > 0}
        step = 2
        while len(wrongs) < 3:
            wrongs.add(value * 10 ** step)
            step += 1
        bands = f"{COLOURS[first]} {COLOURS[second]} {COLOURS[power]} ทอง"
        return _labelled(
            stem=(f"ตัวต้านทานมีแถบสีเรียงจากซ้ายไปขวาเป็น {bands} "
                  f"กำหนดรหัสสี ดำ 0 น้ำตาล 1 แดง 2 ส้ม 3 เหลือง 4 เขียว 5 น้ำเงิน 6 ม่วง 7 เทา 8 ขาว 9 "
                  f"ตัวต้านทานนี้มีค่าเท่าใด"),
            correct=ohms(value), wrongs=tuple(ohms(w) for w in rng.sample(sorted(wrongs), 3)),
            hint="แถบที่หนึ่งและสองเป็นตัวเลขสองหลัก แถบที่สามบอกจำนวนศูนย์ที่ต่อท้าย แถบสีทองบอกค่าความคลาดเคลื่อน",
            topic=PARTS_TOPIC,
        )


@question_type(
    "tech.electronics_mechanism_application",
    display_name={"th": "เลือกกลไกให้ได้การเคลื่อนที่ที่ต้องการ"},
    level=M2, subject=SUBJECT, topic=PARTS_TOPIC,
)
class ElectronicsMechanismApplication(QuestionType):
    USES = {
        "ลูกเบี้ยว": "ของเล่นที่หมุนแกนแล้วให้ตุ๊กตากระโดดขึ้นลง",
        "เฟืองกับแร็ก (เฟืองสะพาน)": "ประตูเลื่อนที่ใช้มอเตอร์หมุนแล้วบานประตูเลื่อนเปิด",
        "ข้อเหวี่ยงกับก้านต่อ": "จักรเย็บผ้าแบบเท้าเหยียบที่เหยียบขึ้นลงแล้วล้อหมุน",
        "พูลเลย์กับสายพาน": "เครื่องที่มอเตอร์อยู่ด้านล่างแต่ต้องหมุนแกนที่อยู่ด้านบน",
        "เฟืองขนาดต่างกันสองตัว": "เครื่องกวนที่ต้องการให้ใบกวนหมุนช้ากว่ามอเตอร์",
        "คาน": "ที่งัดฝากระป๋องสีให้เปิดได้โดยออกแรงน้อย",
    }

    def build(self, rng: Random, **params):
        index = rng.randrange(len(MECHANISMS))
        name, motion = MECHANISMS[index]
        others = rng.sample([row for i, row in enumerate(MECHANISMS) if i != index], 3)
        hint = "ระบุว่าต้องการเปลี่ยนการเคลื่อนที่แบบใดเป็นแบบใด แล้วเลือกกลไกที่ทำได้"
        if rng.random() < 0.5:
            return _labelled(stem=f"ต้องการสร้าง{self.USES[name]} ควรใช้กลไกใด",
                             correct=name, wrongs=tuple(n for n, _ in others), hint=hint, topic=PARTS_TOPIC)
        return _labelled(stem=f"{name}ทำหน้าที่ใด",
                         correct=motion, wrongs=tuple(m for _, m in others), hint=hint, topic=PARTS_TOPIC)
