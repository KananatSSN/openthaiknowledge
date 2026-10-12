"""การเลือกวิธีคุมกำเนิด

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/16

Sets moved here from: science_wave_b13.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import LEVEL, SUBJECT, TOPIC, labelled, scenario_question
from otk.sets._support.science_wave_b13 import CONTRACEPTION_SCENARIOS

PROVENANCE = Provenance("original")


class Method(NamedTuple):
    """One method, how it works, and the need it answers better than the rest."""
    name: str
    mechanism: str
    best_for: str


# Each ``best_for`` names a different need. Two methods answering the same need
# would give the situation question two defensible answers.
CONTRACEPTION = (
    Method("ถุงยางอนามัย",
           "กั้นไม่ให้เซลล์อสุจิเข้าไปพบกับเซลล์ไข่",
           "ต้องการป้องกันทั้งการตั้งครรภ์และโรคติดต่อทางเพศสัมพันธ์ไปพร้อมกัน"),
    Method("ยาเม็ดคุมกำเนิด",
           "มีฮอร์โมนที่ยับยั้งการตกไข่ จึงไม่มีเซลล์ไข่ให้ปฏิสนธิ",
           "ต้องการคุมกำเนิดต่อเนื่อง และรับประทานยาได้เป็นเวลาทุกวัน"),
    Method("ยาฉีดคุมกำเนิด",
           "ฮอร์โมนที่ฉีดออกฤทธิ์ยับยั้งการตกไข่ได้นานหลายสัปดาห์ต่อการฉีดหนึ่งครั้ง",
           "ต้องการคุมกำเนิดโดยไม่ต้องจำว่าต้องทำสิ่งใดทุกวัน"),
    Method("ห่วงอนามัย",
           "เป็นอุปกรณ์ที่ใส่ไว้ในมดลูกเพื่อขัดขวางการฝังตัวของตัวอ่อน",
           "ต้องการคุมกำเนิดต่อเนื่องหลายปีโดยไม่ต้องทำสิ่งใดเพิ่มเติมระหว่างนั้น"),
    Method("การทำหมัน",
           "ผูกหรือตัดหลอดนำอสุจิหรือท่อนำไข่ เซลล์สืบพันธุ์จึงไม่มาพบกัน",
           "ตัดสินใจแล้วว่าจะไม่มีบุตรอีกอย่างถาวร"),
    Method("การนับระยะปลอดภัย",
           "หลีกเลี่ยงช่วงที่มีการตกไข่ โดยอาศัยการนับรอบประจำเดือน",
           "ต้องการวิธีที่ไม่ใช้ยาหรืออุปกรณ์ โดยยอมรับความไม่แน่นอนที่สูงกว่าวิธีอื่น"),
)


@question_type(
    "body.contraception_foundation",
    display_name={"th": "วิธีคุมกำเนิดและหลักการทำงาน"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ContraceptionFoundation(QuestionType):
    """How each method prevents a pregnancy."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CONTRACEPTION)
        others = [other for other in CONTRACEPTION if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return labelled(
                stem=f"“{item.name}” ป้องกันการตั้งครรภ์ด้วยหลักการใด",
                correct=item.mechanism,
                wrongs=tuple(other.mechanism for other in others[:3]),
                hint="แยกว่าวิธีนั้นกั้นไม่ให้เซลล์สืบพันธุ์พบกัน ยับยั้งการตกไข่ "
                     "หรือขัดขวางการฝังตัว",
            )
        return labelled(
            stem=f"วิธีคุมกำเนิดใดทำงานโดย{item.mechanism}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านหลักการให้จบก่อน แล้วจึงเลือกวิธีที่ทำงานตามหลักการนั้น",
        )


@question_type(
    "body.contraception_fluency",
    display_name={"th": "ความต้องการที่วิธีคุมกำเนิดแต่ละวิธีตอบได้"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ContraceptionFluency(QuestionType):
    """Match a method to the need it answers, in either direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CONTRACEPTION)
        others = [other for other in CONTRACEPTION if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return labelled(
                stem=f"“{item.name}” เหมาะกับผู้ที่มีความต้องการแบบใดมากที่สุด",
                correct=item.best_for,
                wrongs=tuple(other.best_for for other in others[:3]),
                hint="ดูว่าวิธีนั้นต้องทำอะไรบ่อยแค่ไหน ใช้ได้นานเพียงใด "
                     "และป้องกันโรคติดต่อได้หรือไม่",
            )
        return labelled(
            stem=f"ผู้ที่{item.best_for} ควรใช้วิธีคุมกำเนิดใด",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านความต้องการให้ครบทุกข้อ แล้วจึงเลือกวิธีที่ตอบได้ทั้งหมด",
        )


@question_type(
    "body.contraception_application",
    display_name={"th": "เลือกวิธีคุมกำเนิดให้เหมาะกับสถานการณ์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ContraceptionApplication(QuestionType):
    """Choose the method a described situation calls for, and say why.

    ``ม.2/16``'s verb is ``เลือก…ที่เหมาะสมกับสถานการณ์ที่กำหนด``, so this is the
    one set in the topic filed ``exact``: the situation is given and the choice
    has to be made.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, CONTRACEPTION_SCENARIOS,
            hint="อ่านเงื่อนไขในสถานการณ์ให้ครบ ทั้งระยะเวลาที่ต้องการ "
                 "ความสะดวกในการปฏิบัติ และการป้องกันโรค",
        )
