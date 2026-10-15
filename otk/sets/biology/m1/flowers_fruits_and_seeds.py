"""โครงสร้างดอกและการเกิดผลและเมล็ด

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/12

Sets moved here from: science_wave_b5.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import contextual_scenario_question
from otk.sets._support.science_wave_b5 import (
    LEVEL,
    SEED_SCENARIOS,
    SUBJECT,
    TOPIC,
    _labelled,
    _statement_question,
)
from otk.sets._support.life_earth_diagrams import FLOWER_ALT, FLOWERS
from otk.sets._support.ms1_diagrams import diagram_question

PROVENANCE = Provenance("original")


class FlowerPart(NamedTuple):
    """One part of a flower and what it does."""
    name: str
    function: str


FLOWER_PARTS = (
    FlowerPart("กลีบเลี้ยง", "ห่อหุ้มและป้องกันดอกในขณะที่ยังตูมอยู่"),
    FlowerPart("กลีบดอก", "มีสีสันและกลิ่นสำหรับล่อแมลงให้มาช่วยถ่ายเรณู"),
    FlowerPart("อับเรณู", "เป็นที่สร้างและเก็บเรณู"),
    FlowerPart("ก้านชูอับเรณู", "ชูอับเรณูขึ้นไปอยู่ในตำแหน่งที่เหมาะแก่การถ่ายเรณู"),
    FlowerPart("ยอดเกสรเพศเมีย", "มีน้ำเหนียวสำหรับดักจับเรณูที่ปลิวหรือถูกพามา"),
    FlowerPart("ก้านเกสรเพศเมีย", "เป็นทางให้หลอดเรณูเจริญลงไปยังรังไข่"),
    FlowerPart("รังไข่", "ภายในมีออวุล และเจริญไปเป็นผลหลังการปฏิสนธิ"),
    FlowerPart("ออวุล", "ภายในมีเซลล์ไข่ และเจริญไปเป็นเมล็ดหลังการปฏิสนธิ"),
)


# Four statements true of each kind of flower. Both agents get the same number so
# either direction of the question has three wrongs to draw on.
INSECT_FLOWER_FACTS = (
    "กลีบดอกมีขนาดใหญ่และมีสีสันสดใสสะดุดตา",
    "มีกลิ่นหอมและมีต่อมน้ำหวานอยู่ภายในดอก",
    "เรณูมีผิวขรุขระหรือเหนียว จึงติดไปกับตัวแมลงได้",
    "สร้างเรณูในปริมาณไม่มากนัก เพราะมีตัวพาที่ค่อนข้างแม่นยำ",
)


WIND_FLOWER_FACTS = (
    "กลีบดอกมีขนาดเล็กหรือไม่มีกลีบดอกเลย",
    "ไม่มีสีสันสะดุดตาและไม่มีกลิ่นหอม",
    "เรณูมีขนาดเล็กและเบามาก จึงปลิวไปตามลมได้ไกล",
    "ยอดเกสรเพศเมียมักแผ่เป็นพู่หรือขนนกเพื่อดักเรณูที่ปลิวมา",
)


# (โครงสร้างก่อนการปฏิสนธิ, สิ่งที่เจริญไปเป็น)
AFTER_FERTILISATION = (
    ("รังไข่", "ผล"),
    ("ออวุล", "เมล็ด"),
    ("เซลล์ไข่ที่ปฏิสนธิแล้ว", "ต้นอ่อนที่อยู่ภายในเมล็ด"),
    ("ผนังของรังไข่", "เปลือกและเนื้อของผล"),
)


@question_type(
    "plant.flower_parts_foundation",
    display_name={"th": "ส่วนประกอบของดอกและหน้าที่"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class FlowerPartsFoundation(QuestionType):
    """Name a part's job, or the part that does a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(FLOWER_PARTS)
        others = [other for other in FLOWER_PARTS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” ทำหน้าที่ใดในดอก",
                correct=item.function,
                wrongs=tuple(other.function for other in others[:3]),
                hint="แยกก่อนว่าส่วนนั้นอยู่ในเกสรเพศผู้ เกสรเพศเมีย "
                     "หรือเป็นส่วนที่ห่อหุ้มอยู่ด้านนอก",
            )
        return _labelled(
            stem=f"ส่วนใดของดอกทำหน้าที่{item.function}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกส่วนที่ทำหน้าที่นั้นโดยตรง",
        )


@question_type(
    "plant.pollination_fluency",
    display_name={"th": "การถ่ายเรณูและการเปลี่ยนแปลงหลังการปฏิสนธิ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PollinationFluency(QuestionType):
    """Read a flower's features for its pollinator, and follow a part into the fruit.

    Two agents means the item cannot ask "แมลงหรือลม" directly. It offers four
    statements instead, each true of one kind of flower, so the learner has to
    attach the feature to the right agent.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            insect = rng.random() < 0.5
            return _statement_question(
                subject=("ดอกที่ถ่ายเรณูโดยแมลง" if insect
                         else "ดอกที่ถ่ายเรณูโดยลม"),
                mine=list(INSECT_FLOWER_FACTS if insect else WIND_FLOWER_FACTS),
                theirs=list(WIND_FLOWER_FACTS if insect else INSECT_FLOWER_FACTS),
                rng=rng,
                hint="ดอกที่ใช้แมลงต้องลงทุนกับสีและกลิ่นเพื่อเรียกตัวพา "
                     "ส่วนดอกที่ใช้ลมลงทุนกับจำนวนและน้ำหนักของเรณูแทน",
            )
        before, after = rng.choice(AFTER_FERTILISATION)
        others = [other for item, other in AFTER_FERTILISATION if other != after]
        rng.shuffle(others)
        return _labelled(
            stem=f"หลังการปฏิสนธิของพืชดอก “{before}” จะเจริญไปเป็นสิ่งใด",
            correct=after,
            wrongs=tuple(others[:3]),
            hint="รังไข่กับสิ่งที่อยู่ภายในรังไข่เจริญไปเป็นคนละส่วนของผลที่เรากิน",
        )


@question_type(
    "plant.seed_application",
    display_name={"th": "วิเคราะห์การถ่ายเรณู การเกิดผล การกระจายเมล็ด และการงอก"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class SeedApplication(QuestionType):
    """Read a fruit's shape, a bagged flower or a drowned seed for what it implies.

    ``ม.1/12`` runs from the flower through fertilisation to fruit, seed,
    dispersal and germination. Each item picks one link in that chain and states
    an observation that only holds if the link is understood.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, SEED_SCENARIOS,
            hint="ถามว่าลักษณะที่เห็นช่วยเรื่องใด: การเรียกตัวพา การเดินทางของเมล็ด "
                 "หรือการงอกเมื่อถึงที่หมาย",
            topic=TOPIC,
        )


@question_type(
    "plant.flower_diagram",
    display_name={"th": "ระบุส่วนประกอบของดอกจากภาพตัดตามยาว"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class FlowerDiagram(QuestionType):
    """A numbered flower cut lengthways: name a part, give its job, or find what becomes fruit or seed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(FLOWERS)
        part = rng.choice(FLOWER_PARTS)
        number = spec.number_of(part.name)
        hint = "ไล่จากนอกเข้าใน: กลีบเลี้ยง กลีบดอก เกสรเพศผู้ (อับเรณูบนก้านชู) แล้วเกสรเพศเมียตรงกลาง"
        kind = rng.randrange(3)
        if kind == 0:
            others = [p.name for p in FLOWER_PARTS if p is not part]
            rng.shuffle(others)
            return diagram_question(
                spec.asset_id, FLOWER_ALT,
                stem=f"จากภาพดอกไม้ ส่วนหมายเลข {number} คือส่วนใด",
                correct=part.name, wrongs=tuple(others[:4]),
                hint=hint, topic=TOPIC,
            )
        if kind == 1:
            return diagram_question(
                spec.asset_id, FLOWER_ALT,
                stem=f"จากภาพดอกไม้ ส่วนหมายเลข {number} ทำหน้าที่ใด",
                correct=part.function,
                wrongs=tuple(p.function for p in FLOWER_PARTS if p is not part),
                hint="ระบุชื่อส่วนจากตำแหน่งในภาพก่อน แล้วนึกถึงหน้าที่ของส่วนนั้น",
                topic=TOPIC,
            )
        becomes, grows_into = rng.choice((("รังไข่", "ผล"), ("ออวุล", "เมล็ด")))
        target = spec.number_of(becomes)
        return diagram_question(
            spec.asset_id, FLOWER_ALT,
            stem=f"จากภาพดอกไม้ หลังการปฏิสนธิ ส่วนหมายเลขใดจะเจริญไปเป็น{grows_into}",
            correct=f"หมายเลข {target}",
            wrongs=tuple(f"หมายเลข {n}" for n in range(1, len(spec.labelled) + 1) if n != target),
            hint="รังไข่เจริญไปเป็นผล ส่วนออวุลที่อยู่ภายในรังไข่เจริญไปเป็นเมล็ด",
            topic=TOPIC,
        )
