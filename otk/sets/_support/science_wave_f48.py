"""Wave F slice 48 — cellular respiration, and Mendel.

Three ``additional_outcome`` indicators, each filed whole:

* ``ชีววิทยาเพิ่มเติม 1 ม.4/17`` — respiration with enough oxygen and without;
* ``ชีววิทยาเพิ่มเติม 2 ม.4/1`` — Mendel's pea experiments and their results;
* ``ชีววิทยาเพิ่มเติม 2 ม.4/2`` — segregation, independent assortment, and the
  chance of each genotype and phenotype in F₁ and F₂.

Cross probabilities are worked out by listing every gamete pairing, and shown
as fractions in lowest terms.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

SUBJECT = "ชีวะ"
UPPER_FOUR = {"th": "ม.4"}

# ══ ชีววิทยาเพิ่มเติม 1 ม.4/17 — การหายใจระดับเซลล์ ═══════════════════════════════════


# ══ ชีววิทยาเพิ่มเติม 2 ม.4/1 — การทดลองของเมนเดล ═══════════════════════════════════


# ══ ชีววิทยาเพิ่มเติม 2 ม.4/2 — กฎของเมนเดล ═════════════════════════════════════════


def gametes(genotype: str) -> list[str]:
    pairs = [genotype[i:i + 2] for i in range(0, len(genotype), 2)]
    return ["".join(p) for p in product(*pairs)]


def offspring(p1: str, p2: str) -> dict[str, Fraction]:
    counts: dict[str, int] = {}
    g1, g2 = gametes(p1), gametes(p2)
    for x in g1:
        for y in g2:
            child = "".join("".join(sorted(a + b, key=lambda ch: (ch.islower(), ch))) for a, b in zip(x, y))
            counts[child] = counts.get(child, 0) + 1
    total = len(g1) * len(g2)
    return {k: Fraction(v, total) for k, v in counts.items()}


def frac_text(x: Fraction) -> str:
    return "0" if x == 0 else ("1" if x == 1 else f"{x.numerator}/{x.denominator}")


