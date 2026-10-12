"""การเรียกชื่อสารประกอบอินทรีย์ตามระบบ IUPAC

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/4

Sets moved here from: science_wave_f27.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f27 import (
    COMPOUNDS,
    SUBJECT,
    UPPER_SIX,
    atoms_of,
    carbons,
    isomers_of,
)

PROVENANCE = Provenance("original")


TOPIC_NAME = "การเรียกชื่อสารประกอบอินทรีย์ตามระบบ IUPAC"


BY_NAME = {c[0]: c for c in COMPOUNDS}


# Common wrong names: a numbering or chain slip, and the name it should have been.
MISNAMED = (
    ("3-เมทิลบิวเทน", "2-เมทิลบิวเทน"), ("1-เมทิลโพรเพน", "บิวเทน"), ("บิวต์-3-อีน", "บิวต์-1-อีน"),
    ("2-เอทิลบิวเทน", "3-เมทิลเพนเทน"), ("บิวทาน-3-ออล", "บิวทาน-2-ออล"), ("4-เมทิลเพนเทน", "2-เมทิลเพนเทน"),
    ("เพนทาน-4-โอน", "เพนทาน-2-โอน"), ("เพนต์-4-อีน", "เพนต์-1-อีน"), ("3-คลอโรโพรเพน", "1-คลอโรโพรเพน"),
    ("2-เอทิลโพรเพน", "2-เมทิลบิวเทน"), ("1-เมทิลบิวเทน", "เพนเทน"), ("3-คลอโรบิวเทน", "2-คลอโรบิวเทน"),
)


def _name_wrongs(rng: Random, c) -> tuple[str, ...]:
    """Isomers first (same formula, other structure), then the same class one carbon off."""
    near = [x[0] for x in isomers_of(c)]
    rng.shuffle(near)
    same = [x[0] for x in COMPOUNDS if x[2] == c[2] and x is not c and x[0] not in near]
    same.sort(key=lambda n: abs(carbons(BY_NAME[n]) - carbons(c)))
    rest = [x[0] for x in COMPOUNDS if x is not c and x[0] not in near and x[0] not in same]
    pool = near[:2] + same[:4]
    picks = rng.sample(pool, min(3, len(pool)))
    while len(picks) < 3:
        picks.append(rng.choice([n for n in rest if n not in picks]))
    return tuple(picks)


@question_type(
    "chem.iupac_name_foundation",
    display_name={"th": "เรียกชื่อสารประกอบอินทรีย์จากสูตรโครงสร้าง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_NAME,
)
class IupacNameFoundation(QuestionType):
    """Longest chain gives the root, the group gives the ending, the lowest numbers win."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        c = rng.choice(COMPOUNDS)
        return _labelled(stem=f"สาร {c[1]} มีชื่อตามระบบ IUPAC ว่าอย่างไร", correct=c[0], wrongs=_name_wrongs(rng, c),
                         topic=TOPIC_NAME,
                         hint="หาสายคาร์บอนที่ยาวที่สุดเป็นชื่อหลัก ลงท้ายตามหมู่ฟังก์ชัน (-เอน -อีน -ไอน์ -ออล -อัล "
                              "-โอน -โอิก -โอเอต) และให้ตำแหน่งหมู่ฟังก์ชันหรือกิ่งมีตัวเลขน้อยที่สุด")


@question_type(
    "chem.iupac_name_fluency",
    display_name={"th": "เขียนสูตรโครงสร้างจากชื่อ IUPAC"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_NAME,
)
class IupacNameFluency(QuestionType):
    """From the name back to a structure: the right structure against its isomers."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        c = rng.choice(COMPOUNDS)
        wrongs = [BY_NAME[n][1] for n in _name_wrongs(rng, c)]
        if rng.random() < 0.5:
            return _labelled(stem=f"{c[0]} มีสูตรโครงสร้างแบบย่อใด", correct=c[1], wrongs=tuple(wrongs), topic=TOPIC_NAME,
                             hint="ชื่อหลักบอกจำนวนคาร์บอนในสายหลัก (เมท 1 เอท 2 โพรพ 3 บิวท 4 เพนท 5 เฮกซ 6) "
                                  "ตัวเลขบอกตำแหน่งของกิ่งหรือหมู่ฟังก์ชัน")
        atoms = atoms_of(c[1])
        element = rng.choice(["C", "H"] + [k for k in atoms if k not in ("C", "H")])
        label = {"C": "คาร์บอน", "H": "ไฮโดรเจน", "O": "ออกซิเจน", "N": "ไนโตรเจน", "Cl": "คลอรีน"}[element]
        return numeric(stem=f"{c[0]} หนึ่งโมเลกุลมีอะตอม{label}กี่อะตอม", answer=atoms[element],
                       wrongs=[atoms[element] + 1, atoms[element] + 2, atoms[element] * 2], unit="อะตอม",
                       topic=TOPIC_NAME, hint="เขียนสูตรโครงสร้างจากชื่อก่อน แล้วนับอะตอม (C มี 4 พันธะเสมอ)")


@question_type(
    "chem.iupac_name_application",
    display_name={"th": "ตรวจและแก้ชื่อที่ผิดหลัก IUPAC"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_NAME,
)
class IupacNameApplication(QuestionType):
    """Spot a chain or numbering slip and give the right name."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ตรวจว่าเลือกสายที่ยาวที่สุดหรือไม่ และนับตำแหน่งจากปลายที่ทำให้ตัวเลขน้อยที่สุดหรือไม่"
        wrong, right = rng.choice(MISNAMED)
        if rng.random() < 0.5:
            return _labelled(stem=f"ชื่อ \"{wrong}\" ผิดหลัก IUPAC ชื่อที่ถูกต้องของสารนี้คือข้อใด", correct=right,
                             wrongs=tuple(_name_wrongs(rng, BY_NAME[right])[:2]) + (wrong,), topic=TOPIC_NAME,
                             hint=hint)
        bad = rng.sample([w for w, _ in MISNAMED if w != wrong], 2) + [wrong]
        return _labelled(stem="ชื่อใดถูกต้องตามหลัก IUPAC", correct=right, wrongs=tuple(bad), topic=TOPIC_NAME,
                         hint=hint)
