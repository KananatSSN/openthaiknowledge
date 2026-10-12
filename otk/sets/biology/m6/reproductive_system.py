"""ระบบสืบพันธุ์ของมนุษย์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/13

Sets moved here from: science_wave_f68.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f68 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_SYSTEM = "ระบบสืบพันธุ์ของมนุษย์"


ORGANS = (
    ("อัณฑะ", "สร้างอสุจิและฮอร์โมนเทสโทสเตอโรน"),
    ("ถุงหุ้มอัณฑะ", "ช่วยให้อุณหภูมิของอัณฑะต่ำกว่าอุณหภูมิร่างกายเล็กน้อย"),
    ("หลอดเก็บอสุจิ (เอพิดิดิมิส)", "เก็บอสุจิไว้จนเจริญเต็มที่"),
    ("ต่อมลูกหมาก", "หลั่งสารที่เป็นเบสอ่อนช่วยลดความเป็นกรดในท่อปัสสาวะ"),
    ("ถุงสร้างน้ำเลี้ยงอสุจิ", "สร้างของเหลวที่มีน้ำตาลฟรักโทสเป็นแหล่งพลังงานของอสุจิ"),
    ("รังไข่", "สร้างเซลล์ไข่และฮอร์โมนเอสโทรเจนและโพรเจสเทอโรน"),
    ("ท่อนำไข่", "เป็นบริเวณที่มักเกิดการปฏิสนธิ"),
    ("มดลูก", "เป็นที่ฝังตัวและเจริญของเอ็มบริโอ"),
)


SPERM_PATH = ("อัณฑะ", "หลอดเก็บอสุจิ", "ท่อนำอสุจิ", "ท่อปัสสาวะ")


SYSTEM_HINT = ("อัณฑะสร้างอสุจิ อสุจิเก็บในหลอดเก็บอสุจิ ผ่านท่อนำอสุจิและท่อปัสสาวะ รังไข่สร้างไข่ การปฏิสนธิเกิดที่ท่อนำไข่ "
               "เอ็มบริโอฝังตัวที่มดลูก การตกไข่เกิดประมาณ 14 วันก่อนประจำเดือนรอบถัดไป")


@question_type(
    "biology.reproductive_system_foundation",
    display_name={"th": "อวัยวะในระบบสืบพันธุ์เพศชายและเพศหญิง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SYSTEM,
)
class ReproductiveSystemFoundation(QuestionType):
    """Each organ and what it does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        organ, role = rng.choice(ORGANS)
        others = rng.sample([o for o in ORGANS if o[0] != organ], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{organ}ทำหน้าที่อะไร", correct=role, wrongs=tuple(o[1] for o in others), topic=TOPIC_SYSTEM, hint=SYSTEM_HINT)
        return _labelled(stem=f"อวัยวะใด{role}", correct=organ, wrongs=tuple(o[0] for o in others), topic=TOPIC_SYSTEM, hint=SYSTEM_HINT)


@question_type(
    "biology.reproductive_system_fluency",
    display_name={"th": "เส้นทางของอสุจิและตำแหน่งสำคัญในระบบสืบพันธุ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SYSTEM,
)
class ReproductiveSystemFluency(QuestionType):
    """The sperm's route, and where fertilisation and implantation happen."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            i = rng.randrange(len(SPERM_PATH) - 1)
            pool = [p for p in SPERM_PATH if p not in (SPERM_PATH[i], SPERM_PATH[i + 1])] + ["ท่อไต", "กระเพาะปัสสาวะ"]
            return _labelled(stem=f"อสุจิที่ออกจาก{SPERM_PATH[i]}จะเคลื่อนที่ไปยังส่วนใดต่อไป", correct=SPERM_PATH[i + 1],
                             wrongs=tuple(pool), topic=TOPIC_SYSTEM, hint=SYSTEM_HINT)
        facts = (("โดยปกติการปฏิสนธิของมนุษย์เกิดขึ้นที่ใด", "ท่อนำไข่", ("มดลูก", "รังไข่", "ช่องคลอด", "ปากมดลูก")),
                 ("เอ็มบริโอของมนุษย์ฝังตัวที่ใด", "ผนังมดลูก", ("ท่อนำไข่", "รังไข่", "ช่องคลอด", "กระเพาะปัสสาวะ")),
                 ("เหตุใดอัณฑะจึงอยู่ในถุงหุ้มอัณฑะนอกช่องท้อง", "การสร้างอสุจิต้องการอุณหภูมิต่ำกว่าอุณหภูมิร่างกายเล็กน้อย",
                  ("เพื่อให้อสุจิได้รับแสง", "เพื่อให้ใกล้ไตมากขึ้น", "เพราะช่องท้องไม่มีที่ว่าง", "เพื่อให้ได้รับออกซิเจนจากอากาศ")),
                 ("ประจำเดือนเกิดจากอะไร", "ผนังมดลูกที่หนาขึ้นสลายตัวและหลุดออกเมื่อไม่มีการฝังตัวของเอ็มบริโอ",
                  ("รังไข่แตกออก", "ท่อนำไข่อักเสบ", "เซลล์ไข่ที่ได้รับการผสมแล้วหลุดออก", "ฮอร์โมนเทสโทสเตอโรนเพิ่มขึ้น")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_SYSTEM, hint=SYSTEM_HINT)


@question_type(
    "biology.reproductive_system_application",
    display_name={"th": "คำนวณวันตกไข่จากรอบประจำเดือน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SYSTEM,
)
class ReproductiveSystemApplication(QuestionType):
    """Ovulation falls about 14 days before the next period starts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cycle = rng.randint(24, 35)
        ovulation = cycle - 14
        if rng.random() < 0.35:
            start = rng.randint(1, 10)
            return numeric(stem=f"หญิงคนหนึ่งมีรอบประจำเดือนสม่ำเสมอ {cycle} วัน ประจำเดือนรอบนี้เริ่มวันที่ {start} มีนาคม "
                                f"การตกไข่น่าจะเกิดประมาณวันที่เท่าใดของเดือนมีนาคม", answer=start + ovulation - 1,
                           wrongs=[start + 13, start + ovulation, start + cycle - 1], unit="", topic=TOPIC_SYSTEM,
                           hint="วันตกไข่ของรอบ = ความยาวรอบ − 14 นับวันที่เริ่มมีประจำเดือนเป็นวันที่ 1 ของรอบ")
        if rng.random() < 0.6:
            return numeric(stem=f"หญิงคนหนึ่งมีรอบประจำเดือนสม่ำเสมอ {cycle} วัน ถ้านับวันแรกที่มีประจำเดือนเป็นวันที่ 1 การตกไข่น่าจะเกิดประมาณวันที่เท่าใด",
                           answer=ovulation, wrongs=[14, cycle // 2 if cycle // 2 != ovulation else cycle // 2 + 1, cycle], unit="",
                           topic=TOPIC_SYSTEM, hint="การตกไข่เกิดประมาณ 14 วันก่อนประจำเดือนรอบถัดไป วันตกไข่ = ความยาวรอบ − 14")
        return numeric(stem=f"หญิงคนหนึ่งมีรอบประจำเดือนสม่ำเสมอ ตกไข่ในวันที่ {ovulation} ของรอบ (นับวันแรกที่มีประจำเดือนเป็นวันที่ 1) "
                            f"รอบประจำเดือนยาวประมาณกี่วัน", answer=cycle,
                       wrongs=[ovulation * 2, ovulation + 7, 28 if cycle != 28 else 30], unit="วัน", topic=TOPIC_SYSTEM,
                       hint="ความยาวรอบ = วันตกไข่ + 14")
