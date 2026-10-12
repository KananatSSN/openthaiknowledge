"""ไอโซเมอร์โครงสร้างของสารประกอบอินทรีย์

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/5

Sets moved here from: science_wave_f27.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f27 import (
    ACID,
    ALCOHOL,
    ALDEHYDE,
    ALKANE,
    ALKENE,
    ALKYNE,
    COMPOUNDS,
    ESTER,
    ETHER,
    HALO,
    KETONE,
    SUBJECT,
    UPPER_SIX,
    carbons,
    isomers_of,
    molecular,
)

PROVENANCE = Provenance("original")


TOPIC_ISOMER = "ไอโซเมอร์โครงสร้างของสารประกอบอินทรีย์"


# (molecular formula, which isomers are counted, how many)
ISOMER_COUNTS = (
    ("C₄H₁₀", (ALKANE,), 2), ("C₅H₁₂", (ALKANE,), 3), ("C₆H₁₄", (ALKANE,), 5), ("C₄H₈", (ALKENE,), 3),
    ("C₄H₆", (ALKYNE,), 2), ("C₃H₇Cl", (HALO,), 2), ("C₄H₉Cl", (HALO,), 4), ("C₃H₈O", (ALCOHOL,), 2),
    ("C₄H₁₀O", (ALCOHOL,), 4), ("C₄H₁₀O", (ETHER,), 3), ("C₂H₆O", (ALCOHOL, ETHER), 2),
    ("C₃H₈O", (ALCOHOL, ETHER), 3), ("C₄H₁₀O", (ALCOHOL, ETHER), 7), ("C₃H₆O₂", (ACID, ESTER), 3),
    ("C₄H₈O", (ALDEHYDE, KETONE), 3), ("C₄H₈O₂", (ACID,), 2),
)


def _kinds(classes) -> str:
    return "และ".join(classes)


@question_type(
    "chem.structural_isomer_foundation",
    display_name={"th": "ระบุไอโซเมอร์จากสูตรโมเลกุล"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ISOMER,
)
class StructuralIsomerFoundation(QuestionType):
    """Isomers share a molecular formula and differ in structure."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        c = rng.choice([x for x in COMPOUNDS if isomers_of(x)])
        right = rng.choice(isomers_of(c))
        pool = [x for x in COMPOUNDS if molecular(x[1]) != molecular(c[1])]
        pool.sort(key=lambda x: (abs(carbons(x) - carbons(c)), x[2] != c[2]))
        wrongs = rng.sample(pool[:10], 3)
        return _labelled(stem=f"สารใดเป็นไอโซเมอร์โครงสร้างของ {c[1]}", correct=right[1],
                         wrongs=tuple(x[1] for x in wrongs), topic=TOPIC_ISOMER,
                         hint="ไอโซเมอร์มีสูตรโมเลกุลเดียวกันแต่สูตรโครงสร้างต่างกัน นับ C H O ของแต่ละข้อแล้วเทียบ")


@question_type(
    "chem.structural_isomer_fluency",
    display_name={"th": "นับจำนวนไอโซเมอร์โครงสร้าง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ISOMER,
)
class StructuralIsomerFluency(QuestionType):
    """Draw every chain and position without repeats, then count."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        formula, classes, count = rng.choice(ISOMER_COUNTS)
        if rng.random() < 0.5:
            members = [c for c in COMPOUNDS if molecular(c[1]) == formula and c[2] in classes]
            pick = rng.choice(members)
            others = [c for c in COMPOUNDS if c[2] in classes and molecular(c[1]) != formula]
            if len(others) < 3:
                others += [c for c in COMPOUNDS if c[2] not in classes and molecular(c[1]) != formula
                           and carbons(c) == carbons(pick)]
            return _labelled(stem=f"ข้อใดเป็นไอโซเมอร์หนึ่งของสารสูตรโมเลกุล {formula} ที่เป็น{_kinds(classes)}",
                             correct=f"{pick[0]} ({pick[1]})",
                             wrongs=tuple(f"{c[0]} ({c[1]})" for c in rng.sample(others, 3)), topic=TOPIC_ISOMER,
                             hint="นับอะตอมของแต่ละข้อให้ได้สูตรโมเลกุล แล้วเลือกข้อที่ตรงกับสูตรที่กำหนด")
        return numeric(stem=f"สารที่มีสูตรโมเลกุล {formula} ที่เป็น{_kinds(classes)} มีไอโซเมอร์โครงสร้างทั้งหมดกี่ไอโซเมอร์",
                       answer=count, wrongs=[count + 1, count - 1 or count + 2, count + 2], unit="ไอโซเมอร์",
                       topic=TOPIC_ISOMER,
                       hint="เขียนสายตรงก่อน แล้วลดสายหลักทีละ 1 คาร์บอนเป็นกิ่ง และเลื่อนตำแหน่งหมู่ฟังก์ชัน "
                            "ระวังโครงสร้างที่หมุนหรือกลับด้านแล้วซ้ำกัน")


@question_type(
    "chem.structural_isomer_application",
    display_name={"th": "ไอโซเมอร์ต่างหมู่ฟังก์ชันและต่างโครงสร้าง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ISOMER,
)
class StructuralIsomerApplication(QuestionType):
    """Same formula, a different class: alcohol ↔ ether, acid ↔ ester, aldehyde ↔ ketone."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        pairs = [(a, b) for a in COMPOUNDS for b in isomers_of(a) if a[2] != b[2]]
        a, b = rng.choice(pairs)
        if rng.random() < 0.5:
            pool = [x for x in COMPOUNDS if x[2] == b[2] and molecular(x[1]) != molecular(a[1])]
            pool += [x for x in isomers_of(a) if x[2] == a[2]]
            wrongs = rng.sample(pool, min(3, len(pool)))
            while len(wrongs) < 3:
                wrongs.append(rng.choice([x for x in COMPOUNDS if x not in wrongs and x is not b and x is not a
                                          and molecular(x[1]) != molecular(a[1])]))
            return _labelled(stem=f"สารใดเป็นไอโซเมอร์ของ {a[0]} ({a[1]}) แต่เป็นสารคนละประเภท",
                             correct=f"{b[0]} ({b[1]})", wrongs=tuple(f"{x[0]} ({x[1]})" for x in wrongs),
                             topic=TOPIC_ISOMER,
                             hint="หาสารที่มีสูตรโมเลกุลเท่ากันแต่หมู่ฟังก์ชันต่างกัน เช่น แอลกอฮอล์กับอีเทอร์ "
                                  "กรดกับเอสเทอร์ แอลดีไฮด์กับคีโตน")
        return _labelled(stem=f"{a[0]} ({a[1]}) กับ {b[0]} ({b[1]}) มีความสัมพันธ์กันอย่างไร",
                         correct=f"เป็นไอโซเมอร์กัน มีสูตรโมเลกุล {molecular(a[1])} เหมือนกันแต่หมู่ฟังก์ชันต่างกัน",
                         wrongs=("ไม่เป็นไอโซเมอร์กัน เพราะไอโซเมอร์ต้องมีหมู่ฟังก์ชันเดียวกันเท่านั้น",
                                 "เป็นสารชนิดเดียวกัน เพราะไอโซเมอร์ต้องมีสมบัติทุกอย่างเหมือนกัน",
                                 "ไม่เป็นไอโซเมอร์กัน เพราะไอโซเมอร์ต้องมีจุดเดือดเท่ากันด้วย"),
                         topic=TOPIC_ISOMER, hint="ไอโซเมอร์ไม่จำเป็นต้องอยู่ในประเภทเดียวกัน ขอให้สูตรโมเลกุลเท่ากัน")
