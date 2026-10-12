"""ม.2 sets that the สสวท. books teach and the catalog did not have.

ม.2's exponent and polynomial work is deep already. What was missing is the
applied half of the grade: Pythagoras in a ladder, a screen or a walk; cube
roots; the surface area of prisms and cylinders (only a cylinder's volume
existed); and the chapter สถิติ with its แผนภาพจุด, แผนภาพต้น-ใบ and grouped
frequency. This module adds them in book order. Circles use π ≈ 22/7 with
radii that keep answers whole.
"""

from __future__ import annotations

from random import Random

LEVEL = {"th": "ม.2"}

_TRIPLES = ((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41))


def triple(rng: Random, k_hi: int = 5) -> tuple[int, int, int]:
    a, b, c = rng.choice(_TRIPLES)
    k = rng.randint(1, k_hi)
    return a * k, b * k, c * k


# ── ทฤษฎีบทพีทาโกรัส (ค 2.2 ม.2) ──────────────────────────────────────────────


# ── จำนวนจริง (ค 1.1 ม.2) ────────────────────────────────────────────────────


# ── พื้นที่ผิวและปริมาตร (ค 2.1 ม.2) ─────────────────────────────────────────


# ── สถิติ (ค 3.1 ม.2) ────────────────────────────────────────────────────────


