"""การแยกสารด้วยเครื่องหมุนเหวี่ยง

เคมี · ม.2 · เสริมทักษะ
Indicators: —

Sets moved here from: science_successors.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.sets._support.science_successors import FluencyStage
from otk.sets.chemistry.p6.sedimentation import Sedimentation

PROVENANCE = Provenance("original")


@question_type(
    "chem.sedimentation_centrifuge",
    display_name={"th": "การแยกสารด้วยเครื่องหมุนเหวี่ยง"},
    level={"th": "ม.2"}, subject="เคมี", topic="การแยกสาร",
)
class SedimentationCentrifuge(FluencyStage, Sedimentation):
    source_key = "chem.sedimentation"
    ITEMS = [Sedimentation.ITEMS[index] for index in (4, 6, 7)]
