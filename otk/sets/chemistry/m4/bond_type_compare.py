"""สมบัติและการใช้ประโยชน์ของสารประกอบไอออนิก สารโคเวเลนต์ และโลหะ

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/21

Sets moved here from: science_wave_f24.
"""

from __future__ import annotations

from itertools import permutations
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f24 import SUBJECT

PROVENANCE = Provenance("original")


UPPER_FOUR = {"th": "ม.4"}


TOPIC_COMPARE = "สมบัติและการใช้ประโยชน์ของสารประกอบไอออนิก สารโคเวเลนต์ และโลหะ"


IONIC = "สารประกอบไอออนิก"


MOLECULAR = "สารโคเวเลนต์แบบโมเลกุล"


NETWORK = "สารโคเวเลนต์โครงร่างตาข่าย"


METAL = "โลหะ"


KINDS = (IONIC, MOLECULAR, NETWORK, METAL)


SAMPLES = (
    ("NaCl (โซเดียมคลอไรด์)", IONIC), ("MgO (แมกนีเซียมออกไซด์)", IONIC), ("CaF₂ (แคลเซียมฟลูออไรด์)", IONIC),
    ("KBr (โพแทสเซียมโบรไมด์)", IONIC), ("KNO₃ (โพแทสเซียมไนเตรต)", IONIC), ("CaCO₃ (แคลเซียมคาร์บอเนต)", IONIC),
    ("Na₂SO₄ (โซเดียมซัลเฟต)", IONIC), ("NH₄Cl (แอมโมเนียมคลอไรด์)", IONIC), ("CuSO₄ (คอปเปอร์(II) ซัลเฟต)", IONIC),
    ("H₂O (น้ำ)", MOLECULAR), ("CO₂ (คาร์บอนไดออกไซด์)", MOLECULAR), ("C₆H₁₂O₆ (กลูโคส)", MOLECULAR),
    ("CH₄ (มีเทน)", MOLECULAR), ("I₂ (ไอโอดีน)", MOLECULAR), ("C₂H₅OH (เอทานอล)", MOLECULAR),
    ("NH₃ (แอมโมเนีย)", MOLECULAR), ("S₈ (กำมะถัน)", MOLECULAR), ("SiO₂ (ซิลิคอนไดออกไซด์)", NETWORK),
    ("C (เพชร)", NETWORK), ("C (แกรไฟต์)", NETWORK), ("SiC (ซิลิคอนคาร์ไบด์)", NETWORK), ("Si (ซิลิคอน)", NETWORK),
    ("Cu (ทองแดง)", METAL), ("Fe (เหล็ก)", METAL), ("Al (อะลูมิเนียม)", METAL), ("Mg (แมกนีเซียม)", METAL),
    ("Zn (สังกะสี)", METAL), ("Ag (เงิน)", METAL), ("Au (ทองคำ)", METAL), ("K₂O (โพแทสเซียมออกไซด์)", IONIC),
    ("LiF (ลิเทียมฟลูออไรด์)", IONIC), ("HCl (ไฮโดรเจนคลอไรด์)", MOLECULAR), ("CCl₄ (คาร์บอนเตตระคลอไรด์)", MOLECULAR),
    ("P₄ (ฟอสฟอรัสขาว)", MOLECULAR), ("Ca (แคลเซียม)", METAL),
)


# kind: (the clue that decides it, extra clues, melting-point range °C)
PROFILES = {
    IONIC: ("ของแข็งไม่นำไฟฟ้า แต่เมื่อหลอมเหลวนำไฟฟ้าได้",
            ("ละลายน้ำได้และสารละลายนำไฟฟ้า", "แข็งแต่เปราะ แตกเมื่อทุบ"), (600, 1100)),
    METAL: ("นำไฟฟ้าได้ทั้งในสถานะของแข็งและของเหลว",
            ("ตีแผ่เป็นแผ่นบางได้", "ผิวมันวาว", "นำความร้อนได้ดี"), (300, 1600)),
    MOLECULAR: ("ไม่นำไฟฟ้าทั้งในสถานะของแข็งและของเหลว",
                ("ระเหยได้ง่าย", "ของแข็งค่อนข้างอ่อน"), (-150, 150)),
    NETWORK: ("ของแข็งไม่นำไฟฟ้า และแข็งมาก",
              ("ไม่ละลายน้ำ", "หลอมเหลวยากมาก"), (1400, 3600)),
}


USES = (
    ("ทำสายไฟฟ้า", "ทองแดง", METAL), ("โรยถนนละลายน้ำแข็งและถนอมอาหาร", "โซเดียมคลอไรด์", IONIC),
    ("เป็นเชื้อเพลิงหุงต้ม", "โพรเพน", MOLECULAR), ("ทำปุ๋ยที่ให้ธาตุไนโตรเจนและโพแทสเซียม", "โพแทสเซียมไนเตรต", IONIC),
    ("ทำแก้ว", "ซิลิคอนไดออกไซด์", NETWORK), ("ทำหัวเจาะ", "เพชร", NETWORK),
    ("ทำกระป๋องเครื่องดื่มและฟอยล์", "อะลูมิเนียม", METAL), ("ผสมในยาสีฟันป้องกันฟันผุ", "โซเดียมฟลูออไรด์", IONIC),
    ("ฆ่าเชื้อโรคบนผิวหนัง", "เอทานอล", MOLECULAR), ("ทำชิปคอมพิวเตอร์", "ซิลิคอน", NETWORK),
    ("อัดในเครื่องดื่มให้มีฟอง", "คาร์บอนไดออกไซด์", MOLECULAR), ("ทำปูนและชอล์ก", "แคลเซียมคาร์บอเนต", IONIC),
)


# Melting points °C: every network solid here melts above every ionic one, and every ionic one above every molecule.
MELT_NETWORK = (("เพชร", 3550), ("ซิลิคอนคาร์ไบด์", 2730), ("ซิลิคอนไดออกไซด์", 1713), ("ซิลิคอน", 1414))


MELT_IONIC = (("NaCl", 801), ("KCl", 770), ("KBr", 734), ("NaF", 993), ("LiF", 845), ("CaCl₂", 772))


MELT_MOLECULAR = (("I₂", 114), ("น้ำแข็ง (H₂O)", 0), ("กำมะถัน (S₈)", 115), ("แนฟทาลีน", 80), ("CH₄", -182))


@question_type(
    "chem.bond_type_compare_foundation",
    display_name={"th": "จำแนกสารเป็นสารประกอบไอออนิก สารโคเวเลนต์ หรือโลหะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_COMPARE,
)
class BondTypeCompareFoundation(QuestionType):
    """Metal with non-metal is ionic, non-metals alone are covalent, a metal alone is metallic."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        label, kind = rng.choice(SAMPLES)
        return _labelled(stem=f"{label} จัดเป็นสารประเภทใด", correct=kind,
                         wrongs=tuple(k for k in KINDS if k != kind), topic=TOPIC_COMPARE,
                         hint="โลหะกับอโลหะ (หรือไอออนกลุ่มอะตอม) เป็นสารประกอบไอออนิก อโลหะกับอโลหะเป็นสารโคเวเลนต์ "
                              "(C, Si, SiO₂, SiC เป็นโครงร่างตาข่าย) ธาตุโลหะล้วนมีพันธะโลหะ")


@question_type(
    "chem.bond_type_compare_fluency",
    display_name={"th": "ระบุประเภทของสารจากสมบัติ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_COMPARE,
)
class BondTypeCompareFluency(QuestionType):
    """Conduction by state separates the kinds; the melting point separates the two covalent ones."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(KINDS)
        key, extras, (low, high) = PROFILES[kind]
        clues = [key, *rng.sample(extras, rng.randint(1, len(extras)))]
        rng.shuffle(clues)
        melt = rng.randint(low, high)
        return _labelled(stem=f"สาร X มีจุดหลอมเหลว {melt} °C {' '.join(clues)} สาร X น่าจะเป็นสารประเภทใด",
                         correct=kind, wrongs=tuple(k for k in KINDS if k != kind), topic=TOPIC_COMPARE,
                         hint="ดูการนำไฟฟ้าก่อน: โลหะนำไฟฟ้าทั้งของแข็งและของเหลว สารไอออนิกนำไฟฟ้าเมื่อหลอมเหลว "
                              "สารโคเวเลนต์ไม่นำไฟฟ้า แล้วแยกโมเลกุล (จุดหลอมเหลวต่ำ) กับโครงร่างตาข่าย (สูงมาก)")


@question_type(
    "chem.bond_type_compare_application",
    display_name={"th": "เปรียบเทียบจุดหลอมเหลวและเลือกใช้สารตามสมบัติ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_COMPARE,
)
class BondTypeCompareApplication(QuestionType):
    """Order a network solid, an ionic compound and a molecule, or pick a substance for a use."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            trio = (rng.choice(MELT_NETWORK)[0], rng.choice(MELT_IONIC)[0], rng.choice(MELT_MOLECULAR)[0])
            shown = rng.sample(trio, 3)
            right = " > ".join(trio)
            others = [" > ".join(p) for p in permutations(trio) if p != trio]
            return _labelled(stem=f"เรียงจุดหลอมเหลวของ {', '.join(shown)} จากสูงไปต่ำ", correct=right,
                             wrongs=tuple(others), topic=TOPIC_COMPARE,
                             hint="โครงร่างตาข่ายต้องสลายพันธะโคเวเลนต์ > สารไอออนิกต้องเอาชนะแรงดึงดูดระหว่างไอออน "
                                  "> สารโมเลกุลเอาชนะเพียงแรงระหว่างโมเลกุล")
        use, name, kind = rng.choice(USES)
        others = [u for u in USES if u[1] != name]
        return _labelled(stem=f"สารใดเหมาะนำมา{use}", correct=f"{name} ({kind})",
                         wrongs=tuple(f"{u[1]} ({u[2]})" for u in rng.sample(others, 3)), topic=TOPIC_COMPARE,
                         hint="เลือกสารที่มีสมบัติตรงกับงาน เช่น นำไฟฟ้า ละลายน้ำ เผาไหม้ได้ หรือแข็งมาก")
