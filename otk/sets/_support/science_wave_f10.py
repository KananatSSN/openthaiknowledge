"""Wave F slice 10 — ฟิสิกส์เพิ่มเติม 3: static charge, Coulomb's law, and the
electric field.

Three ``additional_outcome`` indicators, each filed whole, opening ``ฟิสิกส์ 3``:

* ``ฟิสิกส์เพิ่มเติม 3 ม.5/1`` — charging a neutral body by rubbing and by
  electrostatic induction;
* ``ฟิสิกส์เพิ่มเติม 3 ม.5/2`` — the electric force by Coulomb's law;
* ``ฟิสิกส์เพิ่มเติม 3 ม.5/3`` — the electric field, the force on a charge in
  it, and the resultant field of point charges added as vectors.

k = 9 × 10⁹ N·m²/C² and e = 1.6 × 10⁻¹⁹ C. Charges are in microcoulombs and
distances are drawn so every force and field comes out exact.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_FIVE = {"th": "ม.5"}

K = 9 * 10 ** 9
MICRO = Fraction(1, 10 ** 6)


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


def _charge(q: int) -> str:
    return f"{'+' if q > 0 else '−'}{abs(q)} μC"


# ══ ม.5/1 — การทำให้วัตถุมีประจุ ════════════════════════════════════════════════


# ══ ม.5/2 — กฎของคูลอมบ์ ════════════════════════════════════════════════════════


DISTANCES = tuple(Fraction(x, 100) for x in (3, 5, 10, 15, 20, 30, 50, 60, 90, 100, 150, 300))


# ══ ม.5/3 — สนามไฟฟ้า ═══════════════════════════════════════════════════════════


