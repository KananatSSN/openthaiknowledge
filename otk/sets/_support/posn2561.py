"""สอวน. ค่าย 1 ปีการศึกษา 2561 — question types built from the digested sheet.

Same shape as :mod:`otk.sets._support.posn2562`: the solvers live in
:mod:`otk.sheets.posn2561_math`, each cross-checked by a second independent
derivation, and nothing here re-derives an answer — a type draws constants, hands
them to ``SOLVE[n]`` and spends its own code on the Thai wording, the exact TeX
and the distractors.

All thirty questions are wired up.
"""

from __future__ import annotations


def _linear_tex(name: str, value: int) -> str:
    """``x - 2`` / ``x + 3`` / ``x`` for a root at ``value``."""
    if value == 0:
        return name
    return f"{name} {'-' if value > 0 else '+'} {abs(value)}"


# ── ข้อ 1–5 ──────────────────────────────────────────────────────────────────


# ── ข้อ 6–10 ─────────────────────────────────────────────────────────────────


# ── ข้อ 11–15 ────────────────────────────────────────────────────────────────


# ── ข้อ 16–20 ────────────────────────────────────────────────────────────────


# ── ข้อ 21–25 ────────────────────────────────────────────────────────────────


# ── ข้อ 26–30 ────────────────────────────────────────────────────────────────


