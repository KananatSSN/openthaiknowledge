"""วัฏจักรชีวิตของสัตว์

ชีวะ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.3/3

Sets moved here from: science_wave_b16.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, labelled, scenario_question
from otk.sets._support.science_wave_b15 import ANIMAL_TOPIC, _retopic
from otk.sets._support.science_wave_b16 import ANIMAL_CYCLE_SCENARIOS, PRIMARY_THREE

PROVENANCE = Provenance("original")


def _labelled(*, stem, correct, wrongs, hint):
    return _retopic(labelled(stem=stem, correct=correct, wrongs=wrongs, hint=hint),
                    ANIMAL_TOPIC)


class Cycle(NamedTuple):
    """One animal's life cycle and the group its pattern belongs to."""
    animal: str
    stages: tuple[str, ...]
    pattern: str


# ``pattern`` is what the comparing half of the indicator is about. Each pattern
# has more than one animal, so "which animals are alike" has a real answer.
CYCLES = (
    Cycle("ผีเสื้อ", ("ไข่", "หนอน", "ดักแด้", "ตัวเต็มวัย"),
          "มีระยะดักแด้ และตัวอ่อนมีรูปร่างต่างจากตัวเต็มวัยมาก"),
    Cycle("ยุง", ("ไข่", "ลูกน้ำ", "ตัวโม่ง", "ตัวเต็มวัย"),
          "มีระยะดักแด้ และตัวอ่อนมีรูปร่างต่างจากตัวเต็มวัยมาก"),
    Cycle("ตั๊กแตน", ("ไข่", "ตัวอ่อน", "ตัวเต็มวัย"),
          "ไม่มีระยะดักแด้ ตัวอ่อนมีรูปร่างคล้ายตัวเต็มวัยแต่เล็กกว่า"),
    Cycle("แมลงสาบ", ("ไข่", "ตัวอ่อน", "ตัวเต็มวัย"),
          "ไม่มีระยะดักแด้ ตัวอ่อนมีรูปร่างคล้ายตัวเต็มวัยแต่เล็กกว่า"),
    Cycle("กบ", ("ไข่", "ลูกอ๊อด", "ลูกอ๊อดมีขา", "กบตัวเต็มวัย"),
          "ออกไข่ในน้ำ ตัวอ่อนอาศัยในน้ำและหายใจด้วยเหงือกก่อนขึ้นบก"),
    Cycle("ไก่", ("ไข่", "ลูกไก่", "ไก่ตัวเต็มวัย"),
          "ออกลูกเป็นไข่ และลูกที่ฟักออกมามีรูปร่างคล้ายตัวเต็มวัย"),
    Cycle("แมว", ("ลูกแมวแรกเกิด", "ลูกแมว", "แมวตัวเต็มวัย"),
          "ออกลูกเป็นตัว ไม่มีระยะไข่ และลูกมีรูปร่างคล้ายตัวเต็มวัย"),
)


PATTERNS = tuple(dict.fromkeys(cycle.pattern for cycle in CYCLES))


@question_type(
    "animal.life_cycle_foundation",
    display_name={"th": "ระยะต่าง ๆ ในวัฏจักรชีวิตของสัตว์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class AnimalLifeCycleFoundation(QuestionType):
    """Follow one animal's own cycle, in order."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CYCLES)
        pool = [name for cycle in CYCLES for name in cycle.stages]
        if rng.random() < 0.5:
            index = rng.randrange(len(item.stages) - 1)
            current, following = item.stages[index], item.stages[index + 1]
            others = [name for name in dict.fromkeys(pool) if name != following]
            rng.shuffle(others)
            return _labelled(
                stem=f"วัฏจักรชีวิตของ “{item.animal}” หลังระยะ{current}"
                     f"จะเป็นระยะใดต่อไป",
                correct=following,
                wrongs=tuple(others[:3]),
                hint="นึกภาพสัตว์ชนิดนั้นตั้งแต่เกิดจนโตเต็มวัยตามลำดับ",
            )
        # ตั๊กแตน and แมลงสาบ have the same three stages. Keying on the stages
        # keeps that one cycle from being both the answer and a distractor, and
        # from appearing as two identical distractors.
        by_stages = {cycle.stages: cycle for cycle in CYCLES}
        wrong_cycles = [cycle for stages, cycle in by_stages.items()
                        if stages != item.stages]
        rng.shuffle(wrong_cycles)
        return _labelled(
            stem=f"ข้อใดเป็นวัฏจักรชีวิตของ “{item.animal}”",
            correct=" → ".join(item.stages),
            wrongs=tuple(" → ".join(cycle.stages) for cycle in wrong_cycles[:3]),
            hint="ดูว่าสัตว์ชนิดนี้ออกลูกเป็นไข่หรือเป็นตัว และมีระยะดักแด้หรือไม่",
        )


@question_type(
    "animal.life_cycle_fluency",
    display_name={"th": "เปรียบเทียบวัฏจักรชีวิตของสัตว์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class AnimalLifeCycleFluency(QuestionType):
    """Compare one animal's cycle with another's.

    This is the ``เปรียบเทียบวัฏจักรชีวิตของสัตว์บางชนิด`` half of ``ป.3/3``,
    which stands free of the model requirement — so this is the one set in the
    topic filed ``exact``.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CYCLES)
        partners = [cycle.animal for cycle in CYCLES
                    if cycle.pattern == item.pattern and cycle.animal != item.animal]
        # Three of the seven patterns belong to one animal each, so the
        # "which animal is alike" direction is only asked where there is one.
        if not partners or rng.random() < 0.5:
            others = [pattern for pattern in PATTERNS if pattern != item.pattern]
            rng.shuffle(others)
            return _labelled(
                stem=f"วัฏจักรชีวิตของ “{item.animal}” มีลักษณะอย่างไร",
                correct=item.pattern,
                wrongs=tuple(others[:3]),
                hint="ดูสามอย่าง ออกลูกเป็นไข่หรือเป็นตัว มีระยะดักแด้หรือไม่ "
                     "และตัวอ่อนหน้าตาเหมือนตัวเต็มวัยหรือไม่",
            )
        different = [cycle.animal for cycle in CYCLES
                     if cycle.pattern != item.pattern]
        rng.shuffle(different)
        return _labelled(
            stem=f"สัตว์ชนิดใดมีวัฏจักรชีวิตแบบเดียวกับ “{item.animal}”",
            correct=rng.choice(partners),
            wrongs=tuple(different[:3]),
            hint="เทียบทีละข้อว่ามีระยะเหมือนกันหรือไม่ โดยเฉพาะระยะไข่และระยะดักแด้",
        )


@question_type(
    "animal.life_cycle_application",
    display_name={"th": "ตีความแบบจำลองวัฏจักรชีวิตของสัตว์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=ANIMAL_TOPIC,
)
class AnimalLifeCycleApplication(QuestionType):
    """Read a life-cycle model, and say where it stops being a good likeness."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ANIMAL_CYCLE_SCENARIOS,
            hint="ไล่ตามลำดับของระยะให้ครบ และดูว่าสัตว์สองชนิดนั้นเหมือนหรือ"
                 "ต่างกันตรงระยะใด",
        ), ANIMAL_TOPIC)
