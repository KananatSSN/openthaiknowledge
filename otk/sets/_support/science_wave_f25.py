"""Wave F slice 25 — เคมีเพิ่มเติม 1: Avogadro's law and the ideal gas law,
Dalton's law, Graham's law, and gases at work.

Four ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 1 ม.5/3`` — Avogadro's law and PV = nRT, including molar
  mass;
* ``เคมีเพิ่มเติม 1 ม.5/4`` — partial pressures in a mixture;
* ``เคมีเพิ่มเติม 1 ม.5/5`` — diffusion and Graham's law;
* ``เคมีเพิ่มเติม 1 ม.5/6`` — the gas laws applied to diving, air bags and hot
  air balloons.

R is the textbook's 0.0821 L·atm/(mol·K) and a mole of gas at STP takes
22.4 L. Every draw is kept only when the answer is exact to two places.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "เคมี"
UPPER_FIVE = {"th": "ม.5"}

STP_VOLUME = Fraction(224, 10)
QUARTERS = tuple(Fraction(k, 4) for k in range(1, 21))
# formula: (Thai name, molar mass)
GASES = {
    "H₂": ("ไฮโดรเจน", 2), "He": ("ฮีเลียม", 4), "CH₄": ("มีเทน", 16), "NH₃": ("แอมโมเนีย", 17),
    "Ne": ("นีออน", 20), "N₂": ("ไนโตรเจน", 28), "O₂": ("ออกซิเจน", 32), "Ar": ("อาร์กอน", 40),
    "CO₂": ("คาร์บอนไดออกไซด์", 44), "SO₂": ("ซัลเฟอร์ไดออกไซด์", 64), "Cl₂": ("คลอรีน", 71),
    "HI": ("ไฮโดรเจนไอโอไดด์", 128), "Br₂": ("โบรมีน", 160),
}


# Bromine is a liquid at room temperature, so it only appears as a vapour in diffusion.
STABLE_GASES = tuple(f for f in GASES if f != "Br₂")


def gas(formula: str) -> str:
    return f"แก๊ส{GASES[formula][0]} ({formula})"


# ══ ม.5/3 — กฎของอาโวกาโดรและกฎแก๊สอุดมคติ ═══════════════════════════════════════


# ══ ม.5/4 — กฎความดันย่อยของดอลตัน ════════════════════════════════════════════


# ══ ม.5/5 — กฎการแพร่ผ่านของเกรแฮม ═══════════════════════════════════════════════


SPEEDS = tuple(Fraction(x, 4) for x in (2, 3, 5, 6, 8, 10, 12, 16))


# ══ ม.5/6 — การประยุกต์ใช้กฎของแก๊ส ══════════════════════════════════════════════


