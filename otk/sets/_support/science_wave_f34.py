"""Wave F slice 34 — เคมีเพิ่มเติม 2: the equilibrium constant, equilibrium
concentrations, multi-step equilibria, and Le Chatelier's principle.

Four ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 2 ม.5/9`` — writing and calculating K;
* ``เคมีเพิ่มเติม 2 ม.5/10`` — concentrations at equilibrium;
* ``เคมีเพิ่มเติม 2 ม.5/11`` — K for reversed, scaled and combined reactions;
* ``เคมีเพิ่มเติม 2 ม.5/12`` — how a disturbed equilibrium shifts, and what
  changes K.

Solids and pure liquids stay out of K. Every draw is kept only when K and the
answer are exact to two places; square roots are asked only of perfect
squares.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.kit.answer_choices import show
from otk.sets._support.science_wave_f24 import _find, exact

SUBJECT = "เคมี"
UPPER_FIVE = {"th": "ม.5"}

# (equation, reactants, products): each species (formula, coefficient, phase)
K_SYSTEMS = (
    ("H₂(g) + I₂(g) ⇌ 2HI(g)", (("H₂", 1, "g"), ("I₂", 1, "g")), (("HI", 2, "g"),)),
    ("N₂(g) + 3H₂(g) ⇌ 2NH₃(g)", (("N₂", 1, "g"), ("H₂", 3, "g")), (("NH₃", 2, "g"),)),
    ("2SO₂(g) + O₂(g) ⇌ 2SO₃(g)", (("SO₂", 2, "g"), ("O₂", 1, "g")), (("SO₃", 2, "g"),)),
    ("N₂O₄(g) ⇌ 2NO₂(g)", (("N₂O₄", 1, "g"),), (("NO₂", 2, "g"),)),
    ("PCl₅(g) ⇌ PCl₃(g) + Cl₂(g)", (("PCl₅", 1, "g"),), (("PCl₃", 1, "g"), ("Cl₂", 1, "g"))),
    ("CO(g) + H₂O(g) ⇌ CO₂(g) + H₂(g)", (("CO", 1, "g"), ("H₂O", 1, "g")), (("CO₂", 1, "g"), ("H₂", 1, "g"))),
    ("CaCO₃(s) ⇌ CaO(s) + CO₂(g)", (("CaCO₃", 1, "s"),), (("CaO", 1, "s"), ("CO₂", 1, "g"))),
    ("C(s) + CO₂(g) ⇌ 2CO(g)", (("C", 1, "s"), ("CO₂", 1, "g")), (("CO", 2, "g"),)),
    ("Fe³⁺(aq) + SCN⁻(aq) ⇌ FeSCN²⁺(aq)", (("Fe³⁺", 1, "aq"), ("SCN⁻", 1, "aq")), (("FeSCN²⁺", 1, "aq"),)),
    ("2NO(g) + O₂(g) ⇌ 2NO₂(g)", (("NO", 2, "g"), ("O₂", 1, "g")), (("NO₂", 2, "g"),)),
    ("CH₃COOH(aq) + H₂O(l) ⇌ CH₃COO⁻(aq) + H₃O⁺(aq)", (("CH₃COOH", 1, "aq"), ("H₂O", 1, "l")),
     (("CH₃COO⁻", 1, "aq"), ("H₃O⁺", 1, "aq"))),
    ("2H₂(g) + O₂(g) ⇌ 2H₂O(g)", (("H₂", 2, "g"), ("O₂", 1, "g")), (("H₂O", 2, "g"),)),
    ("2NOCl(g) ⇌ 2NO(g) + Cl₂(g)", (("NOCl", 2, "g"),), (("NO", 2, "g"), ("Cl₂", 1, "g"))),
    ("Ag⁺(aq) + Cl⁻(aq) ⇌ AgCl(s)", (("Ag⁺", 1, "aq"), ("Cl⁻", 1, "aq")), (("AgCl", 1, "s"),)),
    ("NH₃(aq) + H₂O(l) ⇌ NH₄⁺(aq) + OH⁻(aq)", (("NH₃", 1, "aq"), ("H₂O", 1, "l")), (("NH₄⁺", 1, "aq"), ("OH⁻", 1, "aq"))),
    ("3Fe(s) + 4H₂O(g) ⇌ Fe₃O₄(s) + 4H₂(g)", (("Fe", 3, "s"), ("H₂O", 4, "g")), (("Fe₃O₄", 1, "s"), ("H₂", 4, "g"))),
)
CONCS = tuple(Fraction(x, 100) for x in (10, 20, 25, 40, 50, 80, 100, 150, 200, 250, 300, 400))


def counted(side):
    """Only gases and dissolved species appear in K."""
    return [s for s in side if s[2] in ("g", "aq")]


def k_value(system, conc: dict) -> Fraction:
    _, reactants, products = system
    value = Fraction(1)
    for f, c, _ in counted(products):
        value *= conc[f] ** c
    for f, c, _ in counted(reactants):
        value /= conc[f] ** c
    return value


def k_case(rng: Random, systems=K_SYSTEMS):
    def draw():
        system = rng.choice(systems)
        conc = {f: rng.choice(CONCS) for f, _, _ in counted(system[1]) + counted(system[2])}
        k = k_value(system, conc)
        return (system, conc, k) if exact(k) and Fraction(1, 100) <= k <= 10000 else None
    return _find(rng, draw)


def conc_text(conc: dict) -> str:
    return ", ".join(f"[{f}] = {show(v)}" for f, v in conc.items())


# ══ ม.5/9 — ค่าคงที่สมดุล ══════════════════════════════════════════════════════════


# ══ ม.5/10 — ความเข้มข้นที่ภาวะสมดุล ═══════════════════════════════════════════════


# ══ ม.5/11 — ปฏิกิริยาหลายขั้นตอน ════════════════════════════════════════════════════


# ══ ม.5/12 — หลักของเลอชาเตอลิเอ ═════════════════════════════════════════════════════


