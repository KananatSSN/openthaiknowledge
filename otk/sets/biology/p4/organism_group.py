"""กลุ่มพืช กลุ่มสัตว์ และกลุ่มที่ไม่ใช่พืชและสัตว์

ชีวะ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 1.3 ป.4/1

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
from otk.sets._support.science_wave_b23 import GROUP_SCENARIOS, GROUP_TOPIC

PROVENANCE = Provenance("original")


class Group(NamedTuple):
    """One of the three groups, and what marks a member of it."""
    name: str
    mark: str


GROUPS = (
    Group("กลุ่มพืช",
          "สร้างอาหารเองได้จากแสง มีสีเขียวของคลอโรฟิลล์ "
          "และเคลื่อนที่จากที่หนึ่งไปอีกที่หนึ่งไม่ได้"),
    Group("กลุ่มสัตว์",
          "สร้างอาหารเองไม่ได้จึงต้องกินสิ่งมีชีวิตอื่นเป็นอาหาร "
          "และเคลื่อนที่จากที่หนึ่งไปอีกที่หนึ่งได้"),
    Group("กลุ่มที่ไม่ใช่พืชและไม่ใช่สัตว์",
          "สร้างอาหารเองจากแสงไม่ได้และไม่ได้กินอาหารแบบสัตว์ "
          "แต่ย่อยสลายหรือดูดซึมอาหารจากสิ่งที่มันอาศัยอยู่"),
)


class Organism(NamedTuple):
    """A living thing, the group it belongs to, and why it lands there."""
    name: str
    group: str
    because: str


ORGANISMS = (
    Organism("ต้นมะม่วง", "กลุ่มพืช",
             "มีใบสีเขียวที่สร้างอาหารเองได้จากแสง และยืนอยู่กับที่"),
    Organism("ต้นเฟิร์น", "กลุ่มพืช",
             "มีใบสีเขียวที่สร้างอาหารเองได้จากแสง แม้จะไม่มีดอกก็ตาม"),
    Organism("ต้นมอส", "กลุ่มพืช",
             "เป็นพืชขนาดเล็กที่มีคลอโรฟิลล์และสร้างอาหารเองได้จากแสง"),
    Organism("ปลานิล", "กลุ่มสัตว์",
             "ต้องกินอาหารจากสิ่งมีชีวิตอื่น และว่ายน้ำเคลื่อนที่ไปได้"),
    Organism("ไส้เดือนดิน", "กลุ่มสัตว์",
             "กินซากพืชซากสัตว์ในดินเป็นอาหาร และเคลื่อนที่ไปมาในดินได้"),
    Organism("ผีเสื้อ", "กลุ่มสัตว์",
             "ดูดน้ำหวานจากดอกไม้เป็นอาหาร และบินเคลื่อนที่ไปได้"),
    Organism("เห็ดฟาง", "กลุ่มที่ไม่ใช่พืชและไม่ใช่สัตว์",
             "ไม่มีคลอโรฟิลล์จึงสร้างอาหารเองไม่ได้ แต่ย่อยสลายซากพืชที่มันขึ้นอยู่"),
    Organism("ราขนมปัง", "กลุ่มที่ไม่ใช่พืชและไม่ใช่สัตว์",
             "ขึ้นเป็นเส้นใยบนอาหารและย่อยอาหารนั้น ไม่มีคลอโรฟิลล์และไม่กินแบบสัตว์"),
    Organism("อะมีบา", "กลุ่มที่ไม่ใช่พืชและไม่ใช่สัตว์",
             "เป็นสิ่งมีชีวิตเซลล์เดียวที่มองด้วยตาเปล่าไม่เห็น "
             "ไม่จัดอยู่ในกลุ่มพืชหรือกลุ่มสัตว์"),
)


# Each group's mark in three wordings. Every wording still names the food source
# and so fits one group only.
GROUP_MARKS = {
    "กลุ่มพืช": (
        GROUPS[0].mark,
        "มีคลอโรฟิลล์จึงสร้างอาหารเองได้จากแสง และอยู่กับที่ไม่ย้ายไปไหน",
        "ใช้แสงสร้างอาหารขึ้นเองโดยไม่ต้องกินสิ่งมีชีวิตอื่น และย้ายที่อยู่เองไม่ได้",
    ),
    "กลุ่มสัตว์": (
        GROUPS[1].mark,
        "ต้องกินพืชหรือสัตว์อื่นเป็นอาหาร และย้ายตัวเองไปหาอาหารได้",
        "ไม่มีคลอโรฟิลล์ จึงต้องกินสิ่งมีชีวิตอื่น และเคลื่อนที่ไปที่อื่นได้เอง",
    ),
    "กลุ่มที่ไม่ใช่พืชและไม่ใช่สัตว์": (
        GROUPS[2].mark,
        "ไม่มีคลอโรฟิลล์และไม่กินอาหารแบบสัตว์ แต่ดูดซึมอาหารจากสิ่งที่มันขึ้นอยู่",
        "ย่อยสลายซากหรืออาหารที่มันขึ้นอยู่แล้วดูดซึมเข้าไป โดยไม่สร้างอาหารจากแสง",
    ),
}


# Only three groups exist, so the fourth choice is a plausible but wrong criterion.
GROUP_SPARES = (
    "แบ่งตามขนาดของสิ่งมีชีวิต โดยสิ่งที่ใหญ่กว่าจัดอยู่คนละกลุ่มกับสิ่งที่เล็กกว่า",
    "แบ่งตามสีของสิ่งมีชีวิต โดยสิ่งที่มีสีสดใสจัดอยู่ในกลุ่มเดียวกัน",
    "แบ่งตามที่อยู่ โดยสิ่งที่อยู่ในน้ำจัดอยู่คนละกลุ่มกับสิ่งที่อยู่บนบก",
    "แบ่งตามจำนวนที่พบ โดยสิ่งที่พบมากจัดอยู่คนละกลุ่มกับสิ่งที่พบน้อย",
)


# The third wrong reading in Fluency: the right group for a reason that is not a criterion.
GROUP_BAD_REASONS = (
    "มีขนาดใหญ่กว่าสิ่งมีชีวิตในกลุ่มอื่น",
    "มีสีสันสดใสกว่าสิ่งมีชีวิตในกลุ่มอื่น",
    "อาศัยอยู่ในที่ชื้นเหมือนสิ่งมีชีวิตอื่นในกลุ่มนี้",
    "พบได้บ่อยในสวนหลังบ้าน",
)


@question_type(
    "life.organism_group_foundation",
    display_name={"th": "เกณฑ์ของกลุ่มพืช กลุ่มสัตว์ และกลุ่มอื่น"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class OrganismGroupFoundation(QuestionType):
    """The mark of each of the three groups, before anything is sorted."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(GROUPS)
        others = [other for other in GROUPS if other.name != item.name]
        rng.shuffle(others)
        pool = list(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"สิ่งมีชีวิตใน “{item.name}” มีลักษณะร่วมกันอย่างไร",
                correct=rng.choice(GROUP_MARKS[item.name]),
                wrongs=tuple([rng.choice(GROUP_MARKS[other.name]) for other in pool]
                             + [rng.choice(GROUP_SPARES)]),
                hint="ดูสองอย่าง คือสร้างอาหารเองได้หรือไม่ "
                     "และเคลื่อนที่จากที่หนึ่งไปอีกที่หนึ่งได้หรือไม่",
                topic=GROUP_TOPIC,
            )
        return _labelled(
            stem=f"สิ่งมีชีวิตกลุ่มใด{rng.choice(GROUP_MARKS[item.name])}",
            correct=item.name,
            wrongs=tuple([other.name for other in pool]
                         + ["กลุ่มสิ่งไม่มีชีวิต"]),
            hint="อ่านลักษณะให้จบ แล้วจึงเลือกกลุ่มที่มีลักษณะนั้นเป็นเกณฑ์",
            topic=GROUP_TOPIC,
        )


@question_type(
    "life.organism_group_fluency",
    display_name={"th": "จำแนกสิ่งมีชีวิตออกเป็นสามกลุ่ม"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class OrganismGroupFluency(QuestionType):
    """Sort an organism into one of the three groups, with the reason."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ORGANISMS)
        wrong_groups = [group.name for group in GROUPS if group.name != item.group]
        rng.shuffle(wrong_groups)
        return _labelled(
            stem=f"“{item.name}” จัดอยู่ในกลุ่มใด และเพราะเหตุใด",
            correct=f"{item.group} เพราะ{item.because}",
            wrongs=(f"{wrong_groups[0]} เพราะ{item.because}",
                    f"{wrong_groups[1]} เพราะ{item.because}",
                    f"{item.group} เพราะ{rng.choice(GROUP_BAD_REASONS)}",
                    # Wrong group and a wrong reason.
                    *(f"{group} เพราะ{reason}" for group, reason
                      in zip(wrong_groups, rng.sample(GROUP_BAD_REASONS, 2)))),
            hint="เห็ด รา และสิ่งมีชีวิตเซลล์เดียวไม่ใช่ทั้งพืชและสัตว์ "
                 "แม้จะขึ้นอยู่กับที่เหมือนพืชก็ตาม",
            topic=GROUP_TOPIC,
        )


@question_type(
    "life.organism_group_application",
    display_name={"th": "วิเคราะห์การจำแนกสิ่งมีชีวิตเป็นกลุ่ม"},
    level=PRIMARY_FOUR, subject=SUBJECT, topic=GROUP_TOPIC,
)
class OrganismGroupApplication(QuestionType):
    """Judge a grouping, or the criterion someone used to make it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, GROUP_SCENARIOS,
            hint="กลับไปที่เกณฑ์เสมอ คือสร้างอาหารเองได้หรือไม่ "
                 "ไม่ใช่ที่รูปร่างหรือที่อยู่อาศัย",
        ), GROUP_TOPIC)
