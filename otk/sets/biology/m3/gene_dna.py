"""ยีน ดีเอ็นเอ และโครโมโซม

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.3/1

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
from otk.sets._support.science_wave_b25 import GENE_SCENARIOS, MIDDLE_THREE

PROVENANCE = Provenance("original")


GENE_TOPIC = "ยีน ดีเอ็นเอ และโครโมโซม"


GENE_FACTS = (
    Fact("โครโมโซมคืออะไร",
         "โครงสร้างในนิวเคลียสที่เกิดจากดีเอ็นเอพันรอบโปรตีนแล้วขดแน่นขึ้น "
         "จนเห็นเป็นแท่งขณะที่เซลล์กำลังแบ่งตัว"),
    Fact("ดีเอ็นเอคืออะไร",
         "สารพันธุกรรมที่มีลักษณะเป็นสายยาวสองสายพันกันเป็นเกลียว "
         "และเก็บข้อมูลไว้ในลำดับของนิวคลีโอไทด์"),
    Fact("ยีนคืออะไร",
         "ช่วงหนึ่งของสายดีเอ็นเอที่ควบคุมลักษณะทางพันธุกรรมหนึ่งลักษณะ"),
    Fact("ยีน ดีเอ็นเอ และโครโมโซม สัมพันธ์กันอย่างไร",
         "ยีนเป็นช่วงหนึ่งบนสายดีเอ็นเอ และดีเอ็นเอขดตัวรวมกับโปรตีนเป็นโครโมโซม "
         "ทั้งสามจึงซ้อนกันอยู่ตั้งแต่หน่วยเล็กไปหาหน่วยใหญ่"),
    Fact("เซลล์ร่างกายของมนุษย์มีโครโมโซมกี่แท่ง",
         "มี 46 แท่ง หรือ 23 คู่ โดยแต่ละคู่ได้รับมาจากพ่อหนึ่งแท่งและ"
         "จากแม่หนึ่งแท่ง"),
    Fact("โครโมโซมคู่เหมือนหมายถึงอะไร",
         "โครโมโซมสองแท่งที่มีขนาดและตำแหน่งของยีนตรงกัน "
         "โดยแท่งหนึ่งมาจากพ่อและอีกแท่งหนึ่งมาจากแม่"),
    Fact("แอลลีลหมายถึงอะไร",
         "รูปแบบที่ต่างกันของยีนเดียวกัน ซึ่งอยู่ตรงตำแหน่งเดียวกัน"
         "บนโครโมโซมคู่เหมือน"),
)


class Model(NamedTuple):
    """A model a learner is handed, and what it correctly shows."""
    description: str
    reading: str


MODELS = (
    Model("นักเรียนใช้ด้ายยาวหนึ่งเส้นแทนดีเอ็นเอ พันด้ายรอบลูกปัดหลายเม็ด "
          "แล้วขดรวมกันจนเป็นก้อนหนึ่งก้อน",
          "ก้อนที่ได้แทนโครโมโซมหนึ่งแท่ง ด้ายแทนสายดีเอ็นเอ "
          "และลูกปัดแทนโปรตีนที่ดีเอ็นเอพันรอบ"),
    Model("นักเรียนใช้ริบบิ้นยาวแทนดีเอ็นเอ แล้วใช้ปากกาสีต่างกันระบายเป็นช่วง ๆ "
          "บนริบบิ้นเส้นเดียวกัน",
          "แต่ละช่วงสีแทนยีนหนึ่งยีน ซึ่งเป็นช่วงหนึ่งของสายดีเอ็นเอที่ควบคุม"
          "ลักษณะหนึ่งลักษณะ"),
    Model("นักเรียนใช้กล่องใหญ่แทนนิวเคลียส ใส่เส้นด้ายที่ขดเป็นก้อนไว้ข้างใน"
          "จำนวน 46 ก้อน",
          "กล่องแทนนิวเคลียสของเซลล์ร่างกายมนุษย์ และก้อนด้าย 46 ก้อน"
          "แทนโครโมโซม 46 แท่งในเซลล์นั้น"),
    Model("นักเรียนวางก้อนด้ายสองก้อนที่ยาวเท่ากันไว้เคียงกัน "
          "โดยระบายสีตรงตำแหน่งเดียวกันของทั้งสองก้อน",
          "ก้อนทั้งสองแทนโครโมโซมคู่เหมือน และตำแหน่งสีที่ตรงกัน"
          "แทนตำแหน่งของยีนเดียวกันบนโครโมโซมทั้งคู่"),
    Model("นักเรียนใช้ซิปที่รูดเข้าหากันได้แทนดีเอ็นเอ โดยฟันซิปสองฝั่ง"
          "จับคู่กันตลอดความยาว",
          "ฟันซิปที่จับคู่กันแทนนิวคลีโอไทด์ที่จับคู่กันระหว่างสายดีเอ็นเอสองสาย"),
    Model("นักเรียนวาดวงกลมใหญ่ ข้างในมีวงกลมเล็กหลายวง "
          "และในวงเล็กแต่ละวงมีจุดเรียงกันเป็นแถว",
          "วงใหญ่แทนโครโมโซม วงเล็กแทนยีนแต่ละยีนบนโครโมโซมนั้น "
          "และจุดที่เรียงกันแทนลำดับนิวคลีโอไทด์ภายในยีน"),
)


@question_type(
    "cell.gene_dna_foundation",
    display_name={"th": "ยีน ดีเอ็นเอ และโครโมโซม"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=GENE_TOPIC,
)
class GeneDnaFoundation(QuestionType):
    """The three terms, before any model is read."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, GENE_FACTS, topic=GENE_TOPIC,
            hint="เรียงจากหน่วยเล็กไปใหญ่เสมอ คือยีนอยู่บนดีเอ็นเอ "
                 "และดีเอ็นเอขดตัวเป็นโครโมโซม",
        )


@question_type(
    "cell.gene_dna_fluency",
    display_name={"th": "อ่านแบบจำลองยีน ดีเอ็นเอ และโครโมโซม"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=GENE_TOPIC,
)
class GeneDnaFluency(QuestionType):
    """Read a stated model — ``โดยใช้แบบจำลอง`` as an item can pose it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(MODELS)
        others = [other.reading for other in MODELS
                  if other.reading != item.reading]
        rng.shuffle(others)
        return _labelled(
            stem=f"{item.description} ข้อใดอธิบายแบบจำลองนี้ได้ถูกต้อง",
            correct=item.reading, wrongs=tuple(others[:3]),
            hint="จับคู่ทีละส่วนว่าของจริงส่วนใดถูกแทนด้วยวัสดุชิ้นใด "
                 "แล้วตรวจว่าลำดับจากเล็กไปใหญ่ถูกต้อง",
            topic=GENE_TOPIC,
        )


@question_type(
    "cell.gene_dna_application",
    display_name={"th": "วิเคราะห์แบบจำลองทางพันธุกรรม"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=GENE_TOPIC,
)
class GeneDnaApplication(QuestionType):
    """Judge a model's reach, or correct a claim about how the three nest."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, GENE_SCENARIOS,
            hint="ตรวจลำดับจากเล็กไปใหญ่ก่อน แล้วจึงถามว่าแบบจำลองนั้น"
                 "แสดงอะไรได้และแสดงอะไรไม่ได้",
        ), GENE_TOPIC)
