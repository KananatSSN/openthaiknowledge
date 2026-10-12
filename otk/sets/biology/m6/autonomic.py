"""ระบบประสาทโซมาติกและระบบประสาทอัตโนวัติ

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/6

Sets moved here from: science_wave_f66.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f66 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_AUTO = "ระบบประสาทโซมาติกและระบบประสาทอัตโนวัติ"


# organ: (sympathetic effect, parasympathetic effect)
ORGAN_EFFECTS = {
    "หัวใจ": ("เต้นเร็วและแรงขึ้น", "เต้นช้าลง"),
    "ม่านตา": ("รูม่านตาขยาย", "รูม่านตาหรี่"),
    "หลอดลม": ("หลอดลมขยายกว้าง อากาศผ่านได้มากขึ้น", "หลอดลมตีบแคบลง"),
    "ทางเดินอาหาร": ("การบีบตัวและการย่อยลดลง", "การบีบตัวและการย่อยเพิ่มขึ้น"),
    "ต่อมน้ำลาย": ("หลั่งน้ำลายน้อยและข้น", "หลั่งน้ำลายมากและใส"),
    "กระเพาะปัสสาวะ": ("กล้ามเนื้อผนังคลายตัว กลั้นปัสสาวะ", "กล้ามเนื้อผนังหดตัว ขับปัสสาวะ"),
}


AUTO_HINT = ("ระบบประสาทโซมาติกสั่งกล้ามเนื้อลายซึ่งอยู่ในอำนาจจิตใจ ระบบประสาทอัตโนวัติสั่งกล้ามเนื้อเรียบ กล้ามเนื้อหัวใจ และต่อม "
             "ซิมพาเทติกเตรียมพร้อมสู้หรือหนี พาราซิมพาเทติกทำงานขณะพักผ่อนและย่อยอาหาร")


@question_type(
    "biology.autonomic_foundation",
    display_name={"th": "ระบบประสาทโซมาติกและระบบประสาทอัตโนวัติ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_AUTO,
)
class AutonomicFoundation(QuestionType):
    """Voluntary skeletal muscle, or involuntary organs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        somatic = ("การยกแขนหยิบหนังสือ", "การเดินไปเปิดประตู", "การกระพริบตาเมื่อตั้งใจ", "การเตะลูกฟุตบอล", "การเขียนหนังสือ")
        auto = ("การเต้นของหัวใจ", "การบีบตัวของลำไส้", "การหลั่งเหงื่อ", "การปรับขนาดรูม่านตา", "การหลั่งน้ำลายเมื่อได้กลิ่นอาหาร")
        roll = rng.random()
        if roll < 0.6:
            is_somatic = rng.random() < 0.5
            same, other = (somatic, auto) if is_somatic else (auto, somatic)
            kind = "ระบบประสาทโซมาติก" if is_somatic else "ระบบประสาทอัตโนวัติ"
            return _labelled(stem=f"ข้อใดถูกควบคุมโดย{kind}", correct=rng.choice(same), wrongs=tuple(other), topic=TOPIC_AUTO,
                             hint=AUTO_HINT)
        facts = (("ระบบประสาทโซมาติกสั่งการหน่วยปฏิบัติงานใด", "กล้ามเนื้อลาย", ("กล้ามเนื้อหัวใจ", "กล้ามเนื้อเรียบของลำไส้", "ต่อมเหงื่อ")),
                 ("ระบบประสาทอัตโนวัติสั่งการหน่วยปฏิบัติงานใด", "กล้ามเนื้อเรียบ กล้ามเนื้อหัวใจ และต่อม",
                  ("กล้ามเนื้อลายที่แขนขาเท่านั้น", "กระดูกและข้อต่อ", "ผิวหนังชั้นนอก")),
                 ("เซลล์ประสาทสั่งการของระบบประสาทอัตโนวัติแตกต่างจากระบบโซมาติกอย่างไร", "มีเซลล์ประสาทสั่งการ 2 เซลล์ต่อกันที่ปมประสาทอัตโนวัติ",
                  ("มีเซลล์ประสาทสั่งการเพียงเซลล์เดียว", "ไม่มีเซลล์ประสาทสั่งการ", "สั่งการเฉพาะกล้ามเนื้อลาย")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_AUTO, hint=AUTO_HINT)


@question_type(
    "biology.autonomic_fluency",
    display_name={"th": "ผลของระบบประสาทซิมพาเทติกและพาราซิมพาเทติกต่ออวัยวะ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_AUTO,
)
class AutonomicFluency(QuestionType):
    """Each organ's two opposite responses."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        organ = rng.choice(sorted(ORGAN_EFFECTS))
        symp, para = ORGAN_EFFECTS[organ]
        sympathetic = rng.random() < 0.5
        right, opposite = (symp, para) if sympathetic else (para, symp)
        division = "ระบบประสาทซิมพาเทติก" if sympathetic else "ระบบประสาทพาราซิมพาเทติก"
        if rng.random() < 0.6:
            pool = [e for o, pair in ORGAN_EFFECTS.items() if o != organ for e in pair]
            return _labelled(stem=f"{division}ทำให้{organ}เป็นอย่างไร", correct=right, wrongs=(opposite, *rng.sample(pool, 2)),
                             topic=TOPIC_AUTO, hint=AUTO_HINT)
        return _labelled(stem=f"การที่{organ}{right} เป็นผลของระบบประสาทใด", correct=division,
                         wrongs=("ระบบประสาทพาราซิมพาเทติก" if sympathetic else "ระบบประสาทซิมพาเทติก", "ระบบประสาทโซมาติก", "รีเฟล็กซ์ของไขสันหลังเพียงอย่างเดียว"),
                         topic=TOPIC_AUTO, hint=AUTO_HINT)


@question_type(
    "biology.autonomic_application",
    display_name={"th": "วิเคราะห์การตอบสนองของร่างกายในสถานการณ์ต่าง ๆ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_AUTO,
)
class AutonomicApplication(QuestionType):
    """Fright or rest: which side is in charge, and which effects follow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        fright = ("ถูกสุนัขวิ่งไล่", "ตกใจเสียงฟ้าผ่า", "กำลังจะขึ้นแข่งวิ่งระยะสั้น", "ตื่นเต้นก่อนขึ้นพูดหน้าชั้น")
        rest = ("นั่งพักหลังรับประทานอาหารกลางวัน", "นอนหลับพักผ่อนตอนกลางคืน", "นั่งอ่านหนังสือสบาย ๆ หลังอาหารเย็น")
        sympathetic = rng.random() < 0.5
        scene = rng.choice(fright if sympathetic else rest)
        organ = rng.choice(sorted(ORGAN_EFFECTS))
        symp, para = ORGAN_EFFECTS[organ]
        right = symp if sympathetic else para
        if rng.random() < 0.5:
            return _labelled(stem=f"ขณะ{scene} {organ}น่าจะเป็นอย่างไร", correct=right, wrongs=(para if sympathetic else symp,
                             *rng.sample([e for o, pair in ORGAN_EFFECTS.items() if o != organ for e in pair], 2)),
                             topic=TOPIC_AUTO, hint=AUTO_HINT)
        division = "ระบบประสาทซิมพาเทติก" if sympathetic else "ระบบประสาทพาราซิมพาเทติก"
        return _labelled(stem=f"ขณะ{scene} ระบบประสาทใดทำงานเด่น", correct=division,
                         wrongs=("ระบบประสาทพาราซิมพาเทติก" if sympathetic else "ระบบประสาทซิมพาเทติก", "ระบบประสาทโซมาติกเท่านั้น",
                                 "ไม่มีระบบประสาทใดทำงาน"), topic=TOPIC_AUTO, hint=AUTO_HINT)
