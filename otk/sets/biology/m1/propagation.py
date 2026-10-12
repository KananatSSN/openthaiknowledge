"""การเลือกวิธีขยายพันธุ์พืช

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/16

Sets moved here from: science_wave_b7.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import contextual_scenario_question
from otk.sets._support.science_wave_b7 import (
    LEVEL,
    METHODS,
    PROPAGATION_SCENARIOS,
    SUBJECT,
    TOPIC,
    _labelled,
)

PROVENANCE = Provenance("original")


@question_type(
    "plant.propagation_foundation",
    display_name={"th": "วิธีขยายพันธุ์พืชและขั้นตอนของแต่ละวิธี"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PropagationFoundation(QuestionType):
    """Name what a method does, or the method that does it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(METHODS)
        others = [other for other in METHODS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” ทำอย่างไร",
                correct=item.procedure,
                wrongs=tuple(other.procedure for other in others[:3]),
                hint="สังเกตว่าวิธีนั้นเริ่มจากเมล็ด จากกิ่ง จากหน่อ "
                     "หรือจากชิ้นส่วนเล็ก ๆ ของพืช",
            )
        return _labelled(
            stem=f"วิธีขยายพันธุ์พืชวิธีใดทำโดย{item.procedure}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านขั้นตอนให้จบก่อน แล้วจึงเลือกชื่อวิธีที่ตรงกับขั้นตอนนั้น",
        )


@question_type(
    "plant.propagation_fluency",
    display_name={"th": "ข้อดีและความเหมาะสมของแต่ละวิธีขยายพันธุ์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PropagationFluency(QuestionType):
    """Match a method to the need it answers best, or a need to its method.

    Each method's ``best_for`` is worded so that no two overlap — the difference
    between ปักชำ and ตอนกิ่ง is whether the plant roots easily, and between
    ปักชำ and ติดตา is whether the rootstock matters. Without that the item would
    have two defensible answers.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(METHODS)
        others = [other for other in METHODS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” เหมาะกับความต้องการแบบใดมากที่สุด",
                correct=item.best_for,
                wrongs=tuple(other.best_for for other in others[:3]),
                hint="ถามว่าวิธีนั้นให้ต้นที่เหมือนต้นแม่หรือไม่ "
                     "และได้ต้นจำนวนมากหรือน้อยเพียงใด",
            )
        return _labelled(
            stem=f"ถ้า{item.best_for} ควรเลือกวิธีขยายพันธุ์ใด",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="จับคู่ความต้องการกับวิธีที่ตอบความต้องการนั้นได้ตรงที่สุด "
                 "ไม่ใช่วิธีที่พอทำได้",
        )


@question_type(
    "plant.propagation_application",
    display_name={"th": "เลือกวิธีขยายพันธุ์พืชให้เหมาะกับความต้องการ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PropagationApplication(QuestionType):
    """Choose a method for a stated need and justify it.

    This is ``ม.1/16`` word for word. Every wrong choice names a real method with
    a reason that is *almost* right — usually a property the method does have,
    claimed for a situation it does not fit.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, PROPAGATION_SCENARIOS,
            hint="ระบุความต้องการให้ชัดก่อน: ต้องการต้นเหมือนเดิมหรือหลากหลาย "
                 "ต้องการกี่ต้น และพืชชนิดนั้นออกรากง่ายหรือยาก",
            topic=TOPIC,
        )
