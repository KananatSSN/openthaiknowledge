"""ผลของการเปลี่ยนลำดับนิวคลีโอไทด์

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.4/3

Sets moved here from: science_wave_b29.
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
from otk.sets._support.science_wave_b19 import UPPER_FOUR, Fact, _fact_question
from otk.sets._support.science_wave_b29 import MUTATION_SCENARIOS

PROVENANCE = Provenance("original")


MUTATION_TOPIC = "การเปลี่ยนแปลงของสารพันธุกรรม"


MUTATION_FACTS = (
    Fact("มิวเทชันคืออะไร",
         "การเปลี่ยนแปลงของลำดับนิวคลีโอไทด์ในดีเอ็นเอ "
         "ซึ่งอาจเกิดขึ้นเองหรือเกิดจากสิ่งกระตุ้นจากภายนอก"),
    Fact("การแทนที่เบสหนึ่งตัวส่งผลอย่างไรได้บ้าง",
         "อาจไม่เปลี่ยนกรดแอมิโนเลย อาจเปลี่ยนเป็นกรดแอมิโนตัวอื่น "
         "หรืออาจกลายเป็นรหัสหยุดจนได้โปรตีนที่สั้นผิดปกติ"),
    Fact("เหตุใดการแทนที่เบสบางครั้งจึงไม่มีผลต่อโปรตีนเลย",
         "เพราะกรดแอมิโนตัวหนึ่งมีโคดอนกำหนดได้หลายแบบ "
         "การเปลี่ยนเบสบางตำแหน่งจึงยังให้กรดแอมิโนตัวเดิม"),
    Fact("การเพิ่มหรือขาดเบสหนึ่งตัวส่งผลรุนแรงกว่าการแทนที่อย่างไร",
         "ทำให้การอ่านรหัสทีละสามเบสเลื่อนไปทั้งสาย "
         "กรดแอมิโนตั้งแต่จุดนั้นไปจึงเปลี่ยนไปเกือบทั้งหมด"),
    Fact("มิวเทชันที่เกิดในเซลล์ร่างกายกับในเซลล์สืบพันธุ์ต่างกันอย่างไร",
         "ที่เกิดในเซลล์ร่างกายส่งผลเฉพาะกับผู้นั้นและไม่ถ่ายทอดต่อ "
         "ส่วนที่เกิดในเซลล์สืบพันธุ์ถ่ายทอดไปยังรุ่นลูกได้"),
    Fact("สิ่งใดกระตุ้นให้เกิดมิวเทชันได้",
         "รังสีบางชนิด เช่น รังสีอัลตราไวโอเลตและรังสีเอกซ์ "
         "และสารเคมีบางชนิด เช่น สารในควันบุหรี่"),
    Fact("มิวเทชันมีผลต่อสิ่งมีชีวิตในทางใดได้บ้าง",
         "อาจไม่มีผล อาจเป็นโทษจนทำให้เกิดโรค "
         "หรืออาจเป็นประโยชน์จนได้ลักษณะใหม่ที่ได้เปรียบในสิ่งแวดล้อมนั้น"),
)


class Change(NamedTuple):
    """A described change in a sequence, and what it does to the protein."""
    change: str
    effect: str


CHANGES = (
    Change("เบสหนึ่งตัวถูกแทนที่ด้วยเบสอื่น แต่โคดอนใหม่ยังกำหนดกรดแอมิโนตัวเดิม",
           "ลำดับกรดแอมิโนไม่เปลี่ยน โปรตีนจึงทำงานได้ตามปกติ "
           "และลักษณะที่ปรากฏไม่เปลี่ยนแปลง"),
    Change("เบสหนึ่งตัวถูกแทนที่จนโคดอนใหม่กำหนดกรดแอมิโนคนละตัว",
           "โปรตีนมีกรดแอมิโนต่างไปหนึ่งตัว ซึ่งอาจทำงานได้ตามเดิม "
           "หรือทำงานผิดปกติ ขึ้นกับว่าตำแหน่งนั้นสำคัญต่อการพับตัวเพียงใด"),
    Change("เบสหนึ่งตัวถูกแทนที่จนโคดอนกลางสายกลายเป็นรหัสหยุด",
           "การสร้างสายพอลิเพปไทด์หยุดก่อนกำหนด "
           "ได้โปรตีนที่สั้นกว่าปกติและมักทำหน้าที่ไม่ได้"),
    Change("มีเบสเพิ่มเข้ามาหนึ่งตัวตรงกลางของยีน",
           "การอ่านรหัสทีละสามเบสเลื่อนไปทั้งสายตั้งแต่จุดนั้น "
           "กรดแอมิโนหลังจุดนั้นจึงเปลี่ยนไปเกือบทั้งหมดและโปรตีนมักใช้การไม่ได้"),
    Change("มีเบสขาดหายไปสามตัวติดกันตรงกลางของยีน",
           "กรอบการอ่านรหัสยังคงเดิม แต่โปรตีนขาดกรดแอมิโนไปหนึ่งตัว "
           "ผลจึงมักไม่รุนแรงเท่าการขาดหายเพียงหนึ่งตัว"),
    Change("เบสเปลี่ยนไปในช่วงของยีนที่ไม่ได้ถูกแปลรหัสเป็นโปรตีน",
           "ลำดับกรดแอมิโนไม่เปลี่ยน แต่ถ้าตำแหน่งนั้นควบคุมการแสดงออกของยีน "
           "ปริมาณโปรตีนที่สร้างได้อาจเปลี่ยนไป"),
)


@question_type(
    "life.mutation_effect_foundation",
    display_name={"th": "การเปลี่ยนแปลงลำดับนิวคลีโอไทด์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=MUTATION_TOPIC,
)
class MutationEffectFoundation(QuestionType):
    """What kinds of change there are, and what each can do."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, MUTATION_FACTS, topic=MUTATION_TOPIC,
            hint="แยกการแทนที่เบสออกจากการเพิ่มหรือขาดเบส "
                 "เพราะสองอย่างนี้ส่งผลต่อการอ่านรหัสไม่เหมือนกัน",
        )


@question_type(
    "life.mutation_effect_fluency",
    display_name={"th": "ผลของการเปลี่ยนลำดับนิวคลีโอไทด์ต่อการแสดงลักษณะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=MUTATION_TOPIC,
)
class MutationEffectFluency(QuestionType):
    """Say what a stated change does to the protein and to the trait."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CHANGES)
        others = [other.effect for other in CHANGES if other.effect != item.effect]
        rng.shuffle(others)
        return _labelled(
            stem=f"ถ้า{item.change} จะเกิดผลอย่างไรต่อโปรตีนและการแสดงลักษณะ",
            correct=item.effect, wrongs=tuple(others[:3]),
            hint="ถามก่อนว่ากรอบการอ่านรหัสเลื่อนไปหรือไม่ "
                 "แล้วจึงถามว่ากรดแอมิโนที่เปลี่ยนไปอยู่ตำแหน่งสำคัญเพียงใด",
            topic=MUTATION_TOPIC,
        )


@question_type(
    "life.mutation_effect_application",
    display_name={"th": "วิเคราะห์ผลของมิวเทชันต่อสิ่งมีชีวิต"},
    level=UPPER_FOUR, subject=SUBJECT, topic=MUTATION_TOPIC,
)
class MutationEffectApplication(QuestionType):
    """Judge a case where a sequence change did — or did not — matter."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, MUTATION_SCENARIOS,
            hint="ถามว่าเกิดที่เซลล์ร่างกายหรือเซลล์สืบพันธุ์ "
                 "และการเปลี่ยนแปลงนั้นเลื่อนกรอบการอ่านรหัสหรือไม่",
        ), MUTATION_TOPIC)
