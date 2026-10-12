"""ลักษณะทางพันธุกรรม

ชีวะ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 1.3 ป.5/1

Sets moved here from: science_wave_b24.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b24 import HEREDITY_TOPIC, INHERITED_SCENARIOS, PRIMARY_FIVE

PROVENANCE = Provenance("original")


class Inherited(NamedTuple):
    """A trait passed from parents, the kind of organism, and how it shows."""
    trait: str
    kind: str
    shows: str


INHERITED = (
    Inherited("สีของดอก", "พืช",
              "ต้นที่ปลูกจากเมล็ดของต้นแม่ที่ดอกสีแดง มักออกดอกสีแดงตามต้นแม่"),
    Inherited("รูปร่างของเมล็ด", "พืช",
              "ถั่วที่เกิดจากต้นพ่อแม่ซึ่งมีเมล็ดกลม มักได้เมล็ดกลมตามพ่อแม่"),
    Inherited("ความสูงของต้น", "พืช",
              "ข้าวพันธุ์ต้นเตี้ยที่ปลูกจากเมล็ดของต้นเตี้ย ก็ยังได้ต้นเตี้ยตามพันธุ์"),
    Inherited("สีขน", "สัตว์",
              "ลูกแมวที่เกิดจากพ่อแม่ขนสีส้ม มักมีขนสีส้มเหมือนพ่อแม่"),
    Inherited("ลักษณะของหู", "สัตว์",
              "ลูกกระต่ายที่เกิดจากพ่อแม่หูตก มักมีหูตกเหมือนพ่อแม่"),
    Inherited("ลักษณะเส้นผม", "มนุษย์",
              "ลูกที่เกิดจากพ่อแม่ผมหยิก มักมีผมหยิกเหมือนพ่อแม่"),
    Inherited("ลักษณะของติ่งหู", "มนุษย์",
              "ลูกอาจมีติ่งหูแบบติดหรือแบบไม่ติด ตามลักษณะที่ได้รับจากพ่อและแม่"),
    Inherited("ลักษณะการมีลักยิ้ม", "มนุษย์",
              "ลูกที่มีลักยิ้มมักมีพ่อหรือแม่ที่มีลักยิ้มอยู่ด้วย"),
)


class Observed(NamedTuple):
    """A trait seen in an individual, and whether it was passed down."""
    description: str
    verdict: str


OBSERVED = (
    Observed("ลูกสุนัขตัวหนึ่งมีขนสีดำเหมือนแม่ของมัน",
             "เป็นลักษณะทางพันธุกรรม เพราะสีขนถ่ายทอดจากพ่อแม่มาสู่ลูกได้"),
    Observed("ต้นกุหลาบที่ปลูกจากเมล็ดของต้นดอกสีเหลือง ออกดอกสีเหลืองเช่นกัน",
             "เป็นลักษณะทางพันธุกรรม เพราะสีของดอกถ่ายทอดจากต้นพ่อแม่มาสู่ต้นลูกได้"),
    Observed("เด็กคนหนึ่งมีผมหยิกเหมือนพ่อและแม่ของเขา",
             "เป็นลักษณะทางพันธุกรรม เพราะลักษณะเส้นผมถ่ายทอดจากพ่อแม่มาสู่ลูกได้"),
    Observed("สุนัขตัวหนึ่งมีรอยแผลเป็นที่ขาจากการถูกรถชน",
             "ไม่ใช่ลักษณะทางพันธุกรรม เพราะเป็นสิ่งที่เกิดขึ้นภายหลังจากอุบัติเหตุ "
             "จึงไม่ถ่ายทอดไปสู่ลูก"),
    Observed("ต้นไม้ต้นหนึ่งเตี้ยกว่าต้นอื่นเพราะปลูกในดินที่ขาดธาตุอาหาร",
             "ไม่ใช่ลักษณะทางพันธุกรรม เพราะเกิดจากสภาพแวดล้อมที่ปลูก "
             "ไม่ได้รับถ่ายทอดมาจากต้นพ่อแม่"),
    Observed("นักกีฬาคนหนึ่งมีกล้ามเนื้อแขนใหญ่จากการฝึกยกน้ำหนักทุกวัน",
             "ไม่ใช่ลักษณะทางพันธุกรรม เพราะเกิดจากการฝึกฝนของตนเอง "
             "จึงไม่ถ่ายทอดไปสู่ลูก"),
    Observed("เด็กคนหนึ่งพูดภาษาอังกฤษได้คล่องเพราะเรียนมาตั้งแต่เล็ก",
             "ไม่ใช่ลักษณะทางพันธุกรรม เพราะเป็นความสามารถที่เกิดจากการเรียนรู้ "
             "ไม่ได้รับถ่ายทอดมาจากพ่อแม่"),
)


@question_type(
    "life.inherited_trait_foundation",
    display_name={"th": "ลักษณะทางพันธุกรรมของพืช สัตว์ และมนุษย์"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=HEREDITY_TOPIC,
)
class InheritedTraitFoundation(QuestionType):
    """Which traits pass from parents, across all three kinds of organism."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(INHERITED)
        others = [other for other in INHERITED if other.trait != item.trait]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.trait}” ของ{item.kind}ถ่ายทอดจากพ่อแม่สู่ลูก"
                     f"อย่างไร",
                correct=item.shows,
                wrongs=tuple(other.shows for other in others[:3]),
                hint="ตัวอย่างที่ถูกต้องต้องพูดถึงสิ่งมีชีวิตชนิดเดียวกับที่โจทย์ถาม",
                topic=HEREDITY_TOPIC,
            )
        return _labelled(
            stem=f"ข้อความที่ว่า “{item.shows}” เป็นการถ่ายทอดลักษณะใด",
            correct=f"{item.trait}ของ{item.kind}",
            wrongs=tuple(f"{other.trait}ของ{other.kind}" for other in others[:3]),
            hint="อ่านตัวอย่างให้จบว่าเป็นพืช สัตว์ หรือมนุษย์ "
                 "แล้วจึงดูว่าลักษณะที่พูดถึงคืออะไร",
            topic=HEREDITY_TOPIC,
        )


@question_type(
    "life.inherited_trait_fluency",
    display_name={"th": "แยกลักษณะทางพันธุกรรมออกจากลักษณะที่เกิดภายหลัง"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=HEREDITY_TOPIC,
)
class InheritedTraitFluency(QuestionType):
    """Say whether an observed trait was passed down, and why."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(OBSERVED)
        others = [other.verdict for other in OBSERVED
                  if other.verdict != item.verdict]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.description}” ข้อใดกล่าวได้ถูกต้อง",
            correct=item.verdict, wrongs=tuple(others[:3]),
            hint="ถามว่าลักษณะนั้นมีมาตั้งแต่เกิดโดยได้รับจากพ่อแม่ "
                 "หรือเกิดขึ้นภายหลังจากสิ่งแวดล้อมและการฝึกฝน",
            topic=HEREDITY_TOPIC,
        )


@question_type(
    "life.inherited_trait_application",
    display_name={"th": "วิเคราะห์การถ่ายทอดลักษณะทางพันธุกรรม"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=HEREDITY_TOPIC,
)
class InheritedTraitApplication(QuestionType):
    """Read a family or a crop back to what heredity does and does not explain."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, INHERITED_SCENARIOS,
            hint="ลูกได้รับลักษณะจากทั้งพ่อและแม่ "
                 "และสิ่งที่เกิดขึ้นกับร่างกายภายหลังจะไม่ถ่ายทอดต่อไป",
        ), HEREDITY_TOPIC)
