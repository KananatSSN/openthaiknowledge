"""ทิศทางการลำเลียงสารในพืช

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/10

Sets moved here from: science_wave_b4.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import (
    Concept,
    ConceptBankType,
    contextual_scenario_question,
    widen,
)
from otk.sets._support.science_wave_b4 import (
    DIRECTION_SCENARIOS,
    LEVEL,
    PHLOEM,
    SUBJECT,
    TOPIC,
    XYLEM,
    _labelled,
)

PROVENANCE = Provenance("original")


UPWARD = "ลำเลียงจากส่วนล่างขึ้นไปยังส่วนบน"


DOWNWARD = "ลำเลียงจากส่วนบนลงไปยังส่วนล่าง"


# The four labels a direction question can offer. Two vessels times two
# directions: a real space with exactly one right answer per journey, and no
# invented option.
DIRECTION_CHOICES = tuple(
    f"{tissue} {direction}"
    for tissue in (XYLEM, PHLOEM)
    for direction in (UPWARD, DOWNWARD)
)


class Journey(NamedTuple):
    """One substance moving between two named parts of the plant."""
    substance: str
    origin: str
    destination: str
    tissue: str
    direction: str


JOURNEYS = (
    Journey("น้ำที่รากดูดขึ้นมาจากดิน", "ราก", "ใบ", XYLEM, UPWARD),
    Journey("ธาตุอาหารที่ละลายอยู่ในน้ำในดิน", "ขนราก", "ยอดของลำต้น", XYLEM, UPWARD),
    Journey("น้ำที่ใช้ในการสังเคราะห์ด้วยแสง", "ราก", "เซลล์ในใบ", XYLEM, UPWARD),
    Journey("น้ำตาลที่ใบสร้างขึ้น", "ใบ", "รากที่อยู่ใต้ดิน", PHLOEM, DOWNWARD),
    Journey("น้ำตาลที่ใบสร้างขึ้น", "ใบ", "หัวใต้ดินที่กำลังสะสมอาหาร",
            PHLOEM, DOWNWARD),
    Journey("อาหารที่สะสมไว้ในหัวใต้ดิน", "หัวใต้ดิน", "ยอดอ่อนที่กำลังงอก",
            PHLOEM, UPWARD),
    Journey("น้ำตาลที่ใบด้านล่างสร้างขึ้น", "ใบด้านล่างของต้น",
            "ผลที่กำลังเจริญอยู่บนกิ่งด้านบน", PHLOEM, UPWARD),
)


@question_type(
    "plant.transport_direction_foundation",
    display_name={"th": "ทิศทางการลำเลียงน้ำและอาหารในพืช"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class TransportDirectionFoundation(ConceptBankType):
    """The rule each vessel follows, including the one that goes both ways."""

    ITEMS = widen([
        Concept(
            "ไซเล็มลำเลียงสารไปในทิศทางใด",
            "ไปในทิศทางเดียว คือจากรากขึ้นสู่ลำต้นและใบ",
            ("ไปในทิศทางเดียว คือจากใบลงสู่ลำต้นและราก",
             "ไปได้ทั้งขึ้นและลง ขึ้นกับว่าส่วนใดต้องการน้ำมากกว่า",
             "ไปในแนวขวางจากกลางลำต้นออกสู่เปลือกเท่านั้น"),
        ),
        Concept(
            "โฟลเอ็มลำเลียงอาหารไปในทิศทางใด",
            "ไปได้ทั้งขึ้นและลง จากแหล่งที่สร้างอาหารไปยังแหล่งที่ใช้หรือสะสมอาหาร",
            ("ไปในทิศทางเดียว คือจากใบลงสู่รากเสมอ เพราะรากเป็นแหล่งสะสมอาหารแห่งเดียว",
             "ไปในทิศทางเดียว คือจากรากขึ้นสู่ใบเสมอ",
             "ไม่มีทิศทางแน่นอน เพราะอาหารกระจายไปทั่วต้นพร้อมกันในทันทีทุกส่วน"),
        ),
        Concept(
            "แรงใดเป็นแรงหลักที่ดึงน้ำในไซเล็มขึ้นไปจนถึงยอดของต้นไม้สูง",
            "แรงดึงจากการคายน้ำที่ใบ ซึ่งดึงสายน้ำที่ต่อเนื่องกันในไซเล็มขึ้นไป",
            ("แรงดันที่รากอัดน้ำขึ้นไปเพียงอย่างเดียว",
             "แรงจากการเต้นของเซลล์ที่มีชีวิตในไซเล็มที่บีบน้ำขึ้นไปทีละช่วง",
             "แรงโน้มถ่วงที่ดึงน้ำจากดินขึ้นสู่ยอดของต้นไม้"),
        ),
        Concept(
            "“แหล่งสร้างอาหาร” ของพืชโดยทั่วไปคือส่วนใด",
            "ใบที่กำลังสังเคราะห์ด้วยแสง",
            ("รากที่กำลังดูดน้ำและธาตุอาหาร",
             "หัวใต้ดินที่กำลังสะสมอาหาร",
             "ผลที่กำลังเจริญเติบโต"),
        ),
        Concept(
            "เหตุใดโฟลเอ็มจึงลำเลียงอาหารขึ้นไปด้านบนได้ด้วย",
            "เพราะอาหารลำเลียงจากแหล่งสร้างไปแหล่งใช้ เช่น หัวใต้ดินส่งอาหารขึ้นไปเลี้ยงยอดอ่อน",
            ("เพราะโฟลเอ็มใช้แรงดึงจากการคายน้ำเช่นเดียวกับไซเล็ม อาหารจึงขึ้นไปพร้อมกับน้ำ",
             "เพราะอาหารมีน้ำหนักเบากว่าน้ำจึงลอยขึ้นไปเองได้ตามท่อโฟลเอ็มสู่ยอดอ่อน",
             "เพราะโฟลเอ็มเปลี่ยนหน้าที่ไปเป็นไซเล็มชั่วคราวเมื่อต้องลำเลียงขึ้น"),
        ),
        Concept(
            "การคายน้ำของพืชเกิดขึ้นที่ส่วนใดเป็นหลัก และเกี่ยวข้องกับการลำเลียงอย่างไร",
            "เกิดที่ปากใบ และทำให้เกิดแรงดึงที่ช่วยลำเลียงน้ำในไซเล็มขึ้นไปจากราก",
            ("เกิดที่ราก และทำให้เกิดแรงดันที่ดันน้ำขึ้นไปในโฟลเอ็มจนถึงใบ",
             "เกิดที่เปลือกของลำต้น และทำให้อาหารเคลื่อนลงสู่ราก",
             "เกิดที่ผล และช่วยดึงน้ำตาลจากใบมายังผล"),
        ),
    ], (
        ("ไปในทิศทางเดียว คือจากผลลงสู่ราก",
         "ไม่มีทิศทาง เพราะไซเล็มเก็บน้ำไว้นิ่ง ๆ"),
        ("ไปเฉพาะจากรากขึ้นสู่ผลเท่านั้น",
         "ไปทางเดียวกับไซเล็มเสมอ"),
        ("แรงลมที่พัดผ่านลำต้นดันน้ำขึ้นไป",
         "แรงจากโฟลเอ็มที่บีบตัวดันน้ำในไซเล็มขึ้นไป"),
        ("ดอกที่กำลังบาน",
         "เมล็ดที่กำลังพักตัว"),
        ("เพราะอาหารทั้งหมดถูกสร้างที่ราก",
         "เพราะแรงโน้มถ่วงดึงอาหารขึ้นไปด้านบน"),
        ("เกิดที่ดอก และทำให้เกิดแรงดันที่ดันเรณูออกมาจากอับเรณูสู่ยอดเกสร",
         "เกิดที่ไซเล็ม และทำให้อาหารเคลื่อนขึ้นสู่ยอด"),
    ))


@question_type(
    "plant.transport_direction_fluency",
    display_name={"th": "ระบุท่อลำเลียงและทิศทางของการเดินทางของสารในพืช"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class TransportDirectionFluency(QuestionType):
    """Given what moves and where from and to, name the vessel and the direction.

    The four choices are the two vessels crossed with the two directions, so the
    space is real and closed. The rows deliberately include sugar travelling
    *up* — from a tuber to a sprouting shoot — because "โฟลเอ็มลงเสมอ" is the
    misconception that makes ``ม.1/10`` worth asking at all.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        journey = rng.choice(JOURNEYS)
        correct = f"{journey.tissue} {journey.direction}"
        if rng.random() < 0.5:
            # The other way round: a vessel and direction, and the journey that fits it.
            def trip(j: Journey) -> str:
                return f"“{j.substance}” จาก{j.origin}ไปยัง{j.destination}"
            others = [trip(j) for j in JOURNEYS
                      if (j.tissue, j.direction) != (journey.tissue, journey.direction)]
            return _labelled(
                stem=f"การลำเลียงใดต่อไปนี้เกิดใน{journey.tissue} และ{journey.direction}",
                correct=trip(journey),
                wrongs=tuple(others),
                hint="น้ำและธาตุอาหารเดินทางในไซเล็มขึ้นเท่านั้น ส่วนอาหารเดินทางในโฟลเอ็ม"
                     "จากแหล่งสร้างหรือแหล่งสะสมไปยังแหล่งที่ใช้",
            )
        return _labelled(
            stem=f"“{journey.substance}” เดินทางจาก{journey.origin}"
                 f"ไปยัง{journey.destination} การลำเลียงนี้เกิดในท่อใดและทิศทางใด",
            correct=correct,
            wrongs=tuple(label for label in DIRECTION_CHOICES if label != correct),
            hint="ดูก่อนว่าสิ่งที่เดินทางคือน้ำหรืออาหาร แล้วจึงดูว่าจุดปลายทาง"
                 "อยู่สูงหรือต่ำกว่าจุดเริ่มต้น",
        )


@question_type(
    "plant.transport_direction_application",
    display_name={"th": "อธิบายทิศทางการลำเลียงสารในพืชจากสถานการณ์จริง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class TransportDirectionApplication(QuestionType):
    """Work out which way things moved from what happened to the plant.

    ``ม.1/10`` asks for a diagram, which an item like this cannot require; one
    scenario therefore asks which diagram would be correct, and the rest ask for
    the reasoning a correct diagram would encode.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, DIRECTION_SCENARIOS,
            hint="ถามว่าแหล่งสร้างอาหารอยู่ที่ใดและแหล่งที่ใช้อยู่ที่ใด "
                 "ทิศทางในโฟลเอ็มขึ้นกับสองจุดนี้ ไม่ใช่ขึ้นกับแรงโน้มถ่วง",
            topic=TOPIC,
        )


# More items: the set drew from six, so a learner met them all in a few tries.
TransportDirectionFoundation.ITEMS = [*TransportDirectionFoundation.ITEMS,
    Concept('รากดูดน้ำจากดินเข้าสู่เซลล์ขนรากด้วยกระบวนการใด',
            'ออสโมซิส เพราะภายในเซลล์ขนรากมีความเข้มข้นของสารละลายสูงกว่าน้ำในดิน',
            ('การแพร่ของน้ำจากเซลล์ขนรากออกไปสู่ดินที่มีน้ำน้อยกว่า', 'การคายน้ำที่ราก ซึ่งดึงน้ำจากดินเข้ามาทางเปลือกของราก', 'ออสโมซิส เพราะน้ำในดินมีความเข้มข้นของสารละลายสูงกว่าภายในเซลล์', 'การลำเลียงในโฟลเอ็ม ซึ่งดูดน้ำจากดินขึ้นไปพร้อมกับอาหาร', 'การสังเคราะห์ด้วยแสงที่ราก ซึ่งสร้างน้ำขึ้นใหม่ภายในเซลล์ขนราก')),
    Concept('“แหล่งใช้อาหาร” ของพืชหมายถึงส่วนใด',
            'ส่วนที่กำลังเจริญหรือสะสมอาหาร เช่น ยอดอ่อน ราก ผล และหัว',
            ('ใบที่โตเต็มที่และกำลังสังเคราะห์ด้วยแสงได้ดีที่สุด', 'เฉพาะรากที่อยู่ในดิน เพราะอาหารไหลลงได้ทางเดียว', 'ไซเล็มที่ลำเลียงน้ำและธาตุอาหารขึ้นจากรากสู่ใบ', 'ปากใบที่เป็นทางเข้าออกของแก๊สและไอน้ำ', 'ดินรอบรากที่พืชส่งอาหารออกไปเก็บไว้ใช้ภายหลัง')),
    Concept('ธาตุอาหารที่รากดูดขึ้นมาถูกลำเลียงไปยังใบได้อย่างไร',
            'ถูกลำเลียงไปพร้อมกับน้ำในไซเล็ม ขึ้นสู่ลำต้นและใบ',
            ('ถูกลำเลียงไปในโฟลเอ็มพร้อมกับน้ำตาลจากใบ', 'แพร่ผ่านเปลือกของลำต้นขึ้นไปทีละเซลล์จนถึงใบ', 'ถูกเก็บไว้ที่รากทั้งหมด ใบจึงไม่ได้รับธาตุอาหารเลย', 'ระเหยเป็นไอจากรากแล้วไปควบแน่นที่ใบ', 'ถูกลำเลียงในไซเล็มลงจากใบมาที่รากก่อน แล้วจึงกลับขึ้นไป')),
    Concept('เหตุใดในวันที่อากาศชื้นมากและไม่มีลม พืชจึงลำเลียงน้ำขึ้นได้ช้าลง',
            'การคายน้ำเกิดได้น้อย แรงดึงที่ใบจึงน้อยลง น้ำในไซเล็มจึงเคลื่อนช้าลง',
            ('ความชื้นทำให้รากหยุดดูดน้ำทันที น้ำจึงไม่เข้าสู่ไซเล็มเลย', 'อากาศชื้นทำให้โฟลเอ็มลำเลียงน้ำแทนไซเล็ม จึงช้ากว่าปกติ', 'ไม่มีลมทำให้แสงน้อย พืชจึงหยุดลำเลียงทุกอย่างจนกว่าจะมีลม', 'ความชื้นทำให้ไซเล็มอุดตัน น้ำจึงไหลย้อนกลับลงไปที่ราก', 'อากาศชื้นทำให้ปากใบเปิดกว้างที่สุด น้ำจึงถูกดึงขึ้นช้าลง')),
]
