"""วัฏจักรชีวิตของพืชดอก

ชีวะ · ป.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.2/3

Sets moved here from: science_wave_b15.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import PLANT_TOPIC, _labelled
from otk.sets._support.science_wave_b15 import PLANT_CYCLE_SCENARIOS, PRIMARY_TWO, _retopic

PROVENANCE = Provenance("original")


class Stage(NamedTuple):
    """One stage of the flowering-plant life cycle."""
    name: str
    happening: str


FLOWER_STAGES = (
    Stage("เมล็ด", "เป็นระยะเริ่มต้นที่มีต้นอ่อนและอาหารสะสมอยู่ข้างใน"),
    Stage("ต้นอ่อน", "เมล็ดงอกออกมาเป็นต้นเล็ก ๆ มีรากหยั่งลงดินและมีใบเลี้ยง"),
    Stage("ต้นโตเต็มวัย", "ต้นสูงขึ้น มีรากและใบมากขึ้น จนพร้อมที่จะออกดอกได้"),
    Stage("ออกดอก", "ต้นสร้างดอกขึ้นมา ซึ่งเป็นส่วนที่ทำให้เกิดผลและเมล็ดต่อไป"),
    Stage("ติดผลและเกิดเมล็ดใหม่", "ดอกกลายเป็นผล ภายในผลมีเมล็ดที่จะงอกเป็นต้นใหม่ได้"),
)


# The cycle in order. It is a cycle, so the last stage leads back to the first.
FLOWER_CYCLE = tuple(stage.name for stage in FLOWER_STAGES)


@question_type(
    "plant.life_cycle_foundation",
    display_name={"th": "ระยะต่าง ๆ ในวัฏจักรชีวิตของพืชดอก"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantLifeCycleFoundation(QuestionType):
    """Say what happens in a stage, or name the stage described."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(FLOWER_STAGES)
        others = [other for other in FLOWER_STAGES if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ในระยะ “{item.name}” เกิดอะไรขึ้นกับพืช",
                correct=item.happening,
                wrongs=tuple(other.happening for other in others[:3]),
                hint="นึกภาพต้นไม้ในระยะนั้นว่ามีอะไรบ้าง มีรากแล้วหรือยัง "
                     "มีดอกแล้วหรือยัง",
                topic=PLANT_TOPIC,
            )
        return _labelled(
            stem=f"ระยะใดของพืชดอกที่{item.happening}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านให้จบว่าเกิดอะไรขึ้น แล้วจึงเลือกชื่อระยะนั้น",
            topic=PLANT_TOPIC,
        )


@question_type(
    "plant.life_cycle_fluency",
    display_name={"th": "ลำดับของวัฏจักรชีวิตพืชดอก"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantLifeCycleFluency(QuestionType):
    """Follow the cycle round, including back to the seed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            # Back one step: the stage that comes just before, round the cycle.
            index = rng.randrange(len(FLOWER_CYCLE))
            current = FLOWER_CYCLE[index]
            before = FLOWER_CYCLE[index - 1]
            others = [name for name in FLOWER_CYCLE if name != before]
            rng.shuffle(others)
            return _labelled(
                stem=f"ก่อนจะถึงระยะ “{current}” พืชดอกอยู่ในระยะใด",
                correct=before,
                wrongs=tuple(others[:3]),
                hint="วัฏจักรชีวิตหมุนเป็นวง ระยะเมล็ดเกิดต่อจากการติดผลและเกิดเมล็ดใหม่",
                topic=PLANT_TOPIC,
            )
        if roll < 0.6:
            index = rng.randrange(len(FLOWER_CYCLE))
            current = FLOWER_CYCLE[index]
            following = FLOWER_CYCLE[(index + 1) % len(FLOWER_CYCLE)]
            others = [name for name in FLOWER_CYCLE if name != following]
            rng.shuffle(others)
            return _labelled(
                stem=f"หลังจากระยะ “{current}” พืชดอกจะเข้าสู่ระยะใดต่อไป",
                correct=following,
                wrongs=tuple(others[:3]),
                hint="วัฏจักรชีวิตหมุนเป็นวง เมื่อเกิดเมล็ดใหม่แล้วก็เริ่มต้นใหม่ได้อีก",
                topic=PLANT_TOPIC,
            )
        swapped = list(FLOWER_CYCLE)
        swapped[1], swapped[3] = swapped[3], swapped[1]
        late = list(FLOWER_CYCLE)
        late[3], late[4] = late[4], late[3]
        early = list(FLOWER_CYCLE)
        early[0], early[1] = early[1], early[0]
        return _labelled(
            stem="ข้อใดเรียงลำดับวัฏจักรชีวิตของพืชดอก โดยเริ่มจากเมล็ด ได้ถูกต้อง",
            correct=" → ".join(FLOWER_CYCLE),
            wrongs=(" → ".join(reversed(FLOWER_CYCLE)), " → ".join(swapped),
                    " → ".join(FLOWER_CYCLE[2:] + FLOWER_CYCLE[:2]),
                    " → ".join(late), " → ".join(early)),
            hint="โจทย์บอกให้เริ่มจากเมล็ด แล้วต้นอ่อนจึงงอกออกมาก่อนอย่างอื่น",
            topic=PLANT_TOPIC,
        )


@question_type(
    "plant.life_cycle_application",
    display_name={"th": "ตีความแบบจำลองวัฏจักรชีวิตของพืชดอก"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantLifeCycleApplication(QuestionType):
    """Read a life-cycle model, and say where it stops being a good likeness."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, PLANT_CYCLE_SCENARIOS,
            hint="ไล่ตามลำดับของระยะให้ครบ และจำไว้ว่าเมล็ดใหม่เริ่มวัฏจักรใหม่ได้",
        ), PLANT_TOPIC)
