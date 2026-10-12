"""โรคจากความผิดปกติของระบบภูมิคุ้มกัน

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/6

Sets moved here from: science_wave_b20.
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
from otk.sets._support.science_wave_b20 import DISORDER_SCENARIOS, IMMUNE_TOPIC

PROVENANCE = Provenance("original")


class Disorder(NamedTuple):
    """One immune disorder, what goes wrong, and a case that points to it."""
    name: str
    cause: str
    case: str


DISORDERS = (
    Disorder("โรคภูมิแพ้",
             "ระบบภูมิคุ้มกันตอบสนองรุนแรงเกินไปต่อสารที่ไม่เป็นอันตราย "
             "เช่น ไรฝุ่นหรือละอองเกสร",
             "ผู้ป่วยจามและคัดจมูกทุกครั้งที่ทำความสะอาดห้องที่มีฝุ่นมาก "
             "แต่ไม่มีไข้และหายเองเมื่อออกจากห้อง"),
    Disorder("ปฏิกิริยาแอนาไฟแล็กซิส",
             "การแพ้อย่างรุนแรงและรวดเร็วทั่วร่างกายหลังได้รับสารก่อภูมิแพ้ "
             "จนความดันเลือดตกและหลอดลมตีบ",
             "ผู้ป่วยหน้าบวม หายใจไม่ออก และความดันเลือดตกภายในไม่กี่นาที"
             "หลังถูกต่อต่อย"),
    Disorder("โรคเอสแอลอี",
             "ระบบภูมิคุ้มกันสร้างแอนติบอดีต่อเนื้อเยื่อของตนเองหลายระบบ "
             "จึงเกิดการอักเสบทั้งที่ผิวหนัง ข้อ และไต",
             "ผู้ป่วยมีผื่นรูปปีกผีเสื้อที่ใบหน้า ปวดข้อหลายข้อ "
             "และตรวจพบแอนติบอดีต่อสารพันธุกรรมของตนเอง"),
    Disorder("โรคข้ออักเสบรูมาตอยด์",
             "ภูมิคุ้มกันทำลายเยื่อบุข้อของตนเอง ทำให้ข้ออักเสบเรื้อรัง "
             "และข้อผิดรูปในระยะยาว",
             "ผู้ป่วยมีข้อนิ้วมือทั้งสองข้างบวมและฝืดในตอนเช้าติดต่อกันหลายเดือน "
             "จนข้อเริ่มผิดรูป"),
    Disorder("โรคเบาหวานชนิดที่ 1",
             "ภูมิคุ้มกันทำลายเซลล์ของตับอ่อนที่สร้างอินซูลิน "
             "ร่างกายจึงขาดอินซูลินอย่างถาวร",
             "เด็กอายุสิบปีผอมลงและปัสสาวะบ่อย ตรวจพบน้ำตาลในเลือดสูง "
             "และตับอ่อนสร้างอินซูลินได้น้อยมาก"),
    Disorder("ภาวะปฏิเสธอวัยวะที่ปลูกถ่าย",
             "ภูมิคุ้มกันจำแอนติเจนบนอวัยวะของผู้บริจาคว่าเป็นสิ่งแปลกปลอม "
             "จึงเข้าทำลายอวัยวะนั้น",
             "ผู้ป่วยที่ได้รับการปลูกถ่ายไตมีไข้และค่าการทำงานของไตแย่ลง"
             "หลังหยุดยากดภูมิคุ้มกันเอง"),
    Disorder("โรคหืด",
             "ทางเดินหายใจตอบสนองไวเกินต่อสิ่งกระตุ้น "
             "จนหลอดลมอักเสบเรื้อรังและตีบแคบลงเป็นครั้งคราว",
             "ผู้ป่วยหายใจมีเสียงหวีดและหอบเมื่ออยู่ในอากาศเย็นหรือได้กลิ่นควัน "
             "และดีขึ้นเมื่อใช้ยาขยายหลอดลม"),
)


@question_type(
    "body.immune_disorder_foundation",
    display_name={"th": "ความผิดปกติของระบบภูมิคุ้มกัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=IMMUNE_TOPIC,
)
class ImmuneDisorderFoundation(QuestionType):
    """Explain what goes wrong in each disorder — the ``อธิบาย`` of ``ม.4/6``."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DISORDERS)
        others = [other for other in DISORDERS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” เกิดจากความผิดปกติของระบบภูมิคุ้มกันอย่างไร",
                correct=item.cause,
                wrongs=tuple(other.cause for other in others[:3]),
                hint="แยกให้ออกว่าเป็นการตอบสนองที่มากเกินไปต่อสารภายนอก "
                     "หรือเป็นการทำลายเนื้อเยื่อของตนเอง",
                topic=IMMUNE_TOPIC,
            )
        return _labelled(
            stem=f"โรคหรือภาวะใดเกิดจากการที่{item.cause}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านสาเหตุให้จบก่อนว่าเป็นเนื้อเยื่อใดที่ถูกทำลาย "
                 "หรือสารใดที่กระตุ้น แล้วจึงเลือกโรค",
            topic=IMMUNE_TOPIC,
        )


@question_type(
    "body.immune_disorder_fluency",
    display_name={"th": "ยกตัวอย่างโรคจากความผิดปกติของระบบภูมิคุ้มกัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=IMMUNE_TOPIC,
)
class ImmuneDisorderFluency(QuestionType):
    """Name the disorder a described case points to — the ``ยกตัวอย่าง`` half."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DISORDERS)
        others = [other.name for other in DISORDERS if other.name != item.name]
        rng.shuffle(others)
        return _labelled(
            stem=f"{item.case} อาการนี้ตรงกับโรคหรือภาวะใดมากที่สุด",
            correct=item.name, wrongs=tuple(others[:3]),
            hint="ดูว่าอาการเกิดขึ้นเร็วเพียงใด เกิดกับอวัยวะใด "
                 "และมีสิ่งกระตุ้นจากภายนอกที่ระบุได้หรือไม่",
            topic=IMMUNE_TOPIC,
        )


@question_type(
    "body.immune_disorder_application",
    display_name={"th": "วิเคราะห์โรคจากความผิดปกติของระบบภูมิคุ้มกัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=IMMUNE_TOPIC,
)
class ImmuneDisorderApplication(QuestionType):
    """Compare disorders, or judge a claim about what an immune disorder means."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, DISORDER_SCENARIOS,
            hint="จัดกลุ่มก่อนว่าเป็นการตอบสนองมากเกินไปต่อสารภายนอก "
                 "การทำลายเนื้อเยื่อของตนเอง หรือการต้านเนื้อเยื่อจากผู้อื่น",
        ), IMMUNE_TOPIC)
