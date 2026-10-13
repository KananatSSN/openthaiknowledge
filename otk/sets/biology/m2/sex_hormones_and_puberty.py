"""ฮอร์โมนเพศและการเปลี่ยนแปลงเมื่อเข้าสู่วัยหนุ่มสาว

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/13

Sets moved here from: science_wave_b12.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import LEVEL, SUBJECT, TOPIC, labelled, scenario_question
from otk.sets._support.science_wave_b12 import PUBERTY_SCENARIOS

PROVENANCE = Provenance("original")


class Fact(NamedTuple):
    """One question about the sex hormones, and its single answer."""
    question: str
    answer: str


HORMONE_FACTS = (
    Fact("ฮอร์โมนเพศชายมีชื่อว่าอะไร และสร้างขึ้นที่ใด",
         "เทสโทสเตอโรน สร้างขึ้นที่อัณฑะ"),
    Fact("ฮอร์โมนเพศหญิงหลักมีชื่อว่าอะไร และสร้างขึ้นที่ใด",
         "เอสโทรเจน สร้างขึ้นที่รังไข่"),
    Fact("ฮอร์โมนเพศเดินทางไปยังอวัยวะเป้าหมายได้อย่างไร",
         "ถูกลำเลียงไปตามกระแสเลือดจนถึงอวัยวะเป้าหมายทั่วร่างกาย"),
    Fact("การเปลี่ยนแปลงของร่างกายเมื่อเข้าสู่วัยหนุ่มสาวเกิดจากสิ่งใดโดยตรง",
         "ฮอร์โมนเพศที่หลั่งออกมามากขึ้นและไปออกฤทธิ์ที่อวัยวะเป้าหมาย"),
    Fact("เหตุใดแต่ละคนจึงเข้าสู่วัยหนุ่มสาวไม่พร้อมกัน",
         "ช่วงเวลาที่ฮอร์โมนเพศเริ่มหลั่งมากขึ้นแตกต่างกันไปในแต่ละบุคคล "
         "ซึ่งเป็นเรื่องปกติ ไม่ใช่ความผิดปกติ"),
    Fact("นอกจากควบคุมการเปลี่ยนแปลงของร่างกายแล้ว ฮอร์โมนเพศยังมีบทบาทใดอีก",
         "กระตุ้นให้อัณฑะสร้างเซลล์อสุจิ และให้รังไข่ปล่อยเซลล์ไข่เป็นรอบ ๆ"),
)


HORMONE_FACTS += (
    Fact('อวัยวะใดหลั่งฮอร์โมนไปกระตุ้นให้อัณฑะและรังไข่เริ่มสร้างฮอร์โมนเพศ',
         'ต่อมใต้สมอง ซึ่งอยู่ที่ฐานของสมองและหลั่งฮอร์โมนกระตุ้นต่อมเพศ'),
    Fact('เทสโทสเตอโรนทำให้เกิดการเปลี่ยนแปลงใดในเพศชาย',
         'เสียงแตก มีหนวดเครา กล้ามเนื้อเจริญ และไหล่กว้างขึ้น'),
    Fact('เอสโทรเจนทำให้เกิดการเปลี่ยนแปลงใดในเพศหญิง',
         'เต้านมขยาย สะโพกผาย และเริ่มมีรอบประจำเดือน'),
    Fact('เพศหญิงมีฮอร์โมนเทสโทสเตอโรนในร่างกายหรือไม่',
         'มีในปริมาณน้อย เช่นเดียวกับที่เพศชายมีเอสโทรเจนในปริมาณน้อย'),
)


MALE_HORMONE = "เทสโทสเตอโรน"


FEMALE_HORMONE = "เอสโทรเจน"


MALE_CHANGES = (
    "เสียงแตกห้าวขึ้นเพราะกล่องเสียงขยายใหญ่",
    "มีหนวดเคราขึ้นที่ใบหน้า",
    "ไหล่กว้างขึ้นและกล้ามเนื้อเจริญมากขึ้น",
    "อัณฑะเริ่มสร้างเซลล์อสุจิและเริ่มมีการหลั่งอสุจิ",
)


FEMALE_CHANGES = (
    "สะโพกผายกว้างขึ้นและมีไขมันสะสมใต้ผิวหนังมากขึ้น",
    "เต้านมขยายขนาดขึ้น",
    "รังไข่เริ่มปล่อยเซลล์ไข่และเริ่มมีประจำเดือน",
    "เยื่อบุมดลูกเริ่มหนาตัวและหลุดลอกเป็นรอบ ๆ",
)


# True of both sexes. These have no single defensible answer to "which sex", so
# they are never offered as a wrong choice there — they get their own question.
SHARED_CHANGES = (
    "ส่วนสูงเพิ่มขึ้นอย่างรวดเร็วในช่วงเวลาสั้น ๆ",
    "ต่อมไขมันและต่อมเหงื่อทำงานมากขึ้นจนเกิดสิวและกลิ่นกาย",
    "มีขนขึ้นบริเวณรักแร้และอวัยวะเพศ",
    "อารมณ์แปรปรวนง่ายกว่าเดิม",
)


@question_type(
    "body.sex_hormone_foundation",
    display_name={"th": "ฮอร์โมนเพศและแหล่งที่สร้าง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class SexHormoneFoundation(QuestionType):
    """What the sex hormones are, where they come from, and how they travel."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(HORMONE_FACTS)
        others = [other.answer for other in HORMONE_FACTS
                  if other.answer != item.answer]
        rng.shuffle(others)
        return labelled(
            stem=item.question, correct=item.answer, wrongs=tuple(others[:3]),
            hint="ฮอร์โมนเพศสร้างจากอวัยวะที่สร้างเซลล์สืบพันธุ์ "
                 "และออกฤทธิ์ที่อวัยวะเป้าหมายหลังเดินทางไปตามกระแสเลือด",
        )


@question_type(
    "body.puberty_change_fluency",
    display_name={"th": "การเปลี่ยนแปลงที่ควบคุมโดยฮอร์โมนเพศแต่ละชนิด"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PubertyChangeFluency(QuestionType):
    """Say which hormone brings about a change, or which changes are shared.

    Two hormones would give two choices if asked by name, so the item offers
    four changes instead. Changes true of both sexes are kept out of those
    choices and asked about separately.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            wrongs = list(MALE_CHANGES + FEMALE_CHANGES)
            rng.shuffle(wrongs)
            return labelled(
                stem="ข้อใดเป็นการเปลี่ยนแปลงในวัยหนุ่มสาวที่เกิดขึ้นทั้งในเพศชาย"
                     "และเพศหญิง",
                correct=rng.choice(SHARED_CHANGES),
                wrongs=tuple(wrongs[:3]),
                hint="การเปลี่ยนแปลงที่เกี่ยวกับเซลล์สืบพันธุ์หรือรูปร่างเฉพาะเพศ "
                     "จะเกิดกับเพศเดียว ส่วนการเติบโตและการทำงานของต่อมเกิดกับทั้งสองเพศ",
            )
        male = rng.random() < 0.5
        mine = MALE_CHANGES if male else FEMALE_CHANGES
        theirs = list(FEMALE_CHANGES if male else MALE_CHANGES)
        rng.shuffle(theirs)
        hormone = MALE_HORMONE if male else FEMALE_HORMONE
        return labelled(
            stem=f"ข้อใดเป็นการเปลี่ยนแปลงที่ควบคุมโดยฮอร์โมน “{hormone}”",
            correct=rng.choice(mine),
            wrongs=tuple(theirs[:3]),
            hint="เทสโทสเตอโรนสร้างจากอัณฑะและควบคุมลักษณะของเพศชาย "
                 "ส่วนเอสโทรเจนสร้างจากรังไข่และควบคุมลักษณะของเพศหญิง",
        )


@question_type(
    "body.puberty_application",
    display_name={"th": "วิเคราะห์ผลของฮอร์โมนเพศในวัยหนุ่มสาว"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PubertyApplication(QuestionType):
    """Explain a difference between two people by what the hormone does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, PUBERTY_SCENARIOS,
            hint="เริ่มที่ฮอร์โมนใดหลั่งเพิ่มขึ้นและออกฤทธิ์ที่อวัยวะใด "
                 "แล้วจึงดูว่าความต่างที่พบอยู่ในช่วงปกติหรือไม่",
        )
