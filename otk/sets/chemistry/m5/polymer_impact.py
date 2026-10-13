"""ผลกระทบของผลิตภัณฑ์พอลิเมอร์ต่อสิ่งมีชีวิตและสิ่งแวดล้อม

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/19

Sets moved here from: science_wave_e6.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e6 import SUBJECT, _labelled

PROVENANCE = Provenance("original")


TOPIC_POLYMER_IMPACT = "ผลกระทบของผลิตภัณฑ์พอลิเมอร์ต่อสิ่งมีชีวิตและสิ่งแวดล้อม"


IMPACT, MITIGATION = "ผลกระทบต่อสิ่งมีชีวิตหรือสิ่งแวดล้อม", "แนวทางป้องกันหรือแก้ไขผลกระทบ"


class PolymerImpactItem(NamedTuple):
    text: str
    kind: str


POLYMER_IMPACT_ITEMS: tuple[PolymerImpactItem, ...] = (
    PolymerImpactItem("ถุงพลาสติกที่ทิ้งในทะเลทำให้สัตว์ทะเลกินเข้าไปและตายจากการอุดตันทางเดินอาหาร",
                       IMPACT),
    PolymerImpactItem("ไมโครพลาสติกที่แตกตัวจากพลาสติกสะสมในห่วงโซ่อาหารและปนเปื้อนในร่างกายมนุษย์",
                       IMPACT),
    PolymerImpactItem("ขยะพลาสติกที่ไม่ย่อยสลายสะสมในหลุมฝังกลบเป็นเวลานานหลายร้อยปี",
                       IMPACT),
    PolymerImpactItem("การคัดแยกขยะพลาสติกเพื่อนำไปรีไซเคิลช่วยลดปริมาณขยะพอลิเมอร์ที่ตกค้างในสิ่งแวดล้อม",
                       MITIGATION),
    PolymerImpactItem("การใช้พลาสติกที่ย่อยสลายได้ทางชีวภาพ (bioplastic) ทดแทนพลาสติกทั่วไป",
                       MITIGATION),
    PolymerImpactItem("การลดการใช้ผลิตภัณฑ์พลาสติกแบบใช้ครั้งเดียวทิ้งในชีวิตประจำวัน",
                       MITIGATION),
    PolymerImpactItem("การเผาขยะพลาสติกกลางแจ้งปล่อยควันพิษและสารก่อมะเร็งสู่อากาศ", IMPACT),
    PolymerImpactItem("ขยะพลาสติกอุดตันท่อระบายน้ำทำให้เกิดน้ำท่วมขังในเมือง", IMPACT),
    PolymerImpactItem("เศษอวนพลาสติกที่ทิ้งในทะเลพันรัดเต่าทะเลจนบาดเจ็บ", IMPACT),
    PolymerImpactItem("การนำขวดพลาสติกกลับมาใช้ซ้ำหรือดัดแปลงเป็นของใช้", MITIGATION),
    PolymerImpactItem("การพกถุงผ้าและแก้วน้ำส่วนตัวแทนถุงและแก้วพลาสติก", MITIGATION),
    PolymerImpactItem("การเก็บขยะพลาสติกตามชายหาดและแหล่งน้ำ", MITIGATION),
)


IMPACT_FACTS = (
    ("การใช้ผลิตภัณฑ์พอลิเมอร์อย่างไม่เหมาะสมและไม่มีการจัดการหลังใช้งานก่อให้เกิดผลกระทบต่อสิ่งมีชีวิตและสิ่งแวดล้อมหรือไม่",
     "ก่อให้เกิดผลกระทบต่อทั้งสิ่งมีชีวิตและสิ่งแวดล้อม",
     ("ไม่ก่อให้เกิดผลกระทบเลย", "ก่อให้เกิดประโยชน์เท่านั้น",
      "ขึ้นอยู่กับชนิดของพอลิเมอร์เท่านั้น ไม่เกี่ยวกับการใช้งาน",
      "ก่อผลกระทบเฉพาะกับพืช ไม่เกี่ยวกับสัตว์", "ก่อผลกระทบเฉพาะเมื่อพลาสติกยังใหม่",
      "ก่อให้เกิดผลกระทบต่อสิ่งแวดล้อม แต่ไม่กระทบสิ่งมีชีวิตใด",
      "ก่อให้เกิดผลกระทบต่อสิ่งมีชีวิต แต่ไม่กระทบสิ่งแวดล้อมใด")),
    ("เหตุใดขยะพลาสติกส่วนใหญ่จึงสะสมอยู่ในสิ่งแวดล้อมได้นาน",
     "พอลิเมอร์ส่วนใหญ่เป็นโมเลกุลขนาดใหญ่ที่จุลินทรีย์ย่อยสลายได้ยาก",
     ("พลาสติกละลายน้ำได้ดีจึงกระจายไปทั่ว", "พลาสติกย่อยสลายหมดภายในไม่กี่วัน แต่มีการทิ้งเพิ่มขึ้นทุกวัน",
      "พอลิเมอร์ส่วนใหญ่เป็นโมเลกุลขนาดเล็กที่ละลายน้ำได้ จึงแทรกซึมลงดินได้ลึก", "พลาสติกระเหยกลายเป็นไอได้ง่าย",
      "พลาสติกเปลี่ยนเป็นดินได้เองเมื่อโดนแดด",
      "พอลิเมอร์ส่วนใหญ่เป็นโมเลกุลขนาดใหญ่ที่จุลินทรีย์ย่อยสลายหมดได้ในไม่กี่วัน")),
    ("ไมโครพลาสติกคืออะไร",
     "ชิ้นพลาสติกขนาดเล็กมากที่แตกตัวจากพลาสติกชิ้นใหญ่หรือถูกผลิตขึ้นให้มีขนาดเล็ก",
     ("พลาสติกชนิดใหม่ที่ออกแบบให้ย่อยสลายได้ทันทีเมื่อโดนน้ำหรือแสงแดด", "จุลินทรีย์ขนาดเล็กมากที่ย่อยพลาสติกชิ้นใหญ่ให้แตกเป็นชิ้นเล็กได้",
      "พลาสติกที่ผลิตจากพืชทั้งหมด", "แก๊สและฝุ่นละอองขนาดเล็กมากที่เกิดขึ้นจากการเผาขยะพลาสติกกลางแจ้ง", "ชิ้นโลหะขนาดเล็กมากที่ผสมอยู่ในเนื้อพลาสติกเพื่อให้พลาสติกแข็งแรงและทนทานขึ้น")),
    ("แนวทางใดช่วยลดผลกระทบของผลิตภัณฑ์พอลิเมอร์ได้ตรงจุดที่สุด",
     "ลดการใช้ ใช้ซ้ำ และคัดแยกพลาสติกเพื่อรีไซเคิล",
     ("เผาขยะพลาสติกกลางแจ้งให้หมดไป", "ทิ้งพลาสติกลงทะเลให้คลื่นพัดไป", "ฝังขยะพลาสติกไว้ใต้ดินในสวนบ้านให้ย่อยสลายเอง",
      "ใช้พลาสติกแบบใช้ครั้งเดียวทิ้งให้มากขึ้น", "ทิ้งพลาสติกรวมกับขยะเศษอาหาร",
      "ใช้ถุงพลาสติกใบใหม่ทุกครั้ง แล้วทิ้งใบเก่ารวมกับขยะทั่วไป")),
)


@question_type(
    "chem.polymer_impact_foundation",
    display_name={"th": "การใช้ผลิตภัณฑ์พอลิเมอร์อย่างไม่เหมาะสมก่อให้เกิดผลกระทบหรือไม่"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_POLYMER_IMPACT,
)
class PolymerImpactFoundation(QuestionType):
    """A general fact about polymer waste — not yet classifying a named example."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(IMPACT_FACTS)
        return _labelled(
            stem=stem,
            correct=correct,
            wrongs=wrongs,
            topic=TOPIC_POLYMER_IMPACT,
            hint="พอลิเมอร์ส่วนใหญ่ย่อยสลายเองตามธรรมชาติได้ยาก จึงสะสมและก่อผลกระทบต่อสิ่งมีชีวิตและสิ่งแวดล้อมหากจัดการไม่ถูกต้อง",
        )


@question_type(
    "chem.polymer_impact_fluency",
    display_name={"th": "ข้อความนี้เป็นผลกระทบหรือแนวทางป้องกัน/แก้ไข"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_POLYMER_IMPACT,
)
class PolymerImpactFluency(QuestionType):
    """Classify one named example directly — the whole ม.5/19 indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(POLYMER_IMPACT_ITEMS)
        other = MITIGATION if item.kind == IMPACT else IMPACT
        return _labelled(
            stem=f"ข้อความนี้เป็นผลกระทบหรือแนวทางป้องกัน/แก้ไข: \"{item.text}\"",
            correct=item.kind,
            wrongs=(other, "ไม่เกี่ยวข้องกับผลิตภัณฑ์พอลิเมอร์", "เป็นทั้งผลกระทบและแนวทางแก้ไขพร้อมกัน",
                    "เป็นสมบัติทางกายภาพของพอลิเมอร์", "เป็นขั้นตอนการผลิตพอลิเมอร์ในโรงงาน"),
            topic=TOPIC_POLYMER_IMPACT,
            hint="ผลกระทบอธิบายความเสียหายที่เกิดขึ้นแล้ว ส่วนแนวทางป้องกัน/แก้ไขเสนอวิธีลดหรือหยุดความเสียหายนั้น",
        )


@question_type(
    "chem.polymer_impact_application",
    display_name={"th": "ข้อความในข้อใดจัดอยู่ในหมวดที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_POLYMER_IMPACT,
)
class PolymerImpactApplication(QuestionType):
    """Reverse direction: given the category, pick the matching example."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice((IMPACT, MITIGATION))
        same = [item for item in POLYMER_IMPACT_ITEMS if item.kind == kind]
        other = [item for item in POLYMER_IMPACT_ITEMS if item.kind != kind]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        return _labelled(
            stem=f"ข้อความในข้อใดต่อไปนี้เป็นตัวอย่างของ{kind}จากผลิตภัณฑ์พอลิเมอร์",
            correct=correct.text,
            wrongs=tuple(w.text for w in wrongs),
            topic=TOPIC_POLYMER_IMPACT,
            hint="ผลกระทบอธิบายความเสียหายที่เกิดขึ้นแล้ว ส่วนแนวทางป้องกัน/แก้ไขเสนอวิธีลดหรือหยุดความเสียหายนั้น",
        )


# More rows: the set drew from four or five, so a learner met them all in a
# few tries. Every added row asks something the others do not.
IMPACT_FACTS += (
    ('เหตุใดการเผาพลาสติกพีวีซีกลางแจ้งจึงเป็นอันตราย',
     'เกิดแก๊สพิษและสารที่มีคลอรีน เช่น ไดออกซิน',
     ('เกิดเพียงไอน้ำที่ไม่มีพิษใด ๆ เลย', 'เกิดแก๊สออกซิเจนบริสุทธิ์จำนวนมาก', 'ไม่เกิดควันหรือแก๊สใด ๆ ออกมา',
      'ทำให้อากาศรอบบริเวณสะอาดขึ้นกว่าเดิม', 'เปลี่ยนพลาสติกให้กลายเป็นปุ๋ยบำรุงดิน')),
    ('พลาสติกย่อยสลายได้ทางชีวภาพ เช่น พอลิแล็กติกแอซิด มีข้อจำกัดใด',
     'ต้องหมักในสภาวะที่เหมาะสมจึงจะย่อยได้เร็ว',
     ('ย่อยสลายได้ทันทีทุกที่โดยไม่มีข้อจำกัด', 'ไม่ย่อยสลายเลยเหมือนพลาสติกทั่วไปทุกชนิด',
      'ใช้ซ้ำได้ไม่จำกัดจำนวนครั้งโดยไม่เสื่อม', 'ผลิตได้จากน้ำมันดิบเท่านั้นไม่มีทางอื่น',
      'อันตรายกว่าพลาสติกทั่วไปในทุกกรณี')),
    ('ขยะพลาสติกในทะเลส่งผลต่อสัตว์ทะเลอย่างไร',
     'สัตว์กินเข้าไปหรือติดพันจนบาดเจ็บหรือตาย',
     ('ช่วยเป็นอาหารเสริมให้สัตว์ทะเลเติบโต', 'ไม่มีผลใด ๆ ต่อสัตว์ที่อาศัยในทะเล',
      'ทำให้น้ำทะเลกลายเป็นน้ำจืดในระยะยาว', 'ทำให้ปะการังเติบโตเร็วขึ้นเป็นสองเท่า',
      'ทำให้ปลาในทะเลมีจำนวนเพิ่มมากขึ้น')),
    ('ตัวเลขในสัญลักษณ์รีไซเคิลบนบรรจุภัณฑ์พลาสติกบอกอะไร',
     'ชนิดของพลาสติก เพื่อช่วยคัดแยก',
     ('จำนวนครั้งที่ใช้ซ้ำได้', 'อายุการใช้งานเป็นปี', 'ราคาของพลาสติก',
      'จำนวนวันที่ย่อยสลาย', 'เฉดสีของพลาสติก')),
)
