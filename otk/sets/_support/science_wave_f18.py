"""Wave F slice 18 — ฟิสิกส์เพิ่มเติม 4: binding energy, fission and fusion,
radiation at work and radiation safety, and particle physics.

Four ``additional_outcome`` indicators, each filed whole, closing
``ฟิสิกส์เพิ่มเติม``:

* ``ฟิสิกส์เพิ่มเติม 4 ม.6/15`` — the nuclear force, nuclear stability and
  binding energy;
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/16`` — fission and fusion, and the energy released;
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/17`` — uses of nuclear energy and radiation, their
  hazards, and protection;
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/18`` — particle physics research, the standard model,
  and what the research is used for.

Mass converts to energy at 1 u = 931 MeV. Quark charges are ±2/3 and ±1/3.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_SIX = {"th": "ม.6"}

U_MEV = 931


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


# ══ ม.6/15 — พลังงานยึดเหนี่ยว ═══════════════════════════════════════════════════


# ══ ม.6/16 — ฟิชชันและฟิวชัน ═══════════════════════════════════════════════════


# ══ ม.6/17 — ประโยชน์และการป้องกันรังสี ═══════════════════════════════════════════


# ══ ม.6/18 — ฟิสิกส์อนุภาค ═══════════════════════════════════════════════════════


