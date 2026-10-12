"""ความยาวพันธะ พลังงานพันธะ และพลังงานของปฏิกิริยา

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/16

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


TOPIC_ENERGY = "ความยาวพันธะ พลังงานพันธะ และพลังงานของปฏิกิริยา"


BOND_ENERGY = {"H–H": 436, "Cl–Cl": 243, "H–Cl": 432, "C–H": 414, "O=O": 498, "C=O": 803, "O–H": 464, "N≡N": 946,
               "N–H": 391, "C–C": 346, "C=C": 614, "C≡C": 839, "Br–Br": 193, "H–Br": 366, "F–F": 158, "H–F": 568,
               "C–Cl": 330, "I–I": 151, "H–I": 299}


# (equation, bonds broken, bonds formed)
REACTIONS = (
    ("H₂ + Cl₂ → 2HCl", {"H–H": 1, "Cl–Cl": 1}, {"H–Cl": 2}),
    ("H₂ + Br₂ → 2HBr", {"H–H": 1, "Br–Br": 1}, {"H–Br": 2}),
    ("H₂ + F₂ → 2HF", {"H–H": 1, "F–F": 1}, {"H–F": 2}),
    ("H₂ + I₂ → 2HI", {"H–H": 1, "I–I": 1}, {"H–I": 2}),
    ("N₂ + 3H₂ → 2NH₃", {"N≡N": 1, "H–H": 3}, {"N–H": 6}),
    ("CH₄ + 2O₂ → CO₂ + 2H₂O", {"C–H": 4, "O=O": 2}, {"C=O": 2, "O–H": 4}),
    ("2H₂ + O₂ → 2H₂O", {"H–H": 2, "O=O": 1}, {"O–H": 4}),
    ("C₂H₄ + H₂ → C₂H₆", {"C=C": 1, "H–H": 1}, {"C–C": 1, "C–H": 2}),
    ("CH₄ + Cl₂ → CH₃Cl + HCl", {"C–H": 1, "Cl–Cl": 1}, {"C–Cl": 1, "H–Cl": 1}),
    ("C₂H₂ + 2H₂ → C₂H₆", {"C≡C": 1, "H–H": 2}, {"C–C": 1, "C–H": 4}),
)


LENGTH_FACTS = (
    ("พันธะใดสั้นที่สุด", "C≡C", ("C=C", "C–C", "ยาวเท่ากันทั้งหมด")),
    ("พันธะใดแข็งแรงที่สุด (พลังงานพันธะมากที่สุด)", "N≡N", ("N=N", "N–N", "แข็งแรงเท่ากันทั้งหมด")),
    ("เมื่อจำนวนพันธะระหว่างอะตอมคู่เดียวกันเพิ่มขึ้น ความยาวพันธะและพลังงานพันธะเป็นอย่างไร", "ความยาวลดลง พลังงานพันธะเพิ่มขึ้น",
     ("ความยาวเพิ่มขึ้น พลังงานพันธะเพิ่มขึ้น", "ความยาวลดลง พลังงานพันธะลดลง", "ไม่เปลี่ยนทั้งสองอย่าง")),
    ("การสลายพันธะเป็นกระบวนการแบบใด", "ดูดพลังงาน", ("คายพลังงาน", "ไม่เกี่ยวกับพลังงาน", "ขึ้นกับชนิดของพันธะ")),
    ("การสร้างพันธะเป็นกระบวนการแบบใด", "คายพลังงาน", ("ดูดพลังงาน", "ไม่เกี่ยวกับพลังงาน", "ขึ้นกับชนิดของพันธะ")),
    ("พันธะ H–X ใดยาวที่สุด", "H–I", ("H–Br", "H–Cl", "H–F")),
)


def _energy(bonds: dict[str, int]) -> int:
    return sum(BOND_ENERGY[b] * n for b, n in bonds.items())


def _bond_list(bonds: dict[str, int]) -> str:
    return " ".join(f"{b} = {BOND_ENERGY[b]}" for b in bonds)


@question_type(
    "chem.bond_energy_foundation",
    display_name={"th": "ความยาวพันธะและพลังงานพันธะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ENERGY,
)
class BondEnergyFoundation(QuestionType):
    """More shared pairs make a bond shorter and stronger; breaking costs energy."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(LENGTH_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_ENERGY,
                             hint="พันธะสามสั้นและแข็งแรงกว่าพันธะคู่และพันธะเดี่ยว อะตอมใหญ่ทำให้พันธะยาวขึ้น")
        bonds = rng.sample(sorted(BOND_ENERGY), 3)
        strongest = rng.random() < 0.5
        pick = (max if strongest else min)(bonds, key=BOND_ENERGY.get)
        return _labelled(stem=f"จากพลังงานพันธะ ({', '.join(f'{b} {BOND_ENERGY[b]} kJ/mol' for b in bonds)}) พันธะใด{'แข็งแรงที่สุด' if strongest else 'สลายได้ง่ายที่สุด'}",
                         correct=pick, wrongs=tuple(b for b in bonds if b != pick) + ("เท่ากันทั้งหมด",),
                         topic=TOPIC_ENERGY, hint="พลังงานพันธะมาก พันธะแข็งแรง ต้องใช้พลังงานมากในการสลาย")


@question_type(
    "chem.bond_energy_fluency",
    display_name={"th": "คำนวณพลังงานของปฏิกิริยาจากพลังงานพันธะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ENERGY,
)
class BondEnergyFluency(QuestionType):
    """ΔH = energy to break bonds − energy released forming bonds, scaled by the amount."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq, broken, formed = rng.choice(REACTIONS)
        moles = rng.choice((1, 1, 2, 3, 4, 5))
        dh = (_energy(broken) - _energy(formed)) * moles
        amount = "ตามสมการ" if moles == 1 else f"เมื่อเกิดปฏิกิริยา {moles} เท่าของสมการ"
        return numeric(
            stem=f"ปฏิกิริยา {eq} {amount} มีพลังงานของปฏิกิริยาเท่าใด (พลังงานพันธะ kJ/mol: {_bond_list({**broken, **formed})})",
            answer=dh, wrongs=[-dh, (_energy(broken) + _energy(formed)) * moles, dh // moles if moles > 1 else dh * 2],
            unit="kJ", topic=TOPIC_ENERGY, allow_negative=True,
            hint="ΔH = ผลรวมพลังงานพันธะที่สลาย − ผลรวมพลังงานพันธะที่สร้าง (ค่าลบคือคายพลังงาน)")


@question_type(
    "chem.bond_energy_application",
    display_name={"th": "หาพลังงานพันธะที่ไม่ทราบค่าจากพลังงานของปฏิกิริยา"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ENERGY,
)
class BondEnergyApplication(QuestionType):
    """Work the bond-energy sum backwards for the one bond left out."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq, broken, formed = rng.choice(REACTIONS)
        dh = _energy(broken) - _energy(formed)
        side, bonds = rng.choice((("broken", broken), ("formed", formed)))
        hidden = rng.choice(sorted(bonds))
        known = {b: e for b, e in BOND_ENERGY.items() if b in {**broken, **formed} and b != hidden}
        listed = ", ".join(f"{b} = {e}" for b, e in known.items())
        if rng.random() < 0.5:
            return numeric(
                stem=f"ปฏิกิริยา {eq} มีพลังงานของปฏิกิริยา {dh:+d} kJ ถ้าพลังงานพันธะ {listed} kJ/mol พลังงานพันธะ {hidden} เท่าใด",
                answer=BOND_ENERGY[hidden], wrongs=[BOND_ENERGY[hidden] + abs(dh), abs(BOND_ENERGY[hidden] - abs(dh)) or 100,
                                                    BOND_ENERGY[hidden] * 2],
                unit="kJ/mol", topic=TOPIC_ENERGY,
                hint="ΔH = Σพันธะที่สลาย − Σพันธะที่สร้าง แทนค่าที่รู้แล้วแก้หาพลังงานพันธะที่ไม่รู้ (อย่าลืมจำนวนพันธะ)")
        return _labelled(
            stem=f"ปฏิกิริยา {eq} (พลังงานพันธะ kJ/mol: {_bond_list({**broken, **formed})}) เป็นปฏิกิริยาแบบใด",
            correct="คายพลังงาน" if dh < 0 else "ดูดพลังงาน",
            wrongs=("ดูดพลังงาน" if dh < 0 else "คายพลังงาน", "ไม่มีการเปลี่ยนแปลงพลังงาน", "บอกไม่ได้"),
            topic=TOPIC_ENERGY, hint="ถ้าพลังงานที่ได้จากการสร้างพันธะมากกว่าพลังงานที่ใช้สลายพันธะ ปฏิกิริยาคายพลังงาน")
