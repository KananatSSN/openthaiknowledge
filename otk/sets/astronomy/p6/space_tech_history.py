"""พัฒนาการของเทคโนโลยีอวกาศและการนำมาใช้ประโยชน์

ดาราศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.6/2

Sets moved here from: science_wave_c3.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import PRIMARY_SIX
from otk.sets._support.science_wave_c1 import SKY_TOPIC, SUBJECT
from otk.sets._support.science_wave_c3 import SPACE_TECH_SCENARIOS

PROVENANCE = Provenance("original")


class Milestone(NamedTuple):
    """One step in the development of space technology, as a record would list it."""
    year: str
    event: str
    what: str


# A timeline the learner reads, in order. Each ``what`` names a different first,
# so no two rows answer the same question.
TIMELINE = (
    Milestone("พ.ศ. 2500", "ส่งดาวเทียมดวงแรกของโลกขึ้นสู่วงโคจร",
              "ดาวเทียมดวงแรกที่มนุษย์ส่งขึ้นไปโคจรรอบโลก"),
    Milestone("พ.ศ. 2504", "มนุษย์คนแรกเดินทางขึ้นไปโคจรรอบโลก",
              "การเดินทางขึ้นสู่อวกาศครั้งแรกของมนุษย์"),
    Milestone("พ.ศ. 2512", "มนุษย์ลงเหยียบพื้นผิวดวงจันทร์เป็นครั้งแรก",
              "การลงเหยียบดวงจันทร์ครั้งแรกของมนุษย์"),
    Milestone("พ.ศ. 2533", "ส่งกล้องโทรทรรศน์อวกาศขึ้นไปโคจรรอบโลก",
              "การนำกล้องโทรทรรศน์ขึ้นไปสังเกตนอกชั้นบรรยากาศ"),
    Milestone("พ.ศ. 2541", "เริ่มประกอบสถานีอวกาศนานาชาติในวงโคจร",
              "ที่อยู่อาศัยของมนุษย์ในอวกาศที่ใช้งานต่อเนื่อง"),
    Milestone("พ.ศ. 2555", "ส่งรถสำรวจขนาดใหญ่ลงสำรวจพื้นผิวดาวอังคาร",
              "การสำรวจพื้นผิวดาวเคราะห์ดวงอื่นด้วยรถสำรวจ"),
)


def _timeline() -> str:
    return " / ".join(f"{item.year} {item.event}" for item in TIMELINE)


class Use(NamedTuple):
    """One everyday use of space technology, and a situation that needs it."""
    technology: str
    situation: str
    because: str


# Each situation needs exactly one of these. A weather satellite also photographs
# a flood, so the survey row asks about land use instead, where no overlap can
# give a situation two answers.
USES = (
    Use("ดาวเทียมสื่อสาร",
        "ชมการถ่ายทอดสดการแข่งขันกีฬาจากต่างประเทศทางโทรทัศน์",
        "สัญญาณภาพและเสียงถูกส่งผ่านดาวเทียมข้ามทวีปมายังสถานีรับบนพื้นโลก"),
    Use("ดาวเทียมนำทาง",
        "ใช้แอปแผนที่ในโทรศัพท์บอกทางไปสถานที่ที่ไม่เคยไป",
        "เครื่องรับคำนวณตำแหน่งของเราจากสัญญาณเวลาที่ดาวเทียมหลายดวงส่งลงมา"),
    Use("ดาวเทียมอุตุนิยมวิทยา",
        "ดูภาพกลุ่มเมฆในพยากรณ์อากาศเพื่อรู้ว่าพรุ่งนี้ฝนจะตกหรือไม่",
        "ดาวเทียมถ่ายภาพกลุ่มเมฆและวัดอุณหภูมิของบรรยากาศจากด้านบนอย่างต่อเนื่อง"),
    Use("ดาวเทียมสำรวจทรัพยากร",
        "ทำแผนที่แสดงพื้นที่ป่าและพื้นที่เพาะปลูกของทั้งจังหวัด",
        "ดาวเทียมถ่ายภาพพื้นผิวโลกเป็นบริเวณกว้างซ้ำ ๆ จึงเห็นการใช้ที่ดินทั้งผืน"),
    Use("วัสดุที่พัฒนาขึ้นเพื่องานอวกาศ",
        "ใช้ที่นอนโฟมจำรูปและผ้าน้ำหนักเบาที่เก็บความอบอุ่นได้ดี",
        "วัสดุเหล่านี้พัฒนาขึ้นเพื่อใช้ในยานอวกาศก่อน แล้วจึงนำมาใช้ในชีวิตประจำวัน"),
    Use("กล้องถ่ายภาพขนาดเล็กความละเอียดสูง",
        "ถ่ายภาพด้วยกล้องเล็ก ๆ ในโทรศัพท์มือถือ",
        "กล้องขนาดเล็กที่กินไฟน้อยถูกพัฒนาขึ้นเพื่อติดไปกับยานอวกาศ"),
)


@question_type(
    "astro.space_tech_history_foundation",
    display_name={"th": "พัฒนาการของเทคโนโลยีอวกาศ"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=SKY_TOPIC,
)
class SpaceTechHistoryFoundation(QuestionType):
    """Describe how space technology developed, from a timeline in the stem.

    ``อธิบายพัฒนาการ`` and ``ยกตัวอย่างการนำมาใช้ประโยชน์`` are joined by ``และ``
    and carry objects of their own, so each earns an ``exact`` set. Both answer
    ``จากข้อมูลที่รวบรวมได้``: this one from the timeline printed in its stem.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem = ("นักเรียนรวบรวมข้อมูลพัฒนาการของเทคโนโลยีอวกาศ ได้ดังนี้ "
                f"{_timeline()} ")
        draw = rng.random()
        if draw < 0.35:
            item = rng.choice(TIMELINE)
            return _labelled(
                stem=stem + f"จากข้อมูลนี้ เหตุการณ์ใดเกิดขึ้นใน{item.year}",
                correct=item.event,
                wrongs=tuple([other.event for other in TIMELINE
                                         if other.year != item.year]),
                hint="หาปีที่โจทย์ถามในลำดับเวลา แล้วอ่านเหตุการณ์ที่เขียนไว้",
                topic=SKY_TOPIC,
            )
        if draw < 0.7:
            item = rng.choice(TIMELINE)
            return _labelled(
                stem=stem + f"จากข้อมูลนี้ “{item.what}” เกิดขึ้นในปีใด",
                correct=item.year,
                wrongs=tuple([other.year for other in TIMELINE
                                         if other.year != item.year]),
                hint="อ่านคำอธิบายแล้วหาเหตุการณ์ที่ตรงกันในลำดับเวลา",
                topic=SKY_TOPIC,
            )
        return _labelled(
            stem=stem + "จากข้อมูลนี้ ข้อใดสรุปพัฒนาการของเทคโนโลยีอวกาศได้ถูกต้อง",
            correct="เริ่มจากการส่งดาวเทียมขึ้นวงโคจร แล้วจึงส่งมนุษย์ขึ้นไป "
                    "ต่อมาจึงสำรวจดวงจันทร์ ดาวเคราะห์ดวงอื่น และสร้างที่อยู่อาศัยในอวกาศ",
            wrongs=("เริ่มจากการสำรวจพื้นผิวดาวอังคาร แล้วจึงย้อนกลับมาส่งดาวเทียมดวงแรก",
                    "เริ่มจากการสร้างสถานีอวกาศ แล้วจึงส่งมนุษย์คนแรกขึ้นสู่อวกาศ",
                    "เริ่มจากการส่งมนุษย์ไปดวงจันทร์ แล้วจึงเริ่มส่งดาวเทียมดวงแรก"),
            hint="เรียงเหตุการณ์ตามปีจากน้อยไปมาก แล้วดูว่าเรื่องใดมาก่อนเรื่องใด",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.space_tech_history_fluency",
    display_name={"th": "ยกตัวอย่างการใช้เทคโนโลยีอวกาศในชีวิตประจำวัน"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=SKY_TOPIC,
)
class SpaceTechHistoryFluency(QuestionType):
    """Name the space technology an everyday situation rests on, and why.

    This is the indicator's second free verb, ``ยกตัวอย่างการนำเทคโนโลยีอวกาศมาใช้
    ประโยชน์ในชีวิตประจำวัน``, so it is the second ``exact`` set.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(USES)
        others = [other for other in USES if other.technology != item.technology]
        rng.shuffle(others)
        draw = rng.random()
        if draw < 0.4:
            return _labelled(
                stem=f"“{item.situation}” อาศัยเทคโนโลยีอวกาศชนิดใด",
                correct=item.technology,
                wrongs=tuple(other.technology for other in others[:3]),
                hint="นึกว่าสิ่งที่ต้องส่งหรือรับในสถานการณ์นั้นคืออะไร",
                topic=SKY_TOPIC,
            )
        if draw < 0.7:
            return _labelled(
                stem=f"“{item.technology}” ถูกนำมาใช้ประโยชน์ในชีวิตประจำวันอย่างไร",
                correct=item.situation,
                wrongs=tuple(other.situation for other in others[:3]),
                hint="เลือกสถานการณ์ในชีวิตประจำวันที่ต้องใช้เทคโนโลยีชนิดนั้นโดยตรง",
                topic=SKY_TOPIC,
            )
        return _labelled(
            stem=f"เหตุใดการ “{item.situation}” จึงต้องอาศัย{item.technology}",
            correct=item.because,
            wrongs=tuple(other.because for other in others[:3]),
            hint="อธิบายว่าเทคโนโลยีนั้นทำอะไรให้ สถานการณ์จึงเป็นไปได้",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.space_tech_history_application",
    display_name={"th": "วิเคราะห์การใช้เทคโนโลยีอวกาศ"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=SKY_TOPIC,
)
class SpaceTechHistoryApplication(QuestionType):
    """Reason about a storm warning, a lost signal, and a source with no date."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SPACE_TECH_SCENARIOS,
            hint="ถามว่าสถานการณ์นั้นต้องใช้อะไรจากอวกาศ และข้อมูลที่ใช้เชื่อถือได้หรือไม่",
        ), SKY_TOPIC)
