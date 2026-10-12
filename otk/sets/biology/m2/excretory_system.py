"""อวัยวะในระบบขับถ่ายและการกำจัดของเสียทางไต

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/4

Sets moved here from: science_wave_b9.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import (
    EXCRETORY_SCENARIOS,
    LEVEL,
    SUBJECT,
    TOPIC,
    labelled,
    scenario_question,
)

PROVENANCE = Provenance("original")


class ExcretoryOrgan(NamedTuple):
    """One organ of the urinary route and what it does."""
    name: str
    function: str


EXCRETORY_ORGANS = (
    ExcretoryOrgan("ไต",
                   "กรองของเสียและน้ำส่วนเกินออกจากเลือด แล้วสร้างเป็นปัสสาวะ"),
    ExcretoryOrgan("หน่วยไต",
                   "เป็นหน่วยย่อยจำนวนมากภายในไต ที่ทำหน้าที่กรองเลือด "
                   "และดูดสารที่ยังมีประโยชน์กลับคืนสู่เลือด"),
    ExcretoryOrgan("ท่อไต", "ลำเลียงปัสสาวะจากไตลงสู่กระเพาะปัสสาวะ"),
    ExcretoryOrgan("กระเพาะปัสสาวะ",
                   "เก็บสะสมปัสสาวะไว้ชั่วคราวก่อนถูกขับออกนอกร่างกาย"),
    ExcretoryOrgan("ท่อปัสสาวะ", "เป็นทางที่ปัสสาวะออกจากร่างกาย"),
    ExcretoryOrgan("หลอดเลือดที่นำเลือดเข้าสู่ไต",
                   "นำเลือดที่มีของเสียละลายอยู่มายังไตเพื่อให้ถูกกรอง"),
)


# The route urine actually takes. Stored once; the "what comes next" question
# reads it and nothing else does.
URINE_PATH = ("ไต", "ท่อไต", "กระเพาะปัสสาวะ", "ท่อปัสสาวะ")


# Real organs that are not on the urine's path, offered only as wrong next stops.
PATH_DECOYS = ("ลำไส้ใหญ่", "ท่อน้ำดี")


class Substance(NamedTuple):
    """What the kidney does with one substance in the blood it filters."""
    name: str
    fate: str


# The three fates a substance can meet at the nephron. Every wrong choice in the
# item is another substance's real fate, not an invented one.
SUBSTANCES = (
    Substance("ยูเรีย", "ถูกกรองออกจากเลือดและขับออกไปกับปัสสาวะเกือบทั้งหมด"),
    Substance("กลูโคส", "ถูกกรองออกมาแล้วถูกดูดกลับเข้าสู่เลือดจนหมดในคนปกติ"),
    Substance("โปรตีนโมเลกุลใหญ่ในเลือด",
              "มีขนาดใหญ่เกินกว่าจะผ่านการกรองได้ จึงยังคงอยู่ในเลือด"),
    Substance("น้ำ", "ถูกกรองออกมาแล้วถูกดูดกลับมากหรือน้อยตามปริมาณน้ำในร่างกาย"),
    Substance("เซลล์เม็ดเลือดแดง",
              "มีขนาดใหญ่เกินกว่าจะผ่านการกรองได้ จึงไม่พบในปัสสาวะของคนปกติ"),
)


@question_type(
    "body.excretory_organs_foundation",
    display_name={"th": "อวัยวะในระบบขับถ่ายและหน้าที่"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ExcretoryOrgansFoundation(QuestionType):
    """Name an organ's job, or the organ that does a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(EXCRETORY_ORGANS)
        others = [other for other in EXCRETORY_ORGANS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return labelled(
                stem=f"“{item.name}” ทำหน้าที่ใดในการกำจัดของเสียทางไต",
                correct=item.function,
                wrongs=tuple(other.function for other in others[:3]),
                hint="แยกก่อนว่าอวัยวะนั้นทำหน้าที่กรอง เก็บ หรือเป็นเพียงทางผ่าน",
            )
        return labelled(
            stem=f"อวัยวะใดในระบบขับถ่ายทำหน้าที่{item.function}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกอวัยวะที่ทำหน้าที่นั้นโดยตรง",
        )


@question_type(
    "body.urine_path_fluency",
    display_name={"th": "เส้นทางของปัสสาวะและการกรองที่หน่วยไต"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class UrinePathFluency(QuestionType):
    """Follow the urine out, and say what the nephron does with each substance.

    Naming organs is Foundation work. ``ม.2/4`` asks for the organs' part *in the
    removal of waste through the kidney*, and that is a sequence and a set of
    fates, not a list of names.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        draw = rng.random()
        if draw < 0.34:
            index = rng.randrange(len(URINE_PATH) - 1)
            current, following = URINE_PATH[index], URINE_PATH[index + 1]
            others = [name for name in URINE_PATH if name != following] + list(PATH_DECOYS)
            rng.shuffle(others)
            return labelled(
                stem=f"ปัสสาวะที่ผ่าน “{current}” แล้วจะผ่านอวัยวะใดต่อไป",
                correct=following,
                wrongs=tuple(others[:3]),
                hint="ไล่จากที่ที่ปัสสาวะถูกสร้างขึ้น ออกไปจนถึงภายนอกร่างกาย",
            )
        if draw < 0.5:
            correct = " → ".join(URINE_PATH)
            swapped = list(URINE_PATH)
            swapped[1], swapped[2] = swapped[2], swapped[1]
            return labelled(
                stem="ข้อใดเรียงลำดับเส้นทางของปัสสาวะได้ถูกต้อง",
                correct=correct,
                wrongs=(" → ".join(reversed(URINE_PATH)), " → ".join(swapped),
                        " → ".join(("หน่วยไต", "กระเพาะปัสสาวะ", "ท่อไต",
                                    "ท่อปัสสาวะ")),
                        " → ".join(("ไต", "ท่อปัสสาวะ", "กระเพาะปัสสาวะ", "ท่อไต")),
                        " → ".join(("กระเพาะปัสสาวะ", "ไต", "ท่อไต", "ท่อปัสสาวะ"))),
                hint="ปัสสาวะถูกสร้างที่ไตเสมอ และออกจากร่างกายเป็นขั้นสุดท้าย",
            )
        item = rng.choice(SUBSTANCES)
        others = [other.fate for other in SUBSTANCES if other.fate != item.fate]
        rng.shuffle(others)
        return labelled(
            stem=f"ที่หน่วยไตของคนปกติ “{item.name}” ในเลือดจะเป็นอย่างไร",
            correct=item.fate,
            wrongs=tuple(others[:3]),
            hint="ถามสองข้อตามลำดับ สารนั้นผ่านการกรองได้หรือไม่ "
                 "และถ้าผ่านได้ ร่างกายยังต้องการมันอยู่หรือไม่",
        )


@question_type(
    "body.excretory_application",
    display_name={"th": "วิเคราะห์การทำงานของไตจากผลตรวจและสถานการณ์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ExcretoryApplication(QuestionType):
    """Read a urine result or a change in fluid balance back to the nephron."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, EXCRETORY_SCENARIOS,
            hint="เริ่มที่หน่วยไตเสมอ ถามว่าสารนั้นถูกกรองออกมาหรือไม่ "
                 "และถูกดูดกลับมากน้อยเพียงใด",
        )
