"""การดูแลส่วนต่าง ๆ ของร่างกาย

ชีวะ · ป.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ป.1/2

Sets moved here from: science_wave_b14.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import (
    SUBJECT,
    Care,
    Need,
    care_fluency,
    care_foundation,
    scenario_question,
)
from otk.sets._support.science_wave_b14 import BODY_CARE_SCENARIOS, LIFE_TOPIC, PRIMARY_ONE

PROVENANCE = Provenance("original")


BODY_CARE = (
    Care("ล้างมือด้วยสบู่ก่อนรับประทานอาหารทุกครั้ง",
         "มือที่หยิบจับสิ่งของมีเชื้อโรคติดอยู่ การล้างมือจึงไม่ให้เชื้อโรคเข้าปาก"
         "ไปพร้อมกับอาหาร"),
    Care("แปรงฟันอย่างน้อยวันละสองครั้ง",
         "เศษอาหารที่ติดอยู่ตามซอกฟันทำให้ฟันผุ การแปรงฟันจึงทำให้ฟันสะอาด"
         "และใช้เคี้ยวอาหารได้นาน"),
    Care("ไม่นำสิ่งของแหลมคมมาเล่น และไม่แหย่สิ่งของเข้าหูหรือจมูก",
         "หู ตา และจมูกเป็นส่วนที่บอบบางมาก สิ่งของแหลมคมทำให้บาดเจ็บได้ง่าย"
         "และบางครั้งก็รักษาไม่หาย"),
    Care("อ่านหนังสือในที่ที่มีแสงสว่างพอ และพักสายตาเป็นระยะ",
         "การใช้สายตาในที่มืดเป็นเวลานานทำให้ตาล้าและมองเห็นได้ไม่ชัด"),
    Care("ไม่ฟังเสียงดังมากเป็นเวลานาน",
         "เสียงที่ดังเกินไปทำให้หูได้ยินเสียงแย่ลง และถ้าฟังนาน ๆ ก็อาจไม่กลับมา"
         "เหมือนเดิม"),
    Care("ตัดเล็บให้สั้นและสะอาดอยู่เสมอ",
         "เล็บที่ยาวเก็บสิ่งสกปรกไว้ข้างใต้ และอาจข่วนผิวหนังของตนเองหรือผู้อื่น"
         "จนเป็นแผลได้"),
)


BODY_CARE_NEEDS = (
    Need("นักเรียนเพิ่งเล่นกับสัตว์เลี้ยงเสร็จ แล้วจะมารับประทานขนม ควรทำอย่างไร",
         "ล้างมือด้วยสบู่ก่อนรับประทานอาหารทุกครั้ง"),
    Need("นักเรียนรับประทานขนมหวานแล้วมีเศษขนมติดอยู่ตามซอกฟัน ควรทำอย่างไร",
         "แปรงฟันอย่างน้อยวันละสองครั้ง"),
    Need("เพื่อนชวนนักเรียนเอาปลายดินสอแหย่เข้าไปในหูเล่น ควรทำอย่างไร",
         "ไม่นำสิ่งของแหลมคมมาเล่น และไม่แหย่สิ่งของเข้าหูหรือจมูก"),
    Need("นักเรียนอ่านหนังสือในห้องที่ปิดไฟจนรู้สึกแสบตาและปวดตา ควรทำอย่างไร",
         "อ่านหนังสือในที่ที่มีแสงสว่างพอ และพักสายตาเป็นระยะ"),
    Need("นักเรียนใส่หูฟังเปิดเสียงดังมากติดต่อกันหลายชั่วโมงทุกวัน ควรทำอย่างไร",
         "ไม่ฟังเสียงดังมากเป็นเวลานาน"),
    Need("เล็บของนักเรียนยาวจนมีคราบดำอยู่ข้างใต้ และเผลอข่วนหน้าตัวเองเป็นรอย "
         "ควรทำอย่างไร",
         "ตัดเล็บให้สั้นและสะอาดอยู่เสมอ"),
)


@question_type(
    "life.body_care_foundation",
    display_name={"th": "เหตุผลของการดูแลส่วนต่าง ๆ ของร่างกาย"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=LIFE_TOPIC,
)
class BodyCareFoundation(QuestionType):
    """Why looking after a part keeps it working."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        question = care_foundation(
            rng, system="ร่างกายของเรา", cares=BODY_CARE,
            hint="นึกว่าส่วนนั้นทำหน้าที่อะไร แล้วถ้าไม่ดูแลจะเกิดอะไรขึ้นกับหน้าที่นั้น",
        )
        return GeneratedQuestion(
            stem=question.stem, correct=question.correct,
            distractors=question.distractors, topic=LIFE_TOPIC, hint=question.hint,
        )


@question_type(
    "life.body_care_fluency",
    display_name={"th": "เลือกวิธีดูแลร่างกายให้ตรงกับสถานการณ์"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=LIFE_TOPIC,
)
class BodyCareFluency(QuestionType):
    """Pick the way of looking after oneself the situation calls for.

    ``ป.1/2``'s evidence clause is ``โดยการดูแลส่วนต่าง ๆ`` — conduct, so this set
    is ``standard_scope`` even though it is the closest an item gets.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        question = care_fluency(
            rng, needs=BODY_CARE_NEEDS, cares=BODY_CARE,
            hint="ดูว่าสถานการณ์นี้กำลังจะทำให้ส่วนใดของร่างกายสกปรกหรือเจ็บ",
        )
        return GeneratedQuestion(
            stem=question.stem, correct=question.correct,
            distractors=question.distractors, topic=LIFE_TOPIC, hint=question.hint,
        )


@question_type(
    "life.body_care_application",
    display_name={"th": "วิเคราะห์การดูแลร่างกายในชีวิตประจำวัน"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=LIFE_TOPIC,
)
class BodyCareApplication(QuestionType):
    """Judge a piece of everyday advice about looking after the body."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        question = scenario_question(
            rng, BODY_CARE_SCENARIOS,
            hint="ตรวจว่าคำแนะนำนั้นช่วยให้ส่วนของร่างกายทำหน้าที่ได้ดีขึ้นจริงหรือไม่",
        )
        return GeneratedQuestion(
            stem=question.stem, correct=question.correct,
            distractors=question.distractors, topic=LIFE_TOPIC, hint=question.hint,
        )


# More practices, each with its own reason and the one situation it answers,
# so every practice still answers exactly one situation.
BODY_CARE += (
    Care('อาบน้ำทำความสะอาดร่างกายทุกวัน',
         'เหงื่อและฝุ่นที่ติดผิวหนังทำให้เกิดกลิ่นและผื่นคัน การอาบน้ำช่วยให้ผิวสะอาด'),
    Care('สวมหมวกหรือกางร่มเมื่อออกไปกลางแดดจัด',
         'แสงแดดที่แรงจัดทำให้ผิวหนังแดงแสบ และทำให้ตาพร่ามัว'),
)
BODY_CARE_NEEDS += (
    Need('นักเรียนเล่นฟุตบอลจนเหงื่อออกทั้งตัวและเปื้อนฝุ่น แล้วจะเข้านอนทันที ควรทำอย่างไร',
         'อาบน้ำทำความสะอาดร่างกายทุกวัน'),
    Need('นักเรียนต้องเดินกลับบ้านตอนเที่ยงวันที่แดดร้อนจัด ควรทำอย่างไร',
         'สวมหมวกหรือกางร่มเมื่อออกไปกลางแดดจัด'),
)
