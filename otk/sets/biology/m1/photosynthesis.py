"""ปัจจัยและผลผลิตของการสังเคราะห์ด้วยแสง

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/6

Sets moved here from: science_wave_b3.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import contextual_scenario_question
from otk.sets._support.science_wave_b3 import (
    LEVEL,
    PHOTOSYNTHESIS_SCENARIOS,
    SUBJECT,
    TOPIC,
    _labelled,
)

PROVENANCE = Provenance("original")


# What photosynthesis needs, and what it makes. Kept as two short lists because
# every question below is "is this one of these" in one direction or the other.
FACTORS = (
    "แสง",
    "คลอโรฟิลล์",
    "น้ำ",
    "แก๊สคาร์บอนไดออกไซด์",
)


PRODUCTS = (
    "น้ำตาลกลูโคส",
    "แก๊สออกซิเจน",
)


# Things a learner may reasonably think are involved but are not a factor and not
# a product. Every one is a real thing a plant deals with, so eliminating it takes
# knowing the process rather than spotting the odd word out.
NEITHER = (
    "แก๊สไนโตรเจนในอากาศ",
    "ธาตุอาหารไนโตรเจนในดิน",
    "แรงโน้มถ่วง",
    "อุณหภูมิที่ต่ำกว่าจุดเยือกแข็ง",
    "ความมืดในเวลากลางคืน",
    "จุลินทรีย์ในดิน",
)


class Experiment(NamedTuple):
    """One classroom setup: what it changes, and what the test then shows."""
    setup: str
    factor: str
    result: str


# The setups ``ม.1/6`` is taught with. Each one removes exactly one factor and
# leaves the rest alone, which is what makes the result attributable.
EXPERIMENTS = (
    Experiment("นำใบด่างที่มีทั้งส่วนสีเขียวและส่วนสีขาวไปทดสอบด้วยสารละลายไอโอดีน "
               "หลังจากพืชได้รับแสงมาทั้งวัน",
               "คลอโรฟิลล์",
               "เฉพาะส่วนสีเขียวเปลี่ยนเป็นสีน้ำเงินเข้ม ส่วนสีขาวไม่เปลี่ยนสี"),
    Experiment("ปิดส่วนหนึ่งของใบด้วยกระดาษทึบแสงไว้ทั้งวัน แล้วนำใบทั้งใบไปทดสอบ"
               "ด้วยสารละลายไอโอดีน",
               "แสง",
               "เฉพาะส่วนที่ไม่ได้ถูกปิดเปลี่ยนเป็นสีน้ำเงินเข้ม ส่วนที่ถูกปิดไม่เปลี่ยนสี"),
    Experiment("ครอบพืชทั้งต้นไว้ในโหลแก้วที่มีโซเดียมไฮดรอกไซด์ ซึ่งดูดแก๊ส"
               "คาร์บอนไดออกไซด์ไว้ แล้วให้แสงตามปกติหนึ่งวัน",
               "แก๊สคาร์บอนไดออกไซด์",
               "ใบไม่เปลี่ยนเป็นสีน้ำเงินเข้มเมื่อทดสอบด้วยสารละลายไอโอดีน"),
    Experiment("นำสาหร่ายหางกระรอกใส่ในบีกเกอร์น้ำแล้ววางไว้กลางแดด "
               "พร้อมครอบกรวยและหลอดทดลองไว้เหนือสาหร่าย",
               "แสง",
               "มีฟองแก๊สลอยขึ้นไปสะสมในหลอดทดลอง และก้านธูปที่คุแดงลุกเป็นเปลวไฟ"
               "เมื่อจ่อที่ปากหลอด"),
)


# Results no setup here gives, offered only as wrong expectations.
RESULT_DECOYS = (
    "ใบทั้งใบเปลี่ยนเป็นสีน้ำเงินเข้มเท่ากันทุกส่วน",
    "ใบเปลี่ยนเป็นสีแดงเมื่อทดสอบด้วยสารละลายไอโอดีน",
    "มีฟองแก๊สลอยขึ้น แต่ก้านธูปที่คุแดงดับทันทีเมื่อจ่อที่ปากหลอด",
)


@question_type(
    "plant.photosynthesis_foundation",
    display_name={"th": "ปัจจัยและผลผลิตของการสังเคราะห์ด้วยแสง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PhotosynthesisFoundation(QuestionType):
    """Which things go in, and which come out.

    Asked as one-of-four rather than as a three-way sort into ปัจจัย, ผลผลิต and
    neither: that sort offers one choice per category, and three categories give
    three choices. Here each question keeps four.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        if which == 0:
            # A factor among things that are not factors — including the two
            # products, which is the confusion worth catching.
            others = list(PRODUCTS + NEITHER)
            rng.shuffle(others)
            return _labelled(
                stem="ข้อใดเป็นปัจจัยที่จำเป็นต่อการสังเคราะห์ด้วยแสงของพืช",
                correct=rng.choice(FACTORS),
                wrongs=tuple(others[:3]),
                hint="ปัจจัยคือสิ่งที่พืชต้องได้รับเข้าไปจึงจะสังเคราะห์ด้วยแสงได้ "
                     "ไม่ใช่สิ่งที่ได้ออกมา",
            )
        if which == 1:
            others = list(FACTORS + NEITHER)
            rng.shuffle(others)
            return _labelled(
                stem="ข้อใดเป็นผลผลิตที่ได้จากการสังเคราะห์ด้วยแสงของพืช",
                correct=rng.choice(PRODUCTS),
                wrongs=tuple(others[:3]),
                hint="ผลผลิตคือสิ่งที่เกิดขึ้นใหม่หลังกระบวนการ ไม่ใช่สิ่งที่พืชใช้ไป",
            )
        others = list(FACTORS + PRODUCTS)
        rng.shuffle(others)
        return _labelled(
            stem="ข้อใดไม่ใช่ทั้งปัจจัยและผลผลิตของการสังเคราะห์ด้วยแสง",
            correct=rng.choice(NEITHER),
            wrongs=tuple(others[:3]),
            hint="ไล่ทีละข้อว่าเป็นสิ่งที่พืชรับเข้าไปในกระบวนการ หรือเป็นสิ่งที่ได้ออกมา",
        )


@question_type(
    "plant.photosynthesis_fluency",
    display_name={"th": "อ่านผลการทดลองเรื่องการสังเคราะห์ด้วยแสง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PhotosynthesisFluency(QuestionType):
    """Say which factor a setup tests, and what its result should be.

    ``โดยใช้หลักฐานเชิงประจักษ์`` is in the indicator, so the evidence is the
    object here: the same four setups are read in both directions, from setup to
    factor and from setup to expected result.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(EXPERIMENTS)
        if rng.random() < 0.5:
            # "ความมืด" is left out: for a covered leaf it reads as the factor itself.
            others = [name for name in FACTORS if name != item.factor] + [
                name for name in NEITHER if name != "ความมืดในเวลากลางคืน"]
            rng.shuffle(others)
            return _labelled(
                stem=f"{item.setup} การทดลองนี้ตรวจสอบปัจจัยใดของการสังเคราะห์ด้วยแสง",
                correct=item.factor,
                wrongs=tuple(others[:3]),
                hint="หาว่าการทดลองนี้ตัดสิ่งใดออกไปจากพืช สิ่งนั้นคือปัจจัยที่กำลังตรวจสอบ",
            )
        others = [other.result for other in EXPERIMENTS if other.result != item.result]
        others += list(RESULT_DECOYS)
        rng.shuffle(others)
        return _labelled(
            stem=f"{item.setup} ผลการทดลองที่คาดว่าจะเกิดขึ้นคือข้อใด",
            correct=item.result,
            wrongs=tuple(others[:3]),
            hint="สารละลายไอโอดีนเปลี่ยนเป็นสีน้ำเงินเข้มเมื่อพบแป้ง "
                 "ซึ่งเกิดจากน้ำตาลที่พืชสร้างขึ้น",
        )


@question_type(
    "plant.photosynthesis_application",
    display_name={"th": "ออกแบบและตีความการทดลองเรื่องการสังเคราะห์ด้วยแสง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PhotosynthesisApplication(QuestionType):
    """Judge a control, a conflicting result, or a proposed design.

    Reading one setup is Fluency work. Here the learner has to say why a control
    step exists, which variable a plan fails to hold constant, or which of two
    conflicting results is explainable — the reasoning ``หลักฐานเชิงประจักษ์``
    actually calls for.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, PHOTOSYNTHESIS_SCENARIOS,
            hint="ถามว่าการทดลองเปลี่ยนตัวแปรใดและคุมตัวแปรใดไว้ "
                 "ข้อสรุปจะเชื่อได้ก็ต่อเมื่อเปลี่ยนเพียงตัวแปรเดียว",
            topic=TOPIC,
        )
