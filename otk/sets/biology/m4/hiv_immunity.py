"""ภาวะภูมิคุ้มกันบกพร่องจากการติดเชื้อเอชไอวี

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/7

Sets moved here from: science_wave_b21.
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
from otk.sets._support.science_wave_b20 import IMMUNE_TOPIC
from otk.sets._support.science_wave_b21 import HIV_SCENARIOS

PROVENANCE = Provenance("original")


HIV_FACTS = (
    Fact("เชื้อเอชไอวีเข้าทำลายเซลล์ชนิดใดของระบบภูมิคุ้มกัน",
         "เซลล์ทีผู้ช่วย ซึ่งเป็นเซลล์ที่คอยกระตุ้นเซลล์อื่นให้ทำงาน"
         "ในการตอบสนองแบบจำเพาะ"),
    Fact("เหตุใดการติดเชื้อเอชไอวีจึงทำให้ภูมิคุ้มกันบกพร่อง",
         "เมื่อเซลล์ทีผู้ช่วยลดจำนวนลงเรื่อย ๆ ทั้งเซลล์บีและเซลล์ทีพิฆาต"
         "ก็ถูกกระตุ้นให้ทำงานไม่ได้ตามปกติ การตอบสนองแบบจำเพาะจึงอ่อนแอลง"),
    Fact("การติดเชื้อเอชไอวีต่างจากโรคเอดส์อย่างไร",
         "การติดเชื้อเอชไอวีคือการมีเชื้ออยู่ในร่างกาย ส่วนโรคเอดส์คือระยะที่"
         "เซลล์ทีผู้ช่วยลดลงมากจนเกิดโรคติดเชื้อฉวยโอกาสหรือมะเร็งบางชนิด"),
    Fact("โรคติดเชื้อฉวยโอกาสหมายถึงอะไร",
         "โรคที่เกิดจากเชื้อซึ่งปกติไม่ก่อโรคในผู้ที่มีภูมิคุ้มกันปกติ "
         "แต่ก่อโรครุนแรงได้เมื่อภูมิคุ้มกันบกพร่อง"),
    Fact("เชื้อเอชไอวีถ่ายทอดจากคนสู่คนได้ทางใดบ้าง",
         "ทางเลือด ทางการมีเพศสัมพันธ์ที่ไม่ได้ป้องกัน "
         "และจากแม่สู่ลูกในระหว่างตั้งครรภ์ คลอด หรือให้นม"),
    Fact("ยาต้านไวรัสเอชไอวีออกฤทธิ์อย่างไร",
         "ยับยั้งการเพิ่มจำนวนของเชื้อ ปริมาณเชื้อในเลือดจึงลดลงและจำนวน"
         "เซลล์ทีผู้ช่วยกลับสูงขึ้นได้ แต่ยังกำจัดเชื้อออกจากร่างกายไม่ได้"),
    Fact("การติดตามผู้ติดเชื้อเอชไอวีอาศัยค่าใดเป็นหลัก",
         "จำนวนเซลล์ทีผู้ช่วยในเลือด ซึ่งบอกว่าภูมิคุ้มกันเหลืออยู่เพียงใด "
         "ร่วมกับปริมาณสารพันธุกรรมของไวรัสในเลือด"),
)


class Contact(NamedTuple):
    """A kind of contact, and the verdict on it with the reason behind it."""
    situation: str
    verdict: str


CONTACTS = (
    Contact("ใช้เข็มฉีดยาร่วมกับผู้อื่น",
            "มีโอกาสรับเชื้อ เพราะเลือดที่ค้างอยู่ในเข็มเข้าสู่กระแสเลือดโดยตรง"),
    Contact("มีเพศสัมพันธ์โดยไม่ใช้ถุงยางอนามัย",
            "มีโอกาสรับเชื้อ เพราะเชื้อในสารคัดหลั่งผ่านเยื่อบุเข้าสู่ร่างกายได้"),
    Contact("แม่ที่ติดเชื้อให้นมบุตรโดยไม่ได้รับยาต้านไวรัส",
            "มีโอกาสรับเชื้อ เพราะเชื้อผ่านทางน้ำนมไปสู่ทารกได้"),
    Contact("รับประทานอาหารร่วมสำรับกับผู้ติดเชื้อ",
            "ไม่มีโอกาสรับเชื้อ เพราะเชื้อไม่ถ่ายทอดทางน้ำลายหรืออาหาร"),
    Contact("ใช้สระว่ายน้ำหรือห้องน้ำร่วมกับผู้ติดเชื้อ",
            "ไม่มีโอกาสรับเชื้อ เพราะเชื้ออยู่นอกร่างกายได้ไม่นานและไม่ถ่ายทอดทางน้ำ"),
    Contact("ถูกยุงที่เคยกัดผู้ติดเชื้อมากัด",
            "ไม่มีโอกาสรับเชื้อ เพราะเชื้อไม่เพิ่มจำนวนในยุงและไม่ถ่ายทอด"
            "ผ่านการกัดของยุง"),
    Contact("กอดหรือจับมือกับผู้ติดเชื้อ",
            "ไม่มีโอกาสรับเชื้อ เพราะผิวหนังที่ไม่มีบาดแผลกั้นเชื้อไว้ได้"),
)


@question_type(
    "body.hiv_immunity_foundation",
    display_name={"th": "ภาวะภูมิคุ้มกันบกพร่องจากการติดเชื้อเอชไอวี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=IMMUNE_TOPIC,
)
class HivImmunityFoundation(QuestionType):
    """What the virus destroys, and why that leaves the body defenceless."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, HIV_FACTS, topic=IMMUNE_TOPIC,
            hint="ตามให้ครบเป็นลูกโซ่ คือเชื้อทำลายเซลล์ใด "
                 "เซลล์นั้นเคยทำหน้าที่อะไร แล้วผลที่ตามมาคืออะไร",
        )


@question_type(
    "body.hiv_immunity_fluency",
    display_name={"th": "การถ่ายทอดเชื้อเอชไอวีและสิ่งที่ไม่ถ่ายทอด"},
    level=UPPER_FOUR, subject=SUBJECT, topic=IMMUNE_TOPIC,
)
class HivImmunityFluency(QuestionType):
    """Judge one contact — the verdict must come with the reason that fits it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CONTACTS)
        others = [other.verdict for other in CONTACTS
                  if other.verdict != item.verdict]
        rng.shuffle(others)
        return _labelled(
            stem=f"ข้อใดกล่าวถึงการ “{item.situation}” ได้ถูกต้อง",
            correct=item.verdict, wrongs=tuple(others[:3]),
            hint="ถามว่าเลือดหรือสารคัดหลั่งของผู้ติดเชื้อเข้าสู่ร่างกาย"
                 "อีกคนหนึ่งได้จริงหรือไม่",
            topic=IMMUNE_TOPIC,
        )


@question_type(
    "body.hiv_immunity_application",
    display_name={"th": "วิเคราะห์กรณีที่เกี่ยวกับการติดเชื้อเอชไอวี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=IMMUNE_TOPIC,
)
class HivImmunityApplication(QuestionType):
    """Read a result or a claim about HIV against how the virus actually works."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, HIV_SCENARIOS,
            hint="กลับไปที่ข้อเท็จจริงสองข้อ คือเชื้อทำลายเซลล์ทีผู้ช่วย "
                 "และเชื้อถ่ายทอดได้เพียงสามทางเท่านั้น",
        ), IMMUNE_TOPIC)
