"""ระบบประสาทส่วนกลางและระบบประสาทรอบนอก

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/4

Sets moved here from: science_wave_f66.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f66 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_CNS = "ระบบประสาทส่วนกลางและระบบประสาทรอบนอก"


CENTRAL = ("สมองส่วนหน้า", "ไขสันหลัง", "สมองส่วนหลัง", "ซีรีบรัม", "เมดัลลาออบลองกาตา")


PERIPHERAL = ("เส้นประสาทสมอง", "เส้นประสาทไขสันหลัง", "ปมประสาทรากบน", "เส้นประสาทที่ไปยังกล้ามเนื้อแขน")


SPINAL = (
    ("เนื้อสีเทาของไขสันหลัง", "อยู่ด้านในเป็นรูปคล้ายผีเสื้อ เป็นที่อยู่ของตัวเซลล์ประสาท"),
    ("เนื้อสีขาวของไขสันหลัง", "อยู่ด้านนอก ประกอบด้วยแอกซอนที่มีเยื่อไมอีลิน"),
    ("รากบนของเส้นประสาทไขสันหลัง", "มีใยประสาทของเซลล์ประสาทรับความรู้สึก และมีปมประสาทรากบน"),
    ("รากล่างของเส้นประสาทไขสันหลัง", "มีใยประสาทของเซลล์ประสาทสั่งการ"),
    ("เยื่อหุ้มสมองและไขสันหลัง", "มี 3 ชั้น ปกป้องสมองและไขสันหลัง มีน้ำหล่อสมองและไขสันหลังอยู่ภายใน"),
)


ARC = ("หน่วยรับความรู้สึกที่ผิวหนัง", "เซลล์ประสาทรับความรู้สึก", "เซลล์ประสาทประสานงานในไขสันหลัง", "เซลล์ประสาทสั่งการที่ออกจากไขสันหลัง", "หน่วยปฏิบัติงานคือกล้ามเนื้อ")


CNS_HINT = ("ระบบประสาทส่วนกลางคือสมองและไขสันหลัง ระบบประสาทรอบนอกคือเส้นประสาทสมอง 12 คู่ และเส้นประสาทไขสันหลัง 31 คู่ "
            "รากบนนำความรู้สึกเข้า รากล่างนำคำสั่งออก")


@question_type(
    "biology.cns_pns_foundation",
    display_name={"th": "ส่วนประกอบของระบบประสาทส่วนกลางและรอบนอก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_CNS,
)
class CnsPnsFoundation(QuestionType):
    """Central or peripheral; and the nerve counts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.55:
            central = rng.random() < 0.5
            same, other = (CENTRAL, PERIPHERAL) if central else (PERIPHERAL, CENTRAL)
            kind = "ระบบประสาทส่วนกลาง" if central else "ระบบประสาทรอบนอก"
            return _labelled(stem=f"ข้อใดเป็นส่วนหนึ่งของ{kind}", correct=rng.choice(same), wrongs=tuple(other), topic=TOPIC_CNS,
                             hint=CNS_HINT)
        which = rng.choice((("เส้นประสาทสมอง", 12), ("เส้นประสาทไขสันหลัง", 31)))
        if rng.random() < 0.5:
            return numeric(stem=f"คนมี{which[0]}กี่คู่", answer=which[1], wrongs=[43 - which[1], which[1] * 2, 33], unit="คู่", topic=TOPIC_CNS,
                           hint=CNS_HINT)
        return numeric(stem="คนมีเส้นประสาทสมองและเส้นประสาทไขสันหลังรวมกันทั้งหมดกี่เส้น", answer=86, wrongs=[43, 62, 24], unit="เส้น",
                       topic=TOPIC_CNS, hint=CNS_HINT + " รวม 43 คู่ = 86 เส้น")


@question_type(
    "biology.cns_pns_fluency",
    display_name={"th": "โครงสร้างของไขสันหลังและเส้นประสาทไขสันหลัง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_CNS,
)
class CnsPnsFluency(QuestionType):
    """Grey and white matter, dorsal and ventral roots, meninges."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part, what = rng.choice(SPINAL)
        others = rng.sample([p for p in SPINAL if p[0] != part], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{part}มีลักษณะอย่างไร", correct=what, wrongs=tuple(p[1] for p in others), topic=TOPIC_CNS, hint=CNS_HINT)
        return _labelled(stem=f"ส่วนใด{what}", correct=part, wrongs=tuple(p[0] for p in others), topic=TOPIC_CNS, hint=CNS_HINT)


@question_type(
    "biology.cns_pns_application",
    display_name={"th": "วงจรรีเฟล็กซ์และผลเมื่อเส้นประสาทเสียหาย"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_CNS,
)
class CnsPnsApplication(QuestionType):
    """The reflex arc in order, and what a cut root does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            i = rng.randrange(len(ARC) - 1)
            pool = [a for a in ARC if a not in (ARC[i], ARC[i + 1])] + ["สมองส่วนหน้าที่ควบคุมการคิด"]
            return _labelled(stem=f"ในวงจรรีเฟล็กซ์ของการกระตุกขาเมื่อเคาะใต้สะบ้า หลังจาก{ARC[i]} กระแสประสาทไปที่ใดต่อ",
                             correct=ARC[i + 1], wrongs=tuple(pool), topic=TOPIC_CNS,
                             hint="หน่วยรับความรู้สึก → เซลล์ประสาทรับความรู้สึก → ไขสันหลัง → เซลล์ประสาทสั่งการ → หน่วยปฏิบัติงาน")
        cases = (("ถ้ารากบนของเส้นประสาทไขสันหลังที่ไปเลี้ยงขาขาด จะเกิดอะไรขึ้น", "ขาไม่รู้สึก แต่ยังสั่งให้กล้ามเนื้อขาเคลื่อนไหวได้",
                  ("ขารู้สึกได้ แต่ขยับกล้ามเนื้อขาเองไม่ได้", "ขาทั้งรู้สึกและขยับได้ตามปกติ เพราะรากอีกข้างยังทำงาน", "ขาเคลื่อนไหวเองตลอดเวลาโดยควบคุมไม่ได้", "แขนและขาไม่รู้สึกทั้งหมดทั้งสองข้าง")),
                 ("ถ้ารากล่างของเส้นประสาทไขสันหลังที่ไปเลี้ยงขาขาด จะเกิดอะไรขึ้น", "ขารู้สึกได้ แต่ขยับกล้ามเนื้อขาไม่ได้",
                  ("ขาไม่รู้สึก แต่ขยับได้ตามปกติ", "ขาทั้งรู้สึกและขยับได้ตามปกติ เพราะรากอีกข้างยังทำงาน", "ขาเคลื่อนไหวเองตลอดเวลาโดยควบคุมไม่ได้", "แขนและขาไม่รู้สึกทั้งหมดทั้งสองข้าง")),
                 ("เหตุใดเมื่อมือสัมผัสของร้อนจึงกระตุกออกก่อนรู้สึกร้อน", "รีเฟล็กซ์สั่งการผ่านไขสันหลังก่อนที่กระแสประสาทไปถึงสมอง",
                  ("สมองสั่งการเร็วกว่าไขสันหลัง จึงดึงมือออกก่อนรู้สึกเจ็บ", "กล้ามเนื้อหดตัวเองโดยไม่ต้องใช้ประสาท", "ผิวหนังสั่งกล้ามเนื้อโดยตรง",
                   "ระบบประสาทอัตโนวัติสั่งกล้ามเนื้อลายให้ดึงมือออก")),
                 ("ผู้ที่ได้รับบาดเจ็บจนไขสันหลังขาดที่ระดับเอว มักเป็นอย่างไร", "ขาทั้งสองข้างอัมพาตและไม่รู้สึก แต่แขนยังใช้ได้",
                  ("แขนอัมพาตแต่ขาปกติ เพราะรอยขาดอยู่ต่ำกว่าแขน", "ทุกส่วนของร่างกายปกติ เพราะสมองยังทำงานได้", "หัวใจหยุดเต้นทันที แต่แขนและขาใช้ได้ปกติ", "ตาบอดทั้งสองข้างแต่ขายังใช้ได้")))
        stem, right, wrongs = rng.choice(cases)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_CNS, hint=CNS_HINT)
