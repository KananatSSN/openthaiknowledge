"""มวลอะตอม มวลโมเลกุล และมวลสูตร

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 3 ม.4/5

Sets moved here from: science_wave_f41.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f30 import ATOMIC, atoms, mass_of
from otk.sets._support.science_wave_f41 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_MASS = "มวลอะตอม มวลโมเลกุล และมวลสูตร"


ELEMENT_ISOTOPES = (
    ("Cl", (35, 37)), ("B", (10, 11)), ("Cu", (63, 65)), ("Li", (6, 7)), ("Br", (79, 81)), ("Ga", (69, 71)),
    ("Ag", (107, 109)), ("Rb", (85, 87)), ("Sb", (121, 123)), ("X", (20, 22)),
)


FORMULAS = ("H₂O", "CO₂", "NaCl", "CaCO₃", "H₂SO₄", "NH₃", "C₆H₁₂O₆", "Ca(OH)₂", "Al₂(SO₄)₃", "KNO₃", "MgCl₂",
            "Na₂CO₃", "CuSO₄", "Fe₂O₃", "C₂H₅OH", "Pb(NO₃)₂", "HNO₃", "NaHCO₃", "Mg(OH)₂", "CH₃COOH")


IONIC = {"NaCl", "CaCO₃", "Ca(OH)₂", "Al₂(SO₄)₃", "KNO₃", "MgCl₂", "Na₂CO₃", "CuSO₄", "Fe₂O₃", "Pb(NO₃)₂", "NaHCO₃",
         "Mg(OH)₂"}


@question_type(
    "chem.atomic_mass_foundation",
    display_name={"th": "ความหมายของมวลอะตอมสัมพัทธ์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MASS,
)
class AtomicMassFoundation(QuestionType):
    """Relative to one twelfth of a carbon-12 atom, so it has no unit."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        facts = (
            ("มวลอะตอมของธาตุเทียบกับมวลของอะไร", "1/12 ของมวลอะตอมคาร์บอน-12",
             ("มวลของอะตอมไฮโดรเจน 1 อะตอม", "มวลของโปรตอน 1 อนุภาค", "มวลของอะตอมออกซิเจน 1 อะตอม")),
            ("มวลอะตอมของธาตุที่แสดงในตารางธาตุมักเป็นเลขทศนิยมเพราะเหตุใด",
             "เป็นค่าเฉลี่ยของไอโซโทปตามปริมาณที่พบในธรรมชาติ",
             ("เครื่องชั่งมวลอะตอมยังชั่งได้ไม่แม่นยำพอ", "อะตอมมีอิเล็กตรอนเป็นเศษส่วนของอนุภาค", "นิวเคลียสมีโปรตอนไม่ครบจำนวนเต็มในบางอะตอม")),
            ("มวลอะตอมสัมพัทธ์มีหน่วยอย่างไร", "ไม่มีหน่วย เพราะเป็นอัตราส่วนเทียบกับมาตรฐาน",
             ("มีหน่วยเป็นกรัม เพราะชั่งได้ด้วยเครื่องชั่ง", "มีหน่วยเป็นกิโลกรัม เพราะเป็นมวลจริงของอะตอม",
              "มีหน่วยเป็นโมล เพราะนับจำนวนอะตอม")),
            ("ถ้าธาตุ X มีมวลอะตอม 24 หมายความว่าอย่างไร", "อะตอม X หนึ่งอะตอมมีมวลเป็น 24 เท่าของ 1/12 ของมวลคาร์บอน-12",
             ("อะตอม X หนึ่งอะตอมหนัก 24 กรัมพอดีเมื่อชั่งเทียบกับคาร์บอน-12", "อะตอม X มีโปรตอน 24 ตัวและนิวตรอน 24 ตัว", "ธาตุ X 1 โมลมีปริมาตร 24 dm³ ที่อุณหภูมิห้อง")),
        )
        if rng.random() < 0.5:
            stem, right, wrongs = rng.choice(facts)
            wrongs = tuple(wrongs)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_MASS,
                             hint="มวลอะตอมเป็นค่าเปรียบเทียบกับ 1/12 ของมวลคาร์บอน-12 จึงไม่มีหน่วย")
        formula = rng.choice(FORMULAS)
        kind = "มวลสูตร" if formula in IONIC else "มวลโมเลกุล"
        other = "มวลโมเลกุล" if kind == "มวลสูตร" else "มวลสูตร"
        return _labelled(stem=f"ค่ามวลของ {formula} ที่คำนวณจากผลรวมมวลอะตอมเรียกว่าอะไร",
                         correct=f"{kind} เพราะ{'เป็นสารประกอบไอออนิกที่ไม่มีโมเลกุลเดี่ยว' if kind == 'มวลสูตร' else 'เป็นสารโคเวเลนต์ที่มีโมเลกุล'}",
                         wrongs=(f"{other} เพราะ{'เป็นสารประกอบไอออนิกที่ไม่มีโมเลกุลเดี่ยว' if other == 'มวลสูตร' else 'เป็นสารโคเวเลนต์ที่มีโมเลกุล'}",
                                 "มวลอะตอม เพราะรวมจากอะตอมทุกตัวในสูตร", "มวลโมล เพราะมีหน่วยเป็นกรัมต่อโมล"),
                         topic=TOPIC_MASS, hint="สารโคเวเลนต์ใช้มวลโมเลกุล สารประกอบไอออนิกใช้มวลสูตร")


@question_type(
    "chem.atomic_mass_fluency",
    display_name={"th": "คำนวณมวลอะตอมเฉลี่ยจากไอโซโทป"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MASS,
)
class AtomicMassFluency(QuestionType):
    """Average = Σ(isotope mass × fraction found)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        element, (m1, m2) = rng.choice(ELEMENT_ISOTOPES)
        p1 = rng.randrange(5, 96)
        average = Fraction(m1 * p1 + m2 * (100 - p1), 100)
        if rng.random() < 0.6:
            return numeric(stem=f"ธาตุ {element} มีไอโซโทป {element}-{m1} ร้อยละ {p1} และ {element}-{m2} ร้อยละ {100 - p1} "
                                "มวลอะตอมเฉลี่ยเท่าใด (ใช้เลขมวลเป็นมวลของไอโซโทป)",
                           answer=average, wrongs=[Fraction(m1 + m2, 2), Fraction(m1 * (100 - p1) + m2 * p1, 100), m1 * p1 + m2 * (100 - p1)],
                           unit="", topic=TOPIC_MASS, hint="มวลอะตอมเฉลี่ย = Σ(มวลไอโซโทป × ร้อยละที่พบ) ÷ 100")
        return numeric(stem=f"ธาตุ {element} มีมวลอะตอมเฉลี่ย {show(average)} ประกอบด้วยไอโซโทป {element}-{m1} และ {element}-{m2} "
                            f"มี {element}-{m1} อยู่ร้อยละเท่าใด",
                       answer=p1, wrongs=[100 - p1, 50, p1 + 10 if p1 < 90 else p1 - 20], unit="%", topic=TOPIC_MASS,
                       hint="ให้ร้อยละของไอโซโทปแรกเป็น x: มวลเฉลี่ย = [m₁x + m₂(100 − x)] ÷ 100 แล้วแก้หา x")


@question_type(
    "chem.atomic_mass_application",
    display_name={"th": "คำนวณมวลโมเลกุลและมวลสูตร"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MASS,
)
class AtomicMassApplication(QuestionType):
    """Add each atom's mass as many times as the formula shows it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        formula = rng.choice(FORMULAS)
        mass = mass_of(formula)
        elements = [e for e, _ in atoms(formula)]
        given = ", ".join(f"{e} = {show(ATOMIC[e])}" for e in elements)
        naive = sum(ATOMIC[e] for e in elements)
        if rng.random() < 0.5:
            element, count = rng.choice(atoms(formula))
            part = ATOMIC[element] * count
            return numeric(stem=f"{formula} หนึ่งหน่วยสูตรมีมวลของธาตุ {element} รวมเท่าใด (มวลอะตอม {given})",
                           answer=part, wrongs=[ATOMIC[element] if count > 1 else part * 2, mass, part + ATOMIC[element]],
                           unit="", topic=TOPIC_MASS, hint="มวลของธาตุในสูตร = มวลอะตอม × จำนวนอะตอมของธาตุนั้นในสูตร")
        return numeric(stem=f"{formula} มี{'มวลสูตร' if formula in IONIC else 'มวลโมเลกุล'}เท่าใด (มวลอะตอม {given})",
                       answer=mass, wrongs=[naive if naive != mass else mass + 16, mass + 16, mass - 1], unit="",
                       topic=TOPIC_MASS, hint="คูณมวลอะตอมของแต่ละธาตุด้วยจำนวนอะตอมในสูตร (รวมตัวเลขนอกวงเล็บ) แล้วบวกกัน")
