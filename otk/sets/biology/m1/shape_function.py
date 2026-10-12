"""รูปร่างของเซลล์กับการทำหน้าที่

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/3

Sets moved here from: science_wave_b2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import contextual_scenario_question
from otk.sets._support.science_wave_b2 import (
    LEVEL,
    SHAPE_SCENARIOS,
    SPECIAL_CELLS,
    SUBJECT,
    TOPIC,
    _labelled,
)

PROVENANCE = Provenance("original")


@question_type(
    "cell.shape_function_foundation",
    display_name={"th": "หน้าที่ของเซลล์ที่ทำหน้าที่เฉพาะ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class CellShapeFoundation(QuestionType):
    """What each specialised cell is for, before why its shape suits it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cell = rng.choice(SPECIAL_CELLS)
        others = [other for other in SPECIAL_CELLS if other.name != cell.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{cell.name}” ทำหน้าที่ใด",
                correct=cell.job,
                wrongs=tuple(other.job for other in others[:3]),
                hint="นึกถึงว่าเซลล์ชนิดนั้นอยู่ในอวัยวะใด แล้วอวัยวะนั้นทำงานอะไร",
            )
        return _labelled(
            stem=f"เซลล์ชนิดใดทำหน้าที่{cell.job}",
            correct=cell.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกเซลล์ที่ทำหน้าที่นั้นโดยตรง",
        )


@question_type(
    "cell.shape_function_fluency",
    display_name={"th": "รูปร่างของเซลล์ที่เหมาะกับหน้าที่"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class CellShapeFluency(QuestionType):
    """Match a cell to its shape, and say what the shape buys it.

    This is the whole of ``ม.1/3``: not that a nerve cell is long, but that being
    long is what lets it do its job. The second branch asks for the reason
    directly, and every wrong reason belongs to a different cell in the table.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cell = rng.choice(SPECIAL_CELLS)
        others = [other for other in SPECIAL_CELLS if other.name != cell.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{cell.name}” มีรูปร่างลักษณะอย่างไร",
                correct=cell.shape,
                wrongs=tuple(other.shape for other in others[:3]),
                hint="นึกถึงหน้าที่ของเซลล์นั้นก่อน แล้วรูปร่างที่ช่วยให้ทำหน้าที่นั้นได้ดี",
            )
        return _labelled(
            stem=f"“{cell.name}” มีลักษณะ{cell.shape} ลักษณะนี้ช่วยให้ทำหน้าที่ได้ดีอย่างไร",
            correct=cell.reason,
            wrongs=tuple(other.reason for other in others[:3]),
            hint="ถามว่าลักษณะนั้นเพิ่มพื้นที่ผิว เพิ่มระยะทาง หรือทำให้เคลื่อนที่ได้",
        )


@question_type(
    "cell.shape_function_application",
    display_name={"th": "วิเคราะห์ผลของรูปร่างเซลล์ต่อการทำหน้าที่"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class CellShapeApplication(QuestionType):
    """Predict what changing or losing a cell's shape would cost it.

    Naming the shape is Fluency work. Here the shape has to be connected to a
    consequence — a wilting seedling, a slower gas exchange — which is the form
    ``ม.1/3`` takes once it leaves the diagram.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, SHAPE_SCENARIOS,
            hint="เริ่มจากหน้าที่ของเซลล์นั้น แล้วถามว่ารูปร่างที่เปลี่ยนไป"
                 "ทำให้ทำหน้าที่นั้นได้ดีขึ้นหรือแย่ลง",
            topic=TOPIC,
        )
