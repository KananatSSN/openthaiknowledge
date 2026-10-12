"""สารอาหารที่พืชสังเคราะห์ได้

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/8

Sets moved here from: science_wave_b21.
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
from otk.sets._support.science_wave_b19 import UPPER_FOUR
from otk.sets._support.science_wave_b21 import FOOD_TEST_SCENARIOS, PLANT_TOPIC

PROVENANCE = Provenance("original")


class Test(NamedTuple):
    """One food test: what it looks for, what is used, and the positive result."""
    substance: str
    reagent: str
    result: str


TESTS = (
    Test("แป้ง", "สารละลายไอโอดีน",
         "สีของสารละลายเปลี่ยนจากสีน้ำตาลเป็นสีน้ำเงินเข้มถึงดำ"),
    Test("น้ำตาลโมเลกุลเดี่ยว", "สารละลายเบเนดิกต์แล้วให้ความร้อน",
         "สีของสารละลายเปลี่ยนจากสีฟ้าเป็นตะกอนสีส้มถึงแดงอิฐ"),
    Test("โปรตีน", "สารละลายไบยูเรต",
         "สีของสารละลายเปลี่ยนจากสีฟ้าเป็นสีม่วง"),
    Test("ไขมัน", "การถูตัวอย่างลงบนกระดาษแล้วส่องดูกับแสง",
         "เกิดรอยโปร่งแสงบนกระดาษที่ยังคงอยู่แม้กระดาษจะแห้งแล้ว"),
    Test("วิตามินซี", "การหยดตัวอย่างลงในสารละลายไอโอดีนเจือจางทีละหยด",
         "สีของสารละลายไอโอดีนจางหายไปจนกว่าจะหยดเกินปริมาณที่ทำปฏิกิริยาได้"),
)


class Observation(NamedTuple):
    """A recorded test result on plant material, and the substance it names."""
    record: str
    substance: str


OBSERVATIONS = (
    Observation("นำใบพืชที่ได้รับแสงมาต้มในแอลกอฮอล์จนสีเขียวออกหมด "
                "แล้วหยดสารละลายไอโอดีนลงไป พบว่าใบเปลี่ยนเป็นสีน้ำเงินเข้ม",
                "แป้ง"),
    Observation("นำน้ำคั้นจากผลไม้สุกมาต้มกับสารละลายเบเนดิกต์ "
                "พบตะกอนสีแดงอิฐเกิดขึ้น",
                "น้ำตาลโมเลกุลเดี่ยว"),
    Observation("หยดสารละลายไบยูเรตลงในน้ำคั้นจากเมล็ดถั่วบด "
                "พบว่าสารละลายเปลี่ยนเป็นสีม่วง",
                "โปรตีน"),
    Observation("ถูเมล็ดงาที่บดแล้วลงบนกระดาษ แล้วทิ้งไว้จนกระดาษแห้ง "
                "พบว่ายังมีรอยโปร่งแสงอยู่บนกระดาษ",
                "ไขมัน"),
    Observation("หยดน้ำคั้นจากผลฝรั่งลงในสารละลายไอโอดีนเจือจางทีละหยด "
                "พบว่าสีของไอโอดีนจางหายไปในหยดแรก ๆ",
                "วิตามินซี"),
    Observation("นำน้ำคั้นจากหัวมันเทศมาต้มกับสารละลายเบเนดิกต์แล้วไม่เกิดตะกอน "
                "แต่เมื่อหยดสารละลายไอโอดีนกลับได้สีน้ำเงินเข้ม",
                "แป้ง"),
    Observation("หยดสารละลายไบยูเรตลงในน้ำนมถั่วเหลือง "
                "พบว่าสารละลายเปลี่ยนจากสีฟ้าเป็นสีม่วง",
                "โปรตีน"),
    Observation("ถูเนื้อมะพร้าวขูดลงบนกระดาษ แล้วทิ้งไว้จนกระดาษแห้ง "
                "พบว่ามีรอยโปร่งแสงติดอยู่บนกระดาษ",
                "ไขมัน"),
    Observation("นำน้ำคั้นจากผลองุ่นมาต้มกับสารละลายเบเนดิกต์ "
                "พบตะกอนสีส้มเกิดขึ้น",
                "น้ำตาลโมเลกุลเดี่ยว"),
    Observation("หยดน้ำมะนาวลงในสารละลายไอโอดีนเจือจางทีละหยด "
                "พบว่าสีของไอโอดีนจางหายไปอย่างรวดเร็ว",
                "วิตามินซี"),
)


@question_type(
    "plant.food_test_foundation",
    display_name={"th": "การทดสอบสารอาหารที่พืชสังเคราะห์ได้"},
    level=UPPER_FOUR, subject=SUBJECT, topic=PLANT_TOPIC,
)
class FoodTestFoundation(QuestionType):
    """Which reagent goes with which substance, and what a positive result is."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(TESTS)
        others = [other for other in TESTS if other.substance != item.substance]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"การทดสอบหา “{item.substance}” ในตัวอย่างจากพืช "
                     f"ใช้สิ่งใดและได้ผลอย่างไรเมื่อพบสารนั้น",
                correct=f"ใช้{item.reagent} แล้ว{item.result}",
                wrongs=tuple(f"ใช้{other.reagent} แล้ว{other.result}"
                             for other in others[:3]),
                hint="จำคู่ของสารทดสอบกับการเปลี่ยนสีให้ได้ "
                     "แล้วตรวจว่าทั้งสองส่วนในตัวเลือกเข้าคู่กันถูกต้อง",
                topic=PLANT_TOPIC,
            )
        return _labelled(
            stem=f"เมื่อใช้{item.reagent} กับตัวอย่างจากพืชแล้วพบว่า{item.result} "
                 f"แสดงว่าตัวอย่างนั้นมีสารใด",
            correct=item.substance,
            wrongs=tuple(other.substance for other in others[:3]),
            hint="อ่านทั้งสารทดสอบและผลที่เกิดขึ้นประกอบกัน "
                 "เพราะไอโอดีนถูกใช้ในการทดสอบมากกว่าหนึ่งอย่าง",
            topic=PLANT_TOPIC,
        )


@question_type(
    "plant.food_test_fluency",
    display_name={"th": "บอกชนิดของสารอาหารจากผลการทดสอบ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=PLANT_TOPIC,
)
class FoodTestFluency(QuestionType):
    """Name the substance a recorded result points to — ``บอกชนิด`` itself."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(OBSERVATIONS)
        others = [test.substance for test in TESTS
                  if test.substance != item.substance]
        rng.shuffle(others)
        return _labelled(
            stem=f"{item.record} ผลนี้แสดงว่าตัวอย่างมีสารอาหารชนิดใด",
            correct=item.substance, wrongs=tuple(others[:3]),
            hint="ดูให้ครบว่าใช้สารทดสอบใด และผลที่ได้เป็นผลบวกหรือผลลบ",
            topic=PLANT_TOPIC,
        )


@question_type(
    "plant.food_test_application",
    display_name={"th": "วิเคราะห์การทดสอบสารอาหารในพืช"},
    level=UPPER_FOUR, subject=SUBJECT, topic=PLANT_TOPIC,
)
class FoodTestApplication(QuestionType):
    """Say what a test design can and cannot conclude about what a plant made."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, FOOD_TEST_SCENARIOS,
            hint="ถามว่าการทดลองเปลี่ยนอะไรไปหนึ่งอย่าง "
                 "และผลการทดสอบตอบคำถามที่ตั้งไว้ได้จริงหรือไม่",
        ), PLANT_TOPIC)
