"""ตัวรีดิวซ์ ตัวออกซิไดส์ และครึ่งปฏิกิริยา

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/25

Sets moved here from: science_wave_f38.
"""

from __future__ import annotations

import re
from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f38 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_AGENT = "ตัวรีดิวซ์ ตัวออกซิไดส์ และครึ่งปฏิกิริยา"


# (equation, reducing agent, oxidising agent, oxidation half, reduction half)
REDOX = (
    ("Zn + Cu²⁺ → Zn²⁺ + Cu", "Zn", "Cu²⁺", "Zn → Zn²⁺ + 2e⁻", "Cu²⁺ + 2e⁻ → Cu"),
    ("Mg + 2H⁺ → Mg²⁺ + H₂", "Mg", "H⁺", "Mg → Mg²⁺ + 2e⁻", "2H⁺ + 2e⁻ → H₂"),
    ("Fe + Cu²⁺ → Fe²⁺ + Cu", "Fe", "Cu²⁺", "Fe → Fe²⁺ + 2e⁻", "Cu²⁺ + 2e⁻ → Cu"),
    ("Cu + 2Ag⁺ → Cu²⁺ + 2Ag", "Cu", "Ag⁺", "Cu → Cu²⁺ + 2e⁻", "Ag⁺ + e⁻ → Ag"),
    ("Cl₂ + 2Br⁻ → 2Cl⁻ + Br₂", "Br⁻", "Cl₂", "2Br⁻ → Br₂ + 2e⁻", "Cl₂ + 2e⁻ → 2Cl⁻"),
    ("Cl₂ + 2I⁻ → 2Cl⁻ + I₂", "I⁻", "Cl₂", "2I⁻ → I₂ + 2e⁻", "Cl₂ + 2e⁻ → 2Cl⁻"),
    ("Br₂ + 2I⁻ → 2Br⁻ + I₂", "I⁻", "Br₂", "2I⁻ → I₂ + 2e⁻", "Br₂ + 2e⁻ → 2Br⁻"),
    ("2Fe³⁺ + 2I⁻ → 2Fe²⁺ + I₂", "I⁻", "Fe³⁺", "2I⁻ → I₂ + 2e⁻", "Fe³⁺ + e⁻ → Fe²⁺"),
    ("Zn + 2H⁺ → Zn²⁺ + H₂", "Zn", "H⁺", "Zn → Zn²⁺ + 2e⁻", "2H⁺ + 2e⁻ → H₂"),
    ("Mg + Zn²⁺ → Mg²⁺ + Zn", "Mg", "Zn²⁺", "Mg → Mg²⁺ + 2e⁻", "Zn²⁺ + 2e⁻ → Zn"),
    ("2Al + 3Cu²⁺ → 2Al³⁺ + 3Cu", "Al", "Cu²⁺", "Al → Al³⁺ + 3e⁻", "Cu²⁺ + 2e⁻ → Cu"),
    ("Sn²⁺ + 2Fe³⁺ → Sn⁴⁺ + 2Fe²⁺", "Sn²⁺", "Fe³⁺", "Sn²⁺ → Sn⁴⁺ + 2e⁻", "Fe³⁺ + e⁻ → Fe²⁺"),
    ("Fe + 2H⁺ → Fe²⁺ + H₂", "Fe", "H⁺", "Fe → Fe²⁺ + 2e⁻", "2H⁺ + 2e⁻ → H₂"),
    ("Zn + 2Ag⁺ → Zn²⁺ + 2Ag", "Zn", "Ag⁺", "Zn → Zn²⁺ + 2e⁻", "Ag⁺ + e⁻ → Ag"),
    ("Mg + Cu²⁺ → Mg²⁺ + Cu", "Mg", "Cu²⁺", "Mg → Mg²⁺ + 2e⁻", "Cu²⁺ + 2e⁻ → Cu"),
    ("Pb + Cu²⁺ → Pb²⁺ + Cu", "Pb", "Cu²⁺", "Pb → Pb²⁺ + 2e⁻", "Cu²⁺ + 2e⁻ → Cu"),
    ("Cl₂ + 2Fe²⁺ → 2Cl⁻ + 2Fe³⁺", "Fe²⁺", "Cl₂", "Fe²⁺ → Fe³⁺ + e⁻", "Cl₂ + 2e⁻ → 2Cl⁻"),
    ("2Al + 6H⁺ → 2Al³⁺ + 3H₂", "Al", "H⁺", "Al → Al³⁺ + 3e⁻", "2H⁺ + 2e⁻ → H₂"),
)


def coefficient(side: str, species: str) -> int:
    """How many of a species a side of an equation shows (the leading number)."""
    for part in side.split(" + "):
        match = re.fullmatch(r"(\d*)(.+)", part.strip())
        if match.group(2) == species:
            return int(match.group(1) or 1)
    raise ValueError((side, species))


def electrons_per_unit(ox_half: str, reducer: str) -> Fraction:
    left, right = ox_half.split(" → ")
    lost = int(re.search(r"(\d*)e⁻", right).group(1) or 1)
    return Fraction(lost, coefficient(left, reducer))


def products_of(equation: str) -> list[str]:
    return [re.sub(r"^\d+", "", x.strip()) for x in equation.split("→")[1].split("+") if x.strip()]


@question_type(
    "chem.redox_agent_foundation",
    display_name={"th": "ระบุตัวรีดิวซ์และตัวออกซิไดส์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_AGENT,
)
class RedoxAgentFoundation(QuestionType):
    """The reducing agent is oxidised; the oxidising agent is reduced."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq, reducer, oxidiser, _, _ = rng.choice(REDOX)
        want = rng.choice(("ตัวรีดิวซ์", "ตัวออกซิไดส์"))
        right = reducer if want == "ตัวรีดิวซ์" else oxidiser
        other = oxidiser if want == "ตัวรีดิวซ์" else reducer
        pool = [p for p in products_of(eq) if p not in (right, other)]
        return _labelled(stem=f"ในปฏิกิริยา {eq} สารใดเป็น{want}", correct=right, wrongs=(other, *pool[:2]),
                         topic=TOPIC_AGENT,
                         hint="ตัวรีดิวซ์ให้อิเล็กตรอน (ถูกออกซิไดส์ เลขออกซิเดชันเพิ่ม) ตัวออกซิไดส์รับอิเล็กตรอน (ถูกรีดิวซ์)")


@question_type(
    "chem.redox_agent_fluency",
    display_name={"th": "เขียนครึ่งปฏิกิริยาออกซิเดชันและรีดักชัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_AGENT,
)
class RedoxAgentFluency(QuestionType):
    """Electrons are lost in oxidation (right side) and gained in reduction (left side)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq, _, _, ox, red = rng.choice(REDOX)
        want = rng.choice(("ออกซิเดชัน", "รีดักชัน"))
        right = ox if want == "ออกซิเดชัน" else red
        other = red if want == "ออกซิเดชัน" else ox

        def flip(half: str) -> str:
            left, right_side = half.split(" → ")
            return f"{right_side} → {left}"

        return _labelled(stem=f"ครึ่งปฏิกิริยา{want}ของ {eq} คือข้อใด", correct=right,
                         wrongs=(other, flip(right), flip(other)), topic=TOPIC_AGENT,
                         hint="ออกซิเดชัน: อิเล็กตรอนอยู่ทางขวา (เสีย e⁻) รีดักชัน: อิเล็กตรอนอยู่ทางซ้าย (รับ e⁻)")


@question_type(
    "chem.redox_agent_application",
    display_name={"th": "จำนวนอิเล็กตรอนที่ถ่ายโอนในปฏิกิริยารีดอกซ์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_AGENT,
)
class RedoxAgentApplication(QuestionType):
    """Balance electrons between the halves; moles of electrons follow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq, reducer, _, ox, red = rng.choice(REDOX)
        per_unit = electrons_per_unit(ox, reducer)
        per_reaction = per_unit * coefficient(eq.split(" → ")[0], reducer)
        if rng.random() < 0.5:
            return numeric(stem=f"ในปฏิกิริยา {eq} ตามสมการ มีการถ่ายโอนอิเล็กตรอนทั้งหมดกี่โมล", answer=per_reaction,
                           wrongs=[per_unit if per_unit != per_reaction else per_reaction + 1, per_reaction * 2, per_reaction + 1],
                           unit="โมล", topic=TOPIC_AGENT,
                           hint="ดูครึ่งปฏิกิริยาออกซิเดชันแล้วคูณด้วยสัมประสิทธิ์ของตัวรีดิวซ์ในสมการ")
        moles = rng.choice((Fraction(1, 2), 1, Fraction(3, 2), 2, 3))
        return numeric(stem=f"ในปฏิกิริยา {eq} ถ้า {reducer} ทำปฏิกิริยา {moles} โมล จะให้อิเล็กตรอนกี่โมล",
                       answer=moles * per_unit, wrongs=[moles * per_unit * 2, moles + per_unit, moles * 3 if per_unit != 3 else moles * 2],
                       unit="โมล", topic=TOPIC_AGENT,
                       hint="โมลอิเล็กตรอน = โมลตัวรีดิวซ์ × จำนวนอิเล็กตรอนที่เสียต่อหนึ่งหน่วยในครึ่งปฏิกิริยา")
