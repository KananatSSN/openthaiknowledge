"""กลไกการหายใจและการแลกเปลี่ยนแก๊ส

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/2

Sets moved here from: science_wave_b8.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import contextual_scenario_question
from otk.sets._support.science_wave_b8 import BREATHING_SCENARIOS, LEVEL, SUBJECT, TOPIC, _labelled

PROVENANCE = Provenance("original")


INHALE = "การหายใจเข้า"


EXHALE = "การหายใจออก"


# Four statements true of each phase. Two phases would give two choices if asked
# directly, so the item offers statements and every wrong one is true of the
# other phase.
INHALE_FACTS = (
    "กะบังลมหดตัวและเลื่อนต่ำลง",
    "กระดูกซี่โครงถูกยกสูงขึ้นและเลื่อนออกไปข้างหน้า",
    "ปริมาตรของช่องอกเพิ่มขึ้นและความดันอากาศภายในลดลง",
    "อากาศจากภายนอกเคลื่อนเข้าสู่ปอด",
)


EXHALE_FACTS = (
    "กะบังลมคลายตัวและโค้งสูงขึ้น",
    "กระดูกซี่โครงถูกลดต่ำลงและเลื่อนกลับเข้าที่เดิม",
    "ปริมาตรของช่องอกลดลงและความดันอากาศภายในเพิ่มขึ้น",
    "อากาศภายในปอดเคลื่อนออกสู่ภายนอก",
)


class Exchange(NamedTuple):
    """One gas moving at one place, and where it moves from and to."""
    place: str
    gas: str
    direction: str


# The four movements ม.2/2 names. Direction is stored per (place, gas), so the
# alveolus and the tissue cannot be stated inconsistently.
EXCHANGES = (
    Exchange("ที่ถุงลมในปอด", "แก๊สออกซิเจน", "แพร่จากถุงลมเข้าสู่เลือด"),
    Exchange("ที่ถุงลมในปอด", "แก๊สคาร์บอนไดออกไซด์", "แพร่จากเลือดเข้าสู่ถุงลม"),
    Exchange("ที่เนื้อเยื่อของร่างกาย", "แก๊สออกซิเจน", "แพร่จากเลือดเข้าสู่เซลล์"),
    Exchange("ที่เนื้อเยื่อของร่างกาย", "แก๊สคาร์บอนไดออกไซด์",
             "แพร่จากเซลล์เข้าสู่เลือด"),
)


# Movements learners often believe but that never happen, offered only as wrong
# choices; the real ones above stay the core of every item.
EXCHANGE_MISCONCEPTIONS = (
    "ถูกหัวใจสูบผ่านผนังถุงลมโดยไม่ต้องแพร่",
    "ไม่เคลื่อนที่เลย เพราะความเข้มข้นทั้งสองฝั่งเท่ากันตลอดเวลา",
)


EXCHANGE_PLACE_DECOYS = ("ที่กระเพาะอาหาร แก๊สออกซิเจน", "ที่หัวใจห้องบนขวา แก๊สคาร์บอนไดออกไซด์")


@question_type(
    "body.breathing_mechanism_foundation",
    display_name={"th": "กลไกการหายใจเข้าและการหายใจออก"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class BreathingMechanismFoundation(QuestionType):
    """Which statement is true of the phase named in the stem.

    Two phases means two choices if asked directly, so the item offers four
    statements and every wrong one is true of the other phase.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        inhaling = rng.random() < 0.5
        mine = list(INHALE_FACTS if inhaling else EXHALE_FACTS)
        theirs = list(EXHALE_FACTS if inhaling else INHALE_FACTS)
        rng.shuffle(theirs)
        return _labelled(
            stem=f"ข้อใดเกิดขึ้นใน “{INHALE if inhaling else EXHALE}”",
            correct=rng.choice(mine),
            wrongs=tuple(theirs[:3]),
            hint="เริ่มจากกะบังลม: หดตัวแล้วช่องอกขยาย ความดันลด อากาศจึงไหลเข้า "
                 "คลายตัวแล้วเป็นตรงกันข้าม",
        )


@question_type(
    "body.gas_exchange_fluency",
    display_name={"th": "การแลกเปลี่ยนแก๊สที่ถุงลมและที่เนื้อเยื่อ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class GasExchangeFluency(QuestionType):
    """Say which way each gas moves, at the lung and at the tissue.

    This is the half of ``ม.2/2`` that carries no model requirement, so it is the
    one set here filed ``exact``. Every wrong choice is a real movement stated for
    the wrong place or the wrong gas.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(EXCHANGES)
        others = [other.direction for other in EXCHANGES
                  if other.direction != item.direction] + list(EXCHANGE_MISCONCEPTIONS)
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"{item.place} “{item.gas}” เคลื่อนที่อย่างไร",
                correct=item.direction,
                wrongs=tuple(others[:3]),
                hint="แก๊สแพร่จากบริเวณที่มีความเข้มข้นของแก๊สนั้นสูงไปยังบริเวณที่ต่ำกว่าเสมอ",
            )
        wrong_pairs = [f"{other.place} {other.gas}" for other in EXCHANGES
                       if other.direction != item.direction] + list(EXCHANGE_PLACE_DECOYS)
        rng.shuffle(wrong_pairs)
        return _labelled(
            stem=f"การเคลื่อนที่ที่ว่า “{item.direction}” เกิดขึ้นที่ใดและเป็นแก๊สใด",
            correct=f"{item.place} {item.gas}",
            wrongs=tuple(wrong_pairs[:3]),
            hint="ที่ปอดเลือดกำลังรับออกซิเจนและปล่อยคาร์บอนไดออกไซด์ "
                 "ส่วนที่เนื้อเยื่อเป็นตรงกันข้าม",
        )


@question_type(
    "body.breathing_application",
    display_name={"th": "ตีความแบบจำลองการหายใจและการแลกเปลี่ยนแก๊ส"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class BreathingApplication(QuestionType):
    """Read the bell-jar model, and follow gas concentration into real situations.

    Two items ask about the model — what it shows and where it stops being a good
    likeness — which is as close as multiple choice gets to ``โดยใช้แบบจำลอง``.
    The rest follow the concentration difference into altitude and exercise.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, BREATHING_SCENARIOS,
            hint="สำหรับกลไกให้เริ่มที่ปริมาตรและความดัน "
                 "สำหรับการแลกเปลี่ยนแก๊สให้เริ่มที่ความแตกต่างของความเข้มข้น",
            topic=TOPIC,
        )
