"""การนำมิวเทชันไปใช้ประโยชน์

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.4/4

Sets moved here from: science_wave_b30.
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
from otk.sets._support.science_wave_b19 import UPPER_FOUR
from otk.sets._support.science_wave_b30 import MUTATION_USE_SCENARIOS

PROVENANCE = Provenance("original")


MUTATION_USE_TOPIC = "การใช้ประโยชน์จากมิวเทชัน"


class MutationUse(NamedTuple):
    """One use of induced mutation: how it works, and the need it answers."""
    name: str
    how: str
    need: str


MUTATION_USES = (
    MutationUse("การปรับปรุงพันธุ์พืชด้วยการฉายรังสี",
                 "ฉายรังสีเมล็ดหรือต้นอ่อนเพื่อชักนำให้เกิดมิวเทชันจำนวนมาก "
                 "แล้วคัดเลือกต้นที่มีลักษณะตามต้องการไว้ขยายพันธุ์ต่อ",
                 "ต้องการพัฒนาพันธุ์ข้าวที่ต้นเตี้ยลงจนไม่ล้มง่ายเมื่อลมแรง"),
    MutationUse("การชักนำมิวเทชันในไม้ดอกไม้ประดับ",
                 "ชักนำมิวเทชันแล้วคัดเลือกต้นที่ให้สีหรือรูปทรงของดอกแบบใหม่ "
                 "ซึ่งไม่มีอยู่ในพันธุ์เดิม",
                 "ต้องการเบญจมาศสีใหม่ที่ยังไม่เคยมีในตลาด"),
    MutationUse("การปรับปรุงสายพันธุ์จุลินทรีย์ในอุตสาหกรรม",
                 "ชักนำมิวเทชันในราหรือแบคทีเรีย แล้วคัดสายพันธุ์ที่ผลิตสารเป้าหมาย"
                 "ได้มากกว่าสายพันธุ์เดิมหลายเท่า",
                 "ต้องการเพิ่มปริมาณยาปฏิชีวนะที่ราผลิตได้ต่อถังหมัก"),
    MutationUse("การควบคุมแมลงด้วยเทคนิคแมลงเป็นหมัน",
                 "ใช้รังสีทำให้แมลงตัวผู้เป็นหมัน แล้วปล่อยจำนวนมากไปผสมกับ"
                 "ตัวเมียในธรรมชาติ ไข่ที่ได้จึงไม่ฟัก ประชากรแมลงจึงลดลง",
                 "ต้องการลดประชากรแมลงวันผลไม้ในพื้นที่โดยไม่ใช้สารเคมี"),
    MutationUse("การสร้างพันธุ์ผลไม้ที่มีเมล็ดน้อย",
                 "ชักนำให้ชุดโครโมโซมเปลี่ยนไปจนต้นสร้างเมล็ดที่สมบูรณ์ไม่ได้ "
                 "แต่ยังติดผลได้ตามปกติ",
                 "ต้องการผลไม้ที่รับประทานได้สะดวกเพราะแทบไม่มีเมล็ด"),
    MutationUse("การใช้อัตราการเกิดมิวเทชันเป็นตัวบ่งชี้มลพิษ",
                 "เลี้ยงสิ่งมีชีวิตทดสอบในตัวอย่างที่ต้องการตรวจ "
                 "แล้ววัดว่าเกิดมิวเทชันสูงกว่าปกติหรือไม่",
                 "ต้องการตรวจว่าน้ำทิ้งจากโรงงานมีสารก่อกลายพันธุ์ปนอยู่หรือไม่"),
)


@question_type(
    "life.mutation_use_foundation",
    display_name={"th": "วิธีการนำมิวเทชันไปใช้ประโยชน์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=MUTATION_USE_TOPIC,
)
class MutationUseFoundation(QuestionType):
    """How each technique works — the ``สืบค้นข้อมูล`` side of ``ม.4/4``."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(MUTATION_USES)
        others = [other for other in MUTATION_USES if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” ทำได้อย่างไร",
                correct=item.how,
                wrongs=tuple(other.how for other in others[:3]),
                hint="ทุกวิธีมีสองขั้นตอน คือชักนำให้เกิดมิวเทชัน "
                     "แล้วจึงคัดเลือกสิ่งที่ได้ตามต้องการ",
                topic=MUTATION_USE_TOPIC,
            )
        return _labelled(
            stem=f"การนำมิวเทชันไปใช้ในลักษณะใดทำโดย{item.how}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านวิธีการให้จบก่อนว่าใช้กับพืช จุลินทรีย์ หรือแมลง",
            topic=MUTATION_USE_TOPIC,
        )


@question_type(
    "life.mutation_use_fluency",
    display_name={"th": "ยกตัวอย่างการนำมิวเทชันไปใช้ประโยชน์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=MUTATION_USE_TOPIC,
)
class MutationUseFluency(QuestionType):
    """Give the use that answers a stated need — ``ยกตัวอย่าง`` itself."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(MUTATION_USES)
        others = [other.name for other in MUTATION_USES if other.name != item.name]
        rng.shuffle(others)
        return _labelled(
            stem=f"ถ้า{item.need} ควรนำมิวเทชันไปใช้ประโยชน์ในลักษณะใด",
            correct=item.name, wrongs=tuple(others[:3]),
            hint="จับคู่สิ่งที่ต้องการกับสิ่งมีชีวิตที่ถูกชักนำให้เกิดมิวเทชัน"
                 "ในแต่ละวิธี",
            topic=MUTATION_USE_TOPIC,
        )


@question_type(
    "life.mutation_use_application",
    display_name={"th": "วิเคราะห์การนำมิวเทชันไปใช้ประโยชน์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=MUTATION_USE_TOPIC,
)
class MutationUseApplication(QuestionType):
    """Weigh a use of induced mutation against how mutation actually behaves."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, MUTATION_USE_SCENARIOS,
            hint="มิวเทชันเกิดแบบสุ่ม การใช้ประโยชน์จึงต้องมีขั้นคัดเลือกเสมอ",
        ), MUTATION_USE_TOPIC)
