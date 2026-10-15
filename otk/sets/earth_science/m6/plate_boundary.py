"""แนวรอยต่อของแผ่นธรณี

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/3

Sets moved here from: science_wave_c22.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c13 import _swapped, _swaps
from otk.sets._support.science_wave_c22 import BOUNDARY_SCENARIOS
from otk.sets._support.life_earth_diagrams import PLATE_ALT, PLATE_PICTURES
from otk.sets._support.ms1_diagrams import diagram_question

PROVENANCE = Provenance("original")


BOUNDARY_TOPIC = "แนวรอยต่อของแผ่นธรณี"


class Boundary(NamedTuple):
    """A plate boundary: how the plates move, and a real place that shows it."""
    name: str
    motion: str
    example: str


BOUNDARIES = (
    Boundary("แนวแผ่นธรณีแยกตัว", "แผ่นธรณีเคลื่อนที่ออกจากกัน แมกมาดันขึ้นมาเกิดเป็นพื้นมหาสมุทรใหม่",
             "สันเขากลางมหาสมุทรแอตแลนติก"),
    Boundary("แนวแผ่นธรณีเคลื่อนที่เข้าหากัน", "แผ่นธรณีชนกัน แผ่นที่หนาแน่นกว่ามุดลง หรือแผ่นทวีปชนกันจนยกตัวเป็นเทือกเขา",
             "เทือกเขาหิมาลัยระหว่างอินเดียกับทวีปเอเชีย"),
    Boundary("แนวแผ่นธรณีเคลื่อนที่ผ่านกัน", "แผ่นธรณีเลื่อนผ่านกันในแนวราบ เกิดรอยเลื่อนขนาดใหญ่",
             "รอยเลื่อนแซนแอนเดรียสในรัฐแคลิฟอร์เนีย สหรัฐอเมริกา"),
)


CAUSE = ("การพาความร้อนของเนื้อโลกในชั้นฐานธรณีภาค ซึ่งพาแผ่นธรณีด้านบนให้เคลื่อนที่")


CAUSE_DECOYS = (
    "แรงดึงดูดของดวงจันทร์ที่ทำให้เกิดน้ำขึ้นน้ำลง ซึ่งลากแผ่นธรณีให้เคลื่อนตามไปด้วย",
    "ลมที่พัดผ่านผิวโลกอย่างต่อเนื่อง",
    "น้ำหนักของน้ำทะเลที่กดทับแผ่นธรณี",
    "การหมุนรอบดวงอาทิตย์ของโลกที่เหวี่ยงแผ่นธรณีออกไป",
    "แผ่นดินไหวที่เกิดก่อนแล้วผลักแผ่นธรณีให้เคลื่อน",
    "ความร้อนจากแสงอาทิตย์ที่ทำให้หินบนผิวโลกขยายตัวและดันแผ่นธรณีให้เลื่อนออกไป",
)


# More wordings of each motion and more places each boundary leaves its mark.
# Each still describes its own boundary only.
MORE_MOTIONS = {
    "แนวแผ่นธรณีแยกตัว": (
        "แผ่นธรณีสองแผ่นแยกห่างจากกัน หินหนืดแทรกขึ้นมาเย็นตัวเป็นเปลือกโลกใหม่",
        "แผ่นธรณีถูกดึงให้แยกออก เกิดสันเขาและหุบเขาทรุดตามแนวที่แยก",
    ),
    "แนวแผ่นธรณีเคลื่อนที่เข้าหากัน": (
        "แผ่นธรณีสองแผ่นเคลื่อนมาปะทะกัน แผ่นที่หนักกว่ามุดลงหรือเปลือกโลกยกตัวเป็นภูเขา",
        "แผ่นธรณีบีบอัดเข้าหากัน เปลือกโลกโค้งงอยกสูงเป็นเทือกเขาหรือเกิดร่องลึกก้นสมุทร",
    ),
    "แนวแผ่นธรณีเคลื่อนที่ผ่านกัน": (
        "แผ่นธรณีสองแผ่นเคลื่อนสวนทางกันในแนวราบ โดยไม่มีการสร้างหรือทำลายเปลือกโลก",
        "แผ่นธรณีเสียดสีกันด้านข้าง เกิดรอยเลื่อนตามแนวระดับและแผ่นดินไหวบ่อย",
    ),
}


MORE_EXAMPLES = {
    "แนวแผ่นธรณีแยกตัว": ("หุบเขาทรุดแอฟริกาตะวันออกที่แผ่นทวีปกำลังแยกออกจากกัน", "ประเทศไอซ์แลนด์ที่ตั้งอยู่บนสันเขากลางมหาสมุทร"),
    "แนวแผ่นธรณีเคลื่อนที่เข้าหากัน": ("ร่องลึกก้นสมุทรมาเรียนาและหมู่เกาะภูเขาไฟใกล้เคียง",
                                     "เทือกเขาแอนดีสและภูเขาไฟตามชายฝั่งทวีปอเมริกาใต้"),
    "แนวแผ่นธรณีเคลื่อนที่ผ่านกัน": ("รอยเลื่อนอัลไพน์ในประเทศนิวซีแลนด์", "รอยเลื่อนสะกายที่พาดผ่านตอนกลางของประเทศเมียนมา"),
}


NOT_A_BOUNDARY = ("ทะเลทรายสะฮาราที่อยู่กลางแผ่นทวีปแอฟริกาห่างจากรอยต่อ", "ที่ราบภาคกลางของประเทศไทย",
                  "ทุ่งหญ้าสเตปป์ที่อยู่กลางทวีปเอเชียห่างจากขอบแผ่นธรณี")


def _example(rng: Random, boundary) -> str:
    return rng.choice((boundary.example, *MORE_EXAMPLES[boundary.name]))


def _motion(rng: Random, boundary) -> str:
    return rng.choice((boundary.motion, *MORE_MOTIONS[boundary.name]))


def _boundaries(motions: list[str]) -> str:
    return " / ".join(f"{b.name}: {m}" for b, m in zip(BOUNDARIES, motions))


@question_type(
    "geo.plate_boundary_foundation",
    display_name={"th": "สาเหตุการเคลื่อนที่ของแผ่นธรณีและตัวอย่างหลักฐาน"},
    level=UPPER_SIX, subject=SUBJECT, topic=BOUNDARY_TOPIC,
)
class PlateBoundaryFoundation(QuestionType):
    """Identify the cause, or give the evidence a boundary leaves — two free verbs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return _labelled(
                stem="สาเหตุหลักที่ทำให้แผ่นธรณีเคลื่อนที่คืออะไร",
                correct=CAUSE,
                wrongs=tuple(CAUSE_DECOYS),
                hint="นึกถึงความร้อนภายในโลกที่ทำให้เนื้อโลกไหลวน",
                topic=BOUNDARY_TOPIC,
            )
        boundary = rng.choice(BOUNDARIES)
        others = [other for other in BOUNDARIES if other.name != boundary.name]
        return _labelled(
            stem=f"ข้อใดเป็นตัวอย่างหลักฐานทางธรณีวิทยาที่พบตาม{boundary.name}",
            correct=_example(rng, boundary),
            wrongs=tuple(_example(rng, other) for other in others) + (rng.choice(NOT_A_BOUNDARY),),
            hint="นึกว่าแผ่นธรณีแยกออก ชนกัน หรือเลื่อนผ่านกัน แล้วเกิดลักษณะใดบนผิวโลก",
            topic=BOUNDARY_TOPIC,
        )


@question_type(
    "geo.plate_boundary_fluency",
    display_name={"th": "อธิบายรูปแบบแนวรอยต่อของแผ่นธรณี"},
    level=UPPER_SIX, subject=SUBJECT, topic=BOUNDARY_TOPIC,
)
class PlateBoundaryFluency(QuestionType):
    """Describe all three boundary patterns in one answer; each wrong choice swaps two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        motions = [_motion(rng, boundary) for boundary in BOUNDARIES]
        return _labelled(
            stem="ข้อใดอธิบายรูปแบบแนวรอยต่อของแผ่นธรณีทั้งสามแบบที่สัมพันธ์กับการเคลื่อนที่ของแผ่นธรณีได้ถูกต้องทั้งหมด",
            correct=_boundaries(motions),
            wrongs=tuple(_boundaries(_swapped(motions, i, j)) for i, j in _swaps(rng, 3, 3)),
            hint="แยกออกเกิดพื้นมหาสมุทรใหม่ ชนกันเกิดการมุดหรือเทือกเขา เลื่อนผ่านเกิดรอยเลื่อน",
            topic=BOUNDARY_TOPIC,
        )


@question_type(
    "geo.plate_boundary_application",
    display_name={"th": "วิเคราะห์ปรากฏการณ์ตามแนวรอยต่อของแผ่นธรณี"},
    level=UPPER_SIX, subject=SUBJECT, topic=BOUNDARY_TOPIC,
)
class PlateBoundaryApplication(QuestionType):
    """Japan's volcanoes, the rising Himalaya, and why Thailand still shakes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, BOUNDARY_SCENARIOS,
            hint="หาว่าพื้นที่นั้นอยู่ใกล้แนวรอยต่อแบบใด แล้วเชื่อมกับการเคลื่อนที่ของแผ่นธรณี",
        ), BOUNDARY_TOPIC)


@question_type(
    "geo.plate_boundary_diagram",
    display_name={"th": "ระบุแนวรอยต่อของแผ่นธรณีจากภาพ"},
    level=UPPER_SIX, subject=SUBJECT, topic=BOUNDARY_TOPIC,
)
class PlateBoundaryDiagram(QuestionType):
    """Read the arrows of a drawn boundary: name it, give a real place like it, or say how the plates move."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(PLATE_PICTURES)
        boundary = next(b for b in BOUNDARIES if b.name == spec.boundary)
        others = [b for b in BOUNDARIES if b is not boundary]
        hint = "ดูลูกศร: ออกจากกันคือแยกตัว เข้าหากันคือเคลื่อนที่เข้าหากัน และสวนกันในแนวราบคือเคลื่อนที่ผ่านกัน"
        kind = rng.randrange(3)
        if kind == 0:
            return diagram_question(
                spec.asset_id, PLATE_ALT,
                stem="ภาพนี้แสดงแนวรอยต่อของแผ่นธรณีแบบใด",
                correct=boundary.name,
                wrongs=tuple(b.name for b in others) + ("แนวที่แผ่นธรณีไม่เคลื่อนที่",),
                hint=hint, topic=BOUNDARY_TOPIC,
            )
        if kind == 1:
            return diagram_question(
                spec.asset_id, PLATE_ALT,
                stem="สถานที่ใดเป็นตัวอย่างของแนวรอยต่อแบบที่แสดงในภาพนี้",
                correct=boundary.example,
                wrongs=tuple(b.example for b in others) + (NOT_A_BOUNDARY[0],),
                hint=hint, topic=BOUNDARY_TOPIC,
            )
        return diagram_question(
            spec.asset_id, PLATE_ALT,
            stem="ข้อใดอธิบายการเคลื่อนที่ของแผ่นธรณีในภาพนี้ได้ถูกต้อง",
            correct=boundary.motion,
            wrongs=tuple(b.motion for b in others)
                   + ("แผ่นธรณีทั้งสองอยู่นิ่ง ไม่เคลื่อนที่ จึงไม่มีการเปลี่ยนแปลงที่รอยต่อ",),
            hint=hint, topic=BOUNDARY_TOPIC,
        )
