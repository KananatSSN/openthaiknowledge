"""Wave F slice 13 — ฟิสิกส์เพิ่มเติม 3: motors and meters, induction, and
alternating current.

Three ``additional_outcome`` indicators, each filed whole:

* ``ฟิสิกส์เพิ่มเติม 3 ม.6/3`` — how a galvanometer and a DC motor work, with
  the torque on a coil, meter conversions and the motor's back emf;
* ``ฟิสิกส์เพิ่มเติม 3 ม.6/4`` — induced emf, Faraday's law and Lenz's law, and
  induction in everyday devices;
* ``ฟิสิกส์เพิ่มเติม 3 ม.6/5`` — rms voltage and current.

Peak values that carry √2 are written with the root, as the textbook does, so
every numeric answer stays exact.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_SIX = {"th": "ม.6"}


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


# ══ ม.6/3 — แกลแวนอมิเตอร์และมอเตอร์ ═════════════════════════════════════════════


# ══ ม.6/4 — อีเอ็มเอฟเหนี่ยวนำ ═══════════════════════════════════════════════════


# ══ ม.6/5 — ค่าอาร์เอ็มเอส ═══════════════════════════════════════════════════════


