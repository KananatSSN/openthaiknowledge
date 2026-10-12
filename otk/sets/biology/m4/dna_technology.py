"""ผลของเทคโนโลยีทางดีเอ็นเอ

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.4/5

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
from otk.sets._support.science_wave_b30 import DNA_TECH_SCENARIOS

PROVENANCE = Provenance("original")


DNA_TECH_TOPIC = "เทคโนโลยีทางดีเอ็นเอ"


class Tech(NamedTuple):
    """A DNA technology, what it does, and the effect it has and on whom."""
    name: str
    what: str
    effect: str


TECHNOLOGIES = (
    Tech("การตรวจลายพิมพ์ดีเอ็นเอ",
         "เปรียบเทียบรูปแบบของลำดับดีเอ็นเอบางช่วงที่ต่างกันมากระหว่างบุคคล",
         "ต่อมนุษย์ ช่วยยืนยันตัวบุคคลในคดีความและการพิสูจน์ความสัมพันธ์ทางสายเลือด "
         "แต่ก็ทำให้เกิดคำถามเรื่องความเป็นส่วนตัวของข้อมูลพันธุกรรม"),
    Tech("การผลิตยาด้วยจุลินทรีย์ดัดแปรพันธุกรรม",
         "ใส่ยีนของมนุษย์เข้าไปในแบคทีเรียหรือยีสต์ให้ผลิตโปรตีนที่ต้องการ",
         "ต่อมนุษย์ ทำให้ได้ยาอย่างอินซูลินและฮอร์โมนการเจริญเติบโตในราคาถูกลง"
         "และปลอดภัยกว่าการสกัดจากสัตว์"),
    Tech("การตรวจวินิจฉัยโรคทางพันธุกรรมด้วยดีเอ็นเอ",
         "ตรวจหาการเปลี่ยนแปลงของยีนที่ทราบว่าเกี่ยวข้องกับโรคโดยตรง",
         "ต่อมนุษย์ ทำให้วินิจฉัยได้เร็วและวางแผนการรักษาหรือการมีบุตรได้ "
         "แต่ต้องมีการให้คำปรึกษาควบคู่ไปด้วยเพื่อไม่ให้เกิดการเลือกปฏิบัติ"),
    Tech("ยีนบำบัด",
         "ใส่ยีนที่ทำงานได้เข้าไปในเซลล์ของผู้ป่วยเพื่อทดแทนยีนที่ผิดปกติ",
         "ต่อมนุษย์ เปิดโอกาสรักษาโรคทางพันธุกรรมที่เดิมทำได้เพียงประคับประคอง "
         "แต่ยังมีความเสี่ยงจากตำแหน่งที่ยีนเข้าไปแทรกและมีค่าใช้จ่ายสูงมาก"),
    Tech("การใช้จุลินทรีย์ดัดแปรพันธุกรรมบำบัดมลพิษ",
         "ใส่ยีนที่สร้างเอนไซม์ย่อยสลายสารมลพิษเข้าไปในจุลินทรีย์",
         "ต่อสิ่งแวดล้อม ช่วยย่อยสลายคราบน้ำมันและสารพิษได้เร็วขึ้น "
         "แต่ต้องควบคุมไม่ให้จุลินทรีย์แพร่กระจายและกระทบจุลินทรีย์ท้องถิ่น"),
    Tech("การสร้างพืชดัดแปรพันธุกรรมให้ต้านทานศัตรูพืช",
         "ใส่ยีนที่สร้างสารต้านแมลงหรือยีนต้านทานโรคเข้าไปในพืชปลูก",
         "ต่อสิ่งแวดล้อม ช่วยลดการใช้สารกำจัดแมลงลงได้ "
         "แต่ยีนอาจถ่ายเรณูไปยังพืชพันธุ์พื้นเมืองและแมลงอาจปรับตัวจนทนได้"),
)


@question_type(
    "life.dna_technology_foundation",
    display_name={"th": "เทคโนโลยีทางดีเอ็นเอทำอะไรได้บ้าง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=DNA_TECH_TOPIC,
)
class DnaTechnologyFoundation(QuestionType):
    """What each technology does — the searched-up side of ``ม.4/5``."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(TECHNOLOGIES)
        others = [other for other in TECHNOLOGIES if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” ทำอะไร",
                correct=item.what,
                wrongs=tuple(other.what for other in others[:3]),
                hint="ถามว่ายีนถูกย้ายเข้าไปในสิ่งมีชีวิตใด "
                     "หรือเป็นเพียงการอ่านและเปรียบเทียบลำดับดีเอ็นเอ",
                topic=DNA_TECH_TOPIC,
            )
        return _labelled(
            stem=f"เทคโนโลยีทางดีเอ็นเอใดทำโดย{item.what}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านวิธีการให้จบก่อน แล้วจึงเลือกชื่อเทคโนโลยีที่ตรงกัน",
            topic=DNA_TECH_TOPIC,
        )


@question_type(
    "life.dna_technology_fluency",
    display_name={"th": "ผลของเทคโนโลยีทางดีเอ็นเอต่อมนุษย์และสิ่งแวดล้อม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=DNA_TECH_TOPIC,
)
class DnaTechnologyFluency(QuestionType):
    """State the effect, on the party the indicator names.

    Every answer carries both the benefit and the concern, because ``ม.4/5`` asks
    for ``ผล`` and an answer that names only the upside is not the whole of it.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(TECHNOLOGIES)
        others = [other.effect for other in TECHNOLOGIES
                  if other.effect != item.effect]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.name}” ส่งผลต่อมนุษย์หรือสิ่งแวดล้อมอย่างไร",
            correct=item.effect, wrongs=tuple(others[:3]),
            hint="ตัวเลือกที่ถูกต้องต้องระบุทั้งผู้ที่ได้รับผล "
                 "ประโยชน์ที่เกิดขึ้น และสิ่งที่ต้องเฝ้าระวัง",
            topic=DNA_TECH_TOPIC,
        )


@question_type(
    "life.dna_technology_application",
    display_name={"th": "อภิปรายผลของเทคโนโลยีทางดีเอ็นเอ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=DNA_TECH_TOPIC,
)
class DnaTechnologyApplication(QuestionType):
    """Weigh a use of DNA technology against its benefits and its risks."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, DNA_TECH_SCENARIOS,
            hint="ระบุก่อนว่าผลตกอยู่กับมนุษย์หรือสิ่งแวดล้อม "
                 "แล้วจึงชั่งประโยชน์กับสิ่งที่ต้องเฝ้าระวังไปพร้อมกัน",
        ), DNA_TECH_TOPIC)
