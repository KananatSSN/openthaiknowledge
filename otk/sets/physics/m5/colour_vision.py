"""การมองเห็นสีของวัตถุและความผิดปกติในการมองเห็นสี

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/9

Sets moved here from: science_wave_e15.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e15 import (
    COLOUR_NAME,
    LIGHT_NAME,
    OBJECTS,
    PRIMARY_LIGHTS,
    SUBJECT,
    UPPER_FIVE,
    B,
    G,
    R,
    _colour_choices,
    _labelled,
)

PROVENANCE = Provenance("original")


TOPIC_COLOUR_VISION = "การมองเห็นสีของวัตถุและความผิดปกติในการมองเห็นสี"


def seen_colour(reflects: frozenset, light: frozenset) -> str:
    """An object shows only the part of the incoming light it reflects."""
    return COLOUR_NAME[reflects & light]


VISION_TRUE = (
    "เราเห็นวัตถุเป็นสีใด เพราะวัตถุสะท้อนแสงสีนั้นเข้าสู่ตา และดูดกลืนแสงสีอื่นไว้",
    "เซลล์รูปกรวยในจอตามีสามชนิด ไวต่อแสงสีแดง สีเขียว และสีน้ำเงิน",
    "เซลล์รูปแท่งไวต่อแสงสลัวแต่แยกสีไม่ได้ ในที่มืดจึงแยกสีได้ยาก",
    "ผู้ที่ตาบอดสีแดง-เขียวมีเซลล์รูปกรวยที่ไวต่อแสงสีแดงหรือสีเขียวทำงานผิดปกติ",
    "ภาวะตาบอดสีส่วนใหญ่ถ่ายทอดทางพันธุกรรม และพบในเพศชายมากกว่าเพศหญิง",
    "ผู้ที่ตาบอดสีอาจจำแนกสัญญาณไฟจราจรโดยดูจากตำแหน่งของดวงไฟ",
)


VISION_FALSE = (
    "วัตถุสีแดงสร้างแสงสีแดงขึ้นเองแล้วส่งเข้าสู่ตา",
    "วัตถุสีดำสะท้อนแสงทุกสีเข้าสู่ตา",
    "เซลล์รูปแท่งทำหน้าที่แยกสีได้ดีที่สุดในที่สว่าง",
    "คนตาบอดสีมองไม่เห็นสีใดเลย เห็นเป็นภาพขาวดำเท่านั้น",
    "ภาวะตาบอดสีเกิดจากการมองแสงจ้ามากเกินไปเท่านั้น",
    "เซลล์รูปกรวยในจอตามีเพียงชนิดเดียวแต่รับได้ทุกสี",
)


@question_type(
    "phys.colour_vision_foundation",
    display_name={"th": "วัตถุมีสีเพราะอะไร และตามองเห็นสีได้อย่างไร"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLOUR_VISION,
)
class ColourVisionFoundation(QuestionType):
    """Under white light: what an object reflects is its colour."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        colour = rng.choice([c for c in COLOUR_NAME if c and len(c) < 3])
        name = COLOUR_NAME[colour]
        thing, _ = rng.choice(OBJECTS)
        if rng.random() < 0.5:
            reflected = "และ".join(LIGHT_NAME[frozenset({p})] for p in (R, G, B) if p in colour)
            return _labelled(
                stem=f"{thing}ที่อยู่ใต้แสงขาวสะท้อน{reflected}เข้าสู่ตา และดูดกลืนแสงสีอื่นไว้ เราจะเห็น{thing}เป็นสีใด",
                correct=name, wrongs=_colour_choices(name, rng),
                topic=TOPIC_COLOUR_VISION,
                hint="สีที่เห็นคือแสงที่วัตถุสะท้อนเข้าตา แสงแดงรวมกับแสงเขียวเห็นเป็นสีเหลือง")
        absorbed = [LIGHT_NAME[frozenset({p})] for p in (R, G, B) if p not in colour]
        correct = f"สะท้อน{'และ'.join(LIGHT_NAME[frozenset({p})] for p in (R, G, B) if p in colour)} และดูดกลืน{'และ'.join(absorbed)}"
        wrong_swap = f"สะท้อน{'และ'.join(absorbed)} และดูดกลืน{'และ'.join(LIGHT_NAME[frozenset({p})] for p in (R, G, B) if p in colour)}"
        return _labelled(
            stem=f"{thing}{name}ที่อยู่ใต้แสงขาวสะท้อนและดูดกลืนแสงสีใด",
            correct=correct,
            wrongs=(wrong_swap, "สะท้อนแสงทุกสีเท่ากัน", "ดูดกลืนแสงทุกสีไว้หมด"),
            topic=TOPIC_COLOUR_VISION,
            hint="แสงขาวประกอบด้วยแสงสีแดง เขียว และน้ำเงิน วัตถุสะท้อนสีที่เราเห็นและดูดกลืนสีที่เหลือ")


@question_type(
    "phys.colour_vision_fluency",
    display_name={"th": "อธิบายสีที่เห็นเมื่อแสงที่ส่องเปลี่ยนไป และความผิดปกติในการมองเห็นสี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLOUR_VISION,
)
class ColourVisionFluency(QuestionType):
    """Both objects of the indicator: seeing colour under coloured light, and colour blindness."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            reflects = rng.choice([c for c in COLOUR_NAME if c and len(c) < 3])
            light = rng.choice([c for c in COLOUR_NAME if c and c != frozenset({R, G, B})])
            thing, _ = rng.choice(OBJECTS)
            correct = seen_colour(reflects, light)
            return _labelled(
                stem=(f"{thing}ที่เห็นเป็น{COLOUR_NAME[reflects]}ใต้แสงขาว เมื่อนำไปไว้ในห้องมืดแล้วส่อง"
                      f"ด้วย{LIGHT_NAME[light]}เพียงอย่างเดียว จะเห็น{thing}เป็นสีใด"),
                correct=correct, wrongs=_colour_choices(correct, rng),
                topic=TOPIC_COLOUR_VISION,
                hint="วัตถุสะท้อนได้เฉพาะแสงสีที่ส่องมาและเป็นสีที่วัตถุสะท้อนได้ ถ้าไม่มีสีใดตรงกันจะเห็นเป็นสีดำ")
        if rng.random() < 0.5:
            return _labelled(
                stem="ข้อใดอธิบายการมองเห็นสีหรือภาวะตาบอดสีได้ถูกต้อง",
                correct=rng.choice(VISION_TRUE), wrongs=tuple(VISION_FALSE),
                topic=TOPIC_COLOUR_VISION,
                hint="สีเกิดจากแสงที่วัตถุสะท้อน ตาแยกสีได้ด้วยเซลล์รูปกรวยสามชนิด ตาบอดสีคือเซลล์รูปกรวยบางชนิดผิดปกติ")
        return _labelled(
            stem="ผู้ที่มีภาวะตาบอดสีแดง-เขียวน่าจะแยกคู่สีใดได้ยากที่สุด",
            correct="สีแดงกับสีเขียว",
            wrongs=("สีน้ำเงินกับสีเหลือง", "สีดำกับสีขาว", "สีน้ำเงินกับสีขาว"),
            topic=TOPIC_COLOUR_VISION,
            hint="ตาบอดสีแดง-เขียวเกิดจากเซลล์รูปกรวยที่ไวต่อแสงสีแดงหรือสีเขียวผิดปกติ")


@question_type(
    "phys.colour_vision_application",
    display_name={"th": "ใช้การสะท้อนแสงสีอธิบายสถานการณ์และออกแบบให้ทุกคนเห็นได้"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLOUR_VISION,
)
class ColourVisionApplication(QuestionType):
    """Two lights on one object, a stage under one colour, and design for colour-blind readers."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            # Two coloured lights at once: the light falling is their union.
            a, b = rng.sample(PRIMARY_LIGHTS, 2)
            reflects = rng.choice([c for c in COLOUR_NAME if c and len(c) < 3])
            thing, _ = rng.choice(OBJECTS)
            correct = seen_colour(reflects, a | b)
            return _labelled(
                stem=(f"{thing}ที่เห็นเป็น{COLOUR_NAME[reflects]}ใต้แสงขาว ถูกส่องพร้อมกันด้วย{LIGHT_NAME[a]}"
                      f"และ{LIGHT_NAME[b]}ในห้องมืด จะเห็น{thing}เป็นสีใด"),
                correct=correct, wrongs=_colour_choices(correct, rng),
                topic=TOPIC_COLOUR_VISION,
                hint="หาก่อนว่าแสงที่ส่องมารวมกันมีแสงสีใดบ้าง แล้วดูว่าวัตถุสะท้อนสีใดในนั้นได้")
        if shape == 1:
            # Exactly one costume reflects none of the light; the other three
            # all contain it, so there is one right answer.
            light = rng.choice(PRIMARY_LIGHTS)
            answer = rng.choice([c for c in COLOUR_NAME if c and len(c) < 3 and not c & light])
            others = [c for c in COLOUR_NAME if c and len(c) < 3 and c & light]
            return _labelled(
                stem=f"บนเวทีที่ส่องด้วย{LIGHT_NAME[light]}เพียงอย่างเดียว เครื่องแต่งกายสีใด (สีใต้แสงขาว) จะเห็นเป็นสีดำ",
                correct=COLOUR_NAME[answer], wrongs=tuple(COLOUR_NAME[c] for c in others),
                topic=TOPIC_COLOUR_VISION,
                hint="วัตถุจะดูดำเมื่อไม่สะท้อนแสงสีที่ส่องมาเลย")
        return _labelled(
            stem="การออกแบบแผนที่หรือกราฟให้ผู้ที่ตาบอดสีแดง-เขียวอ่านได้ ควรทำอย่างไร",
            correct=rng.choice(("ใช้สัญลักษณ์หรือลวดลายต่างกันควบคู่กับสี",
                                "เลือกคู่สีที่ต่างกันมาก เช่น น้ำเงินกับส้ม แทนแดงกับเขียว")),
            wrongs=("ใช้สีแดงและสีเขียวที่สดขึ้น", "ใช้เฉพาะสีแดงกับสีเขียวเพื่อให้ดูง่าย",
                    "ทำให้ตัวอักษรเล็กลงเพื่อให้ใส่สีได้มากขึ้น"),
            topic=TOPIC_COLOUR_VISION,
            hint="ผู้ที่ตาบอดสีแดง-เขียวแยกแดงกับเขียวได้ยาก ข้อมูลจึงไม่ควรพึ่งความต่างของสองสีนี้อย่างเดียว")
