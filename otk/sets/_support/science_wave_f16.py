"""Wave F slice 16 — ฟิสิกส์เพิ่มเติม 4: gases, the kinetic theory, the first
law of thermodynamics, and Planck and Bohr.

Four ``additional_outcome`` indicators, each filed whole:

* ``ฟิสิกส์เพิ่มเติม 4 ม.6/7`` — the ideal gas laws;
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/8`` — the ideal gas model, kinetic theory, and the rms
  speed of gas molecules;
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/9`` — work done by a gas at constant pressure, and
  heat, internal energy and work;
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/10`` — Planck's hypothesis, Bohr's atom, and the
  hydrogen spectrum.

R = 8.31 J/mol·K, k = 1.38 × 10⁻²³ J/K, h = 6.6 × 10⁻³⁴ J·s; the hydrogen
levels are the textbook's rounded −13.6, −3.4, −1.51, −0.85 and −0.54 eV.
"""

from __future__ import annotations

from fractions import Fraction

from otk.kit.answer_choices import show

SUBJECT = "ฟิสิกส์"
UPPER_SIX = {"th": "ม.6"}

SUPERSCRIPT = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


def _sci(mantissa, exponent: int) -> str:
    return f"{show(mantissa)} × 10{str(exponent).translate(SUPERSCRIPT)}"


# ══ ม.6/7 — กฎของแก๊ส ═══════════════════════════════════════════════════════════


# ══ ม.6/8 — ทฤษฎีจลน์ของแก๊ส ═════════════════════════════════════════════════════

# (pressure in kPa, density in kg/m³, rms speed in m/s) with v² = 3P/ρ.
PRESSURE_DENSITY = ((100, Fraction(6, 5), 500), (100, Fraction(3, 10), 1000), (100, Fraction(24, 5), 250),
                    (200, Fraction(12, 5), 500), (200, Fraction(3, 5), 1000),
                    (50, Fraction(3, 5), 500), (150, Fraction(9, 5), 500))
assert all(3 * p * 1000 / rho == v * v for p, rho, v in PRESSURE_DENSITY)


# ══ ม.6/9 — งาน ความร้อน และพลังงานภายใน ════════════════════════════════════════


# ══ ม.6/10 — พลังค์และโบร์ ═══════════════════════════════════════════════════════


