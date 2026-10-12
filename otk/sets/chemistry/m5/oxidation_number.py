"""เลขออกซิเดชันและปฏิกิริยารีดอกซ์

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/24

Sets moved here from: science_wave_f38.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f38 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_ON = "เลขออกซิเดชันและปฏิกิริยารีดอกซ์"


# (formula, element asked, oxidation number)
SPECIES = (
    ("KMnO₄", "Mn", 7), ("MnO₂", "Mn", 4), ("MnO₄⁻", "Mn", 7), ("K₂Cr₂O₇", "Cr", 6), ("Cr₂O₇²⁻", "Cr", 6),
    ("CrO₄²⁻", "Cr", 6), ("H₂SO₄", "S", 6), ("SO₂", "S", 4), ("SO₃²⁻", "S", 4), ("S₂O₃²⁻", "S", 2),
    ("Na₂S", "S", -2), ("HNO₃", "N", 5), ("NO₂", "N", 4), ("NO", "N", 2), ("NH₃", "N", -3), ("NH₄⁺", "N", -3),
    ("N₂O", "N", 1), ("NO₃⁻", "N", 5), ("KClO₃", "Cl", 5), ("HClO", "Cl", 1), ("ClO₄⁻", "Cl", 7),
    ("Fe₂O₃", "Fe", 3), ("FeO", "Fe", 2), ("Fe₃O₄", "Fe", Fraction(8, 3)), ("CO₂", "C", 4), ("CH₄", "C", -4),
    ("C₂O₄²⁻", "C", 3), ("PO₄³⁻", "P", 5), ("H₃PO₄", "P", 5), ("H₂O₂", "O", -1), ("NaH", "H", -1),
    ("CuO", "Cu", 2), ("Cu₂O", "Cu", 1), ("SnCl₄", "Sn", 4), ("VO₂⁺", "V", 5),
)


def signed(x) -> str:
    x = Fraction(x)
    if x.denominator != 1:
        return f"{'+' if x > 0 else '−'}{abs(x.numerator)}/{x.denominator}"
    return f"{int(x):+d}".replace("-", "−") if x else "0"


# (equation, redox?, element that changes and its before/after oxidation numbers or None)
REACTIONS = (
    ("Zn + CuSO₄ → ZnSO₄ + Cu", True), ("Mg + 2HCl → MgCl₂ + H₂", True), ("2Na + Cl₂ → 2NaCl", True),
    ("CH₄ + 2O₂ → CO₂ + 2H₂O", True), ("Cl₂ + 2KBr → 2KCl + Br₂", True), ("2H₂O₂ → 2H₂O + O₂", True),
    ("Fe₂O₃ + 3CO → 2Fe + 3CO₂", True), ("Cu + 2AgNO₃ → Cu(NO₃)₂ + 2Ag", True),
    ("NaOH + HCl → NaCl + H₂O", False), ("AgNO₃ + NaCl → AgCl + NaNO₃", False),
    ("CaCO₃ → CaO + CO₂", False), ("BaCl₂ + Na₂SO₄ → BaSO₄ + 2NaCl", False),
    ("NH₃ + HCl → NH₄Cl", False), ("CO₂ + H₂O → H₂CO₃", False),
)


@question_type(
    "chem.oxidation_number_foundation",
    display_name={"th": "หาเลขออกซิเดชันของธาตุในสารประกอบและไอออน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ON,
)
class OxidationNumberFoundation(QuestionType):
    """O is −2, H +1, group 1 +1, group 2 +2; the rest balances to the charge."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        formula, element, value = rng.choice([s for s in SPECIES if Fraction(s[2]).denominator == 1])
        pool = [v for v in (value + 1, value - 1, -value, value + 2, value - 2) if v != value]
        picks = []
        for v in pool:
            if signed(v) not in picks:
                picks.append(signed(v))
        return _labelled(stem=f"เลขออกซิเดชันของ {element} ใน {formula} เท่ากับเท่าใด", correct=signed(value),
                         wrongs=tuple(picks), topic=TOPIC_ON,
                         hint="ผลรวมเลขออกซิเดชันทุกอะตอม = ประจุของสาร (O = −2, H = +1, โลหะหมู่ 1 = +1, หมู่ 2 = +2)")


@question_type(
    "chem.oxidation_number_fluency",
    display_name={"th": "การเปลี่ยนแปลงเลขออกซิเดชันในปฏิกิริยา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ON,
)
class OxidationNumberFluency(QuestionType):
    """Compare the oxidation number of one element on both sides."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        changes = (
            ("MnO₄⁻ → Mn²⁺", "Mn", 7, 2), ("Cr₂O₇²⁻ → Cr³⁺", "Cr", 6, 3), ("SO₂ → SO₄²⁻", "S", 4, 6),
            ("NO₃⁻ → NO", "N", 5, 2), ("NO₃⁻ → NO₂", "N", 5, 4), ("Fe²⁺ → Fe³⁺", "Fe", 2, 3),
            ("I⁻ → I₂", "I", -1, 0), ("Cl₂ → Cl⁻", "Cl", 0, -1), ("H₂O₂ → O₂", "O", -1, 0),
            ("H₂O₂ → H₂O", "O", -1, -2), ("NH₃ → NO", "N", -3, 2), ("S₂O₃²⁻ → S₄O₆²⁻", "S", 2, Fraction(5, 2)),
            ("MnO₂ → Mn²⁺", "Mn", 4, 2), ("Sn²⁺ → Sn⁴⁺", "Sn", 2, 4), ("C₂O₄²⁻ → CO₂", "C", 3, 4),
        )
        change, element, before, after = rng.choice(changes)
        numeric_ok = (Fraction(after) - Fraction(before)).denominator == 1
        if rng.random() < 0.5 or not numeric_ok:
            right = "เพิ่มขึ้น จึงเกิดออกซิเดชัน" if after > before else "ลดลง จึงเกิดรีดักชัน"
            return _labelled(stem=f"ในการเปลี่ยนแปลง {change} เลขออกซิเดชันของ {element} เปลี่ยนอย่างไร", correct=right,
                             wrongs=tuple(x for x in ("เพิ่มขึ้น จึงเกิดออกซิเดชัน", "ลดลง จึงเกิดรีดักชัน",
                                                      "เพิ่มขึ้น จึงเกิดรีดักชัน", "ลดลง จึงเกิดออกซิเดชัน") if x != right),
                             topic=TOPIC_ON, hint="เลขออกซิเดชันเพิ่ม = เสียอิเล็กตรอน = ออกซิเดชัน ลดลง = รับอิเล็กตรอน = รีดักชัน")
        diff = abs(Fraction(after) - Fraction(before))
        return numeric(stem=f"ในการเปลี่ยนแปลง {change} เลขออกซิเดชันของ {element} เปลี่ยนไปกี่หน่วย", answer=diff,
                       wrongs=[abs(before) + abs(after) if abs(before) + abs(after) != diff else diff + 1, diff + 1,
                               abs(after) if abs(after) != diff else diff * 2],
                       unit="หน่วย", topic=TOPIC_ON, hint="หาเลขออกซิเดชันก่อนและหลัง แล้วหาผลต่าง")


@question_type(
    "chem.oxidation_number_application",
    display_name={"th": "ระบุปฏิกิริยารีดอกซ์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ON,
)
class OxidationNumberApplication(QuestionType):
    """Redox means some element's oxidation number changes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        want = rng.random() < 0.5
        match = [r[0] for r in REACTIONS if r[1] == want]
        other = [r[0] for r in REACTIONS if r[1] != want]
        return _labelled(stem=f"ปฏิกิริยาใด{'เป็น' if want else 'ไม่เป็น'}ปฏิกิริยารีดอกซ์", correct=rng.choice(match),
                         wrongs=tuple(other), topic=TOPIC_ON,
                         hint="ตรวจว่ามีธาตุใดเลขออกซิเดชันเปลี่ยนหรือไม่ ธาตุอิสระที่กลายเป็นสารประกอบ (หรือกลับกัน) บอกว่าเป็นรีดอกซ์")
