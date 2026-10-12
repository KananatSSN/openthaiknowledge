"""แผ่นดินไหว

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/5

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
    EARTHQUAKE,
    EARTHQUAKE_SCENARIOS,
    explanation_item,
    plan_item,
)

PROVENANCE = Provenance("original")


@question_type(
    "geo.earthquake_foundation",
    display_name={"th": "ออกแบบแนวทางเฝ้าระวังและปฏิบัติตนจากแผ่นดินไหว"},
    level=UPPER_SIX, subject=SUBJECT, topic=EARTHQUAKE,
)
class EarthquakeFoundation(QuestionType):
    """Propose monitoring and safe conduct for an earthquake case."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return plan_item(rng, EARTHQUAKE, EARTHQUAKE)


@question_type(
    "geo.earthquake_fluency",
    display_name={"th": "อธิบายสาเหตุ กระบวนการเกิด ขนาดและความรุนแรง และผลของแผ่นดินไหว"},
    level=UPPER_SIX, subject=SUBJECT, topic=EARTHQUAKE,
)
class EarthquakeFluency(QuestionType):
    """Explain cause, process, magnitude and intensity, and effects together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return explanation_item(rng, EARTHQUAKE, EARTHQUAKE)


@question_type(
    "geo.earthquake_application",
    display_name={"th": "วิเคราะห์ขนาด ความรุนแรง และผลของแผ่นดินไหว"},
    level=UPPER_SIX, subject=SUBJECT, topic=EARTHQUAKE,
)
class EarthquakeApplication(QuestionType):
    """Energy across magnitudes, magnitude against intensity, and Bangkok's soft soil."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, EARTHQUAKE_SCENARIOS,
            hint="แยกขนาดซึ่งเป็นพลังงานที่จุดกำเนิด ออกจากความรุนแรงซึ่งขึ้นกับตำแหน่งที่สังเกต",
        ), EARTHQUAKE)
