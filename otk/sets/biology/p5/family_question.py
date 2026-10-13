"""การตั้งคำถามเกี่ยวกับลักษณะที่คล้ายพ่อแม่

ชีวะ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 1.3 ป.5/2

Sets moved here from: science_wave_b25.
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
from otk.sets._support.science_wave_b24 import HEREDITY_TOPIC, PRIMARY_FIVE
from otk.sets._support.science_wave_b25 import FAMILY_SCENARIOS

PROVENANCE = Provenance("original")


RESEMBLANCE_FACTS = (
    Fact("เหตุใดลูกจึงมีลักษณะหลายอย่างคล้ายพ่อและแม่",
         "เพราะลูกได้รับลักษณะทางพันธุกรรมถ่ายทอดมาจากทั้งพ่อและแม่ตั้งแต่เกิด"),
    Fact("เหตุใดพี่น้องท้องเดียวกันจึงหน้าตาไม่เหมือนกันทุกอย่าง",
         "เพราะลูกแต่ละคนได้รับชุดลักษณะจากพ่อและแม่ในแบบที่ต่างกันไป"),
    Fact("ลักษณะแบบใดของตนเองที่นำไปเปรียบเทียบกับพ่อแม่ได้ดีที่สุด",
         "ลักษณะที่มีมาตั้งแต่เกิดและสังเกตเห็นได้ เช่น ลักษณะติ่งหู "
         "ลักษณะเส้นผม หรือการมีลักยิ้ม"),
    Fact("ลักษณะแบบใดที่นำไปเปรียบเทียบกับพ่อแม่แล้วสรุปเรื่องพันธุกรรมไม่ได้",
         "ลักษณะที่เกิดขึ้นภายหลัง เช่น ทรงผมที่ตัด รอยแผลเป็น "
         "หรือความสามารถที่ได้จากการฝึกฝน"),
    Fact("การตั้งคำถามที่ดีเกี่ยวกับลักษณะของตนเองกับพ่อแม่ควรเป็นอย่างไร",
         "ควรเป็นคำถามที่หาคำตอบได้ด้วยการสังเกตและเปรียบเทียบ "
         "ไม่ใช่คำถามที่ตอบได้ด้วยความคิดเห็นเท่านั้น"),
    Fact("ถ้าลักษณะหนึ่งของเราไม่เหมือนทั้งพ่อและแม่ ควรคิดอย่างไร",
         "อาจเป็นลักษณะที่ได้รับมาจากปู่ ย่า ตา หรือยาย "
         "จึงควรขยายการเปรียบเทียบออกไปถึงญาติรุ่นก่อนด้วย"),
)


RESEMBLANCE_FACTS += (
    Fact('สีของดวงตาเป็นลักษณะที่ได้รับจากพ่อแม่หรือเกิดขึ้นภายหลัง',
         'เป็นลักษณะที่ได้รับถ่ายทอดจากพ่อแม่และมีมาตั้งแต่เกิด'),
    Fact('ความสามารถในการว่ายน้ำได้รับถ่ายทอดมาจากพ่อแม่ใช่หรือไม่',
         'ไม่ใช่ เป็นความสามารถที่ได้จากการฝึกฝนภายหลัง จึงไม่ได้ถ่ายทอดทางพันธุกรรม'),
    Fact('ลูกสัตว์และลูกพืชได้รับลักษณะจากพ่อแม่เหมือนมนุษย์หรือไม่',
         'ได้รับเหมือนกัน เช่น ลูกแมวมีสีขนคล้ายพ่อแม่ และต้นใหม่มีสีดอกคล้ายต้นเดิม'),
    Fact('ควรบันทึกการเปรียบเทียบลักษณะของตนเองกับพ่อแม่อย่างไร',
         'ทำตารางบันทึกลักษณะแต่ละอย่างของตนเอง พ่อ และแม่ แล้วดูว่าเหมือนใคร'),
)


class Wondering(NamedTuple):
    """Something a learner notices, and the question worth asking about it."""
    notice: str
    question: str


WONDERINGS = (
    Wondering("นักเรียนสังเกตว่าตนเองมีลักยิ้มแต่พี่ชายไม่มี",
              "ในครอบครัวของเรา มีใครบ้างที่มีลักยิ้ม และมีความสัมพันธ์กับ"
              "พ่อหรือแม่อย่างไร"),
    Wondering("นักเรียนสังเกตว่าตนเองมีติ่งหูแบบไม่ติด แต่แม่มีแบบติด",
              "พ่อมีติ่งหูแบบใด และปู่ย่าตายายมีติ่งหูแบบใดบ้าง"),
    Wondering("นักเรียนสังเกตว่าผมของตนหยิกกว่าผมของทั้งพ่อและแม่",
              "ในญาติรุ่นปู่ย่าตายาย มีใครผมหยิกบ้างหรือไม่"),
    Wondering("นักเรียนสังเกตว่าตนเองสูงกว่าเพื่อนที่อายุเท่ากันมาก",
              "พ่อและแม่ของเราสูงเท่าใดเมื่อเทียบกับพ่อแม่ของเพื่อน"),
    Wondering("นักเรียนสังเกตว่าตนเองห่อลิ้นได้แต่เพื่อนหลายคนทำไม่ได้",
              "พ่อและแม่ของเราห่อลิ้นได้หรือไม่ และในห้องเรียนมีสัดส่วนเท่าใด"
              "ที่ห่อลิ้นได้"),
    Wondering("นักเรียนสังเกตว่าน้องมีสีผิวเข้มกว่าตนเองทั้งที่พ่อแม่คนเดียวกัน",
              "สีผิวของพ่อและแม่เป็นอย่างไร และน้องออกแดดมากกว่าเราหรือไม่"),
)


WONDERINGS += (
    Wondering('นักเรียนสังเกตว่าตนเองมีสีตาเข้มเหมือนแม่ แต่ไม่เหมือนพ่อ',
          'ตายายมีสีตาแบบใด และพี่น้องของเรามีสีตาเหมือนพ่อหรือแม่'),
    Wondering('นักเรียนสังเกตว่าตนเองถนัดมือซ้าย ทั้งที่ทุกคนในบ้านถนัดมือขวา',
          'ในญาติของเรามีใครถนัดมือซ้ายบ้าง และการถนัดมือเกี่ยวกับการฝึกด้วยหรือไม่'),
    Wondering('นักเรียนสังเกตว่าลูกแมวในครอกเดียวกันที่บ้านมีสีขนต่างกัน',
          'แม่แมวและพ่อแมวมีสีขนแบบใด และลูกแมวแต่ละตัวเหมือนพ่อหรือแม่'),
)


@question_type(
    "life.family_question_foundation",
    display_name={"th": "ความคล้ายคลึงกันระหว่างตนเองกับพ่อแม่"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=HEREDITY_TOPIC,
)
class FamilyQuestionFoundation(QuestionType):
    """Why the resemblance is there, and what is worth comparing."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, RESEMBLANCE_FACTS, topic=HEREDITY_TOPIC,
            hint="แยกลักษณะที่มีมาตั้งแต่เกิด ออกจากลักษณะที่เกิดขึ้นภายหลัง",
        )


@question_type(
    "life.family_question_fluency",
    display_name={"th": "ตั้งคำถามเกี่ยวกับลักษณะของตนเองกับพ่อแม่"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=HEREDITY_TOPIC,
)
class FamilyQuestionFluency(QuestionType):
    """Choose the question that this particular noticing calls for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(WONDERINGS)
        others = [other.question for other in WONDERINGS
                  if other.question != item.question]
        rng.shuffle(others)
        return _labelled(
            stem=f"{item.notice} คำถามใดเหมาะที่จะตั้งขึ้นเพื่อหาคำตอบ"
                 f"เรื่องนี้มากที่สุด",
            correct=item.question, wrongs=tuple(others[:3]),
            hint="คำถามที่ดีต้องตรงกับสิ่งที่สังเกตเห็น "
                 "และหาคำตอบได้ด้วยการสังเกตหรือสอบถามคนในครอบครัว",
            topic=HEREDITY_TOPIC,
        )


@question_type(
    "life.family_question_application",
    display_name={"th": "วิเคราะห์คำถามเกี่ยวกับความคล้ายคลึงในครอบครัว"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=HEREDITY_TOPIC,
)
class FamilyQuestionApplication(QuestionType):
    """Judge a question or a plan for answering one about family resemblance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, FAMILY_SCENARIOS,
            hint="คำถามที่ดีต้องหาคำตอบได้จริงด้วยการสังเกต การวัด "
                 "หรือการสอบถาม",
        ), HEREDITY_TOPIC)
