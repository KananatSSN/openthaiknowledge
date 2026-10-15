"""การแยกสารด้วยเครื่องหมุนเหวี่ยง

เคมี · ม.2 · เสริมทักษะ
Indicators: —

Sets moved here from: science_successors.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.concept_bank import Concept
from otk.sets._support.science_successors import FluencyStage
from otk.sets.chemistry.p6.sedimentation import Sedimentation

PROVENANCE = Provenance("original")


@question_type(
    "chem.sedimentation_centrifuge",
    display_name={"th": "การแยกสารด้วยเครื่องหมุนเหวี่ยง"},
    level={"th": "ม.2"}, subject="เคมี", topic="การแยกสาร",
)
class SedimentationCentrifuge(FluencyStage, Sedimentation):
    source_key = "chem.sedimentation"
    ITEMS = [Sedimentation.ITEMS[index] for index in (4, 6, 7)]

# More items: these tables held six or fewer, so a learner met them all in
# a few tries. Each added item has wrong readings of its own.
SedimentationCentrifuge.ITEMS = [*SedimentationCentrifuge.ITEMS,
    Concept('เหตุใดต้องวางหลอดในเครื่องหมุนเหวี่ยงให้สมดุลกันทั้งสองฝั่ง',
            'เพื่อไม่ให้เครื่องสั่นแรงและเสียหายขณะหมุนด้วยความเร็วสูง',
            ('เพื่อให้สารในหลอดเปลี่ยนเป็นสารใหม่ได้เร็วขึ้นกว่าเดิมมาก', 'เพื่อให้ของเหลวในหลอดระเหยออกไปจนหมดเร็วขึ้น', 'เพื่อให้ตะกอนลอยขึ้นไปอยู่ที่ปากหลอดด้านบนสุด', 'เพื่อให้เครื่องหมุนช้าลงจนตะกอนตกลงเองตามปกติ', 'เพื่อให้หลอดทุกหลอดมีสีเดียวกันหลังการหมุนเสร็จ')),
    Concept('เครื่องซักผ้าในช่วงปั่นหมาดใช้หลักการคล้ายเครื่องหมุนเหวี่ยงอย่างไร',
            'การหมุนเร็วเหวี่ยงน้ำให้ออกจากผ้าไปทางผนังถัง',
            ('การหมุนเร็วทำให้น้ำในผ้าระเหยเป็นไอหมดทันที', 'การหมุนเร็วดูดน้ำเข้าไปอยู่ตรงกลางผ้าแน่นขึ้น', 'การหมุนเร็วเปลี่ยนน้ำในผ้าให้เป็นน้ำแข็ง', 'การหมุนเร็วทำให้ผ้ามีน้ำหนักเพิ่มขึ้นมาก', 'การหมุนเร็วทำให้สบู่กลายเป็นสารใหม่')),
    Concept('โรงงานแยกครีมออกจากน้ำนมดิบอย่างรวดเร็วด้วยวิธีใด',
            'การหมุนเหวี่ยง ให้ครีมที่เบากว่าแยกออกจากน้ำนม',
            ('การกลั่นน้ำนมให้ครีมระเหยออกมาเป็นไอ', 'การใช้แม่เหล็กดูดครีมออกจากน้ำนม', 'การกรองด้วยกระดาษกรองธรรมดาหลายชั้น', 'การระเหิดครีมออกจากน้ำนมด้วยความร้อน', 'การเติมเกลือให้ครีมกลายเป็นของแข็ง')),
]
