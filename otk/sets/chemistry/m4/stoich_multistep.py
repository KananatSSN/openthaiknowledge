"""การคำนวณปริมาณสารในปฏิกิริยาเคมีหลายขั้นตอน

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.4/5

Sets moved here from: science_wave_f31.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f30 import STP, equation_text, mass_of, species
from otk.sets._support.science_wave_f31 import QUARTERS, SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_MULTI = "การคำนวณปริมาณสารในปฏิกิริยาเคมีหลายขั้นตอน"


def coef(eq, formula: str) -> int:
    return next(c for c, f, _ in species(eq) if f == formula)


# Each chain: the reactions in order; each passes one product on as the next reactant.
CHAINS = (
    ("CaCO₃", "Ca(OH)₂", (
        (((1, "CaCO₃", "s"),), ((1, "CaO", "s"), (1, "CO₂", "g"))),
        (((1, "CaO", "s"), (1, "H₂O", "l")), ((1, "Ca(OH)₂", "aq"),)),
    ), ("CaO",)),
    ("KClO₃", "MgO", (
        (((2, "KClO₃", "s"),), ((2, "KCl", "s"), (3, "O₂", "g"))),
        (((2, "Mg", "s"), (1, "O₂", "g")), ((2, "MgO", "s"),)),
    ), ("O₂",)),
    ("Zn", "Cu", (
        (((1, "Zn", "s"), (2, "HCl", "aq")), ((1, "ZnCl₂", "aq"), (1, "H₂", "g"))),
        (((1, "CuO", "s"), (1, "H₂", "g")), ((1, "Cu", "s"), (1, "H₂O", "l"))),
    ), ("H₂",)),
    ("N₂", "NH₄Cl", (
        (((1, "N₂", "g"), (3, "H₂", "g")), ((2, "NH₃", "g"),)),
        (((1, "NH₃", "g"), (1, "HCl", "g")), ((1, "NH₄Cl", "s"),)),
    ), ("NH₃",)),
    ("S", "H₂SO₄", (
        (((1, "S", "s"), (1, "O₂", "g")), ((1, "SO₂", "g"),)),
        (((2, "SO₂", "g"), (1, "O₂", "g")), ((2, "SO₃", "g"),)),
        (((1, "SO₃", "g"), (1, "H₂O", "l")), ((1, "H₂SO₄", "aq"),)),
    ), ("SO₂", "SO₃")),
    ("CH₄", "CaCO₃", (
        (((1, "CH₄", "g"), (2, "O₂", "g")), ((1, "CO₂", "g"), (2, "H₂O", "l"))),
        (((1, "CO₂", "g"), (1, "Ca(OH)₂", "aq")), ((1, "CaCO₃", "s"), (1, "H₂O", "l"))),
    ), ("CO₂",)),
    ("Na", "AgCl", (
        (((2, "Na", "s"), (1, "Cl₂", "g")), ((2, "NaCl", "s"),)),
        (((1, "NaCl", "aq"), (1, "AgNO₃", "aq")), ((1, "AgCl", "s"), (1, "NaNO₃", "aq"))),
    ), ("NaCl",)),
    ("Al", "Al₂O₃", (
        (((2, "Al", "s"), (6, "HCl", "aq")), ((2, "AlCl₃", "aq"), (3, "H₂", "g"))),
        (((1, "AlCl₃", "aq"), (3, "NaOH", "aq")), ((1, "Al(OH)₃", "s"), (3, "NaCl", "aq"))),
        (((2, "Al(OH)₃", "s"),), ((1, "Al₂O₃", "s"), (3, "H₂O", "g"))),
    ), ("AlCl₃", "Al(OH)₃")),
)


def chain_ratio(chain) -> Fraction:
    """Moles of the last product per mole of the first reactant."""
    start, end, eqs, links = chain
    ratio = Fraction(1)
    carried = start
    for eq, nxt in zip(eqs, (*links, end)):
        ratio *= Fraction(coef(eq, nxt), coef(eq, carried))
        carried = nxt
    return ratio


def chain_text(chain) -> str:
    return " และ ".join(equation_text(eq) for eq in chain[2])


@question_type(
    "chem.stoich_multistep_foundation",
    display_name={"th": "อัตราส่วนโมลผ่านปฏิกิริยาหลายขั้นตอน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MULTI,
)
class StoichMultistepFoundation(QuestionType):
    """Multiply the mole ratios of each step through the shared substance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            chain = rng.choice(CHAINS)
            n = rng.choice(QUARTERS)
            out = n * chain_ratio(chain)
            return (chain, n, out) if exact(out) else None

        chain, n, out = _find(rng, draw)
        start, end = chain[0], chain[1]
        ratio = chain_ratio(chain)
        return numeric(stem=f"จากปฏิกิริยาต่อเนื่อง {chain_text(chain)} ถ้าเริ่มจาก {start} {show(n)} โมล "
                            f"(ผลิตภัณฑ์แต่ละขั้นใช้ในขั้นต่อไปทั้งหมด) จะได้ {end} กี่โมล",
                       answer=out, wrongs=[n, n / ratio if exact(n / ratio) else n * 2, out * 2 if out != n else n + 1],
                       unit="โมล", topic=TOPIC_MULTI,
                       hint="หาอัตราส่วนโมลทีละขั้นผ่านสารที่ส่งต่อ แล้วคูณอัตราส่วนทุกขั้นเข้าด้วยกัน")


@question_type(
    "chem.stoich_multistep_fluency",
    display_name={"th": "มวลของผลิตภัณฑ์สุดท้ายจากปฏิกิริยาหลายขั้นตอน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MULTI,
)
class StoichMultistepFluency(QuestionType):
    """grams of the start → moles → through every step → grams of the end."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            chain = rng.choice(CHAINS)
            n = rng.choice(QUARTERS)
            m_start, m_end = n * mass_of(chain[0]), n * chain_ratio(chain) * mass_of(chain[1])
            return (chain, m_start, m_end) if exact(m_start) and exact(m_end) else None

        chain, m_start, m_end = _find(rng, draw)
        start, end = chain[0], chain[1]
        forward = rng.random() < 0.5
        masses = f"(มวลต่อโมล {start} = {show(mass_of(start))}, {end} = {show(mass_of(end))})"
        hint = "มวล → โมล แล้วใช้อัตราส่วนโมลทีละขั้น (หรืออัตราส่วนรวม) แล้วโมล → มวล"
        if forward:
            return numeric(stem=f"จากปฏิกิริยาต่อเนื่อง {chain_text(chain)} เริ่มจาก {start} {show(m_start)} กรัม "
                                f"จะได้ {end} กี่กรัม {masses}",
                           answer=m_end, wrongs=[m_start, m_start / mass_of(start) * mass_of(end), m_end * 2],
                           unit="กรัม", topic=TOPIC_MULTI, hint=hint)
        return numeric(stem=f"จากปฏิกิริยาต่อเนื่อง {chain_text(chain)} ต้องการ {end} {show(m_end)} กรัม "
                            f"ต้องเริ่มจาก {start} กี่กรัม {masses}",
                       answer=m_start, wrongs=[m_end, m_end / mass_of(end) * mass_of(start), m_start * 2],
                       unit="กรัม", topic=TOPIC_MULTI, hint=hint)


@question_type(
    "chem.stoich_multistep_application",
    display_name={"th": "ปริมาตรแก๊สและปริมาณสารกลางในปฏิกิริยาหลายขั้นตอน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MULTI,
)
class StoichMultistepApplication(QuestionType):
    """The substance passed between steps, counted as a mass or as a gas at STP."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            chain = rng.choice(CHAINS)
            eq1 = chain[2][0]
            link = chain[3][0]
            n = rng.choice(QUARTERS)
            n_link = n * Fraction(coef(eq1, link), coef(eq1, chain[0]))
            gas = next(st for c, f, st in eq1[1] if f == link) == "g"
            amount = n_link * (STP if gas else mass_of(link))
            m_start = n * mass_of(chain[0])
            return (chain, link, gas, m_start, amount) if exact(amount) and exact(m_start) else None

        chain, link, gas, m_start, amount = _find(rng, draw)
        unit = "dm³ ที่ STP" if gas else "กรัม"
        per = "22.4 dm³/mol ที่ STP" if gas else f"มวลต่อโมล {link} = {show(mass_of(link))}"
        return numeric(stem=f"จากปฏิกิริยาต่อเนื่อง {chain_text(chain)} เริ่มจาก {chain[0]} {show(m_start)} กรัม "
                            f"(มวลต่อโมล {show(mass_of(chain[0]))}) ในขั้นแรกจะได้ {link} ที่ส่งต่อไปขั้นถัดไปกี่ {unit} ({per})",
                       answer=amount, wrongs=[amount * 2, m_start, amount / 2 if exact(amount / 2) else amount + 1],
                       unit=unit.split()[0], topic=TOPIC_MULTI,
                       hint="ใช้เฉพาะสมการขั้นแรก: โมลสารเริ่มต้น × อัตราส่วนในสมการ = โมลสารที่ส่งต่อ")
