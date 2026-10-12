"""การสืบพันธุ์ของพืชดอก

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/11

Sets moved here from: science_wave_b5.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import contextual_scenario_question
from otk.sets._support.science_wave_b5 import (
    LEVEL,
    REPRODUCTION_SCENARIOS,
    SUBJECT,
    TOPIC,
    _labelled,
    _statement_question,
)

PROVENANCE = Provenance("original")


SEXUAL = "การสืบพันธุ์แบบอาศัยเพศ"


ASEXUAL = "การสืบพันธุ์แบบไม่อาศัยเพศ"


# Four statements true of each mode and of neither other. Both lists are the same
# length so a question in either direction has three wrongs to draw on.
SEXUAL_FACTS = (
    "ต้องอาศัยการปฏิสนธิระหว่างเซลล์สืบพันธุ์เพศผู้กับเซลล์ไข่",
    "ได้ต้นใหม่ที่มีลักษณะทางพันธุกรรมแตกต่างจากต้นพ่อแม่",
    "เริ่มต้นจากดอก และได้ผลกับเมล็ดเป็นผลลัพธ์",
    "ทำให้ประชากรของพืชมีความหลากหลายทางพันธุกรรมมากขึ้น",
)


ASEXUAL_FACTS = (
    "ไม่ต้องอาศัยการปฏิสนธิ ใช้เพียงส่วนของต้นเดิมเจริญขึ้นเป็นต้นใหม่",
    "ได้ต้นใหม่ที่มีลักษณะทางพันธุกรรมเหมือนต้นเดิมทุกประการ",
    "เริ่มต้นจากราก ลำต้น หรือใบของต้นเดิม โดยไม่ต้องมีดอก",
    "ได้ต้นใหม่ที่ให้ผลผลิตเหมือนต้นเดิมและมักโตเร็วกว่าการเพาะเมล็ด",
)


class Propagule(NamedTuple):
    """One plant and the part of itself it grows a new plant from."""
    plant: str
    structure: str


# The structures ม.1 names, each with plants a Thai learner will have seen.
PROPAGULES = (
    Propagule("กล้วย", "หน่อ"),
    Propagule("ว่านหางจระเข้", "หน่อ"),
    Propagule("สตรอว์เบอร์รี", "ไหล"),
    Propagule("บัวบก", "ไหล"),
    Propagule("มันฝรั่ง", "หัวใต้ดินที่เป็นลำต้น"),
    Propagule("เผือก", "หัวใต้ดินที่เป็นลำต้น"),
    Propagule("ขิง", "เหง้า"),
    Propagule("ข่า", "เหง้า"),
    Propagule("ต้นคว่ำตายหงายเป็น", "ใบ"),
    Propagule("มันเทศ", "รากสะสมอาหาร"),
)


PROPAGULE_STRUCTURES = tuple(dict.fromkeys(item.structure for item in PROPAGULES))


@question_type(
    "plant.reproduction_foundation",
    display_name={"th": "การสืบพันธุ์แบบอาศัยเพศและไม่อาศัยเพศของพืชดอก"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ReproductionFoundation(QuestionType):
    """Which statement is true of the mode named in the stem.

    Two modes means two choices if asked directly, so the item offers four
    statements instead and every wrong one is true of the other mode.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        sexual = rng.random() < 0.5
        return _statement_question(
            subject=SEXUAL if sexual else ASEXUAL,
            mine=list(SEXUAL_FACTS if sexual else ASEXUAL_FACTS),
            theirs=list(ASEXUAL_FACTS if sexual else SEXUAL_FACTS),
            rng=rng,
            hint="ถามว่าวิธีนั้นต้องมีการปฏิสนธิหรือไม่ "
                 "แล้วต้นใหม่ที่ได้เหมือนหรือต่างจากต้นเดิม",
        )


@question_type(
    "plant.reproduction_fluency",
    display_name={"th": "โครงสร้างที่พืชใช้สืบพันธุ์แบบไม่อาศัยเพศ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ReproductionFluency(QuestionType):
    """Name the part a plant grows its new plant from, or a plant that uses a part.

    The asexual half of ``ม.1/11`` is where the detail lives: a learner who knows
    "ไม่ต้องมีดอก" still has to say whether a banana uses a หน่อ, a ไหล or a เหง้า.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(PROPAGULES)
        if rng.random() < 0.5:
            others = [name for name in PROPAGULE_STRUCTURES
                      if name != item.structure]
            rng.shuffle(others)
            return _labelled(
                stem=f"“{item.plant}” สืบพันธุ์แบบไม่อาศัยเพศโดยใช้ส่วนใดของต้นเดิม",
                correct=item.structure,
                wrongs=tuple(others[:3]),
                hint="นึกถึงว่าส่วนที่นำไปปลูกต่อได้ของพืชชนิดนั้นอยู่เหนือดินหรือใต้ดิน "
                     "และเป็นราก ลำต้น หรือใบ",
            )
        others = [other.plant for other in PROPAGULES
                  if other.structure != item.structure]
        rng.shuffle(others)
        return _labelled(
            stem=f"พืชในข้อใดสืบพันธุ์แบบไม่อาศัยเพศโดยใช้ “{item.structure}”",
            correct=item.plant,
            wrongs=tuple(others[:3]),
            hint="ไล่ทีละชนิดว่าส่วนที่นำไปขยายพันธุ์ของพืชนั้นคือส่วนใด",
        )


@question_type(
    "plant.reproduction_application",
    display_name={"th": "วิเคราะห์ผลของวิธีสืบพันธุ์ที่มีต่อลักษณะของต้นใหม่"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ReproductionApplication(QuestionType):
    """Explain why the offspring came out the way they did.

    Naming the mode is Foundation work. Every item here turns on the consequence
    the mode has — identical clones or varied seedlings — which is what makes the
    distinction matter to a grower.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, REPRODUCTION_SCENARIOS,
            hint="ถามก่อนว่ามีการปฏิสนธิเกิดขึ้นหรือไม่ "
                 "ถ้าไม่มี ต้นใหม่ย่อมมีพันธุกรรมเหมือนต้นเดิม",
            topic=TOPIC,
        )
