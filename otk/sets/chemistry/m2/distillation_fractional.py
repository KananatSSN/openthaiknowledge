"""การกลั่นลำดับส่วน

เคมี · ม.2 · เสริมทักษะ
Indicators: —

Sets moved here from: science_successors.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.sets._support.science_successors import FluencyStage
from otk.sets.chemistry.m2.distillation import Distillation

PROVENANCE = Provenance("original")


@question_type(
    "chem.distillation_fractional",
    display_name={"th": "การกลั่นลำดับส่วน"},
    level={"th": "ม.2"}, subject="เคมี", topic="การแยกสาร",
)
class FractionalDistillation(FluencyStage, Distillation):
    source_key = "chem.distillation"
    ITEMS = [Distillation.ITEMS[index] for index in (4, 5, 7, 8)]
