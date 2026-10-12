"""Wave F slice 31 — เคมีเพิ่มเติม 2: multi-step stoichiometry, the limiting
reagent, and percent yield.

Three ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 2 ม.4/5`` — amounts through two or three reactions in a row;
* ``เคมีเพิ่มเติม 2 ม.4/6`` — the limiting reagent and the amounts it sets;
* ``เคมีเพิ่มเติม 2 ม.4/7`` — percent yield.

Single equations come from slice 30's balanced bank; the chains here are
balanced the same way and a test checks every atom count.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "เคมี"
UPPER_FOUR = {"th": "ม.4"}

QUARTERS = tuple(Fraction(k, 4) for k in range(1, 41))


# ══ ม.4/5 — หลายขั้นตอน ═══════════════════════════════════════════════════════════


# ══ ม.4/6 — สารกำหนดปริมาณ ═════════════════════════════════════════════════════════


# ══ ม.4/7 — ผลได้ร้อยละ ════════════════════════════════════════════════════════════


