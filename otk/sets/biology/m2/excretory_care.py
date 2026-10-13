"""การดูแลรักษาระบบขับถ่าย

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/5

Sets moved here from: science_wave_b9.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import (
    EXCRETORY_CARE_SCENARIOS,
    LEVEL,
    SUBJECT,
    TOPIC,
    Care,
    Need,
    care_fluency,
    care_foundation,
    scenario_question,
)

PROVENANCE = Provenance("original")


EXCRETORY_CARE = (
    Care("ดื่มน้ำสะอาดให้เพียงพอในแต่ละวัน",
         "น้ำที่เพียงพอทำให้ไตขับของเสียออกได้โดยปัสสาวะไม่เข้มข้นจนสารบางชนิด"
         "ตกผลึกสะสมกลายเป็นนิ่ว"),
    Care("ไม่กลั้นปัสสาวะเป็นเวลานาน",
         "ปัสสาวะที่ค้างอยู่ในกระเพาะปัสสาวะนานเป็นแหล่งให้เชื้อโรคเจริญ "
         "และความดันที่ค้างไว้ยังย้อนขึ้นไปรบกวนการทำงานของไตได้"),
    Care("ลดอาหารรสเค็มจัด",
         "โซเดียมที่มากเกินไปทำให้ไตต้องทำงานหนักขึ้นในการขับส่วนเกิน "
         "และทำให้ร่างกายเก็บน้ำไว้มากจนความดันเลือดสูงขึ้น"),
    Care("ไม่ซื้อยาแก้ปวดมารับประทานเองติดต่อกันเป็นเวลานาน",
         "ยาหลายชนิดถูกขับออกทางไต การได้รับติดต่อกันนานจึงทำให้หน่วยไตเสียหายสะสม"),
    Care("รักษาความสะอาดของอวัยวะขับถ่ายอย่างถูกวิธี",
         "ลดโอกาสที่เชื้อโรคจะเข้าสู่ท่อปัสสาวะแล้วย้อนขึ้นไปถึงกระเพาะปัสสาวะและไต"),
    Care("ตรวจสุขภาพและตรวจปัสสาวะตามกำหนด",
         "ความผิดปกติของไตในระยะแรกมักไม่แสดงอาการ การตรวจจึงพบได้ก่อนที่หน่วยไต"
         "จะเสียหายไปมากจนแก้ไขไม่ได้"),
)


EXCRETORY_NEEDS = (
    Need("นักเรียนซ้อมกีฬากลางแดดทุกเย็นจนเหงื่อออกมาก และสังเกตว่าปัสสาวะมีสีเข้ม"
         "เกือบทุกวัน ควรปฏิบัติตามแนวทางใด",
         "ดื่มน้ำสะอาดให้เพียงพอในแต่ละวัน"),
    Need("นักเรียนไม่กล้าเข้าห้องน้ำที่โรงเรียนจึงอดทนไว้จนกลับถึงบ้านทุกวัน "
         "ควรปฏิบัติตามแนวทางใด",
         "ไม่กลั้นปัสสาวะเป็นเวลานาน"),
    Need("ที่บ้านของนักเรียนปรุงอาหารรสจัดและเติมน้ำปลาเพิ่มทุกมื้อ "
         "อีกทั้งผู้ใหญ่ในบ้านเริ่มมีความดันเลือดสูง ควรปฏิบัติตามแนวทางใด",
         "ลดอาหารรสเค็มจัด"),
    Need("นักเรียนปวดกล้ามเนื้อเรื้อรังและซื้อยาแก้ปวดจากร้านมารับประทานเองทุกวัน"
         "ติดต่อกันหลายเดือน ควรปฏิบัติตามแนวทางใด",
         "ไม่ซื้อยาแก้ปวดมารับประทานเองติดต่อกันเป็นเวลานาน"),
    Need("นักเรียนมีอาการแสบขณะปัสสาวะและปัสสาวะบ่อยเป็นครั้งที่สองในปีนี้ "
         "ควรปฏิบัติตามแนวทางใดเพื่อลดการเกิดซ้ำ",
         "รักษาความสะอาดของอวัยวะขับถ่ายอย่างถูกวิธี"),
    Need("ญาติสายตรงของนักเรียนหลายคนเป็นโรคไต แต่ตัวนักเรียนยังไม่มีอาการผิดปกติใด ๆ "
         "ควรปฏิบัติตามแนวทางใด",
         "ตรวจสุขภาพและตรวจปัสสาวะตามกำหนด"),
)


@question_type(
    "body.excretory_care_foundation",
    display_name={"th": "เหตุผลของแนวทางดูแลระบบขับถ่าย"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ExcretoryCareFoundation(QuestionType):
    """Why a habit protects the kidney and the urinary route."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return care_foundation(
            rng, system="ระบบขับถ่าย", cares=EXCRETORY_CARE,
            hint="โยงแนวทางกลับไปที่ความเข้มข้นของปัสสาวะ ภาระของหน่วยไต "
                 "หรือโอกาสที่เชื้อโรคจะเข้าสู่ทางเดินปัสสาวะ",
        )


@question_type(
    "body.excretory_care_fluency",
    display_name={"th": "เลือกแนวทางดูแลระบบขับถ่ายให้ตรงกับสถานการณ์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ExcretoryCareFluency(QuestionType):
    """State the แนวทาง the situation calls for.

    ``ม.2/5`` names its evidence as ``โดยการบอกแนวทางในการปฏิบัติตน…``, so this
    is the one set in the topic filed ``exact``.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return care_fluency(
            rng, needs=EXCRETORY_NEEDS, cares=EXCRETORY_CARE,
            hint="ระบุปัญหาในสถานการณ์ก่อน เช่น ปัสสาวะเข้มข้น ปัสสาวะค้าง "
                 "ภาระของไต หรือการติดเชื้อ แล้วจึงเลือกแนวทางที่ตรงกับปัญหานั้น",
        )


@question_type(
    "body.excretory_care_application",
    display_name={"th": "วิเคราะห์พฤติกรรมที่มีผลต่อไตและทางเดินปัสสาวะ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ExcretoryCareApplication(QuestionType):
    """Explain why a habit changes how the kidney works."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, EXCRETORY_CARE_SCENARIOS,
            hint="อธิบายด้วยกลไกจริงที่หน่วยไตหรือทางเดินปัสสาวะ "
                 "ไม่ใช่ด้วยความรู้สึกว่าพฤติกรรมนั้นดีหรือไม่ดี",
        )


# More practices, each with its own reason and the one situation it answers,
# so every practice still answers exactly one situation.
EXCRETORY_CARE += (
    Care('ไปพบแพทย์ทันทีเมื่อปัสสาวะแสบขัดหรือมีเลือดปน',
         'อาการเหล่านี้อาจเกิดจากการติดเชื้อหรือนิ่ว การรักษาแต่เนิ่น ๆ จึงป้องกันไม่ให้ลุกลามขึ้นไปถึงไต'),
    Care('ควบคุมระดับน้ำตาลในเลือดเมื่อเป็นเบาหวาน',
         'น้ำตาลในเลือดที่สูงเป็นเวลานานทำลายหลอดเลือดฝอยในหน่วยไต จนไตกรองของเสียได้น้อยลงเรื่อย ๆ'),
)
EXCRETORY_NEEDS += (
    Need('นักเรียนปัสสาวะแสบขัดและมีสีแดงคล้ายมีเลือดปนติดต่อกันมาสองวันแล้ว ควรปฏิบัติตามแนวทางใด',
         'ไปพบแพทย์ทันทีเมื่อปัสสาวะแสบขัดหรือมีเลือดปน'),
    Need('คุณตาเป็นเบาหวานแต่ไม่ค่อยกินยาตามที่แพทย์สั่ง และยังกินขนมหวานทุกวัน ควรแนะนำแนวทางใดเพื่อถนอมไต',
         'ควบคุมระดับน้ำตาลในเลือดเมื่อเป็นเบาหวาน'),
)
