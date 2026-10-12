"""การจัดระบบของสิ่งมีชีวิต

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/4

Sets moved here from: science_wave_b2.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import contextual_scenario_question
from otk.sets._support.science_wave_b2 import (
    LEVEL,
    ORGANISATION_SCENARIOS,
    SUBJECT,
    TOPIC,
    _labelled,
)

PROVENANCE = Provenance("original")


class BodyLevel(NamedTuple):
    """One rung of the ladder from cell to organism."""
    name: str
    definition: str
    example: str


# Ascending, exactly the five rungs ``ม.1/4`` names. Order lives here and nowhere
# else, so the "what comes next" question and the "what is this" question are
# answered from the same list.
BODY_LEVELS = (
    BodyLevel("เซลล์", "หน่วยพื้นฐานที่เล็กที่สุดของสิ่งมีชีวิต",
              "เซลล์กล้ามเนื้อหนึ่งเซลล์"),
    BodyLevel("เนื้อเยื่อ", "กลุ่มของเซลล์ชนิดเดียวกันที่ทำหน้าที่อย่างเดียวกัน",
              "เนื้อเยื่อกล้ามเนื้อหัวใจ"),
    BodyLevel("อวัยวะ", "กลุ่มของเนื้อเยื่อหลายชนิดที่ทำงานร่วมกันเป็นโครงสร้างหนึ่ง",
              "หัวใจ"),
    BodyLevel("ระบบอวัยวะ", "กลุ่มของอวัยวะหลายอวัยวะที่ทำงานร่วมกันเป็นระบบ",
              "ระบบหมุนเวียนเลือด"),
    BodyLevel("สิ่งมีชีวิต", "ผลรวมของทุกระบบอวัยวะที่ทำงานประสานกันจนดำรงชีวิตได้",
              "คนหนึ่งคน"),
)


BODY_LEVEL_NAMES = tuple(level.name for level in BODY_LEVELS)


@question_type(
    "cell.organisation_foundation",
    display_name={"th": "ระดับการจัดระบบของสิ่งมีชีวิต"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class OrganisationFoundation(QuestionType):
    """Name a level from its definition, or from an example of it.

    ``ecology.levels`` climbs the *other* ladder — สิ่งมีชีวิต up to ชีวมณฑล.
    This one goes downward from the organism into its parts, which is where ม.1/4
    starts, and the two must not be confused: ประชากร is not a rung here.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(BODY_LEVELS)
        others = [other for other in BODY_LEVELS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.definition}” คือระดับใดของการจัดระบบของสิ่งมีชีวิต",
                correct=item.name,
                wrongs=tuple(other.name for other in others[:3]),
                hint="ไล่จากเล็กไปใหญ่: เซลล์ เนื้อเยื่อ อวัยวะ ระบบอวัยวะ สิ่งมีชีวิต",
            )
        return _labelled(
            stem=f"“{item.example}” จัดอยู่ในระดับใดของการจัดระบบของสิ่งมีชีวิต",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="ถามว่าสิ่งนั้นประกอบขึ้นจากอะไร แล้วสิ่งที่ประกอบขึ้นนั้นอยู่ระดับใด",
        )


@question_type(
    "cell.organisation_fluency",
    display_name={"th": "ลำดับของระดับการจัดระบบของสิ่งมีชีวิต"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class OrganisationFluency(QuestionType):
    """Put the rungs in order, and say which one contains which.

    Knowing the five names is Foundation work. ``ม.1/4`` asks for the sequence —
    that each level is built out of the one below it — which is what these two
    branches make the learner use.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            index = rng.randrange(1, len(BODY_LEVELS))
            upper, lower = BODY_LEVELS[index], BODY_LEVELS[index - 1]
            others = [name for name in BODY_LEVEL_NAMES if name != lower.name]
            rng.shuffle(others)
            return _labelled(
                stem=f"ระดับที่เล็กถัดลงมาจาก “{upper.name}” หนึ่งระดับคือระดับใด",
                correct=lower.name,
                wrongs=tuple(others[:3]),
                hint="แต่ละระดับประกอบขึ้นจากหลายหน่วยของระดับที่อยู่ต่ำกว่าหนึ่งขั้น",
            )
        if roll < 0.6:
            index = rng.randrange(len(BODY_LEVELS) - 1)
            lower, upper = BODY_LEVELS[index], BODY_LEVELS[index + 1]
            others = [name for name in BODY_LEVEL_NAMES if name != upper.name]
            rng.shuffle(others)
            return _labelled(
                stem=f"ระดับที่ใหญ่ถัดขึ้นไปจาก “{lower.name}” หนึ่งระดับคือระดับใด",
                correct=upper.name,
                wrongs=tuple(others[:3]),
                hint="แต่ละระดับประกอบขึ้นจากหลายหน่วยของระดับที่อยู่ต่ำกว่าหนึ่งขั้น",
            )
        correct = " → ".join(BODY_LEVEL_NAMES)
        reversed_order = " → ".join(reversed(BODY_LEVEL_NAMES))
        swapped = list(BODY_LEVEL_NAMES)
        swapped[1], swapped[2] = swapped[2], swapped[1]
        dropped = [name for name in BODY_LEVEL_NAMES if name != "เนื้อเยื่อ"]
        late = list(BODY_LEVEL_NAMES)
        late[2], late[3] = late[3], late[2]
        early = list(BODY_LEVEL_NAMES)
        early[0], early[1] = early[1], early[0]
        return _labelled(
            stem="ข้อใดเรียงลำดับการจัดระบบของสิ่งมีชีวิตจากเล็กไปใหญ่ได้ถูกต้อง",
            correct=correct,
            wrongs=(reversed_order, " → ".join(swapped),
                    " → ".join(dropped + ["ประชากร"]),
                    " → ".join(late), " → ".join(early)),
            hint="เริ่มจากหน่วยที่เล็กที่สุดของสิ่งมีชีวิต แล้วไล่ขึ้นไปจนถึงตัวสิ่งมีชีวิตเอง",
        )


@question_type(
    "cell.organisation_application",
    display_name={"th": "ไล่ผลกระทบข้ามระดับการจัดระบบของสิ่งมีชีวิต"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class OrganisationApplication(QuestionType):
    """Follow a change at one level through to another.

    Ordering the ladder is Fluency work. Here a real change — a faulty valve, a
    drug binding a membrane — has to be traced across levels, which is what the
    ladder is for.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, ORGANISATION_SCENARIOS,
            hint="ระบุก่อนว่าเหตุการณ์เริ่มที่ระดับใด แล้วจึงไล่ขึ้นไปทีละระดับ",
            topic=TOPIC,
        )
