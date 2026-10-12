"""สารประกอบอินทรีย์ที่มีพันธะเดี่ยว พันธะคู่ และพันธะสามในชีวิตประจำวัน

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/1

Sets moved here from: science_wave_f26.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f26 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_BONDS = "สารประกอบอินทรีย์ที่มีพันธะเดี่ยว พันธะคู่ และพันธะสามในชีวิตประจำวัน"


# (name, condensed formula, everyday use, atoms {element: count}, single, double, triple bonds)
EVERYDAY = (
    ("มีเทน", "CH₄", "แก๊สชีวภาพและแก๊สธรรมชาติ", {"C": 1, "H": 4}, 4, 0, 0),
    ("โพรเพน", "CH₃CH₂CH₃", "แก๊สหุงต้ม (LPG)", {"C": 3, "H": 8}, 10, 0, 0),
    ("บิวเทน", "CH₃CH₂CH₂CH₃", "แก๊สในไฟแช็ก", {"C": 4, "H": 10}, 13, 0, 0),
    ("เอทานอล", "CH₃CH₂OH", "แอลกอฮอล์ล้างแผล", {"C": 2, "H": 6, "O": 1}, 8, 0, 0),
    ("เมทานอล", "CH₃OH", "เชื้อเพลิงและตัวทำละลาย", {"C": 1, "H": 4, "O": 1}, 5, 0, 0),
    ("กลีเซอรอล", "HOCH₂CH(OH)CH₂OH", "ส่วนผสมในเครื่องสำอางและสบู่", {"C": 3, "H": 8, "O": 3}, 13, 0, 0),
    ("เอทีน (เอทิลีน)", "CH₂=CH₂", "แก๊สเร่งการสุกของผลไม้", {"C": 2, "H": 4}, 4, 1, 0),
    ("โพรพีน", "CH₂=CHCH₃", "วัตถุดิบผลิตพลาสติกพอลิโพรพิลีน", {"C": 3, "H": 6}, 7, 1, 0),
    ("บิวทาไดอีน", "CH₂=CHCH=CH₂", "วัตถุดิบผลิตยางสังเคราะห์", {"C": 4, "H": 6}, 7, 2, 0),
    ("ไวนิลคลอไรด์", "CH₂=CHCl", "วัตถุดิบผลิตท่อพลาสติก PVC", {"C": 2, "H": 3, "Cl": 1}, 4, 1, 0),
    ("เตตระฟลูออโรเอทีน", "CF₂=CF₂", "วัตถุดิบผลิตเทฟลอนเคลือบกระทะ", {"C": 2, "F": 4}, 4, 1, 0),
    ("กรดแอซีติก", "CH₃COOH", "น้ำส้มสายชู", {"C": 2, "H": 4, "O": 2}, 6, 1, 0),
    ("กรดฟอร์มิก", "HCOOH", "สารในน้ำกรดของมดแดง", {"C": 1, "H": 2, "O": 2}, 3, 1, 0),
    ("แอซีโตน", "CH₃COCH₃", "น้ำยาล้างเล็บ", {"C": 3, "H": 6, "O": 1}, 8, 1, 0),
    ("ฟอร์มาลดีไฮด์", "HCHO", "ฟอร์มาลินสำหรับรักษาสภาพตัวอย่างสิ่งมีชีวิต", {"C": 1, "H": 2, "O": 1}, 2, 1, 0),
    ("ยูเรีย", "(NH₂)₂CO", "ปุ๋ยไนโตรเจน", {"C": 1, "H": 4, "O": 1, "N": 2}, 6, 1, 0),
    ("เอทิลแอซีเตต", "CH₃COOCH₂CH₃", "ตัวทำละลายในกาวและน้ำยาล้างเล็บ", {"C": 4, "H": 8, "O": 2}, 12, 1, 0),
    ("เอไทน์ (แอซีทิลีน)", "HC≡CH", "แก๊สจากถ่านแก๊สใช้เชื่อมและตัดโลหะ", {"C": 2, "H": 2}, 2, 0, 1),
    ("ไฮโดรเจนไซยาไนด์", "HCN", "สารพิษที่พบในมันสำปะหลังดิบ", {"C": 1, "H": 1, "N": 1}, 1, 0, 1),
    ("แอซีโตไนไตรล์", "CH₃CN", "ตัวทำละลายในห้องปฏิบัติการ", {"C": 2, "H": 3, "N": 1}, 4, 0, 1),
)


HYDROCARBONS = tuple(e for e in EVERYDAY if set(e[3]) == {"C", "H"})


def bond_kind(e) -> str:
    if e[6]:
        return "มีพันธะสาม"
    if e[5]:
        return "มีพันธะคู่"
    return "มีแต่พันธะเดี่ยว"


BOND_KINDS = ("มีแต่พันธะเดี่ยว", "มีพันธะคู่", "มีพันธะสาม")


@question_type(
    "chem.organic_bond_foundation",
    display_name={"th": "ชนิดพันธะในสารประกอบอินทรีย์ที่พบในชีวิตประจำวัน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BONDS,
)
class OrganicBondFoundation(QuestionType):
    """Read the bond type off the condensed formula."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ในสูตรแบบย่อ = คือพันธะคู่ ≡ คือพันธะสาม ส่วน C=O ใน -COOH -CO- -CHO ก็เป็นพันธะคู่"
        if rng.random() < 0.5:
            e = rng.choice(EVERYDAY)
            right = bond_kind(e)
            return _labelled(stem=f"{e[0]} ({e[1]}) ใช้เป็น{e[2]} ในโมเลกุลมีพันธะแบบใด", correct=right,
                             wrongs=tuple(k for k in BOND_KINDS if k != right) + ("มีพันธะไอออนิก",),
                             topic=TOPIC_BONDS, hint=hint)
        kind = rng.choice(BOND_KINDS)
        pick = rng.choice([e for e in EVERYDAY if bond_kind(e) == kind])
        others = [e for e in EVERYDAY if bond_kind(e) != kind]
        label = lambda e: f"{e[0]} ({e[1]})"
        return _labelled(stem=f"สารในชีวิตประจำวันข้อใด{kind}", correct=label(pick),
                         wrongs=tuple(label(e) for e in rng.sample(others, 3)), topic=TOPIC_BONDS, hint=hint)


@question_type(
    "chem.organic_bond_fluency",
    display_name={"th": "นับพันธะเดี่ยว พันธะคู่ และพันธะสามในโมเลกุล"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BONDS,
)
class OrganicBondFluency(QuestionType):
    """Expand the condensed formula to count every bond, C–H and O–H included."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        e = rng.choice(EVERYDAY)
        hint = ("เขียนสูตรโครงสร้างลิวอิสให้ C มี 4 พันธะ N 3 O 2 H และแฮโลเจน 1 "
                "แล้วนับทุกพันธะรวมถึง C–H และ O–H")
        ask = rng.choice(("single", "total") if not (e[5] or e[6]) else ("single", "multiple", "total"))
        if ask == "single":
            return numeric(stem=f"{e[0]} ({e[1]}) มีพันธะเดี่ยวทั้งหมดกี่พันธะ", answer=e[4],
                           wrongs=[e[4] - e[3].get("H", 0) or e[4] + 2, e[4] + 1, e[4] + e[5] + e[6]], unit="พันธะ",
                           topic=TOPIC_BONDS, hint=hint)
        if ask == "multiple":
            kind, count = ("พันธะสาม", e[6]) if e[6] else ("พันธะคู่", e[5])
            return numeric(stem=f"{e[0]} ({e[1]}) มี{kind}กี่พันธะ", answer=count,
                           wrongs=[count + 1, count * 2 + 1, count + 2], unit="พันธะ", topic=TOPIC_BONDS, hint=hint)
        total = e[4] + e[5] + e[6]
        return numeric(stem=f"{e[0]} ({e[1]}) มีพันธะระหว่างอะตอมทั้งหมดกี่พันธะ (พันธะคู่หรือพันธะสามนับเป็น 1 พันธะ)",
                       answer=total, wrongs=[e[4] + 2 * e[5] + 3 * e[6] if e[5] or e[6] else total + 1, total - 1 or 2,
                                             sum(e[3].values())], unit="พันธะ", topic=TOPIC_BONDS, hint=hint)


@question_type(
    "chem.organic_bond_application",
    display_name={"th": "ไฮโดรคาร์บอนอิ่มตัวและไม่อิ่มตัว และการใช้ประโยชน์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BONDS,
)
class OrganicBondApplication(QuestionType):
    """Saturated means single bonds only; match compound, use and bond type."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            saturated = rng.random() < 0.5
            match = [e for e in HYDROCARBONS if (bond_kind(e) == "มีแต่พันธะเดี่ยว") == saturated]
            others = [e for e in HYDROCARBONS if e not in match]
            pick = rng.choice(match)
            return _labelled(stem=f"สารในข้อใดเป็นไฮโดรคาร์บอน{'อิ่มตัว' if saturated else 'ไม่อิ่มตัว'}",
                             correct=f"{pick[1]} ({pick[2]})",
                             wrongs=tuple(f"{e[1]} ({e[2]})" for e in rng.sample(others, min(3, len(others)))),
                             topic=TOPIC_BONDS,
                             hint="ไฮโดรคาร์บอนอิ่มตัวมีแต่พันธะเดี่ยวระหว่าง C ส่วนไม่อิ่มตัวมีพันธะคู่หรือพันธะสามระหว่าง C")
        right = rng.choice(EVERYDAY)
        wrongs = []
        for e in rng.sample([x for x in EVERYDAY if x is not right], 3):
            wrong_kind = rng.choice([k for k in BOND_KINDS if k != bond_kind(e)])
            wrongs.append(f"{e[0]} ใช้เป็น{e[2]} {wrong_kind}")
        return _labelled(stem="ข้อใดกล่าวถึงสาร การใช้ประโยชน์ และชนิดพันธะในโมเลกุลได้ถูกต้อง",
                         correct=f"{right[0]} ใช้เป็น{right[2]} {bond_kind(right)}", wrongs=tuple(wrongs),
                         topic=TOPIC_BONDS, hint="เขียนสูตรโครงสร้างของแต่ละสารแล้วตรวจชนิดพันธะทีละข้อ")
