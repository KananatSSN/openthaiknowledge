"""การทดลองเปรียบเทียบอัตราการเต้นของหัวใจ

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/8

Sets moved here from: science_wave_b10.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import LEVEL, SUBJECT, TOPIC, labelled, scenario_question
from otk.sets._support.science_wave_b10 import HEART_RATE_SCENARIOS

PROVENANCE = Provenance("original")


class Fact(NamedTuple):
    """One question about measuring heart rate, and its single answer."""
    question: str
    answer: str


HEART_RATE_FACTS = (
    Fact("ชีพจรที่จับได้ที่ข้อมือเกิดจากสิ่งใด",
         "แรงดันที่ส่งไปตามผนังหลอดเลือดแดงทุกครั้งที่หัวใจห้องล่างบีบตัว"),
    Fact("หน่วยที่ใช้บอกอัตราการเต้นของหัวใจคือข้อใด",
         "จำนวนครั้งของการเต้นต่อหนึ่งนาที"),
    Fact("เหตุใดอัตราการเต้นของหัวใจจึงเพิ่มขึ้นขณะออกกำลังกาย",
         "เซลล์กล้ามเนื้อต้องการออกซิเจนมากขึ้นและสร้างของเสียมากขึ้น "
         "หัวใจจึงต้องสูบฉีดเลือดให้ถี่ขึ้นเพื่อลำเลียงให้ทัน"),
    Fact("ควรจับชีพจรด้วยวิธีใดจึงจะได้ค่าที่น่าเชื่อถือ",
         "ใช้ปลายนิ้วชี้และนิ้วกลางกดเบา ๆ บนหลอดเลือดแดงที่ข้อมือ แล้วนับให้ครบเวลาที่กำหนด"),
    Fact("หลังหยุดออกกำลังกาย อัตราการเต้นของหัวใจเปลี่ยนแปลงอย่างไร",
         "ค่อย ๆ ลดลงจนกลับสู่ระดับขณะพัก โดยผู้ที่ออกกำลังกายสม่ำเสมอจะลดลงได้เร็วกว่า"),
    Fact("เหตุใดจึงต้องวัดอัตราการเต้นของหัวใจขณะพักก่อนเริ่มทำกิจกรรม",
         "เพื่อให้มีค่าเริ่มต้นของคนคนเดียวกันไว้เปรียบเทียบ ผลที่ได้จึงมาจากกิจกรรม"
         "ไม่ใช่จากความแตกต่างระหว่างบุคคล"),
)


class Variable(NamedTuple):
    """One role in the comparison, and the thing that plays it."""
    role: str
    item: str


EXPERIMENT = ("นักเรียนเปรียบเทียบอัตราการเต้นของหัวใจของตนเองขณะนั่งพัก "
              "กับหลังกระโดดตบเป็นเวลา 1 นาที")


VARIABLES = (
    Variable("ตัวแปรต้น", "กิจกรรมที่ทำก่อนวัด คือ นั่งพัก หรือ กระโดดตบ"),
    Variable("ตัวแปรตาม", "อัตราการเต้นของหัวใจเป็นจำนวนครั้งต่อนาที"),
    Variable("ตัวแปรควบคุม",
             "ผู้ถูกวัดคนเดิม ระยะเวลาของกิจกรรม และวิธีจับชีพจรที่เหมือนกันทุกครั้ง"),
)


# Things present in the room that play no role at all. One of them fills the
# fourth choice, so the item is never a one-in-three guess between the roles.
NON_VARIABLES = (
    "สีของเสื้อที่ผู้ถูกวัดสวมในวันที่ทดลอง",
    "จำนวนเพื่อนที่ยืนดูอยู่ข้างสนาม",
    "ยี่ห้อของนาฬิกาที่ใช้จับเวลา",
    "ชื่อของเพลงที่เปิดในห้องขณะทดลอง",
    "สีของรองเท้าที่ผู้ถูกวัดสวม",
    "ความยาวของผมของผู้ถูกวัด",
    "ชื่อเล่นของผู้ถูกวัด",
    "สีของปากกาที่ใช้จดบันทึกผล",
    "จำนวนหน้าต่างในห้องเรียน",
)


@question_type(
    "body.heart_rate_foundation",
    display_name={"th": "อัตราการเต้นของหัวใจและการวัด"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class HeartRateFoundation(QuestionType):
    """What a pulse is, how it is counted, and why it changes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(HEART_RATE_FACTS)
        others = [other.answer for other in HEART_RATE_FACTS
                  if other.answer != item.answer]
        rng.shuffle(others)
        return labelled(
            stem=item.question, correct=item.answer, wrongs=tuple(others[:3]),
            hint="ชีพจรคือแรงดันจากการบีบตัวของหัวใจ และอัตราการเต้นเปลี่ยนไปตาม"
                 "ความต้องการออกซิเจนของเซลล์",
        )


@question_type(
    "body.heart_rate_experiment_fluency",
    display_name={"th": "ตัวแปรในการทดลองเปรียบเทียบอัตราการเต้นของหัวใจ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class HeartRateExperimentFluency(QuestionType):
    """Name the role each thing plays in the comparison.

    ``ม.2/8`` asks the learner to design *and run* the comparison. This item can
    only reach the design half, which is why the whole topic is filed
    ``standard_scope``.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(VARIABLES)
        others = [other.item for other in VARIABLES if other.role != item.role]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return labelled(
                stem=f"{EXPERIMENT} สิ่งใดเป็น “{item.role}” ของการทดลองนี้",
                correct=item.item,
                wrongs=tuple(others[:2]) + (rng.choice(NON_VARIABLES),),
                hint="ตัวแปรต้นคือสิ่งที่ผู้ทดลองจงใจเปลี่ยน ตัวแปรตามคือสิ่งที่วัดผล "
                     "และตัวแปรควบคุมคือสิ่งที่ต้องทำให้เหมือนกันทุกครั้ง",
            )
        wrong_roles = [other.role for other in VARIABLES if other.role != item.role]
        return labelled(
            stem=f"{EXPERIMENT} สิ่งที่ว่า “{item.item}” ทำหน้าที่เป็นอะไร"
                 "ในการทดลองนี้",
            correct=item.role,
            wrongs=tuple(wrong_roles) + ("สิ่งที่ไม่เกี่ยวข้องกับการทดลองนี้",),
            hint="ถามว่าสิ่งนั้นถูกเปลี่ยน ถูกวัด หรือถูกทำให้เหมือนเดิม",
        )


@question_type(
    "body.heart_rate_application",
    display_name={"th": "วิเคราะห์ผลการทดลองอัตราการเต้นของหัวใจ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class HeartRateApplication(QuestionType):
    """Read a set of readings, or judge a plan for collecting them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, HEART_RATE_SCENARIOS,
            hint="ถามว่าเปรียบเทียบคนเดียวกันหรือไม่ วัดด้วยวิธีเดียวกันหรือไม่ "
                 "และค่าที่ต่างกันนั้นอธิบายด้วยความต้องการออกซิเจนได้หรือไม่",
        )
