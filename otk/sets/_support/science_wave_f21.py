"""Wave F slice 21 — เคมีเพิ่มเติม 1: ionic compounds.

Four ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 1 ม.4/10`` — writing and naming ionic formulas;
* ``เคมีเพิ่มเติม 1 ม.4/11`` — energy of forming an ionic compound from the
  Born-Haber cycle;
* ``เคมีเพิ่มเติม 1 ม.4/12`` — properties of ionic compounds;
* ``เคมีเพิ่มเติม 1 ม.4/13`` — ionic and net ionic equations.

Formulas are built from ion charges, so a formula, its name and its
precipitate are always consistent with one another.
"""

from __future__ import annotations

from math import gcd

SUBJECT = "เคมี"
UPPER_FOUR = {"th": "ม.4"}

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")

# (formula part, Thai name, charge, polyatomic?)
CATIONS = (
    ("Na", "โซเดียม", 1, False), ("K", "โพแทสเซียม", 1, False), ("Li", "ลิเทียม", 1, False),
    ("NH₄", "แอมโมเนียม", 1, True), ("Ag", "ซิลเวอร์", 1, False), ("Mg", "แมกนีเซียม", 2, False),
    ("Ca", "แคลเซียม", 2, False), ("Ba", "แบเรียม", 2, False), ("Zn", "ซิงก์", 2, False),
    ("Al", "อะลูมิเนียม", 3, False), ("Fe", "เหล็ก(II)", 2, False), ("Fe", "เหล็ก(III)", 3, False),
    ("Cu", "คอปเปอร์(I)", 1, False), ("Cu", "คอปเปอร์(II)", 2, False), ("Pb", "เลด(II)", 2, False),
)
ANIONS = (
    ("Cl", "คลอไรด์", 1, False), ("Br", "โบรไมด์", 1, False), ("I", "ไอโอไดด์", 1, False), ("F", "ฟลูออไรด์", 1, False),
    ("O", "ออกไซด์", 2, False), ("S", "ซัลไฟด์", 2, False), ("N", "ไนไตรด์", 3, False),
    ("OH", "ไฮดรอกไซด์", 1, True), ("NO₃", "ไนเตรต", 1, True), ("SO₄", "ซัลเฟต", 2, True),
    ("CO₃", "คาร์บอเนต", 2, True), ("PO₄", "ฟอสเฟต", 3, True), ("HCO₃", "ไฮโดรเจนคาร์บอเนต", 1, True),
)


def _part(symbol: str, count: int, poly: bool) -> str:
    if count == 1:
        return symbol
    return f"({symbol}){str(count).translate(SUB)}" if poly else f"{symbol}{str(count).translate(SUB)}"


def formula(cation, anion) -> str:
    p, q = cation[2], anion[2]
    k = gcd(p, q)
    return _part(cation[0], q // k, cation[3]) + _part(anion[0], p // k, anion[3])


def name(cation, anion) -> str:
    return f"{cation[1]}{anion[1]}" if "(" not in cation[1] else f"{cation[1]} {anion[1]}"


def ion(entry, sign: int) -> str:
    size = "" if entry[2] == 1 else str(entry[2])
    return f"{entry[0]}{(size + ('+' if sign > 0 else '-')).translate(SUP)}"


def _pairs():
    # Nitride only with the group 1 and 2 metals; no ammonium nitride or silver nitride.
    return [(c, a) for c in CATIONS for a in ANIONS
            if not (a[0] == "N" and c[0] not in ("Li", "Na", "Mg", "Ca"))]


# ══ ม.4/10 — สูตรและชื่อสารประกอบไอออนิก ═════════════════════════════════════════


# ══ ม.4/11 — วัฏจักรบอร์น-ฮาเบอร์ ════════════════════════════════════════════════


# ══ ม.4/12 — สมบัติของสารประกอบไอออนิก ═══════════════════════════════════════════


# ══ ม.4/13 — สมการไอออนิกสุทธิ ═══════════════════════════════════════════════════


