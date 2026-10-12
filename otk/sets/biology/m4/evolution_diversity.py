"""ความหลากหลายของสิ่งมีชีวิตอันเป็นผลจากวิวัฒนาการ

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.4/6

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
from otk.sets._support.science_wave_b19 import UPPER_FOUR, Fact, _fact_question
from otk.sets._support.science_wave_b30 import EVOLUTION_SCENARIOS

PROVENANCE = Provenance("original")


EVOLUTION_TOPIC = "วิวัฒนาการและความหลากหลายของสิ่งมีชีวิต"


EVOLUTION_FACTS = (
    Fact("วิวัฒนาการทำให้เกิดความหลากหลายของสิ่งมีชีวิตได้อย่างไร",
         "ประชากรที่แยกจากกันเผชิญสิ่งแวดล้อมต่างกัน การคัดเลือกโดยธรรมชาติ"
         "จึงสะสมลักษณะที่ต่างกันไว้จนกลายเป็นชนิดใหม่ที่ต่างกันในที่สุด"),
    Fact("การคัดเลือกโดยธรรมชาติทำงานอย่างไร",
         "สมาชิกในประชากรมีลักษณะต่างกันอยู่แล้ว ตัวที่มีลักษณะเหมาะกับ"
         "สิ่งแวดล้อมนั้นรอดและสืบพันธุ์ได้มากกว่า ลักษณะนั้นจึงพบมากขึ้นในรุ่นต่อ ๆ ไป"),
    Fact("ความแปรผันในประชากรมีที่มาจากอะไร",
         "จากมิวเทชันที่เกิดขึ้นในสารพันธุกรรม และจากการรวมกันแบบใหม่ของยีน"
         "ในการสืบพันธุ์แบบอาศัยเพศ"),
    Fact("โครงสร้างที่มีต้นกำเนิดเดียวกันบ่งบอกอะไร",
         "บ่งบอกว่าสิ่งมีชีวิตเหล่านั้นมีบรรพบุรุษร่วมกัน แม้โครงสร้างนั้นจะถูก"
         "ปรับไปทำหน้าที่ต่างกันตามสิ่งแวดล้อมของแต่ละกลุ่ม"),
    Fact("ซากดึกดำบรรพ์เป็นหลักฐานของวิวัฒนาการอย่างไร",
         "แสดงลำดับของสิ่งมีชีวิตในช่วงเวลาต่าง ๆ และแสดงรูปแบบที่ค่อย ๆ "
         "เปลี่ยนไป จึงเชื่อมโยงกลุ่มที่ต่างกันในปัจจุบันเข้ากับบรรพบุรุษร่วม"),
    Fact("การเกิดชนิดใหม่มักเริ่มต้นจากอะไร",
         "จากการที่ประชากรถูกแยกออกจากกันจนไม่แลกเปลี่ยนยีนกัน "
         "แล้วสะสมความแตกต่างไว้จนผสมพันธุ์กันไม่ได้อีก"),
    Fact("เหตุใดลักษณะที่ได้เปรียบในที่หนึ่งอาจเสียเปรียบในอีกที่หนึ่ง",
         "เพราะการคัดเลือกโดยธรรมชาติขึ้นกับสิ่งแวดล้อมนั้น ๆ "
         "ไม่มีลักษณะใดที่ดีที่สุดในทุกสภาพแวดล้อม"),
)


class Example(NamedTuple):
    """A case of diversity, and the evolutionary account of it."""
    case: str
    account: str


EXAMPLES = (
    Example("นกฟินช์บนหมู่เกาะกาลาปากอสมีรูปร่างจะงอยปากต่างกันไปในแต่ละเกาะ",
            "ประชากรบนแต่ละเกาะมีอาหารต่างกัน จะงอยปากที่เหมาะกับอาหารนั้น"
            "จึงถูกคัดเลือกไว้ ความแตกต่างสะสมจนกลายเป็นชนิดที่ต่างกัน"),
    Example("กระดูกครีบของวาฬ ปีกของค้างคาว และแขนของมนุษย์ "
            "มีกระดูกชุดเดียวกันเรียงในแบบเดียวกัน",
            "เป็นโครงสร้างที่มีต้นกำเนิดเดียวกัน บ่งชี้ว่ามีบรรพบุรุษร่วมกัน "
            "แล้วถูกปรับไปทำหน้าที่ต่างกันตามวิถีชีวิตของแต่ละกลุ่ม"),
    Example("ผีเสื้อกลางคืนในเขตอุตสาหกรรมเปลี่ยนจากสีอ่อนเป็นสีเข้มเป็นส่วนใหญ่"
            "ภายในไม่กี่สิบปี",
            "เขม่าทำให้ต้นไม้สีเข้มขึ้น ผีเสื้อสีเข้มจึงถูกนกจับได้น้อยกว่าและ"
            "สืบพันธุ์ได้มากกว่า สัดส่วนของสีเข้มในประชากรจึงเพิ่มขึ้น"),
    Example("แบคทีเรียในโรงพยาบาลจำนวนมากดื้อต่อยาปฏิชีวนะหลายชนิด",
            "ในประชากรมีบางตัวที่มีมิวเทชันซึ่งทนยาอยู่ก่อนแล้ว "
            "การใช้ยาบ่อยครั้งคัดให้เหลือเฉพาะตัวที่ทนยา ประชากรจึงดื้อยาเป็นส่วนใหญ่"),
    Example("พืชในทะเลทรายหลายวงศ์ที่ไม่ใกล้ชิดกันต่างก็มีลำต้นอวบน้ำและใบลดรูป"
            "เป็นหนาม",
            "เป็นการที่สิ่งแวดล้อมแบบเดียวกันคัดเลือกลักษณะคล้ายกันไว้ในกลุ่ม"
            "ที่ไม่ได้ใกล้ชิดกัน จึงคล้ายกันโดยไม่ได้มีบรรพบุรุษใกล้กัน"),
    Example("ตัวอ่อนระยะแรกของปลา ไก่ และมนุษย์ มีโครงสร้างคล้ายช่องเหงือก"
            "เหมือนกัน",
            "ความคล้ายกันในระยะตัวอ่อนบ่งชี้ถึงบรรพบุรุษร่วมกันของสัตว์มีกระดูก"
            "สันหลัง แม้เมื่อโตเต็มวัยจะต่างกันมาก"),
)


@question_type(
    "life.evolution_diversity_foundation",
    display_name={"th": "วิวัฒนาการกับความหลากหลายของสิ่งมีชีวิต"},
    level=UPPER_FOUR, subject=SUBJECT, topic=EVOLUTION_TOPIC,
)
class EvolutionDiversityFoundation(QuestionType):
    """Explain how diversity follows from evolution — the ``อธิบาย`` half."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, EVOLUTION_FACTS, topic=EVOLUTION_TOPIC,
            hint="ลำดับที่ใช้เสมอคือ มีความแปรผันอยู่ก่อน แล้วสิ่งแวดล้อม"
                 "จึงคัดเลือก ไม่ใช่สิ่งแวดล้อมสั่งให้เปลี่ยน",
        )


@question_type(
    "life.evolution_diversity_fluency",
    display_name={"th": "ยกตัวอย่างความหลากหลายที่เกิดจากวิวัฒนาการ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=EVOLUTION_TOPIC,
)
class EvolutionDiversityFluency(QuestionType):
    """Account for a stated example — the ``ยกตัวอย่าง`` half of ``ม.4/6``."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(EXAMPLES)
        others = [other.account for other in EXAMPLES
                  if other.account != item.account]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.case}” ข้อใดอธิบายด้วยหลักวิวัฒนาการได้ถูกต้อง",
            correct=item.account, wrongs=tuple(others[:3]),
            hint="คำอธิบายที่ถูกต้องต้องพูดถึงสิ่งมีชีวิตในตัวอย่างนั้นจริง ๆ "
                 "และต้องเริ่มจากความแปรผันที่มีอยู่ก่อน",
            topic=EVOLUTION_TOPIC,
        )


@question_type(
    "life.evolution_diversity_application",
    display_name={"th": "วิเคราะห์ความหลากหลายในแง่วิวัฒนาการ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=EVOLUTION_TOPIC,
)
class EvolutionDiversityApplication(QuestionType):
    """Correct an account that has the direction of causation backwards."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, EVOLUTION_SCENARIOS,
            hint="ความแปรผันต้องมีอยู่ก่อน แล้วสิ่งแวดล้อมจึงคัดเลือก "
                 "สิ่งแวดล้อมไม่ได้สั่งให้ยีนเปลี่ยนตามความต้องการ",
        ), EVOLUTION_TOPIC)
