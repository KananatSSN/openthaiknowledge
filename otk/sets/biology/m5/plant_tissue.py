"""เนื้อเยื่อพืช

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/1

Sets moved here from: science_wave_f54.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f54 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_TISSUE = "เนื้อเยื่อพืช"


TISSUES = (
    ("เอพิเดอร์มิส", "เป็นเซลล์ชั้นนอกสุด ป้องกันอันตรายและลดการสูญเสียน้ำ"),
    ("พาเรงคิมา", "เป็นเซลล์มีชีวิต ผนังบาง ทำหน้าที่สะสมอาหาร และสังเคราะห์ด้วยแสงเมื่อมีคลอโรพลาสต์"),
    ("คอลเลงคิมา", "เป็นเซลล์มีชีวิต ผนังหนาเฉพาะที่มุมเซลล์ ช่วยค้ำจุนส่วนที่ยังอ่อน"),
    ("สเกลอเรงคิมา", "เป็นเซลล์ที่ตายแล้ว ผนังหนามีลิกนิน ให้ความแข็งแรง เช่น ไฟเบอร์และสเกลอรีด"),
    ("ไซเลม", "ลำเลียงน้ำและธาตุอาหารจากรากขึ้นสู่ส่วนต่าง ๆ"),
    ("โฟลเอ็ม", "ลำเลียงอาหารที่พืชสร้างขึ้นไปยังส่วนต่าง ๆ"),
)


MERISTEMS = (
    ("เนื้อเยื่อเจริญส่วนปลาย", "ปลายยอดและปลายราก", "ทำให้ลำต้นและรากยาวขึ้น"),
    ("เนื้อเยื่อเจริญด้านข้าง", "วาสคิวลาร์แคมเบียมและคอร์กแคมเบียม", "ทำให้ลำต้นและรากขยายขนาดทางด้านข้าง"),
    ("เนื้อเยื่อเจริญเหนือข้อ", "บริเวณเหนือข้อของพืชใบเลี้ยงเดี่ยว เช่น หญ้าและไผ่", "ทำให้ปล้องยืดยาวขึ้น"),
)


TISSUE_HINT = ("เนื้อเยื่อเจริญแบ่งเซลล์ได้ตลอด เนื้อเยื่อถาวรไม่แบ่งเซลล์แล้ว เอพิเดอร์มิสป้องกัน พาเรงคิมาสะสมอาหาร "
               "คอลเลงคิมาและสเกลอเรงคิมาค้ำจุน ไซเลมลำเลียงน้ำ โฟลเอ็มลำเลียงอาหาร")


# (cell, alive at maturity, wall, job)
CELLS = (
    ("เวสเซลเมมเบอร์", "ตายแล้ว", "ผนังหนามีลิกนิน ปลายเซลล์ทะลุถึงกัน", "ลำเลียงน้ำในไซเลม"),
    ("เทรคีด", "ตายแล้ว", "ผนังหนามีลิกนิน ปลายเซลล์แหลมมีรูเล็ก ๆ", "ลำเลียงน้ำในไซเลม"),
    ("ซีฟทิวบ์เมมเบอร์", "มีชีวิตแต่ไม่มีนิวเคลียส", "ผนังบาง ปลายเซลล์เป็นแผ่นมีรูพรุน", "ลำเลียงอาหารในโฟลเอ็ม"),
    ("เซลล์คอมพาเนียน", "มีชีวิตและมีนิวเคลียส", "ผนังบาง อยู่ข้างซีฟทิวบ์เมมเบอร์", "ช่วยควบคุมการทำงานของซีฟทิวบ์เมมเบอร์"),
    ("ไฟเบอร์", "ตายแล้ว", "ผนังหนามีลิกนิน เซลล์ยาวปลายแหลม", "ให้ความแข็งแรง"),
    ("สเกลอรีด", "ตายแล้ว", "ผนังหนามีลิกนิน เซลล์สั้นรูปร่างไม่แน่นอน", "ทำให้เปลือกเมล็ดและเนื้อผลบางชนิดแข็ง"),
    ("เซลล์คุม", "มีชีวิตและมีนิวเคลียส", "เซลล์รูปไตมีคลอโรพลาสต์", "ควบคุมการปิดเปิดปากใบ"),
)


@question_type(
    "biology.plant_tissue_foundation",
    display_name={"th": "ชนิดและหน้าที่ของเนื้อเยื่อถาวรในพืช"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TISSUE,
)
class PlantTissueFoundation(QuestionType):
    """What each permanent tissue does, both ways."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, role = rng.choice(TISSUES)
        others = rng.sample([t for t in TISSUES if t[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"เนื้อเยื่อ{name}มีลักษณะหรือหน้าที่ใด", correct=role, wrongs=tuple(t[1] for t in others),
                             topic=TOPIC_TISSUE, hint=TISSUE_HINT)
        return _labelled(stem=f"เนื้อเยื่อใด{role}", correct=name, wrongs=tuple(t[0] for t in others), topic=TOPIC_TISSUE,
                         hint=TISSUE_HINT)


@question_type(
    "biology.plant_tissue_fluency",
    display_name={"th": "เนื้อเยื่อเจริญและตำแหน่งที่พบ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TISSUE,
)
class PlantTissueFluency(QuestionType):
    """Apical, lateral and intercalary meristems, where they sit and what they grow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, where, effect = rng.choice(MERISTEMS)
        others = [m for m in MERISTEMS if m[0] != name]
        roll = rng.random()
        if roll < 0.25:
            extra = ("พาเรงคิมา", "เอพิเดอร์มิส", "สเกลอเรงคิมา", "ไซเลม")
            return _labelled(stem=f"เนื้อเยื่อที่พบที่{where}และ{effect}คือเนื้อเยื่อใด", correct=name,
                             wrongs=(rng.choice(others)[0], *rng.sample(extra, 2)), topic=TOPIC_TISSUE, hint=TISSUE_HINT)
        if roll < 0.5:
            extra = ("ทำให้ใบเปลี่ยนสีตามฤดูกาล", "ลำเลียงน้ำขึ้นสู่ใบ", "ป้องกันการสูญเสียน้ำ", "สะสมอาหารในหัว")
            return _labelled(stem=f"{name}ทำให้พืชเจริญเติบโตอย่างไร", correct=effect,
                             wrongs=(rng.choice(others)[2], *rng.sample(extra, 2)), topic=TOPIC_TISSUE, hint=TISSUE_HINT)
        if roll < 0.7:
            extra = ("ใจกลางพิธของลำต้น", "ชั้นเอพิเดอร์มิสของใบ", "ภายในเนื้อผลที่สุกแล้ว", "ปลายขนราก")
            return _labelled(stem=f"{name}พบที่บริเวณใด", correct=where,
                             wrongs=(rng.choice(others)[1], *rng.sample(extra, 2)), topic=TOPIC_TISSUE, hint=TISSUE_HINT)
        facts = (("ข้อใดเป็นลักษณะของเซลล์เนื้อเยื่อเจริญ", "เซลล์ขนาดเล็ก ผนังบาง นิวเคลียสใหญ่ และแบ่งเซลล์ได้",
                  ("เซลล์ตายแล้ว ผนังหนามีลิกนิน", "เซลล์ขนาดใหญ่มีแวคิวโอลใหญ่ ไม่แบ่งเซลล์", "เซลล์ไม่มีนิวเคลียส",
                   "เซลล์เรียงตัวหลวม ๆ มีช่องอากาศมาก")),
                 ("การที่ต้นไม้ยืนต้นมีลำต้นใหญ่ขึ้นทุกปีเกิดจากการแบ่งเซลล์ของเนื้อเยื่อใด", "วาสคิวลาร์แคมเบียม",
                  ("เนื้อเยื่อเจริญส่วนปลายยอด", "เอพิเดอร์มิส", "พาเรงคิมาในพิธ", "เนื้อเยื่อเจริญเหนือข้อ")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_TISSUE, hint=TISSUE_HINT)


@question_type(
    "biology.plant_tissue_application",
    display_name={"th": "ระบุชนิดเซลล์พืชจากลักษณะที่สังเกตได้"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TISSUE,
)
class PlantTissueApplication(QuestionType):
    """Read a cell's features and name it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, alive, wall, job = rng.choice(CELLS)
        others = rng.sample([c for c in CELLS if c[0] != name], 3)
        hint = "ไซเลม (เวสเซลเมมเบอร์ เทรคีด) และสเกลอเรงคิมาเป็นเซลล์ตาย ซีฟทิวบ์เมมเบอร์มีชีวิตแต่ไม่มีนิวเคลียส อาศัยเซลล์คอมพาเนียน"
        roll = rng.random()
        if roll < 0.45:
            return _labelled(stem=f"เซลล์พืชชนิดหนึ่ง{alive}เมื่อเจริญเต็มที่ มี{wall} ทำหน้าที่{job} เซลล์นี้คือเซลล์ใด", correct=name,
                             wrongs=tuple(c[0] for c in others), topic=TOPIC_TISSUE, hint=hint)
        if roll < 0.75:
            return _labelled(stem=f"{name}มีลักษณะอย่างไรเมื่อเจริญเต็มที่", correct=f"{alive} มี{wall}",
                             wrongs=tuple(f"{c[1]} มี{c[2]}" for c in others), topic=TOPIC_TISSUE, hint=hint)
        dead = rng.random() < 0.5
        pool_right = [c[0] for c in CELLS if (c[1] == "ตายแล้ว") == dead]
        pool_wrong = [c[0] for c in CELLS if (c[1] == "ตายแล้ว") != dead]
        return _labelled(stem=f"เซลล์ใด{'เป็นเซลล์ตาย' if dead else 'ยังมีชีวิต'}เมื่อเจริญเต็มที่", correct=rng.choice(pool_right),
                         wrongs=tuple(pool_wrong), topic=TOPIC_TISSUE, hint=hint)
