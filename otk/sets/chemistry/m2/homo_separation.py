"""ชุดรวมวิธีแยกสารเนื้อเดียว (ความเข้ากันได้)

เคมี · ม.2 · เสริมทักษะ
Indicators: —

Sets moved here from: substances.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.substances import LEVEL, SUBJECT, TOPIC_SEP

PROVENANCE = Provenance("original")


@question_type("chem.homo_separation",
               display_name={"th": "วิธีแยกสารเนื้อเดียว"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC_SEP)
class HomoSeparation(ClassifyType):
    """เลือกวิธีแยกสารเนื้อเดียวทั้งหกวิธีตามที่ใบความรู้ระบุไว้.

    สารเนื้อเดียว cannot be picked apart by eye, so every method here works on a
    *property difference* — จุดเดือด, ความอิ่มตัว, การละลาย, การถูกดูดซับ.
    """

    CLASSIFY_STEM = "ควรแยกองค์ประกอบของสารต่อไปนี้ด้วยวิธีใด: “{member}”"
    PICK_STEM = "ข้อใดควรแยกด้วย{category}"

    CATEGORIES = [
        Category("การระเหยจนแห้ง",
                 ("การทำนาเกลือจากน้ำทะเล",
                  "ต้มน้ำเกลือจนน้ำระเหยหมดเพื่อเก็บเกลือไว้",
                  "แยกของแข็งที่ละลายอยู่ออกมา โดยไม่ต้องเก็บของเหลวไว้ใช้")),
        Category("การตกผลึก",
                 ("ทำสารละลายน้ำตาลให้อิ่มตัวแล้วปล่อยให้เย็นจนได้ผลึกน้ำตาลกรวด",
                  "แยกผลึกจุนสีออกจากสารละลายอิ่มตัวของจุนสี",
                  "ทำเกลือให้บริสุทธิ์ขึ้นโดยละลายแล้วปล่อยให้ตกผลึกใหม่")),
        # "การกลั่นธรรมดา" rather than plain "การกลั่น": a bare label would be a
        # prefix of the next one, so "ข้อใดควรแยกด้วยการกลั่นลำดับส่วน" would name
        # two categories at once and the item would have two right answers.
        Category("การกลั่นธรรมดา",
                 ("แยกน้ำจืดออกจากน้ำทะเลโดยเก็บไอน้ำที่ควบแน่นไว้",
                  "แยกน้ำบริสุทธิ์ออกจากสารละลายจุนสีโดยเก็บไอน้ำที่ควบแน่นไว้",
                  "แยกน้ำออกจากน้ำเชื่อมโดยเก็บทั้งน้ำและน้ำตาลไว้ใช้")),
        Category("การกลั่นลำดับส่วน",
                 ("การแยกน้ำมันดิบออกเป็นน้ำมันเบนซิน น้ำมันก๊าด และน้ำมันเตา",
                  "การแยกแก๊สธรรมชาติออกเป็นองค์ประกอบหลายชนิด",
                  "แยกของเหลวหลายชนิดที่มีจุดเดือดใกล้เคียงกันออกจากกัน")),
        Category("การสกัดด้วยตัวทำละลาย",
                 ("การสกัดน้ำมันหอมระเหยออกจากกลีบดอกไม้",
                  "การสกัดสีจากใบเตยด้วยตัวทำละลายที่เหมาะสม",
                  "การสกัดน้ำมันออกจากเมล็ดพืชด้วยเฮกเซน")),
        Category("การทำโครมาโทกราฟี",
                 ("การแยกสีที่ผสมอยู่ในหมึกปากกาออกเป็นแถบสี",
                  "การแยกสารสีในสารสกัดจากใบไม้ออกจากกัน",
                  "การตรวจว่าสีผสมอาหารตัวอย่างมีสารสีกี่ชนิด")),
    ]
