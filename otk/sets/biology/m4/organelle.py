"""ออร์แกเนลล์

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/12

Sets moved here from: science_wave_f46.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f46 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_ORGANELLE = "ออร์แกเนลล์"


# (organelle, role, membranes, in plant cells, in animal cells)
ORGANELLES = (
    ("ไมโทคอนเดรีย", "สลายสารอาหารในการหายใจระดับเซลล์ให้ได้ ATP", 2, True, True),
    ("คลอโรพลาสต์", "สังเคราะห์ด้วยแสง", 2, True, False),
    ("ไรโบโซม", "สังเคราะห์โปรตีน", 0, True, True),
    ("เอนโดพลาสมิกเรติคูลัมชนิดผิวขรุขระ", "สังเคราะห์และลำเลียงโปรตีน", 1, True, True),
    ("เอนโดพลาสมิกเรติคูลัมชนิดผิวเรียบ", "สังเคราะห์ลิพิดและกำจัดสารพิษ", 1, True, True),
    ("กอลจิคอมเพล็กซ์", "ดัดแปลงและบรรจุสารลงถุงเพื่อส่งออก", 1, True, True),
    ("ไลโซโซม", "ย่อยสลายสารและออร์แกเนลล์ที่เสื่อม", 1, False, True),
    ("แวคิวโอลขนาดใหญ่", "สะสมน้ำและสารต่าง ๆ และช่วยให้เซลล์เต่ง", 1, True, False),
    ("เซนทริโอล", "ช่วยสร้างเส้นใยสปินเดิลเมื่อแบ่งเซลล์", 0, False, True),
    ("นิวเคลียส", "เก็บสารพันธุกรรมและควบคุมการทำงานของเซลล์", 2, True, True),
)


MEMBRANE_TEXT = {0: "ไม่มีเยื่อหุ้ม", 1: "มีเยื่อหุ้มชั้นเดียว", 2: "มีเยื่อหุ้มสองชั้น"}


@question_type(
    "biology.organelle_foundation",
    display_name={"th": "หน้าที่ของออร์แกเนลล์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ORGANELLE,
)
class OrganelleFoundation(QuestionType):
    """Match each organelle to its job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, role, *_ = rng.choice(ORGANELLES)
        others = [o for o in ORGANELLES if o[0] != name]
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}ทำหน้าที่ใด", correct=role, wrongs=tuple(o[1] for o in rng.sample(others, 3)),
                             topic=TOPIC_ORGANELLE, hint="ไมโทคอนเดรียสร้าง ATP ไรโบโซมสร้างโปรตีน กอลจิบรรจุสาร ไลโซโซมย่อยสลาย")
        return _labelled(stem=f"ออร์แกเนลล์ใดทำหน้าที่{role}", correct=name, wrongs=tuple(o[0] for o in rng.sample(others, 3)),
                         topic=TOPIC_ORGANELLE, hint="ไมโทคอนเดรียสร้าง ATP ไรโบโซมสร้างโปรตีน กอลจิบรรจุสาร ไลโซโซมย่อยสลาย")


@question_type(
    "biology.organelle_fluency",
    display_name={"th": "จำนวนชั้นเยื่อหุ้มของออร์แกเนลล์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ORGANELLE,
)
class OrganelleFluency(QuestionType):
    """Nucleus, mitochondria and chloroplasts have two membranes; ribosomes and centrioles none."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, _, membranes, *_ = rng.choice(ORGANELLES)
        if rng.random() < 0.5:
            right = MEMBRANE_TEXT[membranes]
            return _labelled(stem=f"{name}มีเยื่อหุ้มกี่ชั้น", correct=right,
                             wrongs=tuple(v for k, v in MEMBRANE_TEXT.items() if k != membranes) + ("มีเยื่อหุ้มสามชั้น",),
                             topic=TOPIC_ORGANELLE, hint="เยื่อหุ้มสองชั้น: นิวเคลียส ไมโทคอนเดรีย คลอโรพลาสต์ ไม่มีเยื่อหุ้ม: ไรโบโซม เซนทริโอล")
        want = rng.choice((0, 1, 2))
        match = [o[0] for o in ORGANELLES if o[2] == want]
        others = [o[0] for o in ORGANELLES if o[2] != want]
        return _labelled(stem=f"ออร์แกเนลล์ใด{MEMBRANE_TEXT[want]}", correct=rng.choice(match), wrongs=tuple(others),
                         topic=TOPIC_ORGANELLE, hint="เยื่อหุ้มสองชั้น: นิวเคลียส ไมโทคอนเดรีย คลอโรพลาสต์ ไม่มีเยื่อหุ้ม: ไรโบโซม เซนทริโอล")


@question_type(
    "biology.organelle_application",
    display_name={"th": "ออร์แกเนลล์ในเซลล์พืชและเซลล์สัตว์ และเซลล์ที่ทำงานพิเศษ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ORGANELLE,
)
class OrganelleApplication(QuestionType):
    """Which cells carry which organelles, and which a busy cell has plenty of."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            plant_only = rng.random() < 0.5
            match = [o[0] for o in ORGANELLES if o[3] and not o[4]] if plant_only else [o[0] for o in ORGANELLES if o[4] and not o[3]]
            others = [o[0] for o in ORGANELLES if o[3] and o[4]]
            return _labelled(stem=f"ออร์แกเนลล์ใดพบใน{'เซลล์พืช' if plant_only else 'เซลล์สัตว์'}แต่ไม่พบใน{'เซลล์สัตว์' if plant_only else 'เซลล์พืช'}",
                             correct=rng.choice(match), wrongs=tuple(others), topic=TOPIC_ORGANELLE,
                             hint="พืชมีคลอโรพลาสต์และแวคิวโอลใหญ่ สัตว์มีเซนทริโอลและไลโซโซม")
        cells = (("เซลล์กล้ามเนื้อหัวใจที่ทำงานตลอดเวลา", "ไมโทคอนเดรีย"),
                 ("เซลล์ตับอ่อนที่หลั่งเอนไซม์ย่อยอาหารจำนวนมาก", "เอนโดพลาสมิกเรติคูลัมชนิดผิวขรุขระ"),
                 ("เซลล์ตับที่กำจัดสารพิษ", "เอนโดพลาสมิกเรติคูลัมชนิดผิวเรียบ"),
                 ("เซลล์เม็ดเลือดขาวที่กินและย่อยเชื้อโรค", "ไลโซโซม"),
                 ("เซลล์ชั้นแพลิเซดในใบพืช", "คลอโรพลาสต์"),
                 ("เซลล์ต่อมที่ส่งสารคัดหลั่งออกนอกเซลล์", "กอลจิคอมเพล็กซ์"))
        cell, right = rng.choice(cells)
        others = [c[1] for c in cells if c[1] != right]
        return _labelled(stem=f"{cell}น่าจะมีออร์แกเนลล์ใดมากเป็นพิเศษ", correct=right, wrongs=tuple(others),
                         topic=TOPIC_ORGANELLE, hint="เซลล์ที่ใช้พลังงานมากมีไมโทคอนเดรียมาก เซลล์ที่สร้างโปรตีนส่งออกมี RER และกอลจิมาก")
