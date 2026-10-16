"""หน้าที่ของราก ลำต้น ใบ และดอก

ชีวะ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.4/1

Sets moved here from: science_wave_b17.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, labelled, scenario_question
from otk.sets._support.science_wave_b14 import PLANT_TOPIC
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import PLANT_ORGAN_SCENARIOS, PRIMARY_FOUR
from otk.sets._support.life_earth_diagrams import PLANT_ALT, PLANT_ORGANS, PLANT_PICTURES
from otk.sets._support.ms1_diagrams import diagram_question

PROVENANCE = Provenance("original")


def _plant(*, stem, correct, wrongs, hint):
    return _retopic(labelled(stem=stem, correct=correct, wrongs=wrongs, hint=hint),
                    PLANT_TOPIC)


class Organ(NamedTuple):
    """One organ of a flowering plant: its job, and what fails without it."""
    name: str
    function: str
    without: str


# Exactly the four organs the indicator names, so "which organ" offers all four.
ORGANS = (
    Organ("ราก",
          "ดูดน้ำและแร่ธาตุจากดิน และยึดลำต้นไว้ไม่ให้ล้ม",
          "ต้นพืชจะไม่ได้รับน้ำจากดินและล้มได้ง่ายเมื่อมีลมแรง"),
    Organ("ลำต้น",
          "ลำเลียงน้ำและอาหารไปยังส่วนต่าง ๆ และชูกิ่ง ใบ และดอกขึ้นรับแสง",
          "น้ำจากรากจะขึ้นไปถึงใบไม่ได้ และใบก็อยู่ต่ำจนได้รับแสงน้อยลง"),
    Organ("ใบ",
          "สร้างอาหารให้แก่ต้นพืชโดยใช้แสง และเป็นที่คายน้ำออกสู่อากาศ",
          "ต้นพืชจะสร้างอาหารเองไม่ได้ และต้องใช้อาหารที่สะสมไว้จนหมด"),
    Organ("ดอก",
          "เป็นส่วนที่ใช้สืบพันธุ์ จนเกิดเป็นผลและเมล็ดต่อไป",
          "ต้นพืชจะไม่เกิดผลและเมล็ด จึงไม่มีต้นใหม่ในรุ่นถัดไป"),
)


# Each organ's job in more than one wording, and more than one sign of its loss.
# Every line still belongs to one organ only, so a question never has two answers.
ORGAN_JOBS = {
    "ราก": ("ดูดน้ำและแร่ธาตุจากดิน และยึดลำต้นไว้ไม่ให้ล้ม",
            "ดูดน้ำและแร่ธาตุที่อยู่ในดินเข้าสู่ต้นพืช",
            "ยึดต้นพืชไว้กับดินไม่ให้โค่นล้ม"),
    "ลำต้น": ("ลำเลียงน้ำและอาหารไปยังส่วนต่าง ๆ และชูกิ่ง ใบ และดอกขึ้นรับแสง",
              "เป็นทางลำเลียงน้ำจากรากขึ้นไปสู่ใบ",
              "ค้ำชูกิ่งและใบให้ตั้งขึ้นไปรับแสง"),
    "ใบ": ("สร้างอาหารให้แก่ต้นพืชโดยใช้แสง และเป็นที่คายน้ำออกสู่อากาศ",
           "สร้างอาหารให้แก่ต้นพืชโดยใช้แสง น้ำ และแก๊สคาร์บอนไดออกไซด์",
           "คายน้ำออกสู่อากาศในรูปของไอน้ำ"),
    "ดอก": ("เป็นส่วนที่ใช้สืบพันธุ์ จนเกิดเป็นผลและเมล็ดต่อไป",
            "สืบพันธุ์เพื่อสร้างผลและเมล็ดสำหรับต้นรุ่นต่อไป",
            "มีสีและกลิ่นล่อแมลงให้มาช่วยผสมเกสร"),
}


ORGAN_FAILURES = {
    "ราก": ("ต้นพืชจะไม่ได้รับน้ำจากดินและล้มได้ง่ายเมื่อมีลมแรง",
            "ต้นพืชเหี่ยวเฉา แม้จะรดน้ำลงในดินจนชุ่มแล้ว",
            "ต้นพืชโยกคลอนและล้มลงง่ายเมื่อมีลมพัด"),
    "ลำต้น": ("น้ำจากรากจะขึ้นไปถึงใบไม่ได้ และใบก็อยู่ต่ำจนได้รับแสงน้อยลง",
              "น้ำที่รากดูดไว้ส่งขึ้นไปไม่ถึงใบ ใบด้านบนจึงเหี่ยว",
              "กิ่งและใบทรุดลงต่ำ ถูกต้นอื่นบังแสงจนได้แสงน้อย"),
    "ใบ": ("ต้นพืชจะสร้างอาหารเองไม่ได้ และต้องใช้อาหารที่สะสมไว้จนหมด",
           "ต้นพืชสร้างอาหารจากแสงไม่ได้ จึงค่อย ๆ ผอมลงแม้ได้แสงเต็มที่",
           "ต้นพืชไม่มีส่วนที่รับแสงมาสร้างอาหาร จึงเติบโตต่อไปไม่ได้"),
    "ดอก": ("ต้นพืชจะไม่เกิดผลและเมล็ด จึงไม่มีต้นใหม่ในรุ่นถัดไป",
            "ต้นพืชยังเขียวดีแต่ไม่ติดผลเลยตลอดฤดู",
            "ต้นพืชไม่มีเมล็ดไว้ให้งอกเป็นต้นใหม่"),
}


@question_type(
    "plant.organ_function_foundation",
    display_name={"th": "หน้าที่ของราก ลำต้น ใบ และดอก"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantOrganFunctionFoundation(QuestionType):
    """Name an organ's job, or the organ that does a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ORGANS)
        others = [other for other in ORGANS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _plant(
                stem=f"“{item.name}” ของพืชดอกทำหน้าที่ใด",
                correct=rng.choice(ORGAN_JOBS[item.name]),
                wrongs=tuple(rng.choice(ORGAN_JOBS[other.name]) for other in others[:3]),
                hint="แยกว่าอวัยวะนั้นดูดน้ำ ลำเลียง สร้างอาหาร หรือใช้สืบพันธุ์",
            )
        return _plant(
            stem=f"ส่วนใดของพืชดอกทำหน้าที่{rng.choice(ORGAN_JOBS[item.name])}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกส่วนที่ทำหน้าที่นั้นโดยตรง",
        )


@question_type(
    "plant.organ_function_fluency",
    display_name={"th": "ผลเมื่อส่วนของพืชทำหน้าที่ไม่ได้"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantOrganFunctionFluency(QuestionType):
    """Say what fails when one organ cannot do its job.

    Naming the four jobs is Foundation work. Knowing a job well enough to say what
    goes wrong without it is what separates reciting the list from understanding
    it, and it still covers all four organs the indicator names.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ORGANS)
        others = [rng.choice(ORGAN_FAILURES[other.name])
                  for other in ORGANS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _plant(
                stem=f"ถ้า “{item.name}” ของพืชดอกเสียหายจนทำหน้าที่ไม่ได้ "
                     f"จะเกิดอะไรขึ้น",
                correct=rng.choice(ORGAN_FAILURES[item.name]),
                wrongs=tuple(others[:3]),
                hint="เริ่มจากหน้าที่ของส่วนนั้น แล้วถามว่าถ้าหน้าที่นั้นหายไป "
                     "อะไรจะทำต่อไม่ได้",
            )
        return _plant(
            stem=f"อาการที่ว่า {rng.choice(ORGAN_FAILURES[item.name])} "
                 f"เกิดจากส่วนใดของพืชเสียหาย",
            correct=item.name,
            wrongs=tuple(other.name for other in ORGANS if other.name != item.name),
            hint="อ่านอาการให้จบ แล้วย้อนกลับไปว่าหน้าที่ใดหายไป",
        )


@question_type(
    "plant.organ_function_application",
    display_name={"th": "วิเคราะห์การทำงานของส่วนต่าง ๆ ของพืชดอก"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantOrganFunctionApplication(QuestionType):
    """Explain what happened to a plant by the organ concerned."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, PLANT_ORGAN_SCENARIOS,
            hint="ระบุก่อนว่าเรื่องนี้เกี่ยวกับการดูดน้ำ การลำเลียง การสร้างอาหาร "
                 "หรือการสืบพันธุ์",
        ), PLANT_TOPIC)


@question_type(
    "plant.organ_diagram",
    display_name={"th": "ระบุส่วนของพืชจากภาพและบอกหน้าที่"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=PLANT_TOPIC,
)
class PlantOrganDiagram(QuestionType):
    """Root, stem, leaf and flower numbered on a drawn plant: name one, its job, or what fails without it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(PLANT_PICTURES)
        organ = rng.choice(PLANT_ORGANS)
        number = spec.numbers[PLANT_ORGANS.index(organ)]
        hint = "รากอยู่ในดิน ลำต้นชูส่วนอื่นขึ้นไป ใบแผ่ออกรับแสง และดอกอยู่ปลายยอด"
        kind = rng.randrange(3)
        if kind == 0:
            return diagram_question(
                spec.asset_id, PLANT_ALT,
                stem=f"จากภาพต้นพืช ส่วนหมายเลข {number} คือส่วนใด",
                correct=organ,
                wrongs=tuple(o for o in PLANT_ORGANS if o != organ),
                hint=hint, topic=PLANT_TOPIC,
            )
        table = ORGAN_JOBS if kind == 1 else ORGAN_FAILURES
        ask = "ทำหน้าที่ใด" if kind == 1 else "ถ้าต้นพืชไม่มีส่วนนี้ จะเกิดผลอย่างไร"
        return diagram_question(
            spec.asset_id, PLANT_ALT,
            stem=f"จากภาพต้นพืช ส่วนหมายเลข {number} {ask}",
            correct=rng.choice(table[organ]),
            wrongs=tuple(rng.choice(lines) for name, lines in table.items() if name != organ),
            hint="ระบุชื่อส่วนจากตำแหน่งในภาพก่อน แล้วนึกถึงหน้าที่ของส่วนนั้น",
            topic=PLANT_TOPIC,
        )
