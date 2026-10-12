"""สมองและไขสันหลัง

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/5

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


TOPIC_BRAIN = "สมองและไขสันหลัง"


BRAIN = (
    ("ซีรีบรัม", "สมองส่วนหน้า", "ควบคุมความคิด ความจำ การเรียนรู้ และการเคลื่อนไหวที่อยู่ในอำนาจจิตใจ"),
    ("ออลแฟกทอรีบัลบ์", "สมองส่วนหน้า", "รับรู้กลิ่น"),
    ("ทาลามัส", "สมองส่วนหน้า", "ถ่ายทอดกระแสประสาทรับความรู้สึกไปยังซีรีบรัม"),
    ("ไฮโพทาลามัส", "สมองส่วนหน้า", "ควบคุมอุณหภูมิร่างกาย ความหิว ความกระหาย และการหลั่งฮอร์โมน"),
    ("สมองส่วนกลาง", "สมองส่วนกลาง", "ควบคุมการเคลื่อนไหวของลูกตาและม่านตา และเป็นทางผ่านกระแสประสาทการได้ยิน"),
    ("ซีรีเบลลัม", "สมองส่วนหลัง", "ควบคุมการทรงตัวและการประสานงานของกล้ามเนื้อ"),
    ("พอนส์", "สมองส่วนหลัง", "ควบคุมการหายใจร่วมกับเมดัลลา และการเคี้ยว การหลั่งน้ำลาย"),
    ("เมดัลลาออบลองกาตา", "สมองส่วนหลัง", "ควบคุมการเต้นของหัวใจ การหายใจ ความดันเลือด การกลืน การไอ และการจาม"),
)


BRAIN_HINT = ("สมองส่วนหน้า: ซีรีบรัม ออลแฟกทอรีบัลบ์ ทาลามัส ไฮโพทาลามัส สมองส่วนหลัง: ซีรีเบลลัม พอนส์ เมดัลลาออบลองกาตา "
              "ซีรีเบลลัมคุมการทรงตัว เมดัลลาคุมหัวใจและการหายใจ ไฮโพทาลามัสคุมอุณหภูมิ")


SYMPTOMS = (
    ("เดินเซ ทรงตัวไม่ได้ หยิบจับสิ่งของไม่แม่นยำ", "ซีรีเบลลัม"),
    ("ร่างกายควบคุมอุณหภูมิไม่ได้ หิวและกระหายผิดปกติ", "ไฮโพทาลามัส"),
    ("หัวใจเต้นผิดจังหวะและหายใจผิดปกติจนเป็นอันตรายถึงชีวิต", "เมดัลลาออบลองกาตา"),
    ("จำเรื่องใหม่ไม่ได้ และคิดวิเคราะห์ได้ลดลง", "ซีรีบรัม"),
    ("ไม่ได้กลิ่นแม้จมูกปกติ", "ออลแฟกทอรีบัลบ์"),
    ("ม่านตาไม่ปรับขนาดตามแสง", "สมองส่วนกลาง"),
)


@question_type(
    "biology.brain_foundation",
    display_name={"th": "ส่วนของสมองในสมองส่วนหน้า ส่วนกลาง และส่วนหลัง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BRAIN,
)
class BrainFoundation(QuestionType):
    """Which division each part sits in."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part, region, _ = rng.choice(BRAIN)
        if rng.random() < 0.5 and part != "สมองส่วนกลาง":
            return _labelled(stem=f"{part}เป็นส่วนหนึ่งของสมองส่วนใด", correct=region,
                             wrongs=tuple(r for r in ("สมองส่วนหน้า", "สมองส่วนกลาง", "สมองส่วนหลัง", "ไขสันหลัง") if r != region),
                             topic=TOPIC_BRAIN, hint=BRAIN_HINT)
        region = rng.choice(("สมองส่วนหน้า", "สมองส่วนหลัง"))
        same = [b[0] for b in BRAIN if b[1] == region]
        other = [b[0] for b in BRAIN if b[1] != region and b[0] != "สมองส่วนกลาง"] + ["ไขสันหลัง", "เส้นประสาทสมองคู่ที่ 2"]
        return _labelled(stem=f"ข้อใดเป็นส่วนหนึ่งของ{region}", correct=rng.choice(same), wrongs=tuple(other), topic=TOPIC_BRAIN,
                         hint=BRAIN_HINT)


@question_type(
    "biology.brain_fluency",
    display_name={"th": "หน้าที่ของสมองแต่ละส่วน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BRAIN,
)
class BrainFluency(QuestionType):
    """Each part and what it controls."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part, _, job = rng.choice(BRAIN)
        others = rng.sample([b for b in BRAIN if b[0] != part], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{part}ทำหน้าที่อะไร", correct=job, wrongs=tuple(b[2] for b in others), topic=TOPIC_BRAIN, hint=BRAIN_HINT)
        return _labelled(stem=f"สมองส่วนใด{job}", correct=part, wrongs=tuple(b[0] for b in others), topic=TOPIC_BRAIN, hint=BRAIN_HINT)


@question_type(
    "biology.brain_application",
    display_name={"th": "ระบุส่วนของสมองที่ผิดปกติจากอาการ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BRAIN,
)
class BrainApplication(QuestionType):
    """Read the symptom back to the part."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        symptom, part = rng.choice(SYMPTOMS)
        pool = [b[0] for b in BRAIN if b[0] != part]
        who = rng.choice(("ผู้ป่วยรายหนึ่ง", "ผู้ที่ได้รับบาดเจ็บที่ศีรษะ", "ผู้ที่ดื่มแอลกอฮอล์มาก"))
        if part != "ซีรีเบลลัม" and who == "ผู้ที่ดื่มแอลกอฮอล์มาก":
            who = "ผู้ป่วยรายหนึ่ง"
        return _labelled(stem=f"{who}มีอาการ{symptom} สมองส่วนใดน่าจะทำงานผิดปกติ", correct=part, wrongs=tuple(pool),
                         topic=TOPIC_BRAIN, hint=BRAIN_HINT)
