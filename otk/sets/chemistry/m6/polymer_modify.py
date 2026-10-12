"""การปรับเปลี่ยนโครงสร้างและการสังเคราะห์พอลิเมอร์

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/14

Sets moved here from: science_wave_f29.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f29 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_MODIFY = "การปรับเปลี่ยนโครงสร้างและการสังเคราะห์พอลิเมอร์"


MODIFICATIONS = (
    ("การวัลคาไนซ์ยางด้วยกำมะถัน", "เกิดพันธะเชื่อมโยงระหว่างสายยาง ยางแข็งแรง ยืดหยุ่นดี ไม่เหนียวเยิ้มเมื่อร้อน และไม่แข็งเปราะเมื่อเย็น"),
    ("การเติมพลาสติไซเซอร์ลงใน PVC", "โมเลกุลเล็กแทรกระหว่างสาย ลดแรงระหว่างสาย PVC จึงนิ่มและโค้งงอได้ เช่น สายยางและหนังเทียม"),
    ("การสังเคราะห์โคพอลิเมอร์ SBR จากสไตรีนและบิวทาไดอีน", "ได้ยางสังเคราะห์ที่ทนการขัดสีดีกว่ายางธรรมชาติ ใช้ทำดอกยางรถยนต์"),
    ("การเพิ่มจำนวนพันธะเชื่อมโยงระหว่างสายให้มากขึ้น", "พอลิเมอร์แข็งขึ้น ยืดหยุ่นน้อยลง และไม่หลอมเมื่อได้รับความร้อน"),
    ("การดึงยืดเส้นใยพอลิเมอร์ขณะขึ้นรูปให้สายเรียงตัวเป็นระเบียบ", "เส้นใยแข็งแรงและทนแรงดึงมากขึ้น"),
    ("การเติมสารเพิ่มความเสถียรต่อแสง UV", "พลาสติกเสื่อมสภาพและกรอบแตกช้าลงเมื่ออยู่กลางแดด"),
    ("การผลิตพอลิแล็กติกแอซิด (PLA) จากแป้งข้าวโพด", "ได้พลาสติกที่จุลินทรีย์ย่อยสลายได้ภายใต้สภาวะที่เหมาะสม"),
)


@question_type(
    "chem.polymer_modify_foundation",
    display_name={"th": "ผลของการปรับเปลี่ยนโครงสร้างพอลิเมอร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MODIFY,
)
class PolymerModifyFoundation(QuestionType):
    """Each change to the chains changes a property."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        change, effect = rng.choice(MODIFICATIONS)
        others = [m for m in MODIFICATIONS if m[0] != change]
        hint = "พันธะเชื่อมโยงเพิ่มความแข็งและการคืนรูป โมเลกุลเล็กที่แทรกระหว่างสายทำให้นิ่ม การเรียงตัวทำให้แข็งแรง"
        if rng.random() < 0.5:
            return _labelled(stem=f"{change} ทำให้พอลิเมอร์เปลี่ยนไปอย่างไร", correct=effect,
                             wrongs=tuple(m[1] for m in rng.sample(others, 3)), topic=TOPIC_MODIFY, hint=hint)
        return _labelled(stem=f"ต้องการให้ได้ผลว่า \"{effect}\" ต้องปรับเปลี่ยนพอลิเมอร์อย่างไร", correct=change,
                         wrongs=tuple(m[0] for m in rng.sample(others, 3)), topic=TOPIC_MODIFY, hint=hint)


@question_type(
    "chem.polymer_modify_fluency",
    display_name={"th": "คำนวณเกี่ยวกับการวัลคาไนซ์และโคพอลิเมอร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MODIFY,
)
class PolymerModifyFluency(QuestionType):
    """Sulfur share in vulcanised rubber, and monomer share in a copolymer."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            rubber = rng.randrange(100, 1001, 50)
            percent = rng.choice((1, 2, 3, 4, 5, 8, 10, 20, 30))
            sulfur = Fraction(rubber * percent, 100)
            return numeric(stem=f"ต้องการวัลคาไนซ์ยาง {rubber} กรัม โดยใช้กำมะถัน {percent}% ของมวลยาง ต้องใช้กำมะถันกี่กรัม "
                                "(กำมะถันมากขึ้นยางจะแข็งขึ้น)",
                           answer=sulfur, wrongs=[rubber * percent, sulfur * 10, rubber - sulfur], unit="กรัม",
                           topic=TOPIC_MODIFY, hint="มวลกำมะถัน = ร้อยละ × มวลยาง ÷ 100")
        # SBR: styrene C₈H₈ (104) and butadiene C₄H₆ (54) units.
        styrene = rng.randint(1, 5)
        butadiene = rng.randint(1, 8)
        total = styrene * 104 + butadiene * 54
        return numeric(stem=f"ยาง SBR ช่วงหนึ่งมีหน่วยสไตรีน (C₈H₈ มวล 104) {styrene} หน่วย และหน่วยบิวทาไดอีน "
                            f"(C₄H₆ มวล 54) {butadiene} หน่วย ช่วงนี้มีมวลรวมเท่าใด",
                       answer=total, wrongs=[(styrene + butadiene) * 104, (styrene + butadiene) * 54, 104 + 54],
                       unit="g/mol", topic=TOPIC_MODIFY, hint="โคพอลิเมอร์มีหน่วยซ้ำจากมอนอเมอร์สองชนิด รวมมวลของทุกหน่วย")


@question_type(
    "chem.polymer_modify_application",
    display_name={"th": "เลือกวิธีปรับปรุงพอลิเมอร์ให้เหมาะกับงาน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MODIFY,
)
class PolymerModifyApplication(QuestionType):
    """A defect to fix, and the change that fixes it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        problems = (
            ("ยางธรรมชาติเหนียวเยิ้มเมื่อร้อนและแข็งเปราะเมื่อเย็น", MODIFICATIONS[0][0]),
            ("ท่อ PVC แข็งเกินไป ต้องการทำสายยางที่โค้งงอได้", MODIFICATIONS[1][0]),
            ("ยางธรรมชาติสึกเร็วเมื่อใช้ทำดอกยางรถยนต์", MODIFICATIONS[2][0]),
            ("ต้องการเส้นใยที่ทนแรงดึงสูงสำหรับทำเชือก", MODIFICATIONS[4][0]),
            ("เก้าอี้พลาสติกที่ตั้งกลางแดดกรอบแตกเร็ว", MODIFICATIONS[5][0]),
            ("ภาชนะพลาสติกใช้ครั้งเดียวที่ตกค้างในสิ่งแวดล้อมนานมาก", MODIFICATIONS[6][0]),
        )
        problem, fix = rng.choice(problems)
        others = [m[0] for m in MODIFICATIONS if m[0] != fix]
        return _labelled(stem=f"ปัญหา: {problem} ควรแก้ด้วยวิธีใด", correct=fix, wrongs=tuple(others),
                         topic=TOPIC_MODIFY, hint="นึกว่าปัญหาเกิดจากสายพอลิเมอร์ขาดอะไร แล้วเลือกการปรับที่เติมสิ่งนั้น")
