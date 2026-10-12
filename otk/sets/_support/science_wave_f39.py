"""Wave F slice 39 — เคมีเพิ่มเติม 2: balancing redox equations, electrochemical
cells, and standard cell potentials.

Three ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 2 ม.5/27`` — balancing redox equations by oxidation number
  and by half-reactions;
* ``เคมีเพิ่มเติม 2 ม.5/28`` — the parts of a cell, the reactions at each
  electrode, and the cell diagram;
* ``เคมีเพิ่มเติม 2 ม.5/29`` — E°cell, and whether a cell is galvanic or
  electrolytic.

Every stored equation and half-equation is balanced in atoms and in charge,
and a test checks both.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.kit.answer_choices import show

SUBJECT = "เคมี"
UPPER_FIVE = {"th": "ม.5"}


# ══ ม.5/27 — ดุลสมการรีดอกซ์ ═══════════════════════════════════════════════════════


# ══ ม.5/28 — องค์ประกอบของเซลล์ ═════════════════════════════════════════════════════

# (metal, ion, E° in volts) for M^n+ + ne⁻ → M
COUPLES = (
    ("Mg", "Mg²⁺", Fraction(-237, 100)), ("Al", "Al³⁺", Fraction(-166, 100)), ("Zn", "Zn²⁺", Fraction(-76, 100)),
    ("Fe", "Fe²⁺", Fraction(-44, 100)), ("Ni", "Ni²⁺", Fraction(-25, 100)), ("Sn", "Sn²⁺", Fraction(-14, 100)),
    ("Pb", "Pb²⁺", Fraction(-13, 100)), ("Cu", "Cu²⁺", Fraction(34, 100)), ("Ag", "Ag⁺", Fraction(80, 100)),
    ("Au", "Au³⁺", Fraction(150, 100)),
)
CHARGE = {"Mg": 2, "Al": 3, "Zn": 2, "Fe": 2, "Ni": 2, "Sn": 2, "Pb": 2, "Cu": 2, "Ag": 1, "Au": 3}


def e_text(value: Fraction) -> str:
    return f"{'+' if value > 0 else '−' if value < 0 else ''}{show(abs(value))} V"


def pair(rng: Random):
    a, b = rng.sample(COUPLES, 2)
    anode, cathode = (a, b) if a[2] < b[2] else (b, a)
    return anode, cathode


def half(metal: str, ion: str, oxidation: bool) -> str:
    n = CHARGE[metal]
    e = "e⁻" if n == 1 else f"{n}e⁻"
    return f"{metal} → {ion} + {e}" if oxidation else f"{ion} + {e} → {metal}"


def diagram(anode, cathode) -> str:
    return f"{anode[0]}(s) | {anode[1]}(aq) || {cathode[1]}(aq) | {cathode[0]}(s)"


def potentials(anode, cathode) -> str:
    return f"E° ของ {anode[1]}/{anode[0]} = {e_text(anode[2])}, {cathode[1]}/{cathode[0]} = {e_text(cathode[2])}"


# ══ ม.5/29 — ศักย์ไฟฟ้ามาตรฐานของเซลล์ ══════════════════════════════════════════════


