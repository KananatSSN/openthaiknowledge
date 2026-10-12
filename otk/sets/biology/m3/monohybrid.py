"""การถ่ายทอดลักษณะทางพันธุกรรม

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.3/2

Sets moved here from: science_wave_b25.
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
from otk.sets._support.science_wave_b19 import Fact, _fact_question
from otk.sets._support.science_wave_b25 import (
    CROSS_TOPIC,
    MENDEL_TRAITS,
    MIDDLE_THREE,
    MONOHYBRID_SCENARIOS,
    _genotypes,
)

PROVENANCE = Provenance("original")


MENDEL_FACTS = (
    Fact("แอลลีลเด่นหมายถึงอะไร",
         "แอลลีลที่แสดงลักษณะออกมาได้แม้จะมีอยู่เพียงแอลลีลเดียวในคู่"),
    Fact("แอลลีลด้อยหมายถึงอะไร",
         "แอลลีลที่แสดงลักษณะออกมาได้ก็ต่อเมื่อมีอยู่ทั้งสองแอลลีลในคู่"),
    Fact("การข่มอย่างสมบูรณ์หมายถึงอะไร",
         "การที่แอลลีลเด่นบดบังแอลลีลด้อยได้ทั้งหมด ลักษณะที่ปรากฏจึงเหมือนกับ"
         "ผู้ที่มีแอลลีลเด่นทั้งคู่ทุกประการ"),
    Fact("จีโนไทป์หมายถึงอะไร",
         "คู่ของแอลลีลที่สิ่งมีชีวิตนั้นมีอยู่สำหรับลักษณะหนึ่ง เช่น TT Tt หรือ tt"),
    Fact("ฟีโนไทป์หมายถึงอะไร",
         "ลักษณะที่ปรากฏออกมาให้สังเกตเห็นได้ เช่น ต้นสูงหรือต้นเตี้ย"),
    Fact("พันธุ์แท้และพันธุ์ทางต่างกันอย่างไร",
         "พันธุ์แท้มีแอลลีลทั้งคู่เหมือนกัน เช่น TT หรือ tt "
         "ส่วนพันธุ์ทางมีแอลลีลทั้งคู่ต่างกัน เช่น Tt"),
    Fact("เหตุใดสิ่งมีชีวิตที่มีจีโนไทป์ Tt จึงแสดงลักษณะเหมือน TT",
         "เพราะแอลลีล T ข่มแอลลีล t อย่างสมบูรณ์ "
         "ลักษณะที่ปรากฏจึงถูกกำหนดโดยแอลลีลเด่นเพียงตัวเดียว"),
)


class Cross(NamedTuple):
    """A cross written as index pairs into (dominant, hetero, recessive)."""
    first: int
    second: int
    outcome: str


# 0 = both dominant alleles, 1 = one of each, 2 = both recessive.
CROSSES = (
    Cross(0, 2, "ลูกทุกตัวมีจีโนไทป์แบบพันธุ์ทาง จึงแสดง{dom}ทั้งหมด"),
    Cross(1, 1, "ลูกแสดง{dom}ต่อ{rec} ในอัตราส่วน 3 ต่อ 1"),
    Cross(1, 2, "ลูกแสดง{dom}ต่อ{rec} ในอัตราส่วน 1 ต่อ 1"),
    Cross(0, 1, "ลูกทุกตัวแสดง{dom} โดยครึ่งหนึ่งเป็นพันธุ์แท้และอีกครึ่งหนึ่ง"
                "เป็นพันธุ์ทาง"),
    Cross(2, 2, "ลูกทุกตัวมีแอลลีลด้อยทั้งคู่ จึงแสดง{rec}ทั้งหมด"),
    Cross(0, 0, "ลูกทุกตัวมีแอลลีลเด่นทั้งคู่ จึงแสดง{dom}ทั้งหมด"),
)


@question_type(
    "life.monohybrid_foundation",
    display_name={"th": "แอลลีลเด่น แอลลีลด้อย และการข่มอย่างสมบูรณ์"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=CROSS_TOPIC,
)
class MonohybridFoundation(QuestionType):
    """The vocabulary a cross is read with."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, MENDEL_FACTS, topic=CROSS_TOPIC,
            hint="แยกให้ชัดระหว่างจีโนไทป์ซึ่งเป็นคู่ของแอลลีล "
                 "กับฟีโนไทป์ซึ่งเป็นลักษณะที่มองเห็น",
        )


@question_type(
    "life.monohybrid_fluency",
    display_name={"th": "ผลของการผสมพิจารณาลักษณะเดียว"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=CROSS_TOPIC,
)
class MonohybridFluency(QuestionType):
    """Say what a one-trait cross gives, under complete dominance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        trait = rng.choice(MENDEL_TRAITS)
        codes = _genotypes(trait)
        item = rng.choice(CROSSES)
        fill = {"dom": trait.dominant, "rec": trait.recessive}
        others = [other.outcome.format(**fill) for other in CROSSES
                  if other.outcome != item.outcome]
        rng.shuffle(others)
        return _labelled(
            stem=f"ใน{trait.subject} แอลลีล {trait.letter} ซึ่งควบคุม"
                 f"{trait.dominant} ข่มแอลลีล {trait.letter.lower()} "
                 f"ซึ่งควบคุม{trait.recessive} อย่างสมบูรณ์ "
                 f"ถ้าผสม {codes[item.first]} กับ {codes[item.second]} "
                 f"ลูกที่ได้จะเป็นอย่างไร",
            correct=item.outcome.format(**fill),
            wrongs=tuple(others[:3]),
            hint="เขียนแอลลีลที่พ่อแม่แต่ละฝ่ายให้ได้ออกมาก่อน "
                 "แล้วจึงจับคู่กันให้ครบทุกแบบ",
            topic=CROSS_TOPIC,
        )


@question_type(
    "life.monohybrid_application",
    display_name={"th": "วิเคราะห์การถ่ายทอดลักษณะเดียว"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=CROSS_TOPIC,
)
class MonohybridApplication(QuestionType):
    """Reason backwards from offspring to the parents' alleles."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, MONOHYBRID_SCENARIOS,
            hint="ลักษณะด้อยที่ปรากฏในลูกบอกได้เสมอว่าพ่อแม่ทั้งสองฝ่าย"
                 "ต่างก็มีแอลลีลด้อยอยู่",
        ), CROSS_TOPIC)
