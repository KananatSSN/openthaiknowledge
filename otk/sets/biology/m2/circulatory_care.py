"""การดูแลรักษาระบบหมุนเวียนเลือด

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/9

Sets moved here from: science_wave_b11.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import (
    LEVEL,
    SUBJECT,
    TOPIC,
    Care,
    Need,
    care_fluency,
    care_foundation,
    scenario_question,
)
from otk.sets._support.science_wave_b11 import CIRCULATORY_CARE_SCENARIOS

PROVENANCE = Provenance("original")


CIRCULATORY_CARE = (
    Care("ออกกำลังกายแบบแอโรบิกอย่างสม่ำเสมอ",
         "กล้ามเนื้อหัวใจแข็งแรงขึ้นและสูบฉีดเลือดได้มากขึ้นในการเต้นแต่ละครั้ง "
         "หัวใจจึงทำงานน้อยครั้งลงขณะพัก"),
    Care("ลดอาหารที่มีไขมันอิ่มตัวและไขมันทรานส์",
         "ไขมันที่สะสมอยู่ในผนังหลอดเลือดแดงทำให้หลอดเลือดตีบและแข็งตัว "
         "เลือดจึงไหลผ่านไปเลี้ยงอวัยวะได้น้อยลง"),
    Care("ไม่สูบบุหรี่",
         "สารในควันบุหรี่ทำให้ผนังหลอดเลือดเสียหายและหลอดเลือดหดตัว "
         "ความดันเลือดจึงสูงขึ้นและเกิดการอุดตันได้ง่ายขึ้น"),
    Care("ควบคุมน้ำหนักตัวให้เหมาะสม",
         "น้ำหนักที่มากเกินไปทำให้มีเนื้อเยื่อที่ต้องเลี้ยงมากขึ้น "
         "หัวใจจึงต้องสูบฉีดเลือดหนักกว่าปกติอยู่ตลอดเวลา"),
    Care("ตรวจวัดความดันเลือดเป็นระยะ",
         "ความดันเลือดสูงมักไม่แสดงอาการ แต่ทำให้ผนังหลอดเลือดและกล้ามเนื้อหัวใจ"
         "เสียหายสะสม การวัดจึงทำให้พบได้ก่อนเกิดความเสียหาย"),
    Care("นอนหลับให้เพียงพอและจัดการความเครียด",
         "ความเครียดเรื้อรังทำให้หัวใจเต้นเร็วและความดันเลือดสูงค้างอยู่เป็นเวลานาน "
         "หัวใจและหลอดเลือดจึงไม่ได้พัก"),
)


CIRCULATORY_NEEDS = (
    Need("นักเรียนนั่งอยู่กับที่เกือบทั้งวันและเหนื่อยง่ายเมื่อต้องเดินเร็ว "
         "ต้องการให้หัวใจแข็งแรงขึ้น ควรปฏิบัติตามแนวทางใด",
         "ออกกำลังกายแบบแอโรบิกอย่างสม่ำเสมอ"),
    Need("ผลตรวจสุขภาพของผู้ใหญ่ในบ้านพบว่ามีไขมันในเลือดสูงและเริ่มมีคราบไขมัน"
         "เกาะผนังหลอดเลือด ควรปฏิบัติตามแนวทางใด",
         "ลดอาหารที่มีไขมันอิ่มตัวและไขมันทรานส์"),
    Need("เพื่อนของนักเรียนเริ่มทดลองสูบบุหรี่ตามกลุ่มเพื่อน และถามว่าจะมีผลต่อหัวใจ"
         "และหลอดเลือดอย่างไร ควรแนะนำแนวทางใด",
         "ไม่สูบบุหรี่"),
    Need("นักเรียนมีน้ำหนักเกินเกณฑ์มากและรู้สึกเหนื่อยแม้ขณะทำกิจกรรมเบา ๆ "
         "ควรปฏิบัติตามแนวทางใดเพื่อลดภาระของหัวใจ",
         "ควบคุมน้ำหนักตัวให้เหมาะสม"),
    Need("ญาติสายตรงของนักเรียนหลายคนเป็นโรคความดันเลือดสูง แต่ตัวนักเรียนยังไม่มี"
         "อาการผิดปกติใด ๆ ควรปฏิบัติตามแนวทางใด",
         "ตรวจวัดความดันเลือดเป็นระยะ"),
    Need("ในช่วงสอบ นักเรียนนอนดึกติดต่อกันหลายคืนและรู้สึกใจสั่นบ่อยครั้ง "
         "ควรปฏิบัติตามแนวทางใด",
         "นอนหลับให้เพียงพอและจัดการความเครียด"),
)


@question_type(
    "body.circulatory_care_foundation",
    display_name={"th": "เหตุผลของแนวทางดูแลระบบหมุนเวียนเลือด"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class CirculatoryCareFoundation(QuestionType):
    """Why a habit protects the heart and the vessels."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return care_foundation(
            rng, system="ระบบหมุนเวียนเลือด", cares=CIRCULATORY_CARE,
            hint="โยงแนวทางกลับไปที่ภาระของหัวใจ สภาพของผนังหลอดเลือด "
                 "หรือระดับความดันเลือด",
        )


@question_type(
    "body.circulatory_care_fluency",
    display_name={"th": "เลือกแนวทางดูแลระบบหมุนเวียนเลือดให้ตรงกับสถานการณ์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class CirculatoryCareFluency(QuestionType):
    """State the แนวทาง the situation calls for — ``ม.2/9``'s own evidence."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return care_fluency(
            rng, needs=CIRCULATORY_NEEDS, cares=CIRCULATORY_CARE,
            hint="ระบุปัญหาในสถานการณ์ก่อน เช่น หัวใจอ่อนแรง หลอดเลือดตีบ "
                 "ความดันสูง หรือหัวใจทำงานหนักเกินไป",
        )


@question_type(
    "body.circulatory_care_application",
    display_name={"th": "วิเคราะห์พฤติกรรมที่มีผลต่อหัวใจและหลอดเลือด"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class CirculatoryCareApplication(QuestionType):
    """Explain why a habit or a condition changes how the system works."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, CIRCULATORY_CARE_SCENARIOS,
            hint="อธิบายด้วยปริมาณเลือดที่ไหลผ่านและออกซิเจนที่เนื้อเยื่อต้องการ "
                 "ไม่ใช่ด้วยความรู้สึกว่าพฤติกรรมนั้นดีหรือไม่ดี",
        )


# More practices, each with its own reason and the one situation it answers,
# so every practice still answers exactly one situation.
CIRCULATORY_CARE += (
    Care('ลดเครื่องดื่มที่มีน้ำตาลสูงและอาหารหวานจัด',
         'น้ำตาลส่วนเกินถูกเปลี่ยนเป็นไขมันสะสมและเพิ่มความเสี่ยงของเบาหวาน ซึ่งทำลายผนังหลอดเลือดในระยะยาว'),
    Care('ลุกเดินหรือขยับขาเป็นระยะเมื่อต้องนั่งนาน',
         'การหดตัวของกล้ามเนื้อขาช่วยบีบหลอดเลือดดำให้เลือดไหลกลับสู่หัวใจ ลดการคั่งของเลือดที่ขา'),
)
CIRCULATORY_NEEDS += (
    Need('นักเรียนดื่มชานมไข่มุกและน้ำอัดลมรวมกันวันละหลายแก้ว ทั้งที่น้ำหนักตัวยังอยู่ในเกณฑ์ ควรปฏิบัติตามแนวทางใดเพื่อดูแลหลอดเลือด',
         'ลดเครื่องดื่มที่มีน้ำตาลสูงและอาหารหวานจัด'),
    Need('นักเรียนนั่งเรียนออนไลน์หน้าคอมพิวเตอร์ติดต่อกันหลายชั่วโมงจนข้อเท้าบวมในตอนเย็น ควรปฏิบัติตามแนวทางใด',
         'ลุกเดินหรือขยับขาเป็นระยะเมื่อต้องนั่งนาน'),
)
