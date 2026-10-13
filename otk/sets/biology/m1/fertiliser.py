"""การเลือกใช้ปุ๋ยให้เหมาะกับพืช

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/15

Sets moved here from: science_wave_b6.
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
from otk.sets._support.science_wave_b6 import (
    FERTILISER_SCENARIOS,
    LEVEL,
    SUBJECT,
    TOPIC,
    _labelled,
)

PROVENANCE = Provenance("original")


NITROGEN, PHOSPHORUS, POTASSIUM, BALANCED = "N", "P", "K", "balanced"


# What each emphasis is *for*, in the words a purpose question uses.
EMPHASIS_PURPOSE = {
    NITROGEN: "เร่งการเจริญของใบและลำต้น",
    PHOSPHORUS: "เร่งการเจริญของรากและการออกดอก",
    POTASSIUM: "เพิ่มความแข็งแรงของลำต้นและคุณภาพของผล",
    BALANCED: "บำรุงต้นโดยรวมอย่างสมดุลในระยะแรกปลูก",
}


class Fertiliser(NamedTuple):
    """One bag: its N-P-K numbers and which nutrient it leads with."""
    formula: str
    emphasis: str


FERTILISERS = (
    Fertiliser("46-0-0", NITROGEN),
    Fertiliser("21-0-0", NITROGEN),
    Fertiliser("0-46-0", PHOSPHORUS),
    Fertiliser("12-24-12", PHOSPHORUS),
    Fertiliser("0-0-60", POTASSIUM),
    Fertiliser("13-13-21", POTASSIUM),
    Fertiliser("15-15-15", BALANCED),
    Fertiliser("16-16-16", BALANCED),
)


@question_type(
    "plant.fertiliser_foundation",
    display_name={"th": "ตัวเลขบนถุงปุ๋ยและชนิดของปุ๋ย"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class FertiliserFoundation(ConceptBankType):
    """What the numbers mean, before any bag is chosen.

    A learner who cannot read ``15-15-15`` cannot choose between two bags, so
    this set is entirely about reading the label and telling the two kinds of
    fertiliser apart.
    """

    ITEMS = widen([
        Concept(
            "ตัวเลขสามตัวบนถุงปุ๋ย เช่น 15-15-15 บอกอะไร",
            "สัดส่วนของธาตุไนโตรเจน ฟอสฟอรัส และโพแทสเซียมตามลำดับ",
            ("สัดส่วนของน้ำ ดิน และอินทรียวัตถุที่ผสมอยู่ในปุ๋ย",
             "จำนวนครั้งที่ควรใส่ปุ๋ยต่อเดือน ต่อฤดู และต่อปี",
             "ราคาต่อกิโลกรัม น้ำหนักสุทธิ และอายุการเก็บรักษาของปุ๋ย"),
        ),
        Concept(
            "ปุ๋ยสูตร 46-0-0 มีธาตุอาหารใดสูงที่สุด",
            "ไนโตรเจน",
            ("ฟอสฟอรัส", "โพแทสเซียม", "แคลเซียม"),
        ),
        Concept(
            "ปุ๋ยอินทรีย์ต่างจากปุ๋ยเคมีอย่างไร",
            "ปุ๋ยอินทรีย์ได้จากซากพืชซากสัตว์ ปล่อยธาตุอาหารช้าและช่วยปรับปรุงดิน ส่วนปุ๋ยเคมีเข้มข้นและออกฤทธิ์เร็วกว่า",
            ("ปุ๋ยอินทรีย์ได้จากแร่ในโรงงาน ให้ธาตุอาหารเข้มข้นและออกฤทธิ์เร็ว ส่วนปุ๋ยเคมีได้จากซากพืชซากสัตว์",
             "ปุ๋ยอินทรีย์ไม่มีธาตุอาหารเลย มีเพียงอินทรียวัตถุที่ช่วยอุ้มน้ำ",
             "ปุ๋ยเคมีช่วยปรับปรุงโครงสร้างของดินได้ดีกว่าปุ๋ยอินทรีย์ เพราะมีธาตุอาหารเข้มข้นกว่า"),
        ),
        Concept(
            "การใส่ปุ๋ยเคมีมากเกินความจำเป็นก่อผลเสียอย่างไร",
            "ทำให้ดินเค็มจนรากดูดน้ำยากและพืชเหี่ยว ส่วนที่เหลือยังถูกชะลงแหล่งน้ำ",
            ("ทำให้พืชโตเร็วเกินไปจนออกดอกก่อนกำหนดเสมอ",
             "ทำให้ดินมีอินทรียวัตถุมากเกินไปจนรากขาดอากาศและเน่าตาย",
             "ไม่มีผลเสียใด เพราะพืชจะดูดเฉพาะปริมาณที่ต้องการเท่านั้น"),
        ),
        Concept(
            "เหตุใดจึงควรตรวจวิเคราะห์ดินก่อนเลือกซื้อปุ๋ย",
            "เพื่อให้รู้ว่าดินขาดธาตุใด แล้วเลือกสูตรที่เติมเฉพาะธาตุนั้น ไม่สิ้นเปลืองและไม่มากเกินไป",
            ("เพราะการตรวจดินจะบอกได้ว่าควรรดน้ำวันละกี่ครั้ง และควรรดน้ำเวลาใดจึงดีที่สุด",
             "เพราะปุ๋ยทุกสูตรมีราคาเท่ากัน จึงต้องเลือกจากผลตรวจดินเท่านั้น",
             "เพราะดินที่ตรวจแล้วจะดูดซับปุ๋ยได้ดีกว่าดินที่ไม่ได้ตรวจ"),
        ),
        Concept(
            "ปุ๋ยสูตรเสมอ เช่น 15-15-15 เหมาะกับสถานการณ์ใดมากที่สุด",
            "การบำรุงต้นโดยรวมในระยะแรกปลูก เมื่อยังไม่ต้องการเร่งส่วนใดเป็นพิเศษ",
            ("การเร่งให้ไม้ผลออกดอกพร้อมกันทั้งสวน",
             "การเร่งใบของผักกินใบให้เขียวและกว้างที่สุด",
             "การเพิ่มความหวานของผลไม้ในช่วงก่อนเก็บเกี่ยวโดยเฉพาะ"),
        ),
    ], (
        ("อุณหภูมิ ความชื้น และแสงที่เหมาะกับการใช้ปุ๋ย",
         "สัดส่วนของแคลเซียม แมกนีเซียม และกำมะถันตามลำดับ"),
        ("กำมะถัน",
         "แมกนีเซียม"),
        ("ปุ๋ยอินทรีย์และปุ๋ยเคมีเหมือนกันทุกประการ ต่างกันเพียงสี",
         "ปุ๋ยเคมีได้จากการย่อยสลายซากพืชซากสัตว์"),
        ("ทำให้พืชไม่ต้องสังเคราะห์ด้วยแสงอีก เพราะได้อาหารจากปุ๋ยโดยตรง",
         "ทำให้ดินอุ้มน้ำได้ดีขึ้นเสมอ"),
        ("เพราะตรวจดินแล้วไม่ต้องใส่ปุ๋ยอีกเลย",
         "เพราะการตรวจดินบอกชนิดของแมลงศัตรูพืชได้"),
        ("การเร่งหัวของพืชหัวให้ใหญ่ที่สุดในช่วงก่อนเก็บเกี่ยว โดยไม่ต้องบำรุงใบ",
         "การแก้ปัญหาดินที่ขาดโพแทสเซียมเพียงธาตุเดียว"),
    ))


@question_type(
    "plant.fertiliser_fluency",
    display_name={"th": "จับคู่จุดประสงค์กับสูตรปุ๋ยที่เหมาะสม"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class FertiliserFluency(QuestionType):
    """Match a purpose to a bag, or a bag to a purpose.

    Two bags may lead with the same nutrient — 46-0-0 and 21-0-0 both do — so no
    distractor may share the answer's emphasis. Without that filter the item
    would have two right answers.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(FERTILISERS)
        purpose = EMPHASIS_PURPOSE[item.emphasis]
        others = [other for other in FERTILISERS
                  if other.emphasis != item.emphasis]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ต้องการ{purpose} ควรเลือกปุ๋ยสูตรใด",
                correct=item.formula,
                wrongs=tuple(other.formula for other in others[:3]),
                hint="ดูว่าตัวเลขตัวใดสูงที่สุด ตัวแรกคือไนโตรเจน ตัวกลางคือฟอสฟอรัส "
                     "และตัวท้ายคือโพแทสเซียม",
            )
        wrong_purposes = [EMPHASIS_PURPOSE[key] for key in EMPHASIS_PURPOSE
                          if key != item.emphasis]
        rng.shuffle(wrong_purposes)
        return _labelled(
            stem=f"ปุ๋ยสูตร “{item.formula}” เหมาะกับจุดประสงค์ใดมากที่สุด",
            correct=purpose,
            wrongs=tuple(wrong_purposes[:3]),
            hint="หาตัวเลขที่สูงที่สุดก่อน แล้วจึงนึกถึงว่าธาตุนั้นส่งเสริมส่วนใดของพืช",
        )


@question_type(
    "plant.fertiliser_application",
    display_name={"th": "เลือกใช้ปุ๋ยให้เหมาะกับพืชในสถานการณ์ที่กำหนด"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class FertiliserApplication(QuestionType):
    """Choose a bag for a stated situation and say why it fits.

    This is ``ม.1/15`` word for word — ``เลือกใช้ปุ๋ย … ในสถานการณ์ที่กำหนด``.
    Every wrong choice names a real formula with a real property, so the item
    turns on matching the plant's stage to the nutrient rather than on spotting
    an invented product.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, FERTILISER_SCENARIOS,
            hint="ถามก่อนว่าต้องการเร่งส่วนใดของพืช ใบ ราก ดอก หรือผล "
                 "แล้วจึงเลือกสูตรที่ธาตุนั้นสูงที่สุด",
            topic=TOPIC,
        )


# More items: the set drew from six, so a learner met them all in a few tries.
FertiliserFoundation.ITEMS = [*FertiliserFoundation.ITEMS,
    Concept('ตัวเลขตัวกลางในสูตรปุ๋ย เช่น 12-24-12 บอกปริมาณของธาตุใด',
            'ฟอสฟอรัส',
            ('ไนโตรเจน', 'โพแทสเซียม', 'แคลเซียม', 'แมกนีเซียม', 'กำมะถัน')),
    Concept('ปุ๋ยหมักทำมาจากอะไร',
            'เศษพืช เศษอาหาร และมูลสัตว์ที่ปล่อยให้จุลินทรีย์ย่อยสลายจนเปื่อย',
            ('แร่ธาตุที่ขุดได้จากเหมืองแล้วนำมาบดจนละเอียดเป็นผงทั้งหมด', 'สารเคมีที่สังเคราะห์ในโรงงานจากแก๊สธรรมชาติและอากาศ', 'ทรายและหินที่ผ่านการเผาจนร้อนจัดแล้วทิ้งไว้ให้เย็นตัว', 'น้ำฝนที่เก็บไว้ในโอ่งจนมีตะกอนตกลงที่ก้นภาชนะ', 'พลาสติกและโฟมที่ตัดเป็นชิ้นเล็กแล้วผสมกับดินร่วน')),
    Concept('ปุ๋ยพืชสดหมายถึงอะไร',
            'การปลูกพืชตระกูลถั่วแล้วไถกลบลงดินขณะออกดอก เพื่อเพิ่มธาตุอาหารและอินทรียวัตถุ',
            ('การฉีดพ่นน้ำคั้นจากผักสดลงบนใบพืชทุกวันเพื่อให้ใบเขียวขึ้นทันที', 'การนำผลไม้สดที่ยังไม่สุกมาวางรอบโคนต้นเพื่อให้รากดูดน้ำตาลไปใช้', 'การใช้ปุ๋ยเคมีที่เพิ่งผลิตใหม่ ซึ่งยังไม่หมดอายุและมีธาตุอาหารครบ', 'การปลูกพืชชนิดเดียวกันซ้ำในแปลงเดิมทุกปีเพื่อให้ดินคุ้นเคยกับพืช', 'การเผาตอซังพืชแล้วโรยขี้เถ้าที่ได้ลงในแปลงก่อนปลูกรอบใหม่')),
    Concept('ปุ๋ยสูตร 0-0-60 มีธาตุอาหารใดสูงที่สุด',
            'โพแทสเซียม',
            ('ไนโตรเจน', 'ฟอสฟอรัส', 'แคลเซียม', 'แมกนีเซียม', 'เหล็ก')),
]
