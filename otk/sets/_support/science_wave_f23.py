"""Wave F slice 23 — เคมีเพิ่มเติม 1: molecular shape, forces between
molecules, network covalent solids, and metallic bonding.

Four ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 1 ม.4/17`` — molecular shape from VSEPR and the polarity of
  the molecule;
* ``เคมีเพิ่มเติม 1 ม.4/18`` — the kinds of force between covalent molecules,
  boiling points and solubility in water;
* ``เคมีเพิ่มเติม 1 ม.4/19`` — the properties of network covalent solids;
* ``เคมีเพิ่มเติม 1 ม.4/20`` — how the metallic bond forms and the properties
  of metals.

Boiling and melting points are textbook values at 1 atm in °C. A comparison is
only asked where the textbook rule and the measured values agree.
"""

from __future__ import annotations

from itertools import permutations
from random import Random

SUBJECT = "เคมี"
UPPER_FOUR = {"th": "ม.4"}


def _order_choices(rng: Random, order: tuple[str, ...]) -> tuple[str, tuple[str, ...]]:
    """The right high-to-low order and three other orders of the same names."""
    right = " > ".join(order)
    others = [" > ".join(p) for p in permutations(order) if p != order]
    return right, tuple(rng.sample(others, 3))


# ══ ม.4/17 — รูปร่างโมเลกุลและสภาพขั้ว ═══════════════════════════════════════════


# ══ ม.4/18 — แรงยึดเหนี่ยวระหว่างโมเลกุล ═════════════════════════════════════════


# ══ ม.4/19 — สารโคเวเลนต์โครงร่างตาข่าย ═══════════════════════════════════════════


# ══ ม.4/20 — พันธะโลหะ ═══════════════════════════════════════════════════════════


