"""แบบรูปการเปลี่ยนแปลงรูปร่างปรากฏของดวงจันทร์

ดาราศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.4/2

Sets moved here from: science_wave_c4.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import PRIMARY_FOUR
from otk.sets._support.science_wave_c1 import SKY_TOPIC, SUBJECT
from otk.sets._support.science_wave_c4 import MOON_SHAPE_SCENARIOS

PROVENANCE = Provenance("original")


MOON_MODEL = (
    "ครูวางโคมไฟไว้กลางห้องมืดแทนดวงอาทิตย์ ให้นักเรียนคนหนึ่งยืนอยู่กับที่โดยให้ศีรษะ"
    "แทนโลก แล้วถือลูกบอลทาสีขาวแทนดวงจันทร์ยื่นออกไป ค่อย ๆ หมุนตัวพาลูกบอลไปรอบตัวเอง "
    "จนครบหนึ่งรอบ "
)


MOON_MODEL_SEEN = (
    "ด้านของลูกบอลที่หันเข้าหาโคมไฟสว่างอยู่เสมอและสว่างเท่าเดิมตลอด "
    "แต่ส่วนที่นักเรียนมองเห็นว่าสว่างกลับค่อย ๆ เปลี่ยนไป "
    "จากมองไม่เห็นเลย เป็นเสี้ยว เป็นครึ่งดวง จนเต็มดวง แล้วค่อย ๆ ลดลงจนมองไม่เห็นอีกครั้ง"
)


class Phase(NamedTuple):
    """One point of the cycle: what it is called and what it looks like."""
    name: str
    look: str


# Four points of one cycle, about seven to eight days apart. The two half-moons
# are told apart by which way they are heading, so no two ``look`` values repeat.
CYCLE = (
    Phase("จันทร์ดับ (แรม 15 ค่ำ)", "มองไม่เห็นดวงจันทร์"),
    Phase("ขึ้น 8 ค่ำ", "สว่างครึ่งดวง และกำลังสว่างมากขึ้นทุกคืน"),
    Phase("ขึ้น 15 ค่ำ (จันทร์เต็มดวง)", "สว่างเต็มดวงทั้งดวง"),
    Phase("แรม 8 ค่ำ", "สว่างครึ่งดวง และกำลังสว่างน้อยลงทุกคืน"),
)


# Looks that none of the four phases in CYCLE shows.
LOOK_DECOYS = ("มองเห็นดวงจันทร์สองดวงพร้อมกัน", "สว่างครึ่งดวง และไม่เปลี่ยนแปลงอีกเลย")


@question_type(
    "astro.moon_shape_cycle_foundation",
    display_name={"th": "อธิบายการเปลี่ยนรูปร่างปรากฏของดวงจันทร์"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=SKY_TOPIC,
)
class MoonShapeCycleFoundation(QuestionType):
    """Explain the pattern from the lamp-and-ball model — the first free verb.

    The indicator's model clause is ``สร้างแบบจำลองที่อธิบาย``, so what is assessed
    is the explanation, and the model is carried in the stem.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem = f"{MOON_MODEL}ผลที่สังเกตได้คือ {MOON_MODEL_SEEN} "
        draw = rng.random()
        if draw < 0.4:
            return _labelled(
                stem=stem + "จากแบบจำลองนี้ ข้อใดอธิบายการเปลี่ยนรูปร่างปรากฏ"
                            "ของดวงจันทร์ได้ถูกต้อง",
                correct="ด้านสว่างของดวงจันทร์มีเท่าเดิมเสมอ แต่เมื่อดวงจันทร์โคจรไป เราเห็นด้านสว่างมากน้อยต่างกัน",
                wrongs=tuple((
                    "ดวงจันทร์ค่อย ๆ สว่างขึ้นและหรี่ลงเองในแต่ละคืน เพราะแสงในตัวดวงจันทร์เปลี่ยนไป",
                    "เงาของโลกค่อย ๆ บังดวงจันทร์ทีละส่วนจนมิดแล้วจึงเปิดออก",
                    "เมฆบังดวงจันทร์ไว้มากน้อยต่างกันในแต่ละคืน",
                    "ดวงจันทร์หมุนรอบตัวเองจนด้านมืดหันมาหาเราทีละน้อย",
                    "ดวงจันทร์เปลี่ยนขนาดจริงตามระยะห่างจากโลกในแต่ละคืน จึงเห็นส่วนสว่างมากน้อยต่างกัน",
                )),
                hint="ในแบบจำลอง สิ่งที่เปลี่ยนไปคือมุมที่เรามอง ไม่ใช่ความสว่างของลูกบอล",
                topic=SKY_TOPIC,
            )
        if draw < 0.7:
            item = rng.choice(CYCLE)
            return _labelled(
                stem=f"“{item.name}” เรามองเห็นดวงจันทร์เป็นอย่างไร",
                correct=item.look,
                wrongs=tuple([other.look for other in CYCLE if other.name != item.name]
                                        + list(LOOK_DECOYS)),
                hint="นึกถึงลำดับของรูปร่างปรากฏในหนึ่งเดือน",
                topic=SKY_TOPIC,
            )
        return _labelled(
            stem="แบบรูปการเปลี่ยนรูปร่างปรากฏของดวงจันทร์ในหนึ่งรอบเป็นอย่างไร",
            correct="จันทร์ดับ แล้วสว่างขึ้นจนเต็มดวง แล้วค่อย ๆ ลดลงจนจันทร์ดับอีกครั้ง ซ้ำเป็นรอบ",
            wrongs=("เต็มดวงทุกคืน แล้วดับไปทันทีเมื่อครบหนึ่งเดือน แล้วเริ่มเต็มดวงใหม่",
                    "สว่างขึ้นเรื่อย ๆ ไปไม่มีที่สิ้นสุดจนสว่างกว่าดวงอาทิตย์ แล้วไม่ลดลงอีกเลย",
                    "เปลี่ยนรูปร่างไปมาโดยไม่มีลำดับที่แน่นอน"),
            hint="นึกว่าหลังจากเต็มดวงแล้วดวงจันทร์จะสว่างมากขึ้นหรือน้อยลง",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.moon_shape_cycle_fluency",
    display_name={"th": "พยากรณ์รูปร่างปรากฏของดวงจันทร์"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=SKY_TOPIC,
)
class MoonShapeCycleFluency(QuestionType):
    """Predict the next shape — the indicator's second free verb, ``พยากรณ์``."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(CYCLE))
        here = CYCLE[index]
        days = rng.choice((7, 8))
        if rng.random() < 0.5:
            nxt = CYCLE[(index + 1) % len(CYCLE)]
            return _labelled(
                stem=f"คืนนี้เป็น “{here.name}” อีกประมาณ {days} วัน "
                     "จะมองเห็นดวงจันทร์เป็นอย่างไร",
                correct=nxt.look,
                wrongs=tuple([other.look for other in CYCLE if other.name != nxt.name]
                                        + list(LOOK_DECOYS)),
                hint="ไล่ลำดับของรูปร่างปรากฏไปข้างหน้าทีละขั้น",
                topic=SKY_TOPIC,
            )
        nxt = CYCLE[(index + 2) % len(CYCLE)]
        return _labelled(
            stem=f"คืนนี้เป็น “{here.name}” อีกประมาณ {days * 2} วัน "
                 "จะมองเห็นดวงจันทร์เป็นอย่างไร",
            correct=nxt.look,
            wrongs=tuple([other.look for other in CYCLE if other.name != nxt.name]
                                    + list(LOOK_DECOYS)),
            hint="ไล่ลำดับของรูปร่างปรากฏไปข้างหน้าสองขั้น",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.moon_shape_cycle_application",
    display_name={"th": "ใช้แบบรูปรูปร่างปรากฏของดวงจันทร์"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=SKY_TOPIC,
)
class MoonShapeCycleApplication(QuestionType):
    """Judge a prediction, a shadow explanation, and the lunar calendar."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, MOON_SHAPE_SCENARIOS,
            hint="ถามว่าด้านสว่างของดวงจันทร์เปลี่ยนไปจริงหรือเพียงมุมที่เรามองเปลี่ยนไป",
        ), SKY_TOPIC)
