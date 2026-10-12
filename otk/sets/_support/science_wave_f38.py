"""Wave F slice 38 — เคมีเพิ่มเติม 2: oxidation numbers, redox reactions, and
comparing reducing and oxidising strength.

Three ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 2 ม.5/24`` — oxidation numbers, and which reactions are
  redox;
* ``เคมีเพิ่มเติม 2 ม.5/25`` — reducing and oxidising agents and the two half
  reactions;
* ``เคมีเพิ่มเติม 2 ม.5/26`` — which metal or halogen is the stronger
  reducing or oxidising agent, from what is seen (the experiment is the
  student's; reading its result is quizzed).

Oxidation numbers are worked out from the formula by the textbook rules, and
a test checks every tabled answer against that working.
"""

from __future__ import annotations

import re
from fractions import Fraction

SUBJECT = "เคมี"
UPPER_FIVE = {"th": "ม.5"}

UNSUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUPER = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "0123456789+-")
FIXED = {"O": -2, "H": 1, "F": -1, "Cl": -1, "Li": 1, "Na": 1, "K": 1, "Mg": 2, "Ca": 2, "Ba": 2, "Al": 3}


def parse(formula: str) -> tuple[dict[str, int], int]:
    """Atom counts and overall charge of a formula such as Cr₂O₇²⁻."""
    charge_text = re.search(r"([⁰¹²³⁴⁵⁶⁷⁸⁹]*[⁺⁻])$", formula)
    charge = 0
    body = formula
    if charge_text:
        raw = charge_text.group(1).translate(SUPER)
        charge = int(raw[:-1] or 1) * (1 if raw[-1] == "+" else -1)
        body = formula[: charge_text.start()]
    counts: dict[str, int] = {}
    for element, number in re.findall(r"([A-Z][a-z]?)(\d*)", body.translate(UNSUB)):
        counts[element] = counts.get(element, 0) + int(number or 1)
    return counts, charge


def oxidation_number(formula: str, element: str) -> Fraction:
    """Solve Σ(count × ON) = charge for the one element not fixed by the rules."""
    counts, charge = parse(formula)
    fixed = dict(FIXED)
    if formula in ("H₂O₂",):
        fixed["O"] = -1
    if formula in ("NaH",):
        fixed["H"] = -1
    known = sum(fixed[e] * n for e, n in counts.items() if e != element)
    return Fraction(charge - known, counts[element])


# ══ ม.5/24 — เลขออกซิเดชัน ═════════════════════════════════════════════════════════


# ══ ม.5/25 — ตัวรีดิวซ์ ตัวออกซิไดส์ และครึ่งปฏิกิริยา ══════════════════════════════════


# ══ ม.5/26 — เปรียบเทียบความสามารถเป็นตัวรีดิวซ์/ตัวออกซิไดส์ ══════════════════════════════


