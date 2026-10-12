"""อวัยวะในระบบสืบพันธุ์

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/12

Sets moved here from: science_wave_b12.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import LEVEL, SUBJECT, TOPIC, labelled, scenario_question
from otk.sets._support.science_wave_b12 import REPRODUCTIVE_SCENARIOS

PROVENANCE = Provenance("original")


class Organ(NamedTuple):
    """One reproductive organ and the single job it does."""
    name: str
    function: str


MALE_ORGANS = (
    Organ("อัณฑะ", "สร้างเซลล์อสุจิ และสร้างฮอร์โมนเพศชาย"),
    Organ("หลอดเก็บอสุจิ",
          "เป็นที่พักของเซลล์อสุจิจนเจริญเต็มที่และเคลื่อนที่ได้"),
    Organ("หลอดนำอสุจิ", "ลำเลียงเซลล์อสุจิจากหลอดเก็บอสุจิไปยังท่อปัสสาวะ"),
    Organ("ต่อมสร้างน้ำเลี้ยงอสุจิ",
          "สร้างของเหลวที่เป็นทั้งอาหารและตัวกลางให้เซลล์อสุจิเคลื่อนที่ได้"),
    Organ("ถุงหุ้มอัณฑะ",
          "รักษาอุณหภูมิของอัณฑะให้ต่ำกว่าอุณหภูมิภายในร่างกาย "
          "ซึ่งเป็นอุณหภูมิที่เหมาะกับการสร้างเซลล์อสุจิ"),
)


FEMALE_ORGANS = (
    Organ("รังไข่", "สร้างเซลล์ไข่ และสร้างฮอร์โมนเพศหญิง"),
    Organ("ท่อนำไข่",
          "เป็นทางที่เซลล์ไข่เคลื่อนไปยังมดลูก และเป็นบริเวณที่เกิดการปฏิสนธิ"),
    Organ("มดลูก", "เป็นที่ฝังตัวและเจริญเติบโตของตัวอ่อนจนคลอดเป็นทารก"),
    Organ("เยื่อบุมดลูก",
          "หนาตัวขึ้นเพื่อรองรับการฝังตัวของตัวอ่อน และหลุดลอกออกมาเป็นประจำเดือน"
          "เมื่อไม่มีการปฏิสนธิ"),
    Organ("ช่องคลอด",
          "เชื่อมระหว่างมดลูกกับภายนอกร่างกาย และเป็นทางออกของทารกเมื่อคลอด"),
)


# The two journeys, stored once each. Distractors for "what comes next" are drawn
# from both tables, so a learner has to know the sex as well as the order.
SPERM_PATH = ("อัณฑะ", "หลอดเก็บอสุจิ", "หลอดนำอสุจิ", "ท่อปัสสาวะ")


EGG_PATH = ("รังไข่", "ท่อนำไข่", "มดลูก")


@question_type(
    "body.reproductive_organs_foundation",
    display_name={"th": "อวัยวะในระบบสืบพันธุ์และหน้าที่"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ReproductiveOrgansFoundation(QuestionType):
    """Name an organ's job, or the organ that does a job.

    The two systems are drawn as separate tables. Offering มดลูก against a
    question about หลอดนำอสุจิ tests which word looks male, not the function.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        male = rng.random() < 0.5
        organs = MALE_ORGANS if male else FEMALE_ORGANS
        sex = "เพศชาย" if male else "เพศหญิง"
        item = rng.choice(organs)
        others = [other for other in organs if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return labelled(
                stem=f"“{item.name}” ทำหน้าที่ใดในระบบสืบพันธุ์",
                correct=item.function,
                wrongs=tuple(other.function for other in others[:3]),
                hint="แยกก่อนว่าอวัยวะนั้นสร้างเซลล์สืบพันธุ์ เป็นทางผ่าน "
                     "หรือเป็นที่เจริญเติบโตของตัวอ่อน",
            )
        return labelled(
            stem=f"อวัยวะใดในระบบสืบพันธุ์ของ{sex}ทำหน้าที่{item.function}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหน้าที่ให้จบก่อน แล้วจึงเลือกอวัยวะที่ทำหน้าที่นั้นโดยตรง",
        )


@question_type(
    "body.reproductive_organs_fluency",
    display_name={"th": "เส้นทางของเซลล์อสุจิและเซลล์ไข่"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ReproductiveOrgansFluency(QuestionType):
    """Follow each sex cell along its own route.

    Naming organs is Foundation work. The relation ``ม.2/12`` also asks for is how
    the organs connect, and that is the order of the two journeys.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        sperm = rng.random() < 0.5
        path = SPERM_PATH if sperm else EGG_PATH
        cell = "เซลล์อสุจิ" if sperm else "เซลล์ไข่"
        pool = [organ.name for organ in MALE_ORGANS + FEMALE_ORGANS]
        pool.append("ท่อปัสสาวะ")
        if rng.random() < 0.5:
            index = rng.randrange(len(path) - 1)
            current, following = path[index], path[index + 1]
            others = [name for name in pool if name != following]
            rng.shuffle(others)
            return labelled(
                stem=f"{cell}ที่ผ่าน “{current}” แล้วจะผ่านอวัยวะใดต่อไป",
                correct=following,
                wrongs=tuple(others[:3]),
                hint="ไล่จากอวัยวะที่สร้างเซลล์สืบพันธุ์ ออกไปตามทางผ่านทีละขั้น",
            )
        swapped = list(path)
        swapped[0], swapped[1] = swapped[1], swapped[0]
        extra = "ช่องคลอด" if sperm else "ต่อมสร้างน้ำเลี้ยงอสุจิ"
        return labelled(
            stem=f"ข้อใดเรียงลำดับเส้นทางของ{cell}ได้ถูกต้อง",
            correct=" → ".join(path),
            wrongs=(" → ".join(reversed(path)), " → ".join(swapped),
                    " → ".join((extra,) + path[1:])),
            hint="เริ่มที่อวัยวะที่สร้างเซลล์นั้นเสมอ แล้วจึงไล่ตามทางผ่าน",
        )


@question_type(
    "body.reproductive_model_application",
    display_name={"th": "ตีความแบบจำลองและการทำงานของระบบสืบพันธุ์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ReproductiveModelApplication(QuestionType):
    """Read a diagram of the system, then follow the organs into real cases."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, REPRODUCTIVE_SCENARIOS,
            hint="ถามว่าอวัยวะนั้นสร้างเซลล์สืบพันธุ์ เป็นทางผ่าน หรือเป็นที่ให้ตัวอ่อน"
                 "เจริญเติบโต แล้วจึงตามผลที่เกิดขึ้น",
        )
