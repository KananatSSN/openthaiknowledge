"""More ชุดโจทย์ for the calculus and sequence arms.

Companion to :mod:`otk.sets._support.math_number`; see that module's docstring
for how these join the skill tree.

Every item is built backwards from an answer that is exact by construction — a
polynomial whose derivative is known before the question is written, an integral
whose bounds were chosen to make the value whole, a Pythagorean triple standing
in for a ladder. Nothing here evaluates a limit numerically and hopes.
"""

from __future__ import annotations

from random import Random

from otk.kit.math_problems import poly_tex


def _nonzero(rng: Random, lo: int, hi: int) -> int:
    return rng.choice([n for n in range(lo, hi + 1) if n])


def _signed(n: int) -> str:
    return f" + {n}" if n >= 0 else f" - {abs(n)}"


def _linear(a: int, b: int) -> str:
    """``3x - 4`` — the inner function of most chain-rule items."""
    return poly_tex((a, "x"), (b, ""))


# ── แคลคูลัส: ลิมิตและความต่อเนื่อง ───────────────────────────────────────────


# ── อนุพันธ์ ─────────────────────────────────────────────────────────────────


# ── ปริพันธ์ ─────────────────────────────────────────────────────────────────


# ── ลำดับและอนุกรม ───────────────────────────────────────────────────────────


