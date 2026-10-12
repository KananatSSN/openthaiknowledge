"""Wave F slice 30 — เคมีเพิ่มเติม 2: chemical equations and stoichiometry.

Four ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 2 ม.4/1`` — reading the symbols in an equation, and
  balancing;
* ``เคมีเพิ่มเติม 2 ม.4/2`` — amounts in a reaction from masses;
* ``เคมีเพิ่มเติม 2 ม.4/3`` — amounts from the concentration of a solution;
* ``เคมีเพิ่มเติม 2 ม.4/4`` — amounts from gas volumes.

Every equation is stored balanced and a test checks each atom count. Formula
masses are parsed from the formulas with the textbook's rounded atomic
masses. A gas at STP takes 22.4 dm³ per mole, and draws are kept only when
the answer is exact to two places.
"""

from __future__ import annotations

import re
from fractions import Fraction
from functools import lru_cache

SUBJECT = "เคมี"
UPPER_FOUR = {"th": "ม.4"}

ATOMIC = {"H": 1, "C": 12, "N": 14, "O": 16, "Na": 23, "Mg": 24, "Al": 27, "S": 32, "Cl": Fraction(71, 2),
          "K": 39, "Ca": 40, "Fe": 56, "Cu": Fraction(127, 2), "Zn": 65, "Ag": 108, "I": 127, "Ba": 137, "Pb": 207}
UNSUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
STP = Fraction(224, 10)


@lru_cache(maxsize=None)
def atoms(formula: str) -> tuple[tuple[str, int], ...]:
    text = formula.translate(UNSUB)
    stack = [{}]
    for token, number in re.findall(r"([A-Z][a-z]?|\(|\))(\d*)", text):
        count = int(number or 1)
        if token == "(":
            stack.append({})
        elif token == ")":
            group = stack.pop()
            for k, v in group.items():
                stack[-1][k] = stack[-1].get(k, 0) + v * count
        else:
            stack[-1][token] = stack[-1].get(token, 0) + count
    return tuple(sorted(stack[0].items()))


def mass_of(formula: str) -> Fraction:
    return sum((ATOMIC[k] * v for k, v in atoms(formula)), Fraction(0))


# (reactants, products): each a tuple of (coefficient, formula, state)
EQUATIONS = (
    (((2, "H₂", "g"), (1, "O₂", "g")), ((2, "H₂O", "l"),)),
    (((1, "N₂", "g"), (3, "H₂", "g")), ((2, "NH₃", "g"),)),
    (((1, "CH₄", "g"), (2, "O₂", "g")), ((1, "CO₂", "g"), (2, "H₂O", "l"))),
    (((1, "C₃H₈", "g"), (5, "O₂", "g")), ((3, "CO₂", "g"), (4, "H₂O", "l"))),
    (((2, "Mg", "s"), (1, "O₂", "g")), ((2, "MgO", "s"),)),
    (((4, "Al", "s"), (3, "O₂", "g")), ((2, "Al₂O₃", "s"),)),
    (((2, "Na", "s"), (2, "H₂O", "l")), ((2, "NaOH", "aq"), (1, "H₂", "g"))),
    (((1, "Zn", "s"), (2, "HCl", "aq")), ((1, "ZnCl₂", "aq"), (1, "H₂", "g"))),
    (((1, "Mg", "s"), (2, "HCl", "aq")), ((1, "MgCl₂", "aq"), (1, "H₂", "g"))),
    (((2, "Al", "s"), (6, "HCl", "aq")), ((2, "AlCl₃", "aq"), (3, "H₂", "g"))),
    (((1, "CaCO₃", "s"),), ((1, "CaO", "s"), (1, "CO₂", "g"))),
    (((2, "KClO₃", "s"),), ((2, "KCl", "s"), (3, "O₂", "g"))),
    (((1, "Fe₂O₃", "s"), (3, "CO", "g")), ((2, "Fe", "s"), (3, "CO₂", "g"))),
    (((2, "H₂O₂", "aq"),), ((2, "H₂O", "l"), (1, "O₂", "g"))),
    (((1, "CaCO₃", "s"), (2, "HCl", "aq")), ((1, "CaCl₂", "aq"), (1, "H₂O", "l"), (1, "CO₂", "g"))),
    (((2, "NaHCO₃", "s"),), ((1, "Na₂CO₃", "s"), (1, "H₂O", "g"), (1, "CO₂", "g"))),
    (((1, "C₂H₅OH", "l"), (3, "O₂", "g")), ((2, "CO₂", "g"), (3, "H₂O", "l"))),
    (((4, "NH₃", "g"), (5, "O₂", "g")), ((4, "NO", "g"), (6, "H₂O", "g"))),
    (((2, "C₄H₁₀", "g"), (13, "O₂", "g")), ((8, "CO₂", "g"), (10, "H₂O", "l"))),
    (((1, "Fe", "s"), (1, "CuSO₄", "aq")), ((1, "FeSO₄", "aq"), (1, "Cu", "s"))),
    (((1, "NaOH", "aq"), (1, "HCl", "aq")), ((1, "NaCl", "aq"), (1, "H₂O", "l"))),
    (((2, "NaOH", "aq"), (1, "H₂SO₄", "aq")), ((1, "Na₂SO₄", "aq"), (2, "H₂O", "l"))),
    (((1, "AgNO₃", "aq"), (1, "NaCl", "aq")), ((1, "AgCl", "s"), (1, "NaNO₃", "aq"))),
    (((1, "BaCl₂", "aq"), (1, "Na₂SO₄", "aq")), ((1, "BaSO₄", "s"), (2, "NaCl", "aq"))),
    (((1, "Pb(NO₃)₂", "aq"), (2, "KI", "aq")), ((1, "PbI₂", "s"), (2, "KNO₃", "aq"))),
    (((1, "Ca(OH)₂", "aq"), (2, "HCl", "aq")), ((1, "CaCl₂", "aq"), (2, "H₂O", "l"))),
)


def side_text(side, states: bool = False, blanks: bool = False) -> str:
    def one(coef, formula, state):
        lead = "__" if blanks else ("" if coef == 1 else str(coef))
        return f"{lead}{formula}" + (f"({state})" if states else "")
    return " + ".join(one(*x) for x in side)


def equation_text(eq, states: bool = False, blanks: bool = False) -> str:
    return f"{side_text(eq[0], states, blanks)} → {side_text(eq[1], states, blanks)}"


def species(eq):
    return [*eq[0], *eq[1]]


def verb(eq, formula: str) -> str:
    """Reactants are used up; products form."""
    return "ทำปฏิกิริยา" if any(f == formula for _, f, _ in eq[0]) else "เกิดขึ้น"


# ══ ม.4/1 — สมการเคมี ═════════════════════════════════════════════════════════


# ══ ม.4/2 — ปริมาณสารสัมพันธ์กับมวล ═══════════════════════════════════════════════


# ══ ม.4/3 — ปริมาณสารสัมพันธ์กับความเข้มข้น ══════════════════════════════════════════


# ══ ม.4/4 — ปริมาณสารสัมพันธ์กับปริมาตรแก๊ส ═══════════════════════════════════════════


