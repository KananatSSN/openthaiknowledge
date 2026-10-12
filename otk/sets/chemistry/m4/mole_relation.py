"""ความสัมพันธ์ของโมล จำนวนอนุภาค มวล และปริมาตรแก๊ส

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 3 ม.4/6

Sets moved here from: science_wave_f42.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f30 import STP, atoms, mass_of
from otk.sets._support.science_wave_f36 import SUP, sci
from otk.sets._support.science_wave_f42 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_MOLE = "ความสัมพันธ์ของโมล จำนวนอนุภาค มวล และปริมาตรแก๊ส"


AVOGADRO = Fraction(602, 100)  # × 10²³


SUBSTANCES = ("H₂O", "CO₂", "O₂", "N₂", "CH₄", "NH₃", "NaCl", "CaCO₃", "H₂SO₄", "C₆H₁₂O₆", "HCl", "SO₂", "Mg", "Fe",
              "C", "Na₂CO₃", "C₂H₅OH")


GASES = ("CO₂", "O₂", "N₂", "CH₄", "NH₃", "HCl", "SO₂", "H₂")


def particles_text(moles: Fraction, per: int = 1) -> tuple[str, Fraction, int]:
    mantissa, power = sci(moles * per * AVOGADRO)
    return f"{show(mantissa)} × 10{str(power + 23).translate(SUP)}", mantissa, power + 23


@question_type(
    "chem.mole_relation_foundation",
    display_name={"th": "จำนวนอนุภาคจากจำนวนโมล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MOLE,
)
class MoleRelationFoundation(QuestionType):
    """1 mol = 6.02 × 10²³ particles; a molecule of H₂O carries 3 atoms."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            substance = rng.choice(SUBSTANCES)
            moles = Fraction(rng.randrange(1, 41), rng.choice((1, 2, 4, 10)))
            count_atoms = rng.random() < 0.4 and sum(n for _, n in atoms(substance)) > 1
            per = sum(n for _, n in atoms(substance)) if count_atoms else 1
            text, mantissa, power = particles_text(moles, per)
            return (substance, moles, count_atoms, per, text, mantissa, power) if exact(mantissa) else None

        substance, moles, count_atoms, per, text, mantissa, power = _find(rng, draw)
        what = "อะตอมทั้งหมด" if count_atoms else ("อะตอม" if len(atoms(substance)) == 1 and atoms(substance)[0][1] == 1
                                                     else "โมเลกุลหรือหน่วยสูตร")
        return numeric(stem=f"{substance} {show(moles)} โมล มี{what}กี่อนุภาค ตอบในรูป a × 10{str(power).translate(SUP)} "
                            "ค่า a เท่าใด (1 โมล = 6.02 × 10²³ อนุภาค)",
                       answer=mantissa, wrongs=[sci(moles * AVOGADRO)[0] if per > 1 else mantissa * 2 if mantissa * 2 < 10 else mantissa / 2,
                                                AVOGADRO, mantissa + 1 if mantissa + 1 < 10 else mantissa - 1],
                       unit="", topic=TOPIC_MOLE,
                       hint="จำนวนอนุภาค = โมล × 6.02 × 10²³ ถ้าถามจำนวนอะตอม ให้คูณจำนวนอะตอมในหนึ่งโมเลกุลด้วย")


@question_type(
    "chem.mole_relation_fluency",
    display_name={"th": "เปลี่ยนมวลเป็นโมลและจำนวนอนุภาค"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MOLE,
)
class MoleRelationFluency(QuestionType):
    """mol = mass ÷ molar mass; mass = mol × molar mass."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            substance = rng.choice(SUBSTANCES)
            moles = Fraction(rng.randrange(1, 41), rng.choice((1, 2, 4, 10)))
            grams = moles * mass_of(substance)
            return (substance, moles, grams) if exact(grams) and exact(moles) else None

        substance, moles, grams = _find(rng, draw)
        m = mass_of(substance)
        if rng.random() < 0.5:
            return numeric(stem=f"{substance} {show(grams)} กรัม มีกี่โมล (มวลต่อโมล = {show(m)} g/mol)", answer=moles,
                           wrongs=[grams * m if exact(grams * m) else moles * 2, moles * 2, grams], unit="โมล",
                           topic=TOPIC_MOLE, hint="โมล = มวล (g) ÷ มวลต่อโมล (g/mol)")
        return numeric(stem=f"{substance} {show(moles)} โมล มีมวลกี่กรัม (มวลต่อโมล = {show(m)} g/mol)", answer=grams,
                       wrongs=[m / moles if exact(m / moles) else grams * 2, grams * 2, m], unit="กรัม", topic=TOPIC_MOLE,
                       hint="มวล = โมล × มวลต่อโมล")


@question_type(
    "chem.mole_relation_application",
    display_name={"th": "ความสัมพันธ์ของมวล ปริมาตรแก๊สที่ STP และจำนวนโมเลกุล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MOLE,
)
class MoleRelationApplication(QuestionType):
    """Everything goes through moles."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            gas = rng.choice(GASES)
            moles = Fraction(rng.randrange(1, 41), rng.choice((2, 4, 10)))
            grams, volume = moles * mass_of(gas), moles * STP
            text, mantissa, power = particles_text(moles)
            ok = all(exact(x) for x in (grams, volume, mantissa))
            return (gas, moles, grams, volume, text, mantissa, power) if ok else None

        gas, moles, grams, volume, text, mantissa, power = _find(rng, draw)
        m = mass_of(gas)
        kind = rng.randrange(3)
        if kind == 0:
            return numeric(stem=f"แก๊ส {gas} {show(grams)} กรัม มีปริมาตรกี่ dm³ ที่ STP (มวลต่อโมล {show(m)})", answer=volume,
                           wrongs=[grams * STP, volume * 2, STP], unit="dm³", topic=TOPIC_MOLE,
                           hint="มวล → โมล (÷ มวลต่อโมล) → ปริมาตร (× 22.4 dm³ ที่ STP)")
        if kind == 1:
            return numeric(stem=f"แก๊ส {gas} ปริมาตร {show(volume)} dm³ ที่ STP มีมวลกี่กรัม (มวลต่อโมล {show(m)})", answer=grams,
                           wrongs=[volume * m, grams * 2, m], unit="กรัม", topic=TOPIC_MOLE,
                           hint="ปริมาตร → โมล (÷ 22.4) → มวล (× มวลต่อโมล)")
        return numeric(stem=f"แก๊ส {gas} ปริมาตร {show(volume)} dm³ ที่ STP มีกี่โมเลกุล ตอบในรูป a × 10{str(power).translate(SUP)} ค่า a เท่าใด",
                       answer=mantissa, wrongs=[AVOGADRO, mantissa * 2 if mantissa * 2 < 10 else mantissa / 2,
                                                mantissa + 1 if mantissa + 1 < 10 else mantissa - 1],
                       unit="", topic=TOPIC_MOLE, hint="ปริมาตร → โมล (÷ 22.4) → จำนวนโมเลกุล (× 6.02 × 10²³)")
