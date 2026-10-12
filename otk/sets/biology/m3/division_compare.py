"""ไมโทซิสและไมโอซิส

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.3/4

Sets moved here from: science_wave_b26.
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
from otk.sets._support.science_wave_b25 import MIDDLE_THREE
from otk.sets._support.science_wave_b26 import DIVISION_SCENARIOS

PROVENANCE = Provenance("original")


DIVISION_TOPIC = "การแบ่งเซลล์"


class Aspect(NamedTuple):
    """One aspect on which the two kinds of division differ."""
    aspect: str
    mitosis: str
    meiosis: str


ASPECTS = (
    Aspect("จำนวนครั้งที่แบ่ง",
           "แบ่งหนึ่งครั้ง", "แบ่งสองครั้งต่อเนื่องกัน"),
    Aspect("จำนวนเซลล์ลูกที่ได้",
           "ได้เซลล์ลูกสองเซลล์", "ได้เซลล์ลูกสี่เซลล์"),
    Aspect("จำนวนโครโมโซมในเซลล์ลูก",
           "เท่ากับเซลล์ตั้งต้น", "เป็นครึ่งหนึ่งของเซลล์ตั้งต้น"),
    Aspect("ความเหมือนกันของเซลล์ลูก",
           "เซลล์ลูกมีสารพันธุกรรมเหมือนเซลล์ตั้งต้นทุกประการ",
           "เซลล์ลูกมีสารพันธุกรรมต่างกันและต่างจากเซลล์ตั้งต้น"),
    Aspect("การเข้าคู่และแลกเปลี่ยนชิ้นส่วนของโครโมโซม",
           "ไม่เกิดขึ้น", "เกิดขึ้นในระยะแรกของการแบ่ง"),
    Aspect("บทบาทต่อสิ่งมีชีวิต",
           "ใช้ในการเจริญเติบโตและการซ่อมแซมส่วนที่สึกหรอ",
           "ใช้สร้างเซลล์สืบพันธุ์"),
)


class Situation(NamedTuple):
    """A place division happens, and which kind it is with the reason."""
    where: str
    verdict: str


SITUATIONS = (
    Situation("แผลที่ผิวหนังค่อย ๆ สมานจนปิดสนิท",
              "ไมโทซิส เพราะต้องสร้างเซลล์ผิวหนังใหม่ที่เหมือนเซลล์เดิมทุกประการ"),
    Situation("อัณฑะสร้างอสุจิ",
              "ไมโอซิส เพราะเซลล์สืบพันธุ์ต้องมีโครโมโซมเพียงครึ่งหนึ่ง"
              "ของเซลล์ร่างกาย"),
    Situation("รังไข่สร้างเซลล์ไข่",
              "ไมโอซิส เพราะเซลล์ไข่ต้องมีโครโมโซมครึ่งหนึ่ง "
              "เมื่อรวมกับอสุจิแล้วจะได้จำนวนครบตามเดิม"),
    Situation("ปลายรากของพืชยืดยาวขึ้นเรื่อย ๆ",
              "ไมโทซิส เพราะเป็นการเพิ่มจำนวนเซลล์เพื่อการเจริญเติบโต"),
    Situation("ไซโกตแบ่งตัวจากหนึ่งเซลล์เป็นสองและสี่เซลล์หลังการปฏิสนธิ",
              "ไมโทซิส เพราะเซลล์ทุกเซลล์ของตัวอ่อนต้องมีสารพันธุกรรมชุดเดียวกัน"),
    Situation("อับเรณูของดอกไม้สร้างละอองเรณู",
              "ไมโอซิส เพราะละอองเรณูทำหน้าที่เป็นเซลล์สืบพันธุ์เพศผู้ของพืช"),
)


@question_type(
    "cell.division_compare_foundation",
    display_name={"th": "ไมโทซิสและไมโอซิสต่างกันอย่างไร"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=DIVISION_TOPIC,
)
class DivisionCompareFoundation(QuestionType):
    """State the difference on one aspect — ``อธิบายความแตกต่าง`` itself."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ASPECTS)
        others = [other for other in ASPECTS if other.aspect != item.aspect]
        rng.shuffle(others)
        if rng.random() < 0.5:
            # One kind, one true statement; the three others are the other kind's
            # value on three other aspects, so each is plainly wrong for this kind.
            meiosis = rng.random() < 0.5
            kind = "ไมโอซิส" if meiosis else "ไมโทซิส"
            own = item.meiosis if meiosis else item.mitosis
            return _labelled(
                stem=f"ข้อใดกล่าวถึง “{kind}” ได้ถูกต้อง",
                correct=f"{item.aspect}: {own}",
                wrongs=tuple(f"{other.aspect}: {other.mitosis if meiosis else other.meiosis}"
                             for other in others[:3]),
                hint="จำหลักไว้ว่าไมโทซิสรักษาจำนวนโครโมโซมไว้เท่าเดิม "
                     "ส่วนไมโอซิสลดลงครึ่งหนึ่งเพื่อสร้างเซลล์สืบพันธุ์",
                topic=DIVISION_TOPIC,
            )
        first, second = rng.choice((("ไมโทซิส", "ไมโอซิส"), ("ไมโอซิส", "ไมโทซิส")))
        one, two = ((item.mitosis, item.meiosis) if first == "ไมโทซิส"
                    else (item.meiosis, item.mitosis))
        return _labelled(
            stem=f"ในด้าน “{item.aspect}” {first}กับ{second}ต่างกันอย่างไร",
            correct=f"{first}{one} ส่วน{second}{two}",
            wrongs=(f"{first}{two} ส่วน{second}{one}",
                    f"ทั้ง{first}และ{second}ต่าง{one}",
                    f"ทั้ง{first}และ{second}ต่าง{two}"),
            hint="จำหลักไว้ว่าไมโทซิสรักษาจำนวนโครโมโซมไว้เท่าเดิม "
                 "ส่วนไมโอซิสลดลงครึ่งหนึ่งเพื่อสร้างเซลล์สืบพันธุ์",
            topic=DIVISION_TOPIC,
        )


@question_type(
    "cell.division_compare_fluency",
    display_name={"th": "ระบุชนิดของการแบ่งเซลล์จากสถานการณ์"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=DIVISION_TOPIC,
)
class DivisionCompareFluency(QuestionType):
    """Say which division a described case is, and why it must be that one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(SITUATIONS)
        others = [other.verdict for other in SITUATIONS
                  if other.verdict != item.verdict]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.where}” อาศัยการแบ่งเซลล์แบบใด และเพราะเหตุใด",
            correct=item.verdict, wrongs=tuple(others[:3]),
            hint="ถามว่าเซลล์ที่ได้เป็นเซลล์ร่างกายหรือเซลล์สืบพันธุ์",
            topic=DIVISION_TOPIC,
        )


@question_type(
    "cell.division_compare_application",
    display_name={"th": "วิเคราะห์ผลของการแบ่งเซลล์สองแบบ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=DIVISION_TOPIC,
)
class DivisionCompareApplication(QuestionType):
    """Trace a consequence back to which division produced it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, DIVISION_SCENARIOS,
            hint="ตามจำนวนโครโมโซมไปทีละขั้น และถามว่าเซลล์ที่ได้จะถูกใช้ทำอะไร",
        ), DIVISION_TOPIC)
