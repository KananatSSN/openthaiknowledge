"""Wave F slice 24 — เคมีเพิ่มเติม 1: comparing bond types, and the simple and
combined gas laws.

Three ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 1 ม.4/21`` — comparing ionic compounds, covalent substances
  and metals, and their uses;
* ``เคมีเพิ่มเติม 1 ม.5/1`` — Boyle's, Charles's and Gay-Lussac's laws;
* ``เคมีเพิ่มเติม 1 ม.5/2`` — the combined gas law.

Every gas temperature is a whole number of kelvin shown in °C (K − 273), and
every draw is kept only when the answer is exact to two places.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

SUBJECT = "เคมี"
UPPER_FIVE = {"th": "ม.5"}


# ══ ม.4/21 — เปรียบเทียบสารประกอบไอออนิก สารโคเวเลนต์ และโลหะ ═══════════════════════


# ══ ม.5/1 — กฎของบอยล์ ชาร์ล และเกย์-ลูสแซก ══════════════════════════════════════════

KELVINS = (200, 250, 273, 275, 300, 320, 325, 350, 373, 375, 400, 450, 500, 546, 600)
ATMS = tuple(Fraction(n, 10) for n in (5, 8, 10, 12, 15, 20, 25, 30, 40, 50))


def exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


def _find(rng: Random, draw):
    """Redraw until ``draw`` returns a case; every case here comes up often."""
    for _ in range(5000):
        case = draw()
        if case is not None:
            return case
    raise AssertionError("no exact case")


def celsius(kelvin: int) -> str:
    return f"{kelvin - 273} °C"


def _volume(rng: Random):
    """A volume in L or mL, as (value, unit)."""
    if rng.random() < 0.5:
        return rng.randint(1, 30), "L"
    return rng.randrange(50, 1001, 50), "mL"


# ══ ม.5/2 — กฎรวมแก๊ส ═══════════════════════════════════════════════════════════


