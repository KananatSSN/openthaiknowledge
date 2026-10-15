"""เซลล์พืชและเซลล์สัตว์

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/1

Sets moved here from: science_wave_b2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b2 import (
    BOTH,
    CELL_SCENARIOS,
    LEVEL,
    ORGANELLES,
    PLANT_ONLY,
    SUBJECT,
    TOPIC,
    _labelled,
)
from otk.sets._support.life_earth_diagrams import CELL_ALT, CELL_DIAGRAMS, PLANT_PARTS
from otk.sets._support.ms1_diagrams import diagram_question

PROVENANCE = Provenance("original")


@question_type(
    "cell.organelle_function_foundation",
    display_name={"th": "หน้าที่ของโครงสร้างภายในเซลล์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class OrganelleFunctionFoundation(QuestionType):
    """Name a structure's job, or the structure that does a job.

    Both directions read the same table, so the function attributed to a
    structure is the same sentence whichever way the question is asked.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ORGANELLES)
        others = [other for other in ORGANELLES if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” ทำหน้าที่ใดในเซลล์",
                correct=item.function,
                wrongs=tuple(other.function for other in others[:3]),
                hint="นึกถึงว่าโครงสร้างนั้นอยู่ตรงไหนของเซลล์ "
                     "แล้วสิ่งที่อยู่ตรงนั้นน่าจะทำหน้าที่อะไร",
            )
        return _labelled(
            stem=f"โครงสร้างใดในเซลล์ทำหน้าที่{item.function}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกโครงสร้างที่ทำหน้าที่นั้นโดยตรง",
        )


@question_type(
    "cell.plant_animal_fluency",
    display_name={"th": "เปรียบเทียบโครงสร้างของเซลล์พืชกับเซลล์สัตว์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PlantAnimalFluency(QuestionType):
    """Which cell has which structure, and what a listed set of structures implies.

    The comparison ``ม.1/1`` opens with. The second branch is where it bites: a
    learner who knows ผนังเซลล์ is plant-only still has to notice that a list
    *without* it rules the plant cell out.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        if which == 0:
            # Asked as a pair rather than as "which cell has X". The three labels
            # พืช/สัตว์/ทั้งสอง would give a three-choice question, and no
            # structure in ม.1/1's list is animal-only, so that direction has no
            # answer to offer either. A pair keeps four choices and still turns on
            # exactly the plant-versus-animal distinction.
            plant_only = [item.name for item in ORGANELLES
                          if item.where == PLANT_ONLY]
            shared = [item.name for item in ORGANELLES if item.where == BOTH]
            rng.shuffle(shared)
            return _labelled(
                stem="ข้อใดเป็นโครงสร้างที่พบในเซลล์พืชแต่ไม่พบในเซลล์สัตว์ทั้งคู่",
                correct=" และ".join(plant_only),
                wrongs=(f"{plant_only[0]} และ{shared[0]}",
                        f"{plant_only[1]} และ{shared[1]}",
                        f"{shared[2]} และ{shared[3]}"),
                hint="ตรวจทีละชื่อว่าเซลล์สัตว์มีโครงสร้างนั้นหรือไม่ "
                     "ข้อที่ถูกต้องต้องไม่มีในเซลล์สัตว์ทั้งสองชื่อ",
            )
        if which == 1:
            plant_only = [item for item in ORGANELLES
                          if item.where == PLANT_ONLY]
            shared = [item for item in ORGANELLES if item.where == BOTH]
            rng.shuffle(shared)
            answer = rng.choice(plant_only)
            return _labelled(
                stem="โครงสร้างใดต่อไปนี้พบในเซลล์พืชแต่ไม่พบในเซลล์สัตว์",
                correct=answer.name,
                wrongs=tuple(item.name for item in shared[:3]),
                hint="ตัดโครงสร้างที่ทั้งสองชนิดมีเหมือนกันออกก่อน",
            )
        shared = [item.name for item in ORGANELLES if item.where == BOTH]
        rng.shuffle(shared)
        listed = shared[:3]
        if rng.random() < 0.5:
            observed = listed + ["ผนังเซลล์", "คลอโรพลาสต์"]
            correct = "เซลล์พืช เพราะมีผนังเซลล์และคลอโรพลาสต์ซึ่งเซลล์สัตว์ไม่มี"
            wrongs = (
                "เซลล์สัตว์ เพราะมีเยื่อหุ้มเซลล์และนิวเคลียสครบ",
                "เซลล์สัตว์ เพราะผนังเซลล์พบได้ในเซลล์สัตว์บางชนิดเท่านั้น",
                "บอกไม่ได้ เพราะต้องเห็นรูปร่างของเซลล์ก่อนจึงจะระบุชนิดได้",
            )
        else:
            observed = listed
            correct = "เซลล์สัตว์ เพราะไม่พบผนังเซลล์และคลอโรพลาสต์ในภาพ"
            wrongs = (
                "เซลล์พืช เพราะมีเยื่อหุ้มเซลล์และนิวเคลียสเหมือนเซลล์พืชทุกประการ",
                "เซลล์พืช เพราะผนังเซลล์อาจบางจนมองไม่เห็นด้วยกล้องจุลทรรศน์ใช้แสง",
                "บอกไม่ได้ เพราะเซลล์พืชและเซลล์สัตว์มีโครงสร้างเหมือนกันทุกอย่าง",
            )
        rng.shuffle(observed)
        return _labelled(
            stem="ส่องเซลล์ชนิดหนึ่งด้วยกล้องจุลทรรศน์ใช้แสง แล้วบันทึกโครงสร้างที่เห็นได้ดังนี้: "
                 f"{', '.join(observed)} เซลล์นี้น่าจะเป็นเซลล์ชนิดใด และเพราะเหตุใด",
            correct=correct,
            wrongs=wrongs,
            hint="ดูว่าในรายการมีโครงสร้างที่พบเฉพาะในเซลล์พืชหรือไม่",
        )


@question_type(
    "cell.structure_application",
    display_name={"th": "ใช้หน้าที่ของโครงสร้างเซลล์อธิบายสถานการณ์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class CellStructureApplication(QuestionType):
    """Explain an observation by what a structure does — or by its absence.

    Each item states something seen and asks which structure accounts for it.
    The wrong choices all attribute the observation to a real structure doing a
    job that belongs to a different one, so the table has to be known both ways.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(CELL_SCENARIOS)
        return _labelled(
            stem=stem, correct=correct, wrongs=wrongs,
            hint="ระบุก่อนว่าสิ่งที่สังเกตได้เกี่ยวข้องกับโครงสร้างใด "
                 "แล้วจึงตรวจว่าโครงสร้างนั้นทำหน้าที่ตามที่ตัวเลือกอ้างจริงหรือไม่",
        )


PLANT_REASON = "เซลล์พืช เพราะมีผนังเซลล์และคลอโรพลาสต์"
ANIMAL_REASON = "เซลล์สัตว์ เพราะไม่มีผนังเซลล์และคลอโรพลาสต์"


@question_type(
    "cell.cell_diagram",
    display_name={"th": "ระบุส่วนประกอบของเซลล์จากภาพ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class CellDiagram(QuestionType):
    """A numbered plant or animal cell: name a part, give its job, or say which cell it is.

    The numbering differs between pictures of the same cell, and the jobs come
    from ``ORGANELLES``, the same table the other sets in this unit teach from.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(CELL_DIAGRAMS)
        part = rng.choice(spec.labelled)
        number = spec.number_of(part)
        kind = rng.randrange(3)
        if kind == 0:
            others = [p for p in PLANT_PARTS if p != part]
            rng.shuffle(others)
            return diagram_question(
                spec.asset_id, CELL_ALT,
                stem=f"จากภาพเซลล์ ส่วนหมายเลข {number} คือส่วนใด",
                correct=part, wrongs=tuple(others[:4]),
                hint="ไล่จากด้านนอกเข้าด้านใน: ผนังเซลล์ (มีเฉพาะพืช) เยื่อหุ้มเซลล์ ไซโทพลาซึม แล้วจึงเป็นนิวเคลียสและออร์แกเนลล์",
                topic=TOPIC,
            )
        if kind == 1:
            job = {o.name: o.function for o in ORGANELLES}
            return diagram_question(
                spec.asset_id, CELL_ALT,
                stem=f"จากภาพเซลล์ ส่วนหมายเลข {number} ทำหน้าที่ใด",
                correct=job[part],
                wrongs=tuple(j for name, j in job.items() if name != part),
                hint="ระบุชื่อส่วนจากตำแหน่งในภาพก่อน แล้วนึกถึงหน้าที่ของส่วนนั้น",
                topic=TOPIC,
            )
        plant = spec.kind == "plant"
        return diagram_question(
            spec.asset_id, CELL_ALT,
            stem="ภาพนี้เป็นเซลล์พืชหรือเซลล์สัตว์ และใช้สิ่งใดตัดสิน",
            correct=PLANT_REASON if plant else ANIMAL_REASON,
            wrongs=(ANIMAL_REASON if plant else PLANT_REASON,
                    "เซลล์พืช เพราะมีนิวเคลียสและเยื่อหุ้มเซลล์" if not plant
                    else "เซลล์สัตว์ เพราะมีนิวเคลียสและเยื่อหุ้มเซลล์",
                    "บอกไม่ได้ เพราะเซลล์พืชและเซลล์สัตว์มีส่วนประกอบเหมือนกันทุกส่วน"),
            hint="ส่วนที่พบเฉพาะในเซลล์พืชคือผนังเซลล์และคลอโรพลาสต์ ส่วนนิวเคลียสพบได้ทั้งสองแบบ",
            topic=TOPIC,
        )
