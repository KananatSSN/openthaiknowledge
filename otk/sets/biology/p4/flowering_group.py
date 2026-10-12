"""พืชดอกและพืชไม่มีดอก

ชีวะ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 1.3 ป.4/2

Sets moved here from: science_wave_b23.
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
from otk.sets._support.science_wave_b17 import PRIMARY_FOUR
from otk.sets._support.science_wave_b19 import Fact
from otk.sets._support.science_wave_b23 import FLOWERING_SCENARIOS, GROUP_TOPIC

PROVENANCE = Provenance("original")


class Plant(NamedTuple):
    """A plant, whether it flowers, and what is seen instead when it does not."""
    name: str
    group: str
    because: str


PLANTS = (
    Plant("ต้นมะม่วง", "พืชดอก",
          "ออกดอกก่อนแล้วจึงติดผลที่มีเมล็ดอยู่ภายใน"),
    Plant("ต้นข้าว", "พืชดอก",
          "ออกดอกเป็นช่อที่เรียกว่ารวงข้าว แล้วจึงกลายเป็นเมล็ดข้าว"),
    Plant("ต้นกุหลาบ", "พืชดอก",
          "ออกดอกที่เห็นได้ชัดเจน และดอกนั้นทำหน้าที่สืบพันธุ์"),
    Plant("ต้นบัว", "พืชดอก",
          "ออกดอกบัวขึ้นเหนือน้ำ แล้วจึงเกิดฝักบัวที่มีเมล็ดอยู่ภายใน"),
    Plant("ต้นเฟิร์น", "พืชไม่มีดอก",
          "ไม่ออกดอกเลย แต่สืบพันธุ์ด้วยสปอร์ที่อยู่ใต้ใบ"),
    Plant("ต้นมอส", "พืชไม่มีดอก",
          "ไม่ออกดอกเลย แต่สืบพันธุ์ด้วยสปอร์ที่อยู่ในอับสปอร์"),
    Plant("ต้นปรง", "พืชไม่มีดอก",
          "ไม่ออกดอก แต่สร้างเมล็ดไว้ในโครงสร้างที่เรียกว่าโคน"),
    Plant("ต้นสนสองใบ", "พืชไม่มีดอก",
          "ไม่ออกดอก แต่สร้างเมล็ดไว้ในโคนที่เห็นเป็นลูกสน"),
)


FLOWER_FACTS = (
    Fact("ดอกของพืชทำหน้าที่ใด",
         "เป็นส่วนที่ใช้สืบพันธุ์ โดยหลังการถ่ายเรณูจะเกิดเป็นผลและเมล็ดต่อไป"),
    Fact("พืชไม่มีดอกอย่างเฟิร์นและมอสสืบพันธุ์อย่างไร",
         "สืบพันธุ์ด้วยสปอร์ ซึ่งเป็นหน่วยเล็ก ๆ ที่ปลิวไปงอกเป็นต้นใหม่ได้"),
    Fact("พืชไม่มีดอกอย่างปรงและสนสืบพันธุ์อย่างไร",
         "สร้างเมล็ดไว้ในโครงสร้างที่เรียกว่าโคน โดยไม่ต้องมีดอก"),
    Fact("การที่พืชชนิดหนึ่งมีเมล็ด บอกได้หรือไม่ว่าเป็นพืชดอก",
         "บอกไม่ได้ เพราะปรงและสนมีเมล็ดโดยไม่มีดอก "
         "จึงต้องดูที่การมีดอกเป็นเกณฑ์โดยตรง"),
    Fact("พืชดอกกับพืชไม่มีดอกเหมือนกันในเรื่องใด",
         "ทั้งสองกลุ่มมีคลอโรฟิลล์และสร้างอาหารเองได้จากแสง "
         "จึงจัดอยู่ในกลุ่มพืชเหมือนกัน"),
    Fact("เหตุใดจึงควรสำรวจพืชในช่วงที่พืชออกดอก",
         "เพราะการที่พืชยังไม่ออกดอกในวันที่สำรวจ ไม่ได้แปลว่าพืชนั้น"
         "เป็นพืชไม่มีดอก"),
)


@question_type(
    "plant.flowering_group_foundation",
    display_name={"th": "เกณฑ์การจำแนกพืชดอกและพืชไม่มีดอก"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class FloweringGroupFoundation(QuestionType):
    """What the criterion is, and what it is not."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            item = rng.choice(FLOWER_FACTS)
            others = [other.answer for other in FLOWER_FACTS
                      if other.answer != item.answer]
            rng.shuffle(others)
            return _labelled(
                stem=item.question, correct=item.answer,
                wrongs=tuple(others[:3]),
                hint="แยกเรื่องการมีดอกออกจากเรื่องการมีเมล็ด "
                     "เพราะพืชบางชนิดมีเมล็ดโดยไม่มีดอก",
                topic=GROUP_TOPIC,
            )
        return _labelled(
            stem="การจำแนกพืชออกเป็นพืชดอกและพืชไม่มีดอก ใช้สิ่งใดเป็นเกณฑ์",
            correct="ใช้การมีดอกเป็นเกณฑ์ คือพืชที่ออกดอกจัดเป็นพืชดอก "
                    "ส่วนพืชที่ไม่ออกดอกเลยจัดเป็นพืชไม่มีดอก",
            wrongs=("ใช้การมีเมล็ดเป็นเกณฑ์ คือพืชที่มีเมล็ดจัดเป็นพืชดอกทั้งหมด",
                    "ใช้ขนาดของต้นเป็นเกณฑ์ คือต้นไม้ใหญ่จัดเป็นพืชดอก "
                    "ส่วนต้นเล็กจัดเป็นพืชไม่มีดอก",
                    "ใช้สีของใบเป็นเกณฑ์ คือพืชที่มีใบสีเขียวเข้มจัดเป็นพืชดอก"),
            hint="เกณฑ์อยู่ในชื่อของกลุ่มอยู่แล้ว "
                 "ระวังว่าพืชบางชนิดมีเมล็ดโดยไม่ต้องมีดอก",
            topic=GROUP_TOPIC,
        )


@question_type(
    "plant.flowering_group_fluency",
    display_name={"th": "จำแนกพืชดอกและพืชไม่มีดอก"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class FloweringGroupFluency(QuestionType):
    """Sort a named plant by the flowering criterion, with the reason."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(PLANTS)
        other_group = "พืชไม่มีดอก" if item.group == "พืชดอก" else "พืชดอก"
        others = [other.because for other in PLANTS
                  if other.group != item.group]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.name}” จัดเป็นพืชกลุ่มใด และเพราะเหตุใด",
            correct=f"{item.group} เพราะ{item.because}",
            wrongs=(f"{other_group} เพราะ{others[0]}",
                    f"{other_group} เพราะ{others[1]}",
                    f"{item.group} เพราะมีลำต้นสูงและใบสีเขียว"),
            hint="ถามว่าพืชนั้นออกดอกหรือไม่ ไม่ใช่ถามว่ามีเมล็ดหรือไม่",
            topic=GROUP_TOPIC,
        )


@question_type(
    "plant.flowering_group_application",
    display_name={"th": "วิเคราะห์การจำแนกพืชโดยใช้การมีดอกเป็นเกณฑ์"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class FloweringGroupApplication(QuestionType):
    """Judge a sorting done by the wrong criterion, or on incomplete data."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, FLOWERING_SCENARIOS,
            hint="ยึดเกณฑ์เดียวคือการมีดอก และระวังว่าการมีเมล็ด"
                 "ไม่ได้แปลว่ามีดอกเสมอไป",
        ), GROUP_TOPIC)
