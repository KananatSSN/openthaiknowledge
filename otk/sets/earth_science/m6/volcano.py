"""ภูเขาไฟระเบิด

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/4

Sets moved here from: science_wave_c23.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c23 import (
    VOLCANO,
    VOLCANO_SCENARIOS,
    explanation_item,
    plan_item,
)

PROVENANCE = Provenance("original")


@question_type(
    "geo.volcano_foundation",
    display_name={"th": "ออกแบบแนวทางเฝ้าระวังและปฏิบัติตนจากภูเขาไฟระเบิด"},
    level=UPPER_SIX, subject=SUBJECT, topic=VOLCANO,
)
class VolcanoFoundation(QuestionType):
    """Propose monitoring and safe conduct for a volcano case."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return plan_item(rng, VOLCANO, VOLCANO)


@question_type(
    "geo.volcano_fluency",
    display_name={"th": "อธิบายสาเหตุ กระบวนการเกิด และผลของภูเขาไฟระเบิด"},
    level=UPPER_SIX, subject=SUBJECT, topic=VOLCANO,
)
class VolcanoFluency(QuestionType):
    """Explain the cause, process and effects of an eruption together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return explanation_item(rng, VOLCANO, VOLCANO)


@question_type(
    "geo.volcano_application",
    display_name={"th": "วิเคราะห์ภูเขาไฟและการเตือนภัย"},
    level=UPPER_SIX, subject=SUBJECT, topic=VOLCANO,
)
class VolcanoApplication(QuestionType):
    """The Ring of Fire, eruption warnings, and ash far from the volcano."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, VOLCANO_SCENARIOS,
            hint="เชื่อมภูเขาไฟกับแนวรอยต่อของแผ่นธรณีและสัญญาณที่วัดได้ก่อนปะทุ",
        ), VOLCANO)
