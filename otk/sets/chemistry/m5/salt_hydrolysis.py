"""ไฮโดรลิซิสของเกลือ

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/19

Sets moved here from: science_wave_f36.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f36 import ACIDIC, BASIC, NEUTRAL, SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_SALT = "ไฮโดรลิซิสของเกลือ"


# (salt, parent acid, parent base, nature, hydrolysis equation or None)
SALTS = (
    ("NaCl", "HCl", "NaOH", NEUTRAL, None), ("KNO₃", "HNO₃", "KOH", NEUTRAL, None),
    ("Na₂SO₄", "H₂SO₄", "NaOH", NEUTRAL, None), ("KBr", "HBr", "KOH", NEUTRAL, None),
    ("CH₃COONa", "CH₃COOH", "NaOH", BASIC, "CH₃COO⁻ + H₂O ⇌ CH₃COOH + OH⁻"),
    ("NaF", "HF", "NaOH", BASIC, "F⁻ + H₂O ⇌ HF + OH⁻"),
    ("KCN", "HCN", "KOH", BASIC, "CN⁻ + H₂O ⇌ HCN + OH⁻"),
    ("Na₂CO₃", "H₂CO₃", "NaOH", BASIC, "CO₃²⁻ + H₂O ⇌ HCO₃⁻ + OH⁻"),
    ("HCOONa", "HCOOH", "NaOH", BASIC, "HCOO⁻ + H₂O ⇌ HCOOH + OH⁻"),
    ("NH₄Cl", "HCl", "NH₃", ACIDIC, "NH₄⁺ + H₂O ⇌ NH₃ + H₃O⁺"),
    ("NH₄NO₃", "HNO₃", "NH₃", ACIDIC, "NH₄⁺ + H₂O ⇌ NH₃ + H₃O⁺"),
    ("(NH₄)₂SO₄", "H₂SO₄", "NH₃", ACIDIC, "NH₄⁺ + H₂O ⇌ NH₃ + H₃O⁺"),
)


LITMUS = {ACIDIC: "เปลี่ยนกระดาษลิตมัสสีน้ำเงินเป็นสีแดง", BASIC: "เปลี่ยนกระดาษลิตมัสสีแดงเป็นสีน้ำเงิน",
          NEUTRAL: "ไม่เปลี่ยนสีกระดาษลิตมัสทั้งสองสี"}


@question_type(
    "chem.salt_hydrolysis_foundation",
    display_name={"th": "ความเป็นกรด-เบสของสารละลายเกลือ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SALT,
)
class SaltHydrolysisFoundation(QuestionType):
    """The ion from the weak parent reacts with water."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        salt, acid, base, nature, _ = rng.choice(SALTS)
        if rng.random() < 0.5:
            return _labelled(stem=f"สารละลายเกลือ {salt} มีสมบัติอย่างไร", correct=nature,
                             wrongs=tuple(x for x in (ACIDIC, BASIC, NEUTRAL, "เป็นกรดหรือเบสขึ้นกับความเข้มข้น") if x != nature),
                             topic=TOPIC_SALT,
                             hint="เกลือจากกรดแก่+เบสแก่เป็นกลาง กรดอ่อน+เบสแก่เป็นเบส กรดแก่+เบสอ่อนเป็นกรด")
        right = f"{acid} กับ {base}"
        others = sorted({f"{s[1]} กับ {s[2]}" for s in SALTS} - {right})
        return _labelled(stem=f"เกลือ {salt} เกิดจากกรดและเบสคู่ใด", correct=right, wrongs=tuple(others),
                         topic=TOPIC_SALT, hint="ไอออนบวกของเกลือมาจากเบส ไอออนลบมาจากกรด")


@question_type(
    "chem.salt_hydrolysis_fluency",
    display_name={"th": "สมการไฮโดรลิซิสของเกลือ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SALT,
)
class SaltHydrolysisFluency(QuestionType):
    """Only the ion from the weak parent hydrolyses."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        salt, _, _, nature, equation = rng.choice([s for s in SALTS if s[4]])
        others = sorted({s[4] for s in SALTS if s[4] and s[4] != equation})
        wrong_ion = {"Na": "Na⁺ + H₂O ⇌ NaOH + H⁺", "K": "K⁺ + H₂O ⇌ KOH + H⁺"}
        cation_wrong = next((v for k, v in wrong_ion.items() if salt.startswith(k)), "SO₄²⁻ + H₂O ⇌ HSO₄⁻ + OH⁻")
        return _labelled(stem=f"สมการไฮโดรลิซิสที่ทำให้สารละลาย {salt} {nature}คือข้อใด", correct=equation,
                         wrongs=(cation_wrong, *rng.sample(others, 2)), topic=TOPIC_SALT,
                         hint="ไอออนที่มาจากกรดอ่อนรับ H⁺ จากน้ำให้ OH⁻ ไอออนที่มาจากเบสอ่อนให้ H⁺ แก่น้ำได้ H₃O⁺")


@question_type(
    "chem.salt_hydrolysis_application",
    display_name={"th": "ทดสอบสารละลายเกลือด้วยกระดาษลิตมัส"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SALT,
)
class SaltHydrolysisApplication(QuestionType):
    """Predict the litmus result, or pick the salt that gives one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        salt, _, _, nature, _ = rng.choice(SALTS)
        if rng.random() < 0.5:
            return _labelled(stem=f"สารละลายเกลือ {salt} ให้ผลกับกระดาษลิตมัสอย่างไร", correct=LITMUS[nature],
                             wrongs=tuple(v for k, v in LITMUS.items() if k != nature) + ("เปลี่ยนกระดาษลิตมัสทั้งสองสีเป็นสีเหลือง",),
                             topic=TOPIC_SALT, hint="หาก่อนว่าเกลือเป็นกรด เบส หรือกลาง แล้วนึกถึงสีของลิตมัส")
        others = [s[0] for s in SALTS if s[3] != nature]
        return _labelled(stem=f"สารละลายเกลือใด{LITMUS[nature]}", correct=salt, wrongs=tuple(others),
                         topic=TOPIC_SALT, hint="เกลือของกรดอ่อน+เบสแก่เป็นเบส เกลือของกรดแก่+เบสอ่อนเป็นกรด")
