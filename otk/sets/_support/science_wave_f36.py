"""Wave F slice 36 — เคมีเพิ่มเติม 2: strength of acids and bases, pH,
neutralisation, and salt hydrolysis.

Four ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 2 ม.5/16`` — percent ionisation, Ka, and comparing strength;
* ``เคมีเพิ่มเติม 2 ม.5/17`` — pH, [H₃O⁺] and [OH⁻];
* ``เคมีเพิ่มเติม 2 ม.5/18`` — neutralisation and whether the mixture ends
  acidic, basic or neutral;
* ``เคมีเพิ่มเติม 2 ม.5/19`` — salt hydrolysis.

Logarithms come with the question, as the textbook gives them (log 2 = 0.30,
log 3 = 0.48, log 5 = 0.70), so every pH is exact. Small numbers are shown
as a × 10⁻ⁿ, and a question about one asks for a with n given.
"""

from __future__ import annotations

from fractions import Fraction

from otk.kit.answer_choices import show

SUBJECT = "เคมี"
UPPER_FIVE = {"th": "ม.5"}

SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
LOGS = {1: Fraction(0), 2: Fraction(30, 100), 3: Fraction(48, 100), 4: Fraction(60, 100), 5: Fraction(70, 100),
        6: Fraction(78, 100), 8: Fraction(90, 100)}
LOG_TEXT = {1: "", 2: "log 2 = 0.30", 3: "log 3 = 0.48", 4: "log 2 = 0.30", 5: "log 5 = 0.70",
            6: "log 2 = 0.30, log 3 = 0.48", 8: "log 2 = 0.30"}


def sci(value: Fraction) -> tuple[Fraction, int]:
    """value = mantissa × 10^power, with 1 ≤ mantissa < 10."""
    power = 0
    while value >= 10:
        value /= 10
        power += 1
    while value < 1:
        value *= 10
        power -= 1
    return value, power


def sci_text(value: Fraction) -> str:
    mantissa, power = sci(value)
    if power >= -1:
        return show(value)
    return f"{show(mantissa)} × 10{str(power).translate(SUP)}"


def ph_of(conc: Fraction) -> Fraction:
    """pH (or pOH) = n − log a for conc = a × 10⁻ⁿ, a one of the tabled integers."""
    mantissa, power = sci(conc)
    return -power - LOGS[int(mantissa)]


def log_note(conc: Fraction) -> str:
    note = LOG_TEXT[int(sci(conc)[0])]
    return f" (กำหนด {note})" if note else ""


def tabled(conc: Fraction) -> bool:
    mantissa, _ = sci(conc)
    return mantissa.denominator == 1 and int(mantissa) in LOGS


# ══ ม.5/16 — ความแรงของกรดและเบส ═══════════════════════════════════════════════════


# ══ ม.5/17 — pH ═══════════════════════════════════════════════════════════════


# ══ ม.5/18 — ปฏิกิริยาสะเทิน ════════════════════════════════════════════════════════

ACIDIC, BASIC, NEUTRAL = "เป็นกรด", "เป็นเบส", "เป็นกลาง"


# ══ ม.5/19 — ไฮโดรลิซิสของเกลือ ═════════════════════════════════════════════════════


