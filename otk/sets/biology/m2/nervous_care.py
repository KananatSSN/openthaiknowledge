"""การดูแลรักษาและป้องกันอันตรายต่อระบบประสาท

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/11

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
from otk.sets._support.science_wave_b11 import NERVOUS_CARE_SCENARIOS

PROVENANCE = Provenance("original")


NERVOUS_CARE = (
    Care("สวมหมวกนิรภัยทุกครั้งที่ขับขี่หรือซ้อนท้ายรถจักรยานยนต์",
         "หมวกนิรภัยรับและกระจายแรงที่กระทำต่อกะโหลกศีรษะ "
         "จึงลดโอกาสที่สมองจะกระทบกระเทือนเมื่อเกิดอุบัติเหตุ"),
    Care("คาดเข็มขัดนิรภัยทุกครั้งที่โดยสารรถยนต์",
         "เข็มขัดยึดลำตัวไว้กับที่นั่งเมื่อรถหยุดกะทันหัน "
         "จึงลดการสะบัดของศีรษะและคอที่ทำให้ไขสันหลังส่วนคอบาดเจ็บ"),
    Care("ไม่กระโดดพุ่งลงน้ำในที่ที่ไม่ทราบความลึก",
         "การพุ่งศีรษะลงกระแทกพื้นทำให้กระดูกสันหลังส่วนคอหักและกดทับไขสันหลัง "
         "ซึ่งเป็นความเสียหายที่มักถาวร"),
    Care("นอนหลับพักผ่อนให้เพียงพอ",
         "ขณะหลับเป็นช่วงที่สมองจัดระเบียบความจำและกำจัดของเสียที่สะสมระหว่างวัน "
         "การอดนอนจึงทำให้การเรียนรู้และการตัดสินใจแย่ลง"),
    Care("ไม่ดื่มเครื่องดื่มแอลกอฮอล์และไม่ใช้สารเสพติด",
         "สารเหล่านี้รบกวนการส่งกระแสประสาทและทำลายเซลล์ประสาท "
         "ซึ่งร่างกายสร้างทดแทนได้ยากมาก"),
    Care("สวมอุปกรณ์ป้องกันศีรษะขณะเล่นกีฬาที่มีการปะทะ",
         "ลดแรงกระแทกที่ศีรษะซึ่งแม้ครั้งละไม่มากแต่สะสมจนทำให้สมองเสียหายในระยะยาว"),
)


NERVOUS_NEEDS = (
    Need("นักเรียนซ้อนท้ายรถจักรยานยนต์ไปโรงเรียนทุกวันโดยคิดว่าระยะทางใกล้จึงไม่จำเป็น"
         "ต้องเตรียมอะไร ควรปฏิบัติตามแนวทางใด",
         "สวมหมวกนิรภัยทุกครั้งที่ขับขี่หรือซ้อนท้ายรถจักรยานยนต์"),
    Need("นักเรียนนั่งเบาะหลังของรถยนต์และเห็นว่าไม่มีใครในเบาะหลังทำอะไรเลยเมื่อรถออก "
         "ควรปฏิบัติตามแนวทางใดเพื่อป้องกันการบาดเจ็บที่คอ",
         "คาดเข็มขัดนิรภัยทุกครั้งที่โดยสารรถยนต์"),
    Need("เพื่อนชวนนักเรียนกระโดดลงเล่นน้ำในคลองที่ไม่เคยลงมาก่อนและมองไม่เห็นพื้น "
         "ควรปฏิบัติตามแนวทางใด",
         "ไม่กระโดดพุ่งลงน้ำในที่ที่ไม่ทราบความลึก"),
    Need("นักเรียนนอนดึกติดต่อกันหลายคืนจนจำบทเรียนไม่ค่อยได้และตัดสินใจผิดพลาดบ่อย "
         "ควรปฏิบัติตามแนวทางใด",
         "นอนหลับพักผ่อนให้เพียงพอ"),
    Need("เพื่อนชวนนักเรียนลองดื่มเครื่องดื่มแอลกอฮอล์ในงานเลี้ยง โดยบอกว่าดื่มนิดหน่อย"
         "ไม่เป็นไร ควรปฏิบัติตามแนวทางใด",
         "ไม่ดื่มเครื่องดื่มแอลกอฮอล์และไม่ใช้สารเสพติด"),
    Need("นักเรียนเข้าร่วมทีมกีฬาที่มีการปะทะและถูกกระแทกที่ศีรษะเบา ๆ อยู่บ่อยครั้ง "
         "ควรปฏิบัติตามแนวทางใด",
         "สวมอุปกรณ์ป้องกันศีรษะขณะเล่นกีฬาที่มีการปะทะ"),
)


@question_type(
    "body.nervous_care_foundation",
    display_name={"th": "เหตุผลของแนวทางดูแลและป้องกันอันตรายต่อระบบประสาท"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class NervousCareFoundation(QuestionType):
    """Why a precaution protects the brain and the spinal cord."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return care_foundation(
            rng, system="ระบบประสาท", cares=NERVOUS_CARE,
            hint="โยงแนวทางกลับไปที่แรงที่กระทำต่อศีรษะและคอ "
                 "หรือที่การทำงานของเซลล์ประสาทซึ่งสร้างทดแทนได้ยาก",
        )


@question_type(
    "body.nervous_care_fluency",
    display_name={"th": "เลือกแนวทางป้องกันอันตรายต่อสมองและไขสันหลัง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class NervousCareFluency(QuestionType):
    """State the แนวทาง the situation calls for — ``ม.2/11``'s own evidence."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return care_fluency(
            rng, needs=NERVOUS_NEEDS, cares=NERVOUS_CARE,
            hint="ระบุก่อนว่าอันตรายในสถานการณ์นี้จะมาถึงศีรษะ คอ "
                 "หรือมาถึงการทำงานของเซลล์ประสาทโดยตรง",
        )


@question_type(
    "body.nervous_care_application",
    display_name={"th": "วิเคราะห์ความเสี่ยงและการป้องกันการบาดเจ็บทางระบบประสาท"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class NervousCareApplication(QuestionType):
    """Explain why a precaution works, or why an injury does not heal."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, NERVOUS_CARE_SCENARIOS,
            hint="เริ่มจากข้อเท็จจริงที่ว่าเซลล์ประสาทสร้างทดแทนได้ยาก "
                 "แล้วจึงดูว่าแนวทางนั้นลดแรงหรือลดความเสียหายอย่างไร",
        )
