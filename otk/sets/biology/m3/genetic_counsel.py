"""การปรึกษาแพทย์ก่อนแต่งงาน

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.3/6

Sets moved here from: science_wave_b27.
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
from otk.sets._support.science_wave_b19 import Fact, _fact_question
from otk.sets._support.science_wave_b25 import MIDDLE_THREE
from otk.sets._support.science_wave_b26 import DISEASE_TOPIC
from otk.sets._support.science_wave_b27 import COUNSEL_SCENARIOS

PROVENANCE = Provenance("original")


COUNSEL_FACTS = (
    Fact("การเป็นพาหะของโรคทางพันธุกรรมหมายความว่าอย่างไร",
         "มีแอลลีลที่ทำให้เกิดโรคอยู่หนึ่งตัวโดยไม่แสดงอาการ "
         "แต่ถ่ายทอดแอลลีลนั้นไปสู่ลูกได้"),
    Fact("เหตุใดพ่อแม่ที่ไม่แสดงอาการจึงมีลูกเป็นโรคทางพันธุกรรมได้",
         "เพราะทั้งสองฝ่ายอาจเป็นพาหะ เมื่อลูกได้รับแอลลีลด้อยที่ทำให้เกิดโรค"
         "จากทั้งพ่อและแม่ ลูกจึงแสดงอาการของโรค"),
    Fact("การตรวจก่อนแต่งงานบอกอะไรได้",
         "บอกได้ว่าคู่สมรสเป็นพาหะของโรคทางพันธุกรรมบางชนิดหรือไม่ "
         "และลูกที่จะเกิดมามีโอกาสเป็นโรคนั้นมากน้อยเพียงใด"),
    Fact("ความรู้เรื่องโรคทางพันธุกรรมมีประโยชน์อย่างไรต่อครอบครัว",
         "ทำให้วางแผนครอบครัวได้บนข้อมูลจริง และเตรียมการดูแลรักษาไว้ล่วงหน้า"
         "หากลูกมีความเสี่ยง"),
    Fact("เหตุใดประวัติการเจ็บป่วยของญาติจึงสำคัญต่อการประเมินความเสี่ยง",
         "เพราะโรคทางพันธุกรรมถ่ายทอดกันในสายเลือด "
         "การพบโรคเดียวกันในญาติหลายคนจึงบ่งชี้ว่าครอบครัวนั้นมีแอลลีลนั้นอยู่"),
    Fact("การตรวจพบว่าเป็นพาหะ หมายความว่าไม่ควรมีลูกใช่หรือไม่",
         "ไม่ใช่ การตรวจให้ข้อมูลเพื่อประกอบการตัดสินใจและการวางแผนดูแล "
         "การตัดสินใจยังเป็นของคู่สมรสเอง"),
)


COUNSEL_FACTS += (
    Fact('ถ้าคู่สมรสเป็นพาหะของโรคชนิดเดียวกันทั้งคู่ ลูกมีโอกาสเป็นโรคเท่าใด',
         'หนึ่งในสี่ในการตั้งครรภ์แต่ละครั้ง และโอกาสนี้เท่าเดิมทุกครั้งไม่ขึ้นกับลูกคนก่อน'),
    Fact('การตรวจหาพาหะธาลัสซีเมียทำได้อย่างไร',
         'ตรวจเลือดดูลักษณะของเม็ดเลือดแดงและชนิดของฮีโมโกลบิน แล้วยืนยันด้วยการตรวจทางพันธุกรรมเมื่อจำเป็น'),
    Fact('เหตุใดผลการตรวจทางพันธุกรรมจึงต้องเก็บเป็นความลับ',
         'เพราะเป็นข้อมูลส่วนบุคคลที่อาจนำไปสู่การตีตราหรือการเลือกปฏิบัติ ถ้าถูกเปิดเผยโดยไม่ยินยอม'),
    Fact('ผู้ให้คำปรึกษาทางพันธุศาสตร์มีบทบาทอย่างไร',
         'อธิบายผลตรวจ ความเสี่ยง และทางเลือกที่มี โดยให้คู่สมรสเป็นผู้ตัดสินใจเอง'),
)


class Couple(NamedTuple):
    """A couple's situation, and the step the indicator says they should know of."""
    situation: str
    step: str


COUPLES = (
    Couple("คู่สมรสที่มีญาติสายตรงเป็นโรคธาลัสซีเมียหลายคน",
           "ควรไปปรึกษาแพทย์เพื่อตรวจว่าทั้งสองฝ่ายเป็นพาหะของธาลัสซีเมียหรือไม่ "
           "ก่อนวางแผนมีบุตร"),
    Couple("คู่สมรสที่ทั้งสองฝ่ายไม่มีอาการใดเลย แต่ยังไม่เคยตรวจเลือด",
           "ควรไปปรึกษาแพทย์เพื่อตรวจก่อนแต่งงาน เพราะผู้ที่เป็นพาหะ"
           "ไม่แสดงอาการและทราบได้จากการตรวจเท่านั้น"),
    Couple("คู่สมรสที่เคยมีลูกคนแรกเป็นโรคทางพันธุกรรม",
           "ควรไปปรึกษาแพทย์เพื่อประเมินโอกาสที่ลูกคนต่อไปจะเป็นโรคเดียวกัน "
           "และวางแผนการตรวจระหว่างตั้งครรภ์"),
    Couple("คู่สมรสที่เป็นญาติใกล้ชิดกันทางสายเลือด",
           "ควรไปปรึกษาแพทย์เพื่อตรวจ เพราะญาติสายเลือดเดียวกันมีโอกาส"
           "เป็นพาหะของแอลลีลด้อยตัวเดียวกันสูงกว่าคนทั่วไป"),
    Couple("คู่สมรสที่ฝ่ายหญิงมีพี่ชายเป็นโรคฮีโมฟีเลีย",
           "ควรไปปรึกษาแพทย์เพื่อตรวจว่าฝ่ายหญิงเป็นพาหะของยีนบนโครโมโซม X "
           "หรือไม่ เพราะจะส่งต่อไปยังลูกชายได้"),
    Couple("คู่สมรสที่ฝ่ายหญิงอายุมากและกำลังวางแผนมีบุตร",
           "ควรไปปรึกษาแพทย์เพื่อรับคำแนะนำเรื่องการตรวจความผิดปกติ"
           "ของโครโมโซมในทารก ซึ่งมีโอกาสสูงขึ้นตามอายุของมารดา"),
)


COUPLES += (
    Couple('คู่สมรสที่ตรวจแล้วพบว่าฝ่ายหนึ่งเป็นพาหะธาลัสซีเมีย ส่วนอีกฝ่ายไม่เป็นพาหะ',
          'ควรรับคำอธิบายจากแพทย์ว่าลูกจะไม่เป็นโรคชนิดที่ต้องได้แอลลีลผิดปกติจากทั้งสองฝ่าย แต่ลูกอาจเป็นพาหะได้ประมาณครึ่งหนึ่ง'),
)


@question_type(
    "life.genetic_counsel_foundation",
    display_name={"th": "พาหะและความเสี่ยงของโรคทางพันธุกรรม"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=DISEASE_TOPIC,
)
class GeneticCounselFoundation(QuestionType):
    """What being a carrier means, and what a test can tell."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, COUNSEL_FACTS, topic=DISEASE_TOPIC,
            hint="แยกให้ชัดระหว่างผู้ที่เป็นโรค ผู้ที่เป็นพาหะ "
                 "และผู้ที่ไม่มีแอลลีลนั้นเลย",
        )


@question_type(
    "life.genetic_counsel_fluency",
    display_name={"th": "การปรึกษาแพทย์ก่อนแต่งงาน"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=DISEASE_TOPIC,
)
class GeneticCounselFluency(QuestionType):
    """State the step the indicator names — its own evidence clause.

    ``ม.3/6``'s evidence is ``โดยรู้ว่าก่อนแต่งงานควรปรึกษาแพทย์``. Knowing that is
    exactly what this asks for, so this set is ``exact`` while the other two are
    not.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(COUPLES)
        others = [other.step for other in COUPLES if other.step != item.step]
        rng.shuffle(others)
        return _labelled(
            stem=f"{item.situation} ควรทำสิ่งใดก่อนวางแผนมีบุตร",
            correct=item.step, wrongs=tuple(others[:3]),
            hint="คำตอบต้องตรงกับความเสี่ยงที่โจทย์ระบุไว้ "
                 "ไม่ใช่เพียงคำแนะนำทั่วไปที่ใช้ได้กับทุกคู่",
            topic=DISEASE_TOPIC,
        )


@question_type(
    "life.genetic_counsel_application",
    display_name={"th": "วิเคราะห์การใช้ความรู้เรื่องโรคทางพันธุกรรม"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=DISEASE_TOPIC,
)
class GeneticCounselApplication(QuestionType):
    """Judge how a couple or a family uses what a genetic test tells them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, COUNSEL_SCENARIOS,
            hint="ผลตรวจให้ข้อมูลเพื่อวางแผน ไม่ได้เปลี่ยนแอลลีลของใคร "
                 "และไม่ได้ตัดสินใจแทนใคร",
        ), DISEASE_TOPIC)
