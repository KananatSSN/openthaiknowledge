"""สิ่งที่พืชต้องการเพื่อการเจริญเติบโต

ชีวะ · ป.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.2/1

Sets moved here from: science_wave_b14.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import (
    PLANT_GROWTH_SCENARIOS,
    PLANT_TOPIC,
    PRIMARY_TWO,
    _labelled,
)

PROVENANCE = Provenance("original")


class Trial(NamedTuple):
    """One two-pot comparison, and what its result shows."""
    setup: str
    result: str
    conclusion: str


# Every trial changes one thing only. That is what makes each conclusion the one
# thing the trial can show, and it is the point ป.2/1 is really about.
TRIALS = (
    Trial("ปลูกต้นถั่วสองต้นในดินเหมือนกันและวางไว้ริมหน้าต่างที่มีแสงทั้งคู่ "
          "ต้นที่หนึ่งรดน้ำทุกวัน ต้นที่สองไม่รดน้ำเลย",
          "ผ่านไปหนึ่งสัปดาห์ ต้นที่หนึ่งเขียวและสูงขึ้น ส่วนต้นที่สองเหี่ยวและใบแห้ง",
          "พืชต้องการน้ำเพื่อการเจริญเติบโต"),
    Trial("ปลูกต้นถั่วสองต้นในดินเหมือนกันและรดน้ำเท่ากันทั้งคู่ "
          "ต้นที่หนึ่งวางไว้ริมหน้าต่างที่มีแสง ต้นที่สองวางไว้ในตู้ที่ปิดมืดสนิท",
          "ผ่านไปหนึ่งสัปดาห์ ต้นที่หนึ่งเขียวและแข็งแรง ส่วนต้นที่สองใบซีดและต้นอ่อนแอ",
          "พืชต้องการแสงเพื่อการเจริญเติบโต"),
    Trial("ปลูกต้นถั่วสองต้นในดินเหมือนกัน ต้นที่หนึ่งได้ทั้งน้ำและแสง "
          "ต้นที่สองไม่ได้ทั้งน้ำและแสง",
          "ผ่านไปหนึ่งสัปดาห์ ต้นที่หนึ่งเจริญเติบโตตามปกติ ส่วนต้นที่สองเหี่ยวแห้งและตาย",
          "การทดลองนี้บอกไม่ได้ว่าน้ำหรือแสงเป็นสาเหตุ เพราะเปลี่ยนสองอย่างพร้อมกัน"),
    Trial("ปลูกต้นถั่วสองต้นในดินเหมือนกัน รดน้ำเท่ากัน และวางไว้ที่มีแสงเท่ากัน "
          "ต่างกันเพียงใช้กระถางคนละสี",
          "ผ่านไปหนึ่งสัปดาห์ ต้นทั้งสองเจริญเติบโตได้พอ ๆ กัน",
          "สีของกระถางไม่มีผลต่อการเจริญเติบโตของพืช"),
    Trial("ปลูกต้นถั่วสองต้นในดินเหมือนกันและวางไว้ที่มีแสงทั้งคู่ "
          "ต้นที่หนึ่งรดน้ำวันละเล็กน้อยพอชุ่ม ต้นที่สองรดน้ำจนท่วมขังทุกวัน",
          "ผ่านไปหนึ่งสัปดาห์ ต้นที่หนึ่งเจริญเติบโตดี ส่วนต้นที่สองใบเหลืองและรากเน่า",
          "พืชต้องการน้ำในปริมาณที่พอเหมาะ ไม่ใช่ยิ่งมากยิ่งดี"),
    Trial("นำต้นถั่วที่ปลูกในที่มืดจนใบซีดมาวางไว้ริมหน้าต่างที่มีแสง "
          "และรดน้ำตามปกติ",
          "ผ่านไปหนึ่งสัปดาห์ ใบของต้นถั่วกลับมาเขียวขึ้นและต้นแข็งแรงขึ้น",
          "เมื่อพืชได้รับแสงอีกครั้ง ก็กลับมาเจริญเติบโตได้ตามปกติ"),
)


NEEDS_OF_PLANTS = (
    ("น้ำ", "พืชใช้น้ำในการเจริญเติบโต และดูดน้ำขึ้นมาจากดินทางราก"),
    ("แสง", "พืชใช้แสงในการสร้างอาหารที่ใบ ถ้าไม่มีแสงพืชก็สร้างอาหารไม่ได้"),
    ("อากาศ", "พืชใช้อากาศในการหายใจเช่นเดียวกับสิ่งมีชีวิตอื่น"),
    ("ดิน", "ดินเป็นที่ยึดรากของพืชไว้ และเป็นที่ที่พืชดูดน้ำขึ้นไปใช้"),
)


# Things a plant does not need and jobs it does not do, offered only as wrong choices.
NEED_DECOYS = ("ความมืดตลอดวัน", "น้ำหวาน")


REASON_DECOYS = ("พืชใช้สิ่งนี้ในการเดินไปหาอาหาร", "พืชใช้สิ่งนี้ในการมองหาแมลงที่มาเกาะ")


@question_type(
    "plant.growth_needs_foundation",
    display_name={"th": "สิ่งที่พืชต้องการเพื่อการเจริญเติบโต"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantGrowthNeedsFoundation(QuestionType):
    """Name what a plant needs, and what it needs it for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, reason = rng.choice(NEEDS_OF_PLANTS)
        others = [item for item in NEEDS_OF_PLANTS if item[0] != name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"พืชต้องการ “{name}” ไปเพื่ออะไร",
                correct=reason,
                wrongs=tuple(other[1] for other in others) + REASON_DECOYS,
                hint="นึกว่าส่วนใดของพืชใช้สิ่งนั้น และใช้ทำอะไร",
                topic=PLANT_TOPIC,
            )
        return _labelled(
            stem=f"ข้อความที่ว่า {reason} กล่าวถึงสิ่งใดที่พืชต้องการ",
            correct=name,
            wrongs=tuple(other[0] for other in others) + NEED_DECOYS,
            hint="อ่านให้จบว่าพืชเอาสิ่งนั้นไปทำอะไร",
            topic=PLANT_TOPIC,
        )


@question_type(
    "plant.growth_evidence_fluency",
    display_name={"th": "อ่านผลการทดลองการเจริญเติบโตของพืช"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantGrowthEvidenceFluency(QuestionType):
    """Say what one comparison shows — and where it shows nothing.

    ``ป.2/1`` says ``โดยใช้ข้อมูลจากหลักฐานเชิงประจักษ์``. The item gives the
    evidence and asks what it shows, including the trial that changes two things
    at once and therefore shows nothing about either.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(TRIALS)
        others = [other.conclusion for other in TRIALS
                  if other.conclusion != item.conclusion]
        rng.shuffle(others)
        return _labelled(
            stem=f"{item.setup} {item.result} ผลการทดลองนี้แสดงว่าอะไร",
            correct=item.conclusion,
            wrongs=tuple(others[:3]),
            hint="ดูก่อนว่าการทดลองนี้เปลี่ยนกี่อย่าง ถ้าเปลี่ยนมากกว่าหนึ่งอย่าง "
                 "ก็บอกไม่ได้ว่าอย่างไหนเป็นสาเหตุ",
            topic=PLANT_TOPIC,
        )


@question_type(
    "plant.growth_application",
    display_name={"th": "ใช้ความรู้เรื่องสิ่งที่พืชต้องการ"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantGrowthApplication(QuestionType):
    """Plan a fair comparison, or explain a plant that is not thriving."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        question = scenario_question(
            rng, PLANT_GROWTH_SCENARIOS,
            hint="ถามว่าการเปรียบเทียบนี้ต่างกันเพียงอย่างเดียวหรือไม่ "
                 "และพืชต้นนั้นขาดน้ำหรือขาดแสง",
        )
        return GeneratedQuestion(
            stem=question.stem, correct=question.correct,
            distractors=question.distractors, topic=PLANT_TOPIC, hint=question.hint,
        )
