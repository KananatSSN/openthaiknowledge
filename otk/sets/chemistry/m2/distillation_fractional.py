"""การกลั่นลำดับส่วน

เคมี · ม.2 · เสริมทักษะ
Indicators: —

Sets moved here from: science_successors.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.concept_bank import Concept
from otk.sets._support.science_successors import FluencyStage
from otk.sets.chemistry.m2.distillation import Distillation

PROVENANCE = Provenance("original")


@question_type(
    "chem.distillation_fractional",
    display_name={"th": "การกลั่นลำดับส่วน"},
    level={"th": "ม.2"}, subject="เคมี", topic="การแยกสาร",
)
class FractionalDistillation(FluencyStage, Distillation):
    source_key = "chem.distillation"
    ITEMS = [Distillation.ITEMS[index] for index in (4, 5, 7, 8)]

# More items: these tables held six or fewer, so a learner met them all in
# a few tries. Each added item has wrong readings of its own.
FractionalDistillation.ITEMS = [*FractionalDistillation.ITEMS,
    Concept('ไอที่ออกจากส่วนบนสุดของคอลัมน์กลั่นลำดับส่วนเป็นสารที่มีสมบัติอย่างไร',
            'มีจุดเดือดต่ำที่สุดในของผสม',
            ('มีจุดเดือดสูงที่สุดในของผสม', 'มีความหนาแน่นมากที่สุดในของผสม', 'มีสีเข้มที่สุดในของผสม', 'มีปริมาตรมากที่สุดในของผสม', 'เป็นของแข็งที่ละลายอยู่ในของผสม')),
    Concept('ผลิตภัณฑ์ใดจากหอกลั่นน้ำมันดิบที่มีจุดเดือดสูงมาก จึงแยกออกมาที่ส่วนล่างสุดของหอ',
            'ยางมะตอยและน้ำมันเตา',
            ('แก๊สหุงต้ม', 'น้ำมันเบนซิน', 'แก๊สมีเทน', 'น้ำมันก๊าด', 'แก๊สโพรเพน')),
    Concept('อุตสาหกรรมแยกแก๊สออกซิเจนและไนโตรเจนออกจากอากาศที่ทำให้เป็นของเหลวด้วยวิธีใด',
            'การกลั่นลำดับส่วน',
            ('การกรอง', 'การใช้กรวยแยก', 'การระเหิด', 'การตกผลึก', 'การใช้แม่เหล็กดูด')),
]
