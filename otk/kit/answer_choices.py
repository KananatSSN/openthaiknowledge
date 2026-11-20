"""Choice builders most science sets use.

* ``_labelled`` — a question whose choices are labels: the right one and a pool
  of wrong ones (``label_pool`` picks among them);
* ``numeric`` — a computed answer with its unit, offered beside the listed
  slips and then factor slips on both sides, exact to two places;
* ``show`` — a number written the way the stems print it.

It also keeps the physics constants the motion sets were built with: ``G = 10``
and the subject and level they are filed under. (Formerly the support part of
Wave F slice 3, ฟิสิกส์เพิ่มเติม 1 motion, forces, work and power.)
"""

from __future__ import annotations

from fractions import Fraction

from otk.core.content import text
from otk.core.distractors import fixed, label_pool
from otk.core.question import GeneratedQuestion

SUBJECT = "ฟิสิกส์"
UPPER_FOUR = {"th": "ม.4"}

G = 10


def show(x) -> str:
    value = float(x)
    if value == int(value):
        return f"{int(value):,}"
    return f"{value:,.2f}".rstrip("0").rstrip(".")


_SUPERSCRIPT = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def exact(x) -> str:
    """A number as stem text that never rounds, unlike ``show``.

    A short decimal when one is exact (``0.25``, ``1,200``), a power of ten for
    a small terminating value (``3×10⁻⁵``), otherwise a fraction (``2/3``).
    Floats are read as the nearest simple fraction, so pass a ``Fraction``
    when the value is not a short decimal.
    """
    value = Fraction(x) if not isinstance(x, float) else Fraction(x).limit_denominator(10**9)
    if (value * 100).denominator == 1:
        return show(value)
    power, scaled = 0, value
    while scaled.denominator != 1 and power < 12:
        power, scaled = power + 1, scaled * 10
    if scaled.denominator == 1 and abs(scaled) < 10:
        return f"{scaled}×10{str(-power).translate(_SUPERSCRIPT)}"
    if scaled.denominator == 1:
        return f"{float(value):,.{power}f}"
    sign = "-" if value < 0 else ""
    return f"{sign}{abs(value.numerator)}/{value.denominator}"


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...], topic: str,
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)], correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]), topic=topic, hint=[text(hint)],
    )


def numeric(*, stem: str, answer, wrongs, unit: str, topic: str, hint: str,
            allow_negative: bool = False) -> GeneratedQuestion:
    """Distinct values: the listed slips first, then factor slips on both sides.

    The registry's rank balancing chooses among them, so the answer is not
    always the smallest just because every listed slip overshoots.
    """
    answer = Fraction(answer)
    # Every answer must be exact as shown; a repeating decimal would be marked
    # right only to two places.
    assert (answer * 100).denominator == 1, (stem, answer)
    seen = [answer]
    slips = [answer / 2, answer * 2, answer - 1, answer + 1, answer / 10, answer * 10,
             answer - 2, answer + 2, answer * 3, answer + 5]
    for w in [*wrongs, *(s for s in slips if (s * 100).denominator == 1)]:
        w = Fraction(w)
        if (w > 0 or (allow_negative and w != 0)) and show(w) not in {show(s) for s in seen}:
            seen.append(w)
    return GeneratedQuestion(
        stem=[text(stem)], correct=[text(f"{show(seen[0])} {unit}".strip())],
        distractors=fixed(*[[text(f"{show(w)} {unit}".strip())] for w in seen[1:]]),
        topic=topic, hint=[text(hint)],
    )


# ══ ม.4/3 — การเคลื่อนที่แนวตรงด้วยความเร่งคงตัว ═══════════════════════════════


# ══ ม.4/4 — แรงลัพธ์ของแรงสองแรงที่ทำมุมต่อกัน ═══════════════════════════════════


# ══ ม.4/5 — กฎการเคลื่อนที่ของนิวตันและการนำไปใช้ ═══════════════════════════════════


# ══ ม.4/10 — งานและกำลัง ════════════════════════════════════════════════════════


