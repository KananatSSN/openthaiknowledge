"""ชุดรวมวิธีแยกสาร (ความเข้ากันได้)

เคมี · ม.2 · เสริมทักษะ
Indicators: —

Sets moved here from: chemistry.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.chemistry import SUBJECT, TOPIC_MATTER

PROVENANCE = Provenance("original")


@question_type("chem.separation",
               display_name={"th": "การแยกสาร"},
               level={"th": "ป.6"}, subject=SUBJECT, topic=TOPIC_MATTER)
class Separation(ClassifyType):
    """เลือกวิธีแยกสารให้เหมาะกับตัวอย่าง กรอง/ระเหยแห้ง/กลั่น/โครมาโทกราฟี/กรวยแยก/แม่เหล็ก."""

    CLASSIFY_STEM = "ตัวอย่างต่อไปนี้ใช้วิธีแยกสารแบบใด: “{member}”"
    PICK_STEM = "ข้อใดคือตัวอย่างของการแยกสารด้วยวิธี{category}"

    CATEGORIES = [
        Category("การกรอง (Filtration)",
                 ("แยกกากมะพร้าวออกจากน้ำกะทิ", "แยกกากชาหรือกาแฟออกจากน้ำ",
                  "แยกทรายออกจากน้ำ")),
        Category("การระเหยแห้ง (Evaporation)",
                 ("การทำนาเกลือจากน้ำทะเล", "แยกน้ำตาลทรายออกจากน้ำเชื่อม")),
        Category("การกลั่น (Distillation)",
                 ("แยกน้ำจืดออกจากน้ำทะเล", "การกลั่นน้ำมันดิบ",
                  "การแยกแอลกอฮอล์ออกจากน้ำ")),
        Category("การโครมาโทกราฟี (Chromatography)",
                 ("การแยกสีที่ผสมอยู่ในหมึกปากกา", "การแยกสารสีจากใบไม้")),
        Category("การใช้กรวยแยก (Separatory Funnel)",
                 ("การแยกน้ำมันพืชที่ลอยอยู่บนน้ำ",
                  "การแยกของเหลวสองชนิดที่ไม่ละลายเข้าด้วยกัน")),
        Category("การใช้แม่เหล็กดูด (Magnetic Separation)",
                 ("แยกผงตะไบเหล็กออกจากกองทราย", "คัดแยกเศษเหล็กออกจากกองขยะ")),
    ]
