"""สึนามิ

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/6

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
    TSUNAMI,
    TSUNAMI_SCENARIOS,
    explanation_item,
    plan_item,
)

PROVENANCE = Provenance("original")


@question_type(
    "geo.tsunami_foundation",
    display_name={"th": "ออกแบบแนวทางเฝ้าระวังและปฏิบัติตนจากสึนามิ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TSUNAMI,
)
class TsunamiFoundation(QuestionType):
    """Propose monitoring and safe conduct for a tsunami case."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return plan_item(rng, TSUNAMI, TSUNAMI)


@question_type(
    "geo.tsunami_fluency",
    display_name={"th": "อธิบายสาเหตุ กระบวนการเกิด และผลของสึนามิ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TSUNAMI,
)
class TsunamiFluency(QuestionType):
    """Explain the cause, process and effects of a tsunami together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return explanation_item(rng, TSUNAMI, TSUNAMI)


@question_type(
    "geo.tsunami_application",
    display_name={"th": "วิเคราะห์การเกิดสึนามิและระบบเตือนภัย"},
    level=UPPER_SIX, subject=SUBJECT, topic=TSUNAMI,
)
class TsunamiApplication(QuestionType):
    """A calm deep sea, quakes without tsunamis, and Thailand's warning system."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, TSUNAMI_SCENARIOS,
            hint="นึกว่าพื้นทะเลเคลื่อนที่อย่างไร และคลื่นเปลี่ยนไปอย่างไรเมื่อเข้าสู่น้ำตื้น",
        ), TSUNAMI)
