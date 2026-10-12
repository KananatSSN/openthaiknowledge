"""ม.4 sets that the สสวท. books teach and the catalog did not have.

Basic track: three-set counting, logical equivalence and quantifiers, and
functions in use (cost and revenue, exponential models). Additional track: the
rest of ภาคตัดกรวย — only the circle existed — the distance from a point to a
line, triangle area from coordinates, and logarithms as the books apply them
(pH, decibels, earthquake magnitude, doubling time).

Answers that involve a root come from Pythagorean triples, so they are whole.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from otk.core.question import GeneratedQuestion
from otk.sets._support.math_p2 import _maths


def maths(stem: list, correct: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """``_maths`` that follows a numeric answer's named mistakes with its
    neighbours on both sides: four choices survive when two mistakes
    coincide, and the registry's rank balancing has values below the answer
    as well as above it to choose from."""
    wrongs = [w for w in dict.fromkeys(wrongs) if w != correct]
    try:
        v = Fraction(correct.replace("{,}", ""))
    except ValueError:
        v = None
    if v is not None:
        step = Fraction(1) if v.denominator == 1 else Fraction(1, 10 ** len(correct.split(".")[-1]))
        for k in (1, -1, 2, -2, 5, -5):
            cand = v + k * step
            if v >= 0 > cand:
                continue
            text_ = (str(cand.numerator) if cand.denominator == 1 else
                     format(Decimal(cand.numerator) / Decimal(cand.denominator), "f").rstrip("0"))
            if text_ != correct and text_ not in wrongs:
                wrongs.append(text_)
    return _maths(stem, correct, wrongs, topic)

M4 = {"th": "ม.4"}
M5 = {"th": "ม.5"}          # the registry level of ระยะทาง / สมการเส้นตรง / ลอการิทึม

_TRIPLES = ((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15),
            (12, 16, 20), (20, 21, 29))


def _sgn(n: int, first: bool = False) -> str:
    if first:
        return str(n)
    return f"+ {n}" if n >= 0 else f"- {-n}"


# ── เซต (ค 1.1 ม.4) ──────────────────────────────────────────────────────────


# ── ตรรกศาสตร์ (ค 1.1 ม.4) ───────────────────────────────────────────────────


# ── ฟังก์ชัน (ค 1.2 ม.4) ─────────────────────────────────────────────────────


# ── ภาคตัดกรวย (เพิ่มเติม ม.4) ───────────────────────────────────────────────


# ── เรขาคณิตวิเคราะห์ (เพิ่มเติม ม.4) ─────────────────────────────────────────


# ── ลอการิทึม (เพิ่มเติม ม.4) ────────────────────────────────────────────────

