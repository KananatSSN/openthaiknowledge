"""การใช้ประโยชน์จากสารที่พืชสร้างขึ้น

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/9

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
from otk.sets._support.science_wave_b21 import PLANT_TOPIC, USE_SCENARIOS

PROVENANCE = Provenance("original")


class Use(NamedTuple):
    """One substance a plant makes, the plant, and what people use it for."""
    substance: str
    plant: str
    use: str
    need: str


USES = (
    Use("น้ำมันหอมระเหย", "ตะไคร้หอม",
        "ใช้ไล่ยุงและแมลง และใช้แต่งกลิ่นผลิตภัณฑ์ทำความสะอาด",
        "ต้องการผลิตยาไล่ยุงจากธรรมชาติแทนสารเคมีสังเคราะห์"),
    Use("เคอร์คูมิน", "ขมิ้นชัน",
        "ใช้เป็นสีเหลืองผสมอาหาร และใช้ในผลิตภัณฑ์ที่ช่วยลดการอักเสบ",
        "ต้องการสีเหลืองจากธรรมชาติสำหรับแต่งสีอาหาร"),
    Use("น้ำยาง", "ต้นยางพารา",
        "นำไปผลิตยางรถยนต์ ถุงมือยาง และผลิตภัณฑ์ยางอื่น ๆ",
        "ต้องการวัตถุดิบสำหรับผลิตถุงมือยางทางการแพทย์"),
    Use("แคปไซซิน", "พริก",
        "ให้ความเผ็ด และใช้เป็นตัวยาในพลาสเตอร์หรือครีมบรรเทาอาการปวด",
        "ต้องการทำครีมทาบรรเทาอาการปวดกล้ามเนื้อ"),
    Use("ควินิน", "เปลือกต้นซิงโคนา",
        "ใช้เป็นยารักษาโรคมาลาเรีย และใช้แต่งรสขมในเครื่องดื่มบางชนิด",
        "ต้องการยารักษาผู้ป่วยโรคมาลาเรีย"),
    Use("แทนนิน", "ใบชาและเปลือกไม้บางชนิด",
        "ใช้ฟอกหนังสัตว์ให้คงทน และให้รสฝาดในเครื่องดื่มประเภทชา",
        "ต้องการสารสำหรับฟอกหนังสัตว์ให้คงทนไม่เน่าเปื่อย"),
)


USES += (
    Use('สตีวิโอไซด์',
        'หญ้าหวาน',
        'ใช้ให้ความหวานแทนน้ำตาลโดยให้พลังงานน้อย',
        'ต้องการสารให้ความหวานสำหรับเครื่องดื่มของผู้ควบคุมน้ำตาล'),
    Use('อินดิโก',
        'ต้นคราม',
        'ใช้ย้อมผ้าให้เป็นสีน้ำเงินแบบดั้งเดิม',
        'ต้องการสีย้อมผ้าสีน้ำเงินจากธรรมชาติ'),
)


@question_type(
    "plant.useful_substance_foundation",
    display_name={"th": "สารที่พืชสร้างขึ้นและการใช้ประโยชน์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=PLANT_TOPIC,
)
class UsefulSubstanceFoundation(QuestionType):
    """Give an example of what a plant substance is used for, or which plant."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(USES)
        others = [other for other in USES if other.substance != item.substance]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.substance}” ที่ได้จาก{item.plant} "
                     f"ถูกนำไปใช้ประโยชน์อย่างไร",
                correct=item.use,
                wrongs=tuple(other.use for other in others[:3]),
                hint="นึกถึงสมบัติเด่นของสารนั้นก่อน เช่น มีกลิ่น มีสี มีรส "
                     "หรือมีความยืดหยุ่น",
                topic=PLANT_TOPIC,
            )
        return _labelled(
            stem=f"สารใดที่พืชสร้างขึ้นถูกนำไป{item.use}",
            correct=f"{item.substance}จาก{item.plant}",
            wrongs=tuple(f"{other.substance}จาก{other.plant}"
                         for other in others[:3]),
            hint="อ่านการใช้ประโยชน์ให้จบ แล้วจึงเลือกสารที่มีสมบัติตรงกับการใช้นั้น",
            topic=PLANT_TOPIC,
        )


@question_type(
    "plant.useful_substance_fluency",
    display_name={"th": "เลือกสารจากพืชให้ตรงกับการใช้ประโยชน์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=PLANT_TOPIC,
)
class UsefulSubstanceFluency(QuestionType):
    """Pick the plant substance that answers a stated need."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(USES)
        others = [f"{other.substance}จาก{other.plant}" for other in USES
                  if other.substance != item.substance]
        rng.shuffle(others)
        return _labelled(
            stem=f"ถ้า{item.need} ควรเลือกใช้สารใดที่พืชสร้างขึ้น",
            correct=f"{item.substance}จาก{item.plant}",
            wrongs=tuple(others[:3]),
            hint="จับคู่ความต้องการกับสมบัติของสาร ไม่ใช่กับความคุ้นเคยของชื่อพืช",
            topic=PLANT_TOPIC,
        )


@question_type(
    "plant.useful_substance_application",
    display_name={"th": "อภิปรายการใช้ประโยชน์จากสารที่พืชสร้างขึ้น"},
    level=UPPER_FOUR, subject=SUBJECT, topic=PLANT_TOPIC,
)
class UsefulSubstanceApplication(QuestionType):
    """Weigh a claim about using what plants make, against what is known."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, USE_SCENARIOS,
            hint="แยกให้ออกระหว่างประโยชน์ที่สารนั้นมีต่อพืชเอง "
                 "กับประโยชน์ที่มนุษย์นำไปใช้ และดูว่าคำกล่าวอ้างเกินหลักฐานหรือไม่",
        ), PLANT_TOPIC)
