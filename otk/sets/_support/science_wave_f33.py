"""Wave F slice 33 — เคมีเพิ่มเติม 2: rate graphs, reversible reactions, and
the approach to equilibrium.

Three ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 2 ม.5/1`` — reading how a measured substance rises or falls
  over time (the experiment itself is the student's; the graph is quizzed);
* ``เคมีเพิ่มเติม 2 ม.5/7`` — reversible reactions and dynamic equilibrium
  (the test itself is the student's; its meaning is quizzed);
* ``เคมีเพิ่มเติม 2 ม.5/8`` — concentrations and forward and reverse rates
  from the start until equilibrium.

Every data table is generated with shrinking steps, as a real run slows.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

SUBJECT = "เคมี"
UPPER_FIVE = {"th": "ม.5"}


# ══ ม.5/1 — กราฟการเปลี่ยนแปลงของสารที่วัด ═══════════════════════════════════════════


# ══ ม.5/7 — ปฏิกิริยาผันกลับได้และภาวะสมดุล ═══════════════════════════════════════════


# ══ ม.5/8 — ความเข้มข้นและอัตราจนถึงภาวะสมดุล ════════════════════════════════════════

def approach_table(rng: Random):
    """[A] falls and [B] rises (A ⇌ B) in shrinking steps, then both hold."""
    # Each step is start ÷ 20, so starts are chosen to keep every value exact to two places.
    start = rng.choice((Fraction(1), Fraction(2), Fraction(6, 5), Fraction(4, 5), Fraction(2, 5), Fraction(3)))
    steps = rng.choice(((4, 2, 1, 0, 0), (5, 3, 1, 0, 0, 0), (6, 3, 2, 1, 0, 0), (3, 2, 1, 1, 0, 0)))
    unit = start / 20
    gap = rng.choice((5, 10, 15, 20, 30))
    times = [0]
    a, b = [start], [Fraction(0)]
    for s in steps:
        times.append(times[-1] + gap)
        a.append(a[-1] - s * unit)
        b.append(b[-1] + s * unit)
    return times, a, b


