"""การตกไข่ ประจำเดือน การปฏิสนธิ และการตั้งครรภ์

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/15

Sets moved here from: science_wave_b13.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import LEVEL, SUBJECT, TOPIC, labelled, scenario_question
from otk.sets._support.science_wave_b13 import PREGNANCY_SCENARIOS

PROVENANCE = Provenance("original")


class Event(NamedTuple):
    """One event of the cycle or the pregnancy, and what happens in it."""
    name: str
    description: str


EVENTS = (
    Event("การตกไข่",
          "รังไข่ปล่อยเซลล์ไข่ที่เจริญเต็มที่ออกมาสู่ท่อนำไข่ "
          "ซึ่งเกิดขึ้นประมาณเดือนละหนึ่งครั้ง"),
    Event("การมีประจำเดือน",
          "เยื่อบุมดลูกที่หนาตัวเตรียมไว้หลุดลอกออกมาพร้อมเลือด "
          "เมื่อเซลล์ไข่ไม่ได้รับการปฏิสนธิ"),
    Event("การปฏิสนธิ",
          "เซลล์อสุจิเข้าผสมกับเซลล์ไข่ที่ท่อนำไข่ ได้เป็นไซโกตซึ่งมีสารพันธุกรรม"
          "จากทั้งพ่อและแม่"),
    Event("การฝังตัว",
          "ไซโกตที่แบ่งเซลล์มาหลายครั้งเคลื่อนมาถึงมดลูกแล้วฝังตัวที่เยื่อบุมดลูก"),
    Event("การตั้งครรภ์",
          "ตัวอ่อนเจริญเติบโตอยู่ในมดลูก โดยรับอาหารและแก๊สออกซิเจนจากแม่ผ่านรก"),
    Event("การคลอด", "มดลูกบีบตัวเป็นจังหวะเพื่อดันทารกออกมาทางช่องคลอด"),
)


# What follows what, when there is a fertilisation. Stored once.
PREGNANCY_ORDER = ("การตกไข่", "การปฏิสนธิ", "การฝังตัว", "การตั้งครรภ์", "การคลอด")


@question_type(
    "body.reproductive_cycle_foundation",
    display_name={"th": "การตกไข่ ประจำเดือน การปฏิสนธิ และการตั้งครรภ์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ReproductiveCycleFoundation(QuestionType):
    """Say what happens in one named event, or name the event described."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(EVENTS)
        others = [other for other in EVENTS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return labelled(
                stem=f"“{item.name}” คือเหตุการณ์ใด",
                correct=item.description,
                wrongs=tuple(other.description for other in others[:3]),
                hint="แยกก่อนว่าเหตุการณ์นั้นเกิดที่รังไข่ ที่ท่อนำไข่ หรือที่มดลูก",
            )
        return labelled(
            stem=f"เหตุการณ์ที่ว่า {item.description} เรียกว่าอะไร",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านให้จบว่าเกิดอะไรขึ้นกับเซลล์ไข่หรือกับเยื่อบุมดลูก",
        )


@question_type(
    "body.fertilisation_fluency",
    display_name={"th": "ลำดับเหตุการณ์ตั้งแต่การตกไข่จนถึงการคลอด"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class FertilisationFluency(QuestionType):
    """Follow one released egg down both branches.

    This is the set that carries all four things ``ม.2/15`` names, because the
    branch a learner has to choose between *is* fertilisation: with it the path
    runs to birth, without it to menstruation.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        draw = rng.random()
        if draw < 0.4:
            index = rng.randrange(len(PREGNANCY_ORDER) - 1)
            current = PREGNANCY_ORDER[index]
            following = PREGNANCY_ORDER[index + 1]
            others = [event.name for event in EVENTS if event.name != following]
            rng.shuffle(others)
            return labelled(
                stem=f"เมื่อมีการปฏิสนธิเกิดขึ้น เหตุการณ์ใดเกิดต่อจาก “{current}”",
                correct=following,
                wrongs=tuple(others[:3]),
                hint="ไล่ตามเซลล์ไข่ตั้งแต่ออกจากรังไข่ ผ่านท่อนำไข่ ไปจนถึงมดลูก",
            )
        if draw < 0.7:
            swapped = list(PREGNANCY_ORDER)
            swapped[1], swapped[2] = swapped[2], swapped[1]
            return labelled(
                stem="ข้อใดเรียงลำดับเหตุการณ์ตั้งแต่การตกไข่จนถึงการคลอดได้ถูกต้อง",
                correct=" → ".join(PREGNANCY_ORDER),
                wrongs=(" → ".join(reversed(PREGNANCY_ORDER)),
                        " → ".join(swapped),
                        " → ".join(("การตกไข่", "การมีประจำเดือน", "การปฏิสนธิ",
                                    "การฝังตัว", "การคลอด"))),
                hint="การปฏิสนธิเกิดที่ท่อนำไข่ก่อนเสมอ แล้วตัวอ่อนจึงเคลื่อนไปฝังตัว"
                     "ที่มดลูก",
            )
        fertilised = rng.random() < 0.5
        if fertilised:
            return labelled(
                stem="หลังการตกไข่ ถ้าเซลล์ไข่ได้รับการปฏิสนธิ จะเกิดอะไรขึ้นต่อไป",
                correct="ไซโกตแบ่งเซลล์แล้วฝังตัวที่เยื่อบุมดลูกซึ่งหนาตัวเตรียมไว้ "
                        "และเจริญเติบโตต่อไปเป็นทารก",
                wrongs=("เยื่อบุมดลูกหลุดลอกออกมาเป็นประจำเดือนตามรอบเดิม",
                        "เซลล์ไข่ที่ปฏิสนธิแล้วเคลื่อนกลับเข้าสู่รังไข่เพื่อเจริญเติบโต",
                        "รังไข่ปล่อยเซลล์ไข่ใบใหม่ออกมาทันทีเพื่อให้ปฏิสนธิซ้ำ"),
                hint="เยื่อบุมดลูกที่หนาตัวไว้มีไว้เพื่ออะไร ให้ตอบจากตรงนั้น",
            )
        return labelled(
            stem="หลังการตกไข่ ถ้าเซลล์ไข่ไม่ได้รับการปฏิสนธิ จะเกิดอะไรขึ้นต่อไป",
            correct="เยื่อบุมดลูกที่หนาตัวเตรียมไว้จะหลุดลอกออกมาพร้อมเลือดเป็น"
                    "ประจำเดือน แล้วจึงเริ่มรอบใหม่",
            wrongs=("เซลล์ไข่จะฝังตัวที่เยื่อบุมดลูกและเจริญเติบโตต่อไปเอง",
                    "เยื่อบุมดลูกจะหนาตัวขึ้นเรื่อย ๆ จนกว่าจะมีการปฏิสนธิในรอบถัดไป",
                    "รังไข่จะหยุดทำงานจนกว่าจะมีการปฏิสนธิเกิดขึ้น"),
            hint="ถ้าไม่มีตัวอ่อนมาฝังตัว เยื่อบุที่เตรียมไว้จะเป็นอย่างไร",
        )


@question_type(
    "body.pregnancy_application",
    display_name={"th": "วิเคราะห์การปฏิสนธิและการเจริญเติบโตของทารกในครรภ์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PregnancyApplication(QuestionType):
    """Explain an observation about the cycle or the pregnancy by its mechanism."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, PREGNANCY_SCENARIOS,
            hint="ถามว่าเกิดการปฏิสนธิหรือไม่ และเหตุการณ์นั้นเกิดที่รังไข่ "
                 "ที่ท่อนำไข่ หรือที่มดลูก",
        )
