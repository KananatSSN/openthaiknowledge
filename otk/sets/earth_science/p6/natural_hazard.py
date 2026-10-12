"""ภัยธรรมชาติและธรณีพิบัติภัย

ธรณีวิทยา · ป.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.6/6

Sets moved here from: science_wave_c15.
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
from otk.sets._support.science_wave_b17 import PRIMARY_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c13 import _swapped, _swaps
from otk.sets._support.science_wave_c15 import FIVE_LETTERS, HAZARD_SCENARIOS

PROVENANCE = Provenance("original")


HAZARD_TOPIC = "ภัยธรรมชาติและธรณีพิบัติภัย"


class Hazard(NamedTuple):
    """A hazard, its character and effects together, and a sign of it alone."""
    name: str
    description: str
    sign: str


# Each description carries both halves the verb names — character and effects —
# and no two hazards share either, so a description names one hazard.
HAZARDS = (
    Hazard("น้ำท่วม",
           "น้ำเอ่อล้นท่วมพื้นที่ที่ปกติแห้งหลังฝนตกหนักต่อเนื่อง ทำให้บ้านเรือนและพื้นที่เกษตรเสียหาย และเกิดโรคที่มากับน้ำ",
           "ระดับน้ำในแม่น้ำสูงขึ้นอย่างรวดเร็วหลังฝนตกหนักหลายวัน"),
    Hazard("การกัดเซาะชายฝั่ง",
           "คลื่นและกระแสน้ำพัดพาดินและทรายตามแนวชายฝั่งออกไปทีละน้อย ทำให้ชายฝั่งร่นถอยและบ้านเรือนริมทะเลพังเสียหาย",
           "แนวชายหาดแคบลงทุกปีจนต้นไม้ริมหาดโค่นลงทะเล"),
    Hazard("ดินถล่ม",
           "ดินและหินบนที่ลาดชันเคลื่อนที่ลงมาอย่างรวดเร็วเมื่อดินอุ้มน้ำฝนไว้มากเกินไป ทำให้บ้านถูกทับและถนนถูกตัดขาด",
           "น้ำในลำห้วยขุ่นข้นผิดปกติและมีเสียงดังจากภูเขาขณะฝนตกหนัก"),
    Hazard("แผ่นดินไหว",
           "พื้นดินสั่นสะเทือนเพราะแผ่นธรณีหรือรอยเลื่อนเคลื่อนที่ ทำให้อาคารร้าวหรือถล่มลงมา",
           "สิ่งของในบ้านสั่นไหวและตกจากชั้นพร้อมกันทั้งที่ไม่มีลมพัด"),
    Hazard("สึนามิ",
           "คลื่นขนาดใหญ่ที่เกิดจากแผ่นดินไหวใต้ทะเลเคลื่อนเข้าหาฝั่งอย่างรวดเร็ว ทำให้ชายฝั่งถูกกวาดทำลายและมีผู้เสียชีวิตจำนวนมาก",
           "น้ำทะเลลดลงอย่างรวดเร็วผิดปกติหลังเกิดแผ่นดินไหว"),
)


def _match_hazards(letters: list[str]) -> str:
    return " / ".join(f"{hazard.name} → {letter}" for hazard, letter in zip(HAZARDS, letters))


@question_type(
    "geo.natural_hazard_foundation",
    display_name={"th": "ลักษณะของภัยธรรมชาติแต่ละชนิด"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=HAZARD_TOPIC,
)
class NaturalHazardFoundation(QuestionType):
    """One hazard at a time: its description, or the sign that it is coming."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hazard = rng.choice(HAZARDS)
        others = [other for other in HAZARDS if other.name != hazard.name]
        rng.shuffle(others)
        draw = rng.random()
        if draw < 0.35:
            return _labelled(
                stem=f"ข้อใดบรรยายลักษณะและผลกระทบของ{hazard.name}ได้ถูกต้อง",
                correct=hazard.description,
                wrongs=tuple(other.description for other in others[:3]),
                hint="นึกว่าภัยนั้นเกิดจากน้ำ ดิน คลื่น หรือการสั่นของพื้นดิน",
                topic=HAZARD_TOPIC,
            )
        if draw < 0.7:
            return _labelled(
                stem=f"เหตุการณ์ “{hazard.sign}” เป็นสัญญาณของภัยใด",
                correct=hazard.name,
                wrongs=tuple(other.name for other in others[:3]),
                hint="นึกว่าสิ่งที่สังเกตได้เกี่ยวกับน้ำฝน ทะเล ภูเขา หรือการสั่นของพื้นดิน",
                topic=HAZARD_TOPIC,
            )
        return _labelled(
            stem=f"ภัยที่{hazard.description} คือภัยใด",
            correct=hazard.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="นึกว่าภัยนั้นเกิดจากน้ำ ดิน คลื่น หรือการสั่นของพื้นดิน",
            topic=HAZARD_TOPIC,
        )


@question_type(
    "geo.natural_hazard_fluency",
    display_name={"th": "บรรยายลักษณะและผลกระทบของภัยธรรมชาติทั้งห้า"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=HAZARD_TOPIC,
)
class NaturalHazardFluency(QuestionType):
    """Place all five hazards against their descriptions; each wrong choice swaps two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shuffled = list(HAZARDS)
        rng.shuffle(shuffled)
        listing = " / ".join(f"{letter}. {hazard.description}"
                             for letter, hazard in zip(FIVE_LETTERS, shuffled))
        letter_of = {hazard.name: FIVE_LETTERS[i] for i, hazard in enumerate(shuffled)}
        right = [letter_of[hazard.name] for hazard in HAZARDS]
        return _labelled(
            stem=f"ข้อความบรรยายลักษณะและผลกระทบของภัย 5 ชนิด — {listing} "
                 "ข้อใดจับคู่น้ำท่วม การกัดเซาะชายฝั่ง ดินถล่ม แผ่นดินไหว และสึนามิ กับข้อความได้ถูกต้องทั้งหมด",
            correct=_match_hazards(right),
            wrongs=tuple(_match_hazards(_swapped(right, i, j)) for i, j in _swaps(rng, 3, 5)),
            hint="จับคู่ภัยที่มั่นใจที่สุดก่อน แล้วตัดตัวเลือกที่ขัดแย้งออก",
            topic=HAZARD_TOPIC,
        )


@question_type(
    "geo.natural_hazard_application",
    display_name={"th": "วิเคราะห์สาเหตุและผลของภัยธรรมชาติ"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=HAZARD_TOPIC,
)
class NaturalHazardApplication(QuestionType):
    """Why mangroves help, why cleared slopes slide, and a sea that pulls back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, HAZARD_SCENARIOS,
            hint="นึกว่าภัยนั้นเกิดจากอะไร แล้วสิ่งใดทำให้รุนแรงขึ้นหรือลดลง",
        ), HAZARD_TOPIC)
