"""ดุลยภาพของกรด-เบสของเลือด

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/3

Sets moved here from: science_wave_b19.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import (
    ACID_BASE_SCENARIOS,
    BALANCE_TOPIC,
    UPPER_FOUR,
    Fact,
    _fact_question,
)

PROVENANCE = Provenance("original")


# The indicator names both ไต and ปอด, so this table covers both and the draw
# spans them; no set here asks about one organ alone.
ACID_BASE_FACTS = (
    Fact("ค่า pH ของเลือดคนปกติอยู่ในช่วงใด",
         "ประมาณ 7.35 ถึง 7.45 ซึ่งเป็นเบสอ่อน ๆ และเปลี่ยนแปลงได้น้อยมาก"),
    Fact("ปอดมีบทบาทอย่างไรในการควบคุมดุลยภาพกรด-เบสของเลือด",
         "ปรับอัตราการหายใจเพื่อควบคุมปริมาณคาร์บอนไดออกไซด์ในเลือด "
         "ซึ่งรวมกับน้ำได้เป็นกรดคาร์บอนิก"),
    Fact("ไตมีบทบาทอย่างไรในการควบคุมดุลยภาพกรด-เบสของเลือด",
         "ขับไฮโดรเจนไอออนออกไปกับปัสสาวะ "
         "และดูดไฮโดรเจนคาร์บอเนตไอออนกลับเข้าสู่เลือด"),
    Fact("เมื่อเลือดมีความเป็นกรดมากขึ้น ปอดตอบสนองอย่างไร",
         "หายใจเร็วและลึกขึ้นเพื่อขับคาร์บอนไดออกไซด์ออกให้มากขึ้น "
         "กรดคาร์บอนิกในเลือดจึงลดลง"),
    Fact("เมื่อเลือดมีความเป็นกรดมากขึ้น ไตตอบสนองอย่างไร",
         "ขับไฮโดรเจนไอออนออกทางปัสสาวะมากขึ้น "
         "และดูดไฮโดรเจนคาร์บอเนตไอออนกลับเข้าสู่เลือดมากขึ้น"),
    Fact("การควบคุมกรด-เบสโดยปอดกับโดยไตต่างกันอย่างไรในด้านเวลา",
         "ปอดปรับได้ภายในไม่กี่นาทีแต่ปรับได้เพียงส่วนของคาร์บอนไดออกไซด์ "
         "ส่วนไตใช้เวลาเป็นชั่วโมงถึงเป็นวันแต่ปรับได้ละเอียดกว่าและอยู่ได้นานกว่า"),
    Fact("ระบบบัฟเฟอร์ไฮโดรเจนคาร์บอเนตในเลือดทำงานร่วมกับอวัยวะใดบ้าง",
         "ทำงานร่วมกับปอดซึ่งควบคุมคาร์บอนไดออกไซด์ "
         "และไตซึ่งควบคุมไฮโดรเจนคาร์บอเนตไอออนกับไฮโดรเจนไอออน"),
)


class Disturbance(NamedTuple):
    """A challenge to blood pH, and how lungs and kidneys answer it together."""
    situation: str
    response: str


DISTURBANCES = (
    Disturbance("ออกกำลังกายอย่างหนักจนกล้ามเนื้อสร้างกรดแลกติกและ"
                "คาร์บอนไดออกไซด์มากขึ้น",
                "เลือดมีความเป็นกรดมากขึ้น ปอดจึงหายใจเร็วและลึกขึ้นเพื่อขับ"
                "คาร์บอนไดออกไซด์ออก และไตค่อย ๆ ขับไฮโดรเจนไอออนออกเพิ่มขึ้น"),
    Disturbance("หายใจเร็วและลึกติดต่อกันนานทั้งที่ไม่ได้ออกกำลังกาย",
                "คาร์บอนไดออกไซด์ในเลือดลดลงมาก เลือดจึงเป็นเบสมากขึ้น "
                "ร่างกายลดอัตราการหายใจลง และไตขับไฮโดรเจนคาร์บอเนตไอออน"
                "ออกทางปัสสาวะมากขึ้น"),
    Disturbance("ผู้ป่วยถุงลมโป่งพองระบายคาร์บอนไดออกไซด์ออกได้ไม่ดีเป็นเวลานาน",
                "คาร์บอนไดออกไซด์คั่งทำให้เลือดเป็นกรด เมื่อปอดชดเชยไม่ได้ "
                "ไตจึงดูดไฮโดรเจนคาร์บอเนตไอออนกลับมากขึ้นและขับไฮโดรเจนไอออน"
                "ออกมากขึ้นเพื่อชดเชยแทน"),
    Disturbance("ผู้ป่วยไตวายขับไฮโดรเจนไอออนออกทางปัสสาวะได้น้อยลง",
                "ไฮโดรเจนไอออนคั่งทำให้เลือดเป็นกรด ปอดจึงหายใจเร็วและลึกขึ้น"
                "เพื่อขับคาร์บอนไดออกไซด์ออกไปชดเชย แต่ชดเชยได้เพียงบางส่วน"),
    Disturbance("อาเจียนอย่างรุนแรงจนสูญเสียกรดในกระเพาะอาหารไปมาก",
                "เลือดเป็นเบสมากขึ้น ร่างกายจึงลดอัตราการหายใจลงเพื่อเก็บ"
                "คาร์บอนไดออกไซด์ไว้ และไตขับไฮโดรเจนคาร์บอเนตไอออนออกมากขึ้น"),
    Disturbance("กลั้นหายใจไว้นานที่สุดเท่าที่ทำได้",
                "คาร์บอนไดออกไซด์สะสมจนเลือดเป็นกรดมากขึ้น "
                "ศูนย์ควบคุมการหายใจจึงสั่งให้หายใจออกแรงและเร็วขึ้นทันทีที่ทำได้"),
)


@question_type(
    "body.acid_base_foundation",
    display_name={"th": "บทบาทของไตและปอดต่อกรด-เบสของเลือด"},
    level=UPPER_FOUR, subject=SUBJECT, topic=BALANCE_TOPIC,
)
class AcidBaseFoundation(QuestionType):
    """What each of the two organs contributes to holding blood pH steady."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, ACID_BASE_FACTS, topic=BALANCE_TOPIC,
            hint="จำไว้ว่าปอดจัดการกับคาร์บอนไดออกไซด์ "
                 "ส่วนไตจัดการกับไฮโดรเจนไอออนและไฮโดรเจนคาร์บอเนตไอออน",
        )


@question_type(
    "body.acid_base_fluency",
    display_name={"th": "การชดเชยกรด-เบสของเลือดโดยไตและปอด"},
    level=UPPER_FOUR, subject=SUBJECT, topic=BALANCE_TOPIC,
)
class AcidBaseFluency(QuestionType):
    """Say how the two organs answer a given challenge to blood pH."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DISTURBANCES)
        others = [other.response for other in DISTURBANCES
                  if other.response != item.response]
        rng.shuffle(others)
        return _labelled(
            stem=f"เมื่อ{item.situation} ร่างกายจะรักษาดุลยภาพกรด-เบสของเลือด"
                 f"ไว้ได้อย่างไร",
            correct=item.response, wrongs=tuple(others[:3]),
            hint="ตัดสินก่อนว่าเลือดกำลังเป็นกรดขึ้นหรือเป็นเบสขึ้น "
                 "แล้วจึงดูว่าปอดกับไตต้องทำสิ่งใดเพื่อดึงกลับ",
            topic=BALANCE_TOPIC,
        )


@question_type(
    "body.acid_base_application",
    display_name={"th": "วิเคราะห์ภาวะเสียดุลยภาพกรด-เบสของเลือด"},
    level=UPPER_FOUR, subject=SUBJECT, topic=BALANCE_TOPIC,
)
class AcidBaseApplication(QuestionType):
    """Trace a disturbed blood pH back to the organ that failed or compensated."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ACID_BASE_SCENARIOS,
            hint="แยกให้ออกว่าอะไรคือสาเหตุและอะไรคือการชดเชย "
                 "โดยดูว่าปอดหรือไตเป็นฝ่ายที่ทำงานผิดปกติ",
        ), BALANCE_TOPIC)
