"""กระดูกและกล้ามเนื้อของมนุษย์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/10

Sets moved here from: science_wave_f67.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f67 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_BONE = "กระดูกและกล้ามเนื้อของมนุษย์"


AXIAL = ("กะโหลกศีรษะ", "กระดูกสันหลัง", "กระดูกซี่โครง", "กระดูกอก")


APPENDICULAR = ("กระดูกต้นแขน", "กระดูกต้นขา", "กระดูกสะบัก", "กระดูกเชิงกราน", "กระดูกไหปลาร้า")


MUSCLES = {
    "กล้ามเนื้อโครงร่าง": ("เซลล์ยาวทรงกระบอก มีลาย มีหลายนิวเคลียส", "ทำงานภายใต้อำนาจจิตใจ", "ยึดติดกับกระดูก"),
    "กล้ามเนื้อเรียบ": ("เซลล์รูปกระสวย ไม่มีลาย มีนิวเคลียสเดียว", "ทำงานนอกอำนาจจิตใจ พบที่ผนังอวัยวะภายใน", "พบที่ผนังลำไส้และหลอดเลือด"),
    "กล้ามเนื้อหัวใจ": ("มีลาย เซลล์แตกแขนงเชื่อมต่อกัน", "ทำงานนอกอำนาจจิตใจ หดตัวเป็นจังหวะตลอดชีวิต", "พบเฉพาะที่หัวใจ"),
}


BONE_HINT = ("กระดูกแกนคือกะโหลก สันหลัง ซี่โครง และกระดูกอก กระดูกรยางค์คือแขน ขา และกระดูกที่ยึด "
             "กล้ามเนื้อโครงร่างมีลายและอยู่ในอำนาจจิตใจ กล้ามเนื้อเรียบไม่มีลาย กล้ามเนื้อหัวใจมีลายแต่อยู่นอกอำนาจจิตใจ")


@question_type(
    "biology.skeleton_muscle_foundation",
    display_name={"th": "กระดูกแกนและกระดูกรยางค์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BONE,
)
class SkeletonMuscleFoundation(QuestionType):
    """Axial or appendicular."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        axial = rng.random() < 0.5
        same, other = (AXIAL, APPENDICULAR) if axial else (APPENDICULAR, AXIAL)
        kind = "กระดูกแกน" if axial else "กระดูกรยางค์"
        if rng.random() < 0.6:
            return _labelled(stem=f"ข้อใดจัดเป็น{kind}", correct=rng.choice(same), wrongs=tuple(other), topic=TOPIC_BONE,
                             hint=BONE_HINT)
        facts = (("โครงกระดูกของคนมีหน้าที่ใด", "ค้ำจุนร่างกาย ป้องกันอวัยวะภายใน เป็นที่ยึดของกล้ามเนื้อ และสร้างเซลล์เม็ดเลือด",
                  ("ย่อยอาหาร", "แลกเปลี่ยนแก๊ส", "กรองของเสียออกจากเลือด", "สร้างน้ำดี")),
                 ("ผู้ใหญ่มีกระดูกประมาณกี่ชิ้น", "206 ชิ้น", ("106 ชิ้น", "300 ชิ้น", "52 ชิ้น", "412 ชิ้น")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_BONE, hint=BONE_HINT)


@question_type(
    "biology.skeleton_muscle_fluency",
    display_name={"th": "เปรียบเทียบกล้ามเนื้อโครงร่าง กล้ามเนื้อเรียบ และกล้ามเนื้อหัวใจ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BONE,
)
class SkeletonMuscleFluency(QuestionType):
    """Striated or not, voluntary or not, and where each is found."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(MUSCLES))
        feature = rng.choice(MUSCLES[kind])
        others = [k for k in MUSCLES if k != kind]
        if rng.random() < 0.5:
            return _labelled(stem=f"กล้ามเนื้อที่ \"{feature}\" คือกล้ามเนื้อชนิดใด", correct=kind, wrongs=(*others, "กล้ามเนื้อแอนทาโกนิซึม"),
                             topic=TOPIC_BONE, hint=BONE_HINT)
        pool = [f for k in others for f in MUSCLES[k]]
        return _labelled(stem=f"ข้อใดเป็นลักษณะของ{kind}", correct=feature, wrongs=tuple(pool), topic=TOPIC_BONE, hint=BONE_HINT)


@question_type(
    "biology.skeleton_muscle_application",
    display_name={"th": "การหดตัวของซาร์โคเมียร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BONE,
)
class SkeletonMuscleApplication(QuestionType):
    """Actin slides over myosin; every sarcomere shortens a little, and it adds up."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            facts = (("การหดตัวของกล้ามเนื้อโครงร่างเกิดจากอะไร", "แอกตินเลื่อนเข้าหากันบนไมโอซิน ทำให้ซาร์โคเมียร์สั้นลง",
                      ("ไมโอซินสั้นลงเอง", "แอกตินหายไปจากซาร์โคเมียร์", "เซลล์กล้ามเนื้อแบ่งตัว", "กระดูกดึงกล้ามเนื้อ")),
                     ("การหดตัวของกล้ามเนื้อต้องใช้สารใดบ้าง", "ATP และ Ca²⁺", ("กลูโคสโดยตรงเท่านั้น", "Na⁺ และ Cl⁻ เท่านั้น",
                                                                           "ออกซิเจนเท่านั้น", "อินซูลิน")))
            stem, right, wrongs = rng.choice(facts)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_BONE, hint=BONE_HINT)
        rest = Fraction(rng.choice((22, 24, 25, 26)), 10)
        short = rest - Fraction(rng.choice((2, 3, 4, 5, 6)), 10)
        count = rng.randrange(1000, 20001, 1000)
        change = (rest - short) * count
        if rng.random() < 0.5:
            return numeric(stem=f"ซาร์โคเมียร์ยาว {show(rest)} μm หดสั้นลงเหลือ {show(short)} μm ถ้าใยกล้ามเนื้อมีซาร์โคเมียร์เรียงต่อกัน {count} หน่วย "
                                f"ใยกล้ามเนื้อสั้นลงกี่ไมโครเมตร", answer=change, wrongs=[short * count, rest * count, rest - short], unit="μm",
                           topic=TOPIC_BONE, hint="ความยาวที่ลดลง = (ความยาวเดิม − ความยาวใหม่) ของซาร์โคเมียร์ × จำนวนซาร์โคเมียร์")
        return numeric(stem=f"ใยกล้ามเนื้อมีซาร์โคเมียร์ {count} หน่วย แต่ละหน่วยยาว {show(rest)} μm ใยกล้ามเนื้อยาวกี่มิลลิเมตร",
                       answer=rest * count / 1000, wrongs=[rest * count, rest * count / 100, rest * count / 10000 if (rest * count / 10000 * 100).denominator == 1
                                                          else rest], unit="mm", topic=TOPIC_BONE,
                       hint="ความยาวรวม = ความยาวต่อหน่วย × จำนวนหน่วย แล้วแปลง μm เป็น mm (÷ 1,000)")
