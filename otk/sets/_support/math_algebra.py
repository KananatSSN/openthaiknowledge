"""More ชุดโจทย์ for the algebra, exponent and function arms.

Companion to :mod:`otk.sets._support.math_number`; see that module's docstring
for how these join the skill tree.

Everything is string-built from chosen integer roots and coefficients, the same
no-CAS discipline :mod:`otk.kit.math_problems` follows — the answer is known
before the problem is written, so it cannot be wrong.
"""

from __future__ import annotations

from random import Random


def _nonzero(rng: Random, lo: int, hi: int) -> int:
    return rng.choice([n for n in range(lo, hi + 1) if n])


def _signed(n: int) -> str:
    """' + 5' / ' - 5', for gluing onto a leading term."""
    return f" + {n}" if n >= 0 else f" - {abs(n)}"


def _pow(sym: str, e: int) -> str:
    """``x^{3}``, but ``x`` for e = 1 and ``1`` for e = 0 — nobody writes x^1."""
    if e == 0:
        return "1"
    return sym if e == 1 else f"{sym}^{{{e}}}"


def _surd(coef: int, radicand: int) -> str:
    """``3\\sqrt{6}``, with the coefficient dropped when it is 1."""
    lead = "" if coef == 1 else str(coef)
    return rf"{lead}\sqrt{{{radicand}}}"


# ── พีชคณิต ──────────────────────────────────────────────────────────────────


# ── เลขยกกำลังและกรณฑ์ ───────────────────────────────────────────────────────


# ── ฟังก์ชัน ─────────────────────────────────────────────────────────────────


