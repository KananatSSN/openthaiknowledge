"""Wave F slice 15 — ฟิสิกส์เพิ่มเติม 4: elasticity, surface tension and
viscosity, and fluids in motion.

Three ``additional_outcome`` indicators, each filed whole:

* ``ฟิสิกส์เพิ่มเติม 4 ม.6/2`` — elasticity of a rod: stress, strain and Young's
  modulus;
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/5`` — surface tension, and the viscous force of a
  liquid;
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/6`` — the ideal fluid, the continuity equation and
  Bernoulli's equation, and the devices they explain.

Stress is in megapascals (N/mm²) and strain in units of 10⁻³, so Young's
modulus in gigapascals is their quotient; g = 10 m/s² and water is
1,000 kg/m³.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_SIX = {"th": "ม.6"}


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


# ══ ม.6/2 — สภาพยืดหยุ่น ═════════════════════════════════════════════════════════


# ══ ม.6/5 — ความตึงผิวและความหนืด ═══════════════════════════════════════════════


# ══ ม.6/6 — ของไหลที่เคลื่อนที่ ═══════════════════════════════════════════════════


