"""Wave F slice 14 — ฟิสิกส์เพิ่มเติม 3 and 4: transformers and three-phase
power, electromagnetic waves and polarisation, communication, and heat.

Four ``additional_outcome`` indicators, each filed whole:

* ``ฟิสิกส์เพิ่มเติม 3 ม.6/6`` — three-phase generators and transformers;
* ``ฟิสิกส์เพิ่มเติม 3 ม.6/7`` — electromagnetic waves, polarised light and
  polaroids, and devices across the spectrum;
* ``ฟิสิกส์เพิ่มเติม 3 ม.6/8`` — communication by electromagnetic waves, analog
  against digital signals;
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/1`` — heat that changes temperature or state, and
  heat exchange under conservation of energy.

Malus's law uses the stated cos² values of 60°, 37° and 53°. Water has
c = 4,200 J/kg·K, ice melts at 336,000 J/kg, and every draw keeps the answer
exact.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_SIX = {"th": "ม.6"}


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


# ══ ฟิสิกส์ 3 ม.6/6 — หม้อแปลงและไฟฟ้า 3 เฟส ═══════════════════════════════════════


# ══ ฟิสิกส์ 3 ม.6/7 — คลื่นแม่เหล็กไฟฟ้าและโพลาไรเซชัน ═══════════════════════════════


# ══ ฟิสิกส์ 3 ม.6/8 — การสื่อสาร ═══════════════════════════════════════════════════


# ══ ฟิสิกส์ 4 ม.6/1 — ความร้อน ═══════════════════════════════════════════════════


