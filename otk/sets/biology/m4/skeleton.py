"""โครงกระดูกมนุษย์

ชีวะ · ม.4 · เสริมทักษะ
Indicators: —

Sets moved here from: biology.
"""

from __future__ import annotations

from abc import abstractmethod
from random import Random
from typing import NamedTuple

from otk.core.content import Marker, image, text
from otk.core.distractors import label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type

PROVENANCE = Provenance("original")


class Part(NamedTuple):
    asset_id: str          # diagram this part belongs to
    marker: Marker         # where the arrow points (normalized 0..1)
    label: str             # Thai part name — the correct answer


class LabeledDiagramType(QuestionType):
    """Base: pick a part, arrow it, ask for its name; distractors are siblings."""

    @abstractmethod
    def parts(self) -> list[Part]:
        """The labelled parts this type draws from (≥ 4 for four choices)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        parts = self.parts()
        chosen = rng.choice(parts)
        return GeneratedQuestion(
            stem=[image(chosen.asset_id, chosen.marker,
                        alt="ชี้ส่วนที่ลูกศรชี้")],
            correct=[text(chosen.label)],
            distractors=label_pool([p.label for p in parts]),
            topic=self.topic,
        )


@question_type("anatomy.skeleton",
               display_name={"th": "กระดูกและโครงร่าง"},
               level={"th": "ม.4"}, subject="ชีวะ",
               topic="กายวิภาค: โครงกระดูก")
class SkeletonLabel(LabeledDiagramType):
    # Marker coords are aligned with the built-in schematic, drawn by
    # make_skeleton in otk/pictures/generate.py.
    _PARTS = [
        Part("skeleton", Marker(x=0.50, y=0.08), "กะโหลกศีรษะ"),
        Part("skeleton", Marker(x=0.34, y=0.21), "กระดูกไหปลาร้า"),
        Part("skeleton", Marker(x=0.42, y=0.39), "กระดูกซี่โครง"),
        Part("skeleton", Marker(x=0.50, y=0.46), "กระดูกสันหลัง"),
        Part("skeleton", Marker(x=0.44, y=0.63), "กระดูกต้นขา"),
        Part("skeleton", Marker(x=0.43, y=0.85), "กระดูกหน้าแข้ง"),
        Part("skeleton", Marker(x=0.27, y=0.31), "กระดูกต้นแขน"),
        Part("skeleton", Marker(x=0.23, y=0.48), "กระดูกปลายแขน"),
        Part("skeleton", Marker(x=0.44, y=0.72), "กระดูกสะบ้า"),
        Part("skeleton", Marker(x=0.40, y=0.935), "กระดูกเท้า"),
    ]

    def parts(self) -> list[Part]:
        return self._PARTS
