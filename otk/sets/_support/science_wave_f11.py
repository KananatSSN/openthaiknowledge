"""Wave F slice 11 — ฟิสิกส์เพิ่มเติม 3: capacitors, static electricity at work,
and current as drifting electrons.

Three ``additional_outcome`` indicators, each filed whole:

* ``ฟิสิกส์เพิ่มเติม 3 ม.5/5`` — the parts of a capacitor, Q = CV, the energy it
  stores, and equivalent capacitance;
* ``ฟิสิกส์เพิ่มเติม 3 ม.5/6`` — static electricity in devices and everyday
  events;
* ``ฟิสิกส์เพิ่มเติม 3 ม.5/7`` — free electrons in a wire, I = Q/t, and the
  drift speed from I = nevA.

Capacitances are in microfarads; the electron density is 5 × 10²⁸ m⁻³ and
e = 1.6 × 10⁻¹⁹ C, so nevA = 8,000 A·s/m per mm² and every drift speed is
exact in millimetres per second.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_FIVE = {"th": "ม.5"}


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


# ══ ม.5/5 — ตัวเก็บประจุ ════════════════════════════════════════════════════════


# ══ ม.5/6 — ไฟฟ้าสถิตในชีวิตประจำวัน ═════════════════════════════════════════════


# ══ ม.5/7 — กระแสไฟฟ้าและความเร็วลอยเลื่อน ═══════════════════════════════════════


