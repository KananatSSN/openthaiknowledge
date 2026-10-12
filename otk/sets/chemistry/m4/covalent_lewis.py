"""พันธะโคเวเลนต์และโครงสร้างลิวอิส

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/14

Sets moved here from: science_wave_f22.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f22 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_LEWIS = "พันธะโคเวเลนต์และโครงสร้างลิวอิส"


# (formula, Thai name, single bonds, double bonds, triple bonds, lone pairs on the whole molecule)
MOLECULES = (
    ("H₂", "ไฮโดรเจน", 1, 0, 0, 0), ("Cl₂", "คลอรีน", 1, 0, 0, 6), ("O₂", "ออกซิเจน", 0, 1, 0, 4),
    ("N₂", "ไนโตรเจน", 0, 0, 1, 2), ("HCl", "ไฮโดรเจนคลอไรด์", 1, 0, 0, 3), ("H₂O", "น้ำ", 2, 0, 0, 2),
    ("NH₃", "แอมโมเนีย", 3, 0, 0, 1), ("CH₄", "มีเทน", 4, 0, 0, 0), ("CO₂", "คาร์บอนไดออกไซด์", 0, 2, 0, 4),
    ("C₂H₄", "เอทีน", 4, 1, 0, 0), ("C₂H₂", "เอไทน์", 2, 0, 1, 0), ("HCN", "ไฮโดรเจนไซยาไนด์", 1, 0, 1, 1),
    ("CCl₄", "คาร์บอนเตตระคลอไรด์", 4, 0, 0, 12), ("PCl₃", "ฟอสฟอรัสไตรคลอไรด์", 3, 0, 0, 10),
    ("H₂S", "ไฮโดรเจนซัลไฟด์", 2, 0, 0, 2), ("CH₂O", "เมทานาล", 2, 1, 0, 2), ("HF", "ไฮโดรเจนฟลูออไรด์", 1, 0, 0, 3),
    ("C₂H₆", "อีเทน", 7, 0, 0, 0),
)


def _bond_kind(m) -> str:
    if m[4]:
        return "มีพันธะสาม"
    if m[3]:
        return "มีพันธะคู่"
    return "มีแต่พันธะเดี่ยว"


@question_type(
    "chem.covalent_lewis_foundation",
    display_name={"th": "ชนิดของพันธะโคเวเลนต์ในโมเลกุล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LEWIS,
)
class CovalentLewisFoundation(QuestionType):
    """Single, double or triple: read off the Lewis structure."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        m = rng.choice(MOLECULES)
        if rng.random() < 0.5:
            right = _bond_kind(m)
            return _labelled(stem=f"โมเลกุล {m[0]} ({m[1]}) มีพันธะโคเวเลนต์แบบใด", correct=right,
                             wrongs=tuple(k for k in ("มีแต่พันธะเดี่ยว", "มีพันธะคู่", "มีพันธะสาม", "มีพันธะไอออนิก") if k != right)[:3],
                             topic=TOPIC_LEWIS, hint="พันธะเดี่ยวใช้อิเล็กตรอนร่วมกัน 1 คู่ พันธะคู่ 2 คู่ พันธะสาม 3 คู่")
        kind = rng.choice(("มีพันธะสาม", "มีพันธะคู่"))
        match = [x for x in MOLECULES if _bond_kind(x) == kind]
        others = [x for x in MOLECULES if _bond_kind(x) != kind]
        pick = rng.choice(match)
        return _labelled(stem=f"โมเลกุลใด{kind}", correct=f"{pick[0]}",
                         wrongs=tuple(x[0] for x in rng.sample(others, 3)), topic=TOPIC_LEWIS,
                         hint="เขียนโครงสร้างลิวอิสให้ทุกอะตอมครบออกเตต (ไฮโดรเจนครบ 2) แล้วนับคู่อิเล็กตรอนระหว่างอะตอม")


@question_type(
    "chem.covalent_lewis_fluency",
    display_name={"th": "นับคู่อิเล็กตรอนร่วมพันธะและคู่อิเล็กตรอนโดดเดี่ยว"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LEWIS,
)
class CovalentLewisFluency(QuestionType):
    """Bonding pairs = singles + 2 × doubles + 3 × triples; lone pairs are the rest."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        m = rng.choice(MOLECULES)
        bonding = m[2] + 2 * m[3] + 3 * m[4]
        if rng.random() < 0.5:
            return numeric(stem=f"โครงสร้างลิวอิสของ {m[0]} ({m[1]}) มีอิเล็กตรอนคู่ร่วมพันธะทั้งหมดกี่คู่",
                           answer=bonding, wrongs=[m[2] + m[3] + m[4], bonding * 2, bonding + m[5]], unit="คู่",
                           topic=TOPIC_LEWIS, hint="พันธะคู่นับเป็น 2 คู่ พันธะสามนับเป็น 3 คู่")
        return numeric(stem=f"โครงสร้างลิวอิสของ {m[0]} ({m[1]}) มีอิเล็กตรอนคู่โดดเดี่ยวทั้งหมดกี่คู่",
                       answer=m[5], wrongs=[m[5] + 1, bonding, m[5] * 2 if m[5] else 2], unit="คู่",
                       topic=TOPIC_LEWIS, hint="คู่โดดเดี่ยวคือคู่อิเล็กตรอนที่ไม่ได้ใช้สร้างพันธะ นับรวมทุกอะตอม")


@question_type(
    "chem.covalent_lewis_application",
    display_name={"th": "จำนวนอิเล็กตรอนเวเลนซ์ทั้งหมดในโครงสร้างลิวอิส"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LEWIS,
)
class CovalentLewisApplication(QuestionType):
    """Every valence electron sits either in a bond or in a lone pair."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        m = rng.choice(MOLECULES)
        bonding = m[2] + 2 * m[3] + 3 * m[4]
        total = 2 * (bonding + m[5])
        shape = rng.randrange(2)
        if shape == 0:
            return numeric(stem=f"โครงสร้างลิวอิสของ {m[0]} ({m[1]}) ใช้เวเลนซ์อิเล็กตรอนทั้งหมดกี่ตัว",
                           answer=total, wrongs=[bonding + m[5], 2 * bonding, total + 2], unit="ตัว", topic=TOPIC_LEWIS,
                           hint="เวเลนซ์อิเล็กตรอนทั้งหมด = 2 × (คู่ร่วมพันธะ + คู่โดดเดี่ยว) = ผลรวมเวเลนซ์อิเล็กตรอนของทุกอะตอม")
        return numeric(
            stem=(f"{m[0]} ({m[1]}) มีเวเลนซ์อิเล็กตรอนรวม {total} ตัว และมีอิเล็กตรอนคู่ร่วมพันธะ {bonding} คู่ "
                  "มีอิเล็กตรอนคู่โดดเดี่ยวกี่คู่"),
            answer=m[5], wrongs=[total - bonding, total // 2, m[5] + 2], unit="คู่", topic=TOPIC_LEWIS,
            hint="คู่โดดเดี่ยว = (อิเล็กตรอนทั้งหมด ÷ 2) − คู่ร่วมพันธะ")
