"""การจำแนกการถ่ายโอนความร้อนจากภาพ

ฟิสิกส์ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.1/6

Sets moved here from: science_wave_g2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.ms1_diagrams import (
    HEAT_SCENES,
    MODE_LABELS,
    diagram_question,
    heat_scene_alt,
)
from otk.sets._support.science_wave_b2 import LEVEL as MIDDLE_ONE
from otk.sets._support.science_wave_d14 import SUBJECT as PHYS_SUBJECT

PROVENANCE = Provenance("original")


HEAT_TRANSFER_DIAGRAM_TOPIC = "การจำแนกการถ่ายโอนความร้อนจากภาพ"


@question_type(
    "phys.heat_transfer_diagram_foundation",
    display_name={"th": "จำแนกวิธีถ่ายโอนความร้อนจากภาพ"},
    level=MIDDLE_ONE, subject=PHYS_SUBJECT, topic=HEAT_TRANSFER_DIAGRAM_TOPIC,
)
class HeatTransferDiagramFoundation(QuestionType):
    """Name the mode the drawn scene shows.

    All three labels are offered every time, so the answer comes from the
    picture rather than from which words happen to be on screen.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(HEAT_SCENES)
        wrongs = tuple(m for m in MODE_LABELS if m != spec.thai_mode)
        return diagram_question(
            spec.asset_id, heat_scene_alt(spec),
            stem="จากภาพ ความร้อนถ่ายโอนด้วยวิธีใด",
            correct=spec.thai_mode,
            wrongs=wrongs + (rng.choice(("ไม่มีการถ่ายโอนความร้อนเกิดขึ้นในภาพนี้", "การระเหยของน้ำ",
                                         "การควบแน่นของไอน้ำ", "การขยายตัวของวัตถุเมื่อได้รับความร้อน")),),
            hint=("ดูว่าความร้อนผ่านอะไรไป ผ่านของแข็งที่อยู่กับที่ ผ่านของไหลที่หมุนเวียน "
                  "หรือผ่านช่องว่างที่ไม่มีตัวกลางเลย"),
            topic=HEAT_TRANSFER_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.heat_transfer_diagram_fluency",
    display_name={"th": "อธิบายเหตุผลของวิธีถ่ายโอนความร้อนที่เห็นในภาพ"},
    level=MIDDLE_ONE, subject=PHYS_SUBJECT, topic=HEAT_TRANSFER_DIAGRAM_TOPIC,
)
class HeatTransferDiagramFluency(QuestionType):
    """Not which mode, but why the drawing shows that one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(HEAT_SCENES)
        others = {s.mode: s.because for s in HEAT_SCENES if s.mode != spec.mode}
        return diagram_question(
            spec.asset_id, heat_scene_alt(spec),
            stem="จากภาพ ข้อใดอธิบายการถ่ายโอนความร้อนที่เกิดขึ้นได้ถูกต้อง",
            correct=spec.because,
            wrongs=tuple(others.values()) + (rng.choice((
                "ความร้อนถ่ายโอนได้เพราะวัตถุทั้งสองมีอุณหภูมิเท่ากันพอดี",
                "ความเย็นเคลื่อนจากวัตถุที่เย็นกว่าเข้าไปแทนที่ความร้อน",
                "ความร้อนถ่ายโอนจากวัตถุที่เย็นกว่าไปยังวัตถุที่ร้อนกว่า",
                "อนุภาคของวัตถุหยุดเคลื่อนไหวทั้งหมด ความร้อนจึงไหลออกมา")),),
            hint="การนำอนุภาคอยู่กับที่ การพาอนุภาคเคลื่อนที่ไปด้วย การแผ่รังสีไม่ต้องใช้ตัวกลาง",
            topic=HEAT_TRANSFER_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.heat_transfer_diagram_application",
    display_name={"th": "เลือกวิธีลดการถ่ายโอนความร้อนให้ตรงกับภาพ"},
    level=MIDDLE_ONE, subject=PHYS_SUBJECT, topic=HEAT_TRANSFER_DIAGRAM_TOPIC,
)
class HeatTransferDiagramApplication(QuestionType):
    """Each mode is slowed by a different thing; the picture says which."""

    _FIX = {
        "conduction": "คั่นด้วยวัสดุที่นำความร้อนได้ไม่ดี เช่น ไม้หรือพลาสติก ตรงบริเวณที่ความร้อนต้องผ่าน",
        "convection": "ปิดกั้นไม่ให้ของไหลหมุนเวียนได้ เช่น ใช้ฝาปิดหรือแบ่งช่องให้แคบลง",
        "radiation": "ใช้ผิวมันวาวสะท้อนรังสีความร้อนกลับไป เช่น แผ่นฟอยล์หรือผิวเงา",
    }

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(HEAT_SCENES)
        wrongs = tuple(v for k, v in self._FIX.items() if k != spec.mode)
        return diagram_question(
            spec.asset_id, heat_scene_alt(spec),
            stem="จากภาพ ถ้าต้องการลดการถ่ายโอนความร้อนที่เกิดขึ้น ควรทำอย่างไรจึงตรงจุดที่สุด",
            correct=self._FIX[spec.mode],
            wrongs=wrongs + (rng.choice((
                "เพิ่มอุณหภูมิของแหล่งความร้อนให้สูงขึ้น เพื่อให้ความร้อนกระจายเร็วจนหมดไป",
                "ทาสีดำด้านบนผิวที่รับความร้อน เพื่อให้ดูดความร้อนได้ดีขึ้น",
                "เปลี่ยนวัสดุเป็นโลหะที่นำความร้อนได้ดีกว่าเดิม",
                "เปิดช่องให้อากาศร้อนไหลเวียนเข้าหาบริเวณนั้นมากขึ้น")),),
            hint="แก้ที่ทางที่ความร้อนใช้เดินทาง ตัวกลางที่เป็นของแข็ง การหมุนเวียนของของไหล หรือรังสี",
            topic=HEAT_TRANSFER_DIAGRAM_TOPIC,
        )
